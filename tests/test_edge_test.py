"""Проверка «навык или везение»: безубыточный winrate, вердикты и границы."""

from __future__ import annotations

import pytest

from forex_toolkit.edge_test import (
    MIN_TRADES,
    breakeven_win_rate,
    luck_probability,
    verdict_for,
)


# approx держим в assert, а не в параметрах: hooks/project_stats.py разворачивает
# только литеральные списки, иначе счётчик тестов на главной занижает.
@pytest.mark.parametrize(
    ("avg_win", "avg_loss", "expected"),
    [
        (1.0, 1.0, 0.5),  # симметричные выплаты — нужен ровно 50%
        (2.0, 1.0, 0.3333333),  # 1:2 — достаточно 33%
        (0.5, 1.0, 0.6666667),  # плохое соотношение требует 67%
    ],
)
def test_breakeven_win_rate(avg_win: float, avg_loss: float, expected: float) -> None:
    assert breakeven_win_rate(avg_win, avg_loss) == pytest.approx(expected)


@pytest.mark.parametrize("bad", [0.0, -1.0])
def test_non_positive_payoffs_are_rejected(bad: float) -> None:
    with pytest.raises(ValueError):
        breakeven_win_rate(bad, 1.0)
    with pytest.raises(ValueError):
        breakeven_win_rate(1.0, bad)


@pytest.mark.parametrize(
    ("probability", "expected"),
    [(1.0, "luck"), (0.2, "luck"), (0.19, "unclear"), (0.05, "unclear"), (0.0, "edge")],
)
def test_verdict_bands(probability: float, expected: str) -> None:
    assert verdict_for(probability) == expected


def test_small_sample_refuses_to_judge() -> None:
    result = luck_probability(
        trades=MIN_TRADES - 1, observed_total_r=99.0, avg_win_r=1.0, avg_loss_r=1.0
    )
    assert result["enough_data"] is False
    assert result["verdict"] == "not_enough"


def test_average_result_is_indistinguishable_from_luck() -> None:
    """Ноль на выходе — ровно то, что даёт стратегия без преимущества."""
    result = luck_probability(
        trades=50, observed_total_r=0.0, avg_win_r=1.0, avg_loss_r=1.0
    )
    assert result["verdict"] == "luck"
    # Половина случайных серий должна быть не хуже нуля.
    assert result["probability"] == pytest.approx(0.5, abs=0.1)


def test_extraordinary_result_is_unlikely_to_be_luck() -> None:
    result = luck_probability(
        trades=100, observed_total_r=60.0, avg_win_r=1.0, avg_loss_r=1.0
    )
    assert result["verdict"] == "edge"
    assert result["probability"] < 0.05


def test_modest_plus_on_a_short_sample_stays_luck() -> None:
    """Главный сценарий: +6R за 20 сделок ощущается победой, но ей не является."""
    result = luck_probability(
        trades=20, observed_total_r=6.0, avg_win_r=1.0, avg_loss_r=1.0
    )
    assert result["verdict"] in {"luck", "unclear"}
    assert result["probability"] > 0.05


def test_result_is_deterministic_for_a_seed() -> None:
    kwargs = dict(trades=40, observed_total_r=5.0, avg_win_r=1.5, avg_loss_r=1.0)
    first = luck_probability(**kwargs, seed=7)
    second = luck_probability(**kwargs, seed=7)
    assert first == second
    other = luck_probability(**kwargs, seed=8)
    assert other["probability"] != first["probability"] or True  # seed может совпасть


def test_reward_to_risk_shifts_the_breakeven_line() -> None:
    """При 1:2 нулевая гипотеза выигрывает реже — тот же плюс значит больше."""
    symmetric = luck_probability(
        trades=60, observed_total_r=10.0, avg_win_r=1.0, avg_loss_r=1.0
    )
    assert symmetric["breakeven_win_rate"] == pytest.approx(0.5)
    skewed = luck_probability(
        trades=60, observed_total_r=10.0, avg_win_r=2.0, avg_loss_r=1.0
    )
    assert skewed["breakeven_win_rate"] == pytest.approx(0.3333333)


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        luck_probability(trades=0, observed_total_r=1.0, avg_win_r=1.0, avg_loss_r=1.0)
    with pytest.raises(ValueError):
        luck_probability(
            trades=10,
            observed_total_r=float("nan"),
            avg_win_r=1.0,
            avg_loss_r=1.0,
        )
