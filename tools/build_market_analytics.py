#!/usr/bin/env python3
"""Тепловая карта волатильности и матрица корреляций из локальных котировок.

Читает data/<PAIR>_1h.csv (8 пар), считает:
  * volatility[pips]: средний True Range в пипсах по каждому часу суток (UTC)
    для каждой пары — «когда рынок реально двигается»;
  * correlations: матрица 8×8 Пирсона по часовым лог-доходностям —
    «какие пары ходят вместе» (открывая обе, вы удваиваете риск).

Результат — _mkdocs/data/market-analytics.json для страницы
tools/market-analytics.md. Штамп generated_at ставит rebuild_showcase_data.py
(при самостоятельном запуске ставим сами).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_PATH = ROOT / "_mkdocs" / "data" / "market-analytics.json"

PAIRS = [
    "AUDUSD",
    "EURJPY",
    "EURUSD",
    "GBPJPY",
    "GBPUSD",
    "NZDUSD",
    "USDCAD",
    "USDJPY",
]

# Минимум общих часовых баров для честной корреляции; меньше — данных не хватает.
MIN_OVERLAP = 500


def pip_size(pair: str) -> float:
    return 0.01 if pair.endswith("JPY") else 0.0001


def load_candles(pair: str) -> list[dict]:
    """Свечи пары: час UTC, true range в пипсах, лог-доходность close."""
    path = DATA_DIR / f"{pair}_1h.csv"
    if not path.exists():
        sys.exit(f"❌ Нет котировок: {path} (скачайте через tools/fetch_quotes.py)")
    candles: list[dict] = []
    prev_close: float | None = None
    with path.open(encoding="utf-8") as fh:
        header = fh.readline()
        if "open" not in header:
            sys.exit(f"❌ Неожиданный формат {path}: {header.strip()}")
        for line in fh:
            stamp, open_, high, low, close = line.strip().split(",")
            moment = datetime.fromisoformat(stamp).astimezone(timezone.utc)
            high_f, low_f, close_f = float(high), float(low), float(close)
            if prev_close is None:
                prev_close = float(open_)
            true_range = max(
                high_f - low_f,
                abs(high_f - prev_close),
                abs(low_f - prev_close),
            )
            log_return = math.log(close_f / prev_close) if prev_close > 0 else 0.0
            candles.append(
                {
                    "hour": moment.hour,
                    "stamp": moment.strftime("%Y-%m-%dT%H:00"),
                    "tr_pips": true_range / pip_size(pair),
                    "ret": log_return,
                }
            )
            prev_close = close_f
    return candles


def volatility_matrix(candles_by_pair: dict[str, list[dict]]) -> dict:
    """Средний TR в пипсах по часам UTC для каждой пары."""
    matrix: dict[str, list[float]] = {}
    for pair, candles in candles_by_pair.items():
        sums = [0.0] * 24
        counts = [0] * 24
        for candle in candles:
            sums[candle["hour"]] += candle["tr_pips"]
            counts[candle["hour"]] += 1
        matrix[pair] = [
            round(sums[h] / counts[h], 1) if counts[h] else 0.0 for h in range(24)
        ]
    return {
        "unit": "pips",
        "hours_utc": list(range(24)),
        "pairs": PAIRS,
        "values": matrix,
    }


def correlation_matrix(candles_by_pair: dict[str, list[dict]]) -> dict:
    """Пирсон 8×8 по часовым лог-доходностям на общих барах."""
    returns_by_stamp = {
        pair: {c["stamp"]: c["ret"] for c in candles}
        for pair, candles in candles_by_pair.items()
    }
    matrix: list[list[float | None]] = []
    for left in PAIRS:
        row: list[float | None] = []
        for right in PAIRS:
            common = sorted(set(returns_by_stamp[left]) & set(returns_by_stamp[right]))
            if len(common) < MIN_OVERLAP:
                row.append(None)
                continue
            xs = [returns_by_stamp[left][t] for t in common]
            ys = [returns_by_stamp[right][t] for t in common]
            row.append(round(_pearson(xs, ys), 2))
        matrix.append(row)
    return {"pairs": PAIRS, "values": matrix}


def _pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    var_x = sum((x - mean_x) ** 2 for x in xs)
    var_y = sum((y - mean_y) ** 2 for y in ys)
    if var_x == 0 or var_y == 0:
        return 1.0 if xs == ys else 0.0
    return cov / math.sqrt(var_x * var_y)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--stamp", default=None, help="дата generated_at (YYYY-MM-DD)")
    args = parser.parse_args()

    candles_by_pair = {pair: load_candles(pair) for pair in PAIRS}
    first_stamp = min(c["stamp"] for c in candles_by_pair[PAIRS[0]])
    last_stamp = max(c["stamp"] for c in candles_by_pair[PAIRS[0]])

    document = {
        "meta": {
            "generated_at": args.stamp or datetime.now(timezone.utc).date().isoformat(),
            "source": "tools/build_market_analytics.py",
            "timeframe": "1h",
            "from": first_stamp,
            "to": last_stamp,
            "range": {"from": first_stamp, "to": last_stamp},
        },
        "pairs": PAIRS,
        "volatility": volatility_matrix(candles_by_pair),
        "correlations": correlation_matrix(candles_by_pair),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(document, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    vol = document["volatility"]["values"]
    hottest = max(
        ((pair, h) for pair in PAIRS for h in range(24)),
        key=lambda ph: vol[ph[0]][ph[1]],
    )
    try:
        shown = args.out.relative_to(ROOT)
    except ValueError:  # --check пишет во временный каталог вне репозитория
        shown = args.out
    print(
        f"✅ {shown}: {len(PAIRS)} пар, "
        f"{len(candles_by_pair[PAIRS[0]])} баров каждая; "
        f"пик волатильности — {hottest[0]} в {hottest[1]:02d}:00 UTC "
        f"({vol[hottest[0]][hottest[1]]} пипсов)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
