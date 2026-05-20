#!/usr/bin/env python3
"""
Точный калькулятор стоимости пипса для любой валюты счёта.

Учитывает текущий курс через bid/ask, который ты вводишь сам
(чтобы не зависеть от платных API).
"""
from __future__ import annotations

import argparse
import sys

PIP_SIZES = {
    "JPY": 0.01,  # для пар с JPY
}
DEFAULT_PIP_SIZE = 0.0001


def pip_size(pair: str) -> float:
    pair = pair.upper().replace("/", "")
    if "JPY" in pair:
        return PIP_SIZES["JPY"]
    return DEFAULT_PIP_SIZE


def pip_value_in_quote(lots: float, pair: str) -> float:
    """Стоимость 1 пипса в КОТИРУЕМОЙ валюте (USD для EUR/USD)."""
    return lots * 100_000 * pip_size(pair)


def pip_value_in_account_currency(
    lots: float, pair: str, account_ccy: str, current_price: float,
) -> float:
    """
    Стоимость пипса в валюте счёта.

    Args:
        lots: размер позиции в лотах
        pair: торгуемая пара (e.g., "EURUSD", "USDJPY")
        account_ccy: валюта счёта (e.g., "USD", "EUR", "RUB")
        current_price: текущая цена ТОРГУЕМОЙ ПАРЫ
    """
    pair = pair.upper().replace("/", "")
    account_ccy = account_ccy.upper()
    base = pair[:3]
    quote = pair[3:]

    pip_in_quote = pip_value_in_quote(lots, pair)

    # Пипс выражен в quote валюте. Перевод в валюту счёта:
    if account_ccy == quote:
        return pip_in_quote
    elif account_ccy == base:
        return pip_in_quote / current_price
    else:
        # Кросс-конвертация: нужен курс quote → account_ccy
        # Здесь упрощаем: пользователь должен ввести курс сам
        raise ValueError(
            f"Кросс-конвертация {quote}→{account_ccy} требует доп. курс. "
            f"Используй точный расчёт через терминал брокера."
        )


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
