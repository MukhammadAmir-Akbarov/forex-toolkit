from datetime import date

import pytest

from forex_toolkit.risk_budget import ClosedTrade, RiskLimits, risk_budget_summary


def test_risk_budget_combines_open_and_new_risk() -> None:
    summary = risk_budget_summary(
        planned_percent=0.5,
        open_percent=1.25,
        new_percent=1.0,
        trades=[],
        limits=RiskLimits(max_open_percent=2),
        today=date(2026, 8, 6),
    )

    assert summary["after_percent"] == pytest.approx(2.25)
    assert summary["remaining_open_percent"] == 0
    assert summary["reasons"] == ["open_risk"]
    assert summary["requires_confirmation"] is True


def test_risk_budget_tracks_day_week_and_latest_loss_streak() -> None:
    trades = [
        ClosedTrade(date(2026, 8, 3), -1),
        ClosedTrade(date(2026, 8, 5), -1.25),
        ClosedTrade(date(2026, 8, 6), -1),
    ]
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0.5,
        new_percent=0.5,
        trades=trades,
        limits=RiskLimits(daily_loss_r=1, weekly_loss_r=3, pause_after_losses=3),
        today=date(2026, 8, 6),
    )

    assert summary["daily_r"] == pytest.approx(-1)
    assert summary["weekly_r"] == pytest.approx(-3.25)
    assert summary["loss_streak"] == 3
    assert summary["reasons"] == ["daily_loss", "weekly_loss", "loss_streak"]


def test_risk_limits_reject_invalid_values() -> None:
    with pytest.raises(ValueError):
        RiskLimits(max_open_percent=0)
