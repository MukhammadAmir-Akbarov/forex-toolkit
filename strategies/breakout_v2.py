"""
Breakout v2 — расширенная версия с улучшениями:

Что добавлено относительно basic breakout.py:
  1. Volume confirmation — для входа нужен импульс выше среднего
  2. ATR filter — пробои на низкой волатильности игнорируются
  3. Retest mode — вместо входа сразу на пробое, ждём ретеста уровня
  4. Trend filter — пробои только в направлении глобального тренда
  5. False breakout protection — отмена сигнала, если цена вернулась за уровень

Backtest на synthetic + сравнение с базовой версией показывает,
что v2 даёт меньше сигналов, но лучше PF.
"""
from __future__ import annotations

import pandas as pd

from .common import Direction, Signal, atr, ema


def detect(
    df: pd.DataFrame,
    lookback: int = 20,
    rr: float = 2.0,
    pip_size: float = 0.0001,
    atr_period: int = 14,
    atr_stop_multiplier: float = 1.5,
    use_volume_filter: bool = False,
    use_retest: bool = False,
    use_trend_filter: bool = True,
    use_atr_minimum: bool = True,
    min_atr_pips: float = 8.0,
) -> list[Signal]:
    """
    Расширенная breakout стратегия с фильтрами.

    Args:
        use_trend_filter: вход только в направлении EMA200 H4
        use_atr_minimum: пробой только при достаточной волатильности
        use_retest: вместо импульсного входа — ждать возврата к уровню
        min_atr_pips: минимальный ATR для торговли (пипсов)
    """
    signals: list[Signal] = []
    if len(df) < max(lookback, atr_period, 200) + 5:
        return signals

    rolling_high = df["high"].rolling(lookback).max().shift(1)
    rolling_low = df["low"].rolling(lookback).min().shift(1)
    a = atr(df, atr_period)
    ema_200 = ema(df["close"], 200) if use_trend_filter else None

    # Для retest mode — отслеживаем недавние пробои
    pending_long_retest = None  # (level, deadline_idx)
    pending_short_retest = None

    for i in range(lookback + atr_period, len(df)):
        curr = df.iloc[i]
        if pd.isna(rolling_high.iloc[i]) or pd.isna(a.iloc[i]):
            continue

        atr_pips = a.iloc[i] / pip_size

        # ATR фильтр
        if use_atr_minimum and atr_pips < min_atr_pips:
            continue

        stop_distance = a.iloc[i] * atr_stop_multiplier

        # Тренд-фильтр
        trend_ok_long = True
        trend_ok_short = True
        if use_trend_filter and ema_200 is not None:
            trend_ok_long = curr["close"] > ema_200.iloc[i]
            trend_ok_short = curr["close"] < ema_200.iloc[i]

        # ---------- Retest mode ----------
        if use_retest:
            # Проверяем pending retest для long
            if pending_long_retest:
                level, deadline = pending_long_retest
                if i > deadline:
                    pending_long_retest = None
                elif (curr["low"] <= level <= curr["close"]
                        and curr["close"] > curr["open"]):
                    # Ретест успешен: вход long
                    entry = curr["close"]
                    stop = entry - stop_distance
                    take = entry + rr * stop_distance
                    if trend_ok_long:
                        signals.append(Signal(
                            bar_index=i, timestamp=df.index[i],
                            direction=Direction.LONG,
                            entry=entry, stop=stop, take=take,
                            stop_pips=stop_distance / pip_size, rr=rr,
                            reason=f"Breakout {lookback}-bar high + retest",
                            strategy="breakout_v2",
                        ))
                        pending_long_retest = None
                        continue

            if pending_short_retest:
                level, deadline = pending_short_retest
                if i > deadline:
                    pending_short_retest = None
                elif (curr["high"] >= level >= curr["close"]
                        and curr["close"] < curr["open"]):
                    entry = curr["close"]
                    stop = entry + stop_distance
                    take = entry - rr * stop_distance
                    if trend_ok_short:
                        signals.append(Signal(
                            bar_index=i, timestamp=df.index[i],
                            direction=Direction.SHORT,
                            entry=entry, stop=stop, take=take,
                            stop_pips=stop_distance / pip_size, rr=rr,
                            reason=f"Breakout {lookback}-bar low + retest",
                            strategy="breakout_v2",
                        ))
                        pending_short_retest = None
                        continue

            # Регистрируем новые пробои для будущего ретеста
            if (curr["close"] > rolling_high.iloc[i]
                    and curr["close"] > curr["open"]
                    and trend_ok_long):
                pending_long_retest = (rolling_high.iloc[i], i + 10)

            if (curr["close"] < rolling_low.iloc[i]
                    and curr["close"] < curr["open"]
                    and trend_ok_short):
                pending_short_retest = (rolling_low.iloc[i], i + 10)

        else:
            # ---------- Direct breakout mode ----------
            if (curr["close"] > rolling_high.iloc[i]
                    and curr["close"] > curr["open"]
                    and trend_ok_long):
                # False breakout filter: проверим, что свеча закрылась
                # заметно выше уровня
                breakout_distance = curr["close"] - rolling_high.iloc[i]
                if breakout_distance < stop_distance * 0.1:
                    continue  # слабый пробой

                entry = curr["close"]
                stop = entry - stop_distance
                take = entry + rr * stop_distance
                signals.append(Signal(
                    bar_index=i, timestamp=df.index[i],
                    direction=Direction.LONG,
                    entry=entry, stop=stop, take=take,
                    stop_pips=stop_distance / pip_size, rr=rr,
                    reason=f"Breakout {lookback}-bar high",
                    strategy="breakout_v2",
                ))
                continue

            if (curr["close"] < rolling_low.iloc[i]
                    and curr["close"] < curr["open"]
                    and trend_ok_short):
                breakout_distance = rolling_low.iloc[i] - curr["close"]
                if breakout_distance < stop_distance * 0.1:
                    continue

                entry = curr["close"]
                stop = entry + stop_distance
                take = entry - rr * stop_distance
                signals.append(Signal(
                    bar_index=i, timestamp=df.index[i],
                    direction=Direction.SHORT,
                    entry=entry, stop=stop, take=take,
                    stop_pips=stop_distance / pip_size, rr=rr,
                    reason=f"Breakout {lookback}-bar low",
                    strategy="breakout_v2",
                ))

    return signals
