"""Фабрика для создания broker-инстансов."""
from __future__ import annotations

from .base import Broker


def get_broker(name: str, **kwargs) -> Broker:
    """Создаёт broker по имени.

    name: "mt5" | "binance" | "yfinance" | "ctrader"
    """
    name = name.lower().strip()

    if name == "yfinance":
        from .yfinance_broker import YFinanceBroker
        return YFinanceBroker()

    elif name == "mt5":
        from .mt5_broker import MT5Broker
        return MT5Broker()

    elif name == "binance":
        from .binance_broker import BinanceBroker
        return BinanceBroker(testnet=kwargs.get("testnet", True))

    elif name == "ctrader":
        raise NotImplementedError(
            "cTrader broker не реализован. "
            "API: https://help.ctrader.com/open-api/"
        )

    else:
        raise ValueError(
            f"Неизвестный broker: '{name}'. "
            f"Доступные: yfinance, mt5, binance, ctrader"
        )
