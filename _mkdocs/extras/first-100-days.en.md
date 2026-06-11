# First 100 Days — Day by Day

> A concrete step-by-step plan for 100 days (~3 months) of learning. The goal is **not to make money**, but to **lay the groundwork**. After 100 days you will be ready for your first real account with minimal risk.

---

## 🌱 Week 1: Core Theory

### Day 1
- [ ] Read `КАК-ПОЛЬЗОВАТЬСЯ.md`
- [ ] Read sections 1–3 of the main guide (forex-guide.md)
- [ ] **Do not trade.** Read only.

### Day 2
- [ ] Sections 4–6 of the main guide (broker, platforms, demo)
- [ ] Read `extras/brokers-comparison.md`

### Day 3
- [ ] Section 7 — **RISK MANAGEMENT** (re-read **3 times**)
- [ ] Study the mathematics of ruin

### Day 4
- [ ] Sections 8–9 — analysis + strategy
- [ ] **Don't try to memorise everything** — just read to know what exists

### Day 5
- [ ] Sections 10–14 (mistakes, legal, resources, final)
- [ ] Read `extras/faq.md`

### Day 6
- [ ] Read `extras/psychology.md` in full
- [ ] Reflect: which psychological traps already exist in my character?

### Day 7 (rest day)
- [ ] Take a break. Think honestly: do I really want to trade?
- [ ] If YES — continue from next week

---

## 🛠️ Week 2: Infrastructure Setup

### Day 8
- [ ] Choose **one broker** from the top 5 (via `brokers-comparison.md`)
- [ ] Verify the licence on the regulator's website
- [ ] Read reviews from the last 6 months

### Day 9
- [ ] Open a **demo account** with the chosen broker
- [ ] Download MT5
- [ ] Follow `advanced/SETUP-mt5.md` — installation and first login

### Day 10
- [ ] Set up the EUR/USD H1 chart
- [ ] Add EMA 50, EMA 200, RSI(14)
- [ ] Save the template
- [ ] **Do not trade.** Just watch the chart for 1 hour.

### Day 11
- [ ] Open Google Sheets
- [ ] Import `journal/trading-journal-template.csv`
- [ ] Set up statistics formulas
- [ ] Read `journal/README.md`

### Day 12
- [ ] Print `extras/checklist-printable.md`
- [ ] Fill in `extras/trading-plan-template.md` **completely**, skipping nothing
- [ ] Print and sign it

### Day 13
- [ ] Run `tools/position_calculator.py`
- [ ] Practice: "with $1000 and 0.5% risk, how many lots on EUR/USD with a 25-pip stop?"

### Day 14 (rest day)
- [ ] Re-read your Trading Plan
- [ ] Install Anki, import `extras/anki-cards.csv`

---

## 📚 Weeks 3–4: Learning Technical Analysis

### Days 15–21
- [ ] Read `docs/technical-analysis.md` in full
- [ ] Study charts **carefully**
- [ ] Do Anki cards every day for 15 minutes

### Day 22
- [ ] Read `docs/strategy-details.md`
- [ ] Write the strategy rules **by hand** on paper

### Days 23–28
- [ ] **Manual backtest** on TradingView (Replay)
- [ ] Open EUR/USD H1 for the last 2 months
- [ ] Find **20 setups** according to the strategy
- [ ] For each one — log in the journal: entry, SL, TP, result
- [ ] **Do not trade on demo** — backtest only

---

## 🎯 Weeks 5–8: First Demo Trades

### Day 29
- [ ] **First demo trade**
- [ ] Size: 0.01 lot (minimum)
- [ ] Checklist physically in front of you
- [ ] Calculator open, position sized
- [ ] Journal ready

### Days 30–50 (3 weeks)
**Every day:**
1. Launch MT5
2. Review H4 and H1 on EUR/USD
3. Check the Forex Factory calendar (`tools/news_scraper.py`)
4. If there is a setup → **checklist** → calculator → trade
5. If there is none — **do not trade**
6. After each closed trade — journal entry
7. End of day — brief review: what went well, what went poorly

**Limits:**
- Maximum 3 trades per day
- Maximum 2 open simultaneously
- 3 consecutive losses → stop for the day

