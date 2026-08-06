"""Daily, weekly and simultaneous risk-budget helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable


@dataclass(frozen=True)
class RiskLimits:
    """User-defined guardrails expressed in percent and R multiples."""

    max_open_percent: float = 2.0
    daily_loss_r: float = 2.0
    weekly_loss_r: float = 5.0
    pause_after_losses: int = 3

    def __post_init__(self) -> None:
        values = (self.max_open_percent, self.daily_loss_r, self.weekly_loss_r)
        if any(not math.isfinite(value) or value <= 0 for value in values):
            raise ValueError("risk limits must be positive finite numbers")
        if self.pause_after_losses < 1:
            raise ValueError("pause_after_losses must be positive")


@dataclass(frozen=True)
class ClosedTrade:
    closed_on: date
    result_r: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.result_r):
            raise ValueError("result_r must be finite")


def consecutive_losses(trades: Iterable[ClosedTrade]) -> int:
    """Count the latest uninterrupted run of negative-R trades."""
    ordered = sorted(trades, key=lambda trade: trade.closed_on)
    streak = 0
    for trade in reversed(ordered):
        if trade.result_r >= 0:
            break
        streak += 1
    return streak


def risk_budget_summary(
    *,
    planned_percent: float,
    open_percent: float,
    new_percent: float,
    trades: Iterable[ClosedTrade],
    limits: RiskLimits = RiskLimits(),
    today: date | None = None,
) -> dict[str, float | int | bool | list[str]]:
    """Return the risk state used by the browser pre-trade guard."""
    values = (planned_percent, open_percent, new_percent)
    if any(not math.isfinite(value) or value < 0 for value in values):
        raise ValueError("risk percentages must be non-negative finite numbers")

    current = today or date.today()
    week_start = current - timedelta(days=current.weekday())
    history = list(trades)
    daily_r = sum(t.result_r for t in history if t.closed_on == current)
    weekly_r = sum(t.result_r for t in history if week_start <= t.closed_on <= current)
    streak = consecutive_losses(history)
    after_percent = open_percent + new_percent
    reasons: list[str] = []
    if after_percent > limits.max_open_percent:
        reasons.append("open_risk")
    if daily_r <= -limits.daily_loss_r:
        reasons.append("daily_loss")
    if weekly_r <= -limits.weekly_loss_r:
        reasons.append("weekly_loss")
    if streak >= limits.pause_after_losses:
        reasons.append("loss_streak")

    return {
        "planned_percent": planned_percent,
        "open_percent": open_percent,
        "new_percent": new_percent,
        "after_percent": after_percent,
        "remaining_open_percent": max(0.0, limits.max_open_percent - after_percent),
        "daily_r": daily_r,
        "weekly_r": weekly_r,
        "remaining_daily_r": max(0.0, limits.daily_loss_r + daily_r),
        "remaining_weekly_r": max(0.0, limits.weekly_loss_r + weekly_r),
        "loss_streak": streak,
        "requires_confirmation": bool(reasons),
        "reasons": reasons,
    }
