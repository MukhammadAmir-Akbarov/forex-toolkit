#!/usr/bin/env python3
"""Считает демонстрацию переобучения на РЕАЛЬНЫХ котировках.

Идея одна и она неприятная: подобрать лучшие параметры на первой половине
истории и посмотреть, что они сделали на второй. Если «лучшие» на прошлом
ничем не лучше остальных на будущем — значит подбор ловил шум, а не
закономерность. На этом и продают «роботов»: показывают левую половину.

Данные (`data/*.csv`) не в репозитории, посчитать в CI нельзя. Поэтому результат
фиксируется один раз в `_mkdocs/data/overfitting.json` и оттуда читается сайтом.
Файл содержит и параметры прогона, чтобы число нельзя было выдать за «вообще
так бывает»: конкретная пара, таймфрейм и период.

Симуляцию сделок НЕ переписываем: берём `advanced/parameter_sweep.evaluate` —
в проекте уже четыре копии этой логики, пятая не нужна.

Запуск:
    python tools/overfit_scan.py --csv data/EURUSD_1h.csv --out _mkdocs/data/overfitting.json
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

# Сетка намеренно небольшая: 3×3×3×2 = 54 комбинации. Дело не в размере сетки —
# чем она крупнее, тем СИЛЬНЕЕ переобучение, и это тоже часть урока.
GRID: dict[str, list] = {
    "rr": [1.5, 2.0, 3.0],
    "stop_buffer": [2, 5, 10],
    "ema_dist": [5, 10, 20],
    "rsi_low": [40, 45],
}
RSI_HIGH = 65
MIN_TRADES = 20


def _split(df: pd.DataFrame, ratio: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Делит историю по времени, а не случайно.

    Случайное деление здесь было бы враньём: в реальности будущее приходит
    после прошлого, а не вперемешку с ним.
    """
    cut = int(len(df) * ratio)
    return df.iloc[:cut].reset_index(drop=True), df.iloc[cut:].reset_index(drop=True)


def _as_dict(result) -> dict:
    return {
        "total_r": round(result.total_r, 3),
        "trades": result.n_trades,
        "win_rate": round(result.win_rate, 2),
        "profit_factor": round(min(result.profit_factor, 99), 3),
        "max_dd": round(result.max_dd, 3),
    }


def scan(csv: Path, ratio: float = 0.6) -> dict:
    df = pd.read_csv(csv)
    in_sample, out_sample = _split(df, ratio)

    keys = list(GRID)
    rows = []
    combos = list(itertools.product(*[GRID[k] for k in keys]))
    for i, combo in enumerate(combos, 1):
        params = dict(zip(keys, combo)) | {"rsi_high": RSI_HIGH}
        rows.append(
            {
                "params": {k: params[k] for k in keys},
                "in": _as_dict(evaluate(in_sample, params)),
                "out": _as_dict(evaluate(out_sample, params)),
            }
        )
        print(f"  {i}/{len(combos)}", end="\r", flush=True)
    print()

    return {
        "meta": {
            "source": csv.name,
            "pair": csv.stem.split("_")[0],
            "timeframe": csv.stem.split("_")[-1],
            "bars_total": len(df),
            "bars_in": len(in_sample),
            "bars_out": len(out_sample),
            "from": str(df.iloc[0, 0]),
            "split_at": str(in_sample.iloc[-1, 0]),
            "to": str(df.iloc[-1, 0]),
            "grid": GRID,
            "rsi_high": RSI_HIGH,
            "min_trades": MIN_TRADES,
        },
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "data" / "EURUSD_1h.csv")
    parser.add_argument(
        "--out", type=Path, default=ROOT / "_mkdocs" / "data" / "overfitting.json"
    )
    parser.add_argument("--ratio", type=float, default=0.6)
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"нет файла {args.csv} — котировки не в репозитории, см. docs")
        return 1

    document = scan(args.csv, args.ratio)
    args.out.write_text(
        json.dumps(document, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    from forex_toolkit.overfitting import summarize

    summary = summarize(document["rows"], min_trades=MIN_TRADES)
    print(f"записано: {args.out} ({args.out.stat().st_size // 1024} KB)")
    print(f"лучшие на прошлом:      {summary.best_in.in_total_r:+.1f}R")
    print(f"они же на будущем:      {summary.best_in.out_total_r:+.1f}R")
    print(f"место на будущем:       {summary.rank_out} из {summary.considered}")
    print(f"медиана всех на будущем:{summary.median_out:+.1f}R")
    print(f"связь прошлого и будущего: {summary.correlation:+.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
