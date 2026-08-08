"""Переносится ли настройка стратегии с одной пары на другие.

`overfitting.py` отвечает на вопрос «переносится ли настройка во времени».
Здесь вопрос соседний и не менее неприятный: **переносится ли она между
рынками**. Берём параметры, лучшие на опорной паре, применяем без изменений к
остальным и смотрим на разброс.

Отдельно и намеренно разделены два разных исхода:

* **результат** — сделок хватило, число можно обсуждать;
* **мало сделок** — параметры на этой паре почти не срабатывают.

Смешивать их нельзя. Первый прогон показывал «+0.0R» там, где сделок было
ноль, и пара с четырьмя сделками попадала в «в плюсе». Выглядело как вывод,
а было отсутствием данных.

Без numpy и pandas: формулы зеркалятся в браузере один в один.
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_MIN_TRADES = 20


@dataclass(frozen=True)
class PairResult:
    pair: str
    transferred_r: float
    """Результат опорных параметров на этой паре."""
    transferred_trades: int
    own_best_r: float | None
    """Лучшее, что даёт сама пара. `None` — ни одна комбинация не набрала сделок."""
    own_params: dict
    min_trades: int = DEFAULT_MIN_TRADES

    @property
    def enough(self) -> bool:
        """Хватило ли сделок, чтобы вообще обсуждать результат."""
        return self.transferred_trades >= self.min_trades

    @property
    def gap(self) -> float | None:
        """Насколько подгонка под пару красивее переноса, в R."""
        if self.own_best_r is None:
            return None
        return self.own_best_r - self.transferred_r

    def as_dict(self) -> dict:
        return {
            "pair": self.pair,
            "transferred_r": round(self.transferred_r, 3),
            "transferred_trades": self.transferred_trades,
            "own_best_r": None
            if self.own_best_r is None
            else round(self.own_best_r, 3),
            "own_params": self.own_params,
            "enough": self.enough,
            "gap": None if self.gap is None else round(self.gap, 3),
        }


@dataclass(frozen=True)
class Summary:
    home_pair: str
    home_params: dict
    results: list[PairResult]
    best: PairResult
    worst: PairResult
    median_r: float
    profitable: int
    """Пары, где сделок хватило И результат положительный."""
    pairs: int
    measurable: int
    """Пары, где сделок хватило. Остальные — не результат, а отсутствие данных."""
    thin: int
    own_params_differ: int

    @property
    def spread(self) -> float:
        return self.best.transferred_r - self.worst.transferred_r

    @property
    def home(self) -> PairResult | None:
        return next((r for r in self.results if r.pair == self.home_pair), None)

    def as_dict(self) -> dict:
        return {
            "home_pair": self.home_pair,
            "home_params": self.home_params,
            "results": [r.as_dict() for r in self.results],
            "best": self.best.as_dict(),
            "worst": self.worst.as_dict(),
            "median_r": round(self.median_r, 3),
            "profitable": self.profitable,
            "pairs": self.pairs,
            "measurable": self.measurable,
            "thin": self.thin,
            "own_params_differ": self.own_params_differ,
            "spread": round(self.spread, 3),
        }


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def to_results(
    document: dict, *, min_trades: int = DEFAULT_MIN_TRADES
) -> list[PairResult]:
    results = []
    for entry in document.get("pairs") or []:
        transferred = entry.get("transferred") or {}
        own = entry.get("own_best") or {}
        own_result = own.get("result") or {}
        own_total = own_result.get("total_r")
        results.append(
            PairResult(
                pair=str(entry.get("pair") or "?"),
                transferred_r=float(transferred.get("total_r") or 0.0),
                transferred_trades=int(transferred.get("trades") or 0),
                own_best_r=None if own_total is None else float(own_total),
                own_params=own.get("params") or {},
                min_trades=min_trades,
            )
        )
    return results


def summarize(
    document: dict, *, min_trades: int = DEFAULT_MIN_TRADES
) -> Summary | None:
    """Сводка по переносу. `None`, если ни на одной паре сделок не хватило."""
    results = to_results(document, min_trades=min_trades)
    measurable = [r for r in results if r.enough]
    if not measurable:
        return None

    meta = document.get("meta") or {}
    home_params = meta.get("home_params") or {}
    values = [r.transferred_r for r in measurable]

    return Summary(
        home_pair=str(meta.get("home_pair") or ""),
        home_params=home_params,
        results=results,
        # Лучшая и худшая — только среди измеримых: пара без сделок не может
        # быть «худшей», она просто не участвовала.
        best=max(measurable, key=lambda r: r.transferred_r),
        worst=min(measurable, key=lambda r: r.transferred_r),
        median_r=_median(values),
        profitable=sum(1 for value in values if value > 0),
        pairs=len(results),
        measurable=len(measurable),
        thin=len(results) - len(measurable),
        own_params_differ=sum(
            1 for r in results if r.own_params and r.own_params != home_params
        ),
    )
