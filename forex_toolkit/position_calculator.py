"""Position size calculator — рассчитывает размер позиции по риск-менеджменту."""

from __future__ import annotations

from dataclasses import dataclass

from forex_toolkit.fx_math import MIN_LOT, PIP_VALUE_USD_PER_LOT, calc_lots


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
    # True, когда лот пришлось поднять до минимального (MIN_LOT) и из-за этого
    # фактический риск превысил плановый. Калькулятор/виджет должны предупредить.
    risk_exceeds_plan: bool = False


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

    # Округление вниз — единый источник формулы в fx_math.calc_lots
    # (не дублируем math.floor здесь; см. CLAUDE.md).
    lots_rounded = calc_lots(risk_amount, stop_pips, pip_value)
    # Брокер не примет лот меньше минимального шага. Поднимаем до MIN_LOT —
    # но тогда фактический риск может превысить плановый, помечаем флагом.
    if lots_rounded < MIN_LOT:
        lots_rounded = MIN_LOT
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
        risk_exceeds_plan=actual_risk > risk_amount + 1e-9,
    )
