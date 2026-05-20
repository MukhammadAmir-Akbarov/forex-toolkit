"""
Breakout стратегия — пробой N-периодных хайлов/лоу.

Идея: цена пробила максимум за последние 20 свечей вверх с большим импульсом
→ вход long. Работает в трендовых рынках, на новостных импульсах.
"""
from __future__ import annotations

import pandas as pd

from .common import Direction, Signal, atr


def detect(
    df: pd.DataFrame,
    lookback: int = 20,
    rr: float = 2.0,
    pip_size: float = 0.0001,
    atr_period: int = 14,
    atr_stop_multiplier: float = 1.5,
) -> list[Signal]:
    """
    Long: close > max(high) за последние lookback свечей
    Short: close < min(low) за lookback свечей
    Стоп: ATR × multiplier (волатильностный стоп)
    """
    signals: list[Signal] = []
    if len(df) < max(lookback, atr_period) + 5:
        return signals

    rolling_high = df["high"].rolling(lookback).max().shift(1)
    rolling_low = df["low"].rolling(lookback).min().shift(1)
    a = atr(df, atr_period)

    for i in range(lookback + atr_period, len(df)):
        curr = df.iloc[i]
        if pd.isna(rolling_high.iloc[i]) or pd.isna(a.iloc[i]):
            continue

        stop_distance = a.iloc[i] * atr_stop_multiplier

        # LONG: пробой вверх
        if curr["close"] > rolling_high.iloc[i] and curr["close"] > curr["open"]:
            entry = curr["close"]
            stop = entry - stop_distance
            take = entry + rr * stop_distance
            signals.append(Signal(
                bar_index=i, timestamp=df.index[i],
                direction=Direction.LONG,
                entry=entry, stop=stop, take=take,
                stop_pips=stop_distance / pip_size, rr=rr,
                reason=f"Breakout {lookback}-bar high",
                strategy="breakout",
            ))
            continue

        # SHORT: пробой вниз
        if curr["close"] < rolling_low.iloc[i] and curr["close"] < curr["open"]:
            entry = curr["close"]
            stop = entry + stop_distance
            take = entry - rr * stop_distance
            signals.append(Signal(
                bar_index=i, timestamp=df.index[i],
                direction=Direction.SHORT,
                entry=entry, stop=stop, take=take,
                stop_pips=stop_distance / pip_size, rr=rr,
                reason=f"Breakout {lookback}-bar low",
                strategy="breakout",
            ))

    return signals
