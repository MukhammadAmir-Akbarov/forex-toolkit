"""JSON-блоки теста готовности: локали переводят текст, но не подсчёт.

Вопросы лежат на страницах, потому что их нужно переводить. Значит, ничто не
мешает переводчику случайно поменять баллы, порядок вариантов или категорию —
и один и тот же ответ дал бы разный вердикт на разных языках. Этот тест такое
не пропустит.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from risk_profile import QUESTIONS

MKDOCS = Path(__file__).resolve().parent.parent / "_mkdocs"
LOCALES = ("", "en", "uz")
BLOCK = re.compile(
    r'<script type="application/json" id="risk-profile-questions">\s*(.*?)\s*</script>',
    re.DOTALL,
)


def load(locale: str) -> list[dict]:
    name = "risk-profile.md" if not locale else f"risk-profile.{locale}.md"
    text = (MKDOCS / "tools" / name).read_text(encoding="utf-8")
    match = BLOCK.search(text)
    assert match, f"{name}: не найден блок с вопросами"
    return json.loads(match.group(1))


@pytest.mark.parametrize("locale", LOCALES)
def test_every_locale_matches_the_cli_scoring_model(locale: str) -> None:
    questions = load(locale)
    assert len(questions) == len(QUESTIONS)
    for page, source in zip(questions, QUESTIONS):
        assert page["category"] == source.category
        page_points = [option["points"] for option in page["options"]]
        assert page_points == [points for _, points in source.options]


@pytest.mark.parametrize("locale", LOCALES)
def test_every_option_has_visible_text(locale: str) -> None:
    for question in load(locale):
        assert question["q"].strip()
        for option in question["options"]:
            assert option["label"].strip()


def test_russian_block_is_identical_to_the_cli_source() -> None:
    """RU-страница генерируется из tools/risk_profile.py — тексты обязаны совпасть."""
    for page, source in zip(load(""), QUESTIONS):
        assert page["q"] == source.text
        assert [o["label"] for o in page["options"]] == [
            label for label, _ in source.options
        ]


def test_translations_are_not_left_in_russian() -> None:
    """Пустой перевод — это скопированный русский текст, его легко не заметить."""
    russian = [q.text for q in QUESTIONS]
    for locale in ("en", "uz"):
        translated = [q["q"] for q in load(locale)]
        assert translated != russian, f"{locale}: вопросы остались на русском"
