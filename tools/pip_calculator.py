#!/usr/bin/env python3
"""
Точный калькулятор стоимости пипса для любой валюты счёта.

Учитывает текущий курс через bid/ask, который ты вводишь сам
(чтобы не зависеть от платных API).
"""
from __future__ import annotations

import argparse
import sys

# Финансовая математика живёт в одном месте — forex_toolkit.fx_math.
# Импортируем оттуда (с фолбэком на sys.path, чтобы скрипт работал и без
# установки пакета — просто `python tools/pip_calculator.py`).
try:
    from forex_toolkit.fx_math import (
        pip_size,
        pip_value_in_account_currency,
        pip_value_in_quote,
    )
except ModuleNotFoundError:  # запуск скрипта без установки пакета
    from pathlib import Path as _Path
    sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))
    from forex_toolkit.fx_math import (
        pip_size,
        pip_value_in_account_currency,
        pip_value_in_quote,
    )

# Реэкспорт публичного API (используется тестами и как библиотека).
__all__ = ["pip_size", "pip_value_in_quote", "pip_value_in_account_currency"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Точный калькулятор стоимости пипса",
    )
    parser.add_argument("--lots", type=float, default=0.01,
                        help="Размер позиции (по умолч. 0.01)")
    parser.add_argument("--pair", default="EURUSD",
                        help="Торгуемая пара")
    parser.add_argument("--account", default="USD",
                        help="Валюта счёта (USD, EUR, RUB...)")
    parser.add_argument("--price", type=float,
                        help="Текущая цена пары (нужна, если account=base)")
    args = parser.parse_args()

    if args.price is None:
        if args.account.upper() != args.pair.upper().replace("/", "")[3:]:
            print("Введи текущую цену пары (--price), это нужно для конвертации.")
            return 1
        args.price = 1.0  # не используется

    try:
        value = pip_value_in_account_currency(
            args.lots, args.pair, args.account, args.price,
        )
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    pair = args.pair.upper().replace("/", "")
    print(f"\nЛот:     {args.lots}")
    print(f"Пара:    {pair}")
    print(f"Счёт в:  {args.account.upper()}")
    print(f"Цена:    {args.price}")
    print(f"\n→ 1 пипс = {value:.4f} {args.account.upper()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
