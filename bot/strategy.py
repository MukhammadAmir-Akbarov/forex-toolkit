"""
Стратегия «Откат к EMA50 по тренду» — детектор сигналов.

Реализация правил из docs/strategy-details.md в виде функций:
  - расчёт индикаторов (EMA, RSI)
  - детекция сетапов на каждой свече
  - правила входа / выхода

Используется бэктестером (backtest.py).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
import pandas as pd


class Direction(str, Enum):
    LONG = "long"
    SHORT = "short"


@dataclass
class Signal:
    bar_index: int
    timestamp: pd.Timestamp
    direction: Direction
    entry: float
    stop: float
    take: float
    stop_pips: float
    rr: float
    reason: str


# ---------- Индикаторы ----------

def ema(series: pd.Series, period: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index по стандартной формуле Wilder."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50)


# ---------- Свечные паттерны ----------

def is_bullish_engulfing(prev: pd.Series, curr: pd.Series) -> bool:
    """Бычье поглощение: красная свеча, потом большая зелёная,
    тело которой накрывает тело предыдущей."""
    prev_body = prev["close"] - prev["open"]
    curr_body = curr["close"] - curr["open"]
    return bool(
        prev_body < 0
        and curr_body > 0
        and curr["close"] > prev["open"]
        and curr["open"] < prev["close"]
        and abs(curr_body) > abs(prev_body)
    )


def is_bearish_engulfing(prev: pd.Series, curr: pd.Series) -> bool:
    prev_body = prev["close"] - prev["open"]
    curr_body = curr["close"] - curr["open"]
    return bool(
        prev_body > 0
        and curr_body < 0
        and curr["close"] < prev["open"]
        and curr["open"] > prev["close"]
        and abs(curr_body) > abs(prev_body)
    )


def is_hammer(curr: pd.Series) -> bool:
    """Молот: маленькое тело сверху, длинная нижняя тень (≥ 2× тела)."""
    body = abs(curr["close"] - curr["open"])
    if body == 0:
        return False
    lower_shadow = min(curr["open"], curr["close"]) - curr["low"]
    upper_shadow = curr["high"] - max(curr["open"], curr["close"])
    return bool(lower_shadow >= 2 * body and upper_shadow < body)


def is_shooting_star(curr: pd.Series) -> bool:
    body = abs(curr["close"] - curr["open"])
    if body == 0:
        return False
    upper_shadow = curr["high"] - max(curr["open"], curr["close"])
    lower_shadow = min(curr["open"], curr["close"]) - curr["low"]
    return bool(upper_shadow >= 2 * body and lower_shadow < body)


# ---------- Логика сетапа ----------

def detect_signals(
    df: pd.DataFrame,
    rr: float = 2.0,
    stop_buffer_pips: float = 5.0,
    pip_size: float = 0.0001,
    ema_distance_pips: float = 10.0,
    rsi_long_range: tuple[float, float] = (40, 65),
    rsi_short_range: tuple[float, float] = (35, 60),
) -> list[Signal]:
    """
    Сканирует OHLC-серию (H1) и возвращает список сигналов.

    df должен содержать колонки: open, high, low, close, ema50, ema200, rsi.
    Индекс — DatetimeIndex.

    Условия long (зеркально для short):
      1. close > ema200 (тренд H4 имитируем через EMA200 на текущем TF)
      2. low or open в пределах ema_distance_pips от ema50
      3. бычий паттерн (молот / поглощение) на текущей свече
      4. RSI в зоне rsi_long_range
    """
    signals: list[Signal] = []
    if len(df) < 210:
        return signals  # недостаточно для EMA200

    for i in range(1, len(df)):
        curr = df.iloc[i]
        prev = df.iloc[i - 1]

        if pd.isna(curr.ema200) or pd.isna(curr.ema50):
            continue

        dist_to_ema50 = abs(curr["close"] - curr["ema50"]) / pip_size

        # ---------- LONG ----------
        trend_up = curr["close"] > curr["ema200"]
        rsi_ok_long = rsi_long_range[0] <= curr["rsi"] <= rsi_long_range[1]
        near_ema = dist_to_ema50 <= ema_distance_pips
        pulled_back = curr["low"] <= curr["ema50"] * 1.0005
        pattern_long = is_hammer(curr) or is_bullish_engulfing(prev, curr)

        if trend_up and near_ema and pulled_back and rsi_ok_long and pattern_long:
            stop = curr["low"] - stop_buffer_pips * pip_size
            entry = curr["close"]
            risk = entry - stop
            if risk <= 0:
                continue
            take = entry + rr * risk
            reason = "Hammer" if is_hammer(curr) else "BullEng"
            signals.append(Signal(
                bar_index=i,
                timestamp=df.index[i],
                direction=Direction.LONG,
                entry=entry,
                stop=stop,
                take=take,
                stop_pips=risk / pip_size,
                rr=rr,
                reason=reason,
            ))
            continue

        # ---------- SHORT ----------
        trend_dn = curr["close"] < curr["ema200"]
        rsi_ok_short = rsi_short_range[0] <= curr["rsi"] <= rsi_short_range[1]
        pulled_up = curr["high"] >= curr["ema50"] * 0.9995
        pattern_short = is_shooting_star(curr) or is_bearish_engulfing(prev, curr)

        if trend_dn and near_ema and pulled_up and rsi_ok_short and pattern_short:
            stop = curr["high"] + stop_buffer_pips * pip_size
            entry = curr["close"]
            risk = stop - entry
            if risk <= 0:
                continue
            take = entry - rr * risk
            reason = "ShootStar" if is_shooting_star(curr) else "BearEng"
            signals.append(Signal(
                bar_index=i,
                timestamp=df.index[i],
                direction=Direction.SHORT,
                entry=entry,
                stop=stop,
                take=take,
                stop_pips=risk / pip_size,
                rr=rr,
                reason=reason,
            ))

    return signals


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Добавляет EMA50, EMA200, RSI к OHLC-данным."""
    df = df.copy()
    df["ema50"] = ema(df["close"], 50)
    df["ema200"] = ema(df["close"], 200)
    df["rsi"] = rsi(df["close"], 14)
    return df
