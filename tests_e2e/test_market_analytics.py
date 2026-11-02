"""Рыночная аналитика (волатильность + корреляции) — в настоящем браузере.

Проверяем не цифры (они пересчитываются скриптом), а контракт страницы:
обе тепловые карты строятся из JSON на всех трёх локалях, размерность
совпадает с данными, пустые корреляции показаны прочерком, а не нулём
(ноль был бы утверждением «пары независимы» — его у нас нет).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "_mkdocs" / "data" / "market-analytics.json"

LOCALES = ["", "en/", "uz/"]


def _document() -> dict:
    return json.loads(DATASET.read_text(encoding="utf-8"))


def _open(page, site_url, prefix):
    page.goto(f"{site_url}/{prefix}tools/market-analytics/")
    page.wait_for_selector(".ma-vol, .calc-error", timeout=30_000)


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_both_heatmaps_render(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    assert page.locator(".calc-error").count() == 0, (
        f"[{prefix or 'ru'}] данные не загрузились: {page.text_content('.calc-error')}"
    )
    document = _document()
    pairs = len(document["volatility"]["pairs"])
    assert page.locator(".ma-vol tbody tr").count() == pairs
    # 24 часа + ячейка с именем пары.
    assert page.locator(".ma-vol tbody tr").first.locator("td").count() == 24
    assert page.locator(".ma-corr tbody tr").count() == pairs
    assert page.locator(".ma-corr tbody tr").first.locator("td").count() == pairs


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_every_volatility_cell_is_colored(pw_page, site_url, prefix):
    """Ячейка без цвета — дыра в карте: читатель решит, что данных нет."""
    page = pw_page
    _open(page, site_url, prefix)

    cells = page.locator(".ma-vol td")
    for i in range(cells.count()):
        style = cells.nth(i).get_attribute("style") or ""
        assert "background" in style, f"[{prefix or 'ru'}] ячейка {i} без цвета"


def test_missing_correlation_is_a_dash_not_a_zero(pw_page, site_url):
    """null в данных обязан стать прочерком: 0.00 читался бы как факт."""
    page = pw_page
    _open(page, site_url, "")
    document = _document()

    has_null = any(
        value is None for row in document["correlations"]["values"] for value in row
    )
    dashes = page.locator(".ma-corr .ma-none").count()
    assert (dashes > 0) == has_null, (
        "в данных null есть/нет, а прочерки в таблице не совпадают с ними"
    )


def test_diagonal_is_marked(pw_page, site_url):
    """Диагональ (корреляция пары с собой) выделена — иначе читатель
    принимает её за самый «горячий» сигнал матрицы."""
    page = pw_page
    _open(page, site_url, "")

    document = _document()
    pairs = len(document["correlations"]["pairs"])
    assert page.locator(".ma-corr .ma-diag").count() == pairs


def test_peak_is_named_and_matches_data(pw_page, site_url):
    """Подпись пика под картой обязана совпадать с данными: фраза пишется
    скриптом страницы, а не текстом, который протухнет при пересчёте."""
    page = pw_page
    _open(page, site_url, "")

    document = _document()
    vol = document["volatility"]
    peak_pair, peak_value = "", 0.0
    for pair in vol["pairs"]:
        for value in vol["values"][pair]:
            if value > peak_value:
                peak_pair, peak_value = pair, value

    text = page.text_content("#market-analytics")
    assert peak_pair in text
    assert f"{peak_value:.1f}" in text
