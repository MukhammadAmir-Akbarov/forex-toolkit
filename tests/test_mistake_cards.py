"""Карточки из ошибок: хранилище, связь экзамена/квизов с тренажёром карточек.

Слияние (``window.__fxMistakeMerge`` в _mistake-cards.js) выполняется в
Node-песочнице; связку страниц проверяем по исходникам.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "_mkdocs"
WIDGETS = DOCS / "javascripts" / "widgets"
MODULE = WIDGETS / "_mistake-cards.js"
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"
DECKS = [DOCS / "tools" / f"flashcards{s}.md" for s in ("", ".en", ".uz")]

NO_NODE = shutil.which("node") is None


def _call(fn: str, *args):
    done = subprocess.run(
        ["node", str(SANDBOX), str(MODULE), fn, "-", "ru"],
        input=json.dumps(list(args)),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


def _card(q: str) -> dict:
    return {"q": q, "a": "ответ " + q, "explain": "почему", "src": "exam"}


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_new_miss_goes_first_and_repeat_does_not_duplicate() -> None:
    cards = _call("__fxMistakeMerge", [], [_card("A"), _card("B")])
    assert [c["q"] for c in cards] == ["B", "A"]
    cards = _call("__fxMistakeMerge", cards, [_card("A")])
    assert [c["q"] for c in cards] == ["A", "B"]
    assert cards[0]["id"] == _call("__fxMistakeId", "A")


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_limit_and_broken_items() -> None:
    many = [_card(f"Q{i}") for i in range(70)]
    cards = _call("__fxMistakeMerge", [], [*many, {"q": "без ответа"}, None])
    assert len(cards) == 60
    assert cards[0]["q"] == "Q69" and cards[-1]["q"] == "Q10"


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_id_is_stable_and_text_specific() -> None:
    assert _call("__fxMistakeId", "Что такое пипс?") == _call(
        "__fxMistakeId", "Что такое пипс?"
    )
    assert _call("__fxMistakeId", "A") != _call("__fxMistakeId", "B")


@pytest.mark.parametrize("deck", DECKS, ids=lambda p: p.name)
def test_deck_mixes_in_mistakes_with_own_progress_keys(deck: Path) -> None:
    src = deck.read_text(encoding="utf-8")
    # Инлайн-скрипт идёт раньше глобальных: FXMistakes ещё нет, ключ читается напрямую.
    assert "localStorage.getItem('forex_mistake_cards_v1')" in src
    assert "tags: ['mistakes'], key: 'm-' + m.id" in src
    assert re.search(r"'mistakes':\s+'🔁 ", src), "нет подписи фильтра «Мои ошибки»"
    # Прогресс читается, пишется и сбрасывается только через stateKey —
    # иначе карточки из ошибок затрут ftk-flash-<индекс> базовой колоды.
    assert "'ftk-flash-' + idx)" not in src and "'ftk-flash-' + i)" not in src
    assert src.count("stateKey(") == 4


@pytest.mark.parametrize("widget", ["exam.js", "chapter-quiz.js"])
def test_exam_and_quizzes_feed_the_deck(widget: str) -> None:
    src = (WIDGETS / widget).read_text(encoding="utf-8")
    assert "window.FXMistakes ? window.FXMistakes.add(" in src or (
        "window.FXMistakes\n      ? window.FXMistakes.add(" in src
    )
    assert src.count("mistakes: function") == 3, "нужны RU/EN/UZ"
    assert "a: q.options[q.answer]" in src
