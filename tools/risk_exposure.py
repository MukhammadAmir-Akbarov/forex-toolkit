#!/usr/bin/env python3
"""
Risk Exposure Tracker — учёт суммарного риска по открытым позициям.

Учитывает корреляции валютных пар: открытие EUR/USD long
и GBP/USD long даёт фактически удвоенный риск.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass


# Упрощённая матрица корреляций (исторические значения)
CORRELATIONS = {
    ("EURUSD", "GBPUSD"): 0.85,
    ("EURUSD", "AUDUSD"): 0.75,
    ("EURUSD", "NZDUSD"): 0.70,
    ("EURUSD", "USDCHF"): -0.95,
    ("EURUSD", "USDJPY"): -0.30,
    ("GBPUSD", "AUDUSD"): 0.65,
    ("GBPUSD", "USDCHF"): -0.85,
    ("USDJPY", "USDCHF"): 0.40,
    ("AUDUSD", "NZDUSD"): 0.90,
    ("EURJPY", "GBPJPY"): 0.85,
    ("EURUSD", "EURJPY"): 0.55,
}


def get_correlation(pair_a: str, pair_b: str) -> float:
    pair_a = pair_a.upper().replace("/", "")
    pair_b = pair_b.upper().replace("/", "")
    if pair_a == pair_b:
        return 1.0
    key1 = (pair_a, pair_b)
    key2 = (pair_b, pair_a)
    return CORRELATIONS.get(key1, CORRELATIONS.get(key2, 0.0))


@dataclass
class Position:
    pair: str
    direction: str  # "long" / "short"
    risk_usd: float


def effective_risk(positions: list[Position]) -> float:
    """
    Считает эффективный риск с учётом корреляций.
    Для скоррелированных позиций в ОДНОМ направлении риски складываются.
    Для противоположных — компенсируют.
    """
    total = 0.0
    n = len(positions)

    for i in range(n):
        # Каждая позиция вносит свой риск
        total += positions[i].risk_usd

    # Учёт корреляции между парами
    for i in range(n):
        for j in range(i + 1, n):
            corr = get_correlation(positions[i].pair, positions[j].pair)
            same_dir = positions[i].direction == positions[j].direction
            # Если корреляция и направление совпадают — увеличиваем риск
            # Если корреляция и направление противоположны — уменьшаем
            sign = 1 if same_dir else -1
            adjustment = (
                2 * corr * sign
                * (positions[i].risk_usd * positions[j].risk_usd) ** 0.5
            )
            total += adjustment * 0.5  # вес коррекции

    return max(0, total)


def print_report(deposit: float, positions: list[Position]) -> None:
    print("\n" + "=" * 60)
    print("  RISK EXPOSURE TRACKER")
    print("=" * 60)
    print(f"\nДепозит: ${deposit:,.2f}")
    print(f"\nОткрытые позиции:")
    print(f"{'Пара':<10} {'Направление':<12} {'Риск $':>10} "
          f"{'Риск %':>8}")
    print("-" * 50)
    plain_total = 0.0
    for p in positions:
        plain_total += p.risk_usd
        print(f"{p.pair:<10} {p.direction:<12} "
              f"${p.risk_usd:>9,.2f} {p.risk_usd / deposit * 100:>6.2f}%")

    print("-" * 50)
    print(f"\nНОМИНАЛЬНЫЙ риск (просто сумма):     "
          f"${plain_total:,.2f} ({plain_total / deposit * 100:.2f}%)")

    eff = effective_risk(positions)
    print(f"ЭФФЕКТИВНЫЙ риск (с корреляциями):   "
          f"${eff:,.2f} ({eff / deposit * 100:.2f}%)")

    if eff / deposit > 0.02:
        print(f"\n⚠️  Эффективный риск > 2% депозита — много для новичка")
    if eff > plain_total * 1.2:
        print(f"⚠️  Эффективный риск намного больше номинального — "
              f"твои позиции скоррелированы. Это «двойная ставка» в одну сторону.")

    print("\nКорреляции между парами:")
    n = len(positions)
    for i in range(n):
        for j in range(i + 1, n):
            corr = get_correlation(positions[i].pair, positions[j].pair)
            same_dir = positions[i].direction == positions[j].direction
            marker = "↔" if same_dir else "⇄"
            if abs(corr) > 0.5:
                level = "СИЛЬНАЯ"
                emoji = "⚠️ " if same_dir else "✓"
            elif abs(corr) > 0.3:
                level = "средняя"
                emoji = ""
            else:
                level = "слабая"
                emoji = ""
            print(f"  {emoji} {positions[i].pair} {marker} "
                  f"{positions[j].pair}: ρ = {corr:+.2f} ({level})")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Risk Exposure Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  Через CLI:
    python risk_exposure.py --deposit 1000 \\
      --pos EURUSD long 5 \\
      --pos GBPUSD long 5

  Интерактивно (без --pos):
    python risk_exposure.py --deposit 1000
""",
    )
    parser.add_argument("--deposit", "-d", type=float, required=True,
                        help="Размер депозита ($)")
    parser.add_argument(
        "--pos", action="append", nargs=3,
        metavar=("PAIR", "DIRECTION", "RISK_USD"),
        help="Открытая позиция: пара направление риск_в_долларах",
    )
    args = parser.parse_args()

    positions: list[Position] = []
    if args.pos:
        for pair, direction, risk in args.pos:
            positions.append(Position(pair, direction, float(risk)))
    else:
        print("Введи открытые позиции (пусто = закончить):")
        i = 1
        while True:
            try:
                pair = input(f"  [{i}] Пара (например EURUSD): ").strip()
                if not pair:
                    break
                direction = input("      Направление (long/short): ").strip()
                risk = float(input("      Риск в USD: ").strip())
                positions.append(Position(pair, direction, risk))
                i += 1
            except (ValueError, EOFError, KeyboardInterrupt):
                break

    if not positions:
        print("Нет открытых позиций.")
        return 0

    print_report(args.deposit, positions)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
