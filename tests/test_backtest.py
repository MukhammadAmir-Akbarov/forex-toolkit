"""Тесты для bot/backtest.py — симулятор сделок."""

from __future__ import annotations

import pytest

from backtest import simulate, stats, generate_synthetic_data
from strategy import detect_signals, prepare_dataframe


class TestSimulate:
    def test_empty_signals(self, synthetic_ohlc):
        trades = simulate(synthetic_ohlc, [])
        assert trades == []

    def test_simulation_produces_trades(self, synthetic_ohlc):
        df = prepare_dataframe(synthetic_ohlc)
        signals = detect_signals(df)
        if not signals:
            pytest.skip("No signals generated on test data")
        trades = simulate(df, signals)
        # Если сигналы есть — должны быть сделки
        assert len(trades) > 0
        assert len(trades) <= len(signals)

    def test_no_overlapping_trades(self, synthetic_ohlc):
        """Симулятор не должен открывать новую сделку, пока есть открытая."""
        df = prepare_dataframe(synthetic_ohlc)
        signals = detect_signals(df)
        trades = simulate(df, signals)
        # Сортируем по времени входа
        for i in range(1, len(trades)):
            # Время входа следующей >= время выхода предыдущей
            assert trades[i].entry_time >= trades[i - 1].exit_time

    def test_trade_outcome_values(self, synthetic_ohlc):
        df = prepare_dataframe(synthetic_ohlc)
        signals = detect_signals(df)
        trades = simulate(df, signals)
        for t in trades:
            assert t.outcome in ("win", "loss", "timeout")
            # PnL соответствует исходу
            if t.outcome == "win":
                assert t.pnl_r > 0
            elif t.outcome == "loss":
                # Стоп = 1R убытка
                assert t.pnl_r == pytest.approx(-1.0, abs=0.01)


class TestStats:
    def test_empty_trades(self):
        s = stats([])
        assert s["total"] == 0

    def test_stats_structure(self, synthetic_ohlc):
        df = prepare_dataframe(synthetic_ohlc)
        signals = detect_signals(df)
        trades = simulate(df, signals)
        if not trades:
            pytest.skip("No trades")
        s = stats(trades)
        required = {
            "total",
            "wins",
            "losses",
            "win_rate",
            "profit_factor",
            "expectancy_r",
            "total_r",
            "max_drawdown_r",
        }
        assert required.issubset(s.keys())

    def test_winrate_consistency(self, synthetic_ohlc):
        df = prepare_dataframe(synthetic_ohlc)
        signals = detect_signals(df)
        trades = simulate(df, signals)
        if not trades:
            pytest.skip("No trades")
        s = stats(trades)
        # WR = wins / total
        expected_wr = s["wins"] / s["total"] if s["total"] else 0
        assert s["win_rate"] == pytest.approx(expected_wr)

    def test_profit_factor_positive_when_all_wins(self):
        """Если все сделки прибыльные — PF = inf."""
        from backtest import Trade
        import pandas as pd

        trades = [
            Trade(
                entry_time=pd.Timestamp("2025-01-01"),
                exit_time=pd.Timestamp("2025-01-02"),
                direction="long",
                entry=1.08,
                stop=1.07,
                take=1.10,
                exit_price=1.10,
                outcome="win",
                pnl_pips=200,
                pnl_r=2.0,
                reason="test",
                bars_held=24,
            )
        ]
        s = stats(trades)
        assert s["wins"] == 1
        assert s["losses"] == 0
        assert s["profit_factor"] == float("inf")


class TestSyntheticData:
    def test_generate_synthetic_data(self):
        df = generate_synthetic_data(100)
        assert len(df) == 100
        assert all(col in df.columns for col in ["open", "high", "low", "close"])
        # High >= max(open, close)
        assert (df["high"] >= df[["open", "close"]].max(axis=1)).all()
        # Low <= min(open, close)
        assert (df["low"] <= df[["open", "close"]].min(axis=1)).all()
