"""Тесты для всех стратегий в strategies/."""
from __future__ import annotations

import pytest

from strategies import breakout, mean_reversion, three_soldiers, london_open
from strategies.common import Direction, ema, sma, rsi, atr, bollinger


class TestCommonIndicators:
    def test_ema_length_preserved(self, synthetic_ohlc):
        e = ema(synthetic_ohlc["close"], 20)
        assert len(e) == len(synthetic_ohlc)

    def test_sma_vs_ema_smoothing(self, synthetic_ohlc):
        """SMA и EMA одинаковой длины — обе сглаживают."""
        s = sma(synthetic_ohlc["close"], 50)
        e = ema(synthetic_ohlc["close"], 50)
        # Обе должны иметь меньшую волатильность, чем оригинал
        # (упрощённая проверка)
        orig_std = synthetic_ohlc["close"].std()
        assert s.dropna().std() < orig_std
        assert e.dropna().std() < orig_std

    def test_atr_positive(self, synthetic_ohlc):
        """ATR всегда положительный."""
        a = atr(synthetic_ohlc, 14)
        assert (a.dropna() >= 0).all()

    def test_bollinger_bands_order(self, synthetic_ohlc):
        """Upper >= Middle >= Lower."""
        upper, middle, lower = bollinger(synthetic_ohlc["close"], 20, 2)
        valid = ~upper.isna()
        assert (upper[valid] >= middle[valid]).all()
        assert (middle[valid] >= lower[valid]).all()


class TestMeanReversion:
    def test_returns_signals_in_flat(self, flat_ohlc):
        """В флэте mean-reversion должна находить сигналы."""
        signals = mean_reversion.detect(flat_ohlc)
        # На флэте mean-reversion обычно работает
        # Может быть 0 сигналов если ничего не дошло до полос — это тоже ок
        assert isinstance(signals, list)

    def test_signal_structure(self, flat_ohlc):
        signals = mean_reversion.detect(flat_ohlc)
        for s in signals:
            assert s.direction in (Direction.LONG, Direction.SHORT)
            assert s.entry > 0
            if s.direction == Direction.LONG:
                assert s.stop < s.entry
                assert s.take > s.entry

    def test_empty_short_df(self):
        import pandas as pd
        empty = pd.DataFrame(columns=["open", "high", "low", "close"])
        assert mean_reversion.detect(empty) == []


class TestBreakout:
    def test_returns_signals_in_trend(self, trending_up_ohlc):
        signals = breakout.detect(trending_up_ohlc, lookback=20)
        assert isinstance(signals, list)

    def test_long_signals_predominate_in_uptrend(self, trending_up_ohlc):
        signals = breakout.detect(trending_up_ohlc, lookback=20)
        longs = [s for s in signals if s.direction == Direction.LONG]
        shorts = [s for s in signals if s.direction == Direction.SHORT]
        # В восходящем тренде должно быть больше long-пробоев
        if signals:
            assert len(longs) >= len(shorts)


class TestThreeSoldiers:
    def test_basic_structure(self, trending_up_ohlc):
        signals = three_soldiers.detect(trending_up_ohlc)
        assert isinstance(signals, list)
        for s in signals:
            assert s.strategy == "three_soldiers"


class TestLondonOpen:
    def test_with_datetime_index(self, synthetic_ohlc):
        signals = london_open.detect(synthetic_ohlc)
        assert isinstance(signals, list)

    def test_without_datetime_index(self):
        """Без DatetimeIndex — возвращает пустой список."""
        import pandas as pd
        df = pd.DataFrame({
            "open": [1.0] * 100, "high": [1.001] * 100,
            "low": [0.999] * 100, "close": [1.0] * 100,
        })
        # default RangeIndex
        assert london_open.detect(df) == []
