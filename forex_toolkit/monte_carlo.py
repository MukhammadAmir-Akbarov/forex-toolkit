"""Deterministic Monte Carlo engine shared with the browser implementation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ParkMiller:
    state: int

    def __post_init__(self) -> None:
        self.state %= 2_147_483_647
        if self.state <= 0:
            self.state = 1

    def random(self) -> float:
        self.state = self.state * 48_271 % 2_147_483_647
        return (self.state - 1) / 2_147_483_646


def percentile(values: list[float], percent: float) -> float:
    if not values:
        raise ValueError("values cannot be empty")
    ordered = sorted(values)
    index = (len(ordered) - 1) * percent / 100
    lower = int(index)
    fraction = index - lower
    if lower + 1 >= len(ordered):
        return ordered[lower]
    return ordered[lower] + (ordered[lower + 1] - ordered[lower]) * fraction


def simulate_summary(
    simulations: int,
    trades: int,
    win_rate: float,
    reward_risk: float,
    risk_percent: float,
    seed: int = 42,
    ruin_fraction: float = 0.5,
) -> dict[str, float]:
    if simulations <= 0 or trades <= 0:
        raise ValueError("simulations and trades must be positive")
    if not 0 <= win_rate <= 1 or reward_risk <= 0 or not 0 < risk_percent < 100:
        raise ValueError("invalid strategy parameters")
    rng = ParkMiller(seed)
    risk = risk_percent / 100
    finals: list[float] = []
    drawdowns: list[float] = []
    streaks: list[float] = []
    ruined = 0
    for _ in range(simulations):
        equity = peak = 1.0
        max_drawdown = 0.0
        losing_streak = max_losing_streak = 0
        hit_ruin = False
        for _ in range(trades):
            if rng.random() < win_rate:
                equity *= 1 + risk * reward_risk
                losing_streak = 0
            else:
                equity *= 1 - risk
                losing_streak += 1
                max_losing_streak = max(max_losing_streak, losing_streak)
            peak = max(peak, equity)
            max_drawdown = max(max_drawdown, (peak - equity) / peak)
            hit_ruin = hit_ruin or equity <= ruin_fraction
        finals.append(equity)
        drawdowns.append(max_drawdown)
        streaks.append(float(max_losing_streak))
        ruined += int(hit_ruin)
    return {
        "median_final": percentile(finals, 50),
        "p05_final": percentile(finals, 5),
        "median_drawdown": percentile(drawdowns, 50),
        "p95_drawdown": percentile(drawdowns, 95),
        "probability_loss": sum(value < 1 for value in finals) / simulations,
        "probability_drawdown_20": (
            sum(value >= 0.2 for value in drawdowns) / simulations
        ),
        "probability_ruin": ruined / simulations,
        "p95_losing_streak": percentile(streaks, 95),
    }
