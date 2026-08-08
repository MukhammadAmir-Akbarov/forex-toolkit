"""Сохраняется ли порядок стратегий при переходе из прошлого в будущее.

Третий вопрос той же семьи. `overfitting.py` — переносится ли настройка во
времени. `multipair.py` — переносится ли она между рынками. Здесь: **держится
ли рейтинг самих стратегий**.

Вопрос «какая стратегия лучше» бессмысленно задавать одной выборке: выбрать
лучшую из шести — это тот же отбор, что выбрать лучшую из 54 комбинаций
параметров. Осмысленный вопрос другой: если проранжировать стратегии по первой
половине истории, сохранится ли порядок во второй.

Меру берём ранговую (Спирмен), а не обычную корреляцию: нас интересует
**порядок**, а не величины. Стратегия, заработавшая вдвое больше, не обязана
быть вдвое лучше — но обязана остаться выше, если рейтинг вообще о чём-то
говорит.

Без numpy и pandas: зеркалится в браузере один в один.
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_MIN_TRADES = 20


@dataclass(frozen=True)
class StrategyResult:
    name: str
    past_r: float
    past_trades: int
    future_r: float
    future_trades: int

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "past_r": round(self.past_r, 3),
            "past_trades": self.past_trades,
            "future_r": round(self.future_r, 3),
            "future_trades": self.future_trades,
        }


@dataclass(frozen=True)
class Summary:
    results: list[StrategyResult]
    """Только те, у кого сделок хватило на обеих половинах."""
    best_past: StrategyResult
    best_future: StrategyResult
    best_past_rank_future: int
    """Место лучшей по прошлому в рейтинге по будущему, начиная с первого."""
    considered: int
    kept_place: int
    """Сколько стратегий сохранили ровно своё место."""
    rank_correlation: float
    """Спирмен по местам: 1 — порядок сохранился, 0 — рассыпался."""
    skipped: int
    """Стратегии, где сделок не хватило хотя бы на одной половине."""

    @property
    def order_held(self) -> bool:
        """Считаем порядок сохранившимся при связи 0.5 и выше.

        Порог не из статистики, а из здравого смысла: ниже половины рейтинг
        уже нельзя предъявлять как довод при выборе стратегии.
        """
        return self.rank_correlation >= 0.5

    def as_dict(self) -> dict:
        return {
            "results": [r.as_dict() for r in self.results],
            "best_past": self.best_past.as_dict(),
            "best_future": self.best_future.as_dict(),
            "best_past_rank_future": self.best_past_rank_future,
            "considered": self.considered,
            "kept_place": self.kept_place,
            "rank_correlation": round(self.rank_correlation, 4),
            "skipped": self.skipped,
            "order_held": self.order_held,
        }


def _ranks(values: list[float]) -> list[float]:
    """Места по убыванию значения. Равным значениям — среднее место.

    Средний ранг для равных обязателен: иначе порядок в списке (то есть порядок
    объявления стратегий) влиял бы на итоговую связь.
    """
    order = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        shared = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = shared
        i = j + 1
    return ranks


def rank_correlation(xs: list[float], ys: list[float]) -> float:
    """Корреляция Спирмена: Пирсон, посчитанный на местах."""
    n = len(xs)
    if n < 2 or n != len(ys):
        return 0.0
    rx, ry = _ranks(xs), _ranks(ys)
    mean_x = sum(rx) / n
    mean_y = sum(ry) / n
    cov = sum((a - mean_x) * (b - mean_y) for a, b in zip(rx, ry))
    var_x = sum((a - mean_x) ** 2 for a in rx)
    var_y = sum((b - mean_y) ** 2 for b in ry)
    if var_x <= 0 or var_y <= 0:
        return 0.0
    return cov / (var_x * var_y) ** 0.5


def to_results(
    document: dict, *, min_trades: int = DEFAULT_MIN_TRADES
) -> tuple[list[StrategyResult], int]:
    """Отбирает стратегии, у которых сделок хватило на обеих половинах."""
    kept, skipped = [], 0
    for entry in document.get("strategies") or []:
        past = entry.get("past") or {}
        future = entry.get("future") or {}
        past_trades = int(past.get("trades") or 0)
        future_trades = int(future.get("trades") or 0)
        if past_trades < min_trades or future_trades < min_trades:
            skipped += 1
            continue
        kept.append(
            StrategyResult(
                name=str(entry.get("name") or "?"),
                past_r=float(past.get("total_r") or 0.0),
                past_trades=past_trades,
                future_r=float(future.get("total_r") or 0.0),
                future_trades=future_trades,
            )
        )
    return kept, skipped


def summarize(
    document: dict, *, min_trades: int = DEFAULT_MIN_TRADES
) -> Summary | None:
    """Сводка по устойчивости рейтинга. `None`, если сравнивать нечего."""
    results, skipped = to_results(document, min_trades=min_trades)
    if len(results) < 2:
        return None

    past = [r.past_r for r in results]
    future = [r.future_r for r in results]
    past_ranks = _ranks(past)
    future_ranks = _ranks(future)

    best_past = max(results, key=lambda r: r.past_r)
    best_future = max(results, key=lambda r: r.future_r)
    best_index = results.index(best_past)

    return Summary(
        results=results,
        best_past=best_past,
        best_future=best_future,
        best_past_rank_future=int(future_ranks[best_index]),
        considered=len(results),
        kept_place=sum(1 for a, b in zip(past_ranks, future_ranks) if a == b),
        rank_correlation=rank_correlation(past, future),
        skipped=skipped,
    )
