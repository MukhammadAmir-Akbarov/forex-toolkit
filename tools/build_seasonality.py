#!/usr/bin/env python3
"""Сезонность валютных пар: средний ход каждого календарного месяца.

Читает data/<PAIR>_1d.csv (8 пар) и отвечает на вопрос «в какие месяцы пара
исторически ходила чаще и сильнее»: для каждой пары и каждого из 12 месяцев
считает по дневным свечам месячные лог-доходности и по ним — среднее,
медиану, долю положительных лет и число наблюдений.

Сезонность на форексе — слабый эффект: 5–20 наблюдений на месяц не дают
значимости, поэтому JSON честно несёт n (число лет) в каждой ячейке, а
виджет помечает тонкую выборку. Это контекст для плана, а не сигнал входа.

Результат — _mkdocs/data/seasonality.json для страницы tools/seasonality.md.
Штамп generated_at ставит rebuild_showcase_data.py (при самостоятельном
запуске ставим сами).
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
OUT_PATH = ROOT / "_mkdocs" / "data" / "seasonality.json"

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

# Меньше стольких лет наблюдений на месяц — ячейка «тонкая», доверять ей нельзя.
THIN_SAMPLE = 10


def load_daily_closes(pair: str, data_dir: Path = DATA_DIR) -> list[tuple[str, float]]:
    """Дневные закрытия пары: (YYYY-MM-DD, close), отсортированы по дате."""
    path = data_dir / f"{pair}_1d.csv"
    if not path.exists():
        sys.exit(f"❌ Нет котировок: {path} (скачайте через tools/fetch_quotes.py)")
    rows: list[tuple[str, float]] = []
    with path.open(encoding="utf-8") as fh:
        header = fh.readline()
        if "close" not in header:
            sys.exit(f"❌ Неожиданный формат {path}: {header.strip()}")
        for line in fh:
            parts = line.strip().split(",")
            if len(parts) < 5:
                continue
            rows.append((parts[0][:10], float(parts[4])))
    rows.sort()
    return rows


def monthly_returns(closes: list[tuple[str, float]]) -> dict[tuple[int, int], float]:
    """Лог-доходность каждого календарного месяца: {(год, месяц): ret}.

    Месяц считается по последнему торговому дню в данных: закрытие месяца
    против закрытия предыдущего. Первый месяц ряда пропускаем — у него нет
    честной точки отсчёта.
    """
    last_close_by_month: dict[tuple[int, int], float] = {}
    for day, close in closes:
        year, month = int(day[:4]), int(day[5:7])
        last_close_by_month[(year, month)] = close

    months = sorted(last_close_by_month)
    returns: dict[tuple[int, int], float] = {}
    for previous, current in zip(months, months[1:]):
        # Считаем только смежные календарные месяцы: дыра в данных (например,
        # пропущенный месяц) не должна превращаться в «доходность за месяц».
        py, pm = previous
        cy, cm = current
        if (cy * 12 + cm) - (py * 12 + pm) != 1:
            continue
        returns[current] = math.log(
            last_close_by_month[current] / last_close_by_month[previous]
        )
    return returns


def seasonality_stats(returns: dict[tuple[int, int], float]) -> list[dict]:
    """Двенадцать ячеек (янв–дек): среднее, медиана, доля плюсовых лет, n."""
    stats: list[dict] = []
    for month in range(1, 13):
        values = sorted(ret for (year, m), ret in returns.items() if m == month)
        n = len(values)
        if not values:
            stats.append({"avg": None, "median": None, "pos": None, "n": 0})
            continue
        mid = len(values) // 2
        median = values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2
        stats.append(
            {
                "avg": round(sum(values) / len(values) * 100, 2),
                "median": round(median * 100, 2),
                "pos": round(sum(1 for v in values if v > 0) / len(values), 2),
                "n": n,
            }
        )
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--stamp", default=None, help="дата generated_at (YYYY-MM-DD)")
    args = parser.parse_args()

    stats_by_pair: dict[str, list[dict]] = {}
    span_from, span_to = "9999", ""
    for pair in PAIRS:
        closes = load_daily_closes(pair)
        stats_by_pair[pair] = seasonality_stats(monthly_returns(closes))
        span_from = min(span_from, closes[0][0])
        span_to = max(span_to, closes[-1][0])

    document = {
        "meta": {
            "generated_at": args.stamp or datetime.now(timezone.utc).date().isoformat(),
            "source": "tools/build_seasonality.py",
            "timeframe": "1d",
            "from": span_from,
            "to": span_to,
            "range": {"from": span_from, "to": span_to},
            "thin_sample_below": THIN_SAMPLE,
        },
        "pairs": PAIRS,
        "months": list(range(1, 13)),
        "stats": stats_by_pair,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(document, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    thinnest = min(
        (
            (pair, month + 1, cell["n"])
            for pair in PAIRS
            for month, cell in enumerate(stats_by_pair[pair])
            if cell["n"]
        ),
        key=lambda item: item[2],
        default=None,
    )
    try:
        shown = args.out.relative_to(ROOT)
    except ValueError:  # --check пишет во временный каталог вне репозитория
        shown = args.out
    note = (
        f"самая тонкая ячейка: {thinnest[0]} месяц {thinnest[1]} ({thinnest[2]} лет)"
        if thinnest
        else "наблюдений нет"
    )
    print(f"✅ {shown}: {len(PAIRS)} пар × 12 месяцев, {span_from} → {span_to}; {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
