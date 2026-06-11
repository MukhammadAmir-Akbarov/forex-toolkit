# 📅 Weekly Report Template

!!! abstract "From Real Practice"
    This template comes from 2 years of practice in a professional trading community. The format has been tested across hundreds of weeks of public reporting.

    **Goal:** not to "show off your trades", but to **see your own statistics** and adjust your strategy.

---

## 📋 Report Template

Copy and fill in your journal every Sunday:

```markdown
📊 WEEKLY REPORT #__

🗓 Week: __.__-__.__.20__

---

🗓 MONDAY - __.__:
 1. PAIR buy/sell ___ pips ✅/❌  (extra info: lot, news, BU)
 2. PAIR buy/sell ___ pips ✅/❌
 3. ...

🗓 TUESDAY - __.__:
 1. ...

🗓 WEDNESDAY - __.__:
 1. ...

🗓 THURSDAY - __.__:
 1. ...

🗓 FRIDAY - __.__:
 1. ...

---

📈 WEEKLY STATS:

Total trades: ___
✅ Profitable: ___ (___ %)
❌ Losing: ___ (___ %)
⚪ Breakeven (BU): ___

📊 Win Rate: ___ %
📊 Average RR: ___
📊 Profit Factor: ___

💰 Total Win pips: +____
💰 Total Loss pips: -____
💰 Net Result: ____  pips

💵 Deposit:
 Start of week: $____
 End of week: $____
 ROI for the week: ____%

---

🎯 WEEKLY INSIGHTS:

✅ What worked:
 - ___
 - ___

❌ What did NOT work:
 - ___
 - ___

📝 Trading Plan rules I broke:
 - ___ (times/none)

📝 Next week I plan to:
 - ___
```

---

## 🎯 Example of a Completed Report (from practice)

```
📊 WEEKLY REPORT #12

🗓 Week: 17.06-21.06.2024

---

🗓 MONDAY - 17.06:
 1. XAUUSD sell -50 pips ❌ (stop, min risk)
 2. XAUUSD sell +160 pips ✅ (3x lot, add-on)
 3. XAUUSD sell +135 pips ✅

🗓 TUESDAY - 18.06:
 4. XAUUSD sell +110 pips ✅
 5. XAUUSD sell +100 pips ✅

🗓 WEDNESDAY - 19.06:
 6. XAUUSD buy +250 pips ✅ (Tp to 2350)

🗓 THURSDAY - 20.06:
 7. XAUUSD buy +180 pips ✅
 8. XAUUSD sell +50 pips ✅

🗓 FRIDAY - 21.06:
 9. XAUUSD sell +75 pips ✅
 10. XAUUSD buy -50 pips ❌ (min risk)
 11. XAUUSD sell +50 pips ✅ (5x lot)
 12. XAUUSD buy -50 pips ❌
 13. XAUUSD buy +65 pips ✅
 14. XAUUSD buy +50 pips ✅
 15. XAUUSD buy +35 pips ✅
 16. XAUUSD sell +120 pips ✅
 17. XAUUSD sell +160 pips ✅
 18. XAUUSD sell +200 pips ✅

---

📈 WEEKLY STATS:

Total trades: 18
✅ Profitable: 15 (83%)
❌ Losing: 3 (17%)

📊 Win Rate: 83%
📊 Average RR: 1.7

💰 Total Win pips: +1740
💰 Total Loss pips: -150
💰 Net Result: +1590 pips

💵 Deposit:
 Start of week: $1000
 End of week: $1240
 ROI for the week: +24%

---

🎯 WEEKLY INSIGHTS:

✅ What worked:
 - Strong gold trend on Wednesday — a long position delivered 250 pips
 - Used 5x lot ONCE when I was confident — it worked
 - Friday: after a series of stops I paused and switched to scalping — survived

❌ What did NOT work:
 - Entered too early on Monday, before London open
 - Friday: 2 stops in a row — I was emotional, ignored trend strength

📝 Trading Plan rules I broke:
 - 1 time: opened a trade without structure confirmation (second Friday trade)

📝 Next week I plan to:
 - Not enter on Monday before 13:00 UTC
 - After 2 stops in a row — pause for at least 4 hours
 - Lot size no more than 3x base (5x was on the edge)
```

---

## 📊 What to Calculate in the Stats

### Win Rate

```
Win Rate = (Number of profitable trades / Total number of trades) × 100%
```

**Breakeven (BU) trades are NOT counted as either profitable or losing.** They are neutral.

### Profit Factor

```
Profit Factor = Total profit / Total losses (in absolute terms)
```

| Profit Factor | Meaning |
|---|---|
| < 1.0 | Strategy is losing |
| 1.0 - 1.3 | Weak, on the edge |
| **1.3 - 2.0** | **Good** |
| 2.0 - 3.0 | Excellent |
| > 3.0 | Suspicious — double-check your counting |

### Average RR

```
Average RR = Average size of profitable trade / Average size of losing trade
```

For example, if on average you win 80 pips and lose 40 — your average RR = 2.0.

---

## 🔄 What to Do Every Sunday

1. **Open your journal** (`tools/journal_cli.py list` or Excel)
2. **Copy the template** above into a new file `journal/week_NN.md`
3. **Fill in all trades** from Monday through Friday
4. **Calculate the stats** (or run `tools/journal_analyzer.py`)
5. **Write down insights** — what worked, what didn't
6. **Make a plan for next week** based on the insights

!!! tip "The Sunday Report Ritual"
    Do this **at the same time** every Sunday (e.g. 18:00). This builds habit and discipline.

    Without reports you will repeat the same mistakes for 6 months without noticing them.

---

## 📈 Helper Script

The project includes a ready-made CLI for journal analysis:

```bash
# All trades for the week
.venv/bin/python tools/journal_cli.py list --since 7d

# Trade statistics
.venv/bin/python tools/journal_analyzer.py

# Monthly report in HTML
.venv/bin/python tools/journal_dashboard.py --month
```

---

## ⚠️ Common Reporting Mistakes

### ❌ "I'll remember it anyway"

After 3 months you **will not remember** why you opened that trade on Wednesday. And you'll repeat the same mistake.

### ❌ Recording only profitable trades

The most valuable data is **in losing trades**. Don't hide them.

### ❌ Not counting breakeven trades

A breakeven trade is **still work** (you found a setup, opened it, protected it, waited). Count them in the total, but not in Win Rate.

### ❌ Skipping weeks

One skipped week = a gap in your analysis. A short report — "weak week, traded little" — is better than nothing.

---

## 💬 Practitioner Quote

!!! quote
    *"Jami 24 ta signal bo'ldi, 3 tasi minus, 21 tasi plus. Sof profit +1155 pips. Muhimi bu haftaning har bir kuni foydada yopildi."*

    **Translation:** "Total 24 signals, 3 minus, 21 plus. Net profit +1155 pips. The key thing — every day of this week closed in profit."

Idea: look not only at the final result, but also at the **consistency of results**. If 1 day delivered all the profit — that is luck, not strategy.

---

## 🔗 Further Reading

- [Trading Plan template](../extras/trading-plan-template.md) — your personal plan as the foundation for reports
- [WinRate × RR calculator](../tools/winrate-rr-calculator.md) — check your math
- [Mistakes log](mistakes-log.md) — error log
- [Trading Journal template](trading-journal-template.md) — main trade journal
- [Journal Analyzer](../tools/README.md) — automated analysis
