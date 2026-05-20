#!/usr/bin/env python3
"""Скачать историю по 8 мажорным парам за максимально доступный период через yfinance."""
from __future__ import annotations

import sys
from pathlib import Path

import yfinance as yf

PAIRS = [
    ("EURUSD", "EURUSD=X"),
    ("GBPUSD", "GBPUSD=X"),
    ("USDJPY", "JPY=X"),
    ("AUDUSD", "AUDUSD=X"),
    ("USDCAD", "CAD=X"),
    ("NZDUSD", "NZDUSD=X"),
    ("EURJPY", "EURJPY=X"),
    ("GBPJPY", "GBPJPY=X"),
]

DATA = Path(__file__).resolve().parent.parent / "data"
DATA.mkdir(parents=True, exist_ok=True)


def main() -> int:
    print("Скачиваю 8 пар × ~2 года H1 (yfinance limit на 1h)...\n")
    summary = []
    for label, symbol in PAIRS:
        try:
            df = yf.Ticker(symbol).history(period="2y", interval="1h")
            if df.empty:
                print(f"  ❌ {label}: пусто")
                continue
            df.columns = [c.lower() for c in df.columns]
            df = df[["open", "high", "low", "close"]]
            out = DATA / f"{label}_1h.csv"
            df.to_csv(out)
            print(f"  ✓ {label}: {len(df)} свечей → {out.name}")
            summary.append((label, len(df)))
        except Exception as e:
            print(f"  ❌ {label}: {e}")

    print(f"\nИтого: {len(summary)}/{len(PAIRS)} пар скачано")
    print(f"Папка: {DATA}")

    # Также D1 — там доступно 5+ лет
    print("\nСкачиваю те же пары на D1 (5 лет)...\n")
    for label, symbol in PAIRS:
        try:
            df = yf.Ticker(symbol).history(period="5y", interval="1d")
            if df.empty:
                continue
            df.columns = [c.lower() for c in df.columns]
            df = df[["open", "high", "low", "close"]]
            out = DATA / f"{label}_1d.csv"
            df.to_csv(out)
            print(f"  ✓ {label} D1: {len(df)} свечей")
        except Exception as e:
            print(f"  ❌ {label} D1: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
