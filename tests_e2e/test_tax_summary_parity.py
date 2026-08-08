"""Сверка годового итога для декларации: браузер == Python.

Это число человек перепишет в налоговую декларацию, поэтому расхождение между
`forex_toolkit/tax_summary.py` и зеркалом в `journal.js` недопустимо. Заодно
проверяем сам маршрут: журнал → калькулятор налога, которого раньше не было —
цифры переносили руками по экспорту CSV.
"""

from __future__ import annotations

import json

import pytest

from forex_toolkit.tax_summary import summarize_all, summarize_year

# Наборы подобраны по краям: прибыльный год, убыточный, смешанный,
# записи без суммы и мусорные даты.
CASES = {
    "прибыльный год": [
        {"date": "2025-02-03", "pnl": 300.0},
        {"date": "2025-07-19", "pnl": -120.0},
        {"date": "2025-12-30", "pnl": 45.5},
    ],
    "убыточный год": [
        {"date": "2025-01-05", "pnl": -200.0},
        {"date": "2025-03-11", "pnl": 50.0},
    ],
    "два года подряд": [
        {"date": "2025-06-01", "pnl": 100.0},
        {"date": "2026-01-15", "pnl": -40.0},
        {"date": "2026-02-20", "pnl": 250.0},
    ],
    "битые записи": [
        {"date": "2025-04-04", "pnl": 80.0},
        {"date": "2025-04-05", "pnl": None},
        {"date": "не дата", "pnl": 999.0},
        {"date": "2025-04-06", "pnl": "мусор"},
    ],
    "сделка в ноль": [
        {"date": "2025-08-08", "pnl": 0.0},
        {"date": "2025-08-09", "pnl": 10.0},
    ],
}


@pytest.mark.parametrize("name", list(CASES), ids=list(CASES))
def test_browser_matches_python(pw_page, site_url, name):
    trades = CASES[name]
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.wait_for_function("() => typeof window.__fxTaxSummary === 'function'")

    got = page.evaluate("rows => window.__fxTaxSummary(rows)", trades)
    expected = [year.as_dict() for year in summarize_all(trades)]

    assert len(got) == len(expected), f"{name}: разное число лет"
    for browser, python in zip(got, expected):
        assert browser["year"] == python["year"]
        assert browser["trades"] == python["trades"], f"{name}: разное число сделок"
        assert browser["skipped"] == python["skipped"], f"{name}: разные пропуски"
        for field in ("profit", "loss", "net", "taxable", "tax"):
            assert round(browser[field], 2) == python[field], (
                f"{name}: {field} разошлось — браузер {browser[field]}, "
                f"Python {python[field]}"
            )


def test_journal_hands_the_year_over_to_the_tax_calculator(pw_page, site_url):
    """Маршрут целиком: демо-журнал → таблица лет → калькулятор налога."""
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.click("#journal-demo")
    page.wait_for_selector("#journal-tax-summary table")

    stored = page.evaluate(
        "() => JSON.parse(localStorage.getItem('forex_journal_data_v2')"
        " || '{}').rows || []"
    )
    years = summarize_all(
        [{"date": r.get("date"), "pnl": r.get("pnl")} for r in stored]
    )
    assert years, "в демо-журнале нет ни одного года"
    newest = years[0]

    page.click("#journal-tax-summary .journal-tax-open")
    page.wait_for_selector("#tax-from-journal")

    handed = page.evaluate(
        "() => JSON.parse(localStorage.getItem('forex_tool_settings_v1')).tax"
    )
    assert handed["source"] == "journal"
    assert handed["year"] == newest.year
    assert round(handed["profit"], 2) == newest.as_dict()["profit"]
    assert round(handed["loss"], 2) == newest.as_dict()["loss"]

    # Калькулятор должен показать те же деньги, а не значения по умолчанию.
    assert float(page.input_value("#tax-profit")) == pytest.approx(
        newest.profit, abs=0.01
    )
    assert float(page.input_value("#tax-loss")) == pytest.approx(newest.loss, abs=0.01)
    assert str(newest.year) in page.text_content("#tax-from-journal")


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_summary_is_translated_everywhere(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}journal/web-journal/")
    page.click("#journal-demo")
    page.wait_for_selector("#journal-tax-summary table")

    heading = page.text_content("#journal-tax-summary h3").strip()
    assert heading and "undefined" not in heading, f"[{prefix}] заголовок не переведён"
    assert page.locator("#journal-tax-summary .journal-tax-open").count() >= 1


def test_losing_year_shows_no_tax_due(pw_page, site_url):
    """Убыточный год не должен показывать налог к уплате."""
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.wait_for_function("() => typeof window.__fxTaxSummary === 'function'")

    losing = [
        {"date": "2025-01-01", "pnl": -500.0},
        {"date": "2025-02-01", "pnl": 100.0},
    ]
    got = page.evaluate("rows => window.__fxTaxSummary(rows)", losing)[0]
    python = summarize_year(losing, 2025).as_dict()

    assert got["tax"] == 0 and python["tax"] == 0
    assert got["taxable"] == 0 and python["taxable"] == 0
    assert round(got["net"], 2) == python["net"] == -400.0


def test_python_and_browser_agree_on_an_empty_journal(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.wait_for_function("() => typeof window.__fxTaxSummary === 'function'")

    assert page.evaluate("() => window.__fxTaxSummary([])") == []
    assert summarize_all([]) == []
    assert json.dumps(page.evaluate("() => window.__fxTaxSummary(null)")) == "[]"
