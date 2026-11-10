"""Качество банков мини-квизов в конце глав гайда.

Инварианты, на которые опирается виджет chapter-quiz.js:
* каждая глава несёт блок #chapter-quiz + JSON #chapter-quiz-questions;
* ровно 3 вопроса на главу, 4 варианта, тексты вариантов не повторяются
  (правильный ищется по тексту после перемешивания — дубли сделали бы
  ответ неоднозначным);
* во всех локалях один и тот же правильный индекс у вопроса под номером —
  иначе перевод переставил варианты, но не поправил answer;
* нет перекоса позиций правильных ответов (как была дыра в экзамене);
* число глав в dashboard.js (QUIZ_CHAPTERS) совпадает с реальностью.
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "_mkdocs" / "docs"
DASHBOARD = ROOT / "_mkdocs" / "javascripts" / "widgets" / "dashboard.js"
WIDGET = ROOT / "_mkdocs" / "javascripts" / "widgets" / "chapter-quiz.js"

CHAPTERS = (
    "technical-analysis",
    "strategy-details",
    "real-analysis",
    "order-types-mechanics",
    "fundamental-analysis-guide",
    "broker-mechanics-101",
)
LOCALES = ("ru", "en", "uz")
SUFFIX = {"ru": "", "en": ".en", "uz": ".uz"}


def load_bank(chapter: str, locale: str) -> list[dict]:
    path = DOCS / f"{chapter}{SUFFIX[locale]}.md"
    text = path.read_text(encoding="utf-8")
    assert f'data-quiz-key="{chapter}"' in text, (
        f"{chapter}/{locale}: нет #chapter-quiz"
    )
    match = re.search(
        r'<script type="application/json" id="chapter-quiz-questions">(.*?)</script>',
        text,
        re.S,
    )
    assert match, f"{chapter}/{locale}: блок #chapter-quiz-questions не найден"
    return json.loads(match.group(1))


@pytest.mark.parametrize("chapter", CHAPTERS)
@pytest.mark.parametrize("locale", LOCALES)
def test_every_chapter_quiz_is_well_formed(chapter: str, locale: str) -> None:
    bank = load_bank(chapter, locale)
    assert len(bank) == 3, f"{chapter}/{locale}: {len(bank)} вопросов вместо 3"
    for item in bank:
        label = f"{chapter}/{locale}: {item['q'][:50]}"
        assert len(item["options"]) == 4, f"{label} — не 4 варианта"
        assert 0 <= item["answer"] < 4, f"{label} — answer вне диапазона"
        assert item.get("explain"), f"{label} — нет объяснения"
        assert len(set(item["options"])) == 4, f"{label} — дубли вариантов"


@pytest.mark.parametrize("chapter", CHAPTERS)
def test_locales_stay_in_sync(chapter: str) -> None:
    """Один и тот же вопрос под одним номером с одним answer во всех локалях."""
    banks = {locale: load_bank(chapter, locale) for locale in LOCALES}
    for i in range(3):
        answers = {locale: banks[locale][i]["answer"] for locale in LOCALES}
        assert len(set(answers.values())) == 1, (
            f"{chapter} вопрос #{i + 1}: разные правильные ответы по локалям — "
            f"{answers}. Перевод переставил варианты, но не поправил answer."
        )


def test_answer_positions_are_not_skewed() -> None:
    """Клик по одной позиции не должен давать заметную долю верных ответов."""
    answers = [
        load_bank(chapter, "ru")[i]["answer"] for chapter in CHAPTERS for i in range(3)
    ]
    counts = collections.Counter(answers)
    best = max(counts.values()) / len(answers)
    assert best < 0.5, f"перекос позиций ответов: {dict(sorted(counts.items()))}"


def test_dashboard_chapter_count_matches_reality() -> None:
    """Карточка квизов в кабинете считает главы по той же цифре, что и страницы."""
    source = DASHBOARD.read_text(encoding="utf-8")
    match = re.search(r"QUIZ_CHAPTERS\s*=\s*(\d+)", source)
    assert match, "в dashboard.js не найден QUIZ_CHAPTERS"
    assert int(match.group(1)) == len(CHAPTERS), (
        f"dashboard считает {match.group(1)} глав, квизы стоят на {len(CHAPTERS)}"
    )


def test_widget_shuffles_options_without_mutating_the_bank() -> None:
    """Перемешивание идёт по копии — иначе пересдача съезжает по answer."""
    source = WIDGET.read_text(encoding="utf-8")
    assert "function shuffled(list)" in source, "функция перемешивания пропала"
    assert "list.slice()" in source, "перемешивание мутирует исходный массив"
    assert "shuffled(item.options)" in source, "варианты ответа не перемешиваются"
