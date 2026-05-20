"""Yfinance — только чтение данных, без торговли."""
from __future__ import annotations

import pandas as pd
import yfinance as yf

from .base import Broker, Order, Position


TIMEFRAME_MAP = {
    "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
    "H1": "1h", "H4": "4h", "D1": "1d", "W1": "1wk",
}


class YFinanceBroker(Broker):
    """Только чтение OHLC через Yahoo Finance.
    Можешь использовать для бэктестов и анализа.
    Торговля невозможна — нет API."""

    def connect(self, **kwargs) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    def _symbol(self, symbol: str) -> str:
        s = symbol.upper().replace("/", "").replace("-", "")
        if "USD" in s and "=" not in s:
            return f"{s}=X"
        return s

    def get_candles(self, symbol: str, timeframe: str,
                    count: int = 100) -> pd.DataFrame:
        yf_symbol = self._symbol(symbol)
        interval = TIMEFRAME_MAP.get(timeframe, "1h")

        # Подбираем period под нужное количество свечей
        if interval in ("1m", "5m", "15m"):
            period = "5d"
        elif interval in ("30m", "1h"):
            period = "60d"
        elif interval == "4h":
            period = "1y"
        else:
            period = "2y"

        df = yf.Ticker(yf_symbol).history(period=period, interval=interval)
        if df.empty:
            return pd.DataFrame()
        df.columns = [c.lower() for c in df.columns]
        return df[["open", "high", "low", "close"]].tail(count)

    def get_price(self, symbol: str) -> dict:
        df = self.get_candles(symbol, "M5", 1)
        if df.empty:
            return {"bid": 0, "ask": 0, "time": None}
        last = df.iloc[-1]
        return {
            "bid": float(last["close"]),
            "ask": float(last["close"]),
            "time": df.index[-1].to_pydatetime(),
        }

    def get_balance(self) -> float:
        raise NotImplementedError(
            "YFinance не поддерживает счета. Используй для данных только."
        )

    def get_positions(self) -> list[Position]:
        return []

    def place_order(self, *args, **kwargs) -> Order:
        raise NotImplementedError(
            "YFinance не поддерживает торговлю."
        )

    def close_position(self, order_id: str) -> bool:
        raise NotImplementedError(
            "YFinance не поддерживает торговлю."
        )
