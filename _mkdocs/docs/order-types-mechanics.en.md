# 📋 Order Types and Trade Entry Mechanics

!!! abstract "Why this matters"
    Beginners often confuse Market and Limit orders, don't understand the difference between
    Stop-Loss and Stop-Limit, and open positions "however it happens." This page covers
    **all order types**, their logic, common mistakes, and examples in MT5 and TradingView.

> **Educational material.** Price examples are synthetic, for illustrative purposes only.

---

## Table of Contents

1. [Market Order](#1-market-order)
2. [Limit Order](#2-limit-order)
3. [Stop Order](#3-stop-order)
4. [Pending Orders in MT5](#4-pending-orders-in-mt5)
5. [Trailing Stop](#5-trailing-stop)
6. [Common Order Placement Mistakes](#6-common-order-placement-mistakes)
7. [Choosing Order Type: Quick Reference](#7-choosing-order-type-quick-reference)

---

## 1. Market Order

**Buy/sell immediately at the current price** — more precisely, at the best available price
at the time of execution.

```
Current EUR/USD price: Bid 1.08450 / Ask 1.08463
Open BUY Market → execution at Ask = 1.08463
Open SELL Market → execution at Bid = 1.08450
```

!!! warning "Slippage"
    In a fast market (news, session open) the price can **move** while the order travels
    to the broker. You send the order at 1.08463, you get filled at 1.08471.
    This is normal on an ECN broker. A market-maker broker may requote instead.

**When to use:**
- You need **immediate** entry with no waiting
- Trading on lower timeframes where waiting is not an option
- Small volume, sufficient liquidity available

**When NOT to use:**
- Within 30 minutes before/after major news (NFP, FOMC)
- On exotic pairs with wide spreads
- When price has already moved past your entry point

---

## 2. Limit Order

**Enter at no worse than the specified price** — the order sits in the book waiting for the
market to come to you.

```
EUR/USD now: 1.08463
Place Buy Limit at 1.08300 — triggers only if price FALLS to 1.08300
Place Sell Limit at 1.08600 — triggers only if price RISES to 1.08600
```

**Logic:** you wait for price to return to a level you consider favorable.

!!! success "Main advantage"
    You **know your entry price exactly** — execution is no worse than your limit (often
    exactly at it or better on ECN). No risk of slippage in the losing direction.

!!! danger "Trap: a limit that won't fill"
    If price "touched" your level but reversed 1–2 pips short — the order **won't fill**.
    That's normal — the market doesn't owe you a fill.
    Mistake: placing a limit too close to the current price — it may act like a pseudo-market
    order, filling on any tick.

**When to use:**
- Pullback entry to a level
- Trading from support/resistance
- You want a **better price** and are willing to wait

---

## 3. Stop Order

**Enter/exit when price breaks through a level** — triggered "with the market" when reached.

### Buy Stop
```
EUR/USD now: 1.08463
Place Buy Stop at 1.08600 → fires as Market BUY when price RISES to 1.08600
Logic: buying the breakout upward, expecting continuation
```

### Sell Stop
```
Place Sell Stop at 1.08300 → fires as Market SELL when price FALLS to 1.08300
Logic: selling the downward breakout
```

!!! warning "Stop order on the spread"
    If you place a Sell Stop at a support level, note: the **Ask** reaches the level before
    the **Bid**. Example: level at 1.08300, spread 1.3 pips.
    - Bid = 1.08300 → order triggers
    - But Ask at that moment = 1.08313 — position already "underwater" by the spread + possible slippage

### Stop-Loss and Take-Profit

These are **protective orders** on an open position:

| Order | Type | What it does |
|---|---|---|
| **Stop-Loss (SL)** | Stop | Closes position at N pips loss |
| **Take-Profit (TP)** | Limit | Closes position at N pips profit |

```
Opened BUY EUR/USD at 1.08463
SL = 1.08363 (risk 10 pips)
TP = 1.08663 (target 20 pips, RR = 1:2)
```

!!! danger "Never trade without SL"
    The market can move against you hundreds of pips. Without a stop-loss, one losing day
    can wipe out weeks of gains.

---

## 4. Pending Orders in MT5

MT5 offers 6 types of pending orders:

| Type | What it does | When to use |
|---|---|---|
| **Buy Limit** | Buy below current price | Entry on dip |
| **Sell Limit** | Sell above current price | Entry on rally |
| **Buy Stop** | Buy above current price | Buying upside breakout |
| **Sell Stop** | Sell below current price | Selling downside breakout |
| **Buy Stop Limit** | Buy Limit activated when price breaks up | Delayed entry on pullback after breakout |
| **Sell Stop Limit** | Sell Limit activated when price breaks down | Delayed entry on pullback after breakdown |

### Buy Stop Limit — Advanced Tool

```
EUR/USD now: 1.08463
Place Buy Stop Limit: Stop = 1.08600, Limit = 1.08560

What happens:
1. Price rises to 1.08600 → a limit buy order is activated
2. Order now waits for pullback to 1.08560
3. If price keeps going higher without pulling back — order doesn't fill
```

Idea: enter a breakout but at a **better price** on the pullback.

### How to Place Orders in MT5

```
Right-click on chart → "Trading" → "New Order"
Or press F9 (fast)
Select type: Market Execution / Pending Order
Fill in: volume (lots), price, SL, TP, expiration
```

!!! tip "Order expiration"
    By default a pending order persists **indefinitely** (GTC — Good Till Cancelled).
    You can set a date/time expiry. Tip: before weekends or major news,
    **cancel unfilled orders** — price may gap right into your entry.

---

## 5. Trailing Stop

**Automatically moves Stop-Loss with the price**, locking in profit.

```
Opened BUY EUR/USD at 1.08463, SL = 1.08363 (−10 pips)
Set Trailing Stop = 20 pips

Price moves up:
→ 1.08500: SL stays at 1.08363 (distance not yet reached)
→ 1.08663: SL moves automatically to 1.08463 (breakeven!)
→ 1.08763: SL = 1.08563 (locking in 10 pips profit)
→ Price reverses to 1.08720: SL triggers at 1.08563 — close at +10 pips
```

!!! warning "Trailing stop traps"
    1. **Works only while MT5 is open** — this is a local function, not a server order.
       If you close MT5, trailing stops stop.
    2. **Triggers on Bid/Ask ticks** — in ranging markets or on noise, often knocked out.
    3. Don't use on highly volatile pairs (JPY cross in Asian session) with small step.

**Alternative:** manually moving SL to key levels — more reliable but requires discipline.

---

## 6. Common Order Placement Mistakes

### ❌ Mistake 1: "Enter market because price already moved"

```
You wanted to buy EUR/USD at 1.08300 (pullback to support).
Price bounced to 1.08550, you "missed" it.
You open Market Buy at 1.08550 — chasing price.
```

Better: **skip the entry** or place a limit for the next possible pullback.

### ❌ Mistake 2: Stop too close to price

```
EUR/USD: 1.08463, average hourly move (ATR H1) = 15 pips
You place SL = 1.08443 (only 2 pips!) — market noise will hit it for certain
```

Rule: **SL ≥ ATR of current timeframe** over the last 14 candles (check ATR indicator in MT5).

### ❌ Mistake 3: Limit order ignoring spread

```
Want to enter BUY at support 1.08300
Place Buy Limit at 1.08300
On ECN spread can be 2-3 pips during Asian session
Actual entry = 1.08300 + 0.00003 = 1.08303 (minor impact)
But if you want entry at EXACT level — place Limit slightly below
```

### ❌ Mistake 4: Holding a losing position without SL "hoping"

This is called a "mental stop" — and it is **not a stop**. The market doesn't know where
you entered, and won't come back to save you.

### ❌ Mistake 5: TP right on resistance level

```
Opened BUY, TP is exactly at strong resistance 1.09000.
Reality: price often falls "short" by 2–5 pips of a round level.
```

Tip: place TP **3–5 pips below** the nearest resistance (for longs).

---

## 7. Choosing Order Type: Quick Reference

| Situation | Recommended Order |
|---|---|
| "I want to enter now" | Market |
| "Waiting for pullback to level" | Limit (Buy Limit or Sell Limit) |
| "Trading level breakout" | Stop (Buy Stop or Sell Stop) |
| "Trading breakout, want better fill" | Stop Limit |
| "Want to auto-lock profit" | Trailing Stop (while MT5 open) |
| "Want to exit at a specific target" | Take-Profit (Limit) |
| "Want to limit loss" | Stop-Loss (mandatory!) |

---

!!! tip "TradingView vs MT5"
    In **TradingView** (Paper Trading / real accounts via brokers) the interface differs:
    orders are placed directly on the chart via drag-and-drop, or through the Order panel
    on the right. The logic is the same — Market / Limit / Stop / Stop-Limit.
    For real trading a connected broker account is required.

---

*← [Technical analysis](technical-analysis.en.md) · [Market structure →](../practice/market-structure.en.md)*
