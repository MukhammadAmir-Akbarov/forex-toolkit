# 📡 News Trading — Safe Entry Protocol

!!! abstract "Why this matters"
    News events are the **most dangerous moments** for position traders and the **best moments**
    for momentum traders. The difference between a loss and a profit is a **protocol**: knowing
    WHAT to trade, HOW to trade, and WHEN not to trade at all.

!!! danger "Risk warning"
    News trading involves **extreme volatility**, spread widening, slippage, and gaps.
    Beginners are advised **NOT to trade** within 30 minutes before/after major releases
    until accumulating 3+ months of demo account experience.

---

## Table of Contents

1. [Why News Is So Dangerous for Markets](#1-why-news-is-so-dangerous-for-markets)
2. [Economic Calendar — How to Read It](#2-economic-calendar--how-to-read-it)
3. [Key Events — Importance Hierarchy](#3-key-events--importance-hierarchy)
4. [Safe News Trading Strategies](#4-safe-news-trading-strategies)
5. [NFP (Non-Farm Payrolls) Tactics](#5-nfp-non-farm-payrolls-tactics)
6. [FOMC (Fed Meeting) Tactics](#6-fomc-fed-meeting-tactics)
7. [Stop-Loss in News Trading](#7-stop-loss-in-news-trading)
8. [Pre-Entry Checklist](#8-pre-entry-checklist)

---

## 1. Why News Is So Dangerous for Markets

When key data is released, the following happens:

1. **Algorithmic traders** (HFT bots) read data in **milliseconds** and reprice quotes instantly
2. **Spread widens** — on some pairs from 0.5 pips to 20–50 pips at release moment
3. **Liquidity disappears** — brokers pull orders from the book to avoid being on the "wrong"
   side of the trade
4. **Slippage** — Market orders execute 5–30 pips worse than expected

```
Example: NFP comes in much stronger than forecast
Before release: EUR/USD bid/ask = 1.08450 / 1.08453 (0.3 pip spread)
Release moment: spread widens to 1.07900 / 1.09000 (!!!!)
2–3 seconds later: 1.07980 / 1.07990 — market "found" new price
```

If you had a Sell-stop at 1.08100 — it executes at 1.07920 (18 pip slippage).

---

## 2. Economic Calendar — How to Read It

Main sources (free, with history and forecasts):
- **Forex Factory** (forexfactory.com) — industry standard
- **Investing.com** — with country filters
- **Dailyfx.com** — with analysis

### Forex Factory color meanings:

| Color | Importance | What to do |
|---|---|---|
| 🔴 Red | High — market can move 50–300+ pips | **Close positions** or don't enter |
| 🟠 Orange | Medium — 10–50 pip move | Caution, reduce size |
| 🟡 Yellow | Low — less than 10 pips | Usually can be ignored |

### Three numbers in the calendar:

```
Event: Non-Farm Payrolls (NFP)
Previous: 175K  ← last month's number (may be revised)
Forecast:  180K  ← analyst consensus
Actual:    220K  ← real value (appears at release time)
```

**Market reaction logic:**
- Actual >> Forecast → **positive surprise** → country's currency strengthens
- Actual << Forecast → **negative surprise** → country's currency weakens
- Actual ≈ Forecast → weak reaction or "sell the news"

!!! warning "'Buy the rumor, sell the news'"
    The market has often **already priced in** expected data. If NFP comes in exactly at
    forecast — there may be no reaction, or it may reverse (profit-taking).

---

## 3. Key Events — Importance Hierarchy

### Level 1 (🔴🔴🔴 — always close positions)

| Event | Currency | Frequency | Expected move |
|---|---|---|---|
| **NFP** (Non-Farm Payrolls) | USD | 1st Friday of month | 80–200 pips |
| **FOMC Interest Rate Decision** | USD | 8× per year | 100–300 pips |
| **FOMC Press Conference** | USD | 8× per year | 50–150 pips |
| **ECB Rate Decision** | EUR | 8× per year | 80–200 pips |
| **BoE Rate Decision** | GBP | 8× per year | 80–200 pips |
| **US CPI** (inflation) | USD | Monthly | 50–150 pips |
| **US GDP** | USD | Quarterly | 30–100 pips |

### Level 2 (🟠🟠 — caution)

- PMI Manufacturing & Services (EUR, USD, GBP)
- Retail Sales (USD, EUR)
- Consumer Confidence (USD)
- Jobless Claims (USD, weekly)

### Level 3 (🟡 — can be ignored)

- Building Permits, Factory Orders and other "secondary" US data

---

## 4. Safe News Trading Strategies

### Strategy A: "Wait for the dust to settle" (recommended for beginners)

```
1. News released at 13:30 UTC
2. Wait 5–15 minutes (spread normalizes, noise settles)
3. Look at the DIRECTION of the impulse
4. Enter in the direction of the impulse on a pullback (Limit order)
5. SL — behind the opposite extreme of the first 5 minutes
```

Advantage: less slippage risk, trading the fact rather than the forecast.

### Strategy B: Straddle before the news

```
1. 30 minutes before release, market forms a range (consolidation)
2. Place Buy Stop ABOVE the range + Sell Stop BELOW the range
3. Price breaks in any direction — one order triggers
4. Cancel the other order manually or use OCA (One Cancels All)
```

!!! warning "Straddle risk"
    If both orders trigger (first one direction, then reversal) — loss × 2.
    **Always set SL** for each order. Don't use on pairs with wide spreads.

### Strategy C: Positional trading on the central bank cycle (advanced)

If the Fed has been raising rates for several months → upward USD trend is sustained.
No need to trade every meeting — just trade **in the direction of the rate trend**.

---

## 5. NFP (Non-Farm Payrolls) Tactics

NFP is the most important monthly US report. Released **first Friday of each month at 13:30 UTC**.

### EUR/USD behavior around NFP:

```
30 min before: sideways, low volume, spread starts widening
At release: 50–200 pip move in 1–3 seconds
1–5 min after: reversal of 30–50% of initial move (shakeout)
15–30 min after: real direction of the day forms
```

### NFP Protocol:

1. **13:00 UTC** — check open positions. If any — close or set tight SL.
2. **13:25 UTC** — don't open new positions. Spread already widening.
3. **13:30 UTC** — DO NOTHING. Watch the data.
4. **13:32–13:35 UTC** — wait for the "first shakeout" (false move in opposite direction).
5. **13:35–13:45 UTC** — enter in the direction of the **second** move with Limit order on pullback.
6. **SL** — below/above the low/high of the first 10 minutes post-release.
7. **TP** — 1.5–2× the SL (min RR 1:1.5).

!!! success "Successful NFP example"
    ```
    NFP: actual 250K vs forecast 180K (strong USD positive)
    EUR/USD drops from 1.0850 to 1.0790 in 10 seconds
    Pullback to 1.0810 (shakeout up)
    Enter Sell Limit at 1.0808
    SL = 1.0845 (above shakeout high), TP = 1.0752
    Risk 37 pips, target 56 pips (RR ≈ 1:1.5)
    ```

---

## 6. FOMC (Fed Meeting) Tactics

FOMC — **8 times per year**, usually Wednesday. Decision at 18:00 UTC, press conference at 18:30 UTC.

### Three reaction scenarios:

| Scenario | What happened | USD reaction |
|---|---|---|
| **Hawkish Surprise** | Rate hiked more than expected or rhetoric is hawkish | USD strengthens |
| **Dovish Surprise** | Rate cut or hints at future cuts | USD weakens |
| **As Expected** | Rate and rhetoric exactly per forecast | USD neutral or "sell the news" |

### Press conference nuance:

First reaction (18:00 UTC) — to the **rate decision itself**.
Second reaction (18:30 UTC+) — to **the Chair's words** (Powell).

Sometimes they go in **opposite directions**: rate held (neutral), but Powell said "ready to cut"
→ USD falls.

!!! tip "How to trade FOMC"
    No need to trade at 18:00. Best time — **20–30 minutes after the press conference**,
    when the market has processed the information. Spread normalized, direction visible.

---

## 7. Stop-Loss in News Trading

Widened spread = **your SL can trigger before price reaches it**.

```
SL set at 1.0810 (20 pips from entry 1.0830 Sell)
At news moment Ask reaches 1.0812 (while Bid = 1.0806)
SL by Ask = 1.0812 → triggers
Actual move: price fell to 1.0760 — but you're already out
```

### SL rules for news:

1. **Increase SL** before news by at least 1.5× normal
2. **Never place SL exactly on a level** — always behind it (+3–5 pip buffer)
3. **OCO (One Cancels Other)** — if placing both sides, both need SL
4. **Don't expect "good" fills** — with wide spread, accept reality

---

## 8. Pre-Entry Checklist

- [ ] Have I checked the economic calendar for the next 4 hours?
- [ ] Have I closed open positions or moved stops further away?
- [ ] Do I know the forecast and what "good" and "bad" numbers look like?
- [ ] Am I waiting 5–15 minutes after the release before entering?
- [ ] Does my SL account for wider spread (+30–50% of normal)?
- [ ] Is position size reduced (max 0.5% of account per trade)?
- [ ] Do I have a plan "B" if price goes the other way?

!!! quote "Experienced trader's rule"
    *"You don't have to trade every news event. The best trade is the one you skipped,
    rather than the one that emptied your account."*

---

*← [Trading sessions](trading-sessions.en.md) · [Technical analysis →](../docs/technical-analysis.en.md)*
