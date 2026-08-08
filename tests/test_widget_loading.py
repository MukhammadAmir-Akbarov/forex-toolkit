"""Каждый виджет должен быть подключён ровно там, где он нужен.

Зачем: виджеты-калькуляторы висели в `extra_javascript` и грузились на всех
страницах — 38 KB gzip даже там, где не нужен ни один. Теперь страница
объявляет свои виджеты во front matter (`widgets: [pip]`), а глобально
остаются только `_i18n.js` (определяет `window.FXW`) и очередь тренировок.

Ошибиться здесь легко и тихо: страница без объявления просто перестанет
считать, сборка при этом пройдёт, `--strict` промолчит. Поэтому проверяем
связь напрямую — по якорю, которым виджет сам себя опознаёт.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "mkdocs.yml"
DOCS = ROOT / "_mkdocs"
WIDGETS = DOCS / "javascripts" / "widgets"

# Служебные файлы: не виджеты страницы, нужны нескольким и живут в глобальных.
SHARED = {"_i18n", "_training-queue"}


def global_widgets() -> set[str]:
    text = MKDOCS.read_text(encoding="utf-8")
    return set(re.findall(r"javascripts/widgets/([\w-]+)\.js", text))


def anchor_of(widget: Path) -> str | None:
    """Идентификатор, по которому виджет решает, что он на своей странице."""
    source = widget.read_text(encoding="utf-8")
    match = re.search(r'getElementById\(["\']([\w-]+)["\']\)', source)
    return match.group(1) if match else None


def declared_widgets(page: Path) -> set[str]:
    text = page.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return set()
    head = text[4 : text.index("\n---\n", 4)]
    match = re.search(r"widgets:\s*\[([^\]]*)\]", head)
    if not match:
        return set()
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


WIDGET_FILES = sorted(w for w in WIDGETS.glob("*.js") if w.stem not in SHARED)
ALL_PAGES = sorted(DOCS.rglob("*.md"))


def test_shared_helpers_stay_global() -> None:
    """`window.FXW` должен существовать до того, как выполнится любой виджет."""
    assert SHARED <= global_widgets(), "общие хелперы пропали из extra_javascript"


def test_page_widgets_are_not_loaded_globally() -> None:
    """Одностраничный виджет в глобальных — это вес на всех 249 страницах."""
    leaked = {w.stem for w in WIDGET_FILES} & global_widgets()
    assert not leaked, (
        f"грузятся глобально, хотя нужны на одной странице: {sorted(leaked)}"
    )


@pytest.mark.parametrize("widget", WIDGET_FILES, ids=lambda w: w.stem)
def test_every_page_using_a_widget_declares_it(widget: Path) -> None:
    """Страница с якорем виджета обязана объявить его во front matter."""
    anchor = anchor_of(widget)
    if anchor is None:
        pytest.skip(f"{widget.stem}: не нашёл якорь — виджет без getElementById")

    marker = f'id="{anchor}"'
    missing = [
        page.relative_to(DOCS)
        for page in ALL_PAGES
        if marker in page.read_text(encoding="utf-8")
        and widget.stem not in declared_widgets(page)
    ]
    assert not missing, (
        f"{widget.stem}: страницы содержат {marker}, но не объявляют виджет — "
        f"считать будет нечем: {missing}"
    )


@pytest.mark.parametrize("widget", WIDGET_FILES, ids=lambda w: w.stem)
def test_declared_widgets_are_actually_needed(widget: Path) -> None:
    """Обратная сторона: объявили виджет там, где его якоря нет."""
    anchor = anchor_of(widget)
    if anchor is None:
        pytest.skip(f"{widget.stem}: не нашёл якорь")

    marker = f'id="{anchor}"'
    # trade-desk объявляет strategy-lab: два виджета делят одну страницу,
    # и якорь второго появляется только после его же отрисовки.
    extra = [
        page.relative_to(DOCS)
        for page in ALL_PAGES
        if widget.stem in declared_widgets(page)
        and marker not in page.read_text(encoding="utf-8")
        and widget.stem not in {"strategy-lab"}
    ]
    assert not extra, f"{widget.stem}: объявлен без надобности на {extra}"


def test_all_locales_declare_the_same_widgets() -> None:
    """RU/EN/UZ должны получить одинаковый набор — иначе локаль не считает."""
    mismatched = []
    for page in ALL_PAGES:
        if page.name.endswith((".en.md", ".uz.md")):
            continue
        base = declared_widgets(page)
        for suffix in (".en.md", ".uz.md"):
            other = page.with_name(page.name[:-3] + suffix)
            if other.exists() and declared_widgets(other) != base:
                mismatched.append(
                    f"{page.relative_to(DOCS)}: {sorted(base)} != "
                    f"{other.name} {sorted(declared_widgets(other))}"
                )
    assert not mismatched, "\n".join(mismatched)
