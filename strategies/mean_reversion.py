"""
Mean Reversion стратегия — возврат к среднему через Bollinger Bands.

Идея: цена касается верхней/нижней полосы Боллинджера → ожидаем
возврата к средней. Работает в БОКОВИКАХ.
"""
from __future__ import annotations

import pandas as pd

from .common import Direction, Signal, bollinger, rsi


def detect(
    df: pd.DataFrame,
    rr: float = 1.5,
    pip_size: float = 0.0001,
    stop_buffer_pips: float = 5,
) -> list[Signal]:
    """
    Long: цена касается нижней полосы + RSI < 30 + бычья свеча
    Short: цена касается верхней полосы + RSI > 70 + медвежья свеча
    """
    signals: list[Signal] = []
    if len(df) < 30:
        return signals

    upper, middle, lower = bollinger(df["close"], 20, 2.0)
    r = rsi(df["close"], 14)

    for i in range(1, len(df)):
        if pd.isna(upper.iloc[i]) or pd.isna(lower.iloc[i]):
            continue
        curr = df.iloc[i]
        prev = df.iloc[i - 1]

        # LONG: коснулась нижней + RSI перепродан + бычья свеча
        touched_lower = curr["low"] <= lower.iloc[i]
        rsi_oversold = r.iloc[i] < 35
        bullish = curr["close"] > curr["open"]
        if touched_lower and rsi_oversold and bullish:
            stop = curr["low"] - stop_buffer_pips * pip_size
            entry = curr["close"]
            risk = entry - stop
            if risk <= 0:
                continue
            take = entry + rr * risk
            signals.append(Signal(
                bar_index=i, timestamp=df.index[i],
                direction=Direction.LONG,
                entry=entry, stop=stop, take=take,
                stop_pips=risk / pip_size, rr=rr,
                reason="BB-lower + RSI oversold",
                strategy="mean_reversion",
            ))
            continue

        # SHORT
        touched_upper = curr["high"] >= upper.iloc[i]
        rsi_overbought = r.iloc[i] > 65
        bearish = curr["close"] < curr["open"]
        if touched_upper and rsi_overbought and bearish:
            stop = curr["high"] + stop_buffer_pips * pip_size
            entry = curr["close"]
            risk = stop - entry
            if risk <= 0:
                continue
            take = entry - rr * risk
            signals.append(Signal(
                bar_index=i, timestamp=df.index[i],
                direction=Direction.SHORT,
                entry=entry, stop=stop, take=take,
                stop_pips=risk / pip_size, rr=rr,
                reason="BB-upper + RSI overbought",
                strategy="mean_reversion",
            ))

    return signals
