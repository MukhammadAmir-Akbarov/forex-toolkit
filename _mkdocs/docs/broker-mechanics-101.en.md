# ⚙️ Real Broker Mechanics — What Happens "Behind the Scenes"

!!! abstract "Why this matters"
    Most beginners think: "I bought EUR/USD — the market reacted." In reality, your order
    may never reach "the market" — the broker may take the other side of the trade itself.
    Understanding this explains **slippage, requotes, spread differentiation**, and helps you
    choose a broker by real conditions, not flashy advertising.

> **Educational material.** Mechanisms described are well-known industry facts, not claims
> about specific brokers.

---

## Table of Contents

1. [Two Execution Models: MM vs ECN/STP](#1-two-execution-models-mm-vs-ecnstp)
2. [Slippage: Where It Comes From and Why](#2-slippage-where-it-comes-from-and-why)
3. [Requotes — What They Are and How to Avoid Them](#3-requotes--what-they-are-and-how-to-avoid-them)
4. [Spread: Fixed vs Floating](#4-spread-fixed-vs-floating)
5. [Swap — The Cost of Holding a Position Overnight](#5-swap--the-cost-of-holding-a-position-overnight)
6. [Margin and Margin Call: The Mechanics](#6-margin-and-margin-call-the-mechanics)
7. [The Real Conflict of Interest](#7-the-real-conflict-of-interest)
8. [How to Choose a Broker by Objective Criteria](#8-how-to-choose-a-broker-by-objective-criteria)

---

## 1. Two Execution Models: MM vs ECN/STP

### Market Maker (MM) — "the Kitchen"

The broker **takes the opposite side** of your trade itself. You buy EUR/USD — broker sells.

```
You: Buy 0.1 lot EUR/USD at 1.08463
Broker internally: "accepted" the sell of 0.1 lot

What broker does with this risk:
A) Hedges with a liquidity provider (honest MM)
B) Doesn't hedge, "hoping" you lose (conflict of interest)
```

**Signs of an MM broker:**
- Fixed spread (2–3 pips on EUR/USD even at night)
- Requotes in fast markets
- Minimum deposit $10–50
- "Instant Execution"

### ECN (Electronic Communication Network)

Your order **actually goes to market** — into a liquidity pool from banks, other brokers,
institutional players.

```
You: Buy 0.1 lot EUR/USD
Broker: sends to ECN platform
ECN: finds a seller (another trader, bank, LP)
Execution: at best available price
```

**Signs of an ECN broker:**
- Floating spread (from 0.0 pip + $3–5 commission per lot)
- No requotes (always Market Execution)
- Minimum deposit $200–1000
- Transparent pricing

### STP (Straight Through Processing)

Hybrid: orders pass automatically to liquidity provider, but broker may add
**markup to spread** instead of commission.

| Criterion | Market Maker | ECN/STP |
|---|---|---|
| Execution | Instant / Requote | Market (no requotes) |
| Spread | Fixed, wider | Floating, tighter + commission |
| Conflict of interest | Possible | Minimal |
| Minimum deposit | Low ($10–100) | Higher ($200+) |
| Best for | Education, small accounts | Active trading |

---

## 2. Slippage: Where It Comes From and Why

**Slippage** — the difference between the price when you sent the order and the execution price.

### Causes:

1. **Speed**: market moves faster than your order travels (10–100 ms)
2. **Liquidity**: with large volume, not enough counterparties at one price
3. **Volatility**: during news, price jumps ticks per millisecond

```
Example of positive slippage (in your favour):
Sent Buy Market at 1.08463
Executed at 1.08459 → 0.4 pips better
(On ECN this happens when price moved IN YOUR FAVOUR while order was in transit)

Example of negative slippage (loss):
Sent Buy Market at 1.08463
Executed at 1.08481 → 1.8 pips worse
(Price jumped while order was processing)
```

### How to minimise slippage:

- Trade during **liquid hours** (London/New York, not Asian session)
- Use **Limit instead of Market** — guarantees price but not execution
- Avoid **Market during news releases**
- Check broker's average slippage in their **execution quality reports**

---

## 3. Requotes — What They Are and How to Avoid Them

**Requote** — broker rejects your price and offers a new one.

```
You click "Buy" at 1.08463
Pop-up: "Price has changed. New price: 1.08471. Accept?"
```

This is typical of **Instant Execution** at MM brokers. With Market Execution there are no
requotes — the order always executes, but at market price.

### How to avoid requotes:

1. Choose a broker with **Market Execution**
2. Don't trade **Market at news release moments**
3. Check statistics: brokers are required to publish their requote percentage

---

## 4. Spread: Fixed vs Floating

**Spread** — the difference between Ask (buy) and Bid (sell). The main "tax" of trading.

```
EUR/USD: Bid = 1.08450, Ask = 1.08453
Spread = 0.3 pip (or $0.30 per 0.1 lot)
```

### When spread widens:

| Time / Event | EUR/USD Spread |
|---|---|
| London+NY overlap (15:00–17:00 UTC) | 0.1–0.5 pip |
| Asian session | 0.5–1.5 pip |
| 5 min before/after 🔴 news | 3–50+ pip |
| Friday evening / weekends | 2–5 pip |
| Week opening (Sunday 22:00 UTC) | 5–15 pip |

### Real cost of spread

```
Strategy: 10 trades per day, 0.1 lot EUR/USD, spread = 0.5 pip
Spread cost per trade = 0.5 pip × $1 = $0.50
Per day = $0.50 × 10 = $5.00
Per month (22 days) = $110.00
```

This is the **breakeven cost on every trade** — price must move at least the spread to return to zero.

---

## 5. Swap — The Cost of Holding a Position Overnight

**Swap (Rollover)** — payment or credit for **holding a position past midnight (22:00 UTC)**.

Logic: you hold one currency and "borrowed" another. The difference in interest rates is the swap.

```
Long EUR/USD (holding EUR, borrowed USD):
EUR rate = 4.0%, USD rate = 5.5%
You receive 4.0%, pay 5.5%
Swap = negative (you pay)

Short EUR/USD (holding USD, borrowed EUR):
You receive 5.5%, pay 4.0%
Swap = positive (you receive)
```

### Triple swap on Wednesday

Forex settles on T+2 (two business days). A position held through Wednesday 22:00 carries
three days of swap (Wed + Sat + Sun). Important for scalpers.

!!! warning "Swap on exotic pairs"
    On pairs like USD/TRY, USD/ZAR, USD/BRL swaps can reach **−$10–30 per lot per day**
    for a long. Holding 10+ days creates significant losses even without price movement.

### Swap-free accounts (Islamic)

Brokers offer **swap-free** accounts (no swap) for Muslims. But usually replace swaps with
**an administrative fee** after holding 3+ days. Always check the actual conditions.

---

## 6. Margin and Margin Call: The Mechanics

**Margin** — the deposit the broker blocks when you open a position.

```
Account: $1000, leverage 1:100, open 0.1 lot EUR/USD
Position value = 10,000 EUR ≈ $10,800
Margin = $10,800 / 100 = $108 → broker blocks $108 of $1000
Free margin = $1000 − $108 = $892
```

### Margin Call vs Stop Out

| Level | What happens |
|---|---|
| **Margin Call** (~100% margin level) | Broker warns: add funds |
| **Stop Out** (~50% margin level) | Broker forcibly closes positions |

```
Example Stop Out:
Margin = $108, Stop Out at 50%
Stop Out trigger = $108 × 50% = $54 equity
If loss on position = $946 (from $1000 only $54 left)
→ Broker closes position by force
```

!!! danger "Never open a position that uses more than 10% of your account as margin"
    Rule: one position's margin ≤ 2–5% of deposit. Otherwise a few extreme moves → Stop Out.

---

## 7. The Real Conflict of Interest

### "B-book" vs "A-book"

Every broker internally divides clients:

**A-book** — profitable, experienced traders. Their orders go to the real market.
Broker earns on commission/spread.

**B-book** — the majority of retail traders. Their orders **don't go to market** — the broker
"takes" the trade itself. When you lose → broker profits.

```
Statistics: 70–80% of retail traders lose money.
For an MM broker with B-book this means:
Broker profit ≈ client losses (without going to market)
```

!!! warning "This doesn't mean MM brokers are 'cheating'"
    A regulated MM broker can't arbitrarily move prices — they show quotes from liquidity
    providers. The conflict is in **motivation**: MM benefits when you lose. ECN is
    indifferent to your outcome (earns on volume).

### How to identify an honest broker

1. **Regulation** — FCA (UK), ASIC (Australia), CySEC (Cyprus).
   No licence = offshore = risk of total loss.
2. **Execution quality reports** — FCA requires publishing slippage statistics.
3. **Segregated accounts** — client money held separately from broker funds.
4. **Independent reviews** — Trustpilot, WikiFX, trader forums.

---

## 8. How to Choose a Broker by Objective Criteria

| Criterion | Red flag | Good sign |
|---|---|---|
| Regulation | None / offshore Vanuatu/Belize | FCA, ASIC, CySEC, FSA |
| EUR/USD spread | > 2 pips during trading hours | < 0.5 pip (ECN) or < 1 pip (MM) |
| Execution | Requotes, forced spread widening | Market Execution, transparent stats |
| Deposit/withdrawal | > 3% fee, > 3 days delay | 0% fee, withdrawal within 24 hours |
| Min deposit | > $1000 without reason | $100–500 for standard |
| Support | Pushy "managers", constant calls | Neutral support |
| Bonuses | "100% deposit bonus" (often unwithdrawable) | No bonuses or transparent conditions |

!!! success "Recommendation for beginners from Uzbekistan"
    See the [Brokers for Uzbekistan](../uz/brokers-uz.en.md) page — brokers with convenient
    VISA/Mastercard UZS deposits and Telegram support are listed there.

---

*← [Fundamental analysis](fundamental-analysis-guide.en.md) · [Order types →](order-types-mechanics.en.md)*
