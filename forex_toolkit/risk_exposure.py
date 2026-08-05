"""Portfolio-level risk sizing and currency exposure helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass

CORRELATIONS: dict[tuple[str, str], float] = {
    ("EURUSD", "GBPUSD"): 0.85,
    ("EURUSD", "AUDUSD"): 0.75,
    ("EURUSD", "NZDUSD"): 0.70,
    ("EURUSD", "USDCHF"): -0.95,
    ("EURUSD", "USDJPY"): -0.30,
    ("GBPUSD", "AUDUSD"): 0.65,
    ("GBPUSD", "USDCHF"): -0.85,
    ("USDJPY", "USDCHF"): 0.40,
    ("AUDUSD", "NZDUSD"): 0.90,
    ("EURJPY", "GBPJPY"): 0.85,
    ("EURUSD", "EURJPY"): 0.55,
}


def normalize_pair(pair: str) -> str:
    value = pair.upper().replace("/", "").replace(" ", "")
    if len(value) != 6 or not value.isalpha():
        raise ValueError("pair must contain two three-letter currency codes")
    return value


def get_correlation(pair_a: str, pair_b: str) -> float:
    a, b = normalize_pair(pair_a), normalize_pair(pair_b)
    if a == b:
        return 1.0
    return CORRELATIONS.get((a, b), CORRELATIONS.get((b, a), 0.0))


@dataclass(frozen=True)
class Position:
    pair: str
    direction: str
    risk_usd: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "pair", normalize_pair(self.pair))
        direction = self.direction.lower()
        if direction not in {"long", "short"}:
            raise ValueError("direction must be long or short")
        if not math.isfinite(self.risk_usd) or self.risk_usd < 0:
            raise ValueError("risk_usd must be a non-negative finite number")
        object.__setattr__(self, "direction", direction)


def effective_risk(positions: list[Position]) -> float:
    """Return covariance-style risk using the static correlation table."""
    variance = sum(position.risk_usd**2 for position in positions)
    for index, first in enumerate(positions):
        first_sign = 1 if first.direction == "long" else -1
        for second in positions[index + 1 :]:
            second_sign = 1 if second.direction == "long" else -1
            variance += (
                2
                * get_correlation(first.pair, second.pair)
                * first_sign
                * second_sign
                * first.risk_usd
                * second.risk_usd
            )
    return math.sqrt(max(0.0, variance))


def currency_exposure(positions: list[Position]) -> dict[str, float]:
    """Return signed risk proxies per base and quote currency."""
    exposure: dict[str, float] = {}
    for position in positions:
        base, quote = position.pair[:3], position.pair[3:]
        sign = 1 if position.direction == "long" else -1
        exposure[base] = exposure.get(base, 0.0) + sign * position.risk_usd
        exposure[quote] = exposure.get(quote, 0.0) - sign * position.risk_usd
    return {code: value for code, value in exposure.items() if abs(value) > 1e-9}


def allocate_risk(
    total_risk_usd: float,
    stop_pips: list[float],
    method: str = "equal",
) -> list[float]:
    if total_risk_usd < 0 or not math.isfinite(total_risk_usd):
        raise ValueError("total_risk_usd must be non-negative")
    if not stop_pips or any(stop <= 0 or not math.isfinite(stop) for stop in stop_pips):
        raise ValueError("stop_pips must contain positive finite values")
    if method == "equal":
        return [total_risk_usd / len(stop_pips)] * len(stop_pips)
    if method == "weighted":
        weights = [1 / stop for stop in stop_pips]
        total_weight = sum(weights)
        return [total_risk_usd * weight / total_weight for weight in weights]
    raise ValueError("method must be equal or weighted")


def lot_size(risk_usd: float, stop_pips: float, pip_value: float = 10.0) -> float:
    if risk_usd < 0 or stop_pips <= 0 or pip_value <= 0:
        raise ValueError(
            "risk must be non-negative; stop and pip value must be positive"
        )
    return risk_usd / (stop_pips * pip_value)


def risk_summary(
    deposit: float,
    limit_percent: float,
    positions: list[Position],
) -> dict[str, object]:
    if deposit <= 0 or limit_percent <= 0:
        raise ValueError("deposit and limit_percent must be positive")
    nominal = sum(position.risk_usd for position in positions)
    effective = effective_risk(positions)
    budget = deposit * limit_percent / 100
    return {
        "nominal_usd": nominal,
        "nominal_percent": nominal / deposit * 100,
        "effective_usd": effective,
        "effective_percent": effective / deposit * 100,
        "budget_usd": budget,
        "remaining_usd": max(0.0, budget - nominal),
        "over_budget": nominal > budget,
        "currency_exposure": currency_exposure(positions),
    }
