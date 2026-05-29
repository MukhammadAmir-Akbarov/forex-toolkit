#!/usr/bin/env python3
"""
Python ↔ MetaTrader 5 коннектор.

⚠️ ВНИМАНИЕ:
  1. Работает ТОЛЬКО на Windows. Пакет MetaTrader5 не поддерживает macOS/Linux.
  2. Использовать ТОЛЬКО на демо-счёте.
  3. Этот код — скелет. Перед реальным использованием нужно:
     - Установить MetaTrader 5 (Windows-приложение)
     - Войти в демо-счёт в самом терминале MT5
     - Установить пакет: pip install MetaTrader5
     - Запустить этот скрипт — он подключится к запущенному MT5

Что делает скелет:
  - Подключается к MT5
  - Скачивает последние 500 свечей H1 по выбранной паре
  - Применяет стратегию из bot/strategy.py
  - Печатает сигналы (НЕ открывает реальные ордера)

ЕСЛИ ХОЧЕШЬ автоматическую торговлю — это далеко не тривиально:
  - Нужна обработка ошибок (потеря соединения, проскальзывание, реджекты)
  - Логирование
  - Защита от двойных входов
  - Лимиты дня
  - Аварийные стопы
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# === Платформенная проверка ===
if sys.platform != "win32":
    print("⚠️  MetaTrader5 Python API работает только на Windows.")
    print("    Этот скрипт — образовательный. Для запуска:")
    print("    1. Перенеси проект на Windows-машину")
    print("    2. Установи MT5 (терминал)")
    print("    3. pip install MetaTrader5")
    print("    4. Запусти этот скрипт")
    sys.exit(0)

try:
    import MetaTrader5 as mt5
except ImportError:
    print("Пакет MetaTrader5 не установлен. Установи: pip install MetaTrader5")
    sys.exit(1)

import pandas as pd

# Добавляем bot/ в path для импорта стратегии
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bot"))
from strategy import detect_signals, prepare_dataframe  # noqa: E402


def connect(login: int | None = None, password: str | None = None,
            server: str | None = None) -> bool:
    """Подключение к запущенному терминалу MT5."""
    if login and password and server:
        ok = mt5.initialize(login=login, password=password, server=server)
    else:
        ok = mt5.initialize()

    if not ok:
        print(f"❌ Не удалось подключиться: {mt5.last_error()}")
        return False

    account_info = mt5.account_info()
    if account_info is None:
        print("❌ Не удалось получить информацию о счёте")
        return False

    # Проверка демо
    if account_info.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
        print("⚠️  ОПАСНО: счёт НЕ демо!")
        print(f"   Логин: {account_info.login}")
        print(f"   Сервер: {account_info.server}")
        print(f"   Баланс: {account_info.balance} {account_info.currency}")
        confirm = input("Точно продолжить на РЕАЛЬНОМ счёте? (введи 'YES'): ")
        if confirm != "YES":
            mt5.shutdown()
            return False

    print(f"✓ Подключён. Счёт #{account_info.login} "
          f"({account_info.balance:.2f} {account_info.currency})")
    return True


def fetch_ohlc(symbol: str = "EURUSD", timeframe: int = mt5.TIMEFRAME_H1,
               n_bars: int = 500) -> pd.DataFrame:
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_bars)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"Не удалось получить данные {symbol}")
    df = pd.DataFrame(rates)
    df["datetime"] = pd.to_datetime(df["time"], unit="s")
    df = df.set_index("datetime")
    df = df.rename(columns={
        "open": "open", "high": "high", "low": "low", "close": "close",
    })
    return df[["open", "high", "low", "close"]]


def scan_signals(symbol: str = "EURUSD") -> None:
    print(f"\n📊 Сканирую {symbol}…")
    df = fetch_ohlc(symbol)
    df = prepare_dataframe(df)
    signals = detect_signals(df)

    print(f"  Свечей: {len(df)}")
    print(f"  Сигналов всего за период: {len(signals)}")

    # Самые свежие сигналы (последние 5)
    recent = signals[-5:] if signals else []
    if not recent:
        print("  ❌ Сигналов в последних свечах нет.")
        return

    print("\nПоследние сигналы:")
    for s in recent:
        age_bars = len(df) - s.bar_index
        print(
            f"  • {s.timestamp}  {s.direction.value.upper()}  "
            f"вход={s.entry:.5f}  SL={s.stop:.5f}  TP={s.take:.5f}  "
            f"R:R=1:{s.rr:.1f}  ({age_bars} свечей назад)  [{s.reason}]"
        )

    if recent and len(df) - recent[-1].bar_index <= 1:
        print("\n🚨 СВЕЖИЙ СИГНАЛ! Проверь чек-лист перед открытием.")


def main() -> int:
    import argparse
    import os

    parser = argparse.ArgumentParser(description="MT5 connector + signal scanner")
    parser.add_argument("--symbol", default="EURUSD")
    parser.add_argument(
        "--login", type=int,
        help="MT5 login. Лучше задать через переменную окружения MT5_LOGIN.",
    )
    parser.add_argument(
        "--password",
        help="MT5 password. НЕБЕЗОПАСНО в CLI (попадает в историю shell). "
             "Используй переменную окружения MT5_PASSWORD.",
    )
    parser.add_argument(
        "--server",
        help="MT5 server. Лучше задать через переменную окружения MT5_SERVER.",
    )
    args = parser.parse_args()

    # Приоритет — переменные окружения; CLI-флаги только как override.
    login = args.login or (
        int(os.environ["MT5_LOGIN"]) if os.environ.get("MT5_LOGIN") else None
    )
    password = args.password or os.environ.get("MT5_PASSWORD")
    server = args.server or os.environ.get("MT5_SERVER")

    if args.password:
        print(
            "⚠️  Пароль передан через --password и теперь в истории shell. "
            "Безопаснее: export MT5_PASSWORD=… (или храни в .env, см. .env.example)."
        )

    if not connect(login, password, server):
        return 1

    try:
        scan_signals(args.symbol)
    finally:
        mt5.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
