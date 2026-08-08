"""Сколько стоили привычки за период.

Зачем: журнал уже хранит, соблюдался ли план, с какой эмоцией входили и на
какой паре. Но он показывает это раздельно — «дисциплина 78%», «худшая эмоция
FOMO» — и никогда не отвечает на вопрос, который меняет поведение: **во что
конкретно мне обошлась эта привычка в деньгах**. Число в долларах убеждает
там, где процент не убеждает.

Метод. Для каждой привычки делим сделки на две группы — где привычка была и
где её не было — и сравниваем средний результат. Разницу умножаем на число
сделок с привычкой: столько потеряно (или заработано) относительно того, как
человек торгует без неё.

Чего этот расчёт НЕ доказывает, и это надо говорить прямо: связь наблюдаемая,
а не причинная. Возможно, на эмоции входят в худшие моменты рынка, а не эмоция
портит сделку. На маленькой выборке разница вообще может быть шумом — поэтому
рядом всегда стоит число сделок, а привычки с одной-двумя сделками
отбрасываются.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Меньше этого числа сделок с привычкой обсуждать нечего: одна неудачная
# сделка сделает любую привычку «самой дорогой».
MIN_TRADES = 3

# Эмоции, которые журнал считает тревожными (совпадает со списком в journal.js).
TENSE_EMOTIONS = ("anxious", "frustrated", "fomo", "angry")


@dataclass(frozen=True)
class HabitCost:
    """Во что обошлась одна привычка."""

    key: str
    trades: int
    total: float
    """Суммарный результат сделок с привычкой."""
    avg_with: float
    avg_without: float
    cost: float
    """Разница со «своей нормой», умноженная на число сделок."""

    def as_dict(self) -> dict[str, float | int | str]:
        return {
            "key": self.key,
            "trades": self.trades,
            "total": round(self.total, 2),
            "avg_with": round(self.avg_with, 2),
            "avg_without": round(self.avg_without, 2),
            "cost": round(self.cost, 2),
        }


def _amount(value: object) -> float | None:
    try:
        amount = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return amount if math.isfinite(amount) else None


def _has_broken_rules(trade: dict) -> bool:
    return str(trade.get("rules", "")).lower() == "no"


def _is_tense(trade: dict) -> bool:
    return str(trade.get("emotion", "")).lower() in TENSE_EMOTIONS


HABITS = {
    "broke_rules": _has_broken_rules,
    "traded_tense": _is_tense,
}


def cost_of(trades: list[dict], matches) -> HabitCost | None:
    """Стоимость одной привычки; ``None``, если сравнивать не с чем."""
    with_habit: list[float] = []
    without: list[float] = []
    for trade in trades:
        amount = _amount(trade.get("pnl"))
        if amount is None:
            continue
        (with_habit if matches(trade) else without).append(amount)

    if len(with_habit) < MIN_TRADES or not without:
        return None

    avg_with = sum(with_habit) / len(with_habit)
    avg_without = sum(without) / len(without)
    return HabitCost(
        key="",
        trades=len(with_habit),
        total=sum(with_habit),
        avg_with=avg_with,
        avg_without=avg_without,
        cost=(avg_with - avg_without) * len(with_habit),
    )


def expensive_habits(trades: list[dict], *, limit: int = 3) -> list[HabitCost]:
    """Самые дорогие привычки периода, от худшей к лучшей.

    Возвращаются только те, что обошлись в минус: список называется «дорогие
    привычки», и хвалить за дисциплину — задача другого блока.
    """
    found: list[HabitCost] = []
    for key, matches in HABITS.items():
        measured = cost_of(trades, matches)
        if measured is None or measured.cost >= 0:
            continue
        found.append(
            HabitCost(
                key=key,
                trades=measured.trades,
                total=measured.total,
                avg_with=measured.avg_with,
                avg_without=measured.avg_without,
                cost=measured.cost,
            )
        )

    # Дополнительно — худшая группа по паре и по сетапу: это тоже привычка,
    # просто выраженная выбором инструмента.
    for field in ("pair", "setup"):
        worst = _worst_group(trades, field)
        if worst is not None:
            found.append(worst)

    found.sort(key=lambda item: item.cost)
    return found[:limit]


def _worst_group(trades: list[dict], field: str) -> HabitCost | None:
    groups: dict[str, list[float]] = {}
    for trade in trades:
        amount = _amount(trade.get("pnl"))
        name = str(trade.get(field) or "").strip()
        if amount is None or not name:
            continue
        groups.setdefault(name, []).append(amount)

    candidates = [name for name, values in groups.items() if len(values) >= MIN_TRADES]
    if len(groups) < 2 or not candidates:
        return None

    worst_name = min(candidates, key=lambda name: sum(groups[name]))
    inside = groups[worst_name]
    outside = [
        v for name, values in groups.items() if name != worst_name for v in values
    ]
    if not outside:
        return None

    avg_with = sum(inside) / len(inside)
    avg_without = sum(outside) / len(outside)
    cost = (avg_with - avg_without) * len(inside)
    if cost >= 0:
        return None
    return HabitCost(
        key=f"{field}:{worst_name}",
        trades=len(inside),
        total=sum(inside),
        avg_with=avg_with,
        avg_without=avg_without,
        cost=cost,
    )


def month_of(value: object) -> str | None:
    """``YYYY-MM`` из даты вида ``YYYY-MM-DD``."""
    text = str(value or "").strip()
    if len(text) < 7 or text[4] != "-":
        return None
    year, month = text[:4], text[5:7]
    if not (year.isdigit() and month.isdigit()):
        return None
    return f"{year}-{month}" if 1 <= int(month) <= 12 else None


def months_in(trades: list[dict]) -> list[str]:
    """Месяцы журнала от свежего к старому."""
    seen = {m for m in (month_of(t.get("date")) for t in trades) if m}
    return sorted(seen, reverse=True)


def trades_of_month(trades: list[dict], month: str) -> list[dict]:
    return [t for t in trades if month_of(t.get("date")) == month]
