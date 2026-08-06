#!/usr/bin/env python3
"""
Калькулятор сложного процента для трейдинга.

Показывает, во что превратится депозит при стабильной месячной доходности.
Также строит график роста.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def project_growth(
    initial: float,
    monthly_return_pct: float,
    months: int,
    monthly_deposit: float = 0.0,
) -> list[float]:
    """Считает рост депозита по месяцам."""
    balance = initial
    history = [balance]
    for _ in range(months):
        balance = balance * (1 + monthly_return_pct / 100) + monthly_deposit
        history.append(balance)
    return history


def plot_growth(
    initial: float,
    returns: list[float],
    months: int,
    out_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(11, 6))
    colors = ["#10b981", "#3b82f6", "#f59e0b", "#ef4444"]
    for r, color in zip(returns, colors):
        history = project_growth(initial, r, months)
        x = np.arange(len(history))
        ax.plot(
            x,
            history,
            linewidth=2.2,
            color=color,
            label=f"{r}% в месяц → ${history[-1]:,.0f}",
        )
        ax.fill_between(x, initial, history, alpha=0.08, color=color)

    ax.axhline(
        initial,
        color="#6b7280",
        linestyle="--",
        linewidth=1,
        label=f"Начало: ${initial:,.0f}",
    )
    ax.set_xlabel("Месяц")
    ax.set_ylabel("Депозит ($)")
    ax.set_title(
        f"Сложный процент: рост ${initial:,.0f} за {months} месяцев",
        fontsize=13,
        weight="bold",
    )
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_yscale("log")
    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Калькулятор сложного процента для трейдинга",
    )
    parser.add_argument(
        "--initial", "-i", type=float, default=1000, help="Начальный депозит ($)"
    )
    parser.add_argument(
        "--months",
        "-m",
        type=int,
        default=24,
        help="Сколько месяцев проецировать (по умолч. 24)",
    )
    parser.add_argument(
        "--monthly", type=float, default=0, help="Ежемесячное пополнение ($)"
    )
    parser.add_argument(
        "--out", type=Path, default=Path("compound-growth.png"), help="Файл для графика"
    )
    args = parser.parse_args()

    # Сценарии: 1%, 3%, 5%, 10% в месяц
    returns = [1, 3, 5, 10]

    print(f"\nНачальный депозит: ${args.initial:,.2f}")
    print(f"Горизонт: {args.months} месяцев")
    if args.monthly > 0:
        print(f"Ежемесячное пополнение: ${args.monthly:.2f}")
    print()
    print(
        f"{'% в мес.':>10} {'Через 6 мес.':>15} "
        f"{'Через 12 мес.':>17} {'Через 24 мес.':>17} "
        f"{'Через 60 мес.':>17}"
    )
    print("─" * 80)

    for r in returns:
        h6 = project_growth(args.initial, r, 6, args.monthly)[-1]
        h12 = project_growth(args.initial, r, 12, args.monthly)[-1]
        h24 = project_growth(args.initial, r, 24, args.monthly)[-1]
        h60 = project_growth(args.initial, r, 60, args.monthly)[-1]
        print(f"{r:>9}% ${h6:>13,.0f} ${h12:>15,.0f} ${h24:>15,.0f} ${h60:>15,.0f}")

    print()
    print("─" * 80)
    print("РЕАЛИСТИЧНЫЕ ОЖИДАНИЯ:")
    print("  • Новичок: цель первого года — НЕ ПОТЕРЯТЬ депозит (0%)")
    print("  • Опытный трейдер: 3–5% в месяц = очень хороший результат")
    print("  • 10%+ в месяц регулярно — практически невозможно")
    print("  • Любые обещания 30%+ в месяц = МОШЕННИЧЕСТВО")

    plot_growth(args.initial, returns, args.months, args.out)
    print(f"\nГрафик сохранён: {args.out}")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
