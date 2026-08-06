from __future__ import annotations

import re
from datetime import date, timedelta

import pytest

from forex_toolkit.monte_carlo import simulate_summary
from forex_toolkit.risk_budget import ClosedTrade, RiskLimits, risk_budget_summary
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
        "window.__events=[];"
        "window.goatcounter={count:function(x){window.__events.push(x.path)}};"
    )
    page.goto(f"{site_url}/{prefix}")
    form = page.locator("form.md-feedback")
    assert form.is_visible()
    assert form.locator(".md-feedback__title").inner_text() == title
    form.locator('button[data-md-value="1"]').click()
    assert (
        page.evaluate("window.__events.filter(x => x === 'feedback_yes').length") == 1
    )
    page.reload()
    assert page.locator(".md-feedback__list").is_hidden()


@pytest.mark.parametrize(
    "path", ["/", "/tools/trade-desk/", "/en/tools/trade-desk/", "/uz/offline/"]
)
def test_pwa_manifest_and_icon_resolve_at_every_depth(pw_page, site_url, path):
    """base_url has no trailing slash, so a missing "/" silently 404s the manifest."""
    page = pw_page
    page.goto(f"{site_url}{path}")
    for selector in ('link[rel="manifest"]', 'link[rel="apple-touch-icon"]'):
        status = page.evaluate(
            "sel => fetch(document.querySelector(sel).href).then(r => r.status)",
            selector,
        )
        assert status == 200, f"{selector} broken on {path}"


def test_risk_budget_matches_python(pw_page, site_url):
    """Two implementations of the same guard drift silently without this check."""
    page = pw_page
    page.goto(f"{site_url}/tools/trade-desk/")
    page.evaluate(
        """
        () => {
          localStorage.setItem('forex_trade_drafts_v1', JSON.stringify([
            {id: 'o1', status: 'open', risk_pct: 1.5, risk_usd: 150},
            {id: 'o2', status: 'open', risk_pct: 0.8, risk_usd: 80},
            {id: 'p1', status: 'plan', risk_pct: 0.5, risk_usd: 50}
          ]));
          const d = back => {
            const t = new Date();
            const x = new Date(t.getFullYear(), t.getMonth(), t.getDate() - back);
            return x.getFullYear() + '-' + String(x.getMonth() + 1).padStart(2, '0')
              + '-' + String(x.getDate()).padStart(2, '0');
          };
          // Все три дня лежат в текущей неделе только начиная со среды; тест
          // сравнивает JS и Python на одних и тех же данных, поэтому сдвиг
          // недели одинаково влияет на обе стороны.
          localStorage.setItem('forex_journal_risk_history_v1', JSON.stringify([
            {id: 'h1', date: d(2), r: -1}, {id: 'h2', date: d(1), r: -1},
            {id: 'h3', date: d(0), r: -1.2}
          ]));
        }
        """
    )
    page.reload()
    page.click("#td-calc")
    actual = page.evaluate(
        "() => JSON.parse(JSON.stringify(window.__fxRiskBudget || null))"
    )
    assert actual is not None, "trade-desk must expose the budget for parity checks"

    today = date.today()
    expected = risk_budget_summary(
        planned_percent=0.5,
        open_percent=2.3,
        new_percent=actual["new_percent"],
        trades=[
            ClosedTrade(today - timedelta(days=2), -1.0),
            ClosedTrade(today - timedelta(days=1), -1.0),
            ClosedTrade(today, -1.2),
        ],
        limits=RiskLimits(),
        today=today,
    )
    for key in (
        "planned_percent",
        "open_percent",
        "after_percent",
        "remaining_open_percent",
        "daily_r",
        "weekly_r",
        "remaining_daily_r",
        "remaining_weekly_r",
        "loss_streak",
        "requires_confirmation",
        "reasons",
    ):
        assert actual[key] == pytest.approx(expected[key]), f"{key} drifted"


