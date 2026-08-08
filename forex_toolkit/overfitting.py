"""Переобучение: почему «лучшие параметры» на истории ничего не обещают.

Берём один и тот же перебор параметров, посчитанный на двух отрезках времени
подряд: «прошлое» (по нему выбирают) и «будущее» (на нём проверяют). Дальше
задаём четыре вопроса, на которые продавцы «роботов» отвечать не любят:

1. Что лучшая комбинация из прошлого сделала в будущем?
2. Какое место она заняла в будущем среди всех остальных?
3. Насколько она лучше медианы — то есть лучше случайного выбора?
4. Есть ли вообще связь между результатом на прошлом и на будущем?

Если связь около нуля, подбор параметров ловил шум. Это не мнение, это число.

Модуль намеренно без numpy и pandas: те же формулы зеркалятся в браузере
(`_mkdocs/javascripts/widgets/overfitting.js`), и сверка идёт один в один.
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_MIN_TRADES = 20


@dataclass(frozen=True)
class Combo:
    """Одна комбинация параметров с результатами на обоих отрезках."""

    params: dict
    in_total_r: float
    in_trades: int
    out_total_r: float
    out_trades: int

    def as_dict(self) -> dict:
        return {
            "params": self.params,
            "in_total_r": round(self.in_total_r, 3),
            "in_trades": self.in_trades,
            "out_total_r": round(self.out_total_r, 3),
            "out_trades": self.out_trades,
        }


@dataclass(frozen=True)
class Summary:
    best_in: Combo
    """Лучшая комбинация по прошлому — та самая, которую и продают."""
    best_out: Combo
    """Лучшая по будущему. Обычно это другая комбинация — в этом всё дело."""
    rank_out: int
    """Место `best_in` в рейтинге по будущему, начиная с первого."""
    considered: int
    median_out: float
    mean_out: float
    correlation: float
    """Связь результата на прошлом и на будущем, от -1 до 1. Около нуля — шум."""

    @property
    def degradation(self) -> float:
        """Насколько результат просел: прошлое минус будущее, в R."""
        return self.best_in.in_total_r - self.best_in.out_total_r

    @property
    def beat_median(self) -> bool:
        """Обошла ли «лучшая» комбинация обычную середину — хоть на сколько."""
        return self.best_in.out_total_r > self.median_out

    def as_dict(self) -> dict:
        return {
            "best_in": self.best_in.as_dict(),
            "best_out": self.best_out.as_dict(),
            "rank_out": self.rank_out,
            "considered": self.considered,
            "median_out": round(self.median_out, 3),
            "mean_out": round(self.mean_out, 3),
            "correlation": round(self.correlation, 4),
            "degradation": round(self.degradation, 3),
            "beat_median": self.beat_median,
        }


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def correlation(xs: list[float], ys: list[float]) -> float:
    """Корреляция Пирсона. Нулевая дисперсия — ноль, а не деление на ноль.

    Ноль здесь читается буквально: результат на прошлом ничего не говорит о
    результате на будущем.
    """
    n = len(xs)
    if n < 2 or n != len(ys):
        return 0.0
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    var_x = sum((x - mean_x) ** 2 for x in xs)
    var_y = sum((y - mean_y) ** 2 for y in ys)
    if var_x <= 0 or var_y <= 0:
        return 0.0
    return cov / (var_x * var_y) ** 0.5


def to_combos(rows: list[dict], *, min_trades: int = DEFAULT_MIN_TRADES) -> list[Combo]:
    """Отбирает комбинации, у которых сделок хватает на обоих отрезках.

    Без этого фильтра «победителем» становится комбинация с двумя сделками:
    две удачи подряд дают отличный результат и ничего не значат.
    """
    combos = []
    for row in rows:
        inside, outside = row.get("in") or {}, row.get("out") or {}
        in_trades = int(inside.get("trades") or 0)
        out_trades = int(outside.get("trades") or 0)
        if in_trades < min_trades or out_trades < min_trades:
            continue
        combos.append(
            Combo(
                params=row.get("params") or {},
                in_total_r=float(inside.get("total_r") or 0.0),
                in_trades=in_trades,
                out_total_r=float(outside.get("total_r") or 0.0),
                out_trades=out_trades,
            )
        )
    return combos


def summarize(
    rows: list[dict], *, min_trades: int = DEFAULT_MIN_TRADES
) -> Summary | None:
    """Сводка по перебору. `None`, если сравнивать нечего."""
    combos = to_combos(rows, min_trades=min_trades)
    if not combos:
        return None

    # При равенстве берём первую по порядку сетки, а не случайную: иначе один и
    # тот же прогон давал бы разные «лучшие» параметры в Python и в браузере.
    best_in = max(combos, key=lambda c: c.in_total_r)
    best_out = max(combos, key=lambda c: c.out_total_r)

    outs = [c.out_total_r for c in combos]
    ranked = sorted(combos, key=lambda c: c.out_total_r, reverse=True)
    rank_out = next(i for i, c in enumerate(ranked, 1) if c.params == best_in.params)

    return Summary(
        best_in=best_in,
        best_out=best_out,
        rank_out=rank_out,
        considered=len(combos),
        median_out=_median(outs),
        mean_out=sum(outs) / len(outs),
        correlation=correlation([c.in_total_r for c in combos], outs),
    )
