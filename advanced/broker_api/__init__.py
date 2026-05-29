"""
Унифицированный broker-API.

Один интерфейс для разных брокеров и бирж:
  - MetaTrader 5 (forex брокеры)
  - cTrader API (forex брокеры)
  - Binance / Bybit (crypto биржи)
  - Yahoo Finance (только данные, не торговля)

Пример использования:

    from broker_api import get_broker

    broker = get_broker("mt5")  # или "binance", "ctrader", "yfinance"
    broker.connect(login=..., password=..., server=...)

    candles = broker.get_candles("EURUSD", "H1", 100)
    broker.place_order("EURUSD", "long", 0.01, stop=1.08, take=1.09)

⚠️ Это СКЕЛЕТ-пример, НЕ входит в публикуемый пакет forex-toolkit.
Реальные методы реализованы только для yfinance (read-only).
MT5/Binance умеют ставить ордера, но авто-торговля на реальном счёте
заблокирована: разрешена только на демо/testnet, либо при FX_ALLOW_LIVE=1.
"""
from .base import Broker
from .factory import get_broker

__all__ = ["Broker", "get_broker"]
