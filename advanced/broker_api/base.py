"""Базовый абстрактный интерфейс для всех брокеров."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Order:
    id: str
    symbol: str
    direction: str  # "long" | "short"
    volume: float
    entry: float
    stop: float | None = None
    take: float | None = None
    status: str = "pending"  # "pending" | "filled" | "closed" | "cancelled"


@dataclass
class Position:
    order_id: str
    symbol: str
    direction: str
    volume: float
    entry_price: float
    current_price: float
    pnl: float
    stop: float | None = None
    take: float | None = None


class Broker(ABC):
    """Унифицированный интерфейс брокера / биржи."""

    @abstractmethod
    def connect(self, **kwargs) -> bool:
        """Подключение. Параметры зависят от брокера."""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Отключение."""
        ...

    @abstractmethod
    def get_candles(self, symbol: str, timeframe: str,
                    count: int = 100):
        """OHLC данные. Возвращает pandas DataFrame."""
        ...

    @abstractmethod
    def get_price(self, symbol: str) -> dict:
        """Текущая цена. {bid, ask, time}."""
        ...

    @abstractmethod
    def get_balance(self) -> float:
        """Баланс счёта."""
        ...

    @abstractmethod
    def get_positions(self) -> list[Position]:
        """Открытые позиции."""
        ...

    @abstractmethod
    def place_order(self, symbol: str, direction: str, volume: float,
                    stop: float | None = None,
                    take: float | None = None) -> Order:
        """Открыть рыночный ордер."""
        ...

    @abstractmethod
    def close_position(self, order_id: str) -> bool:
        """Закрыть позицию."""
        ...

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.disconnect()
