#!/usr/bin/env python3
"""
Пример использования унифицированного broker-API.

Один и тот же код работает с любым брокером — только меняешь имя.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from broker_api import get_broker


def demo_yfinance():
    """Только чтение — работает везде, не нужен ключ."""
    print("\n=== YFinance (Yahoo Finance) ===")
    broker = get_broker("yfinance")
    broker.connect()

    candles = broker.get_candles("EURUSD", "H1", 10)
    print(f"\n10 последних свечей EUR/USD H1:")
    print(candles.tail())

    price = broker.get_price("EURUSD")
    print(f"\nТекущая цена: bid={price['bid']:.5f}, ask={price['ask']:.5f}")
    broker.disconnect()


def demo_mt5_skeleton():
    """Скелет для MT5 — не сможет реально подключиться без Windows + MT5."""
    print("\n=== MT5 (только Windows + MT5 терминал) ===")
    try:
        broker = get_broker("mt5")
        # broker.connect(login=123, password="xxx", server="Broker-Demo")
        print("✓ MT5 broker инициализирован")
        print("  Для реального использования передай login/password/server")
    except ImportError as e:
        print(f"❌ {e}")


def demo_binance_skeleton():
    """Скелет для Binance — нужен API key."""
    print("\n=== Binance (нужны API ключи) ===")
    try:
        broker = get_broker("binance", testnet=True)
        # broker.connect(api_key="xxx", api_secret="yyy")
        print("✓ Binance broker инициализирован")
        print("  Для реального использования: pip install python-binance")
        print("  и API ключи (рекомендую testnet)")
    except ImportError as e:
        print(f"❌ {e}")


def main():
    print("=" * 60)
    print("  BROKER API EXAMPLE")
    print("=" * 60)

    # Только yfinance работает «из коробки»
    demo_yfinance()

    # Остальные требуют дополнительной настройки
    demo_mt5_skeleton()
    demo_binance_skeleton()

    print("\n" + "=" * 60)
    print("Все брокеры реализуют один интерфейс:")
    print("  broker.connect(**creds)")
    print("  broker.get_candles(symbol, timeframe, count)")
    print("  broker.get_price(symbol)")
    print("  broker.get_balance()")
    print("  broker.get_positions()")
    print("  broker.place_order(symbol, direction, volume, stop, take)")
    print("  broker.close_position(order_id)")
    print()
    print("Замена брокера = смена ОДНОЙ строки.")


if __name__ == "__main__":
    main()
