#!/usr/bin/env python3
"""
Multi-position sizer — расчёт размеров для НЕСКОЛЬКИХ сделок одновременно.

Распределяет общий риск-бюджет (2% депозита) между N запланированными сделками.
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass


@dataclass
class TradePlan:
    pair: str
    stop_pips: float
    pip_value: float = 10.0  # USD per pip per lot


def calc_lots(risk_usd: float, stop_pips: float, pip_value: float) -> float:
    if stop_pips <= 0 or pip_value <= 0:
        return 0.0
    raw = risk_usd / (stop_pips * pip_value)
    return math.floor(raw * 100 + 1e-9) / 100


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Расчёт лотов для нескольких сделок",
    )
    parser.add_argument("--deposit", "-d", type=float, required=True)
    parser.add_argument("--total-risk", "-r", type=float, default=2.0,
                        help="Общий риск-бюджет в %% (по умолч. 2.0)")
    parser.add_argument(
        "--trade", action="append", nargs=2,
        metavar=("PAIR", "STOP_PIPS"),
        required=True,
        help="Сделка: пара стоп_в_пипсах. Можно указать несколько раз.",
    )
    parser.add_argument("--allocation", choices=["equal", "weighted"],
                        default="equal",
                        help="Как распределять риск (equal по умолч.)")
    args = parser.parse_args()

    trades: list[TradePlan] = []
    for pair, stop in args.trade:
        trades.append(TradePlan(pair.upper(), float(stop)))

    n = len(trades)
    total_risk_usd = args.deposit * args.total_risk / 100

    if args.allocation == "equal":
        per_trade = total_risk_usd / n
        allocations = [per_trade] * n
    else:
        # Weighted: больше риска на сделки с меньшим стопом
        weights = [1 / t.stop_pips for t in trades]
        total_w = sum(weights)
        allocations = [total_risk_usd * w / total_w for w in weights]

    print(f"\n  Депозит:           ${args.deposit:,.2f}")
    print(f"  Общий риск:        {args.total_risk}% = ${total_risk_usd:.2f}")
    print(f"  Сделок:            {n}")
    print(f"  Распределение:     {args.allocation}")
    print()
    print(f"{'Пара':<10} {'Стоп пипс':>10} {'Риск $':>10} "
          f"{'Лот':>8} {'Реальн. риск $':>16}")
    print("─" * 60)

    total_actual = 0.0
    for t, alloc in zip(trades, allocations):
        lots = calc_lots(alloc, t.stop_pips, t.pip_value)
        actual = lots * t.stop_pips * t.pip_value
        total_actual += actual
        print(f"{t.pair:<10} {t.stop_pips:>10.0f} "
              f"${alloc:>9.2f} {lots:>8.2f} ${actual:>14.2f}")

    print("─" * 60)
    print(f"{'ИТОГО':<10} {'':<10} {'':<10} "
          f"{'':<8} ${total_actual:>14.2f}")
    print(f"\nРеальный использованный риск: {total_actual / args.deposit * 100:.2f}%")

    if total_actual / args.deposit > 0.025:
        print("⚠️  Превышение бюджета — проверь стопы")
    return 0


if __name__ == "__main__":
    sys.exit(main())
