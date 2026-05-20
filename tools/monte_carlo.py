#!/usr/bin/env python3
"""
Монте-Карло симулятор торговой стратегии.

Прогоняет стратегию N раз с разным порядком сделок, показывает
ДИАПАЗОН возможных исходов. Полезно для понимания, что хороший месяц
может быть просто удачей.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def simulate_one(
    n_trades: int, win_rate: float, rr: float, risk_per_trade: float,
    rng: np.random.Generator,
) -> tuple[list[float], float]:
    """
    Одна симуляция. Возвращает equity curve и максимальную просадку.
    """
    equity = 1.0
    history = [equity]
    peak = equity
    max_dd = 0.0
    for _ in range(n_trades):
        wins = rng.random() < win_rate
        if wins:
            equity *= 1 + risk_per_trade * rr
        else:
            equity *= 1 - risk_per_trade
        history.append(equity)
        peak = max(peak, equity)
        dd = (peak - equity) / peak
        max_dd = max(max_dd, dd)
    return history, max_dd


def run_monte_carlo(
    n_simulations: int = 1000,
    n_trades: int = 100,
    win_rate: float = 0.5,
    rr: float = 2.0,
    risk_per_trade: float = 0.01,
    seed: int | None = None,
) -> dict:
    rng = np.random.default_rng(seed)
    results = []
    final_equities = []
    drawdowns = []
    for _ in range(n_simulations):
        history, max_dd = simulate_one(
            n_trades, win_rate, rr, risk_per_trade, rng,
        )
        results.append(history)
        final_equities.append(history[-1])
        drawdowns.append(max_dd)
    return {
        "histories": results,
        "final_equities": np.array(final_equities),
        "drawdowns": np.array(drawdowns),
    }


def print_summary(r: dict) -> None:
    fe = r["final_equities"]
    dd = r["drawdowns"]
    print("\n" + "=" * 60)
    print("  МОНТЕ-КАРЛО РЕЗУЛЬТАТЫ")
    print("=" * 60)
    print(f"\nФинальный капитал (множитель к начальному):")
    print(f"  Среднее:           {fe.mean():.3f}x")
    print(f"  Медиана:           {np.median(fe):.3f}x")
    print(f"  Худший 5%:         {np.percentile(fe, 5):.3f}x")
    print(f"  Худший 1%:         {np.percentile(fe, 1):.3f}x")
    print(f"  Лучший 95%:        {np.percentile(fe, 95):.3f}x")
    print(f"  Лучший 99%:        {np.percentile(fe, 99):.3f}x")

    print(f"\nМаксимальная просадка:")
    print(f"  Средняя:           {dd.mean()*100:.1f}%")
    print(f"  Медианная:         {np.median(dd)*100:.1f}%")
    print(f"  Худший 5% случаев: {np.percentile(dd, 95)*100:.1f}%")
    print(f"  Худший 1% случаев: {np.percentile(dd, 99)*100:.1f}%")

    print(f"\nВероятность просадки:")
    for threshold in [0.1, 0.2, 0.3, 0.5]:
        pct = (dd >= threshold).mean() * 100
        print(f"  ≥ {threshold*100:.0f}%: {pct:.1f}% случаев")

    print(f"\nВероятность потери:")
    print(f"  Закончить ниже 0.5x (-50%): {(fe < 0.5).mean()*100:.1f}%")
    print(f"  Закончить ниже 1.0x (минус): {(fe < 1.0).mean()*100:.1f}%")
    print(f"  Закончить выше 1.5x (+50%): {(fe > 1.5).mean()*100:.1f}%")
    print(f"  Закончить выше 2.0x (+100%): {(fe > 2.0).mean()*100:.1f}%")
    print()


def plot_results(r: dict, out_path: Path, title_suffix: str = "") -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    # 1. Equity curves (показываем 100 случайных)
    ax = axes[0, 0]
    histories = r["histories"]
    idx = np.random.default_rng(0).choice(len(histories), 100, replace=False)
    for i in idx:
        ax.plot(histories[i], alpha=0.15, color="#3b82f6", linewidth=0.5)
    median_curve = np.median(np.array(histories), axis=0)
    ax.plot(median_curve, color="#1e40af", linewidth=2.5, label="Медиана")
    ax.axhline(1.0, color="black", linewidth=1)
    ax.set_xlabel("Номер сделки")
    ax.set_ylabel("Equity (множитель)")
    ax.set_title(f"100 случайных equity curves {title_suffix}",
                 fontsize=11, weight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Распределение финального результата
    ax = axes[0, 1]
    ax.hist(r["final_equities"], bins=50, color="#10b981", alpha=0.7,
            edgecolor="#065f46")
    ax.axvline(1.0, color="red", linewidth=2, label="Безубыток")
    ax.axvline(r["final_equities"].mean(), color="blue", linewidth=2,
               label=f"Среднее: {r['final_equities'].mean():.2f}x")
    ax.set_xlabel("Финальный капитал (множитель)")
    ax.set_ylabel("Кол-во симуляций")
    ax.set_title("Распределение финального результата",
                 fontsize=11, weight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. Распределение просадок
    ax = axes[1, 0]
    ax.hist(r["drawdowns"] * 100, bins=50, color="#ef4444", alpha=0.7,
            edgecolor="#7f1d1d")
    ax.axvline(np.percentile(r["drawdowns"], 95) * 100, color="orange",
               linewidth=2, label=f"95% < {np.percentile(r['drawdowns'], 95)*100:.0f}%")
    ax.set_xlabel("Максимальная просадка (%)")
    ax.set_ylabel("Кол-во симуляций")
    ax.set_title("Распределение максимальной просадки",
                 fontsize=11, weight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. P&L vs Drawdown scatter
    ax = axes[1, 1]
    ax.scatter(r["drawdowns"] * 100, r["final_equities"],
               alpha=0.3, s=10, c="#7c3aed")
    ax.axhline(1.0, color="red", linewidth=1)
    ax.set_xlabel("Макс. просадка (%)")
    ax.set_ylabel("Финальный капитал (множитель)")
    ax.set_title("P&L vs Просадка по симуляциям",
                 fontsize=11, weight="bold")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Монте-Карло симуляция торговой стратегии",
    )
    parser.add_argument("--simulations", "-n", type=int, default=10000,
                        help="Число симуляций (по умолч. 10 000)")
    parser.add_argument("--trades", "-t", type=int, default=100,
                        help="Сделок в одной симуляции (по умолч. 100)")
    parser.add_argument("--winrate", "-w", type=float, default=0.5,
                        help="Win rate (0.5 = 50%%)")
    parser.add_argument("--rr", "-r", type=float, default=2.0,
                        help="Risk/Reward (2.0 = 1:2)")
    parser.add_argument("--risk", type=float, default=0.01,
                        help="Риск на сделку (0.01 = 1%%)")
    parser.add_argument("--out", type=Path,
                        default=Path("monte-carlo.png"),
                        help="Файл для графика")
    parser.add_argument("--seed", type=int, default=None,
                        help="Seed для воспроизводимости")
    args = parser.parse_args()

    print(f"Запускаю {args.simulations:,} симуляций × "
          f"{args.trades} сделок каждая...")
    print(f"  Win rate: {args.winrate*100:.0f}%")
    print(f"  R:R: 1:{args.rr}")
    print(f"  Риск на сделку: {args.risk*100:.1f}%")

    results = run_monte_carlo(
        args.simulations, args.trades, args.winrate, args.rr,
        args.risk, args.seed,
    )
    print_summary(results)
    plot_results(
        results, args.out,
        title_suffix=f"(WR={args.winrate*100:.0f}%, R:R=1:{args.rr})",
    )
    print(f"График сохранён: {args.out}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
