"""Тесты для остальных калькуляторов."""
from __future__ import annotations

import pytest

from pip_calculator import pip_size, pip_value_in_quote, pip_value_in_account_currency
from compound_calculator import project_growth
from margin_calculator import margin_required
from multi_position_sizer import calc_lots
from risk_exposure import get_correlation, effective_risk, Position


class TestPipCalculator:
    def test_pip_size_default(self):
        assert pip_size("EURUSD") == 0.0001
        assert pip_size("GBPUSD") == 0.0001

    def test_pip_size_jpy(self):
        assert pip_size("USDJPY") == 0.01
        assert pip_size("EURJPY") == 0.01

    def test_pip_value_in_quote(self):
        # 1 lot EURUSD = 100000 EUR, 1 pip = 0.0001 USD/EUR
        # → 100000 * 0.0001 = 10 USD
        assert pip_value_in_quote(1.0, "EURUSD") == 10.0
        # 0.01 lot → 0.10 USD
        assert pip_value_in_quote(0.01, "EURUSD") == pytest.approx(0.10)

    def test_pip_value_account_quote_currency(self):
        # USD счёт, EUR/USD пара → quote=USD → не нужна конвертация
        v = pip_value_in_account_currency(1.0, "EURUSD", "USD", 1.08)
        assert v == 10.0

    def test_pip_value_account_base_currency(self):
        # EUR счёт, EUR/USD пара → base=EUR → конвертация
        # 10 USD / 1.08 ≈ 9.26 EUR
        v = pip_value_in_account_currency(1.0, "EURUSD", "EUR", 1.08)
        assert v == pytest.approx(10.0 / 1.08, rel=0.01)


class TestCompoundCalculator:
    def test_zero_months(self):
        h = project_growth(1000, 5, 0)
        assert h == [1000]

    def test_positive_growth(self):
        h = project_growth(1000, 10, 12)
        # +10%/мес × 12 мес = 1.1^12 ≈ 3.138x
        assert h[-1] == pytest.approx(1000 * 1.1**12, rel=0.01)

    def test_with_monthly_deposit(self):
        h = project_growth(1000, 5, 12, monthly_deposit=100)
        # Депозит и пополнения растут — итог больше, чем без пополнений
        h_without = project_growth(1000, 5, 12)
        assert h[-1] > h_without[-1]


class TestMarginCalculator:
    def test_basic_margin(self):
        # 0.01 лот × 100000 × 1.08 / 30 = 36
        m = margin_required(0.01, 1.08, 30)
        assert m == pytest.approx(36.0, rel=0.01)

    def test_higher_leverage_lower_margin(self):
        m_30 = margin_required(0.01, 1.08, 30)
        m_500 = margin_required(0.01, 1.08, 500)
        assert m_500 < m_30


class TestMultiPositionSizer:
    def test_basic_lot_calc(self):
        # $10 риск, 25 пипсов стоп, $10/пипс → 0.04 лот точно, округление вниз
        lots = calc_lots(10, 25, 10)
        assert lots == 0.04

    def test_zero_stop(self):
        assert calc_lots(10, 0, 10) == 0

    def test_floor_rounding(self):
        # 5 / (33 × 10) ≈ 0.0151 → 0.01 (округлено вниз)
        lots = calc_lots(5, 33, 10)
        assert lots == 0.01


class TestRiskExposure:
    def test_self_correlation(self):
        assert get_correlation("EURUSD", "EURUSD") == 1.0

    def test_known_correlation(self):
        # EUR/USD и USD/CHF — почти обратная корреляция
        c = get_correlation("EURUSD", "USDCHF")
        assert c < -0.5

    def test_unknown_correlation(self):
        # Несуществующая пара → 0
        c = get_correlation("XAUUSD", "USDCAD")
        assert c == 0.0

    def test_effective_risk_increases_with_correlation(self):
        """Скоррелированные позиции в одну сторону увеличивают риск."""
        two_correlated = [
            Position("EURUSD", "long", 5),
            Position("GBPUSD", "long", 5),  # сильно скоррелированы
        ]
        correlated_risk = effective_risk(two_correlated)
        # Сильная корреляция повышает риск относительно независимых позиций,
        # но ковариационная оценка не превышает простую сумму стоп-рисков.
        assert correlated_risk > (5**2 + 5**2) ** 0.5
        assert correlated_risk < 10
