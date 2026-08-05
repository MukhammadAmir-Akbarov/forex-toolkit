from __future__ import annotations

import re

import pytest

from forex_toolkit.monte_carlo import simulate_summary
from forex_toolkit.risk_exposure import Position, effective_risk


def _number(text: str) -> float:
    value = text.replace("$", "").replace(" ", "").replace(" ", "").replace(" ", "")
    if "," in value and "." not in value:
        value = value.replace(",", ".")
    elif "," in value and "." in value:
        value = value.replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    assert match
    return float(match.group())


@pytest.mark.parametrize(
    ("prefix", "title"),
    [
        ("", "Была ли страница полезна?"),
        ("en/", "Was this page helpful?"),
        ("uz/", "Bu sahifa foydali bo'ldimi?"),
    ],
)
def test_feedback_is_localized_and_deduplicated(pw_page, site_url, prefix, title):
    page = pw_page
    page.add_init_script(
        "window.__events=[]; window.goatcounter={count:function(x){window.__events.push(x.path)}};"
    )
    page.goto(f"{site_url}/{prefix}")
    form = page.locator("form.md-feedback")
    assert form.is_visible()
    assert form.locator(".md-feedback__title").inner_text() == title
    form.locator('button[data-md-value="1"]').click()
    assert page.evaluate("window.__events.filter(x => x === 'feedback_yes').length") == 1
    page.reload()
    assert page.locator(".md-feedback__list").is_hidden()


def test_aggregate_risk_matches_python(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/risk-exposure-calculator/")
    page.click("#rx-calc")
    values = page.locator("#rx-result .fx-metrics strong").all_inner_texts()
    assert _number(values[0].split("/")[0]) == pytest.approx(20)
    expected = effective_risk(
        [Position("EURUSD", "long", 10), Position("GBPUSD", "long", 10)]
    )
    assert _number(values[1].split("/")[0]) == pytest.approx(expected, abs=0.01)
    assert "EURUSD" in page.locator("#rx-result").inner_text()


def test_calculator_event_has_no_payload_and_is_deduplicated(pw_page, site_url):
    page = pw_page
    page.add_init_script(
        "window.__events=[]; window.goatcounter={count:function(x){window.__events.push(x)}};"
    )
    page.goto(f"{site_url}/tools/cost-calculator/")
    page.click("#co-calc-btn")
    page.click("#co-calc-btn")
    events = page.evaluate(
        "window.__events.filter(x => x.path === 'calculator_completed')"
    )
    assert events == [
        {
            "path": "calculator_completed",
            "title": "calculator_completed",
            "event": True,
        }
    ]


def test_trade_desk_saves_journal_ready_draft(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/trade-desk/")
    page.click("#td-calc")
    assert "0.05 lot" in page.locator("#td-result").inner_text()
    page.locator("#td-checks input").evaluate_all(
        "inputs => inputs.forEach(input => { input.checked = true; })"
    )
    page.click("#td-save")
    draft = page.evaluate("JSON.parse(localStorage.getItem('forex_trade_drafts_v1'))[0]")
    assert draft["pair"] == "EURUSD"
    assert draft["lot_size"] == 0.05
    assert page.locator("#td-download").is_enabled()


def test_monte_carlo_matches_python_fixture(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/monte-carlo/")
    page.fill("#mco-sims", "100")
    page.fill("#mco-trades", "50")
    page.click("#mco-run")
    values = page.locator("#mco-result .fx-metrics strong").all_inner_texts()
    expected = simulate_summary(100, 50, 0.45, 2, 1, seed=42)
    assert _number(values[0]) == pytest.approx(expected["median_final"] * 1000, abs=0.01)
    assert page.locator("#mco-chart").is_visible()


def test_service_worker_registers(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/")
    page.wait_for_function(
        "async () => Boolean(await navigator.serviceWorker.getRegistration())"
    )
    registration = page.evaluate(
        "async () => (await navigator.serviceWorker.getRegistration()).scope"
    )
    assert registration == f"{site_url}/"
