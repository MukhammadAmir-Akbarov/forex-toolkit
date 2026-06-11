# 🛡️ Safe (Move to Breakeven) — when to move your stop to breakeven

!!! abstract "From practice (509 mentions in the archive)"
    «Seyf» (Safe) — a Uzbek-Russian term used in CIS trading circles. It means **moving the Stop Loss to the entry point** so that a loss on the position becomes impossible.

    In the archive of 2 years of practice — **509 mentions** of this technique. It is the most frequently used protective move.

---

## 🎯 What is «Safe» (Breakeven)

```
Opened BUY at 1.0850
Stop Loss: 1.0800 (50 pips risk)
Take Profit: 1.0950 (100 pips target)

Price moved up to 1.0900 (+50 pips profit)

→ Move Stop Loss from 1.0800 to 1.0850 (to the entry point)
→ Now even if price reverses — we WILL NOT LOSE

This is the «safe» — a breakeven position.
```

!!! tip "Psychological effect"
    After moving to BE you are **completely calm**. The trade can close at a small profit (at the new stop price) or reach the full TP. **A loss is impossible.**

    This removes a huge amount of stress and lets you focus on the next trades.

---

## 📐 When to move to breakeven — specific rules

### Rule 1: 50% of the distance to TP has been reached

```
Entry: 1.0850
SL: 1.0800 (50 pips risk)
TP: 1.0950 (100 pips target)

→ When price reaches 1.0900 (50% of the way to TP) — move SL to BE
```

### Rule 2: 1:1 RR level has been reached

As soon as profit equals the initial risk size (RR=1), move to BE.

```
If SL = 30 pips, move to BE after +30 pips of profit
If SL = 50 pips, move to BE after +50 pips of profit
```

### Rule 3: Price has reached the nearest resistance

If there is a **strong resistance** (for BUY) or **support** (for SELL) on the way to TP — move to BE before it. The probability of a bounce is high.

### Rule 4: Before a red news event

**15–30 minutes before an important news release** (NFP, CPI, FOMC) — always move all open positions to BE or partially close them.

---

## ⚠️ When NOT to move to breakeven

### ❌ Too early

If you move SL to BE when price has only covered 10–20% of the way to TP — **you will be stopped out on a pullback** and miss the move.

The market breathes. **Give it room to pull back.**

### ❌ In consolidation before a move

If price has moved +20 pips and then entered consolidation (flat) — do NOT move immediately. Move to BE **after the level breaks** in your direction.

### ❌ If the trade has not yet structurally proven the move

Moving to BE should happen **after** at least one HH (Higher High for BUY) or LL (Lower Low for SELL) has formed from the entry point.

---

## 🔢 The Math of the «Safe»

### Without breakeven:

```
10 trades with equal lot size
Risk: 1% per trade, RR = 1:2

Scenario: 5 wins, 5 losses
Win: +5 × 2% = +10%
Loss: -5 × 1% = -5%
Total: +5%
```

### With breakeven (applied correctly):

```
10 trades, risk 1%, RR = 1:2, BE at +50% to TP
Of 5 "wins" — 2 went to BE (reversed after safe) = +0%
Of 5 "losses" — 0 losses (some also went to BE)

3 wins × 2% = +6%
3 BE × 0% = 0%
4 losses × 1% = -4%
Total: +2%

⚠️ If you move VERY early — the result can be worse!
```

**Conclusion:** the safe reduces risk, but **can also reduce profit**. The balance must be carefully calibrated.

---

## 🎯 Safe vs Trailing Stop

| Parameter | Safe (fixed BE) | Trailing Stop (floating) |
|---|---|---|
| Complexity | ✅ Simple | ⚠️ Requires configuration |
| When triggered | After a pre-defined level | Constantly follows the price |
| Risk of noise stop-out | Low | High (if tight) |
| Best for | Scalping, news | Swing, trending moves |
| Emotional load | Low | Low |

**Recommendation for beginners:** start with the regular «Safe». Trailing — after 6+ months of practice.

---

## 📋 Checklist «Can I move to breakeven?»

Before moving SL to BE, check:

- [ ] At least 50% of the distance from entry to TP has been covered
- [ ] Price is not at a round number (1.0900, 2000.00) — bounces are frequent there
- [ ] No nearby resistance/support behind me
- [ ] More than 30 minutes until a red news event (or I am moving BE *because of* the news)
- [ ] I am not moving SL into profit (i.e. «better than BE») — only to BE
- [ ] Broker allows SL modification (no Trading Halt)

---

## 💬 Practitioner quote

!!! quote
    *«+50 пипс ✅✅ сейф киламиз - сессия алмашадиган пайтга келиб колди»*

    **Translation:** «+50 pips ✅✅ we do the safe — time for the session change has come.»

Idea: **session change (London → NY, NY → Asia) = reversal risk**. Protecting the position is mandatory.

---

## 🔗 What to read next

- [Scaling In](scaling-in.md) — the opposite technique: adding to a winning position
- [LOT Discipline](lot-discipline.md) — the foundation of everything
- [Trading Psychology](../extras/psychology.md) — why you fear moving to BE too early
- [Position Calculator](../tools/position-calculator.md) — a properly calculated position makes breakeven decisions easier
