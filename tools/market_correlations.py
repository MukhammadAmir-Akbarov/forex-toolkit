#!/usr/bin/env python3
"""
Корреляции forex с другими рынками.

Скачивает данные через yfinance:
  - DXY (доллар-индекс) — главный драйвер всех USD-пар
  - Gold (XAUUSD) — обратно коррелирует с USD
  - S&P 500 (SPY) — индикатор risk-on / risk-off
  - VIX — индекс страха
  - Treasuries 10Y — облигации (TLT)
  - Bitcoin — для понимания aрик-он риска

Считает корреляции с EUR/USD, GBP/USD, USD/JPY.
Строит heatmap.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


SYMBOLS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",        # = USD/JPY
    "AUD/USD": "AUDUSD=X",
    "DXY": "DX-Y.NYB",         # US Dollar Index
    "Gold": "GC=F",            # Gold futures
    "S&P 500": "SPY",          # S&P 500 ETF
    "VIX": "^VIX",             # Volatility Index
    "10Y bonds": "TLT",        # 20+ Year Treasury Bond ETF (proxy)
    "Bitcoin": "BTC-USD",
}


def download_data(period: str = "1y") -> pd.DataFrame:
    """Скачивает закрытие всех символов."""
    print(f"Скачиваю данные за {period}...")
    closes = {}
    for label, symbol in SYMBOLS.items():
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            if not df.empty:
                closes[label] = df["Close"]
                print(f"  ✓ {label} ({symbol}): {len(df)} точек")
            else:
                print(f"  ❌ {label} ({symbol}): пусто")
        except Exception as e:
            print(f"  ❌ {label}: {e}")

    return pd.DataFrame(closes).dropna()


def calc_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Корреляции дневных доходностей."""
    returns = df.pct_change().dropna()
    return returns.corr()


def plot_heatmap(corr: pd.DataFrame, out_path: Path,
                 period_label: str = "1y") -> None:
    fig, ax = plt.subplots(figsize=(11, 9))

    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.index)

    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            v = corr.values[i, j]
            color = "white" if abs(v) > 0.5 else "black"
            weight = "bold" if abs(v) > 0.7 else "normal"
            ax.text(j, i, f"{v:+.2f}", ha="center", va="center",
                    color=color, fontsize=10, weight=weight)

    ax.set_title(
        f"Корреляция дневных доходностей ({period_label})\n"
        "🔴 = двигаются вместе, 🔵 = противоположно",
        fontsize=12, weight="bold",
    )
    fig.colorbar(im, ax=ax, label="Коэффициент корреляции (-1...+1)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def print_insights(corr: pd.DataFrame) -> None:
    print("\n" + "=" * 70)
    print("  КЛЮЧЕВЫЕ ИНСАЙТЫ")
    print("=" * 70)

    pairs = ["EUR/USD", "GBP/USD", "USD/JPY"]
    other = ["DXY", "Gold", "S&P 500", "VIX", "10Y bonds", "Bitcoin"]

    for pair in pairs:
        if pair not in corr.index:
            continue
        print(f"\n📊 {pair}:")
        for o in other:
            if o not in corr.columns:
                continue
            c = corr.loc[pair, o]
            if abs(c) > 0.7:
                direction = "↑↑ сильно положительная" if c > 0 else "↑↓ сильно отрицательная"
                emoji = "⚠️"
            elif abs(c) > 0.4:
                direction = "↑ положительная" if c > 0 else "↓ отрицательная"
                emoji = "📌"
            else:
                continue
            print(f"  {emoji} {o:<12} → {c:+.2f}  ({direction})")

    print("\n" + "─" * 70)
    print("📚 ВАЖНЫЕ ЗАМЕТКИ:")
    print()
    print("  💵 DXY (доллар-индекс):")
    print("     • Растёт → доллар сильный → EUR/USD, GBP/USD падают")
    print("     • Падает → EUR/USD, GBP/USD растут")
    print("     • Всегда смотри DXY перед сделкой!")
    print()
    print("  🥇 Gold:")
    print("     • Обратно коррелирует с DXY")
    print("     • Растёт в кризис (safe haven)")
    print("     • XAU/USD = «анти-USD»")
    print()
    print("  📈 S&P 500 / VIX:")
    print("     • Risk-on (рост S&P, падение VIX) → AUD, NZD, CAD растут")
    print("     • Risk-off (падение S&P, рост VIX) → JPY, CHF, USD растут")
    print()
    print("  ₿ Bitcoin:")
    print("     • Иногда коррелирует с risk-on (как акции)")
    print("     • Иногда — со страхом (как защитный актив)")
    print("     • Изменчиво — следи свежие данные")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Корреляции forex с другими рынками",
    )
    parser.add_argument("--period", default="1y",
                        choices=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                        help="Период анализа")
    parser.add_argument(
        "--out", type=Path,
        default=Path(__file__).resolve().parent.parent
        / "docs" / "images" / "market-correlations.png",
    )
    parser.add_argument("--csv", type=Path,
                        help="Сохранить корреляции в CSV")
    args = parser.parse_args()

    df = download_data(args.period)
    if df.empty or len(df.columns) < 3:
        print("❌ Не удалось скачать данные. Проверь интернет / yfinance.")
        return 1

    print(f"\n✓ Совмещённых дат: {len(df)}")
    corr = calc_correlations(df)

    print("\n📊 Матрица корреляции:")
    print(corr.round(2).to_string())

    print_insights(corr)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    plot_heatmap(corr, args.out, args.period)
    print(f"\nГрафик: {args.out}")

    if args.csv:
        corr.to_csv(args.csv)
        print(f"CSV: {args.csv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
