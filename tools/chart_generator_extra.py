"""
Дополнительные учебные графики:
  - Fibonacci retracement
  - Расширенные свечные паттерны (morning/evening star, three soldiers)
  - Time-of-day heatmap
  - Корреляция валютных пар
  - Anatomy of a loss
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT = Path(__file__).resolve().parent.parent / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fafafa",
    "axes.grid": True,
    "grid.color": "#e5e5e5",
    "grid.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 11,
})

UP, DOWN = "#10b981", "#ef4444"


def draw_candle(ax, x, o, h, l, c, width=0.6):
    color = UP if c >= o else DOWN
    ax.plot([x, x], [l, h], color=color, linewidth=1.2, zorder=2)
    body_low = min(o, c)
    body_h = max(abs(c - o), (h - l) * 0.001)
    ax.add_patch(Rectangle((x - width / 2, body_low), width, body_h,
                           facecolor=color, edgecolor=color, zorder=3))


# ---------- Fibonacci retracement ----------
def chart_fibonacci():
    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(100)
    # Тренд вверх, потом откат
    trend_up = 1.080 + np.linspace(0, 0.015, 60)
    pullback = 1.095 - np.linspace(0, 0.009, 40)
    price = np.concatenate([trend_up, pullback])

    ax.plot(x, price, color="#3b82f6", linewidth=2)
    high = price[59]
    low = trend_up[0]
    delta = high - low

    fib_levels = [
        (0.000, "0.0 (high)", "#000000"),
        (0.236, "23.6%", "#9333ea"),
        (0.382, "38.2%", "#3b82f6"),
        (0.500, "50.0%", "#10b981"),
        (0.618, "61.8%", "#f59e0b"),
        (0.786, "78.6%", "#ef4444"),
        (1.000, "100% (low)", "#000000"),
    ]
    for ratio, label, color in fib_levels:
        y = high - delta * ratio
        ax.axhline(y, color=color, linewidth=1.2,
                   linestyle="--" if ratio not in (0.0, 1.0) else "-",
                   alpha=0.7)
        ax.text(101, y, f"  {label}: {y:.4f}", fontsize=10, color=color,
                va="center")

    ax.annotate("HIGH (точка 0)", xy=(59, high), xytext=(45, high + 0.003),
                fontsize=10, weight="bold",
                arrowprops=dict(arrowstyle="->"))
    ax.annotate("LOW (точка 1)", xy=(0, low), xytext=(5, low - 0.003),
                fontsize=10, weight="bold",
                arrowprops=dict(arrowstyle="->"))
    ax.set_title("Fibonacci retracement — уровни отката",
                 fontsize=13, weight="bold")
    ax.set_xlabel("Свечи")
    ax.set_ylabel("Цена")
    ax.set_xlim(-2, 130)
    plt.tight_layout()
    plt.savefig(OUT / "fibonacci.png", dpi=130)
    plt.close()


# ---------- Расширенные свечные паттерны ----------
def chart_advanced_candles():
    fig, axes = plt.subplots(1, 4, figsize=(15, 5), sharey=False)
    patterns = [
        ("Утренняя звезда\n(разворот вверх)",
         [(0, 1.085, 1.087, 1.080, 1.082),   # длинная красная
          (1, 1.0815, 1.0820, 1.0805, 1.0810),  # маленькая
          (2, 1.0815, 1.0875, 1.0810, 1.0865)]),  # длинная зелёная
        ("Вечерняя звезда\n(разворот вниз)",
         [(0, 1.082, 1.087, 1.080, 1.086),
          (1, 1.0865, 1.0875, 1.0860, 1.0867),
          (2, 1.0865, 1.0870, 1.0815, 1.0820)]),
        ("Три белых солдата",
         [(0, 1.080, 1.083, 1.0795, 1.0825),
          (1, 1.0825, 1.0850, 1.0820, 1.0845),
          (2, 1.0845, 1.0875, 1.0840, 1.0870)]),
        ("Три чёрные вороны",
         [(0, 1.087, 1.0875, 1.0845, 1.085),
          (1, 1.085, 1.0855, 1.0820, 1.0825),
          (2, 1.0825, 1.083, 1.0795, 1.0800)]),
    ]
    for ax, (title, candles) in zip(axes, patterns):
        for x, o, h, l, c in candles:
            draw_candle(ax, x, o, h, l, c, width=0.5)
        ax.set_title(title, fontsize=11, weight="bold")
        ax.set_xticks([])
        ax.set_xlim(-0.7, 2.7)
    axes[0].set_ylabel("Цена")
    plt.suptitle("Расширенные свечные паттерны",
                 fontsize=14, weight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(OUT / "advanced-candles.png", dpi=130, bbox_inches="tight")
    plt.close()


# ---------- Time-of-day heatmap ----------
def chart_time_heatmap():
    rng = np.random.default_rng(7)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    hours = list(range(0, 24))

    # Реалистичное распределение: лучше всего лондон+нью-йорк (10-16 UTC),
    # хуже всего азиатская сессия и пятница вечер
    heatmap = np.zeros((len(days), len(hours)))
    for i, d in enumerate(days):
        for j, h in enumerate(hours):
            base = rng.normal(0, 0.15)
            if 10 <= h <= 16:
                base += 0.6  # London + NY overlap
            elif 7 <= h <= 10:
                base += 0.3  # London open
            elif 14 <= h <= 19:
                base += 0.4  # NY
            elif 0 <= h <= 6:
                base -= 0.3  # Asian (плохо для мажоров)
            if d == "Fri" and h >= 18:
                base -= 0.5  # Friday evening
            heatmap[i, j] = base

    fig, ax = plt.subplots(figsize=(14, 4))
    im = ax.imshow(heatmap, cmap="RdYlGn", aspect="auto",
                   vmin=-0.8, vmax=0.8)

    ax.set_xticks(range(len(hours)))
    ax.set_xticklabels([f"{h:02d}" for h in hours])
    ax.set_yticks(range(len(days)))
    ax.set_yticklabels(days)
    ax.set_xlabel("Час (UTC)")
    ax.set_title("Карта прибыльности по времени (учебный пример)",
                 fontsize=13, weight="bold")

    # Подписи на ячейках
    for i in range(len(days)):
        for j in range(len(hours)):
            color = "white" if abs(heatmap[i, j]) > 0.4 else "black"
            ax.text(j, i, f"{heatmap[i, j]:+.1f}",
                    ha="center", va="center", color=color, fontsize=7)

    fig.colorbar(im, ax=ax, label="Средний P&L (R)")
    plt.tight_layout()
    plt.savefig(OUT / "time-heatmap.png", dpi=130)
    plt.close()


# ---------- Корреляция валютных пар ----------
def chart_correlation_matrix():
    pairs = ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDJPY",
             "USDCHF", "USDCAD", "EURJPY", "GBPJPY"]

    # Реалистичные исторические корреляции
    corr = np.array([
        [1.00, 0.85, 0.75, 0.70, -0.30, -0.95, -0.50, 0.55, 0.45],
        [0.85, 1.00, 0.65, 0.60, -0.25, -0.85, -0.40, 0.50, 0.85],
        [0.75, 0.65, 1.00, 0.90, -0.20, -0.70, 0.30, 0.40, 0.35],
        [0.70, 0.60, 0.90, 1.00, -0.15, -0.65, 0.25, 0.35, 0.30],
        [-0.30, -0.25, -0.20, -0.15, 1.00, 0.40, 0.45, 0.60, 0.65],
        [-0.95, -0.85, -0.70, -0.65, 0.40, 1.00, 0.50, -0.45, -0.40],
        [-0.50, -0.40, 0.30, 0.25, 0.45, 0.50, 1.00, -0.20, -0.10],
        [0.55, 0.50, 0.40, 0.35, 0.60, -0.45, -0.20, 1.00, 0.85],
        [0.45, 0.85, 0.35, 0.30, 0.65, -0.40, -0.10, 0.85, 1.00],
    ])

    fig, ax = plt.subplots(figsize=(10, 9))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)

    ax.set_xticks(range(len(pairs)))
    ax.set_yticks(range(len(pairs)))
    ax.set_xticklabels(pairs, rotation=45, ha="right")
    ax.set_yticklabels(pairs)

    for i in range(len(pairs)):
        for j in range(len(pairs)):
            color = "white" if abs(corr[i, j]) > 0.5 else "black"
            ax.text(j, i, f"{corr[i, j]:+.2f}",
                    ha="center", va="center", color=color, fontsize=10,
                    weight="bold" if abs(corr[i, j]) > 0.7 else "normal")

    ax.set_title(
        "Корреляция валютных пар (исторические значения)\n"
        "🔴 > +0.7 — двойная ставка в одну сторону   "
        "🔵 < −0.7 — противоположные позиции компенсируются",
        fontsize=12, weight="bold",
    )
    fig.colorbar(im, ax=ax, label="Коэффициент корреляции")
    plt.tight_layout()
    plt.savefig(OUT / "correlation-matrix.png", dpi=130)
    plt.close()


# ---------- Anatomy of a loss ----------
def chart_anatomy_of_loss():
    rng = np.random.default_rng(13)
    n = 80
    price = np.cumsum(rng.normal(0.00005, 0.0008, n)) + 1.085
    price[40:50] += np.linspace(0, 0.003, 10)
    price[50:60] -= np.linspace(0, 0.006, 10)  # резкий откат
    price[60:] -= np.linspace(0, 0.002, n - 60)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(np.arange(n), price, color="#3b82f6", linewidth=2)

    # 4 точки с ошибками
    points = [
        (15, "ОШИБКА 1:\nВход без чёткого\nсигнала (FOMO)", 0.4),
        (35, "ОШИБКА 2:\nСтоп слишком близко\n(20 пипсов на\nволатильном рынке)", 0.4),
        (52, "ОШИБКА 3:\nДвинул стоп дальше\n«чтобы дать шанс»", 0.45),
        (68, "ОШИБКА 4:\nЗакрыл руками\nна максимуме боли,\nне дождавшись стопа", 0.5),
    ]
    for x, text, ytext_frac in points:
        y = price[x]
        y_text = y + (price.max() - price.min()) * ytext_frac
        ax.annotate(
            text, xy=(x, y), xytext=(x + 3, y_text),
            fontsize=9.5, weight="bold", color="#7f1d1d",
            arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#fee2e2",
                      edgecolor="#dc2626", linewidth=1),
        )

    ax.set_title("Анатомия убыточной сделки — 4 типичные ошибки",
                 fontsize=13, weight="bold")
    ax.set_xlabel("Свечи (H1)")
    ax.set_ylabel("Цена")
    plt.tight_layout()
    plt.savefig(OUT / "anatomy-of-loss.png", dpi=130)
    plt.close()


# ---------- Monte Carlo иллюстрация ----------
def chart_monte_carlo_demo():
    """Сводный график для документации."""
    rng = np.random.default_rng(42)
    n_trades = 100
    n_sims = 200
    win_rate = 0.5
    rr = 2.0

    fig, ax = plt.subplots(figsize=(12, 7))
    final_results = []
    for _ in range(n_sims):
        eq = [1.0]
        for _ in range(n_trades):
            if rng.random() < win_rate:
                eq.append(eq[-1] * (1 + 0.01 * rr))
            else:
                eq.append(eq[-1] * (1 - 0.01))
        final_results.append(eq[-1])
        ax.plot(eq, alpha=0.15, color="#3b82f6", linewidth=0.5)

    median = np.median(np.array([list(range(n_trades + 1))] * n_sims), axis=0)
    ax.axhline(1.0, color="black", linewidth=1, label="Начало")
    ax.set_xlabel("Сделка")
    ax.set_ylabel("Equity (множитель)")
    ax.set_title(
        f"Монте-Карло: {n_sims} симуляций × {n_trades} сделок "
        f"(WR={int(win_rate*100)}%, R:R 1:{rr:.0f})",
        fontsize=12, weight="bold",
    )
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUT / "monte-carlo-demo.png", dpi=130)
    plt.close()


if __name__ == "__main__":
    print(f"Генерирую дополнительные графики в {OUT}")
    chart_fibonacci()
    chart_advanced_candles()
    chart_time_heatmap()
    chart_correlation_matrix()
    chart_anatomy_of_loss()
    chart_monte_carlo_demo()
    print("Готово. Создано:")
    for p in sorted(OUT.glob("*.png")):
        print(f"  {p.name} ({p.stat().st_size // 1024} KB)")
