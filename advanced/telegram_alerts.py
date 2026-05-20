#!/usr/bin/env python3
"""
Telegram-бот для алертов о торговых сигналах.

Что делает:
  1. Каждый час (или по cron) скачивает свечи EUR/USD через yfinance
  2. Применяет стратегию из bot/strategy.py
  3. Если есть свежий сигнал — отправляет тебе в Telegram

Настройка:
  1. Создай бота через @BotFather в Telegram → получишь TOKEN
  2. Напиши /start своему боту → получи chat_id через @userinfobot
  3. Установи переменные:
     export TELEGRAM_BOT_TOKEN="123456:ABC..."
     export TELEGRAM_CHAT_ID="123456789"
  4. Запусти: python telegram_alerts.py
  5. Для автозапуска — добавь в cron (см. README в этой папке)
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bot"))
from strategy import detect_signals, prepare_dataframe  # noqa: E402


def send_telegram(message: str, token: str, chat_id: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }, timeout=10)
        return resp.ok
    except requests.RequestException as e:
        print(f"Ошибка Telegram: {e}", file=sys.stderr)
        return False


def fetch_data(symbol: str, days: int = 30):
    """Скачивает свечи H1 через yfinance."""
    import yfinance as yf
    yf_symbol = symbol.replace("USD", "USD=X").replace("USDUSD=X", "USD=X")
    if "=" not in yf_symbol:
        yf_symbol = symbol + "=X"

    ticker = yf.Ticker(yf_symbol)
    df = ticker.history(period=f"{days}d", interval="1h")
    if df.empty:
        raise RuntimeError(f"Не удалось скачать {symbol}")

    df.columns = [c.lower() for c in df.columns]
    return df[["open", "high", "low", "close"]]


def format_signal_message(symbol: str, signal) -> str:
    direction = "🟢 LONG" if signal.direction.value == "long" else "🔴 SHORT"
    return (
        f"*🚨 Forex Signal*\n\n"
        f"*Пара:* {symbol}\n"
        f"*Направление:* {direction}\n"
        f"*Время:* {signal.timestamp}\n\n"
        f"*Вход:* `{signal.entry:.5f}`\n"
        f"*Stop Loss:* `{signal.stop:.5f}` ({signal.stop_pips:.0f} пипсов)\n"
        f"*Take Profit:* `{signal.take:.5f}` (R:R 1:{signal.rr:.1f})\n\n"
        f"*Причина:* {signal.reason}\n\n"
        f"⚠️ _Это не торговая рекомендация. Проверь чек-лист перед входом._"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Telegram-бот для сигналов",
    )
    parser.add_argument("--symbol", default="EURUSD")
    parser.add_argument("--max-age-hours", type=int, default=2,
                        help="Сигналы свежее N часов (по умолч. 2)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Не отправлять в Telegram, только печатать")
    args = parser.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not args.dry_run and (not token or not chat_id):
        print("❌ Установи переменные:")
        print("  export TELEGRAM_BOT_TOKEN='your_token'")
        print("  export TELEGRAM_CHAT_ID='your_chat_id'")
        return 1

    print(f"📥 Скачиваю данные {args.symbol}…")
    try:
        df = fetch_data(args.symbol)
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

    print(f"  {len(df)} свечей, последняя: {df.index[-1]}")

    df = prepare_dataframe(df)
    signals = detect_signals(df)
    print(f"  Сигналов всего: {len(signals)}")

    if not signals:
        print("Свежих сигналов нет.")
        return 0

    # Фильтрация по свежести
    now = datetime.now()
    fresh = []
    for s in signals:
        age = now - s.timestamp.to_pydatetime().replace(tzinfo=None)
        if age <= timedelta(hours=args.max_age_hours):
            fresh.append(s)

    if not fresh:
        print(f"Сигналов за последние {args.max_age_hours} часов нет.")
        return 0

    print(f"📤 Отправляю {len(fresh)} свежих сигнала(ов)…")
    for s in fresh:
        msg = format_signal_message(args.symbol, s)
        if args.dry_run:
            print("\n--- DRY RUN ---")
            print(msg)
        else:
            ok = send_telegram(msg, token, chat_id)
            print(f"  {'✓' if ok else '✗'} {s.timestamp} {s.direction.value}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
