"""Тесты для математики пакета: индикаторы, свечные паттерны, калькулятор позиции.

CLAUDE.md прямо требует проверять финансовую математику. Раньше прямых тестов на
``forex_toolkit.indicators``, ``forex_toolkit.candles`` и
``forex_toolkit.position_calculator`` не было — этот файл закрывает дыру.

Эталонные значения (EMA, Bollinger, ATR) выверены независимым расчётом, а не
снятием с самой реализации; остальное проверяется через математические
инварианты (границы RSI, симметрия полос Боллинджера, состав MACD).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from forex_toolkit.candles import (
    is_bearish_engulfing,
    is_bullish_engulfing,
    is_doji,
    is_hammer,
    is_shooting_star,
)
from forex_toolkit.indicators import atr, bollinger, ema, macd, rsi, sma
from forex_toolkit.position_calculator import calculate_position


class TestSMA:
    def test_known_values(self):
        # Скользящая средняя по 3 от [1..5]: первые два — NaN, дальше 2,3,4.
        s = pd.Series([1, 2, 3, 4, 5], dtype=float)
        out = sma(s, 3)
        assert np.isnan(out.iloc[0]) and np.isnan(out.iloc[1])
        assert list(out.iloc[2:]) == [2.0, 3.0, 4.0]

    def test_constant_series(self):
        s = pd.Series([7.0] * 10)
        assert sma(s, 5).iloc[-1] == 7.0


class TestEMA:
    def test_first_value_equals_input(self):
        # При adjust=False первое значение EMA совпадает с первым значением ряда.
        s = pd.Series([1, 2, 3, 4, 5], dtype=float)
        assert ema(s, 3).iloc[0] == 1.0

    def test_known_values_span3(self):
        # span=3 → alpha=0.5; ряд [1..5] даёт точную последовательность.
        s = pd.Series([1, 2, 3, 4, 5], dtype=float)
        expected = [1.0, 1.5, 2.25, 3.125, 4.0625]
        assert ema(s, 3).round(6).tolist() == expected

    def test_constant_series(self):
        s = pd.Series([42.0] * 20)
        assert ema(s, 10).iloc[-1] == pytest.approx(42.0)

    def test_bounded_by_series_range(self):
        s = pd.Series([1, 5, 2, 8, 3, 9, 4], dtype=float)
        e = ema(s, 3)
        assert e.min() >= s.min() - 1e-9
        assert e.max() <= s.max() + 1e-9


class TestRSI:
    def test_bounds(self):
        # RSI всегда в [0, 100] на любых осмысленных данных.
        rng = pd.Series(
            [
                10,
                11,
                10.5,
                12,
                11.5,
                13,
                12.5,
                14,
                13.5,
                15,
                14.5,
                16,
                15.5,
                17,
                16.5,
                18,
            ],
            dtype=float,
        )
        r = rsi(rng, 14).dropna()
        assert r.min() >= 0.0
        assert r.max() <= 100.0

    def test_bullish_bias_above_50(self):
        # Ряд с перевесом роста над откатами → RSI > 50.
        s = pd.Series(
            [
                10,
                11,
                10.5,
                12,
                11.5,
                13,
                12.5,
                14,
                13.5,
                15,
                14.5,
                16,
                15.5,
                17,
                16.5,
                18,
            ],
            dtype=float,
        )
        assert rsi(s, 14).iloc[-1] > 50.0

    def test_bearish_bias_below_50(self):
        # Зеркальный нисходящий ряд → RSI < 50.
        s = pd.Series(
            [
                18,
                16.5,
                17,
                15.5,
                16,
                14.5,
                15,
                13.5,
                14,
                12.5,
                13,
                11.5,
                12,
                10.5,
                11,
                10,
            ],
            dtype=float,
        )
        assert rsi(s, 14).iloc[-1] < 50.0

    def test_shift_invariance(self):
        # RSI зависит только от приращений: сдвиг всего ряда на константу
        # не меняет результат.
        s = pd.Series(
            [10, 11, 10.5, 12, 11.5, 13, 12.5, 14, 13.5, 15, 14.5, 16],
            dtype=float,
        )
        assert np.allclose(rsi(s, 14).values, rsi(s + 100, 14).values, equal_nan=True)

    def test_monotonic_up_returns_50_quirk(self):
        """Документирует КРАЙ: строго растущий ряд даёт 50, а не 100.

        Причина — ``avg_loss.replace(0, np.nan)`` в реализации: при полном
        отсутствии убытков rs становится NaN и затем ``fillna(50)`` отдаёт
        нейтральные 50. На реальных данных (где есть хоть какие-то откаты)
        этого не происходит — RSI корректно стремится к 100. Тест фиксирует
        текущее поведение, чтобы изменение формулы было замечено осознанно.
        """
        s = pd.Series(np.arange(1, 21), dtype=float)
        assert rsi(s, 14).iloc[-1] == pytest.approx(50.0)


class TestATR:
    def test_constant_true_range(self):
        # high-low=2 на каждом баре, гэпов нет → TR=2 → ATR=2 после прогрева.
        df = pd.DataFrame(
            {"open": [10] * 6, "high": [11] * 6, "low": [9] * 6, "close": [10] * 6}
        )
        assert atr(df, 3).iloc[-1] == pytest.approx(2.0)

    def test_non_negative(self):
        df = pd.DataFrame(
            {
                "open": [10, 11, 9, 12, 8, 13],
                "high": [11, 12, 11, 13, 10, 14],
                "low": [9, 10, 8, 11, 7, 12],
                "close": [10.5, 11.5, 10, 12.5, 9, 13.5],
            },
            dtype=float,
        )
        a = atr(df, 3).dropna()
        assert (a >= 0).all()


class TestBollinger:
    def test_known_values_period2(self):
        # period=2 на [10, 12]: середина=11, std(ddof=1)=sqrt(2),
        # верх=11+2*sqrt(2), низ=11-2*sqrt(2).
        u, m, lo = bollinger(pd.Series([10, 12], dtype=float), period=2, std_mult=2.0)
        assert m.iloc[-1] == pytest.approx(11.0)
        assert u.iloc[-1] == pytest.approx(11 + 2 * 2**0.5)
        assert lo.iloc[-1] == pytest.approx(11 - 2 * 2**0.5)

    def test_middle_equals_sma(self):
        s = pd.Series(np.arange(1, 30), dtype=float)
        _, m, _ = bollinger(s, period=20)
        assert np.allclose(m.dropna().values, sma(s, 20).dropna().values)

    def test_symmetric_around_middle(self):
        s = pd.Series([1, 3, 2, 5, 4, 7, 6, 9, 8, 11], dtype=float)
        u, m, lo = bollinger(s, period=5, std_mult=2.0)
        # Полосы симметричны: верх − середина == середина − низ.
        assert np.allclose((u - m).dropna().values, (m - lo).dropna().values)

    def test_constant_series_collapses(self):
        # На плоском ряду std=0 → все три линии совпадают.
        s = pd.Series([5.0] * 25)
        u, m, lo = bollinger(s, period=20)
        assert u.iloc[-1] == pytest.approx(m.iloc[-1]) == pytest.approx(lo.iloc[-1])


class TestMACD:
    def test_line_is_fast_minus_slow_ema(self):
        s = pd.Series(np.linspace(1, 50, 60) + np.sin(np.arange(60)))
        macd_line, _, _ = macd(s)
        assert np.allclose(macd_line.values, (ema(s, 12) - ema(s, 26)).values)

    def test_histogram_is_line_minus_signal(self):
        s = pd.Series(np.linspace(1, 50, 60) + np.sin(np.arange(60)))
        macd_line, signal, hist = macd(s)
        assert np.allclose(hist.values, (macd_line - signal).values)


class TestCandles:
    def _row(self, o, h, low, c):
        return pd.Series({"open": o, "high": h, "low": low, "close": c})

    def test_hammer(self):
        # Длинная нижняя тень (0.6), маленькое тело (0.2), почти нет верхней (0.05).
        assert is_hammer(self._row(10.0, 10.25, 9.4, 10.2))
        # Обычная свеча — не молот.
        assert not is_hammer(self._row(10.0, 11.0, 9.0, 10.8))
        # Тело нулевое → не молот (защита от деления).
        assert not is_hammer(self._row(10.0, 10.5, 9.5, 10.0))

    def test_shooting_star(self):
        # Длинная верхняя тень (0.6), маленькое тело (0.1), короткая нижняя (0.05).
        assert is_shooting_star(self._row(10.0, 10.6, 9.85, 9.9))
        # Это молот, а не звезда.
        assert not is_shooting_star(self._row(10.0, 10.25, 9.4, 10.2))

    def test_doji(self):
        # Тело 0.01 при диапазоне 1.0 → 1% < 10% порога.
        assert is_doji(self._row(10.0, 10.5, 9.5, 10.01))
        # Крупное тело → не доджи.
        assert not is_doji(self._row(10.0, 10.6, 9.9, 10.5))

    def test_bullish_engulfing(self):
        prev = self._row(11.0, 11.1, 9.9, 10.0)  # медвежья, тело 1.0
        curr = self._row(9.9, 11.3, 9.8, 11.2)  # бычья, накрывает, тело 1.3
        assert is_bullish_engulfing(prev, curr)
        # Если текущая не бычья — не поглощение.
        assert not is_bullish_engulfing(prev, prev)

    def test_bearish_engulfing(self):
        prev = self._row(10.0, 11.1, 9.9, 11.0)  # бычья, тело 1.0
        curr = self._row(11.2, 11.3, 9.7, 9.8)  # медвежья, накрывает, тело 1.4
        assert is_bearish_engulfing(prev, curr)
        assert not is_bearish_engulfing(prev, prev)


class TestCalculatePosition:
    def test_known_case(self):
        # $1000, риск 1% = $10, стоп 25 пипсов, EUR/USD ($10/пипс) → 0.04 лота.
        r = calculate_position(1000, 1.0, 25, "EURUSD")
        assert r.lots_rounded == 0.04
        assert r.actual_risk == pytest.approx(10.0)
        assert r.actual_risk_percent == pytest.approx(1.0)
        assert r.risk_exceeds_plan is False

    def test_rounds_down_to_step(self):
        # Сырой лот 0.0151 → округление вниз до 0.01.
        r = calculate_position(1000, 0.5, 33, "EURUSD")
        assert r.lots_rounded == 0.01

    def test_actual_risk_never_exceeds_plan_when_not_floored(self):
        """Главное защитное свойство: округление ВНИЗ не даёт превысить план.

        Действует, пока лот не упёрся в минимальные 0.01 (см. отдельный тест).
        """
        r = calculate_position(5000, 1.0, 37, "GBPUSD")
        assert r.lots_rounded < r.lots  # округлили вниз
        assert r.actual_risk <= r.risk_amount + 1e-9

    def test_min_lot_floor_can_exceed_planned_risk(self):
        """Край: на крошечном депозите лот поднимается до 0.01, и фактический
        риск превышает плановый. Это НЕ должно быть тихим — калькулятор обязан
        выставить флаг risk_exceeds_plan, чтобы виджет/CLI предупредили."""
        r = calculate_position(100, 0.5, 50, "EURUSD")  # план $0.50
        assert r.lots_rounded == 0.01
        assert r.actual_risk > r.risk_amount
        assert r.risk_exceeds_plan is True

    def test_risk_exceeds_plan_false_for_normal_account(self):
        # На нормальном депозите флаг не должен срабатывать.
        r = calculate_position(5000, 1.0, 37, "GBPUSD")
        assert r.risk_exceeds_plan is False

    def test_normalizes_pair_format(self):
        r = calculate_position(1000, 1.0, 25, "eur/usd")
        assert r.pair == "EURUSD"

    @pytest.mark.parametrize(
        "balance,risk,stop,pair",
        [
            (0, 1.0, 25, "EURUSD"),  # депозит ≤ 0
            (1000, 0, 25, "EURUSD"),  # риск ≤ 0
            (1000, 11, 25, "EURUSD"),  # риск > 10%
            (1000, 1.0, 0, "EURUSD"),  # стоп ≤ 0
            (1000, 1.0, 25, "XXXYYY"),  # неизвестная пара
        ],
    )
    def test_invalid_inputs_raise(self, balance, risk, stop, pair):
        with pytest.raises(ValueError):
            calculate_position(balance, risk, stop, pair)
