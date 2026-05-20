#!/usr/bin/env python3
"""
Multi-pair backtest — прогоняет стратегию EMA50 на 8 мажорных парах
и строит сравнительный отчёт.

Цель: понять, **универсальна ли стратегия** или подогнана под одну пару.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bot"))

from strategy import detect_signals, prepare_dataframe  # noqa: E402

PAIRS = [
    "EURUSD", "GBPUSD", "AUDUSD", "NZDUSD",
    "USDJPY", "USDCAD", "EURJPY", "GBPJPY",
]

DATA = ROOT / "data"
OUT_IMG = ROOT / "docs" / "images" / "multi-pair-backtest.png"


@dataclass
class PairResult:
    pair: str
    timeframe: str
    bars: int
    n_signals: int
    n_trades: int
    wins: int
    losses: int
    win_rate: float
    profit_factor: float
    total_r: float
    avg_r: float
    max_dd: float


def load(pair: str, tf: str = "1h") -> pd.DataFrame:
    path = DATA / f"{pair}_{tf}.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df = df.set_index("datetime")
    return df[["open", "high", "low", "close"]].astype(float)


def simulate(df: pd.DataFrame, signals, max_bars: int = 30) -> list[dict]:
    trades = []
    busy = -1
    for s in signals:
        if s.bar_index <= busy:
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
            if s.direction.value == "long":
                if low <= s.stop:
                    exit_idx, exit_price, outcome = j, s.stop, "loss"; break
                if high >= s.take:
                    exit_idx, exit_price, outcome = j, s.take, "win"; break
            else:
                if high >= s.stop:
                    exit_idx, exit_price, outcome = j, s.stop, "loss"; break
                if low <= s.take:
                    exit_idx, exit_price, outcome = j, s.take, "win"; break
        pnl = ((exit_price - s.entry) if s.direction.value == "long"
               else (s.entry - exit_price)) / risk
        trades.append({"pnl_r": pnl, "outcome": outcome})
        busy = exit_idx
    return trades


def run_pair(pair: str, tf: str) -> PairResult | None:
    df = load(pair, tf)
    if df.empty or len(df) < 250:
        return None

    # Для JPY-пар нужно учесть размер пипса
    pip_size = 0.01 if "JPY" in pair else 0.0001

    df_prep = prepare_dataframe(df)
    signals = detect_signals(df_prep, pip_size=pip_size)
    trades = simulate(df, signals)

    if not trades:
        return PairResult(pair, tf, len(df), len(signals), 0, 0, 0,
                          0.0, 0.0, 0.0, 0.0, 0.0)

    wins = sum(1 for t in trades if t["pnl_r"] > 0)
    losses = sum(1 for t in trades if t["pnl_r"] < 0)
    win_pnl = sum(t["pnl_r"] for t in trades if t["pnl_r"] > 0)
    loss_pnl = -sum(t["pnl_r"] for t in trades if t["pnl_r"] < 0)
    pf = win_pnl / loss_pnl if loss_pnl > 0 else (99 if win_pnl else 0)

    equity = np.cumsum([t["pnl_r"] for t in trades])
    peak = -np.inf
    dd = 0.0
    for e in equity:
        peak = max(peak, e)
        dd = max(dd, peak - e)

    return PairResult(
        pair=pair, timeframe=tf, bars=len(df),
        n_signals=len(signals), n_trades=len(trades),
        wins=wins, losses=losses,
        win_rate=wins / len(trades) * 100,
        profit_factor=pf,
        total_r=sum(t["pnl_r"] for t in trades),
        avg_r=sum(t["pnl_r"] for t in trades) / len(trades),
        max_dd=dd,
    )


def plot_comparison(results: list[PairResult], out_path: Path) -> None:
    if not results:
        return

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    pairs = [r.pair for r in results]
    pfs = [r.profit_factor for r in results]
    wrs = [r.win_rate for r in results]
    totals = [r.total_r for r in results]
    dds = [r.max_dd for r in results]

    colors = ["#10b981" if p >= 1.2 else "#ef4444" for p in pfs]

    ax1.bar(pairs, pfs, color=colors, edgecolor="black", alpha=0.7)
    ax1.axhline(1.5, color="green", linestyle="--", label="Хорошо (≥1.5)")
    ax1.axhline(1.2, color="orange", linestyle="--", label="Граница (≥1.2)")
    ax1.axhline(1.0, color="red", linestyle="--", label="Breakeven")
    ax1.set_ylabel("Profit Factor")
    ax1.set_title("Profit Factor по парам", weight="bold")
    ax1.tick_params(axis="x", rotation=45)
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    colors = ["#10b981" if w >= 40 else "#ef4444" for w in wrs]
    ax2.bar(pairs, wrs, color=colors, edgecolor="black", alpha=0.7)
    ax2.axhline(40, color="orange", linestyle="--")
    ax2.set_ylabel("Win Rate (%)")
    ax2.set_title("Win Rate по парам", weight="bold")
    ax2.tick_params(axis="x", rotation=45)
    ax2.grid(alpha=0.3)

    colors = ["#10b981" if t > 0 else "#ef4444" for t in totals]
    ax3.bar(pairs, totals, color=colors, edgecolor="black", alpha=0.7)
    ax3.axhline(0, color="black")
    ax3.set_ylabel("Итого (R)")
    ax3.set_title("Итоговый результат (R)", weight="bold")
    ax3.tick_params(axis="x", rotation=45)
    ax3.grid(alpha=0.3)

    ax4.bar(pairs, dds, color="#7c3aed", edgecolor="black", alpha=0.7)
    ax4.set_ylabel("Просадка (R)")
    ax4.set_title("Максимальная просадка по парам", weight="bold")
    ax4.tick_params(axis="x", rotation=45)
    ax4.grid(alpha=0.3)

    plt.suptitle("Multi-Pair Backtest — EMA50 Pullback на 8 парах",
                 fontsize=14, weight="bold", y=1.00)
    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def print_report(results: list[PairResult]) -> None:
    print("\n" + "=" * 95)
    print("  MULTI-PAIR BACKTEST — EMA50 Pullback")
    print("=" * 95)
    print(f"\n{'Пара':<10} {'TF':<5} {'Свечей':<8} {'Сигн':<6} "
          f"{'Сделок':<8} {'WR%':<6} {'PF':<6} {'Итого R':<10} {'DD':<8}")
    print("─" * 95)

    for r in sorted(results, key=lambda x: -x.profit_factor):
        marker = "✅" if r.profit_factor >= 1.5 else \
                 "🟡" if r.profit_factor >= 1.2 else "❌"
        print(f"{r.pair:<10} {r.timeframe:<5} {r.bars:<8} "
              f"{r.n_signals:<6} {r.n_trades:<8} "
              f"{r.win_rate:<5.1f}% {r.profit_factor:<6.2f} "
              f"{r.total_r:<+10.2f} {r.max_dd:<7.2f} {marker}")

    print("─" * 95)

    # Аггрегаты
    valid = [r for r in results if r.n_trades > 0]
    if valid:
        avg_pf = np.mean([r.profit_factor for r in valid])
        median_pf = np.median([r.profit_factor for r in valid])
        good = sum(1 for r in valid if r.profit_factor >= 1.5)
        bad = sum(1 for r in valid if r.profit_factor < 1.0)
        total_trades = sum(r.n_trades for r in valid)
        total_r = sum(r.total_r for r in valid)

        print(f"\n  Пар протестировано:    {len(valid)}")
        print(f"  Всего сделок:          {total_trades}")
        print(f"  Средний PF:            {avg_pf:.2f}")
        print(f"  Медиана PF:            {median_pf:.2f}")
        print(f"  С PF ≥ 1.5:            {good}/{len(valid)}")
        print(f"  Убыточных (PF < 1):    {bad}/{len(valid)}")
        print(f"  Суммарно R:            {total_r:+.2f}")

        # Вердикт
        print("\n" + "─" * 95)
        if good / len(valid) >= 0.6:
            print("✅ ВЕРДИКТ: Стратегия УНИВЕРСАЛЬНА — работает на большинстве пар")
        elif good / len(valid) >= 0.3:
            print("🟡 ВЕРДИКТ: Стратегия СРЕДНЯЯ — работает на части пар")
        else:
            print("❌ ВЕРДИКТ: Стратегия ПОДОГНАНА под конкретные пары — переобучение")

        if bad >= len(valid) // 2:
            print("⚠️  Больше половины пар УБЫТОЧНЫ — стратегия НЕ для торговли")


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-pair backtest")
    parser.add_argument("--tf", default="1h", choices=["1h", "1d"])
    parser.add_argument("--pairs", nargs="+", default=PAIRS)
    args = parser.parse_args()

    print(f"Запускаю бэктест на {len(args.pairs)} парах, TF={args.tf}...")
    results = []
    for pair in args.pairs:
        r = run_pair(pair, args.tf)
        if r is None:
            print(f"  ⏭️  {pair}: нет данных")
            continue
        results.append(r)
        print(f"  ✓ {pair}: {r.n_trades} сделок, "
              f"WR {r.win_rate:.1f}%, PF {r.profit_factor:.2f}")

    print_report(results)
    plot_comparison(results, OUT_IMG)
    print(f"\nГрафик: {OUT_IMG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
