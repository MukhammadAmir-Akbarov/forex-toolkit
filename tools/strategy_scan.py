#!/usr/bin/env python3
"""Сравнивает стратегии на РЕАЛЬНЫХ котировках и проверяет устойчивость места.

`strategies/compare.py` считает на синтетических свечах (`generate_synthetic`).
Для картинки в учебнике это приемлемо, для утверждения «эта стратегия лучше» —
нет: числа были бы выдуманными. Здесь берутся настоящие котировки.

И вопрос ставится не «какая лучше», а честнее: **сохраняется ли порядок**.
Ранжируем стратегии по первой половине истории, затем смотрим, какие места они
заняли во второй. Если порядок рассыпается, то «лучшая стратегия по бэктесту» —
такой же артефакт отбора, как «лучшие параметры» на странице про переобучение.

Ни симуляция сделок, ни статистика не переписываются: берём `simulate` и
`stats` из `strategies/compare.py`.

Запуск:
    python tools/strategy_scan.py --csv data/EURUSD_1h.csv
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bot"))

from strategies import breakout, breakout_v2, london_open  # noqa: E402
from strategies import mean_reversion, three_soldiers  # noqa: E402
from strategies.common import Direction, Signal  # noqa: E402
from strategies.compare import simulate, stats  # noqa: E402

MIN_TRADES = 20


def _ema_pullback(df: pd.DataFrame) -> list[Signal]:
    """Штатная стратегия проекта — та, что живёт в bot/strategy.py."""
    from strategy import detect_signals, prepare_dataframe

    prepared = prepare_dataframe(df)
    return [
        Signal(
            bar_index=s.bar_index,
            timestamp=s.timestamp,
            direction=Direction(s.direction.value),
            entry=s.entry,
            stop=s.stop,
            take=s.take,
            stop_pips=s.stop_pips,
            rr=s.rr,
            reason=s.reason,
            strategy="ema_pullback",
        )
        for s in detect_signals(prepared)
    ]


STRATEGIES: dict[str, object] = {
    "EMA50 Pullback": _ema_pullback,
    "Mean Reversion": mean_reversion.detect,
    "Breakout": breakout.detect,
    "Breakout v2": breakout_v2.detect,
    "Three Soldiers": three_soldiers.detect,
    "London Open Range": london_open.detect,
}


def _with_time_index(df: pd.DataFrame) -> pd.DataFrame:
    """Ставит временной индекс — без него часть стратегий молча ничего не видит.

    `london_open.detect` первым делом проверяет `isinstance(df.index,
    DatetimeIndex)` и при обычном индексе возвращает пустой список. Ошибки при
    этом нет: стратегия просто «не находит сигналов». Первый прогон дал по ней
    НОЛЬ сделок в обеих половинах, и это выглядело как её свойство.
    """
    column = next(
        (c for c in ("datetime", "Datetime", "date", "timestamp") if c in df.columns),
        None,
    )
    if column is None:
        return df
    prepared = df.copy()
    prepared[column] = pd.to_datetime(prepared[column], utc=True)
    return prepared.set_index(column)


def _half(df: pd.DataFrame, ratio: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    cut = int(len(df) * ratio)
    return df.iloc[:cut], df.iloc[cut:]


def _measure(df: pd.DataFrame, detect) -> dict:
    trades = simulate(df, detect(df))
    numbers = stats(trades)
    return {
        "total_r": round(float(numbers["total_r"]), 3),
        "trades": int(numbers["total"]),
        "win_rate": round(float(numbers["win_rate"]), 2),
        "profit_factor": round(min(float(numbers["pf"]), 99), 3),
        "max_dd": round(float(numbers["dd"]), 3),
    }


def scan(csv: Path, ratio: float = 0.6) -> dict:
    raw = pd.read_csv(csv)
    df = _with_time_index(raw)
    past, future = _half(df, ratio)

    rows = []
    for name, detect in STRATEGIES.items():
        print(f"{name}…", end=" ", flush=True)
        row = {
            "name": name,
            "past": _measure(past, detect),
            "future": _measure(future, detect),
        }
        print(
            f"прошлое {row['past']['total_r']:+.1f}R за {row['past']['trades']},"
            f" будущее {row['future']['total_r']:+.1f}R за {row['future']['trades']}"
        )
        rows.append(row)

    return {
        "meta": {
            "source": csv.name,
            "pair": csv.stem.split("_")[0],
            "timeframe": csv.stem.split("_")[-1],
            "bars_total": len(df),
            "bars_past": len(past),
            "bars_future": len(future),
            "from": str(df.index[0]),
            "split_at": str(past.index[-1]),
            "to": str(df.index[-1]),
            "min_trades": MIN_TRADES,
        },
        "strategies": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "data" / "EURUSD_1h.csv")
    parser.add_argument(
        "--out", type=Path, default=ROOT / "_mkdocs" / "data" / "strategies.json"
    )
    parser.add_argument("--ratio", type=float, default=0.6)
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"нет файла {args.csv} — котировки не в репозитории")
        return 1

    document = scan(args.csv, args.ratio)
    args.out.write_text(
        json.dumps(document, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    from forex_toolkit.strategy_ranking import summarize

    summary = summarize(document, min_trades=MIN_TRADES)
    print()
    print(f"записано: {args.out}")
    if summary is None:
        print("сравнивать нечего: ни одна стратегия не набрала сделок")
        return 0
    print(f"стратегий в сравнении:   {summary.considered}")
    print(
        f"лучшая на прошлом:       {summary.best_past.name} {summary.best_past.past_r:+.1f}R"
    )
    print(
        f"она же на будущем:       {summary.best_past.future_r:+.1f}R, место {summary.best_past_rank_future}"
    )
    print(
        f"лучшая на будущем:       {summary.best_future.name} {summary.best_future.future_r:+.1f}R"
    )
    print(f"совпадение порядка:      {summary.rank_correlation:+.2f}")
    print(f"мест сохранили:          {summary.kept_place} из {summary.considered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
