"""TL;DR-блок «Простыми словами за 30 секунд» — на каждой странице ×3 локали.

Проверяем контракт механики, а не тексты: блок появляется там, где у страницы
есть запись в data/tldr.json, текст совпадает с записью, а служебные страницы
(index/offline/privacy) и кириллическая копия uz-cyrl блока не получают.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

DATA = json.loads(
    (
        Path(__file__).resolve().parent.parent / "_mkdocs" / "data" / "tldr.json"
    ).read_text(encoding="utf-8")
)

SPOTS = [
    ("", "tools/pip-calculator", "ru"),
    ("en/", "tools/pip-calculator", "en"),
    ("uz/", "tools/pip-calculator", "uz"),
    ("", "forex-guide", "ru"),
    ("en/", "uz/forex-nima", "en"),
    ("uz/", "uz/forex-nima", "uz"),
]


@pytest.mark.parametrize(
    "prefix,slug,lang", SPOTS, ids=[f"{s[2]}:{s[1]}" for s in SPOTS]
)
def test_tldr_block_matches_the_json(pw_page, site_url, prefix, slug, lang):
    page = pw_page
    page.goto(f"{site_url}/{prefix}{slug}/")
    page.wait_for_selector(".fx-tldr", timeout=15_000)

    block = page.locator(".fx-tldr")
    assert DATA[slug][lang] in block.inner_text(), (
        f"[{prefix or 'ru'}{slug}] текст блока не совпал с tldr.json"
    )
    # Блок обязан стоять сразу после H1 — читатель видит его до длинного текста.
    h1 = page.locator(".md-content__inner h1").first
    following = h1.evaluate(
        "el => el.nextElementSibling && el.nextElementSibling.className"
    )
    assert "fx-tldr" in following


@pytest.mark.parametrize(
    "slug", ["", "offline", "privacy"], ids=["index", "offline", "privacy"]
)
def test_service_pages_have_no_tldr(pw_page, site_url, slug):
    page = pw_page
    page.goto(f"{site_url}/{slug}/" if slug else f"{site_url}/")
    page.wait_for_selector(".md-content__inner")
    page.wait_for_timeout(800)  # даём fetch(tldr.json) шанс отработать
    assert page.locator(".fx-tldr").count() == 0


def test_uz_cyrl_does_not_duplicate_the_block(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/uz-cyrl/")
    page.wait_for_selector(".md-content__inner")
    page.wait_for_timeout(800)
    assert page.locator(".fx-tldr").count() == 0, (
        "на кириллической копии uz-cyrl латинский TL;DR выглядит "
        "чужеродно — не вставляем"
    )


def test_every_ru_page_key_has_all_three_locales():
    """Строка без одной из локалей — дыра, которую дрейф-чекер md-файлов
    не поймает: блок молча пропадёт на этой локали."""
    for slug, entry in DATA.items():
        for lang in ("ru", "en", "uz"):
            assert entry.get(lang), f"{slug}: нет локали {lang}"
