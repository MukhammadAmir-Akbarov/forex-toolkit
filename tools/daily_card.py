#!/usr/bin/env python3
"""Карточка дня в Telegram — утренний повтор терминов из тренажёра.

Механика возврата в учебник: каждое утро в личку/канал приходит одна
карточка из tools/flashcards (front = термин, back = определение под
спойлером). Одна карточка в день не утомляет, а за квартал прогоняет весь
словарь — безо всякой силы воли.

Выбор детерминирован: день года % число карточек — всем подписчикам приходит
одна и та же, а тест воспроизводит отправку без сети.

Запуск:
    export TELEGRAM_BOT_TOKEN="123456:ABC..."
    export TELEGRAM_CHAT_ID="123456789"   # или @channel
    python tools/daily_card.py            # отправить сегодняшнюю
    python tools/daily_card.py --dry-run  # показать, не отправляя

cron (08:05 по местному):
    5 8 * * * cd /path/to/repo && /usr/bin/python3 tools/daily_card.py

Требования: stdlib + requests (есть в dev-зависимостях). Карточки парсятся из
_mkdocs/tools/flashcards.md — источник истины один, дублирования банка нет.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLASHCARDS = ROOT / "_mkdocs" / "tools" / "flashcards.md"
SITE_URL = "https://mukhammadamir-akbarov.github.io/forex-toolkit/tools/flashcards/"

# {front:"Pip",back:"…",tags:["forex","basic"]} — JS-литералы, не JSON:
# парсим терпимо к пробелам, но строго к структуре.
CARD_RE = re.compile(
    r'\{front:"(?P<front>(?:[^"\\]|\\.)*)",'
    r'back:"(?P<back>(?:[^"\\]|\\.)*)",'
    r"tags:\[(?P<tags>[^\]]*)\]\}",
)


def load_cards(path: Path = FLASHCARDS) -> list[dict]:
    """Карточки из JS-блока страницы flashcards."""
    text = path.read_text(encoding="utf-8")
    cards = []
    for match in CARD_RE.finditer(text):
        cards.append(
            {
                "front": json.loads(f'"{match.group("front")}"'),
                "back": json.loads(f'"{match.group("back")}"'),
                "tags": re.findall(r'"([^"]+)"', match.group("tags")),
            }
        )
    if not cards:
        raise RuntimeError(f"Не нашёл карточек в {path} — формат CARDS изменился?")
    return cards


def pick_card(cards: list[dict], day: dt.date | None = None) -> tuple[int, dict]:
    """Карточка дня: день года % N. Одинакова для всех в этот день."""
    day = day or dt.date.today()
    index = day.timetuple().tm_yday % len(cards)
    return index, cards[index]


def build_message(index: int, total: int, card: dict) -> str:
    """HTML-сообщение: термин открытым текстом, определение под спойлером."""
    front = html.escape(card["front"])
    back = html.escape(card["back"])
    return (
        f"🎴 <b>Карточка дня #{index + 1}</b> (из {total})\n\n"
        f"<b>{front}</b> — что это?\n\n"
        f"<tg-spoiler>{back}</tg-spoiler>\n\n"
        f'Повторить ещё: <a href="{SITE_URL}">тренажёр карточек</a>'
    )


def send_message(message: str, token: str, chat_id: str) -> None:
    import requests

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=10,
    )
    if not response.ok:
        raise RuntimeError(f"Telegram ответил {response.status_code}: {response.text}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dry-run", action="store_true", help="показать сообщение, не отправляя"
    )
    parser.add_argument(
        "--date",
        type=dt.date.fromisoformat,
        default=None,
        help="дата карточки (YYYY-MM-DD), по умолчанию — сегодня",
    )
    args = parser.parse_args()

    cards = load_cards()
    index, card = pick_card(cards, args.date)
    message = build_message(index, len(cards), card)

    if args.dry_run:
        print(message)
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        sys.exit(
            "❌ Задай TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID "
            "(см. docstring или advanced/SETUP-telegram.md)"
        )
    send_message(message, token, chat_id)
    print(f"✅ Карточка дня #{index + 1} отправлена: {card['front']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
