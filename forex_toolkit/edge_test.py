"""Проверка «навык или везение» для результата журнала.

Зачем: Monte Carlo смотрит вперёд — «что может случиться с такими
параметрами». Он не отвечает на вопрос, который стоит новичку дороже всего:
**мог ли мой нынешний результат получиться случайно?** На 15 сделках отличить
навык от везения нельзя, и ошибаются в обе стороны — поднимают риск после
случайного плюса и бросают рабочую стратегию после нормальной просадки.

Метод. Берём нулевую гипотезу «у стратегии нет преимущества»: те же размеры
выигрыша и проигрыша, но winrate ровно безубыточный. Прогоняем много серий
такой же длины и считаем, какая доля из них дала результат не хуже
фактического. Это доля и есть ответ: если случайность повторяет твой результат
в каждой третьей серии — говорить о навыке рано.

Ограничение, которое надо назвать вслух: модель двухисходная — каждый выигрыш
равен среднему выигрышу, каждый проигрыш среднему проигрышу. Реальный разброс
внутри сделок она не учитывает, поэтому это оценка порядка величины, а не
строгий статистический вывод.

Тот же расчёт продублирован в браузере; совпадение держит сверка в tests_e2e.
"""

from __future__ import annotations

import math

from .monte_carlo import ParkMiller

# Границы вердикта по доле случайных серий, оказавшихся не хуже фактической.
LUCK_THRESHOLD = 0.20
UNCLEAR_THRESHOLD = 0.05
# Меньше этого числа сделок обсуждать нечего в принципе.
MIN_TRADES = 10


def breakeven_win_rate(avg_win_r: float, avg_loss_r: float) -> float:
    """Winrate, при котором матожидание равно нулю.

    ``avg_loss_r`` передаётся положительной величиной убытка.
    """
    if avg_win_r <= 0 or avg_loss_r <= 0:
        raise ValueError("средний выигрыш и убыток должны быть положительными")
    return avg_loss_r / (avg_win_r + avg_loss_r)


def verdict_for(probability: float) -> str:
    if probability >= LUCK_THRESHOLD:
        return "luck"
    if probability >= UNCLEAR_THRESHOLD:
        return "unclear"
    return "edge"


def luck_probability(
    *,
    trades: int,
    observed_total_r: float,
    avg_win_r: float,
    avg_loss_r: float,
    simulations: int = 5000,
    seed: int = 42,
) -> dict[str, float | int | str | bool]:
    """Доля случайных серий, давших результат не хуже фактического."""
    if trades <= 0 or simulations <= 0:
        raise ValueError("trades и simulations должны быть положительными")
    if not math.isfinite(observed_total_r):
        raise ValueError("observed_total_r must be finite")

    win_rate = breakeven_win_rate(avg_win_r, avg_loss_r)
    if trades < MIN_TRADES:
        return {
            "trades": trades,
            "enough_data": False,
            "breakeven_win_rate": win_rate,
            "probability": 1.0,
            "verdict": "not_enough",
            "median_random_r": 0.0,
            "observed_total_r": observed_total_r,
        }

    rng = ParkMiller(seed)
    totals: list[float] = []
    at_least_as_good = 0
    for _ in range(simulations):
        total = 0.0
        for _ in range(trades):
            if rng.random() < win_rate:
                total += avg_win_r
            else:
                total -= avg_loss_r
        totals.append(total)
        if total >= observed_total_r:
            at_least_as_good += 1

    probability = at_least_as_good / simulations
    ordered = sorted(totals)
    middle = len(ordered) // 2
    median = (
        ordered[middle]
        if len(ordered) % 2
        else (ordered[middle - 1] + ordered[middle]) / 2
    )
    return {
        "trades": trades,
        "enough_data": True,
        "breakeven_win_rate": win_rate,
        "probability": probability,
        "verdict": verdict_for(probability),
        "median_random_r": median,
        "observed_total_r": observed_total_r,
    }
