#!/usr/bin/env python3
"""
Бэктестер для стратегии «Откат к EMA50 по тренду».

ЭТО НЕ ЖИВОЙ ТОРГОВЫЙ БОТ. Этот скрипт:
  1. Читает исторические OHLC данные (CSV) ИЛИ генерирует синтетические
  2. Применяет стратегию из strategy.py
  3. Считает статистику (win rate, profit factor, drawdown, equity curve)
  4. Строит график результатов

Запуск:
  python backtest.py                    # на синтетических данных
  python backtest.py --csv data.csv     # на своих данных

Формат CSV: колонки datetime,open,high,low,close (можно volume)
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from strategy import Direction, Signal, detect_signals, prepare_dataframe


@dataclass
class Trade:
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    direction: str
    entry: float
    stop: float
    take: float
    exit_price: float
    outcome: str          # "win" | "loss" | "timeout"
    pnl_pips: float
    pnl_r: float           # в единицах риска
    reason: str
    bars_held: int


def simulate(
    df: pd.DataFrame,
    signals: list[Signal],
    max_bars_in_trade: int = 24,
    pip_size: float = 0.0001,
) -> list[Trade]:
    """
    Прогон сделок по сигналам.
    Правило: сделка закрывается по SL, TP, или после max_bars_in_trade свечей.
    Симулятор НЕ открывает новую сделку, пока есть открытая.
    """
    trades: list[Trade] = []
    open_until_idx = -1

    for sig in signals:
        if sig.bar_index <= open_until_idx:
            continue  # пропускаем — позиция ещё открыта

        risk_per_unit = abs(sig.entry - sig.stop)
        if risk_per_unit == 0:
            continue

        # Прогоняем последующие свечи
        end_idx = min(sig.bar_index + max_bars_in_trade, len(df) - 1)
        exit_idx = end_idx
        exit_price = df.iloc[end_idx]["close"]
        outcome = "timeout"

        for j in range(sig.bar_index + 1, end_idx + 1):
            high = df.iloc[j]["high"]
            low = df.iloc[j]["low"]

            if sig.direction == Direction.LONG:
                # На свече касается стопа или тейка? Считаем приоритетом стоп
                hit_stop = low <= sig.stop
                hit_take = high >= sig.take
                if hit_stop and hit_take:
                    # Консервативно: считаем, что стоп сработал первым
                    exit_idx, exit_price, outcome = j, sig.stop, "loss"
                    break
                if hit_stop:
                    exit_idx, exit_price, outcome = j, sig.stop, "loss"
                    break
                if hit_take:
                    exit_idx, exit_price, outcome = j, sig.take, "win"
                    break
            else:  # SHORT
                hit_stop = high >= sig.stop
                hit_take = low <= sig.take
                if hit_stop and hit_take:
                    exit_idx, exit_price, outcome = j, sig.stop, "loss"
                    break
                if hit_stop:
                    exit_idx, exit_price, outcome = j, sig.stop, "loss"
                    break
                if hit_take:
                    exit_idx, exit_price, outcome = j, sig.take, "win"
                    break

        # PnL
        if sig.direction == Direction.LONG:
            pnl_pips = (exit_price - sig.entry) / pip_size
        else:
            pnl_pips = (sig.entry - exit_price) / pip_size

        pnl_r = pnl_pips / (risk_per_unit / pip_size)

        trades.append(Trade(
            entry_time=sig.timestamp,
            exit_time=df.index[exit_idx],
            direction=sig.direction.value,
            entry=sig.entry,
            stop=sig.stop,
            take=sig.take,
            exit_price=exit_price,
            outcome=outcome,
            pnl_pips=pnl_pips,
            pnl_r=pnl_r,
            reason=sig.reason,
            bars_held=exit_idx - sig.bar_index,
        ))
        open_until_idx = exit_idx

    return trades


def stats(trades: list[Trade]) -> dict:
    """Считает основные метрики стратегии."""
    if not trades:
        return {"total": 0}

    wins = [t for t in trades if t.outcome == "win"]
    losses = [t for t in trades if t.outcome == "loss"]
    timeouts = [t for t in trades if t.outcome == "timeout"]

    total_r = sum(t.pnl_r for t in trades)
    gross_win = sum(t.pnl_r for t in trades if t.pnl_r > 0)
    gross_loss = -sum(t.pnl_r for t in trades if t.pnl_r < 0)

    # Equity curve в R
    equity = np.cumsum([t.pnl_r for t in trades])
    drawdowns = []
    peak = -np.inf
    for e in equity:
        peak = max(peak, e)
        drawdowns.append(peak - e)
    max_dd = max(drawdowns) if drawdowns else 0

    return {
        "total": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "timeouts": len(timeouts),
        "win_rate": len(wins) / len(trades) if trades else 0,
        "avg_win_r": np.mean([t.pnl_r for t in wins]) if wins else 0,
        "avg_loss_r": np.mean([t.pnl_r for t in losses]) if losses else 0,
        "profit_factor": gross_win / gross_loss if gross_loss > 0 else float("inf"),
        "expectancy_r": total_r / len(trades),
        "total_r": total_r,
        "max_drawdown_r": max_dd,
    }


def print_report(s: dict) -> None:
    print()
    print("╭" + "─" * 50 + "╮")
    print("│  РЕЗУЛЬТАТЫ БЭКТЕСТА" + " " * 28 + "│")
    print("╰" + "─" * 50 + "╯")
    print()
    if s["total"] == 0:
        print("Сделок нет.")
        return
    print(f"  Всего сделок:         {s['total']}")
    print(f"  Прибыльных (win):     {s['wins']}")
    print(f"  Убыточных (loss):     {s['losses']}")
    print(f"  Закрытых по времени:  {s['timeouts']}")
    print()
    print(f"  Win rate:             {s['win_rate']*100:.1f}%")
    print(f"  Средний win:          {s['avg_win_r']:+.2f}R")
    print(f"  Средний loss:         {s['avg_loss_r']:+.2f}R")
    print(f"  Profit Factor:        {s['profit_factor']:.2f}")
    print(f"  Expectancy:           {s['expectancy_r']:+.2f}R / сделку")
    print(f"  Итого:                {s['total_r']:+.2f}R")
    print(f"  Макс. просадка:       {s['max_drawdown_r']:.2f}R")
    print()
    # Интерпретация
    pf = s["profit_factor"]
    if pf >= 1.5:
        print("  ✅ Profit Factor ≥ 1.5 — статистика подходящая для дальнейшего теста.")
    elif pf >= 1.2:
        print("  ⚠️  Profit Factor 1.2–1.5 — стратегия на грани, нужна доработка.")
    else:
        print("  ❌ Profit Factor < 1.2 — стратегия в текущем виде убыточна.")
    print()


def plot_equity(trades: list[Trade], out_path: Path) -> None:
    """Рисует equity curve (в единицах R)."""
    if not trades:
        return
    pnl_r = [t.pnl_r for t in trades]
    equity = np.cumsum(pnl_r)
    times = [t.exit_time for t in trades]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                    gridspec_kw={"height_ratios": [2, 1]},
                                    sharex=True)
    ax1.plot(times, equity, color="#2563eb", linewidth=2)
    ax1.fill_between(times, equity, 0,
                     where=(np.array(equity) >= 0),
                     color="#10b981", alpha=0.2)
    ax1.fill_between(times, equity, 0,
                     where=(np.array(equity) < 0),
                     color="#ef4444", alpha=0.2)
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.set_ylabel("Equity (R)")
    ax1.set_title("Equity curve — кумулятивный результат в единицах риска",
                  fontsize=12, weight="bold")
    ax1.grid(True, alpha=0.3)

    colors = ["#10b981" if r > 0 else "#ef4444" for r in pnl_r]
    ax2.bar(times, pnl_r, color=colors, width=pd.Timedelta(hours=2))
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylabel("P&L сделки (R)")
    ax2.set_xlabel("Время")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()
    print(f"  График сохранён: {out_path}")


def generate_synthetic_data(
    bars: int = 2000,
    seed: int = 42,
    start_price: float = 1.08,
) -> pd.DataFrame:
    """Генерирует синтетический H1-ряд с волнообразным трендом."""
    rng = np.random.default_rng(seed)
    times = pd.date_range("2026-01-01", periods=bars, freq="h")

    # Цикличный тренд: 800 свечей вверх, 800 вниз, 400 флэт
    closes = [start_price]
    for i in range(bars - 1):
        phase = (i % 2000) / 2000
        if phase < 0.4:
            drift = 0.00015
        elif phase < 0.8:
            drift = -0.00012
        else:
            drift = 0.0
        closes.append(closes[-1] + rng.normal(drift, 0.0008))

    closes = np.array(closes)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + rng.uniform(0.0001, 0.001, bars)
    lows = np.minimum(opens, closes) - rng.uniform(0.0001, 0.001, bars)

    return pd.DataFrame({
        "open": opens, "high": highs, "low": lows, "close": closes,
    }, index=times)


def load_csv(path: Path) -> pd.DataFrame:
    """Загружает OHLC из CSV. Ожидаемые колонки: datetime,open,high,low,close."""
    df = pd.read_csv(path)
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df = df.set_index("datetime")
    elif "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], utc=True)
        df = df.set_index("time")
    else:
        df.index = pd.to_datetime(df.iloc[:, 0], utc=True)
        df = df.iloc[:, 1:]
    required = {"open", "high", "low", "close"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV должен содержать колонки {required}")
    return df[["open", "high", "low", "close"]].astype(float)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Бэктестер стратегии EMA50 pullback",
    )
    parser.add_argument("--csv", type=Path,
                        help="CSV с OHLC данными (опц.). "
                             "Без него — синтетические данные.")
    parser.add_argument("--rr", type=float, default=2.0,
                        help="Risk/Reward соотношение (по умолч. 2.0)")
    parser.add_argument("--out", type=Path,
                        default=Path("equity-curve.png"),
                        help="Путь для графика equity curve")
    parser.add_argument("--bars", type=int, default=2000,
                        help="Сколько синтетических свечей сгенерировать")
    parser.add_argument("--trades-csv", type=Path,
                        help="Сохранить список сделок в CSV")
    args = parser.parse_args()

    if args.csv:
        print(f"Загружаю данные из {args.csv}…")
        df = load_csv(args.csv)
    else:
        print(f"Генерирую {args.bars} синтетических H1-свечей…")
        df = generate_synthetic_data(args.bars)

    print(f"Период: {df.index[0]} → {df.index[-1]} ({len(df)} свечей)")
    df = prepare_dataframe(df)

    print("Сканирую сигналы…")
    signals = detect_signals(df, rr=args.rr)
    print(f"  Найдено сигналов: {len(signals)}")

    print("Прогоняю сделки…")
    trades = simulate(df, signals)
    print(f"  Реальных входов (без перекрытий): {len(trades)}")

    s = stats(trades)
    print_report(s)

    if trades:
        plot_equity(trades, args.out)

    if args.trades_csv:
        trades_df = pd.DataFrame([asdict(t) for t in trades])
        trades_df.to_csv(args.trades_csv, index=False)
        print(f"  Сделки сохранены: {args.trades_csv}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
