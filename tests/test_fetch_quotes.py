"""Слияние и нормализация котировок в fetch_quotes — без сети.

Сеть в тестах не нужна: проверяем две чистые функции, от которых зависит
целостность архива data/:

* merge_rows — склейка старого архива со свежей порцией без дублей и дыр
  в сортировке;
* normalize_frame — приведение ответа yfinance (включая двухэтажные колонки
  и NaN-свечи выходных) к схеме CSV.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from fetch_quotes import merge_rows, normalize_frame  # noqa: E402


def _row(stamp: str, close: float = 1.0) -> dict:
    return {
        "Datetime": stamp,
        "open": "1",
        "high": "1",
        "low": "1",
        "close": repr(close),
    }


def test_merge_appends_new_rows_in_order():
    existing = [_row("2026-05-18 00:00:00+00:00"), _row("2026-05-19 00:00:00+00:00")]
    fresh = [_row("2026-05-20 00:00:00+00:00")]

    merged = merge_rows(existing, fresh, "Datetime")

    assert [r["Datetime"] for r in merged] == [
        "2026-05-18 00:00:00+00:00",
        "2026-05-19 00:00:00+00:00",
        "2026-05-20 00:00:00+00:00",
    ]


def test_merge_overwrites_same_timestamp_with_fresh_value():
    """Источник иногда правит последнюю свечу задним числом — свежее важнее."""
    existing = [_row("2026-05-19 00:00:00+00:00", close=1.10)]
    fresh = [_row("2026-05-19 00:00:00+00:00", close=1.11)]

    merged = merge_rows(existing, fresh, "Datetime")

    assert len(merged) == 1
    assert merged[0]["close"] == repr(1.11)


def test_merge_sorts_even_if_source_sent_chunks_out_of_order():
    existing = [_row("2026-05-20 00:00:00+00:00")]
    fresh = [_row("2026-05-18 00:00:00+00:00"), _row("2026-05-19 00:00:00+00:00")]

    merged = merge_rows(existing, fresh, "Datetime")

    assert [r["Datetime"][:10] for r in merged] == [
        "2026-05-18",
        "2026-05-19",
        "2026-05-20",
    ]


def test_normalize_flat_columns_drops_nan_candles():
    frame = pd.DataFrame(
        {
            "Open": [1.0, None],
            "High": [1.1, 1.1],
            "Low": [0.9, 0.9],
            "Close": [1.05, None],
        },
        index=pd.DatetimeIndex(["2026-05-18", "2026-05-19"], tz="UTC"),
    )

    rows = normalize_frame(frame, "Datetime")

    assert len(rows) == 1
    assert rows[0]["Datetime"].startswith("2026-05-18")
    assert rows[0]["close"] == repr(1.05)


def test_normalize_handles_multiindex_columns():
    columns = pd.MultiIndex.from_tuples(
        [
            ("Close", "EURUSD=X"),
            ("High", "EURUSD=X"),
            ("Low", "EURUSD=X"),
            ("Open", "EURUSD=X"),
        ]
    )
    frame = pd.DataFrame(
        [[1.05, 1.1, 0.9, 1.0]],
        columns=columns,
        index=pd.DatetimeIndex(["2026-05-18"], tz="UTC"),
    )

    rows = normalize_frame(frame, "Date")

    assert rows == [
        {
            "Date": "2026-05-18 00:00:00+00:00",
            "open": repr(1.0),
            "high": repr(1.1),
            "low": repr(0.9),
            "close": repr(1.05),
        }
    ]
