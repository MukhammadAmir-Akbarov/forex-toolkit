"""Тесты для broker_api/."""
from __future__ import annotations

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "advanced"))

from broker_api import Broker, get_broker
from broker_api.base import Order, Position


class TestFactory:
    def test_yfinance_broker(self):
        broker = get_broker("yfinance")
        assert isinstance(broker, Broker)

    def test_unknown_broker(self):
        with pytest.raises(ValueError, match="Неизвестный"):
            get_broker("nonexistent")

    def test_case_insensitive(self):
        b1 = get_broker("YFinance")
        b2 = get_broker("yfinance")
        b3 = get_broker("YFINANCE")
        assert type(b1) is type(b2) is type(b3)


class TestYFinanceBroker:
    def setup_method(self):
        self.broker = get_broker("yfinance")
        self.broker.connect()

    def teardown_method(self):
        self.broker.disconnect()

    def test_connect_returns_true(self):
        # yfinance не требует креденшилов
        broker = get_broker("yfinance")
        assert broker.connect() is True

    def test_get_candles(self):
        df = self.broker.get_candles("EURUSD", "H1", 10)
        assert not df.empty
        assert all(col in df.columns for col in ["open", "high", "low", "close"])

    def test_get_candles_multiple_pairs(self):
        for sym in ["EURUSD", "GBPUSD"]:
            df = self.broker.get_candles(sym, "D1", 5)
            assert len(df) > 0

    def test_get_price(self):
        price = self.broker.get_price("EURUSD")
        assert price["bid"] > 0
        assert price["ask"] > 0
        assert price["time"] is not None

    def test_get_balance_not_supported(self):
        with pytest.raises(NotImplementedError):
            self.broker.get_balance()

    def test_get_positions_empty(self):
        assert self.broker.get_positions() == []

    def test_place_order_not_supported(self):
        with pytest.raises(NotImplementedError):
            self.broker.place_order("EURUSD", "long", 0.01)


class TestOrderPosition:
    def test_order_defaults(self):
        o = Order(id="1", symbol="EURUSD", direction="long",
                  volume=0.01, entry=1.08)
        assert o.status == "pending"
        assert o.stop is None
        assert o.take is None

    def test_position_structure(self):
        p = Position(
            order_id="1", symbol="EURUSD", direction="long",
            volume=0.01, entry_price=1.08, current_price=1.09, pnl=10,
        )
        assert p.pnl == 10
        assert p.direction == "long"
