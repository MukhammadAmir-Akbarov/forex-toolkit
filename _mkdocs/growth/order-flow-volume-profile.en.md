# Order Flow and Volume Profile — Advanced Technical Analysis

> This is an **"after the basics"** level topic. Master candlesticks, EMA, RSI, and a core strategy first. Come back to this section after **6+ months** of practice, when you want to understand market depth more deeply.

## Why This Matters

Classical TA (candles, indicators) tells you **what happened to price**.
Order Flow / Volume Profile tells you **who was trading and at what volumes**.

Professional traders **watch volume** because price without volume is an illusion. A level breakout without volume is often false; a breakout with heavy volume is real.

---

## 1. Concepts

### 1.1 Order Book

The exchange shows **bids/asks at each price level** in real time:

```
                ASK (sellers)
   1.0855  ┃ 2 500 000 lots
   1.0854  ┃ 1 800 000 lots
   1.0853  ┃   500 000 lots
─── current price ────
   1.0852  ┃   400 000 lots
   1.0851  ┃ 1 200 000 lots
   1.0850  ┃ 3 000 000 lots
                BID (buyers)
```

- **Large buy wall** below current price → support
- **Large sell wall** above → resistance
- **Thin liquidity** → price will move through the level quickly

⚠️ **Important:** In forex the order book is **not available** to retail traders (it is an OTC market), unlike crypto exchanges and stock markets.

### 1.2 Volume Profile

A vertical histogram on the right side of the chart showing **how much volume traded at each price level** over a period:

```
Price │
1.090 ┃▓▓
1.088 ┃▓▓▓▓▓
1.086 ┃▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ← POC (Point of Control)
1.084 ┃▓▓▓▓▓▓▓▓▓▓
1.082 ┃▓▓▓
1.080 ┃▓
      └────────────
```

Key terms:
- **POC (Point of Control)** — the price level with the highest volume. The most "fair" price.
- **Value Area (VA)** — the range where 70% of volume traded
- **Value Area High (VAH)** — the top of the Value Area
- **Value Area Low (VAL)** — the bottom of the Value Area
- **HVN (High Volume Node)** — a zone with high volume — acts as support/resistance
- **LVN (Low Volume Node)** — a zone with low volume — price moves through it quickly

### 1.3 ICT Concepts (Inner Circle Trader)

A popular methodology (Michael Huddleston). Key ideas:

- **Liquidity** — where the stop-losses of the majority of traders are sitting (above swing highs / below swing lows)
- **Liquidity sweep** — the market takes those stops before reversing
- **Order Block** — the last candle before a strong impulse, often acts as support/resistance
- **Fair Value Gap (FVG)** — a gap between candles that the market often fills
- **Smart Money Concept (SMC)** — the theory that large players manipulate price

⚠️ **ICT is a controversial school of thought.** Many critics call it "an overly complex explanation of simple things." Study it critically.

---

## 2. Where to Get Volume Data in Forex

Because forex is decentralised, **true volume data does not exist**. Proxies are used instead:

### 2.1 Tick Volume

Each price change = 1 tick. Tick volume = the number of ticks per candle. This is an **indirect** measure of activity.

In MT5: right-click on the chart → **Volumes** → **Tick Volume**.

### 2.2 Futures Volume (More Accurate)

Real volume from the **futures market** (CME):
- **6E** — EUR/USD futures
- **6B** — GBP/USD futures
- **6J** — JPY futures

Available via CME data (paid) or TradingView (Pro subscription).

### 2.3 Data Aggregators

Services that aggregate volume from multiple brokers:
- **Volfix** (paid)
- **ATAS** (paid, aimed at prop traders)
- **Sierra Chart** (paid, more affordable)

For most retail traders — **tick volume is enough**.

---

## 3. Simple Strategies Using Volume Profile

### 3.1 POC Magnet

**Idea:** Price is "magnetised" toward the previous day's/week's POC.

```
Steps:
1. Build a Volume Profile for yesterday (D1)
2. Find the POC
3. If today's price is far from the POC — wait for a return
4. Enter near the POC after a test + candlestick pattern
```

