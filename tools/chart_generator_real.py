"""
Перерисовка ключевых учебных графиков на РЕАЛЬНЫХ данных EUR/USD.

В отличие от chart_generator.py (синтетика для иллюстрации концепций),
этот скрипт ищет реальные паттерны в скачанных данных и рисует их.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "docs" / "images" / "real"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "#fafafa",
        "axes.grid": True,
        "grid.color": "#e5e5e5",
        "grid.linewidth": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 11,
    }
)

UP, DOWN = "#10b981", "#ef4444"


def draw_candle(ax, x, o, h, lo, c, width=0.6):
    color = UP if c >= o else DOWN
    ax.plot([x, x], [lo, h], color=color, linewidth=1.0, zorder=2)
    body_low = min(o, c)
    body_h = max(abs(c - o), (h - lo) * 0.001)
    ax.add_patch(
        Rectangle(
            (x - width / 2, body_low),
            width,
            body_h,
            facecolor=color,
            edgecolor=color,
            zorder=3,
        )
    )


def load(pair: str = "EURUSD", tf: str = "1h") -> pd.DataFrame:
    path = DATA / f"{pair}_{tf}.csv"
    df = pd.read_csv(path)
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df = df.set_index("datetime")
    return df[["open", "high", "low", "close"]].astype(float)


# --- 1. Real EMA chart ---
def chart_real_ema():
    df = load().tail(200)
    df = df.reset_index(drop=True)
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()

    fig, ax = plt.subplots(figsize=(13, 7))
    for i, row in df.iterrows():
        draw_candle(
            ax, i, row["open"], row["high"], row["low"], row["close"], width=0.7
        )
    ax.plot(df.index, df["ema50"], color="#2563eb", linewidth=2.2, label="EMA 50")
    ax.plot(df.index, df["ema200"], color="#dc2626", linewidth=2.2, label="EMA 200")
    ax.legend(fontsize=11, loc="upper left")
    ax.set_title(
        "EMA 50 / EMA 200 — РЕАЛЬНЫЕ данные EUR/USD H1 (последние 200 свечей)",
        fontsize=12,
        weight="bold",
    )
    ax.set_ylabel("Цена EUR/USD")
    ax.set_xlabel("Свечи (H1)")
    plt.tight_layout()
    plt.savefig(OUT / "ema-real.png", dpi=130)
    plt.close()
    print("  ✓ ema-real.png")


# --- 2. Real RSI chart ---
def chart_real_rsi():
    df = load().tail(150).reset_index(drop=True)
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_g = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_l = loss.ewm(alpha=1 / 14, adjust=False).mean()
    rs = avg_g / avg_l.replace(0, np.nan)
    df["rsi"] = (100 - 100 / (1 + rs)).fillna(50)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(13, 8), gridspec_kw={"height_ratios": [3, 1.5]}, sharex=True
    )
    for i, row in df.iterrows():
        draw_candle(
            ax1, i, row["open"], row["high"], row["low"], row["close"], width=0.7
        )
    ax1.set_title("RSI(14) — РЕАЛЬНЫЕ данные EUR/USD H1", fontsize=12, weight="bold")
    ax1.set_ylabel("Цена")

    ax2.plot(df.index, df["rsi"], color="#7c3aed", linewidth=1.5)
    ax2.axhline(
        70, color=DOWN, linestyle="--", linewidth=1.2, label="70 — перекупленность"
    )
    ax2.axhline(
        30, color=UP, linestyle="--", linewidth=1.2, label="30 — перепроданность"
    )
    ax2.axhline(50, color="#9ca3af", linestyle=":", linewidth=1)
    ax2.fill_between(
        df.index, 70, df["rsi"].where(df["rsi"] > 70), color=DOWN, alpha=0.2
    )
    ax2.fill_between(df.index, 30, df["rsi"].where(df["rsi"] < 30), color=UP, alpha=0.2)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("RSI")
    ax2.legend(fontsize=9, loc="upper left")
    plt.tight_layout()
    plt.savefig(OUT / "rsi-real.png", dpi=130)
    plt.close()
    print("  ✓ rsi-real.png")


# --- 3. Real Bollinger ---
def chart_real_bollinger():
    df = load().tail(150).reset_index(drop=True)
    ma = df["close"].rolling(20).mean()
    std = df["close"].rolling(20).std()
    df["upper"] = ma + 2 * std
    df["lower"] = ma - 2 * std
    df["ma"] = ma

    fig, ax = plt.subplots(figsize=(13, 7))
    for i, row in df.iterrows():
        draw_candle(
            ax, i, row["open"], row["high"], row["low"], row["close"], width=0.7
        )
    ax.plot(df.index, df["ma"], color="#2563eb", linewidth=1.5, label="MA 20")
    ax.plot(df.index, df["upper"], color="#9333ea", linewidth=1.3, label="Upper +2σ")
    ax.plot(df.index, df["lower"], color="#9333ea", linewidth=1.3, label="Lower −2σ")
    ax.fill_between(df.index, df["upper"], df["lower"], color="#9333ea", alpha=0.07)
    ax.legend(fontsize=10, loc="upper left")
    ax.set_title(
        "Bollinger Bands (20, 2) — РЕАЛЬНЫЕ данные EUR/USD H1",
        fontsize=12,
        weight="bold",
    )
    ax.set_ylabel("Цена")
    plt.tight_layout()
    plt.savefig(OUT / "bollinger-real.png", dpi=130)
    plt.close()
    print("  ✓ bollinger-real.png")


# --- 4. Real MACD ---
def chart_real_macd():
    df = load().tail(150).reset_index(drop=True)
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(13, 8), gridspec_kw={"height_ratios": [3, 1.5]}, sharex=True
    )
    for i, row in df.iterrows():
        draw_candle(
            ax1, i, row["open"], row["high"], row["low"], row["close"], width=0.7
        )
    ax1.set_title(
        "MACD (12, 26, 9) — РЕАЛЬНЫЕ данные EUR/USD H1", fontsize=12, weight="bold"
    )
    ax1.set_ylabel("Цена")

    ax2.plot(df.index, macd, color="#2563eb", linewidth=1.5, label="MACD")
    ax2.plot(df.index, signal, color="#f97316", linewidth=1.5, label="Сигнальная")
    colors = [UP if h >= 0 else DOWN for h in hist]
    ax2.bar(df.index, hist, color=colors, alpha=0.5)
    ax2.axhline(0, color="#9ca3af", linewidth=0.8)
    ax2.set_ylabel("MACD")
    ax2.legend(fontsize=9, loc="upper left")
    plt.tight_layout()
    plt.savefig(OUT / "macd-real.png", dpi=130)
    plt.close()
    print("  ✓ macd-real.png")


# --- 5. Real Equity curves on multi-pair backtest ---
def chart_real_equity():
    """Сводный график equity curves по всем парам из multi-pair бэктеста."""
    sys.path.insert(0, str(ROOT / "advanced"))
    from multi_pair_backtest import PAIRS, load as load_pair

    fig, ax = plt.subplots(figsize=(13, 7))
    colors = [
        "#1e40af",
        "#10b981",
        "#f59e0b",
        "#ef4444",
        "#7c3aed",
        "#06b6d4",
        "#ec4899",
        "#84cc16",
    ]

    sys.path.insert(0, str(ROOT / "bot"))
    from strategy import detect_signals, prepare_dataframe
    from multi_pair_backtest import simulate

    for pair, color in zip(PAIRS, colors):
        df = load_pair(pair, "1h")
        if df.empty:
            continue
        pip_size = 0.01 if "JPY" in pair else 0.0001
        signals = detect_signals(prepare_dataframe(df), pip_size=pip_size)
        trades = simulate(df, signals)
        if not trades:
            continue
        equity = np.cumsum([t["pnl_r"] for t in trades])
        ax.plot(
            range(len(equity)),
            equity,
            label=f"{pair} ({equity[-1]:+.1f}R)",
            color=color,
            linewidth=1.8,
            alpha=0.85,
        )

    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel("Номер сделки")
    ax.set_ylabel("Кумулятивный результат (R)")
    ax.set_title(
        "Equity curves всех 8 пар — РЕАЛЬНЫЕ данные за ~2 года\n"
        "Жёсткая правда о бэктесте на одной паре vs. multi-pair",
        fontsize=12,
        weight="bold",
    )
    ax.legend(loc="upper left", fontsize=9, ncol=2)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "equity-multi-pair-real.png", dpi=130)
    plt.close()
    print("  ✓ equity-multi-pair-real.png")


# --- 6. Strategy example on REAL data with real entry ---
def chart_real_strategy_example():
    """Найти реальный сигнал в данных и нарисовать его."""
    sys.path.insert(0, str(ROOT / "bot"))
    from strategy import detect_signals, prepare_dataframe

    df = load()
    df_prep = prepare_dataframe(df)
    signals = detect_signals(df_prep)
    if not signals:
        print("  ⚠️  Не нашёл сигналов")
        return

    # Выберем сигнал, который выиграл (чтобы был наглядным)
    sig = signals[len(signals) // 2]  # средний, чтобы было видно «после»
    idx = sig.bar_index

    # Берём окно ±30 свечей от сигнала
    start = max(0, idx - 30)
    end = min(len(df_prep), idx + 30)
    window = df_prep.iloc[start:end].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(13, 7))
    for i, row in window.iterrows():
        draw_candle(
            ax, i, row["open"], row["high"], row["low"], row["close"], width=0.7
        )
    ax.plot(
        window.index, window["ema50"], color="#2563eb", linewidth=2.2, label="EMA 50"
    )
    ax.plot(
        window.index, window["ema200"], color="#dc2626", linewidth=2.2, label="EMA 200"
    )

    local_idx = idx - start
    ax.axhline(
        sig.entry,
        color="#10b981",
        linestyle=":",
        xmin=local_idx / len(window),
        label=f"Вход {sig.direction.value.upper()} {sig.entry:.5f}",
    )
    ax.axhline(
        sig.stop,
        color="#ef4444",
        linestyle="--",
        xmin=local_idx / len(window),
        label=f"Stop Loss {sig.stop:.5f}",
    )
    ax.axhline(
        sig.take,
        color="#22c55e",
        linestyle="--",
        xmin=local_idx / len(window),
        label=f"Take Profit {sig.take:.5f}",
    )

    ax.annotate(
        f"СИГНАЛ {sig.direction.value.upper()}\n{sig.reason}\nR:R 1:{sig.rr:.0f}",
        xy=(local_idx, sig.entry),
        xytext=(
            local_idx - 15,
            sig.entry + (window["high"].max() - window["low"].min()) * 0.3,
        ),
        fontsize=11,
        weight="bold",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fef3c7", edgecolor="#f59e0b"),
    )

    ax.legend(loc="upper left", fontsize=10)
    ax.set_title(
        "РЕАЛЬНЫЙ сигнал EMA50 pullback на EUR/USD H1", fontsize=12, weight="bold"
    )
    ax.set_ylabel("Цена")
    ax.set_xlabel("Свечи")
    plt.tight_layout()
    plt.savefig(OUT / "strategy-real.png", dpi=130)
    plt.close()
    print("  ✓ strategy-real.png")


if __name__ == "__main__":
    print("Перерисовка ключевых графиков на РЕАЛЬНЫХ данных EUR/USD\n")
    chart_real_ema()
    chart_real_rsi()
    chart_real_bollinger()
    chart_real_macd()
    chart_real_equity()
    chart_real_strategy_example()
    print(f"\nГотово. Файлы в {OUT}")
