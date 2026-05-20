#!/usr/bin/env python3
"""
Калькулятор размера позиции для forex.

Считает размер позиции (в лотах) на основе:
  - размера депозита,
  - процента риска на сделку,
  - расстояния до стоп-лосса в пипсах,
  - валютной пары.

Использование:
  Интерактивный режим:
    python position_calculator.py

  Однострочно:
    python position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD

Никаких внешних зависимостей — только стандартная библиотека Python 3.

Disclaimer: учебный калькулятор. Точные котировки и стоимость пипса
лучше брать из терминала твоего брокера.
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass


# Приблизительная стоимость 1 пипса на 1 стандартный лот (100 000 единиц)
# при счёте в USD. Реальные значения зависят от текущего курса.
PIP_VALUE_USD_PER_LOT: dict[str, float] = {
    "EURUSD": 10.00,
    "GBPUSD": 10.00,
    "AUDUSD": 10.00,
    "NZDUSD": 10.00,
    "USDJPY": 6.70,   # зависит от курса USD/JPY (~150)
    "USDCHF": 11.30,  # зависит от курса USD/CHF (~0.88)
    "USDCAD": 7.30,   # зависит от курса USD/CAD (~1.37)
    "EURJPY": 6.70,
    "GBPJPY": 6.70,
    "EURGBP": 12.70,
}


@dataclass
class PositionResult:
    balance: float
    risk_percent: float
    risk_amount: float
    stop_pips: float
    pair: str
    pip_value: float
    lots: float
    lots_rounded: float
    actual_risk: float
    actual_risk_percent: float


def calculate_position(
    balance: float,
    risk_percent: float,
    stop_pips: float,
    pair: str,
) -> PositionResult:
    """Считает размер позиции в лотах."""
    if balance <= 0:
        raise ValueError("Депозит должен быть > 0")
    if risk_percent <= 0 or risk_percent > 10:
        raise ValueError("Риск % должен быть в диапазоне 0 < risk ≤ 10")
    if stop_pips <= 0:
        raise ValueError("Стоп в пипсах должен быть > 0")

    pair = pair.upper().replace("/", "").replace("-", "")
    if pair not in PIP_VALUE_USD_PER_LOT:
        raise ValueError(
            f"Пара {pair!r} не в таблице. Доступные: "
            + ", ".join(sorted(PIP_VALUE_USD_PER_LOT))
        )

    pip_value = PIP_VALUE_USD_PER_LOT[pair]
    risk_amount = balance * risk_percent / 100

    # Размер в стандартных лотах
    lots = risk_amount / (stop_pips * pip_value)

    # Округляем ВНИЗ до 0.01 — минимальный шаг у большинства брокеров.
    # math.floor чтобы реальный риск не превышал плановый.
    lots_rounded = math.floor(lots * 100 + 1e-9) / 100
    if lots_rounded < 0.01:
        lots_rounded = 0.01

    actual_risk = lots_rounded * stop_pips * pip_value
    actual_risk_percent = actual_risk / balance * 100

    return PositionResult(
        balance=balance,
        risk_percent=risk_percent,
        risk_amount=risk_amount,
        stop_pips=stop_pips,
        pair=pair,
        pip_value=pip_value,
        lots=lots,
        lots_rounded=lots_rounded,
        actual_risk=actual_risk,
        actual_risk_percent=actual_risk_percent,
    )


def format_result(r: PositionResult) -> str:
    """Красивый вывод в терминал."""
    warning = ""
    if r.actual_risk > r.risk_amount * 1.05:
        warning = (
            "\n⚠️  Округление дало риск БОЛЬШЕ запланированного — "
            "уменьши размер вручную до 0.01."
        )
    if r.actual_risk_percent > 2.0:
        warning += (
            "\n⚠️  Реальный риск > 2% депозита. Это много для новичка."
        )

    return f"""
╭─────────────────────────────────────────╮
│  КАЛЬКУЛЯТОР РАЗМЕРА ПОЗИЦИИ            │
╰─────────────────────────────────────────╯

Входные данные:
  Депозит:           ${r.balance:,.2f}
  Риск:              {r.risk_percent:.2f}% = ${r.risk_amount:,.2f}
  Стоп-лосс:         {r.stop_pips:.0f} пипсов
  Пара:              {r.pair}
  Стоимость пипса:   ${r.pip_value:.2f} за 1 лот

Расчёт:
  Размер (точный):   {r.lots:.4f} лота
  Размер (округл.):  {r.lots_rounded:.2f} лота
  Реальный риск:     ${r.actual_risk:.2f} ({r.actual_risk_percent:.2f}%)

→ Выстави в терминале: {r.lots_rounded:.2f} лота{warning}
"""


def interactive() -> int:
    """Интерактивный режим — задаёт вопросы пользователю."""
    print("\n=== Калькулятор размера позиции ===\n")
    try:
        balance = float(input("Депозит ($): ").strip())
        risk = float(input("Риск на сделку (%, например 0.5): ").strip())
        stop = float(input("Стоп-лосс (в пипсах): ").strip())
        pair = input(
            "Пара (EURUSD / GBPUSD / USDJPY / ...): "
        ).strip() or "EURUSD"
    except (ValueError, KeyboardInterrupt, EOFError):
        print("\nОтмена.")
        return 1

    try:
        result = calculate_position(balance, risk, stop, pair)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return 1

    print(format_result(result))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Калькулятор размера позиции для forex",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Примеры:\n"
               "  position_calculator.py\n"
               "  position_calculator.py --balance 1000 --risk 0.5 "
               "--stop 25 --pair EURUSD",
    )
    parser.add_argument("--balance", "-b", type=float,
                        help="Депозит в USD")
    parser.add_argument("--risk", "-r", type=float,
                        help="Риск на сделку в процентах (0.5 = 0.5%%)")
    parser.add_argument("--stop", "-s", type=float,
                        help="Стоп-лосс в пипсах")
    parser.add_argument("--pair", "-p", type=str,
                        default="EURUSD",
                        help="Валютная пара (по умолчанию EURUSD)")
    parser.add_argument("--list-pairs", action="store_true",
                        help="Показать список поддерживаемых пар")
    args = parser.parse_args()

    if args.list_pairs:
        print("Поддерживаемые пары:")
        for p, v in sorted(PIP_VALUE_USD_PER_LOT.items()):
            print(f"  {p:8s} ≈ ${v:.2f} / пипс / стд. лот")
        return 0

    # Если не переданы все 3 параметра — интерактивный режим
    if args.balance is None or args.risk is None or args.stop is None:
        return interactive()

    try:
        result = calculate_position(args.balance, args.risk,
                                     args.stop, args.pair)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    print(format_result(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
