"""Сколько нужно капитала, чтобы жить с трейдинга.

Зачем: «бросить работу и жить с трейдинга» — обещание, на котором продают
курсы и «сигналы». Проект честно говорит, что реалистичная доходность
скучная, но нигде не показывает, что из этого следует **в деньгах**. А следует
простое: чтобы снимать сумму месячных расходов, капитал должен быть примерно в
семьдесят раз больше неё. Увидев это число, человек принимает другое решение,
чем услышав «торговля — это не быстрые деньги».

Расчёт::

    снять на руки  ->  заработать до налога  ->  какой капитал это даёт
    need           ->  need / (1 - tax)      ->  gross / monthly_return

Что учтено и почему:

* **налог**: чтобы получить на руки, заработать надо больше на ставку НДФЛ;
* **подушка**: если снимать всю прибыль каждый месяц, убыточный месяц придётся
  покрывать из капитала. Поэтому рядом считается запас расходов на N месяцев,
  который держат отдельно от торгового счёта;
* **срок**: за сколько месяцев такой капитал накопится при текущем депозите и
  ежемесячном пополнении.

Чего расчёт НЕ обещает: что доходность будет стабильной. Это оценка порядка
величины при заданной ставке, а не план. Убыточные месяцы бывают у всех, и
именно поэтому снимать всё до копейки нельзя.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Ставка НДФЛ резидента Узбекистана — та же, что в tax_summary.
DEFAULT_TAX_RATE = 0.12

# Сколько месяцев расходов держать вне торгового счёта. Три месяца — не
# норматив, а нижняя граница здравого смысла: типичная серия убытков короче.
DEFAULT_BUFFER_MONTHS = 6

# Дальше этого горизонта прогноз бессмысленен, а цикл должен завершаться.
MAX_MONTHS = 12 * 60


@dataclass(frozen=True)
class LivingPlan:
    monthly_need: float
    monthly_return: float
    tax_rate: float
    gross_needed: float
    required_capital: float
    buffer: float
    total_needed: float
    months_to_reach: int | None
    """``None``, если при заданных вводных цель не достигается за 60 лет."""

    def as_dict(self) -> dict[str, float | int | None]:
        return {
            "monthly_need": round(self.monthly_need, 2),
            "gross_needed": round(self.gross_needed, 2),
            "required_capital": round(self.required_capital, 2),
            "buffer": round(self.buffer, 2),
            "total_needed": round(self.total_needed, 2),
            "months_to_reach": self.months_to_reach,
        }


def months_to_reach(
    target: float, *, start: float, monthly_add: float, monthly_return: float
) -> int | None:
    """За сколько месяцев капитал дорастёт до цели.

    Считаем шагами, а не формулой: пополнение и доходность применяются в том же
    порядке, что в жизни, и функция честно возвращает ``None``, если цель
    недостижима (например, пополнения нет, а доходность нулевая).
    """
    if target <= 0:
        return 0
    if start >= target:
        return 0
    if monthly_return <= 0 and monthly_add <= 0:
        return None

    balance = start
    for month in range(1, MAX_MONTHS + 1):
        balance = balance * (1 + monthly_return) + monthly_add
        if balance >= target:
            return month
    return None


def plan_for(
    *,
    monthly_need: float,
    monthly_return: float,
    tax_rate: float = DEFAULT_TAX_RATE,
    buffer_months: int = DEFAULT_BUFFER_MONTHS,
    start: float = 0.0,
    monthly_add: float = 0.0,
) -> LivingPlan:
    """Капитал, подушка и срок для заданных месячных расходов."""
    if monthly_need <= 0:
        raise ValueError("месячные расходы должны быть положительными")
    if not 0 < monthly_return < 1:
        raise ValueError("месячная доходность задаётся долей от 0 до 1")
    if not 0 <= tax_rate < 1:
        raise ValueError("ставка налога задаётся долей от 0 до 1")
    if buffer_months < 0:
        raise ValueError("подушка не может быть отрицательной")
    if not math.isfinite(start) or not math.isfinite(monthly_add):
        raise ValueError("стартовый капитал и пополнение должны быть числами")

    gross = monthly_need / (1 - tax_rate)
    capital = gross / monthly_return
    buffer = monthly_need * buffer_months
    total = capital + buffer
    return LivingPlan(
        monthly_need=monthly_need,
        monthly_return=monthly_return,
        tax_rate=tax_rate,
        gross_needed=gross,
        required_capital=capital,
        buffer=buffer,
        total_needed=total,
        months_to_reach=months_to_reach(
            total, start=start, monthly_add=monthly_add, monthly_return=monthly_return
        ),
    )
