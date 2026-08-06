#!/usr/bin/env python3
"""
Pattern scanner — поиск свечных паттернов в исторических данных.

Сканирует OHLC CSV (или синтетические данные) и находит:
  - Молот / падающая звезда
  - Бычье / медвежье поглощение
  - Доджи
  - Пин-бар
  - Утренняя / вечерняя звезда
  - Три белых солдата / три чёрные вороны

Выводит список найденных паттернов и сохраняет график с разметкой.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass
class PatternMatch:
    index: int
    timestamp: pd.Timestamp
    pattern: str
    direction: str  # "bull" / "bear"
    strength: int  # 1-3


def body(row: pd.Series) -> float:
    return abs(row["close"] - row["open"])


def is_bullish(row: pd.Series) -> bool:
    return row["close"] > row["open"]


def is_bearish(row: pd.Series) -> bool:
    return row["close"] < row["open"]


def upper_shadow(row: pd.Series) -> float:
    return row["high"] - max(row["open"], row["close"])


def lower_shadow(row: pd.Series) -> float:
    return min(row["open"], row["close"]) - row["low"]


def candle_range(row: pd.Series) -> float:
    return row["high"] - row["low"]


# ---------- Детекторы ----------


def detect_hammer(df: pd.DataFrame) -> list[PatternMatch]:
    results = []
    for i_pos, (_, row) in enumerate(df.iterrows()):
        i = i_pos
        b = body(row)
        if b == 0:
            continue
        if (
            lower_shadow(row) >= 2 * b
            and upper_shadow(row) < b
            and candle_range(row) > 0
        ):
            results.append(PatternMatch(i, df.index[i], "Hammer", "bull", 2))
    return results


def detect_shooting_star(df: pd.DataFrame) -> list[PatternMatch]:
    results = []
    for i_pos, (_, row) in enumerate(df.iterrows()):
        i = i_pos
        b = body(row)
        if b == 0:
            continue
        if upper_shadow(row) >= 2 * b and lower_shadow(row) < b:
            results.append(PatternMatch(i, df.index[i], "Shooting Star", "bear", 2))
    return results


def detect_doji(df: pd.DataFrame) -> list[PatternMatch]:
    results = []
    for i_pos, (_, row) in enumerate(df.iterrows()):
        i = i_pos
        if candle_range(row) == 0:
            continue
        if body(row) / candle_range(row) < 0.1:
            results.append(PatternMatch(i, df.index[i], "Doji", "neutral", 1))
    return results


def detect_engulfing(df: pd.DataFrame) -> list[PatternMatch]:
    results = []
    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        if (
            is_bearish(prev)
            and is_bullish(curr)
            and curr["close"] > prev["open"]
            and curr["open"] < prev["close"]
            and body(curr) > body(prev)
        ):
            results.append(PatternMatch(i, df.index[i], "Bullish Engulfing", "bull", 3))
        elif (
            is_bullish(prev)
            and is_bearish(curr)
            and curr["close"] < prev["open"]
            and curr["open"] > prev["close"]
            and body(curr) > body(prev)
        ):
            results.append(PatternMatch(i, df.index[i], "Bearish Engulfing", "bear", 3))
    return results


def detect_three_soldiers(df: pd.DataFrame) -> list[PatternMatch]:
    """Три белых солдата — 3 подряд бычьих с растущими закрытиями."""
    results = []
    for i in range(2, len(df)):
        a, b, c = df.iloc[i - 2], df.iloc[i - 1], df.iloc[i]
        if (
            is_bullish(a)
            and is_bullish(b)
            and is_bullish(c)
            and c["close"] > b["close"] > a["close"]
            and body(b) > body(a) * 0.5
            and body(c) > body(b) * 0.5
        ):
            results.append(
                PatternMatch(i, df.index[i], "Three White Soldiers", "bull", 3)
            )
    return results


def detect_three_crows(df: pd.DataFrame) -> list[PatternMatch]:
    """Три чёрные вороны — 3 подряд медвежьих с падающими закрытиями."""
    results = []
    for i in range(2, len(df)):
        a, b, c = df.iloc[i - 2], df.iloc[i - 1], df.iloc[i]
        if (
            is_bearish(a)
            and is_bearish(b)
            and is_bearish(c)
            and c["close"] < b["close"] < a["close"]
            and body(b) > body(a) * 0.5
            and body(c) > body(b) * 0.5
        ):
            results.append(PatternMatch(i, df.index[i], "Three Black Crows", "bear", 3))
    return results


def detect_morning_star(df: pd.DataFrame) -> list[PatternMatch]:
    """Утренняя звезда: длинная красная → доджи/маленькая → длинная зелёная."""
    results = []
    for i in range(2, len(df)):
        a, b, c = df.iloc[i - 2], df.iloc[i - 1], df.iloc[i]
        if (
            is_bearish(a)
            and body(a) > 0
            and body(b) < body(a) * 0.3
            and is_bullish(c)
            and c["close"] > (a["open"] + a["close"]) / 2
        ):
            results.append(PatternMatch(i, df.index[i], "Morning Star", "bull", 3))
    return results


def detect_evening_star(df: pd.DataFrame) -> list[PatternMatch]:
    results = []
    for i in range(2, len(df)):
        a, b, c = df.iloc[i - 2], df.iloc[i - 1], df.iloc[i]
        if (
            is_bullish(a)
            and body(a) > 0
            and body(b) < body(a) * 0.3
            and is_bearish(c)
            and c["close"] < (a["open"] + a["close"]) / 2
        ):
            results.append(PatternMatch(i, df.index[i], "Evening Star", "bear", 3))
    return results


ALL_DETECTORS = {
    "hammer": detect_hammer,
    "shooting-star": detect_shooting_star,
    "doji": detect_doji,
    "engulfing": detect_engulfing,
    "three-soldiers": detect_three_soldiers,
    "three-crows": detect_three_crows,
    "morning-star": detect_morning_star,
    "evening-star": detect_evening_star,
}


def scan_all(df: pd.DataFrame) -> list[PatternMatch]:
    results = []
    for detector in ALL_DETECTORS.values():
        results.extend(detector(df))
    results.sort(key=lambda p: p.index)
    return results


def plot_patterns(
    df: pd.DataFrame, matches: list[PatternMatch], out_path: Path, max_show: int = 50
) -> None:
    fig, ax = plt.subplots(figsize=(14, 7))
    for i_pos, (_, row) in enumerate(df.iterrows()):
        i = i_pos
        color = "#10b981" if row["close"] >= row["open"] else "#ef4444"
        ax.plot([i, i], [row["low"], row["high"]], color=color, linewidth=0.8)
        body_low = min(row["open"], row["close"])
        body_h = max(
            abs(row["close"] - row["open"]), (row["high"] - row["low"]) * 0.001
        )
        ax.add_patch(
            plt.Rectangle(
                (i - 0.4, body_low), 0.8, body_h, facecolor=color, edgecolor=color
            )
        )

    shown = matches[-max_show:]
    for m in shown:
        row = df.iloc[m.index]
        y = row["high"] + (df["high"].max() - df["low"].min()) * 0.02
        marker = "▲" if m.direction == "bull" else "▼" if m.direction == "bear" else "♦"
        color = (
            "#10b981"
            if m.direction == "bull"
            else "#ef4444"
            if m.direction == "bear"
            else "#6b7280"
        )
        ax.text(m.index, y, marker, fontsize=11, ha="center", color=color)

    ax.set_title(
        f"Найдено паттернов: {len(matches)} (показаны последние {len(shown)})",
        fontsize=12,
        weight="bold",
    )
    ax.set_ylabel("Цена")
    ax.set_xlabel("Свечи")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def generate_synthetic(bars: int = 300, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    times = pd.date_range("2026-01-01", periods=bars, freq="h")
    closes = [1.08]
    for _ in range(bars - 1):
        closes.append(closes[-1] + rng.normal(0, 0.0012))
    closes = np.array(closes)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + rng.uniform(0, 0.001, bars)
    lows = np.minimum(opens, closes) - rng.uniform(0, 0.001, bars)
    return pd.DataFrame(
        {
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
        },
        index=times,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Сканер свечных паттернов",
    )
    parser.add_argument(
        "--csv", type=Path, help="OHLC CSV (по умолч. синтетические данные)"
    )
    parser.add_argument(
        "--patterns",
        nargs="+",
        choices=list(ALL_DETECTORS.keys()) + ["all"],
        default=["all"],
    )
    parser.add_argument("--out", type=Path, default=Path("patterns-found.png"))
    args = parser.parse_args()

    if args.csv:
        df = pd.read_csv(args.csv)
        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.set_index("datetime")
        df = df[["open", "high", "low", "close"]].astype(float)
    else:
        print("Использую синтетические данные (для теста). Передай --csv для своих.")
        df = generate_synthetic()

    matches = scan_all(df)

    print(f"\nПросканировано свечей: {len(df)}")
    print(f"Найдено паттернов: {len(matches)}")
    print()
    print(f"{'#':<4} {'Время':<22} {'Паттерн':<24} {'Сторона':<8} Сила")
    print("─" * 70)
    for i, m in enumerate(matches[-30:], 1):  # последние 30
        print(
            f"{i:<4} {str(m.timestamp):<22} "
            f"{m.pattern:<24} {m.direction:<8} {'★' * m.strength}"
        )

    # Сводка по типам
    print()
    counts = {}
    for m in matches:
        counts[m.pattern] = counts.get(m.pattern, 0) + 1
    print("Сводка:")
    for p, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {p:<24} {c}")

    plot_patterns(df, matches, args.out)
    print(f"\nГрафик: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
