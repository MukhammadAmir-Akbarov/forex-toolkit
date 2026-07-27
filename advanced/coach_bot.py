#!/usr/bin/env python3
"""
Coach Bot — ежедневный Telegram-помощник по дисциплине.

Каждый день в 21:00 (или по cron) присылает 3-5 вопросов:
  - Как прошёл день?
  - Сколько было сделок?
  - Какая эмоция была главной?
  - Что вынес?

Сохраняет ответы в coach-log.csv для анализа.

Запуск:
  python advanced/coach_bot.py send
  python advanced/coach_bot.py receive
  python advanced/coach_bot.py analyze --csv journal/my-trades.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

from forex_toolkit.coach import analyze_trades, load_journal

LOG = Path(__file__).resolve().parent.parent / "coach-log.csv"
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "my-trades.csv"
HEADERS = ["date", "question", "answer"]

QUESTIONS = [
    "🤔 Как прошёл торговый день? (1-10)",
    "📊 Сколько сделок ты сегодня сделал?",
    "✅ Был ли хоть один отход от правил? Какой?",
    "💭 Какая эмоция была главной сегодня?",
    "📝 Главный урок дня в одной фразе:",
]


def ensure_log() -> None:
    if not LOG.exists():
        with open(LOG, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEADERS)


def send_telegram(message: str, token: str, chat_id: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }, timeout=10)
        return resp.ok
    except requests.RequestException:
        return False


def get_updates(token: str, offset: int | None = None) -> list[dict]:
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    try:
        resp = requests.get(url, params=params, timeout=35)
        return resp.json().get("result", [])
    except requests.RequestException:
        return []


def cmd_send(token: str, chat_id: str) -> int:
    """Отправляет вечернее сообщение."""
    today = datetime.now().strftime("%Y-%m-%d %A")
    message = (
        f"🌙 *Daily Coach Check-in*\n"
        f"_{today}_\n\n"
        f"Привет! Время вечерней рефлексии. "
        f"Ответь на эти вопросы (пиши прямо в чат):\n\n"
    )
    for i, q in enumerate(QUESTIONS, 1):
        message += f"*{i}.* {q}\n"
    message += (
        "\n💡 _Просто пиши ответы по очереди. "
        "Сохранится автоматически._"
    )

    if send_telegram(message, token, chat_id):
        print(f"✓ Отправлено в Telegram (chat {chat_id})")
        return 0
    else:
        print("❌ Не удалось отправить")
        return 1


def cmd_receive(token: str, chat_id: str, timeout_min: int = 60) -> int:
    """Принимает ответы long-polling до timeout."""
    ensure_log()
    print(f"📥 Слушаю ответы {timeout_min} минут (Ctrl+C для выхода)...")

    deadline = time.time() + timeout_min * 60
    offset = None
    answers = []
    today = datetime.now().strftime("%Y-%m-%d")

    while time.time() < deadline and len(answers) < len(QUESTIONS):
        updates = get_updates(token, offset)
        for upd in updates:
            offset = upd["update_id"] + 1
            msg = upd.get("message", {})
            if str(msg.get("chat", {}).get("id")) != str(chat_id):
                continue
            text = msg.get("text", "").strip()
            if not text:
                continue
            q_index = len(answers)
            if q_index >= len(QUESTIONS):
                break
            answers.append({
                "question": QUESTIONS[q_index],
                "answer": text,
            })
            print(f"  ✓ Ответ {q_index + 1}: {text[:60]}")
            send_telegram(
                f"✓ Записал ответ на вопрос {q_index + 1}\n\n"
                f"Осталось: {len(QUESTIONS) - len(answers)}",
                token, chat_id,
            )
            if len(answers) == len(QUESTIONS):
                break

    if answers:
        with open(LOG, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for a in answers:
                writer.writerow([today, a["question"], a["answer"]])
        print(f"\n✓ Сохранено {len(answers)} ответов в {LOG}")
        send_telegram(
            f"🎉 *Сессия завершена!*\n\n"
            f"Все {len(answers)} ответов сохранены. "
            f"До завтра!",
            token, chat_id,
        )
    else:
        print("Ответов не получено")
    return 0


def cmd_analyze_log() -> int:
    """Простая аналитика накопленных ответов."""
    if not LOG.exists():
        print("Логов пока нет")
        return 1

    with open(LOG, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("Логи пусты")
        return 1

    print(f"\n📊 Анализ Coach логов: {len(rows)} записей\n")

    # Дни
    dates = set(r["date"] for r in rows)
    print(f"Дней с ответами: {len(dates)}")

    # Последние 7 дней
    print("\n📅 Последние 7 ответов (если есть):")
    recent = rows[-7 * len(QUESTIONS):]
    for r in recent[-10:]:
        print(f"  [{r['date']}] {r['question'][:40]}")
        print(f"    → {r['answer'][:80]}")

    return 0


def cmd_analyze(csv_path: Path) -> int:
    """Build three personalized rules from a trading journal."""
    try:
        report = analyze_trades(load_journal(csv_path))
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Не удалось проанализировать журнал: {exc}")
        return 1

    print("\n" + "=" * 64)
    print("  PERSONAL COACH — 3 правила по торговому журналу")
    print("=" * 64)
    print(f"\nИсточник: {csv_path}")
    print(f"Закрытых сделок: {report.trade_count}")
    for index, rule in enumerate(report.rules, 1):
        print(f"\n{index}. {rule.title}")
        print(f"   Факт: {rule.evidence}")
        print(f"   Действие: {rule.action}")
    print()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily Coach Bot")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("send", help="Отправить вопросы в Telegram")
    p_recv = sub.add_parser("receive", help="Принять ответы (long-poll)")
    p_recv.add_argument("--timeout", type=int, default=60,
                        help="Сколько минут слушать (по умолч. 60)")
    p_analyze = sub.add_parser(
        "analyze",
        help="Выдать 3 персональных правила из CSV торгового журнала",
    )
    p_analyze.add_argument(
        "--csv",
        type=Path,
        default=JOURNAL,
        help="Путь к CSV журнала (по умолчанию journal/my-trades.csv)",
    )
    sub.add_parser("analyze-log", help="Показать накопленные ответы Coach")
    args = parser.parse_args()

    if args.cmd == "analyze":
        return cmd_analyze(args.csv)
    if args.cmd == "analyze-log":
        return cmd_analyze_log()

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("❌ Установи TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID")
        return 1

    if args.cmd == "send":
        return cmd_send(token, chat_id)
    elif args.cmd == "receive":
        return cmd_receive(token, chat_id, args.timeout)


if __name__ == "__main__":
    sys.exit(main())
