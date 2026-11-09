#!/usr/bin/env python3
"""Обзор «Неделя на рынке»: архив последних полных недель с топ-3 движениями.

Читает data/<PAIR>_1h.csv (те же восемь пар, что у Replay и аналитики) и для
каждой из последних N полных недель (пн–вс, по умолчанию 8) считает по каждой
паре: ход недели в пипсах и в ATR, день пика, часовые свечи для мини-графика.
Топ-3 по |ход| в ATR — это «движения недели»: пипсы у пар разные, а ход в
единицах собственной волатильности сравним.

Результат — _mkdocs/data/weekly-review.json для страницы
tools/weekly-review.md; виджет листает недели кнопками. Обновление раз в
неделю делает workflow update-data: архив катается вперёд сам.
    python tools/build_weekly_review.py [--weeks 8]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_PATH = ROOT / "_mkdocs" / "data" / "weekly-review.json"

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

TOP_N = 3
ATR_DAYS = 14


def pip_size(pair: str) -> float:
    return 0.01 if pair.endswith("JPY") else 0.0001


def load_weeks(pair: str) -> dict[dt.date, list[dict]]:
    """Часовые свечи пары, сгруппированные по понедельникам ISO-недель."""
    path = DATA_DIR / f"{pair}_1h.csv"
    if not path.exists():
        sys.exit(f"❌ Нет котировок: {path}")
    weeks: dict[dt.date, list[dict]] = {}
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            moment = dt.datetime.fromisoformat(row["Datetime"])
            monday = moment.date() - dt.timedelta(days=moment.weekday())
            weeks.setdefault(monday, []).append(
                {
                    "t": moment.strftime("%Y-%m-%dT%H:%M"),
                    "o": float(row["open"]),
                    "h": float(row["high"]),
                    "l": float(row["low"]),
                    "c": float(row["close"]),
                }
            )
    return weeks


def last_complete_week(weeks: dict[dt.date, list[dict]]) -> dt.date:
    """Последний понедельник, у которого в данных ≥3 торговых дня недели."""
    candidates = []
    for monday, candles in weeks.items():
        days = {c["t"][:10] for c in candles}
        if len(days) >= 3:
            candidates.append(monday)
    if not candidates:
        sys.exit("❌ В данных нет ни одной полной недели")
    return max(candidates)


def daily_atr(candles: list[dict]) -> float:
    """ATR по дневным свечам за ATR_DAYS дней, в пипсах (сглаженная)."""
    by_day: dict[str, dict] = {}
    for candle in candles:
        day = candle["t"][:10]
        slot = by_day.setdefault(day, {"h": candle["h"], "l": candle["l"]})
        slot["h"] = max(slot["h"], candle["h"])
        slot["l"] = min(slot["l"], candle["l"])
    days = sorted(by_day)
    if len(days) < 2:
        return 0.0
    ranges = [by_day[d]["h"] - by_day[d]["l"] for d in days[-ATR_DAYS:]]
    return sum(ranges) / len(ranges)


def week_stats(pair: str, candles: list[dict], atr_price: float) -> dict:
    pip = pip_size(pair)
    open_ = candles[0]["o"]
    close = candles[-1]["c"]
    high = max(c["h"] for c in candles)
    low = min(c["l"] for c in candles)
    change_pips = (close - open_) / pip

    by_day: dict[str, list[dict]] = {}
    for candle in candles:
        by_day.setdefault(candle["t"][:10], []).append(candle)
    biggest_day = max(
        by_day.items(),
        key=lambda item: max(c["h"] for c in item[1]) - min(c["l"] for c in item[1]),
    )
    day_range = max(c["h"] for c in biggest_day[1]) - min(
        c["l"] for c in biggest_day[1]
    )

    atr_pips = atr_price / pip if pip else 0.0
    return {
        "pair": pair,
        "open": open_,
        "close": close,
        "high": high,
        "low": low,
        "change_pips": round(change_pips, 1),
        "change_pct": round((close - open_) / open_ * 100, 2),
        "atr_pips": round(atr_pips, 1),
        "move_in_atr": round(change_pips / atr_pips, 2) if atr_pips else None,
        "biggest_day": biggest_day[0],
        "biggest_day_range_pips": round(day_range / pip, 1),
        # Для мини-графика: часовые свечи, цена в пипсах от открытия недели.
        "candles": [
            [
                round((c["o"] - open_) / pip, 1),
                round((c["h"] - open_) / pip, 1),
                round((c["l"] - open_) / pip, 1),
                round((c["c"] - open_) / pip, 1),
            ]
            for c in candles
        ],
    }


def build_week(
    weeks_by_pair: dict[str, dict[dt.date, list[dict]]], week: dt.date
) -> dict:
    """Одна неделя: топ-N движений в ATR + остальные пары."""
    sunday = week + dt.timedelta(days=6)

    moves = []
    for pair, pair_weeks in weeks_by_pair.items():
        candles = pair_weeks.get(week, [])
        if not candles:
            continue
        history = [c for monday, cs in pair_weeks.items() if monday <= week for c in cs]
        atr_price = daily_atr(history)
        moves.append(week_stats(pair, candles, atr_price))

    moves.sort(key=lambda m: abs(m["move_in_atr"] or 0), reverse=True)
    return {
        "from": week.isoformat(),
        "to": sunday.isoformat(),
        "moves": moves[:TOP_N],
        "others": [
            {
                "pair": m["pair"],
                "change_pips": m["change_pips"],
                "move_in_atr": m["move_in_atr"],
            }
            for m in moves[TOP_N:]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--stamp", default=None, help="дата generated_at (YYYY-MM-DD)")
    parser.add_argument(
        "--weeks",
        type=int,
        default=8,
        help="сколько последних полных недель держать в архиве (виджет листает)",
    )
    args = parser.parse_args()

    weeks_by_pair = {pair: load_weeks(pair) for pair in PAIRS}
    latest = min(last_complete_week(weeks) for weeks in weeks_by_pair.values())
    # Архив идёт назад от последней общей полной недели: неделя попадает
    # в обзор, только если она есть у всех пар, — иначе сравнение нечестное.
    mondays = []
    cursor = latest
    while len(mondays) < args.weeks:
        if all(cursor in weeks for weeks in weeks_by_pair.values()):
            mondays.append(cursor)
        cursor -= dt.timedelta(days=7)
    if not mondays:
        sys.exit("❌ Ни одной общей полной недели у всех восьми пар")

    archive = [build_week(weeks_by_pair, monday) for monday in reversed(mondays)]

    document = {
        "meta": {
            "generated_at": args.stamp or dt.date.today().isoformat(),
            "source": "tools/build_weekly_review.py",
            "week": {"from": archive[-1]["from"], "to": archive[-1]["to"]},
            "weeks_count": len(archive),
        },
        "weeks": archive,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    for move in archive[-1]["moves"]:
        print(
            f"  {move['pair']}: {move['change_pips']:+.1f} пипсов "
            f"({move['move_in_atr']:+.2f} ATR), пик {move['biggest_day']}"
        )
    print(
        f"✅ {args.out}: архив {len(archive)} нед., последняя "
        f"{archive[-1]['from']} → {archive[-1]['to']}, топ-{TOP_N} из {len(PAIRS)} пар"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
