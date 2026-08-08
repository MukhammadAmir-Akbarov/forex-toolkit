"""Годовой итог торговли для налоговой декларации.

Зачем: журнал знает каждую сделку за год, налоговый калькулятор ждёт чистый
годовой результат, декларация в Узбекистане подаётся **до 1 апреля** — и между
этими тремя фактами в проекте не было ничего. Человек считал сумму руками по
экспорту CSV, то есть ровно там, где ошибиться проще всего.

Что считаем. Декларируется **чистый годовой результат**: прибыли минус убытки
за календарный год, а не каждая сделка отдельно. Если год закрыт в минус,
налоговой базы нет — переносить убыток на следующий год правила не позволяют,
поэтому ``taxable`` обнуляется, а не уходит в минус.

Чего НЕ считаем и почему. Комиссии и свопы уже сидят внутри ``pnl`` каждой
сделки (журнал вычитает их при закрытии), поэтому отдельной строкой они здесь
не вычитаются — иначе получилось бы двойное вычитание. Стоимость вывода денег
на карту сюда тоже не входит: это расход после торговли, и учитывается ли он —
вопрос к бухгалтеру, а не к калькулятору.

⚠️ Это оценка для понимания порядка величины, **не налоговая консультация**.
Ставка и правила меняются; сверяйся с soliq.uz.

Тот же расчёт продублирован в браузере (``journal.js``); совпадение держит
сверка в tests_e2e.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

# Ставка НДФЛ для резидента Узбекистана, проверено 2026-08-05 по сообщениям
# Налогового комитета. Меняется — правь здесь и в _mkdocs/uz/tax-calculator.md.
DEFAULT_RATE = 0.12

# Срок подачи декларации за прошедший год.
DECLARATION_MONTH = 4
DECLARATION_DAY = 1


@dataclass(frozen=True)
class YearSummary:
    """Итог одного календарного года."""

    year: int
    trades: int
    profit: float
    loss: float
    net: float
    taxable: float
    tax: float
    skipped: int = field(default=0)

    def as_dict(self) -> dict[str, float | int]:
        return {
            "year": self.year,
            "trades": self.trades,
            "profit": round(self.profit, 2),
            "loss": round(self.loss, 2),
            "net": round(self.net, 2),
            "taxable": round(self.taxable, 2),
            "tax": round(self.tax, 2),
            "skipped": self.skipped,
        }


def _year_of(value: object) -> int | None:
    """Год из даты вида ``YYYY-MM-DD``; всё непонятное отбрасываем."""
    text = str(value or "").strip()
    if len(text) < 4 or not text[:4].isdigit():
        return None
    year = int(text[:4])
    # Отсекаем явный мусор: журнал ведут люди, и опечатка в годе встречается.
    return year if 1990 <= year <= 2999 else None


def _amount_of(value: object) -> float | None:
    try:
        amount = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return amount if math.isfinite(amount) else None


def summarize_year(
    trades: list[dict], year: int, *, rate: float = DEFAULT_RATE
) -> YearSummary:
    """Прибыли, убытки и налог за один год.

    ``trades`` — записи журнала с полями ``date`` (``YYYY-MM-DD``) и ``pnl``
    в долларах. Записи без разбираемой даты или суммы считаются пропущенными:
    их надо показать пользователю, а не тихо потерять.
    """
    if rate < 0:
        raise ValueError("ставка не может быть отрицательной")

    profit = 0.0
    loss = 0.0
    counted = 0
    skipped = 0
    for trade in trades:
        if _year_of(trade.get("date")) != year:
            continue
        amount = _amount_of(trade.get("pnl"))
        if amount is None:
            skipped += 1
            continue
        counted += 1
        if amount > 0:
            profit += amount
        else:
            loss += -amount

    net = profit - loss
    # Убыточный год не даёт отрицательного налога и не переносится вперёд.
    taxable = max(0.0, net)
    return YearSummary(
        year=year,
        trades=counted,
        profit=profit,
        loss=loss,
        net=net,
        taxable=taxable,
        tax=taxable * rate,
        skipped=skipped,
    )


def summarize_all(
    trades: list[dict], *, rate: float = DEFAULT_RATE
) -> list[YearSummary]:
    """Итоги по всем годам, которые встречаются в журнале, от свежего к старому."""
    years = sorted(
        {y for y in (_year_of(t.get("date")) for t in trades) if y is not None},
        reverse=True,
    )
    return [summarize_year(trades, year, rate=rate) for year in years]


def declaration_deadline(year: int) -> str:
    """Крайний срок подачи декларации за указанный год."""
    return f"{year + 1}-{DECLARATION_MONTH:02d}-{DECLARATION_DAY:02d}"
