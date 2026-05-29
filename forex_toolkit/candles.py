"""Свечные паттерны."""

from __future__ import annotations

import pandas as pd


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


def is_hammer(row: pd.Series) -> bool:
    """Молот: длинная нижняя тень + маленькое тело сверху."""
    b = body(row)
    if b == 0:
        return False
    return lower_shadow(row) >= 2 * b and upper_shadow(row) < b


def is_shooting_star(row: pd.Series) -> bool:
    """Падающая звезда: длинная верхняя тень."""
    b = body(row)
    if b == 0:
        return False
    return upper_shadow(row) >= 2 * b and lower_shadow(row) < b


def is_bullish_engulfing(prev: pd.Series, curr: pd.Series) -> bool:
    """Бычье поглощение: красная → зелёная, накрывающая."""
    return bool(
        is_bearish(prev)
        and is_bullish(curr)
        and curr["close"] > prev["open"]
        and curr["open"] < prev["close"]
        and body(curr) > body(prev)
    )


def is_bearish_engulfing(prev: pd.Series, curr: pd.Series) -> bool:
    """Медвежье поглощение."""
    return bool(
        is_bullish(prev)
        and is_bearish(curr)
        and curr["close"] < prev["open"]
        and curr["open"] > prev["close"]
        and body(curr) > body(prev)
    )


def is_doji(row: pd.Series, threshold: float = 0.1) -> bool:
    """Доджи: тело меньше threshold от размера свечи."""
    candle_range = row["high"] - row["low"]
    if candle_range == 0:
        return False
    return body(row) / candle_range < threshold
