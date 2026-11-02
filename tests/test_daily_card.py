"""Карточка дня в Telegram: парсинг банка, детерминизм выбора, спойлер."""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from daily_card import build_message, load_cards, pick_card  # noqa: E402


def test_cards_are_parsed_from_the_flashcards_page():
    cards = load_cards()
    assert len(cards) >= 100, (
        f"нашлось только {len(cards)} карточек — формат CARDS на странице изменился?"
    )
    for card in cards:
        assert card["front"].strip() and card["back"].strip()
        assert card["tags"], f"у карточки {card['front']!r} нет тегов"


def test_pick_is_deterministic_and_covers_the_year():
    cards = load_cards()
    day = dt.date(2026, 11, 3)
    first = pick_card(cards, day)
    second = pick_card(cards, day)
    assert first == second, "выбор дня обязан быть воспроизводимым"
    # Разные дни — разные карточки (иначе подписчик неделю видит одно).
    picks = {pick_card(cards, day + dt.timedelta(days=i))[0] for i in range(30)}
    assert len(picks) >= 25


def test_message_hides_the_answer_under_a_spoiler():
    cards = load_cards()
    index, card = pick_card(cards, dt.date(2026, 11, 3))
    message = build_message(index, len(cards), card)

    assert "<tg-spoiler>" in message, "ответ обязан быть скрыт спойлером"
    assert card["back"] in message
    assert f"#{index + 1}" in message
    assert "flashcards" in message, "нет ссылки обратно в тренажёр"


def test_message_escapes_html():
    card = {"front": "<b>атака</b>", "back": "a & <b>"}
    message = build_message(0, 1, card)
    assert "<b>атака</b>" not in message
    assert "&lt;b&gt;атака&lt;/b&gt;" in message
    assert "a &amp; &lt;b&gt;" in message
