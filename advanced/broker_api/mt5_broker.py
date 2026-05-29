"""MetaTrader 5 broker (только Windows + MT5 терминал)."""
from __future__ import annotations

import os
import sys

from .base import Broker, Order, Position

# Заглушка: импорт MetaTrader5 не упадёт, если пакета нет
try:
    import MetaTrader5 as mt5
    HAS_MT5 = True
except ImportError:
    mt5 = None
    HAS_MT5 = False


TIMEFRAME_MAP = {
    "M1": "TIMEFRAME_M1",
    "M5": "TIMEFRAME_M5",
    "M15": "TIMEFRAME_M15",
    "M30": "TIMEFRAME_M30",
    "H1": "TIMEFRAME_H1",
    "H4": "TIMEFRAME_H4",
    "D1": "TIMEFRAME_D1",
    "W1": "TIMEFRAME_W1",
}


class MT5Broker(Broker):
    """MetaTrader 5 broker.
    Требует:
      - Windows (или WINE)
      - Установленный MT5 терминал
      - pip install MetaTrader5
      - Демо или реал счёт залогинен в терминале
    """

    def __init__(self):
        if not HAS_MT5:
            raise ImportError(
                "MetaTrader5 пакет не установлен.\n"
                "  pip install MetaTrader5\n"
                "  ⚠️ Работает только на Windows."
            )
        self.connected = False
        self.is_demo = False

    def _ensure_trading_allowed(self) -> None:
        """Блокирует авто-торговлю на реальном счёте.

        Реальные ордера разрешены только на демо, либо при осознанно
        выставленной переменной окружения ``FX_ALLOW_LIVE=1``.
        """
        if not self.is_demo and os.environ.get("FX_ALLOW_LIVE") != "1":
            raise RuntimeError(
                "Реальный счёт MT5 заблокирован для авто-торговли. "
                "Торгуй на демо, или установи FX_ALLOW_LIVE=1, если осознанно "
                "торгуешь вживую и понимаешь риски."
            )

    def connect(self, login: int = None, password: str = None,
                server: str = None, **_) -> bool:
        if login and password and server:
            ok = mt5.initialize(login=login, password=password, server=server)
        else:
            ok = mt5.initialize()

        if not ok:
            return False

        info = mt5.account_info()
        if info is None:
            mt5.shutdown()
            return False

        # Защита: запомнить тип счёта и предупредить о реальном
        self.is_demo = info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO
        if not self.is_demo:
            print(f"⚠️  ВНИМАНИЕ: счёт #{info.login} — РЕАЛЬНЫЙ")
            print(f"   Баланс: {info.balance} {info.currency}")
            print("   Авто-ордера заблокированы (нужен FX_ALLOW_LIVE=1).")

        self.connected = True
        return True

    def disconnect(self) -> None:
        if self.connected:
            mt5.shutdown()
            self.connected = False

    def get_candles(self, symbol: str, timeframe: str, count: int = 100):
        import pandas as pd
        tf = getattr(mt5, TIMEFRAME_MAP.get(timeframe, "TIMEFRAME_H1"))
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
        if rates is None:
            return pd.DataFrame()
        df = pd.DataFrame(rates)
        df["datetime"] = pd.to_datetime(df["time"], unit="s")
        df = df.set_index("datetime")
        return df[["open", "high", "low", "close"]]

    def get_price(self, symbol: str) -> dict:
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            return {"bid": 0, "ask": 0, "time": None}
        from datetime import datetime
        return {
            "bid": tick.bid,
            "ask": tick.ask,
            "time": datetime.fromtimestamp(tick.time),
        }

    def get_balance(self) -> float:
        info = mt5.account_info()
        return info.balance if info else 0

    def get_positions(self) -> list[Position]:
        positions = mt5.positions_get()
        if not positions:
            return []
        return [
            Position(
                order_id=str(p.ticket),
                symbol=p.symbol,
                direction="long" if p.type == 0 else "short",
                volume=p.volume,
                entry_price=p.price_open,
                current_price=p.price_current,
                pnl=p.profit,
                stop=p.sl if p.sl > 0 else None,
                take=p.tp if p.tp > 0 else None,
            )
            for p in positions
        ]

    def place_order(self, symbol: str, direction: str, volume: float,
                    stop: float | None = None,
                    take: float | None = None) -> Order:
        self._ensure_trading_allowed()
        tick = mt5.symbol_info_tick(symbol)
        if direction == "long":
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
        else:
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": stop or 0,
            "tp": take or 0,
            "deviation": 10,
            "magic": 20260520,
            "comment": "broker_api",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"Order failed: {result.comment}")

        return Order(
            id=str(result.order),
            symbol=symbol,
            direction=direction,
            volume=volume,
            entry=result.price,
            stop=stop,
            take=take,
            status="filled",
        )

    def close_position(self, order_id: str) -> bool:
        self._ensure_trading_allowed()
        positions = [p for p in (mt5.positions_get() or [])
                     if str(p.ticket) == order_id]
        if not positions:
            return False
        p = positions[0]
        tick = mt5.symbol_info_tick(p.symbol)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": p.symbol,
            "volume": p.volume,
            "type": mt5.ORDER_TYPE_SELL if p.type == 0 else mt5.ORDER_TYPE_BUY,
            "price": tick.bid if p.type == 0 else tick.ask,
            "position": p.ticket,
            "deviation": 10,
            "magic": 20260520,
            "comment": "close",
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return result.retcode == mt5.TRADE_RETCODE_DONE
