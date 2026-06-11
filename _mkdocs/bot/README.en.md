# Bot — Signal Detector and Backtester

> **⚠️ IMPORTANT: this is NOT a live trading bot.**
>
> This code does not connect to a broker and does not open real orders. It is a **learning tool** for:
> - Understanding how a strategy is expressed in code
> - Running a strategy on historical data (backtest)
> - Computing statistics: win rate, profit factor, expectancy, drawdown
>
> Before connecting anything to a real account you need at minimum: one year of demo experience, an understanding of your broker's API, error handling, bug protection, risk limiters, and tests.

## What's Inside

| File | Purpose |
|---|---|
| [`strategy.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/bot/strategy.py) | Strategy logic: indicators, patterns, signal detector |
| [`backtest.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/bot/backtest.py) | Data loading, trade simulation, statistics, equity curve |

## Running

```bash
# From the project root, after activating the venv
.venv/bin/python bot/backtest.py

# With trade list and chart saved
.venv/bin/python bot/backtest.py --out my-curve.png --trades-csv my-trades.csv

# On your own CSV data
.venv/bin/python bot/backtest.py --csv ../data/eurusd_h1.csv

# With a different R:R
.venv/bin/python bot/backtest.py --rr 3.0
```

## What the Output Means

```
Total trades:         9
Profitable:           5
Losing:               4
Win rate:             55.6%
Average win:          +2.00R
Average loss:         −1.00R
Profit Factor:        2.50
Expectancy:           +0.67R / trade
Total:                +6.00R
Max drawdown:         1.00R
```

- **R** — unit of risk (1R = your stop). +2R means "took twice as much as you risked".
- **Win rate 55.6%** — share of profitable trades.
- **Profit Factor 2.50** — for every $1 lost, $2.50 was made. Good.
- **Expectancy +0.67R** — expected result of **one** trade. Over 100 trades = +67R profit.
- **Max drawdown 1.00R** — maximum decline from the peak.

## Equity Curve

After running, a file `equity-curve.png` is created with the cumulative result:

![Equity curve example](https://raw.githubusercontent.com/MukhammadAmir-Akbarov/forex-toolkit/main/bot/equity-curve.png)

A good equity curve **goes from bottom-left to top-right with manageable drawdowns**. Sharp drops, flat or negative dynamics — a signal that the strategy is not working.

## What This Bot Does NOT Do (by design)

- ❌ Does not connect to MetaTrader / cTrader / broker API
- ❌ Does not open real orders
- ❌ Does not account for spread, commission, slippage, or swaps (simplified)
- ❌ Does not use multi-timeframe analysis (simplified — uses EMA200 on the current TF)
- ❌ Has no news filter

These limitations matter: **real account results are always worse than a backtest**. Keep that in mind.

## How to Improve a Backtest Honestly

1. **Do not fit parameters**. If you keep tweaking RSI thresholds until you get a perfect chart — that is **overfitting**, and it will not hold in live markets.
2. **In-sample / out-of-sample**: tune on one half of the data, validate on the other.
3. **Walk-forward**: test on sequential historical windows, not on a single one.
4. **Account for spread**: subtract 1–2 pips from the profit of every trade.
5. **Real win rate on demo is typically 5–10% lower** than the backtest due to psychology and execution.

## CSV Format for Your Own Data

Historical data can be downloaded for free from:
- [Dukascopy Historical Data](https://www.dukascopy.com/swiss/english/marketwatch/historical/)
- In the MT5 terminal: F2 → export to CSV
- TradingView: right panel → Export Data (requires a Pro subscription)

Expected columns:

```csv
datetime,open,high,low,close
2026-01-01 00:00:00,1.08500,1.08620,1.08480,1.08590
2026-01-01 01:00:00,1.08590,1.08650,1.08550,1.08610
...
```

## The Road from This Script to a Real Bot

**It is a long road.** If you ever decide to take it:

1. **At least 6–12 months** of manual demo trading with the same strategy. If manual trading is not profitable — an algorithm will not save you.
2. **Learn your broker's API**: MetaTrader 5 has a Python package [`MetaTrader5`](https://pypi.org/project/MetaTrader5/) — but it only works on Windows.
3. **First**, trade **on demo only** through the bot for at least 3 months.
4. **Only after consistently profitable demo-bot trading** — a real account with a minimum deposit.
5. **Never** leave the bot unattended. Crashes, MT5 updates, bugs in the code — any of these can wipe out the deposit in an hour.

## Disclaimer

Educational code. Do not use on real accounts in its current form. Past backtest statistics do not guarantee future results. The author of the code bears no responsibility for decisions made on its basis.

---

[← Back to the main guide](../forex-guide.md)
