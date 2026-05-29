"""Binance broker — заглушка для crypto."""
from __future__ import annotations

import os

from .base import Broker, Order, Position


try:
    from binance.client import Client
    HAS_BINANCE = True
except ImportError:
    Client = None
    HAS_BINANCE = False


class BinanceBroker(Broker):
    """Binance broker для крипто.

    Требует:
      pip install python-binance
      API key + Secret (создаются в Binance → API Management)

    ⚠️ Используй ТОЛЬКО testnet ключи на начальном этапе!
    Spot Testnet: https://testnet.binance.vision/
    """

    def __init__(self, testnet: bool = True):
        if not HAS_BINANCE:
            raise ImportError(
                "python-binance не установлен.\n"
                "  pip install python-binance"
            )
        self.testnet = testnet
        self.client = None

    def connect(self, api_key: str = None, api_secret: str = None,
                **_) -> bool:
        if not api_key or not api_secret:
            raise ValueError(
                "Нужны api_key и api_secret. Создай в Binance Account → API."
            )
        self.client = Client(api_key, api_secret, testnet=self.testnet)
        try:
            # Проверка подключения
            self.client.ping()
            return True
        except Exception:
            return False

    def disconnect(self) -> None:
        self.client = None

    def get_candles(self, symbol: str, timeframe: str, count: int = 100):
        import pandas as pd
        tf_map = {
            "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
            "H1": "1h", "H4": "4h", "D1": "1d",
        }
        interval = tf_map.get(timeframe, "1h")
        # Binance использует символы без слэша: BTCUSDT, ETHUSDT
        klines = self.client.get_klines(symbol=symbol, interval=interval,
                                        limit=count)
        df = pd.DataFrame(klines, columns=[
            "time", "open", "high", "low", "close", "volume",
            "_ct", "_qv", "_n", "_tb", "_tq", "_i",
        ])
        df["datetime"] = pd.to_datetime(df["time"], unit="ms")
        df = df.set_index("datetime")
        return df[["open", "high", "low", "close"]].astype(float)

    def get_price(self, symbol: str) -> dict:
        from datetime import datetime
        ticker = self.client.get_orderbook_ticker(symbol=symbol)
        return {
            "bid": float(ticker["bidPrice"]),
            "ask": float(ticker["askPrice"]),
            "time": datetime.now(),
        }

    def get_balance(self) -> float:
        # Возвращает баланс USDT (можно расширить)
        account = self.client.get_account()
        for b in account["balances"]:
            if b["asset"] == "USDT":
                return float(b["free"])
        return 0

    def get_positions(self) -> list[Position]:
        # На спот-рынке нет «открытых позиций» в forex-смысле.
        # Только активы на балансе.
        return []

    def place_order(self, symbol: str, direction: str, volume: float,
                    stop: float | None = None,
                    take: float | None = None) -> Order:
        # SL/TP на Binance Spot — отдельный OCO-ордер; пока НЕ реализовано.
        # Раньше стоп молча игнорировался (`if stop: pass`) — ордер уходил на
        # рынок без защиты. Теперь падаем явно, чтобы новичок не торговал без SL.
        if stop is not None or take is not None:
            raise NotImplementedError(
                "SL/TP на Binance Spot требует отдельного OCO-ордера — пока не "
                "реализовано. Не отправляй рыночный ордер без защиты вручную."
            )
        # Защита от реального счёта: на mainnet (testnet=False) требуем явного
        # подтверждения через FX_ALLOW_LIVE=1.
        if not self.testnet and os.environ.get("FX_ALLOW_LIVE") != "1":
            raise RuntimeError(
                "Реальный счёт Binance заблокирован. Используй testnet=True "
                "или установи FX_ALLOW_LIVE=1, если осознанно торгуешь вживую."
            )
        side = "BUY" if direction == "long" else "SELL"
        order = self.client.create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=volume,
        )
        return Order(
            id=str(order["orderId"]),
            symbol=symbol,
            direction=direction,
            volume=volume,
            entry=float(order["fills"][0]["price"]) if order.get("fills") else 0,
            stop=stop,
            take=take,
            status="filled",
        )

    def close_position(self, order_id: str) -> bool:
        # Для spot — продать обратно
        raise NotImplementedError(
            "Для closing на Binance Spot — продать актив обратно "
            "через place_order с противоположным direction."
        )
