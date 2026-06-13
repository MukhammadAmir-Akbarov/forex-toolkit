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
