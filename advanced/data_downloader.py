#!/usr/bin/env python3
"""
Скачивание реальной исторической истории через yfinance.

Сохраняет OHLC в CSV в data/. Поддерживает основные валютные пары.

Использование:
  python data_downloader.py --symbol EURUSD --interval 1h --years 2
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import yfinance as yf


def yfinance_symbol(pair: str) -> str:
    """EURUSD → EURUSD=X для yfinance."""
    pair = pair.upper().replace("/", "")
    return f"{pair}=X"


def download(symbol: str, interval: str = "1h", years: int = 2) -> pd.DataFrame:
    yf_sym = yfinance_symbol(symbol)
    ticker = yf.Ticker(yf_sym)

    # yfinance: 1h данные доступны за последние ~2 года
    if interval in ("1h", "60m"):
        period = "2y" if years >= 2 else f"{years * 365}d"
    elif interval == "1d":
        period = f"{years}y"
    else:
        period = f"{years}y"

    print(f"Скачиваю {yf_sym} ({interval}, период {period})…")
    df = ticker.history(period=period, interval=interval)
    if df.empty:
        raise RuntimeError(f"Не удалось скачать {yf_sym}")

    df.columns = [c.lower() for c in df.columns]
    df = df[["open", "high", "low", "close"]]
    df.index.name = "datetime"
    return df


def main() -> int:
    parser = argparse.ArgumentParser(description="Скачивание истории")
    parser.add_argument("--symbol", default="EURUSD",
                        help="Валютная пара (по умолч. EURUSD)")
    parser.add_argument("--interval", default="1h",
                        choices=["1m", "5m", "15m", "30m", "1h", "1d"],
                        help="Таймфрейм")
    parser.add_argument("--years", type=int, default=2,
                        help="Сколько лет назад (по умолч. 2)")
    parser.add_argument("--out-dir", type=Path,
                        default=Path(__file__).resolve().parent.parent / "data")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    try:
        df = download(args.symbol, args.interval, args.years)
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    out_file = args.out_dir / f"{args.symbol}_{args.interval}.csv"
    df.to_csv(out_file)

    print(f"\n✓ Сохранено: {out_file}")
    print(f"  Свечей: {len(df)}")
    print(f"  Период: {df.index[0]} → {df.index[-1]}")
    print(f"  Размер: {out_file.stat().st_size // 1024} KB")
    print()
    print("Теперь можешь запустить бэктест:")
    print(f"  .venv/bin/python bot/backtest.py --csv {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