### 3.2 Value Area Rejection

**Idea:** Price bounces off VAH / VAL.

```
Steps:
1. Find yesterday's VAH and VAL
2. If price approaches VAL from below and bounces → long
3. If price approaches VAH from above and bounces → short
4. Stop outside the VA
5. Target — POC
```

### 3.3 LVN Breakout

**Idea:** Price moves quickly through low-volume zones.

```
Steps:
1. Find LVNs (zones with thin bars)
2. If price starts moving toward an LVN — it will often pass through quickly
3. Enter in the direction of the move; target — the next HVN
4. Stop below the last swing
```

---

## 4. How to Add Volume Profile in MT5

MT5 does not have a built-in Volume Profile. Options:

### Option A: Free Indicator
1. Download from mql5.com: "Volume Profile" (free versions are available)
2. In MetaEditor: File → Open Data Folder → MQL5/Indicators
3. Place the .mq5 / .ex5 file there
4. In MT5: Refresh → drag onto the chart

### Option B: TradingView (Recommended)
1. On TradingView: Indicators → Volume Profile Visible Range
2. Free in the basic version
3. Much more visual than MT5

### Option C: ATAS / Sierra Chart
- Professional platforms
- $50–200/month
- Full Order Flow + Volume Profile + Footprint

---

## 5. Footprint Charts (Order Flow Bars)

This is an evolution of the standard candle: inside each bar you can see **how many buys and sells occurred at each level**:

```
EUR/USD H1 — Footprint:

1.0855  10 × 50       (10 buys, 50 sells — bears in control)
1.0854  120 × 80      (balanced)
1.0853  200 × 150     (bulls slightly ahead)
1.0852  50 × 300      (bears in control)
```

This reveals the **imbalance** between buyers and sellers **inside the candle**, not just its final result.

Available on: **ATAS, Sierra Chart, TradingView (Pro+)**.

---

## 6. Should You Learn This?

### ✅ Yes, if:
- You have 1+ year of successful trading using the basics
- You feel that classical indicators are giving you little edge
- You are willing to study a new system for 6+ months
- You are willing to pay $50–200/month for quality data

### ❌ No, if:
- You are a beginner (< 6 months of experience)
- Basic strategies are not yet profitable for you
- You are looking for a "secret" instead of discipline
- You are not ready to study for a long time

---

## 7. Books on Order Flow / Volume Profile

1. **"Mind Over Markets"** — Peter Steidlmayer (the creator of Market Profile)
2. **"Trading with Market Statistics"** — Tom Alexander
3. **"The Daily Trading Coach"** — Brett Steenbarger (on professional psychology)
4. **"Reading Price Charts Bar by Bar"** — Al Brooks

---

## 8. Free Resources

- **YouTube channel "AxiaFutures"** — institutional perspective
- **Volumetrica blog** — articles on volume analysis
- **r/Daytrading subreddit** — discussions by experienced traders
- **TradingView Education**

---

## 9. Realistic Expectations

Order Flow and Volume Profile are **tools**, not magic.

❌ They do NOT provide:
- "Clear entry/exit signals"
- 90% accuracy
- The ability to trade without stop-losses
- Profit on every timeframe

✅ They DO provide:
- Better understanding of market context
- Insight into liquidity dynamics
- An additional filter for classical setups
- Confidence in decision-making (after extended study)

---

## 10. Steps to Get Started

1. **Today:** install TradingView, add Volume Profile Visible Range on EUR/USD
2. **One week:** observe — where is the POC, VAH, VAL each day. Write down the levels.
3. **One month:** look for connections between those levels and price movements
4. **3 months:** try a simple strategy (e.g., POC Magnet) on a demo account
5. **6 months:** if it works — incorporate it as a **filter** within your main strategy

**Do not rush to implement.** Volume Profile should **supplement**, not replace, what is already working for you.

---

[← Back to Technical Analysis](../docs/technical-analysis.md) · [← Back to the Main Guide](../forex-guide.md)
