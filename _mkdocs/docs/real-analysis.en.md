# Real Technical Analysis EUR/USD

> All charts below are built on **real historical EUR/USD H1 data** (1-hour candles) downloaded via yfinance. No synthetic data.

---

## EMA 50 / EMA 200 — Trend

Two moving averages are the foundation of trend trading. When EMA50 is above EMA200 — bullish trend. Below — bearish.

![EMA 50/200 on real data](images/real/ema-real.png)

**What we see:**
- The blue line (EMA50) reacts faster to price movement
- The red line (EMA200) — a slow trend filter
- Crossover from below upward = buy signal (Golden Cross)
- Crossover from above downward = sell signal (Death Cross)

---

## RSI(14) — Overbought / Oversold

RSI measures the strength of movement. Above 70 — the market is overbought (a pullback downward is possible). Below 30 — oversold (a bounce upward is possible).

![RSI on real data](images/real/rsi-real.png)

**What we see:**
- Red zones at the top (>70) = caution signal for buyers
- Green zones at the bottom (<30) = zone of interest for buying
- RSI works better in a sideways market; in a strong trend it gives false signals

---

## Bollinger Bands (20, 2) — Volatility

Bollinger Bands show the "normal" price range. A breakout outside the bands = an extreme, and price often returns to the middle.

![Bollinger Bands on real data](images/real/bollinger-real.png)

**What we see:**
- Bands narrow before a strong move (volatility squeeze)
- They expand during a trend
- Touching the upper band ≠ sell signal; confirmation is required

---

## MACD (12, 26, 9) — Trend Momentum

MACD shows the difference between two EMAs. A crossover of the MACD and signal lines produces entry signals.

![MACD on real data](images/real/macd-real.png)

**What we see:**
- The blue line (MACD) crosses the orange line (signal) from below upward → bullish signal
- Green histogram = growing momentum, red = declining momentum
- Divergence between price and MACD = strong reversal signal

---

## Real Trading Signal — Entry, SL, TP

Here is what a genuine EMA50 pullback signal looks like: price is in a bullish trend, has pulled back to EMA50, and a candle confirms the entry.

![Real EMA50 pullback signal](images/real/strategy-real.png)

**What we see:**
- Green dashed line = entry price
- Red dashed line = stop-loss (behind the nearest swing extreme)
- Green dashed line = take-profit (R:R 1:2)

---

## Equity Curves — 8 Currency Pairs (Honest Results)

This is the backtest result of **one strategy (EMA50 pullback)** on 8 different pairs over ~2 years of real data.

![Equity curves 8 pairs](images/real/equity-multi-pair-real.png)

!!! warning "Key Lesson"
    Average Profit Factor = **1.07** — that is nearly break-even. Not a single pair produced PF ≥ 1.5.
    
    **Takeaway:** a strategy that works well on EUR/USD does not necessarily work on other pairs. This is exactly why you cannot trust a backtest run on a single pair only.

---

## How to Run the Analysis Yourself

All scripts are already in the project:

```bash
# Download fresh data (8 pairs × 2 timeframes)
python advanced/download_all_pairs.py

# Regenerate all 6 charts on fresh data
python tools/chart_generator_real.py

# Run the multi-pair backtest
python advanced/multi_pair_backtest.py

# Economic calendar for today (Forex Factory)
python tools/news_scraper.py
```

---

## Economic Calendar (Forex Factory)

We have a script `tools/news_scraper.py` that downloads the important events for today:

```bash
# Show important events today
python tools/news_scraper.py

# Tomorrow
python tools/news_scraper.py --date tomorrow

# This week
python tools/news_scraper.py --date this-week
```

Events with a red icon (high impact) are the most important. These include:
- **NFP** (Non-Farm Payrolls) — every first Friday of the month
- **Fed / ECB rate decisions**
- **CPI** (inflation)
- **GDP**

!!! tip "Beginner's Rule"
    Do not trade 30 minutes before or 30 minutes after red events. Volatility spikes sharply and a stop-loss can be triggered without any meaningful price movement.
