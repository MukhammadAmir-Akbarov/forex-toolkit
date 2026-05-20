"""
Three Soldiers / Three Crows стратегия.

Идея: три подряд бычьих свечи с растущими телами и закрытиями = сильный
импульс вверх. Входим long на 4-й свече с целью продолжения движения.
"""
from __future__ import annotations

import pandas as pd

from .common import Direction, Signal


def detect(
    df: pd.DataFrame,
    rr: float = 1.5,
    pip_size: float = 0.0001,
    stop_buffer_pips: float = 5,
) -> list[Signal]:
    signals: list[Signal] = []
    if len(df) < 5:
        return signals

    for i in range(3, len(df)):
        a = df.iloc[i - 3]
        b = df.iloc[i - 2]
        c = df.iloc[i - 1]
        d = df.iloc[i]

        # LONG: 3 бычьих с растущими closes, тело растёт
        body_a = a["close"] - a["open"]
        body_b = b["close"] - b["open"]
        body_c = c["close"] - c["open"]
        if (body_a > 0 and body_b > 0 and body_c > 0
                and c["close"] > b["close"] > a["close"]
                and body_b > body_a * 0.5
                and body_c > body_b * 0.5):
            entry = d["open"] if d["open"] > c["close"] else c["close"]
            stop = a["low"] - stop_buffer_pips * pip_size
            risk = entry - stop
            if risk <= 0:
                continue
            take = entry + rr * risk
            signals.append(Signal(
                bar_index=i, timestamp=df.index[i],
                direction=Direction.LONG,
                entry=entry, stop=stop, take=take,
                stop_pips=risk / pip_size, rr=rr,
                reason="Three White Soldiers",
                strategy="three_soldiers",
            ))
            continue

        # SHORT: Three Black Crows
        body_a = a["open"] - a["close"]
        body_b = b["open"] - b["close"]
        body_c = c["open"] - c["close"]
        if (body_a > 0 and body_b > 0 and body_c > 0
                and c["close"] < b["close"] < a["close"]
                and body_b > body_a * 0.5
                and body_c > body_b * 0.5):
            entry = d["open"] if d["open"] < c["close"] else c["close"]
            stop = a["high"] + stop_buffer_pips * pip_size
            risk = stop - entry
            if risk <= 0:
                continue
            take = entry - rr * risk
            signals.append(Signal(
                bar_index=i, timestamp=df.index[i],
                direction=Direction.SHORT,
                entry=entry, stop=stop, take=take,
                stop_pips=risk / pip_size, rr=rr,
                reason="Three Black Crows",
                strategy="three_soldiers",
            ))

    return signals
