"""Position size calculator — рассчитывает размер позиции по риск-менеджменту."""

from __future__ import annotations

import math
from dataclasses import dataclass

from forex_toolkit.fx_math import PIP_VALUE_USD_PER_LOT


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
    """Считает размер позиции в лотах с округлением вниз.

    Args:
        balance: депозит в USD
        risk_percent: % риска (0.5 = 0.5%)
        stop_pips: расстояние до стопа в пипсах
        pair: валютная пара (EURUSD, GBPUSD и т.д.)

    Returns:
        PositionResult с полными расчётами.

    Raises:
        ValueError: при невалидных аргументах.
    """
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
    lots = risk_amount / (stop_pips * pip_value)
    lots_rounded = math.floor(lots * 100 + 1e-9) / 100
    if lots_rounded < 0.01:
        lots_rounded = 0.01
    actual_risk = lots_rounded * stop_pips * pip_value

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
        actual_risk_percent=actual_risk / balance * 100,
    )
