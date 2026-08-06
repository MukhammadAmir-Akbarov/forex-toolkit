import pytest

from forex_toolkit.risk_exposure import (
    Position,
    allocate_risk,
    currency_exposure,
    effective_risk,
    lot_size,
    risk_summary,
)


def test_correlated_positions_raise_effective_risk() -> None:
    positions = [Position("EUR/USD", "long", 10), Position("GBPUSD", "long", 10)]
    assert effective_risk(positions) == pytest.approx(19.235384, rel=1e-6)


def test_opposite_direction_reduces_correlated_risk() -> None:
    positions = [Position("EURUSD", "long", 10), Position("GBPUSD", "short", 10)]
    assert effective_risk(positions) == pytest.approx(5.477226, rel=1e-6)


def test_currency_exposure_respects_base_quote_and_direction() -> None:
    result = currency_exposure(
        [
            Position("EURUSD", "long", 10),
            Position("USDJPY", "short", 5),
        ]
    )
    assert result == {"EUR": 10, "USD": -15, "JPY": 5}


def test_allocation_lots_and_summary() -> None:
    allocations = allocate_risk(20, [20, 40])
    assert allocations == [10, 10]
    assert lot_size(10, 20, 10) == pytest.approx(0.05)
    summary = risk_summary(1000, 2, [Position("EURUSD", "long", 10)])
    assert summary["remaining_usd"] == 10
    assert summary["nominal_percent"] == 1


@pytest.mark.parametrize(
    "position",
    [
        ("EUR", "long", 1),
        ("EURUSD", "buy", 1),
        ("EURUSD", "long", -1),
    ],
)
def test_invalid_position(position: tuple[str, str, float]) -> None:
    with pytest.raises(ValueError):
        Position(*position)
