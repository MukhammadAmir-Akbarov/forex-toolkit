#!/usr/bin/env python3
"""Скачивает котировки в data/ — единственный источник свежих данных сайта.

Все витрины (Replay, теплокарта, «Неделя на рынке», рейтинг стратегий)
пересчитываются из data/<PAIR>_<TF>.csv. Раньше эти файлы появлялись
«однажды» и не обновлялись: команда упоминалась в документации, но самого
скрипта не было. Теперь есть:

    python tools/fetch_quotes.py                 # все 8 пар, 1h + 1d
    python tools/fetch_quotes.py --pair EURUSD --timeframe 1h

Источник — yfinance (символы вида EURUSD=X). Ограничения источника честно
отражены в стратегии скачивания:

* часовой таймфрейм отдают максимум за ~730 дней → качаем ``729d``;
* дневной — за всю историю (``max``), сезонность любит длинные ряды.

Слияние с уже лежащими CSV — по ключу времени: строки с совпадающим
таймстампом перезаписываются свежими, остальные сохраняются. Поэтому локальный
архив с длинной историей не схлопывается до «последних двух лет», а каталог
data/ в гит не коммитится: CI скачивает всё с нуля за один прогон.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

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

# (таймфрейм, период запроса, имя колонки времени) — колонка времени различается
# по историческим причинам: часовые файлы начинаются с Datetime, дневные с Date.
TIMEFRAMES = {
    "1h": {"period": "729d", "time_column": "Datetime"},
    "1d": {"period": "max", "time_column": "Date"},
}

COLUMNS = ["open", "high", "low", "close"]


def merge_rows(existing: list[dict], fresh: list[dict], key: str) -> list[dict]:
    """Склеивает старые и новые строки по ключу времени.

    Свежая строка с уже известным таймстампом перезаписывает старую (источник
    иногда правит последнюю свечу задним числом), остальное сохраняется как
    есть. Результат отсортирован по времени — гарантия порядка, даже если
    источник прислал куски не по порядку.
    """
    merged = {row[key]: row for row in existing}
    for row in fresh:
        merged[row[key]] = row
    return [merged[stamp] for stamp in sorted(merged)]


def normalize_frame(frame, time_column: str) -> list[dict]:
    """Приводит DataFrame yfinance к строкам CSV схемы data/*.csv.

    Принимает и плоские колонки (Open/High/Low/Close), и двухэтажные
    (('Close', 'EURUSD=X') — так отвечает свежий yfinance даже на один тикер).
    Свечи без цены (выходные дыры, неполные запросы) выбрасываются.
    """
    columns = frame.columns
    if hasattr(columns, "nlevels") and columns.nlevels > 1:
        frame = frame.droplevel(1, axis=1)
    frame = frame.rename(columns=str.lower)

    rows = []
    for stamp, candle in frame.iterrows():
        values = [candle.get(col) for col in COLUMNS]
        if any(value != value for value in values):  # NaN != NaN
            continue
        rows.append(
            {
                time_column: stamp.isoformat(sep=" "),
                **{col: repr(float(candle[col])) for col in COLUMNS},
            }
        )
    return rows


def read_csv_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, rows: list[dict], time_column: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[time_column, *COLUMNS])
        writer.writeheader()
        writer.writerows(rows)


def fetch_pair(pair: str, timeframe: str, data_dir: Path = DATA_DIR) -> tuple[int, int]:
    """Скачивает одну пару/таймфрейм, сливает с архивом. Возвращает (было, стало)."""
    import yfinance as yf  # noqa: WPS433 — сеть нужна только этой команде

    spec = TIMEFRAMES[timeframe]
    frame = yf.download(
        f"{pair}=X",
        period=spec["period"],
        interval=timeframe,
        auto_adjust=False,
        progress=False,
    )
    if frame.empty:
        raise RuntimeError(f"источник вернул пустой ответ для {pair} {timeframe}")

    # Всё приводим к UTC: старые архивы были в +01:00, читатели понимают
    # любой сдвиг через fromisoformat, а единый пояс упрощает слияние.
    if frame.index.tz is not None:
        frame = frame.tz_convert("UTC")

    fresh = normalize_frame(frame, spec["time_column"])
    path = data_dir / f"{pair}_{timeframe}.csv"
    existing = read_csv_rows(path)
    merged = merge_rows(existing, fresh, spec["time_column"])
    write_csv_rows(path, merged, spec["time_column"])
    return len(existing), len(merged)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pair", choices=PAIRS, help="одна пара вместо всех восьми")
    parser.add_argument(
        "--timeframe", choices=sorted(TIMEFRAMES), help="один таймфрейм вместо обоих"
    )
    args = parser.parse_args()

    pairs = [args.pair] if args.pair else PAIRS
    timeframes = [args.timeframe] if args.timeframe else sorted(TIMEFRAMES)

    failures = 0
    for pair in pairs:
        for timeframe in timeframes:
            try:
                before, after = fetch_pair(pair, timeframe)
            except Exception as error:  # noqa: BLE001 — одна пара не роняет остальные
                print(f"❌ {pair} {timeframe}: {error}")
                failures += 1
                continue
            print(f"✅ {pair} {timeframe}: {before} → {after} свечей")

    if failures:
        print(f"\n❌ Не скачались: {failures}.")
        return 1
    print(
        "\n✅ Котировки обновлены. Пересобери витрины: tools/rebuild_showcase_data.py"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
