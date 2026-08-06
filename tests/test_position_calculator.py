"""Тесты для position_calculator."""

from __future__ import annotations

import pytest

from position_calculator import calculate_position, PIP_VALUE_USD_PER_LOT


class TestCalculatePosition:
    def test_basic_calculation(self):
        """Стандартный сценарий: $1000 риск 0.5% стоп 25 пипсов EUR/USD."""
        r = calculate_position(1000, 0.5, 25, "EURUSD")
        assert r.risk_amount == 5.0
        assert r.lots == pytest.approx(0.02, abs=0.001)
        assert r.lots_rounded == 0.02
        assert r.actual_risk == pytest.approx(5.0, abs=0.01)

    def test_rounds_down(self):
        """Округление ВНИЗ — реальный риск не должен превышать запланированный."""
        # 5000 / (33 * 10) = 0.01515... → должно округлиться до 0.01, не 0.02
        r = calculate_position(1000, 0.5, 33, "EURUSD")
        # 0.0152 -> floor to 0.01
        assert r.lots_rounded == 0.01

    def test_min_lot(self):
        """При слишком маленьком размере — округляется до минимума 0.01."""
        # Очень маленький депозит, большой стоп
        r = calculate_position(100, 0.5, 100, "EURUSD")
        assert r.lots_rounded == 0.01

    def test_invalid_balance(self):
        with pytest.raises(ValueError, match="Депозит"):
            calculate_position(0, 1, 25, "EURUSD")
        with pytest.raises(ValueError, match="Депозит"):
            calculate_position(-100, 1, 25, "EURUSD")

    def test_invalid_risk(self):
        with pytest.raises(ValueError, match="Риск"):
            calculate_position(1000, 0, 25, "EURUSD")
        with pytest.raises(ValueError, match="Риск"):
            calculate_position(1000, 15, 25, "EURUSD")  # > 10%

    def test_invalid_stop(self):
        with pytest.raises(ValueError, match="[Сс]топ"):
            calculate_position(1000, 1, 0, "EURUSD")
        with pytest.raises(ValueError, match="[Сс]топ"):
            calculate_position(1000, 1, -5, "EURUSD")

    def test_unknown_pair(self):
        with pytest.raises(ValueError, match="не в таблице"):
            calculate_position(1000, 1, 25, "UNKNOWN")

    def test_pair_normalization(self):
        """EUR/USD, EUR-USD, eurusd должны работать одинаково."""
        for variant in ["EURUSD", "EUR/USD", "EUR-USD", "eurusd"]:
            r = calculate_position(1000, 0.5, 25, variant)
            assert r.pair == "EURUSD"

    def test_jpy_pair_smaller_pip(self):
        """USD/JPY имеет меньшую стоимость пипса."""
        r_eur = calculate_position(1000, 1, 25, "EURUSD")
        r_jpy = calculate_position(1000, 1, 25, "USDJPY")
        # JPY: стоимость пипса меньше → размер позиции больше
        assert r_jpy.lots > r_eur.lots

    def test_pip_values_consistent(self):
        """Все мажоры с USD как quote дают $10/пипс."""
        for pair in ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD"]:
            assert PIP_VALUE_USD_PER_LOT[pair] == 10.0
