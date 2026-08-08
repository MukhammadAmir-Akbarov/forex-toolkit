#!/usr/bin/env python3
"""Считает, что делает одна и та же стратегия на разных парах.

Продолжение `overfit_scan.py`, но вопрос другой. Там мы спрашивали «переносится
ли настройка во времени». Здесь — «переносится ли она между рынками».

Берём параметры, оказавшиеся лучшими на EUR/USD, и запускаем их без изменений
на всех остальных парах за тот же период. Заодно для каждой пары ищем её
собственные лучшие параметры из той же сетки: если у каждой пары «лучшие» свои,
значит «лучшие» — свойство не стратегии, а выборки.

Данные (`data/*.csv`) не в репозитории, в CI не посчитать. Результат фиксируется
в `_mkdocs/data/multipair.json` вместе с перечнем пар и периодом.

Симуляцию сделок НЕ переписываем: берём `advanced/parameter_sweep.evaluate`.

Запуск:
    python tools/multipair_scan.py --timeframe 1h
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "advanced"))
sys.path.insert(0, str(ROOT / "bot"))

from parameter_sweep import evaluate  # noqa: E402

GRID: dict[str, list] = {
    "rr": [1.5, 2.0, 3.0],
    "stop_buffer": [2, 5, 10],
    "ema_dist": [5, 10, 20],
    "rsi_low": [40, 45],
}
RSI_HIGH = 65
MIN_TRADES = 20
HOME_PAIR = "EURUSD"


def pip_size(pair: str) -> float:
    """Пункт: 0.01 для пар с иеной, 0.0001 для остальных.

    Не мелочь. Первый прогон шёл с общим 0.0001, и на иеновых парах фильтр
    «в пределах N пунктов от EMA» считался в стократно завышенных единицах:
    GBP/JPY дал НОЛЬ сделок за два года, USD/JPY — четыре. Выглядело как
    вывод про рынок, а было ошибкой измерения.
    """
    return 0.01 if pair.upper().endswith("JPY") else 0.0001


def _as_dict(result) -> dict:
    return {
        "total_r": round(result.total_r, 3),
        "trades": result.n_trades,
        "win_rate": round(result.win_rate, 2),
        "profit_factor": round(min(result.profit_factor, 99), 3),
        "max_dd": round(result.max_dd, 3),
    }


def _combos() -> list[dict]:
    keys = list(GRID)
    return [
        dict(zip(keys, combo)) for combo in itertools.product(*[GRID[k] for k in keys])
    ]


def _best_for(df: pd.DataFrame, pip: float) -> tuple[dict, dict]:
    """Лучшая комбинация сетки для одного набора свечей.

    Возвращает пустые словари, если ни одна комбинация не набрала `MIN_TRADES`.
    Пустое — это НЕ ноль: «сделок не хватило» и «результат нулевой» разные
    вещи, и на странице они обязаны выглядеть по-разному.
    """
    best_params, best_result = None, None
    for params in _combos():
        result = evaluate(df, params | {"rsi_high": RSI_HIGH, "pip_size": pip})
        if result.n_trades < MIN_TRADES:
            continue
        if best_result is None or result.total_r > best_result.total_r:
            best_params, best_result = params, result
    return best_params or {}, _as_dict(best_result) if best_result else {}


def scan(timeframe: str) -> dict:
    files = sorted((ROOT / "data").glob(f"*_{timeframe}.csv"))
    if not files:
        raise SystemExit(f"нет файлов data/*_{timeframe}.csv")

    home = ROOT / "data" / f"{HOME_PAIR}_{timeframe}.csv"
    if not home.exists():
        raise SystemExit(f"нет опорной пары {home}")

    print(f"Ищу лучшие параметры на {HOME_PAIR}…")
    home_params, home_result = _best_for(pd.read_csv(home), pip_size(HOME_PAIR))
    print(f"  {home_params} → {home_result['total_r']:+.1f}R")

    pairs = []
    for path in files:
        pair = path.stem.split("_")[0]
        pip = pip_size(pair)
        df = pd.read_csv(path)
        print(f"{pair} (пункт {pip})…", end=" ", flush=True)
        transferred = _as_dict(
            evaluate(df, home_params | {"rsi_high": RSI_HIGH, "pip_size": pip})
        )
        own_params, own_result = _best_for(df, pip)
        print(
            f"перенос {transferred['total_r']:+.1f}R за {transferred['trades']} сделок,"
            f" своё {own_result.get('total_r', 0):+.1f}R"
        )
        pairs.append(
            {
                "pair": pair,
                "pip_size": pip,
                "bars": len(df),
                "from": str(df.iloc[0, 0]),
                "to": str(df.iloc[-1, 0]),
                "transferred": transferred,
                "own_best": {"params": own_params, "result": own_result},
            }
        )

    return {
        "meta": {
            "home_pair": HOME_PAIR,
            "home_params": home_params,
            "home_result": home_result,
            "timeframe": timeframe,
            "grid": GRID,
            "rsi_high": RSI_HIGH,
            "min_trades": MIN_TRADES,
        },
        "pairs": pairs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument(
        "--out", type=Path, default=ROOT / "_mkdocs" / "data" / "multipair.json"
    )
    args = parser.parse_args()

    document = scan(args.timeframe)
    args.out.write_text(
        json.dumps(document, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    from forex_toolkit.multipair import summarize

    summary = summarize(document)
    print()
    print(f"записано: {args.out}")
    print(f"пар всего:            {summary.pairs}")
    print(f"в плюсе при переносе: {summary.profitable}")
    print(f"лучшая:  {summary.best.pair} {summary.best.transferred_r:+.1f}R")
    print(f"худшая:  {summary.worst.pair} {summary.worst.transferred_r:+.1f}R")
    print(f"медиана переноса:     {summary.median_r:+.1f}R")
    print(f"у скольких пар свои лучшие параметры: {summary.own_params_differ}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
