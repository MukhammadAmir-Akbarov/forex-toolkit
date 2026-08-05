#!/usr/bin/env python3
"""CLI report for aggregate position risk."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from forex_toolkit.risk_exposure import (
        Position,
        effective_risk as _effective_risk,
        get_correlation,
        risk_summary,
    )
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from forex_toolkit.risk_exposure import (
        Position,
        effective_risk as _effective_risk,
        get_correlation,
        risk_summary,
    )

effective_risk = _effective_risk


def print_report(deposit: float, limit: float, positions: list[Position]) -> None:
    summary = risk_summary(deposit, limit, positions)
    print("\n" + "=" * 62)
    print("  RISK EXPOSURE TRACKER")
    print("=" * 62)
    print(f"\nДепозит: ${deposit:,.2f}; лимит: {limit:.2f}%")
    print(f"{'Пара':<10} {'Направление':<12} {'Риск $':>10} {'Риск %':>9}")
    print("-" * 48)
    for position in positions:
        print(
            f"{position.pair:<10} {position.direction:<12} "
            f"${position.risk_usd:>9,.2f} "
            f"{position.risk_usd / deposit * 100:>7.2f}%"
        )
    print("-" * 48)
    print(
        f"Номинальный риск: ${summary['nominal_usd']:,.2f} "
        f"({summary['nominal_percent']:.2f}%)"
    )
    print(
        f"Корреляционная оценка: ${summary['effective_usd']:,.2f} "
        f"({summary['effective_percent']:.2f}%)"
    )
    print(f"Остаток лимита: ${summary['remaining_usd']:,.2f}")
    if summary["over_budget"]:
        print("\nВНИМАНИЕ: номинальный риск превышает общий лимит.")

    print("\nВалютная экспозиция (знак и USD-прокси риска):")
    for currency, amount in sorted(summary["currency_exposure"].items()):
        print(f"  {currency}: {amount:+.2f}")

    print("\nСильные связи между позициями:")
    found = False
    for index, first in enumerate(positions):
        for second in positions[index + 1 :]:
            correlation = get_correlation(first.pair, second.pair)
            if abs(correlation) >= 0.7:
                found = True
                print(f"  {first.pair} / {second.pair}: {correlation:+.2f}")
    if not found:
        print("  нет известных сильных связей")


def main() -> int:
    parser = argparse.ArgumentParser(description="Учёт совокупного риска")
    parser.add_argument("--deposit", "-d", type=float, required=True)
    parser.add_argument("--limit", type=float, default=2.0)
    parser.add_argument(
        "--pos",
        action="append",
        nargs=3,
        metavar=("PAIR", "DIRECTION", "RISK_USD"),
    )
    args = parser.parse_args()

    positions: list[Position] = []
    if args.pos:
        positions = [Position(pair, direction, float(risk)) for pair, direction, risk in args.pos]
    else:
        print("Введи позиции (пустая пара завершает ввод):")
        while True:
            try:
                pair = input("  Пара: ").strip()
                if not pair:
                    break
                direction = input("  Направление (long/short): ").strip()
                risk = float(input("  Риск в USD: ").strip())
                positions.append(Position(pair, direction, risk))
            except (ValueError, EOFError, KeyboardInterrupt) as error:
                print(f"Некорректный ввод: {error}")
                break
    if not positions:
        print("Нет позиций.")
        return 1
    print_report(args.deposit, args.limit, positions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
