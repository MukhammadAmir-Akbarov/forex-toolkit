"""Сверка «сколько нужно, чтобы жить с трейдинга»: браузер == Python."""

from __future__ import annotations

import pytest

from forex_toolkit.living_capital import plan_for

# (расходы, месячная доходность, подушка, старт, пополнение)
CASES = [
    (500.0, 0.015, 6, 1000.0, 200.0),
    (300.0, 0.01, 3, 0.0, 100.0),
    (1000.0, 0.03, 12, 5000.0, 500.0),
    (200.0, 0.005, 0, 0.0, 0.0),
    (750.0, 0.02, 6, 20000.0, 0.0),
]


@pytest.mark.parametrize("case", CASES, ids=[f"${c[0]:.0f}@{c[1]:.1%}" for c in CASES])
def test_browser_matches_python(pw_page, site_url, case):
    need, monthly_return, buffer_months, start, add = case
    page = pw_page
    page.goto(f"{site_url}/tools/living-capital/")
    page.wait_for_function("() => typeof window.__fxLivingCapital === 'function'")

    got = page.evaluate(
        "a => window.__fxLivingCapital(a[0], a[1], a[2], a[3], a[4])",
        [need, monthly_return, buffer_months, start, add],
    )
    expected = plan_for(
        monthly_need=need,
        monthly_return=monthly_return,
        buffer_months=buffer_months,
        start=start,
        monthly_add=add,
    ).as_dict()

    for field in ("gross_needed", "required_capital", "buffer", "total_needed"):
        assert round(got[field], 2) == expected[field], (
            f"{field} разошлось: браузер {got[field]}, Python {expected[field]}"
        )
    assert got["months_to_reach"] == expected["months_to_reach"]


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_page_shows_a_number_in_every_locale(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}tools/living-capital/")
    page.wait_for_selector(".tax-headline")

    headline = page.text_content(".tax-headline")
    assert headline.strip().startswith("$"), f"[{prefix}] {headline!r}"
    assert "undefined" not in page.text_content("#lc-result")


def test_lower_return_demands_more_capital_on_screen(pw_page, site_url):
    """Главный вывод страницы должен быть виден, а не только описан текстом."""
    page = pw_page
    page.goto(f"{site_url}/tools/living-capital/")
    page.wait_for_selector(".tax-headline")

    page.fill("#lc-return", "3")
    page.click("#lc-calc-btn")
    optimistic = page.text_content(".tax-headline")

    page.fill("#lc-return", "1")
    page.click("#lc-calc-btn")
    realistic = page.text_content(".tax-headline")

    def to_number(text):
        return float("".join(c for c in text if c.isdigit()))

    assert to_number(realistic) > to_number(optimistic) * 2.5


def test_nonsense_input_shows_an_error_not_a_number(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/living-capital/")
    page.wait_for_selector(".tax-headline")

    page.fill("#lc-need", "0")
    page.click("#lc-calc-btn")

    assert page.locator("#lc-result.calc-error").count() == 1
    assert page.locator(".tax-headline").count() == 0
