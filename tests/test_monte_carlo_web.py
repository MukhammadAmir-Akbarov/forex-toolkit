import pytest

from forex_toolkit.monte_carlo import ParkMiller, percentile, simulate_summary


def test_park_miller_is_reproducible() -> None:
    rng = ParkMiller(42)
    assert [rng.random() for _ in range(3)] == pytest.approx(
        [0.0009440733124241574, 0.5713628638269034, 0.2568094229854731]
    )


def test_percentile_interpolates() -> None:
    assert percentile([1, 2, 3, 4], 50) == 2.5


def test_summary_fixture() -> None:
    result = simulate_summary(100, 50, 0.45, 2, 1, seed=42)
    assert result["median_final"] == pytest.approx(1.2021376653156204)
    assert result["p95_losing_streak"] >= 7
    assert 0 <= result["probability_drawdown_20"] <= 1
