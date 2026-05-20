#!/usr/bin/env python3
"""
Калькулятор маржи: показывает, сколько денег «замёрзнет» под позицию.
"""
from __future__ import annotations

import argparse
import sys


def margin_required(lots: float, price: float, leverage: int,
                    contract_size: int = 100_000) -> float:
    """Маржа = (лоты × контракт × цена) / плечо."""
    return (lots * contract_size * price) / leverage


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Калькулятор маржи",
    )
    parser.add_argument("--lots", type=float, default=0.01)
    parser.add_argument("--price", type=float, default=1.08,
                        help="Текущая цена пары")
    parser.add_argument("--leverage", type=int, default=30,
                        help="Плечо (например 30 для 1:30)")
    parser.add_argument("--deposit", type=float,
                        help="Депозит (опц.) — покажет %% использования маржи")
    args = parser.parse_args()

    margin = margin_required(args.lots, args.price, args.leverage)

    print(f"\n  Лот:        {args.lots}")
    print(f"  Цена:       {args.price}")
    print(f"  Плечо:      1:{args.leverage}")
    print(f"\n  → Маржа:    ${margin:,.2f}")

    if args.deposit:
        pct = margin / args.deposit * 100
        print(f"  → Депозит:  ${args.deposit:,.2f}")
        print(f"  → Использование маржи: {pct:.2f}%")
        if pct > 50:
            print(f"\n⚠️  Маржа > 50% депозита — рискованно, "
                  f"мало свободы для просадки")
        elif pct > 20:
            print(f"\n⚠️  Маржа > 20% депозита — высокая нагрузка")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
