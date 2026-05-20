#!/usr/bin/env python3
"""
Сравнительный бэктестер всех стратегий.

Прогоняет каждую стратегию на одних и тех же данных,
выводит сводную таблицу метрик и сравнительный график equity curves.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Pure relative imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strategies import (  # noqa: E402
    breakout, london_open, mean_reversion, three_soldiers,
)
from strategies.common import Direction, Signal, ema, rsi  # noqa: E402


@dataclass
class Trade:
    strategy: str
    entry_idx: int
    exit_idx: int
    direction: str
    entry: float
    stop: float
    take: float
    exit_price: float
    outcome: str
    pnl_r: float


def simulate(df: pd.DataFrame, signals: list[Signal],
             max_bars: int = 30) -> list[Trade]:
    trades = []
    busy_until = -1
    for s in signals:
        if s.bar_index <= busy_until:
            continue
        risk = abs(s.entry - s.stop)
        if risk == 0:
            continue
        end = min(s.bar_index + max_bars, len(df) - 1)
        exit_idx = end
        exit_price = df.iloc[end]["close"]
        outcome = "timeout"

        for j in range(s.bar_index + 1, end + 1):
            high, low = df.iloc[j]["high"], df.iloc[j]["low"]
            if s.direction == Direction.LONG:
                if low <= s.stop:
                    exit_idx, exit_price, outcome = j, s.stop, "loss"
                    break
                if high >= s.take:
                    exit_idx, exit_price, outcome = j, s.take, "win"
                    break
            else:
                if high >= s.stop:
                    exit_idx, exit_price, outcome = j, s.stop, "loss"
                    break
                if low <= s.take:
                    exit_idx, exit_price, outcome = j, s.take, "win"
                    break

        if s.direction == Direction.LONG:
            pnl = (exit_price - s.entry) / risk
        else:
            pnl = (s.entry - exit_price) / risk

        trades.append(Trade(
            strategy=s.strategy,
            entry_idx=s.bar_index, exit_idx=exit_idx,
            direction=s.direction.value,
            entry=s.entry, stop=s.stop, take=s.take,
            exit_price=exit_price, outcome=outcome, pnl_r=pnl,
        ))
        busy_until = exit_idx

    return trades


def stats(trades: list[Trade]) -> dict:
    if not trades:
        return dict(total=0, win_rate=0, pf=0, exp=0, dd=0, total_r=0)
    wins = [t.pnl_r for t in trades if t.pnl_r > 0]
    losses = [t.pnl_r for t in trades if t.pnl_r < 0]
    pf = sum(wins) / -sum(losses) if losses else float("inf")
    if pf == float("inf"):
        pf = 99
    equity = np.cumsum([t.pnl_r for t in trades])
    peak = -np.inf
    dd_max = 0
    for e in equity:
        peak = max(peak, e)
        dd_max = max(dd_max, peak - e)
    return {
        "total": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(trades) * 100,
        "pf": pf,
        "exp": sum(t.pnl_r for t in trades) / len(trades),
        "dd": dd_max,
        "total_r": sum(t.pnl_r for t in trades),
    }


def generate_synthetic(bars: int = 3000, seed: int = 42) -> pd.DataFrame:
    """Цикличный рынок: тренд → флэт → обратный тренд."""
    rng = np.random.default_rng(seed)
    times = pd.date_range("2025-01-01", periods=bars, freq="h")
    closes = [1.08]
    for i in range(bars - 1):
        phase = (i % 1500) / 1500
        if phase < 0.35:
            drift = 0.0002  # uptrend
        elif phase < 0.55:
            drift = 0.0     # flat
        elif phase < 0.85:
            drift = -0.00015  # downtrend
        else:
            drift = 0.0
        closes.append(closes[-1] + rng.normal(drift, 0.001))
    closes = np.array(closes)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + rng.uniform(0.0001, 0.001, bars)
    lows = np.minimum(opens, closes) - rng.uniform(0.0001, 0.001, bars)
    return pd.DataFrame({
        "open": opens, "high": highs, "low": lows, "close": closes,
    }, index=times)


def main() -> int:
    parser = argparse.ArgumentParser(description="Сравнение стратегий")
    parser.add_argument("--bars", type=int, default=3000)
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).resolve().parent.parent
                        / "docs" / "images" / "strategy-compare.png")
    args = parser.parse_args()

    print(f"Генерирую {args.bars} свечей...")
    df = generate_synthetic(args.bars)

    # EMA pullback strategy (использует код из bot/strategy.py)
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bot"))
    from strategy import detect_signals, prepare_dataframe  # noqa: E402

    df_with_ind = prepare_dataframe(df)

    strategies_def = [
        ("EMA50 Pullback",
         lambda: [
             Signal(bar_index=s.bar_index, timestamp=s.timestamp,
                    direction=Direction(s.direction.value),
                    entry=s.entry, stop=s.stop, take=s.take,
                    stop_pips=s.stop_pips, rr=s.rr,
                    reason=s.reason, strategy="ema_pullback")
             for s in detect_signals(df_with_ind)
         ]),
        ("Mean Reversion", lambda: mean_reversion.detect(df)),
        ("Breakout", lambda: breakout.detect(df)),
        ("Three Soldiers", lambda: three_soldiers.detect(df)),
        ("London Open Range", lambda: london_open.detect(df)),
    ]

    all_trades = {}
    for name, fn in strategies_def:
        signals = fn()
        trades = simulate(df, signals)
        all_trades[name] = trades

    # Сводная таблица
    print(f"\n{'Стратегия':<20} {'Сделок':>8} {'WR%':>6} "
          f"{'PF':>6} {'Exp R':>8} {'Итого R':>10} {'DD':>8}")
    print("─" * 75)
    for name, trades in all_trades.items():
        s = stats(trades)
        print(f"{name:<20} {s['total']:>8} {s['win_rate']:>5.1f} "
              f"{s['pf']:>6.2f} {s['exp']:>+8.2f} "
              f"{s['total_r']:>+10.2f} {s['dd']:>8.2f}")

    # График: сравнительные equity curves
    fig, ax = plt.subplots(figsize=(13, 7))
    colors = ["#1e40af", "#10b981", "#f59e0b", "#ef4444", "#7c3aed"]
    for (name, trades), color in zip(all_trades.items(), colors):
        if not trades:
            continue
        cum = np.cumsum([t.pnl_r for t in trades])
        x = list(range(len(cum)))
        ax.plot(x, cum, label=f"{name} ({stats(trades)['total_r']:+.1f}R)",
                color=color, linewidth=2)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Номер сделки")
    ax.set_ylabel("Кумулятивный результат (R)")
    ax.set_title("Сравнение equity curves — все стратегии на одних данных",
                 fontsize=13, weight="bold")
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(args.out, dpi=130)
    plt.close()

    print(f"\nГрафик сравнения: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
