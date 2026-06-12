"""
Генератор учебных графиков для forex-гайда.
Создаёт PNG-картинки в docs/images/.
Все данные синтетические — для иллюстрации концепций, не реальные котировки.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

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


def draw_candle(ax, x, o, h, low, c, width=0.6):
    color = UP if c >= o else DOWN
    ax.plot([x, x], [low, h], color=color, linewidth=1.2, zorder=2)
    body_low = min(o, c)
    body_h = max(abs(c - o), (h - low) * 0.001)
    ax.add_patch(Rectangle((x - width / 2, body_low), width, body_h,
                           facecolor=color, edgecolor=color, zorder=3))


def synthetic_ohlc(n=80, seed=7, start=1.0850, vol=0.0015, drift=0.0):
    rng = np.random.default_rng(seed)
    closes = [start]
    for _ in range(n - 1):
        closes.append(closes[-1] + rng.normal(drift, vol))
    closes = np.array(closes)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + rng.uniform(0, vol, n)
    lows = np.minimum(opens, closes) - rng.uniform(0, vol, n)
    return pd.DataFrame({"o": opens, "h": highs, "l": lows, "c": closes})


# ---------- 1. Анатомия свечи ----------
def chart_candle_anatomy():
    fig, ax = plt.subplots(figsize=(8, 5))
    # Бычья
    draw_candle(ax, 1, 1.0840, 1.0875, 1.0830, 1.0865, width=0.4)
    ax.annotate("Закрытие", (1.2, 1.0865), fontsize=10)
    ax.annotate("Открытие", (1.2, 1.0840), fontsize=10)
    ax.annotate("Верхняя\nтень", (1.2, 1.0875), fontsize=9, color="#555")
    ax.annotate("Нижняя\nтень", (1.2, 1.0830), fontsize=9, color="#555")
    ax.annotate("Бычья\n(зелёная)\nC > O", (0.5, 1.0890), fontsize=10,
                color=UP, weight="bold", ha="center")

    # Медвежья
    draw_candle(ax, 3, 1.0865, 1.0875, 1.0830, 1.0840, width=0.4)
    ax.annotate("Открытие", (3.2, 1.0865), fontsize=10)
    ax.annotate("Закрытие", (3.2, 1.0840), fontsize=10)
    ax.annotate("Медвежья\n(красная)\nC < O", (2.5, 1.0890), fontsize=10,
                color=DOWN, weight="bold", ha="center")

    ax.set_xlim(0, 4.5)
    ax.set_ylim(1.0815, 1.0905)
    ax.set_xticks([])
    ax.set_title("Анатомия японской свечи", fontsize=13, weight="bold")
    ax.set_ylabel("Цена")
    plt.tight_layout()
    plt.savefig(OUT / "candle-anatomy.png", dpi=130)
    plt.close()


# ---------- 2. Свечные паттерны ----------
def chart_candle_patterns():
    fig, axes = plt.subplots(1, 4, figsize=(14, 4.5), sharey=True)
    patterns = [
        ("Молот\n(разворот вверх)", [(0, 1.082, 1.083, 1.078, 1.0822),
                                       (1, 1.0822, 1.0826, 1.0805, 1.0825),
                                       (2, 1.0825, 1.0830, 1.0823, 1.0828)]),
        ("Поглощение\n(бычье)", [(0, 1.082, 1.0824, 1.0815, 1.0817),
                                  (1, 1.0816, 1.0832, 1.0815, 1.083),
                                  (2, 1.083, 1.0834, 1.0828, 1.0833)]),
        ("Доджи\n(неопределённость)", [(0, 1.082, 1.083, 1.0815, 1.082),
                                         (1, 1.082, 1.0824, 1.0816, 1.0821),
                                         (2, 1.0821, 1.0825, 1.0817, 1.0822)]),
        ("Падающая\nзвезда", [(0, 1.0822, 1.0828, 1.082, 1.0827),
                                (1, 1.0828, 1.0840, 1.0826, 1.0828),
                                (2, 1.0828, 1.0832, 1.0820, 1.0822)]),
    ]
    for ax, (title, candles) in zip(axes, patterns):
        for x, o, h, low, c in candles:
            draw_candle(ax, x, o, h, low, c, width=0.5)
        ax.set_title(title, fontsize=11)
        ax.set_xticks([])
        ax.set_xlim(-0.7, 2.7)
    axes[0].set_ylabel("Цена")
    plt.suptitle("Базовые свечные паттерны", fontsize=13, weight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(OUT / "candle-patterns.png", dpi=130, bbox_inches="tight")
    plt.close()


# ---------- 3. Типы трендов ----------
def chart_trend_types():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    x = np.arange(50)
    up = 1.08 + 0.0003 * x + np.sin(x / 3) * 0.001
    down = 1.10 - 0.0003 * x + np.sin(x / 3) * 0.001
    flat = 1.085 + np.sin(x / 3) * 0.0015

    for ax, data, title, color in zip(
        axes,
        [up, down, flat],
        ["Восходящий тренд\n(higher highs + higher lows)",
         "Нисходящий тренд\n(lower highs + lower lows)",
         "Боковик / флэт\n(нет тренда)"],
        [UP, DOWN, "#6b7280"],
    ):
        ax.plot(x, data, color=color, linewidth=2)
        ax.set_title(title, fontsize=11)
        ax.set_xticks([])
        # Трендовая линия
        if title.startswith("Восход"):
            ax.plot([0, 49], [1.0795, 1.0938], color="#0ea5e9",
                    linestyle="--", linewidth=1.5, label="Линия поддержки")
            ax.legend(loc="upper left", fontsize=9)
        elif title.startswith("Нисход"):
            ax.plot([0, 49], [1.1005, 1.086], color="#f97316",
                    linestyle="--", linewidth=1.5, label="Линия сопротивления")
            ax.legend(loc="upper right", fontsize=9)
        else:
            ax.axhline(1.0870, color="#0ea5e9", linestyle="--", linewidth=1.3)
            ax.axhline(1.0835, color="#f97316", linestyle="--", linewidth=1.3)
    axes[0].set_ylabel("Цена")
    plt.tight_layout()
    plt.savefig(OUT / "trend-types.png", dpi=130)
    plt.close()


# ---------- 4. Поддержка / сопротивление ----------
def chart_support_resistance():
    df = synthetic_ohlc(60, seed=13, start=1.0820, vol=0.0008, drift=0.00005)
    # Прижимаем к уровням
    sup, res = 1.0810, 1.0875
    df["c"] = np.clip(df["c"], sup - 0.0005, res + 0.0005)
    df["h"] = np.maximum(df["h"], df["c"]) + 0.0003
    df["l"] = np.minimum(df["l"], df["c"]) - 0.0003

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, row in df.iterrows():
        draw_candle(ax, i, row.o, row.h, row.l, row.c, width=0.6)
    ax.axhline(res, color="#f97316", linewidth=2, label="Сопротивление 1.0875")
    ax.axhline(sup, color="#0ea5e9", linewidth=2, label="Поддержка 1.0810")
    ax.legend(loc="upper left", fontsize=10)
    ax.set_title("Уровни поддержки и сопротивления (EUR/USD, H1)",
                 fontsize=13, weight="bold")
    ax.set_ylabel("Цена")
    ax.set_xlabel("Свечи (H1)")
    plt.tight_layout()
    plt.savefig(OUT / "support-resistance.png", dpi=130)
    plt.close()


# ---------- 5. EMA ----------
def chart_ema():
    df = synthetic_ohlc(120, seed=42, start=1.0800, vol=0.0008, drift=0.00008)
    df["ema50"] = df["c"].ewm(span=50, adjust=False).mean()
    df["ema200"] = df["c"].ewm(span=200, adjust=False).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, row in df.iterrows():
        draw_candle(ax, i, row.o, row.h, row.l, row.c, width=0.6)
    ax.plot(df.index, df["ema50"], color="#2563eb", linewidth=2, label="EMA 50")
    ax.plot(df.index, df["ema200"], color="#dc2626", linewidth=2, label="EMA 200")
    ax.legend(fontsize=10, loc="upper left")
    ax.set_title("Скользящие средние EMA 50 и EMA 200",
                 fontsize=13, weight="bold")
    ax.set_ylabel("Цена")
    plt.tight_layout()
    plt.savefig(OUT / "ema-example.png", dpi=130)
    plt.close()


# ---------- 6. RSI ----------
def chart_rsi():
    df = synthetic_ohlc(100, seed=21, start=1.0800, vol=0.001, drift=0.00005)
    delta = df["c"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - 100 / (1 + rs)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                    gridspec_kw={"height_ratios": [3, 1.5]},
                                    sharex=True)
    for i, row in df.iterrows():
        draw_candle(ax1, i, row.o, row.h, row.l, row.c, width=0.6)
    ax1.set_title("RSI(14) — индикатор перекупленности/перепроданности",
                  fontsize=13, weight="bold")
    ax1.set_ylabel("Цена")

    ax2.plot(df.index, df["rsi"], color="#7c3aed", linewidth=1.5)
    ax2.axhline(70, color=DOWN, linestyle="--", linewidth=1.2,
                label="70 — перекупленность")
    ax2.axhline(30, color=UP, linestyle="--", linewidth=1.2,
                label="30 — перепроданность")
    ax2.axhline(50, color="#9ca3af", linestyle=":", linewidth=1)
    ax2.fill_between(df.index, 70, df["rsi"].where(df["rsi"] > 70),
                     color=DOWN, alpha=0.2)
    ax2.fill_between(df.index, 30, df["rsi"].where(df["rsi"] < 30),
                     color=UP, alpha=0.2)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("RSI")
    ax2.set_xlabel("Свечи")
    ax2.legend(fontsize=9, loc="upper left")
    plt.tight_layout()
    plt.savefig(OUT / "rsi-example.png", dpi=130)
    plt.close()


# ---------- 7. MACD ----------
def chart_macd():
    df = synthetic_ohlc(120, seed=8, start=1.0800, vol=0.0009, drift=0.00007)
    ema12 = df["c"].ewm(span=12, adjust=False).mean()
    ema26 = df["c"].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                    gridspec_kw={"height_ratios": [3, 1.5]},
                                    sharex=True)
    for i, row in df.iterrows():
        draw_candle(ax1, i, row.o, row.h, row.l, row.c, width=0.6)
    ax1.set_title("MACD (12, 26, 9)", fontsize=13, weight="bold")
    ax1.set_ylabel("Цена")

    ax2.plot(df.index, macd, color="#2563eb", linewidth=1.5, label="MACD")
    ax2.plot(df.index, signal, color="#f97316", linewidth=1.5,
             label="Сигнальная (9)")
    colors = [UP if h >= 0 else DOWN for h in hist]
    ax2.bar(df.index, hist, color=colors, alpha=0.5, label="Гистограмма")
    ax2.axhline(0, color="#9ca3af", linewidth=0.8)
    ax2.set_ylabel("MACD")
    ax2.set_xlabel("Свечи")
    ax2.legend(fontsize=9, loc="upper left")
    plt.tight_layout()
    plt.savefig(OUT / "macd-example.png", dpi=130)
    plt.close()


# ---------- 8. Bollinger Bands ----------
def chart_bollinger():
    df = synthetic_ohlc(100, seed=55, start=1.0800, vol=0.0009, drift=0.0)
    ma = df["c"].rolling(20).mean()
    std = df["c"].rolling(20).std()
    df["upper"] = ma + 2 * std
    df["lower"] = ma - 2 * std
    df["ma"] = ma

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, row in df.iterrows():
        draw_candle(ax, i, row.o, row.h, row.l, row.c, width=0.6)
    ax.plot(df.index, df["ma"], color="#2563eb", linewidth=1.5, label="MA 20")
    ax.plot(df.index, df["upper"], color="#9333ea", linewidth=1.2,
            label="Верхняя полоса (+2σ)")
    ax.plot(df.index, df["lower"], color="#9333ea", linewidth=1.2,
            label="Нижняя полоса (−2σ)")
    ax.fill_between(df.index, df["upper"], df["lower"],
                    color="#9333ea", alpha=0.07)
    ax.legend(fontsize=10, loc="upper left")
    ax.set_title("Bollinger Bands (20, 2)", fontsize=13, weight="bold")
    ax.set_ylabel("Цена")
    plt.tight_layout()
    plt.savefig(OUT / "bollinger-example.png", dpi=130)
    plt.close()


# ---------- 9. Графические паттерны ----------
def chart_patterns():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    # Голова и плечи
    x = np.linspace(0, 10, 200)
    head_shoulders = (
        1.080
        + 0.003 * np.exp(-((x - 2) ** 2) / 0.6)
        + 0.005 * np.exp(-((x - 5) ** 2) / 0.6)
        + 0.003 * np.exp(-((x - 8) ** 2) / 0.6)
    )
    axes[0].plot(x, head_shoulders, color="#2563eb", linewidth=2)
    axes[0].axhline(1.0803, color=DOWN, linestyle="--", label="Линия шеи")
    axes[0].annotate("Левое\nплечо", (2, 1.0833), fontsize=9, ha="center")
    axes[0].annotate("Голова", (5, 1.0855), fontsize=9, ha="center", weight="bold")
    axes[0].annotate("Правое\nплечо", (8, 1.0833), fontsize=9, ha="center")
    axes[0].set_title("Голова и плечи\n(разворот вниз)", fontsize=11)
    axes[0].legend(fontsize=9, loc="lower left")
    axes[0].set_xticks([])

    # Треугольник (восходящий)
    x = np.linspace(0, 10, 200)
    upper = 1.090 * np.ones_like(x)
    lower = 1.080 + 0.001 * x
    tri = lower + (upper - lower) * (0.5 + 0.4 * np.sin(x * 2))
    axes[1].plot(x, tri, color="#2563eb", linewidth=1.8)
    axes[1].plot(x, upper, color=DOWN, linestyle="--", label="Сопротивление")
    axes[1].plot(x, lower, color=UP, linestyle="--", label="Поддержка (растёт)")
    axes[1].set_title("Восходящий треугольник\n(чаще пробой вверх)", fontsize=11)
    axes[1].legend(fontsize=9, loc="lower right")
    axes[1].set_xticks([])

    # Двойная вершина
    x = np.linspace(0, 10, 200)
    double_top = (
        1.082
        + 0.004 * np.exp(-((x - 3) ** 2) / 0.5)
        + 0.004 * np.exp(-((x - 7) ** 2) / 0.5)
    )
    axes[2].plot(x, double_top, color="#2563eb", linewidth=2)
    axes[2].axhline(1.082, color=DOWN, linestyle="--", label="Линия шеи")
    axes[2].annotate("Вершина 1", (3, 1.0867), fontsize=9, ha="center")
    axes[2].annotate("Вершина 2", (7, 1.0867), fontsize=9, ha="center")
    axes[2].set_title("Двойная вершина\n(разворот вниз)", fontsize=11)
    axes[2].legend(fontsize=9, loc="lower left")
    axes[2].set_xticks([])

    axes[0].set_ylabel("Цена")
    plt.tight_layout()
    plt.savefig(OUT / "chart-patterns.png", dpi=130)
    plt.close()


# ---------- 10. Иллюстрация стратегии ----------
def chart_strategy_example():
    df = synthetic_ohlc(80, seed=99, start=1.0820, vol=0.0006, drift=0.00012)
    df["ema50"] = df["c"].ewm(span=50, adjust=False).mean()
    df["ema200"] = df["c"].ewm(span=200, adjust=False).mean()

    fig, ax = plt.subplots(figsize=(13, 7))
    for i, row in df.iterrows():
        draw_candle(ax, i, row.o, row.h, row.l, row.c, width=0.6)
    ax.plot(df.index, df["ema50"], color="#2563eb", linewidth=2, label="EMA 50")
    ax.plot(df.index, df["ema200"], color="#dc2626", linewidth=2, label="EMA 200")

    # Точка входа
    entry_idx = 55
    entry_price = df.loc[entry_idx, "c"]
    sl = entry_price - 0.0025
    tp = entry_price + 0.005

    ax.axhline(entry_price, color="#10b981", linewidth=1.3, linestyle=":",
               xmin=0.65, label=f"Вход (long) {entry_price:.4f}")
    ax.axhline(sl, color="#ef4444", linewidth=1.3, linestyle="--",
               xmin=0.65, label=f"Stop Loss {sl:.4f} (риск 25 пипсов)")
    ax.axhline(tp, color="#22c55e", linewidth=1.3, linestyle="--",
               xmin=0.65, label=f"Take Profit {tp:.4f} (цель 50 пипсов, R:R 1:2)")

    ax.annotate("Откат к EMA50\n+ бычья свеча\n→ ВХОД LONG",
                xy=(entry_idx, entry_price),
                xytext=(entry_idx - 25, entry_price + 0.004),
                fontsize=10, weight="bold",
                arrowprops=dict(arrowstyle="->", color="black", lw=1.4))

    ax.legend(loc="upper left", fontsize=10)
    ax.set_title("Учебный пример сигнала: откат к EMA50 по тренду",
                 fontsize=13, weight="bold")
    ax.set_ylabel("Цена")
    ax.set_xlabel("Свечи (H1)")
    plt.tight_layout()
    plt.savefig(OUT / "strategy-example.png", dpi=130)
    plt.close()


# ---------- 11. Risk / Reward визуализация ----------
def chart_risk_reward():
    fig, ax = plt.subplots(figsize=(10, 6))
    win_rates = np.arange(20, 81, 5)
    for rr, color, label in [
        (1.0, "#ef4444", "R:R = 1:1"),
        (2.0, "#f59e0b", "R:R = 1:2"),
        (3.0, "#10b981", "R:R = 1:3"),
        (5.0, "#3b82f6", "R:R = 1:5"),
    ]:
        ev = (win_rates / 100) * rr - (1 - win_rates / 100)
        ax.plot(win_rates, ev * 100, marker="o", linewidth=2,
                color=color, label=label)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel("Win rate (% прибыльных сделок)")
    ax.set_ylabel("Матожидание на сделку (%) — при риске 1%")
    ax.set_title("Почему Risk/Reward важнее, чем точность прогноза",
                 fontsize=13, weight="bold")
    ax.legend(fontsize=11)
    ax.fill_between(win_rates, -200, 0, color=DOWN, alpha=0.05)
    ax.fill_between(win_rates, 0, 200, color=UP, alpha=0.05)
    ax.set_ylim(-100, 350)
    plt.tight_layout()
    plt.savefig(OUT / "risk-reward.png", dpi=130)
    plt.close()


# ---------- 12. Математика разорения ----------
def chart_drawdown_math():
    losses = np.arange(5, 96, 5)
    recovery = losses / (100 - losses) * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(losses, recovery, width=4, color=DOWN, alpha=0.7,
                  edgecolor="#991b1b")
    for bar, loss, rec in zip(bars, losses, recovery):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
                f"{rec:.0f}%", ha="center", fontsize=9, weight="bold")
    ax.set_xlabel("Просадка депозита (%)")
    ax.set_ylabel("Нужно вернуть, чтобы выйти в ноль (%)")
    ax.set_title("Математика разорения: почему просадку легче не получить,\n"
                 "чем потом отыграть",
                 fontsize=12, weight="bold")
    ax.set_ylim(0, max(recovery) * 1.1)
    plt.tight_layout()
    plt.savefig(OUT / "drawdown-math.png", dpi=130)
    plt.close()


if __name__ == "__main__":
    print("Генерирую графики в", OUT)
    chart_candle_anatomy()
    chart_candle_patterns()
    chart_trend_types()
    chart_support_resistance()
    chart_ema()
    chart_rsi()
    chart_macd()
    chart_bollinger()
    chart_patterns()
    chart_strategy_example()
    chart_risk_reward()
    chart_drawdown_math()
    print("Готово. Создано:")
    for p in sorted(OUT.glob("*.png")):
        print(" ", p.name, f"({p.stat().st_size // 1024} KB)")