### Goal by end of Week 8
- ✅ 30+ trades in the journal
- ✅ Discipline — checklist every time
- ✅ Win rate understood (even if low — that is normal for a start)

---

## 📊 Week 9: First Analysis

### Days 51–57
- [ ] **No trading this week.** Analysis only.
- [ ] Run `tools/journal_dashboard.py` — review metrics
- [ ] Open `journal/mistakes-log.md` — write out **5 main mistakes**
- [ ] For each mistake — a **systemic solution** (not "I'll try harder")
- [ ] Re-read `extras/psychology.md` — which patterns do I recognise in myself?

### If win rate < 30% and PF < 0.8
- **The problem is discipline or setups.** Not the strategy.
- Re-read `docs/strategy-details.md`
- Go through `extras/checklist-printable.md` point by point — where did I cheat?

### If win rate 30–40%, PF 0.8–1.2
- **Normal** for a beginner
- Keep going — discipline matters more than results

### If win rate 40%+, PF 1.5+
- **Excellent.** But don't rush to go live
- Confirm another month on demo

---

## 🔁 Weeks 10–12: Second Trade Cycle

### Days 58–84
- [ ] Another **30+ trades** on demo
- [ ] Apply conclusions from the analysis
- [ ] Journal — every trade
- [ ] Once a week — mini-review (10 minutes)

**Signs of progress:**
- ✅ Fewer checklist violations
- ✅ More consistent win rate
- ✅ Fewer manual closes against the plan
- ✅ Journal filled in **before** opening the trade (planning), not after

---

## 🎓 Week 13: Final Analysis + Expansion

### Days 85–91
- [ ] Run `journal/monthly_report.py` — review the report
- [ ] Compare with the first 30 trades — is there progress?
- [ ] Read `journal/demo-vs-real-comparison.md` (preparing for live)

### Days 92–95
- [ ] Run `bot/backtest.py --csv data/EURUSD_1h.csv` — review backtest on real data
- [ ] **Compare** with my results — better or worse?
- [ ] If worse than the backtest — why?

### Days 96–99
- [ ] Re-read `extras/trading-plan-template.md`
- [ ] **Update the plan** based on 3 months of experience
- [ ] If profitable on demo — choose a broker for a live account

---

## 🚀 Day 100 — The Decision

### Decision A: NOT ready for live
**Signs:**
- Win rate < 40%
- PF < 1.5
- Rule-violation rate > 5%
- Emotions are destabilising

**What to do:**
- ❌ Do not go live. That is completely normal.
- ✅ Another **3 months on demo**
- ✅ Focus on one specific problem
- ✅ Consider a mentor (paid, verified)

### Decision B: Ready for live
**Signs:**
- Win rate ≥ 40% over 60+ trades
- PF ≥ 1.5
- Rule-compliance rate ≥ 95%
- Calm psychology
- Trading Plan filled in and signed

**What to do:**
- ✅ Open a **cent account** or mini deposit of **$100–300**
- ✅ First live month — **half risk** (0.25%)
- ✅ EUR/USD only, H1 only
- ✅ Maximum 1–2 trades per day
- ✅ Journal — mandatory

---

## 🎯 What Must NOT Happen in 100 Days

- ❌ Blowing the deposit (on demo, a "blow-up" means losing > 30%)
- ❌ Desire to switch to lower timeframes
- ❌ Attempting to trade your "own" strategy without rules
- ❌ Buying paid signals
- ❌ Opening a live account before Day 100

---

## 📈 What MUST Happen

- ✅ ~60 trades in the journal
- ✅ Understanding of your typical mistakes
- ✅ Developed discipline (checklist is a reflex)
- ✅ Signed Trading Plan
- ✅ Calm relationship with losses
- ✅ Foundation knowledge (glossary terms feel natural)

---

## Final Thoughts

100 days is the **minimum**. Most professionals will say: "at least a year and a half."

If after 100 days you are NOT ready to go live — **that is normal and correct**. It is better to spend another 100 days than to blow your deposit in a week because you rushed.

**The main victory of the first 100 days:** you **preserved your ability to learn**. You did not quit after the first losing streak on demo. You did not chase losses. You did not buy signals.

Discipline beats intuition. Patience beats haste. Journal beats memory.

---

[← Back to the main guide](../forex-guide.md) · [Trading Plan →](trading-plan-template.md)
