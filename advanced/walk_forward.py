#!/usr/bin/env python3
"""
Walk-forward optimization — проверка устойчивости стратегии.

Идея:
  1. Делим историю на N последовательных окон
  2. На каждом окне делим: тренировочные + проверочные данные
  3. На тренировочных подбираем лучшие параметры
  4. На проверочных проверяем выбранные параметры
  5. Считаем, насколько результат проверки повторяет тренировку

Если на каждом окне разные «лучшие» параметры → стратегия переобучена.
Если параметры стабильны → стратегия робастная.
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bot"))
from strategy import detect_signals, prepare_dataframe  # noqa: E402


def simulate(df, signals, max_bars=30):
    """Упрощённый симулятор. Возвращает суммарный R."""
    trades = []
    busy = -1
    for s in signals:
        if s.bar_index <= busy:
            continue
        risk = abs(s.entry - s.stop)
        if risk == 0:
            continue
        end = min(s.bar_index + max_bars, len(df) - 1)
        exit_price = df.iloc[end]["close"]
        outcome = "timeout"
        exit_idx = end
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
        if s.direction.value == "long":
            pnl = (exit_price - s.entry) / risk
        else:
            pnl = (s.entry - exit_price) / risk
        trades.append(pnl)
        busy = exit_idx
    return sum(trades), len(trades)


def grid_search(df, param_grid):
    """Возвращает лучшую комбинацию параметров и её PnL."""
    best = None
    best_pnl = -float("inf")
    for combo in param_grid:
        rr = combo["rr"]
        df_prep = prepare_dataframe(df)
        signals = detect_signals(df_prep, rr=rr)
        pnl, n = simulate(df, signals)
        if n > 0 and pnl > best_pnl:
            best_pnl = pnl
            best = combo
    return best, best_pnl


def generate_synthetic(bars: int = 5000, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    times = pd.date_range("2024-01-01", periods=bars, freq="h")
    closes = [1.08]
    for i in range(bars - 1):
        phase = (i % 1200) / 1200
        if phase < 0.4:
            drift = 0.00018
        elif phase < 0.7:
            drift = -0.0001
        else:
            drift = 0.0
        closes.append(closes[-1] + rng.normal(drift, 0.0009))
    closes = np.array(closes)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + rng.uniform(0.0001, 0.001, bars)
    lows = np.minimum(opens, closes) - rng.uniform(0.0001, 0.001, bars)
    return pd.DataFrame({
        "open": opens, "high": highs, "low": lows, "close": closes,
    }, index=times)


def walk_forward(df: pd.DataFrame, n_windows: int = 5,
                 train_ratio: float = 0.7) -> list[dict]:
    """Возвращает список результатов по окнам."""
    window_size = len(df) // n_windows
    train_size = int(window_size * train_ratio)

    param_grid = [{"rr": rr} for rr in [1.5, 2.0, 2.5, 3.0]]

    results = []
    for i in range(n_windows):
        start = i * window_size
        end = min((i + 1) * window_size, len(df))
        if end - start < 300:
            continue

        train = df.iloc[start:start + train_size]
        test = df.iloc[start + train_size:end]

        if len(test) < 100:
            continue

        # Поиск лучших параметров на train
        best, train_pnl = grid_search(train, param_grid)
        if best is None:
            continue

        # Проверка на test с теми же параметрами
        df_prep_test = prepare_dataframe(test)
        signals_test = detect_signals(df_prep_test, rr=best["rr"])
        test_pnl, test_n = simulate(test, signals_test)

        results.append({
            "window": i + 1,
            "best_rr": best["rr"],
            "train_pnl": train_pnl,
            "test_pnl": test_pnl,
            "test_trades": test_n,
            "train_period": f"{train.index[0]} → {train.index[-1]}",
            "test_period": f"{test.index[0]} → {test.index[-1]}",
        })

    return results


def plot_results(results: list[dict], out_path: Path) -> None:
    if not results:
        return
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    windows = [r["window"] for r in results]
    train_pnls = [r["train_pnl"] for r in results]
    test_pnls = [r["test_pnl"] for r in results]
    rrs = [r["best_rr"] for r in results]

    x = np.arange(len(windows))
    w = 0.35
    ax1.bar(x - w / 2, train_pnls, w, label="Train PnL", color="#3b82f6")
    ax1.bar(x + w / 2, test_pnls, w, label="Test PnL", color="#10b981")
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"Окно {w}" for w in windows])
    ax1.set_ylabel("PnL (R)")
    ax1.set_title("Walk-forward: Train vs Test результаты",
                  fontsize=12, weight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(x, rrs, "o-", color="#f59e0b", linewidth=2, markersize=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"Окно {w}" for w in windows])
    ax2.set_ylabel("Лучший R:R")
    ax2.set_title("Стабильность параметров (нестабильность = переобучение)",
                  fontsize=12, weight="bold")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Walk-forward optimization")
    parser.add_argument("--bars", type=int, default=5000)
    parser.add_argument("--windows", type=int, default=5)
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--out", type=Path,
                        default=Path("walk-forward.png"))
    args = parser.parse_args()

    print(f"Генерирую {args.bars} свечей…")
    df = generate_synthetic(args.bars)

    print(f"Walk-forward: {args.windows} окон, train ratio {args.train_ratio}")
    print()

    results = walk_forward(df, args.windows, args.train_ratio)
    if not results:
        print("Не удалось получить результаты")
        return 1

    print(f"{'Окно':<6} {'Best R:R':<10} {'Train PnL':>12} "
          f"{'Test PnL':>12} {'Test сделок':>12}")
    print("─" * 60)
    for r in results:
        print(f"{r['window']:<6} {r['best_rr']:<10.1f} "
              f"{r['train_pnl']:>+12.2f}R {r['test_pnl']:>+12.2f}R "
              f"{r['test_trades']:>12}")

    # Анализ
    avg_train = np.mean([r["train_pnl"] for r in results])
    avg_test = np.mean([r["test_pnl"] for r in results])
    consistent_rr = len(set(r["best_rr"] for r in results)) == 1

    print()
    print(f"Среднее train PnL: {avg_train:+.2f}R")
    print(f"Среднее test PnL:  {avg_test:+.2f}R")
    print(f"Стабильные параметры: {'✅ да' if consistent_rr else '⚠️  нет (возможно переобучение)'}")

    if avg_test < avg_train * 0.5:
        print("⚠️  Test результаты сильно хуже train — стратегия переподогнана")
    elif avg_test > 0:
        print("✅ Стратегия даёт прибыль на out-of-sample данных")
    else:
        print("❌ Стратегия не прибыльна на out-of-sample")

    plot_results(results, args.out)
    print(f"\nГрафик: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
