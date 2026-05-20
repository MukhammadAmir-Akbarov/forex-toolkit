"""
London Open Range стратегия.

Идея: определяем диапазон первого часа лондонской сессии (10:00-11:00 UTC).
Пробой этого диапазона = сигнал на вход в направлении пробоя.
"""
from __future__ import annotations

import pandas as pd

from .common import Direction, Signal


def detect(
    df: pd.DataFrame,
    range_start_hour: int = 10,  # UTC
    range_end_hour: int = 11,
    rr: float = 2.0,
    pip_size: float = 0.0001,
) -> list[Signal]:
    """
    Каждый торговый день:
      1. Находим high/low первого часа Лондона
      2. Пробой high → long, пробой low → short
      3. Один сигнал в день
    """
    signals: list[Signal] = []
    if not isinstance(df.index, pd.DatetimeIndex):
        return signals
    if len(df) < 50:
        return signals

    # Группируем по дням
    df_local = df.copy()
    df_local["date"] = df_local.index.date
    df_local["hour"] = df_local.index.hour

    for date, day_df in df_local.groupby("date"):
        # Свечи в диапазоне начального часа
        range_bars = day_df[
            (day_df["hour"] >= range_start_hour)
            & (day_df["hour"] < range_end_hour)
        ]
        if len(range_bars) == 0:
            continue
        rng_high = range_bars["high"].max()
        rng_low = range_bars["low"].min()

        # Дальнейшие свечи дня — ищем пробой
        post_bars = day_df[day_df["hour"] >= range_end_hour]
        signaled = False
        for ts, bar in post_bars.iterrows():
            if signaled:
                break
            i = df.index.get_loc(ts)
            risk = (rng_high - rng_low)
            if risk <= 0:
                break
            if bar["close"] > rng_high:
                entry = bar["close"]
                stop = rng_low
                take = entry + rr * (entry - stop)
                signals.append(Signal(
                    bar_index=i, timestamp=ts,
                    direction=Direction.LONG,
                    entry=entry, stop=stop, take=take,
                    stop_pips=(entry - stop) / pip_size, rr=rr,
                    reason="London range breakout up",
                    strategy="london_open",
                ))
                signaled = True
            elif bar["close"] < rng_low:
                entry = bar["close"]
                stop = rng_high
                take = entry - rr * (stop - entry)
                signals.append(Signal(
                    bar_index=i, timestamp=ts,
                    direction=Direction.SHORT,
                    entry=entry, stop=stop, take=take,
                    stop_pips=(stop - entry) / pip_size, rr=rr,
                    reason="London range breakout down",
                    strategy="london_open",
                ))
                signaled = True

    return signals
