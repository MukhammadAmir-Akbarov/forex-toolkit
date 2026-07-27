"""e2e для локального веб-журнала: CSV-импорт, метрики и фильтры."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def number(text: str) -> float:
    """Число из локализованной строки: '$1,234.56', '$1 234,56', '2.30R'."""
    value = (
        text.replace("$", "")
        .replace("R", "")
        .replace("%", "")
        .replace("\xa0", "")
        .replace("\u202f", "")
        .replace(" ", "")
        .strip()
    )
    decimal = max(value.rfind(","), value.rfind("."))
    if decimal < 0:
        return float(value)
    integer = re.sub(r"[.,]", "", value[:decimal])
    return float(integer + "." + value[decimal + 1 :])


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_web_journal_demo_and_filter(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}journal/web-journal/")
    page.click("#journal-demo")
    page.wait_for_selector("#journal-dashboard", state="visible")

    assert page.text_content("#journal-m-trades").strip() == "6"
    assert number(page.text_content("#journal-m-winrate")) == pytest.approx(50.0)
    assert number(page.text_content("#journal-m-pf")) == pytest.approx(1.72)
    assert number(page.text_content("#journal-m-pnl")) == pytest.approx(23.0)
    assert number(page.text_content("#journal-m-r")) == pytest.approx(2.3)
    assert number(page.text_content("#journal-m-dd")) == pytest.approx(20.0)
    assert number(page.text_content("#journal-m-discipline")) == pytest.approx(
        66.7
    )
    assert page.locator("#journal-heatmap .journal-heatmap-cell").count() == 168
    assert page.locator("#journal-by-pair tr").count() == 3
    assert page.locator("#journal-by-setup tr").count() == 5
    assert page.locator("#journal-by-direction tr").count() == 2
    assert page.locator("#journal-by-emotion tr").count() == 3
    assert page.locator("#journal-insights-list li").count() >= 3

    page.select_option("#journal-rules", "no")
    assert page.text_content("#journal-m-trades").strip() == "2"
    assert number(page.text_content("#journal-m-pnl")) == pytest.approx(-22.0)
    assert page.locator("#journal-table-body tr").count() == 2


def test_web_journal_extended_csv_upload(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.set_input_files(
        "#journal-file", ROOT / "journal" / "trading-journal-template.csv"
    )
    page.wait_for_selector("#journal-dashboard", state="visible")

    assert page.text_content("#journal-m-trades").strip() == "2"
    assert number(page.text_content("#journal-m-winrate")) == pytest.approx(50.0)
    assert number(page.text_content("#journal-m-pf")) == pytest.approx(2.0)
    assert number(page.text_content("#journal-m-pnl")) == pytest.approx(5.0)
    assert number(page.text_content("#journal-m-r")) == pytest.approx(1.0)
    assert number(page.text_content("#journal-m-discipline")) == pytest.approx(
        100.0
    )
    assert page.locator("#journal-table-body tr").count() == 2
    assert "trust the plan" not in page.text_content("#journal-table-body")
    assert page.locator("#journal-by-emotion tr").count() == 2


def test_web_journal_imports_mt5_html(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.set_input_files(
        "#journal-file", ROOT / "tests" / "fixtures" / "mt5-statement.html"
    )
    page.wait_for_selector("#journal-dashboard", state="visible")

    assert page.text_content("#journal-m-trades").strip() == "3"
    assert number(page.text_content("#journal-m-winrate")) == pytest.approx(66.7)
    assert number(page.text_content("#journal-m-pnl")) == pytest.approx(21.4)
    assert page.locator("#journal-by-pair tr").count() == 2
    assert page.locator("#journal-table-body tr").count() == 3

    page.reload()
    page.wait_for_selector("#journal-dashboard", state="visible")
    assert page.text_content("#journal-m-trades").strip() == "3"


def test_web_journal_restores_and_clears_local_data(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.set_input_files(
        "#journal-file", ROOT / "journal" / "trading-journal-template.csv"
    )
    page.wait_for_selector("#journal-dashboard", state="visible")

    stored = page.evaluate("() => localStorage.getItem('forex_journal_data_v2')")
    assert stored

    page.reload()
    page.wait_for_selector("#journal-dashboard", state="visible")
    assert page.text_content("#journal-m-trades").strip() == "2"
    assert "trading-journal-template.csv" in page.text_content("#journal-status")

    page.click("#journal-clear")
    assert not page.is_visible("#journal-dashboard")
    assert page.evaluate(
        "() => localStorage.getItem('forex_journal_data_v2')"
    ) is None


def test_web_journal_exports_summary(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/en/journal/web-journal/")
    page.click("#journal-demo")

    with page.expect_download() as csv_download:
        page.click("#journal-export-csv")
    assert csv_download.value.suggested_filename == "forex-journal-summary.csv"

    with page.expect_download() as html_download:
        page.click("#journal-export-html")
    assert html_download.value.suggested_filename == "forex-journal-summary.html"