def test_strategy_name_from_backup_cannot_inject_html(pw_page, site_url):
    """Backups are shared between people, so a strategy name is untrusted input."""
    page = pw_page
    page.goto(f"{site_url}/tools/trade-desk/")
    page.evaluate(
        """
        () => localStorage.setItem('forex_strategy_playbooks_v1', JSON.stringify([{
          id: 'x1', baseId: 'x1', version: 1, active: true,
          name: '</option><img src=x onerror="window.__pwned=true">',
          session: 'London', timeframe: 'H1', entryRules: 'r',
          invalidation: 'i', maxRiskPct: 0.5, targetTrades: 30
        }]))
        """
    )
    page.reload()
    assert page.evaluate("window.__pwned === true") is False
    assert page.evaluate("document.querySelectorAll('#td-strategy img').length") == 0
    assert "onerror" in page.locator("#td-strategy option").nth(1).inner_text()


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
        "window.__events=[];"
        "window.goatcounter={count:function(x){window.__events.push(x)}};"
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
    draft = page.evaluate(
        "JSON.parse(localStorage.getItem('forex_trade_drafts_v1'))[0]"
    )
    assert draft["pair"] == "EURUSD"
    assert draft["lot_size"] == 0.05
    assert draft["status"] == "plan"
    assert "planned_reason" in draft
    assert page.locator("#td-journal").is_enabled()
    assert page.locator("#td-download").is_enabled()


def test_trade_desk_requires_explicit_risk_limit_confirmation(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/trade-desk/")
    page.evaluate(
        """
        () => localStorage.setItem('forex_trade_drafts_v1', JSON.stringify([{
          id: 'open-1', status: 'open', risk_pct: 1.5, risk_usd: 15,
          pair: 'GBPUSD', direction: 'long'
        }]))
        """
    )
    page.reload()
    page.click("#td-calc")
    assert "2.50%" in page.locator("#td-risk-budget").inner_text()
    assert page.locator("#td-risk-override-wrap").is_visible()
    page.locator("#td-checks input").evaluate_all(
        "inputs => inputs.forEach(input => { input.checked = true; })"
    )
    page.click("#td-save")
    assert (
        page.evaluate(
            "JSON.parse(localStorage.getItem('forex_trade_drafts_v1')).length"
        )
        == 1
    )
    assert "Лимит риска превышен" in page.locator("#td-status").inner_text()
    page.check("#td-risk-override")
    page.click("#td-save")
    plans = page.evaluate("JSON.parse(localStorage.getItem('forex_trade_drafts_v1'))")
    assert len(plans) == 2
    assert plans[0]["risk_guard"]["confirmed_override"] is True


def test_strategy_lab_versions_rules_and_snapshots_plan(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/trade-desk/")
    page.fill("#sl-name", "London Pullback")
    page.fill("#sl-entry", "Sweep and H1 close above structure")
    page.fill("#sl-invalidation", "Close below the sweep")
    page.click("#sl-save")
    assert page.locator(".strategy-card").count() == 1
    page.fill("#sl-entry", "Sweep, retest and H1 close above structure")
    page.click("#sl-save")
    assert page.locator(".strategy-card").count() == 2
    versions = page.evaluate(
        "JSON.parse(localStorage.getItem('forex_strategy_playbooks_v1'))"
        ".map(x => x.version)"
    )
    assert versions == [2, 1]
    strategy_id = page.locator("#td-strategy option").last.get_attribute("value")
    page.select_option("#td-strategy", strategy_id)
    page.click("#td-calc")
    page.locator("#td-checks input").evaluate_all(
        "inputs => inputs.forEach(input => { input.checked = true; })"
    )
    page.click("#td-save")
    plan = page.evaluate("JSON.parse(localStorage.getItem('forex_trade_drafts_v1'))[0]")
    assert plan["strategy"]["version"] == 2
    assert plan["strategy"]["entryRules"].startswith("Sweep, retest")


def test_monte_carlo_matches_python_fixture(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/monte-carlo/")
    page.fill("#mco-sims", "100")
    page.fill("#mco-trades", "50")
    page.click("#mco-run")
    values = page.locator("#mco-result .fx-metrics strong").all_inner_texts()
    expected = simulate_summary(100, 50, 0.45, 2, 1, seed=42)
    assert _number(values[0]) == pytest.approx(
        expected["median_final"] * 1000, abs=0.01
    )
    assert page.locator("#mco-chart").is_visible()
    assert page.locator("#mco-risk-comparison .fx-metrics > div").count() == 3


def test_first_15_minutes_collects_local_progress(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/first-15/")
    assert "0 / 4" in page.locator(".first-15-hero").inner_text()
    page.click("#first-15-basics")
    page.evaluate(
        """
        () => {
          const first = JSON.parse(localStorage.getItem('forex_first15_v1'));
          first.position = true;
          localStorage.setItem('forex_first15_v1', JSON.stringify(first));
          localStorage.setItem('forex_replay_stats', JSON.stringify({trades: 3}));
          localStorage.setItem('forex_trade_drafts_v1', JSON.stringify([{id: 'p1'}]));
        }
        """
    )
    page.reload()
    assert "4 / 4" in page.locator(".first-15-hero").inner_text()
    assert page.locator(".first-15-step.is-done").count() == 4


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
