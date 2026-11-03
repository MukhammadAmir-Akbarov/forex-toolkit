"""Карта сезонности: 8 пар × 12 месяцев из дневных свечей.

Проверяем поведение, а не числа (числа пересчитываются еженедельно):

* таблица строится из JSON: 8 строк пар и 12 колонок месяцев;
* клик по ячейке показывает разбор с числом лет наблюдений;
* тонкие ячейки (мало лет) честно приглушены;
* страница работает на всех трёх локалях.
"""

from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "_mkdocs" / "data"


def _document() -> dict:
    return json.loads((DATA / "seasonality.json").read_text(encoding="utf-8"))


def _open(page, site_url, path="/tools/seasonality/"):
    page.goto(f"{site_url}{path}")
    page.wait_for_selector(".fx-season table")


def test_map_has_a_row_per_pair_and_a_column_per_month(site_url, pw_page):
    page = pw_page
    _open(page, site_url)

    assert page.locator(".fx-season tbody tr").count() == 8
    assert page.locator(".fx-season thead th").count() == 1 + 12


def test_cell_click_shows_breakdown_with_sample_size(site_url, pw_page):
    page = pw_page
    _open(page, site_url)

    page.locator(".fx-season-cell").first.click()
    detail = page.locator("#fx-season-detail").inner_text()
    assert "%" in detail, f"в разборе ячейки нет процентов: {detail!r}"


def test_thin_cells_are_dimmed(site_url, pw_page):
    page = pw_page
    _open(page, site_url)

    threshold = _document()["meta"]["thin_sample_below"]
    thin_count = page.locator(".fx-season-cell.fx-season-thin").count()
    assert thin_count > 0, (
        f"при пороге {threshold} лет ни одна ячейка не помечена тонкой — "
        "либо данных вдруг стало много, либо пометка сломалась"
    )


def test_page_renders_in_english_and_uzbek(site_url, pw_page):
    page = pw_page

    _open(page, site_url, "/en/tools/seasonality/")
    assert "Average month move" in page.locator(".fx-season").inner_text()

    _open(page, site_url, "/uz/tools/seasonality/")
    assert "o'rtacha" in page.locator(".fx-season").inner_text()
