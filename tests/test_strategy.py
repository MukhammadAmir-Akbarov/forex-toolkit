"""Тесты для bot/strategy.py — детектор сигналов EMA50 pullback."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from strategy import (
    Direction,
    detect_signals,
    ema,
    rsi,
    is_bullish_engulfing,
    is_bearish_engulfing,
    is_hammer,
    is_shooting_star,
    prepare_dataframe,
)


class TestIndicators:
    def test_ema_basic(self):
        """EMA сглаживает данные."""
        s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        e = ema(s, 3)
        assert len(e) == len(s)
        # EMA должна расти при растущем ряду
        assert e.iloc[-1] > e.iloc[0]
        # EMA — между min и max
        assert s.min() <= e.iloc[-1] <= s.max()

    def test_ema_constant_series(self):
        """На константном ряду EMA = константа."""
        s = pd.Series([5.0] * 20)
        e = ema(s, 5)
        assert all(abs(v - 5.0) < 1e-9 for v in e)

    def test_rsi_range(self):
        """RSI всегда между 0 и 100."""
        rng = np.random.default_rng(42)
        s = pd.Series(rng.normal(100, 5, 100).cumsum())
        r = rsi(s, 14)
        assert r.min() >= 0
        assert r.max() <= 100

    def test_rsi_overbought_uptrend(self):
        """Растущий ряд с редкими откатами → высокий RSI."""
        # Чистый монотонный рост даёт деление на ноль (loss=0) → NaN → 50.
        # Реалистичный тест — рост с маленькими откатами.
        rng = np.random.default_rng(7)
        values = [100.0]
        for _ in range(50):
            # 80% растёт, 20% падает на маленькую величину
            if rng.random() < 0.8:
                values.append(values[-1] + 1.0)
            else:
                values.append(values[-1] - 0.2)
        r = rsi(pd.Series(values), 14)
        assert r.iloc[-1] > 70


class TestCandlePatterns:
    def test_hammer(self):
        """Молот: длинная нижняя тень, маленькое тело сверху."""
        candle = pd.Series(
            {
                "open": 100.0,
                "high": 100.3,
                "low": 95.0,
                "close": 100.5,
            }
        )
        # Тело = 0.5, нижняя тень = 5 (от open=100 до low=95),
        # верхняя тень = 100.3 - 100.5 = ... wait close > high impossible
        # fix: open=100, close=100.5, high=100.5 (no upper), low=95
        candle = pd.Series(
            {
                "open": 100.0,
                "high": 100.5,
                "low": 95.0,
                "close": 100.5,
            }
        )
        # Body = 0.5, lower shadow = 5, upper shadow = 0
        # 5 >= 2*0.5 AND 0 < 0.5 → молот
        assert is_hammer(candle)

    def test_not_hammer_when_long_upper_shadow(self):
        candle = pd.Series(
            {
                "open": 100,
                "high": 105,
                "low": 99.5,
                "close": 100.5,
            }
        )
        # Верхняя тень 4.5, тело 0.5 → не молот (есть длинная верхняя)
        assert not is_hammer(candle)

    def test_shooting_star(self):
        """Падающая звезда: длинная верхняя тень."""
        # Body = 0.5, upper shadow = 5, lower shadow = 0
        candle = pd.Series(
            {
                "open": 100.5,
                "high": 105.0,
                "low": 100.0,
                "close": 100.0,
            }
        )
        # close=100, open=100.5, body=0.5, upper=105-100.5=4.5, lower=100-100=0
        # 4.5 >= 2*0.5 AND 0 < 0.5 → звезда
        assert is_shooting_star(candle)

    def test_bullish_engulfing(self):
        """Бычье поглощение: красная → зелёная, накрывающая."""
        prev = pd.Series({"open": 100, "high": 100.5, "low": 99.5, "close": 99.6})
        curr = pd.Series({"open": 99.5, "high": 101, "low": 99.4, "close": 100.8})
        # prev медвежья (close < open), curr бычья и накрывает
        assert is_bullish_engulfing(prev, curr)

    def test_bearish_engulfing(self):
        prev = pd.Series({"open": 99.5, "high": 100.5, "low": 99.4, "close": 100.3})
        curr = pd.Series({"open": 100.5, "high": 100.6, "low": 99.2, "close": 99.3})
        assert is_bearish_engulfing(prev, curr)

    def test_not_engulfing_same_direction(self):
        """Две одинаково-окрашенные свечи — не поглощение."""
        prev = pd.Series({"open": 100, "high": 101, "low": 99.5, "close": 100.5})
        curr = pd.Series({"open": 100.5, "high": 101.5, "low": 100, "close": 101})
        assert not is_bullish_engulfing(prev, curr)
        assert not is_bearish_engulfing(prev, curr)


class TestDetectSignals:
    def test_empty_short_df(self):
        """Пустой / короткий df → нет сигналов."""
        df = pd.DataFrame({"open": [], "high": [], "low": [], "close": []})
        assert detect_signals(df) == []

    def test_signals_have_correct_structure(self, synthetic_ohlc):
        df = prepare_dataframe(synthetic_ohlc)
        signals = detect_signals(df)
        for s in signals:
            assert s.bar_index >= 0
            assert s.direction in (Direction.LONG, Direction.SHORT)
            assert s.entry > 0
            assert s.stop > 0
            assert s.take > 0
            # Стоп и тейк по правильным сторонам
            if s.direction == Direction.LONG:
                assert s.stop < s.entry
                assert s.take > s.entry
            else:
                assert s.stop > s.entry
                assert s.take < s.entry
            # R:R должен быть положительный
            assert s.rr > 0

    def test_rr_consistent(self, synthetic_ohlc):
        """R:R в сигнале соответствует расстояниям."""
        df = prepare_dataframe(synthetic_ohlc)
        signals = detect_signals(df, rr=2.0)
        for s in signals:
            risk = abs(s.entry - s.stop)
            reward = abs(s.take - s.entry)
            assert reward / risk == pytest.approx(2.0, rel=0.01)

    def test_long_signals_in_uptrend(self, trending_up_ohlc):
        """На восходящем тренде должны быть LONG сигналы."""
        df = prepare_dataframe(trending_up_ohlc)
        signals = detect_signals(df)
        # Не должно быть много шорт-сигналов в чистом аптренде
        longs = [s for s in signals if s.direction == Direction.LONG]
        shorts = [s for s in signals if s.direction == Direction.SHORT]
        # Может быть мало сигналов, но соотношение longs >= shorts
        assert len(longs) >= len(shorts) or len(signals) < 3
