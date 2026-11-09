"""«Неделя на рынке»: архив недель с топ-3 движениями — в настоящем браузере.

Проверяем контракт, а не цифры (архив пересчитывается скриптом и еженедельным
workflow): карточки с графиками на всех локалях, ходы совпадают с JSON,
таблица «остальных» дополняет топ до восьми пар, порядок — по |ход в ATR|,
кнопки ← → честно листают архив.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "_mkdocs" / "data" / "weekly-review.json"

LOCALES = ["", "en/", "uz/"]


def _document() -> dict:
    return json.loads(DATASET.read_text(encoding="utf-8"))


def _latest_week() -> dict:
    return _document()["weeks"][-1]


def _open(page, site_url, prefix):
    page.goto(f"{site_url}/{prefix}tools/weekly-review/")
    page.wait_for_selector(".wr-card, .calc-error", timeout=30_000)


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_three_move_cards_render(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    assert page.locator(".calc-error").count() == 0
    week = _latest_week()
    assert page.locator(".wr-card").count() == len(week["moves"])
    # У каждой карточки — свой мини-график со свечами недели.
    assert page.locator(".wr-chart").count() == len(week["moves"])
    # «Остальные» дополняют топ до полного набора пар.
    assert page.locator(".wr-others tbody tr").count() == len(week["others"])


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_moves_match_the_json(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    text = page.locator("#weekly-review").inner_text()
    for move in _latest_week()["moves"]:
        assert move["pair"] in text
        assert f"{move['change_pips']:+.1f}" in text


def test_sorted_by_absolute_atr_move(pw_page, site_url):
    """Порядок карточек — по |ход в ATR|: «крупнейшее» — не самое большое
    число пипсов (у иеновых пар их всегда больше), а относительный ход."""
    week = _latest_week()
    atr_moves = [abs(m["move_in_atr"]) for m in week["moves"]]
    assert atr_moves == sorted(atr_moves, reverse=True)

    page = pw_page
    _open(page, site_url, "")
    first_pair = week["moves"][0]["pair"]
    assert first_pair in page.locator(".wr-card").first.inner_text()


def test_week_is_stated_on_the_page(pw_page, site_url):
    """Обзор без дат — украшение: читатель обязан видеть, КАКАЯ это неделя."""
    page = pw_page
    _open(page, site_url, "")

    week = _latest_week()
    text = page.locator(".wr-week").inner_text()
    assert week["from"] in text and week["to"] in text


def test_archive_navigation_walks_back_and_forth(pw_page, site_url):
    """Архив без навигации — мёртвый архив: кнопки обязаны листать недели."""
    document = _document()
    if len(document["weeks"]) < 2:
        pytest.skip("в данных одна неделя — листать нечего")

    page = pw_page
    _open(page, site_url, "")

    # На свежей неделе «позже» запрещена, «раньше» — ведёт в прошлое.
    assert page.locator("#wr-next").is_disabled()
    page.click("#wr-prev")
    previous = document["weeks"][-2]
    text = page.locator(".wr-week").inner_text()
    assert previous["from"] in text, "кнопка «раньше» не привела на прошлую неделю"
    assert page.locator(".wr-card").count() == len(previous["moves"])

    # И обратно — на свежую.
    page.click("#wr-next")
    text = page.locator(".wr-week").inner_text()
    assert _latest_week()["from"] in text, "кнопка «позже» не вернула свежую неделю"
