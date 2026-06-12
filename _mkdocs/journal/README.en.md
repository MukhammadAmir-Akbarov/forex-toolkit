# Trading Journal — How to Use It

Two template formats are available:

- [`trading-journal-template.md`](trading-journal-template.md) — for keeping in Markdown (Obsidian, Notion, VSCode). Great for detailed reviews.
- [`trading-journal-template.csv`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/journal/trading-journal-template.csv) — for importing into Google Sheets / Excel. Great for statistics and charts.

## Getting Started

### Option 1: Google Sheets (recommended for beginners)

1. Open [sheets.google.com](https://sheets.google.com)
2. File → Import → Upload → select `trading-journal-template.csv`
3. Import type: "Replace sheet"
4. Add formula headers on the second tab for analytics:

```
B2: =COUNTIF(Trades!U:U,"Win")                 // number of wins
B3: =COUNTIF(Trades!U:U,"Loss")                // number of losses
B4: =B2/(B2+B3)                                // win rate
B5: =SUMIF(Trades!U:U,"Win",Trades!S:S)        // total profit
B6: =-SUMIF(Trades!U:U,"Loss",Trades!S:S)      // total losses (absolute)
B7: =B5/B6                                     // profit factor
B8: =B5+SUMIF(Trades!U:U,"Loss",Trades!S:S)    // net P&L
```

### Option 2: Markdown in Obsidian / VSCode

1. Copy `trading-journal-template.md` into your folder
2. After each trade: copy the "New Trade Template" block and fill it in
3. One file per month (`2026-05.md`, `2026-06.md`…)
4. At the end of each week — add the weekly report

### Option 3: Notion

Create a database with these fields:

| Field | Type |
|---|---|
| ID | Number |
| Date | Date |
| Pair | Select |
| Direction | Select (Long / Short) |
| Setup | Text |
| Entry / SL / TP | Number |
| Lot Size | Number |
| Risk $ | Number |
| Result $ | Number |
| R-Result | Number |
| Outcome | Select (Win / Loss / BE) |
| Rules Followed? | Checkbox |
| Emotions | Multi-select |
| Mistakes | Text |
| Takeaway | Text |
| Screenshot | Files |

## Absolutely Required Fields

The minimum for each trade:

1. **Date + time** — for time-of-day analysis
2. **Pair + direction**
3. **Entry price / SL / TP / lot**
4. **Result** (pips and $ required, R recommended)
5. **Followed the rules?** (yes/no) — the most important behavioral checkbox
6. **1–2 sentences of takeaway**

Detailed fields (emotions, screenshot, long review) are desirable but not blockers. Start with the minimum and add more as it becomes habit.

## What to Calculate Weekly

Open Google Sheets and calculate:

| Metric | What's Good |
|---|---|
| Win rate | ≥ 40% (for R:R 1:2) |
| Profit Factor | ≥ 1.5 |
| Avg Win / Avg Loss | ≥ 2.0 |
| Net P&L | > 0 |
| Max drawdown for the week | < 6% of deposit |
| % of trades following rules | ≥ 95% |

If **% following rules < 95** — the problem is **discipline**, not strategy. Fix this first.

## What to Look for in Your Analysis

After 30+ trades, open your journal and ask:

- What **time of day** are you most profitable? (e.g., morning trades = positive, evening = negative)
- Which **day of the week** is worse? (e.g., Friday = positive, Monday = negative)
- On which **pairs** do you perform better?
- Rule-based setups vs "intuitive" ones — what's the difference in results?
- In what **emotional state** do you lose money?

These insights matter more than any indicator.
