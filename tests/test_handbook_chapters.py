"""Печатный учебник должен быть одинаковым на трёх языках.

Поломка, ради которой написан файл: EN- и UZ-списки глав велись руками и
отстали от русского — 3 и 5 глав против 14, хотя все переводы лежали рядом в
``_mkdocs/``. Читатель на узбекском получал 192 KB вместо 1.2 MB и не знал,
что остальные одиннадцать глав существуют.
"""

from __future__ import annotations

import handbook_chapters
import pytest

LOCALES = handbook_chapters.LOCALES


def test_every_russian_chapter_source_exists() -> None:
    missing = [
        path for _, path in handbook_chapters.chapters("ru") if not path.exists()
    ]
    assert missing == [], f"нет исходников глав: {missing}"


@pytest.mark.parametrize("lang", LOCALES)
def test_locale_has_the_same_chapters_as_russian(lang: str) -> None:
    """Состав и порядок задаёт RU; локаль отличается только языком файла."""
    ru = handbook_chapters.chapters("ru")
    localized = handbook_chapters.chapters(lang)

    assert len(localized) == len(ru)
    for (_, ru_path), (_, path) in zip(ru, localized, strict=True):
        assert path.name == f"{ru_path.stem}.{lang}.md"
        assert path.parent == ru_path.parent


@pytest.mark.parametrize("lang", LOCALES)
def test_locale_chapter_files_are_translated(lang: str) -> None:
    """Каждая глава учебника переведена — иначе PDF молча потеряет её."""
    missing = [
        path.name for _, path in handbook_chapters.chapters(lang) if not path.exists()
    ]
    assert missing == [], f"главы без перевода на {lang}: {missing}"


@pytest.mark.parametrize("lang", LOCALES)
def test_every_chapter_title_is_translated(lang: str) -> None:
    """Заголовок главы не должен остаться русским в нерусском PDF."""
    titles = handbook_chapters.CHAPTER_TITLES[lang]
    untranslated = [
        ru_title
        for ru_title, _ in handbook_chapters.CHAPTERS_RU
        if ru_title not in titles
    ]
    assert untranslated == [], f"нет перевода заголовка на {lang}: {untranslated}"
