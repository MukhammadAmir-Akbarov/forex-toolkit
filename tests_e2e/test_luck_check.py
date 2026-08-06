"""Сверка проверки «навык или везение»: браузер == Python."""

from __future__ import annotations

import json

import pytest

from forex_toolkit.edge_test import luck_probability

# (сделок, итог R, средний выигрыш R, средний убыток R)
CASES = [
    (20, 6.0, 1.0, 1.0),
    (100, 30.0, 1.0, 1.0),
    (200, 8.0, 1.0, 1.0),
    (50, 12.0, 2.0, 1.0),
    (40, -5.0, 1.0, 1.0),
]


def seed_journal_profile(page, trades, total_r, avg_win, avg_loss):
    page.evaluate(
        """
        ([trades, totalR, avgWinR, avgLossR]) => {
          const key = 'forex_tool_settings_v1';
          const settings = JSON.parse(localStorage.getItem(key) || '{}');
          settings.monteCarlo = {
            source: 'journal', sampleSize: trades, trades: Math.max(10, trades),
            winRate: 50, rewardRisk: avgWinR / avgLossR,
            totalR: totalR, avgWinR: avgWinR, avgLossR: avgLossR,
            updatedAt: new Date().toISOString()
          };
          localStorage.setItem(key, JSON.stringify(settings));
        }
        """,
        [trades, total_r, avg_win, avg_loss],
    )


@pytest.mark.parametrize(("trades", "total_r", "avg_win", "avg_loss"), CASES)
def test_luck_check_matches_python(
    pw_page, site_url, trades, total_r, avg_win, avg_loss
):
    page = pw_page
    page.goto(f"{site_url}/tools/monte-carlo/")
    seed_journal_profile(page, trades, total_r, avg_win, avg_loss)
    page.reload()

    actual = page.evaluate("() => window.__fxLuck")
    assert actual is not None, "виджет должен опубликовать результат для сверки"

    expected = luck_probability(
        trades=trades,
        observed_total_r=total_r,
        avg_win_r=avg_win,
        avg_loss_r=avg_loss,
        simulations=5000,
        seed=42,
    )
    assert actual["probability"] == pytest.approx(expected["probability"])
    assert actual["verdict"] == expected["verdict"]
    assert actual["breakeven_win_rate"] == pytest.approx(expected["breakeven_win_rate"])
    assert actual["median_random_r"] == pytest.approx(expected["median_random_r"])


def test_short_sample_refuses_to_judge(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/monte-carlo/")
    seed_journal_profile(page, 5, 4.0, 1.0, 1.0)
    page.reload()
    panel = page.locator("#mco-luck")
    panel.wait_for(state="visible")
    assert "этого мало" in panel.inner_text()
    assert page.evaluate("() => window.__fxLuck.verdict") == "not_enough"


def test_panel_is_hidden_without_journal_data(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/monte-carlo/")
    assert page.locator("#mco-luck").is_hidden()


def test_modest_plus_on_short_sample_is_called_out(pw_page, site_url):
    """Главный сценарий: +6R за 20 сделок не повод поднимать риск."""
    page = pw_page
    page.goto(f"{site_url}/tools/monte-carlo/")
    seed_journal_profile(page, 20, 6.0, 1.0, 1.0)
    page.reload()
    panel = page.locator("#mco-luck")
    panel.wait_for(state="visible")
    text = panel.inner_text()
    assert "выборки не хватает" in text or "рано" in text
    assert json.loads(page.evaluate("() => JSON.stringify(window.__fxLuck)"))[
        "verdict"
    ] in {"luck", "unclear"}
