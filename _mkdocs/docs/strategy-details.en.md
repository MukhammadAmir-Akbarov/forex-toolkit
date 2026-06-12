# "EMA50 Pullback with Trend" Strategy — In-Depth Breakdown

!!! info "🌐 Translation / Перевод"
    This is the English version of the page. The original is in Russian; switch languages using the language selector at the top of the page.
    *Это английская версия страницы; оригинал доступен на русском.*

> **This is an educational strategy, not a Holy Grail.** The goal is to show the structure of a trading approach: rules, risk management, verification. You must **test any strategy on demo for at least 100 trades** before trading real money.

## Table of Contents

1. [Strategy Idea](#1-strategy-idea)
2. [What Is a Complete Trading System](#2-what-is-a-complete-trading-system)
3. [Strategy Parameters](#3-strategy-parameters)
4. [Long Entry Conditions](#4-long-entry-conditions)
5. [Short Entry Conditions](#5-short-entry-conditions)
6. [Exiting a Trade](#6-exiting-a-trade)
7. [Position Management](#7-position-management)
8. [Chart Illustration](#8-chart-illustration)
9. [Backtest and Forward Test](#9-backtest-and-forward-test)
10. [When the Strategy Does NOT Work](#10-when-the-strategy-does-not-work)
11. [Improving the Strategy Through a Journal](#11-improving-the-strategy-through-a-journal)

---

## 1. Strategy Idea

**Buy low, sell high** — sounds obvious, but that is exactly the logic behind this strategy.

**In a strong trend, price does not move in a straight line**: it makes impulses and pullbacks. This strategy catches **pullbacks in the direction of the trend**, not the extreme highs and lows.

The logic:
- If the trend is bullish (price is above EMA200 on the higher timeframe) — **we only buy**.
- We do not buy at peaks; we buy on **pullbacks to dynamic support** (EMA50).
- We use a candlestick pattern as confirmation that the pullback is over.

This is a **trend-following strategy**. It underperforms in ranging markets, but delivers good R:R in trending conditions.

---

## 2. What Is a Complete Trading System

Any strategy is a set of **6 clear rules**:

| # | What we define | Example from our strategy |
|---|---|---|
| 1 | **When to watch the market** | After every H1 candle closes |
| 2 | **Which market to trade** | EUR/USD, GBP/USD — majors |
| 3 | **Which direction to trade** | Only with the H4 trend |
| 4 | **Entry conditions** | Pullback to EMA50 + bullish pattern |
| 5 | **Where the stop-loss goes** | Behind the last swing low + 5 pips |
| 6 | **Where the take-profit goes** | 2× the distance to the stop, R:R 1:2 |

**Without all 6 rules it is not a strategy — it is improvisation.**

---

## 3. Strategy Parameters

```yaml
Name: "EMA50 Pullback by Trend"
Type: Trend-following
Markets: EUR/USD, GBP/USD (majors only, low spread)
Trading hours: London + US session (12:00–22:00 UTC+3)
              Avoid Asian session (low liquidity), Friday evening

Timeframes:
  - Trend: H4
  - Entry: H1

Indicators:
  - EMA(50) on H1 — dynamic support/resistance
  - EMA(200) on H4 — main directional filter
  - RSI(14) on H1 — overheating filter

Risk Management:
  - Risk per trade: 0.5% of deposit (beginner) or 1% (experience ≥ 6 months)
  - Minimum R:R 1:2
  - Maximum 2 open trades at the same time
  - Maximum 3 losing trades in a day → stop trading for the day
  - Maximum 6% drawdown per week → pause until Monday
```

---

## 4. Long Entry Conditions

**ALL conditions must be met. If even one is not — there is NO trade.**

### Step 1. Trend Filter (H4)
- ☐ Current price is **above EMA(200) on H4**
- ☐ H4 structure shows a series of higher highs / higher lows (uptrend)
- ☐ No serious resistance on H4 within the next 50 pips above

### Step 2. Pullback on H1
- ☐ Price pulled back to EMA(50) on H1 — touching it or within 10 pips
- ☐ The pullback occurred **after a bullish impulse**, not from sideways movement

### Step 3. Candle Signal on H1
Need **at least one** bullish pattern near EMA50:
- ☐ Hammer (long lower shadow, small body at the top, any color)
- ☐ Bullish engulfing (green candle covers the body of the red one)
- ☐ Doji on EMA50 + next green candle
- ☐ Bullish pin bar

### Step 4. RSI Filter
- ☐ RSI(14) on H1 is in the **40–65** zone
  - Below 40 — structure is too weak, better to skip
  - Above 65 — already overheated, stop will be too wide

### Step 5. News Filter
- ☐ No red news on EUR or USD in the **next 2 hours**
- ☐ It is not Friday after 18:00 UTC+3

### If ALL 5 steps are ☑ — open the long.

---

## 5. Short Entry Conditions

Mirror image of the long:

### Step 1. Trend Filter (H4)
- ☐ Price is **below EMA(200) on H4**
- ☐ H4 structure shows a series of lower highs / lower lows

### Step 2. Pullback on H1
- ☐ Price rallied back up to EMA(50) on H1 from below

### Step 3. Candle Signal on H1
- ☐ Shooting star (long upper shadow)
- ☐ Bearish engulfing
- ☐ Doji + next red candle
- ☐ Bearish pin bar

### Step 4. RSI Filter
- ☐ RSI(14) in the **35–60** zone

### Step 5. News Filter
- ☐ No red news in the next 2 hours

---

## 6. Exiting a Trade

### Stop Loss

**For long:**
- Behind the last swing low (the most recent local bottom before the signal) **minus 5 pips**
- The distance from entry to stop = `Stop Distance` (in pips)

**For short:**
- Behind the last swing high plus 5 pips

> **⚠️ The stop is NOT placed "at 20 pips because it felt right."** The stop is a **technical level**; its breach means your trend hypothesis was wrong.

### Take Profit — Three Options

**Option A: Fixed R:R = 1:2 (recommended for beginners)**
```
TP = entry + 2 × Stop Distance  (for long)
TP = entry − 2 × Stop Distance  (for short)
```

**Option B: To the nearest significant resistance level (H4)**
- Use this when there is an obvious obstacle ahead
- Verify that R:R is at least 1:1.5

**Option C: Trailing stop**
- Once price moves 1R in profit — move stop to breakeven (entry price)
- Once price moves 2R — move stop below/above the last swing low/high

**Recommendation:** for your first 50 trades use **Option A only**. This gives clean data for statistics.

### Time in Trade

- If the trade has not moved in either direction for **6 hours** → close manually. The impulse has exhausted itself.
- Do not leave positions over the weekend (close by Friday 22:00 UTC+3) — Monday gap can hit your stop.

---

## 7. Position Management

### Position Size Calculation

Formula:

```
Position size (lots) = (Deposit × Risk%) / (Stop Distance × Pip value per 1 lot)
```

**Example:**
- Deposit: $1,000
- Risk: 0.5% = $5
- Stop Distance: 25 pips
- Pip value for 1 lot EUR/USD: $10

```
Size = $5 / (25 × $10) = $5 / $250 = 0.02 lots
```

Open **0.02 lots** (mini × 0.02 = micro 0.02).

**Use the calculator:** `tools/position_calculator.py` (available in this folder) — it calculates for you.

### Pip Value by Currency Pair (approximate, for USD accounts)

| Pair | Pip value per 1 lot |
|---|---|
| EUR/USD | $10 |
| GBP/USD | $10 |
| AUD/USD | $10 |
| USD/JPY | ~$6.7 (depends on rate) |
| USD/CHF | ~$11 (depends on rate) |

**For precise calculations it is better to use the calculator or the built-in terminal tool.**

### What NOT to Do

- ❌ Open more than 2 positions at the same time
- ❌ Average down a losing position ("add to it so the average price improves")
- ❌ Move the stop **further** from price to "give the trade a chance"
- ❌ Close a winning trade before TP "because I'm scared it will reverse" (if the rules say hold — hold until TP or SL)

---

## 8. Chart Illustration

A textbook example with a clear signal:

![Strategy — illustration](images/strategy-example.png)

**What we see:**

1. **Uptrend:** price moves from 1.0820 toward 1.097+, EMA50 (blue) and EMA200 (red) diverge upward — classic trend structure.
2. **Pullback to EMA50:** on candles 52–55 price pulled back to EMA50 after a bullish impulse.
3. **Bullish confirmation candle** on candle 55.
4. **Entry point:** 1.0961 (after the signal candle closes).
5. **Stop Loss:** 1.0936 (25 pips of risk, behind the last swing low).
6. **Take Profit:** 1.1011 (50 pips, R:R = 1:2).

With a 0.5% risk on a $1,000 deposit (= $5) and a 25-pip stop:
```
Position size = 5 / (25 × 10) = 0.02 lots
Potential profit = 50 × 10 × 0.02 = $10
Ratio = $5 risk / $10 profit = 1:2 ✓
```

---

## 9. Backtest and Forward Test

Before trading on demo, run the strategy through historical data.

### Manual Backtest on TradingView (free)

1. Open the EUR/USD H1 chart for the last 3 months.
2. **Wind back to the beginning of the period** (use the Replay tool).
3. Step through candles one by one. On each candle ask yourself:
   > Are all 5 strategy conditions met?
4. If yes — mark the entry (arrow), stop, and target directly on the chart.
5. Record the result in your journal.

**Goal:** at least 50 trades from 3–6 months of history.

### What to Calculate After the Backtest

| Metric | Formula | What is good |
|---|---|---|
| **Win rate** | Winners / Total | ≥ 40% |
| **Avg Win** | Total profit / Number of winners | — |
| **Avg Loss** | Total loss / Number of losers | — |
| **Profit Factor** | Total profit / Total loss | ≥ 1.5 |
| **Expectancy** | (Win Rate × Avg Win) − (Loss Rate × Avg Loss) | > 0 |
| **Max Drawdown** | Max peak-to-trough decline | < 15% of deposit |

If **Profit Factor < 1.2 or Expectancy < 0** — the strategy does not work in its current form; refine it.

### Forward Test on Demo

After a solid backtest:
- At least **30 trades on demo** in real time
- If results match the backtest → move to live trading
- If results are worse → investigate: you may be breaking your own rules in practice

---

## 10. When the Strategy Does NOT Work

**No strategy works all the time.** Any trend-following strategy performs poorly in:

### Ranging Market (Flat)
- EMA50 and EMA200 on H4 intertwine and move horizontally
- Price bounces between levels
- A series of false signals → a series of losses

**Solution:** do not trade during these periods. Sign of a flat: EMA200 on H4 has a **slope of less than 5°** for 2–3 days in a row.

### High-Impact News Days (FOMC, NFP)
- Sudden moves of 50–100 pips in a minute
- Stops knocked out by spikes
- Spreads widen 3–5×

**Solution:** do not open trades 2 hours before or after red news events. Close open positions before NFP if you have already taken profit.

### Low Liquidity
- Asian session (22:00–08:00 UTC+3) on EUR/USD
- Friday evening
- Holidays (Christmas, New Year, Thanksgiving)

**Solution:** trade only during the London–US window.

### Market Regime Change
Sometimes the market shifts "character" — for example, a trend gives way to a choppy range. If over the last 20 trades the Profit Factor has dropped below 1.0:
- Put the strategy on pause
- Re-run the backtest on fresh data
- Parameter adjustments may be needed

---

## 11. Improving the Strategy Through a Journal

**A trade journal (see `journal/`) is the most powerful growth tool you have.**

### Weekly
- Calculate win rate and profit factor for the week
- Find the **3 worst trades** — what do they have in common?
- Find the **3 best trades** — what do they have in common?

### Monthly
- Open your last 20 trades and categorize them:
  - Followed rules, profit
  - Followed rules, loss
  - Broke rules, profit (dangerous — "got lucky")
  - Broke rules, loss (the classic)
- If you see many rule violations → the problem is discipline, not the strategy

### Every 3 Months
- Review parameters: perhaps the RSI filter is too strict and is cutting good setups?
- Test changes **only on new trades** (on paper or demo)
- Do not change more than one parameter at a time

### Signs That a Strategy Is Mature

- Stable win rate ± 5% month over month
- Profit Factor consistently ≥ 1.3
- Drawdown is controlled (no "catastrophic month" at −15%)
- You can calmly skip a trade if it is not a perfect setup

---

[← Back to main guide](../forex-guide.md) · [← Technical Analysis](technical-analysis.md)
