# Daily Routine — A Trader's Day Template

> A professional trader runs on **routines and habits**, not "genius trades". This document is your daily template.

---

## 🌅 MORNING (30 minutes before the trading session)

### Self-check
- [ ] Slept ≥ 7 hours
- [ ] Ate / drank water
- [ ] Not angry, anxious, or euphoric
- [ ] Not in a rush (not "squeezing it in between other things")

**If even one item is a no → I don't trade today.**

### Environment setup
- [ ] Quiet workspace
- [ ] Phone on "do not disturb" (or in another room)
- [ ] Social media disabled (Telegram, except signals from your own bot, Instagram, TikTok)
- [ ] Only the necessary tabs open

### Tools setup
- [ ] MT5 launched and connected to the server
- [ ] EUR/USD H1 chart + EMA50/EMA200/RSI
- [ ] H4 chart open in parallel (for trend context)
- [ ] Position calculator running in the terminal
- [ ] Journal ready (Google Sheets or Markdown)
- [ ] Printed checklist on the desk

### Morning analysis (15 minutes)

1. **News calendar** (5 min)
   ```bash
   .venv/bin/python tools/news_scraper.py --day today --high-only
   ```
   Note: when are red-impact news today → do not trade 2 hours before and after

2. **Big picture** (5 min)
   - D1 EUR/USD — what is the current trend?
   - H4 EUR/USD — HH/HL or LH/LL structure?
   - Where are the nearest D1 levels?
   - What happened overnight? (Did the Asian session produce a move?)

3. **Plan for the day** (5 min)
   - Which direction will I trade today?
   - Zones of interest (where to wait for a setup)?
   - Maximum number of trades? (1–3)
   - Which news / events to avoid?

---

## 🎯 DAY — working session (London + New York)

### London session (10:00–19:00 UTC = 15:00–24:00 UTC+5)

**Do not sit glued to the chart.** Professional approach:

#### Minute 1: check for a setup
- Open H1
- What happened in the last hour?
- Is there a setup **right now** (per the checklist)?

#### If there is NO setup
- Close MT5 for an hour
- Do something else
- Come back in an hour

#### If a setup IS present
**Walk through the checklist physically:**
```
☐ D1 / H4 trend identified
☐ H1 — pullback to EMA50
☐ Candlestick pattern present
☐ RSI not at an extreme
☐ Stop placed at a technical level
☐ R:R ≥ 1:2
☐ No red news within 2 hours
☐ I am calm
```

#### Position sizing
```bash
.venv/bin/python tools/position_calculator.py
```

#### Journal entry **BEFORE** the trade
- Date, time, pair, direction
- Entry price (planned), SL, TP, lot size
- Emotions (0–10)
- Reason for entering

#### Opening the trade in MT5
- Volume from the calculator
- SL and TP set **immediately** in the order window
- Buy / Sell by Market

#### **Step away from the computer**
- Do not watch every candle
- The trade will either hit TP or SL — you do not manage it any further
- You may check in an hour, not every 5 minutes

---

## 🚨 IF THE TRADE CLOSED IN A LOSS

### Immediately:
1. Log in the journal — **result + emotion**
2. Do not open a new trade right away
3. Minimum **30-minute pause**

### If 2 losses in a row:
- Activate [anti-tilt-protocol.md](anti-tilt-protocol.md), Level 1
- Half position size on the next trade

### If 3 losses in a row:
- **STOP FOR THE DAY.**
- Close MT5
- No "just one more try"

---

## 🏁 END OF SESSION (20:00–22:00 UTC+5)

### One hour before closing
- [ ] Do not open new trades (too late)
- [ ] Cancel pending orders that were never triggered

### If carrying a position overnight
- [ ] Is it worth holding the position overnight?
- [ ] Is the swap positive or negative?
- [ ] What news is scheduled during the Asian session?
- [ ] Decision: close or hold (accounting for the Monday gap)

### End-of-day review (15 minutes)
- [ ] Are all trades logged in the journal?
- [ ] Are emotions recorded?
- [ ] How many trades were taken?
- [ ] How many were profitable / losing?
- [ ] Did I follow all the rules? (% compliance)

---

## 🌙 EVENING (after 22:00 UTC+5)

- [ ] **Charts closed**
- [ ] MT5 minimised
- [ ] **No** trading-related Telegram channels
- [ ] **No** YouTube "how to get rich" videos

### If you feel like checking quotes
- Do not open MT5
- Do not open TradingView
- If the urge is strong → it is a **tilt symptom** — distract yourself

### Preparing for tomorrow
- [ ] Check tomorrow's news calendar
- [ ] Think about what you took away from today (one sentence)
- [ ] In bed before 23:00

---

## 🗓️ WEEKLY ROUTINE

### Monday
- Morning: review last week's results (15 min)
- Start of the trading week — **be cautious**, the market can gap from the weekend
- **Don't rush** for the first trade — better to skip it

### Wednesday (mid-week)
- Mini-review: how is the week going?
- If in the red — halve your position size for the rest of the week

### Friday
- **Do not open new trades after 18:00 UTC+5**
- Close open positions by 22:00 (avoid the Monday gap)
- Wrap up the week

### Saturday
- **No trading.** The forex market is closed.
- Run `tools/journal_dashboard.py` — weekly report
- Analyse the week's mistakes
- One hour of reading (a book on trading or psychology)

### Sunday
- **Full day off from trading.**
- Family, rest, sport
- Mentally prepare for Monday

---

## 🗓️ MONTHLY ROUTINE

### First Saturday of the month
- Run `journal/monthly_report.py --month YYYY-MM`
- Deep analysis:
  - Win rate for the month
  - PF for the month
  - 3 worst trades — what do they have in common?
  - 3 best trades — what do they have in common?
  - % of trades taken by the rules
- **Update** mistakes-log.md
- Decide: am I changing anything in the strategy?

### Last day of the month
- Financial accounting: deposits, withdrawals, total P&L
- If money was withdrawn — save the documents
- Think about taxes (if it is end of quarter)

---

## 🗓️ QUARTERLY ROUTINE

Every 3 months:
- [ ] Re-read the Trading Plan
- [ ] Update the plan version (if changes were made)
- [ ] Read one new book on trading / psychology
- [ ] Full strategy review: is it still working?
- [ ] If the deposit has grown by 50%+ — discuss with yourself whether to increase position size

---

## ⛔ WHAT NOT TO DO EVERY DAY

- Do not open trades without the checklist
- Do not sit at the chart for more than 2 hours straight
- Do not trade after a few drinks
- Do not trade in the first hour after serious stress (an argument, bad news)
- Do not open the terminal on weekends "just to take a look"
- Do not follow other people's trades on Telegram
- Do not compare your results to others (YouTube "gurus")

---

## 🎯 ONE KEY IDEA

> **Do less — not more. But do it well.**
>
> One good setup a day > five "average" ones.
> One hour of deep analysis > 5 hours of watching the chart.
> One trade by the plan > ten "let's see what happens".

Trading is a **marathon**, not a sprint. Routine beats talent.

---

## 📋 "I am ready for the trading day" checklist

Check this every morning:

```
☐ Slept ≥ 7 hours
☐ Had something to eat
☐ Calm
☐ Checklist on the desk
☐ Calculator open
☐ Journal ready
☐ News calendar checked
☐ Telegram signals (if any) checked
☐ I know my maximum number of trades for today
☐ Ready to stop after 3 losses
```

**All ☑ → ready to trade. Even one ☐ → rest day.**

---

[← Back to the main guide](../forex-guide.md) · [Anti-Tilt →](anti-tilt-protocol.md)
