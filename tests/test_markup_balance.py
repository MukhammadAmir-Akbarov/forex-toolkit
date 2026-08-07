"""Баланс HTML-тегов в страницах документации.

Зачем: один лишний ``</div>`` на странице экзамена закрывал не виджет, а
контейнер самой страницы. Остальной контент становился соседом ``.md-content``
во flex-строке Material и отбирал у него всю ширину — на телефоне колонка
схлопывалась до 24px, а текст переносился по одной букве.

Markdown такое не ловит: mkdocs собирается без ошибок, ссылки проходят, и
`--strict` молчит. Поэтому проверяем баланс прямо здесь.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

MKDOCS = Path(__file__).resolve().parent.parent / "_mkdocs"
# Парные теги, которыми в страницах оборачивают виджеты.
TAGS = ("div", "section", "article")
PAGES = sorted(MKDOCS.rglob("*.md"))


def balance(text: str, tag: str) -> tuple[int, bool]:
    """Итоговая глубина вложенности и признак ухода в минус."""
    opening = re.compile(rf"<{tag}\b")
    closing = re.compile(rf"</{tag}>")
    depth = 0
    went_negative = False
    for line in text.split("\n"):
        depth += len(opening.findall(line)) - len(closing.findall(line))
        if depth < 0:
            went_negative = True
    return depth, went_negative


def test_documentation_has_pages() -> None:
    assert len(PAGES) > 200, "страницы не найдены — тест смотрит не туда"


@pytest.mark.parametrize("tag", TAGS)
def test_no_page_closes_more_tags_than_it_opens(tag: str) -> None:
    """Лишний закрывающий тег ломает раскладку всей страницы, а не виджета."""
    broken = []
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        depth, negative = balance(text, tag)
        if negative:
            broken.append(f"{page.relative_to(MKDOCS)}: лишний </{tag}>")
    assert not broken, "\n".join(broken)


@pytest.mark.parametrize("tag", TAGS)
def test_no_page_leaves_tags_open(tag: str) -> None:
    broken = []
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        depth, _ = balance(text, tag)
        if depth != 0:
            broken.append(f"{page.relative_to(MKDOCS)}: не закрыто <{tag}>: {depth}")
    assert not broken, "\n".join(broken)


def test_exam_widget_closes_itself() -> None:
    """Регрессия: именно здесь лишний тег и жил, во всех трёх локалях."""
    for name in ("exam.md", "exam.en.md", "exam.uz.md"):
        text = (MKDOCS / "tools" / name).read_text(encoding="utf-8")
        depth, negative = balance(text, "div")
        assert depth == 0 and not negative, name
        assert 'id="exam-widget"' in text
