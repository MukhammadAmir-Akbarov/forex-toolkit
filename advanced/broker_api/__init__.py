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
    broker.place_order("EURUSD", "long", 0.01, sl=1.08, tp=1.09)

⚠️ Это СКЕЛЕТ. Реальные методы реализованы только для yfinance (read-only).
Остальные требуют установки соответствующих пакетов и доступа к API.
"""
from .base import Broker
from .factory import get_broker

__all__ = ["Broker", "get_broker"]
