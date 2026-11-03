---
widgets: [seasonality]
---

# 🗓️ Currency Pair Seasonality

!!! abstract "What this is"
    A map of 8 pairs × 12 months: which months a pair has **historically**
    risen or fallen more often and more strongly. Computed by a script from
    daily candles — average move, median and share of positive years per cell.

<div id="seasonality" data-src="../../../data/seasonality.json"></div>

---

## How to read the map

**Color is the average month move in percent.** Teal — the month is positive
on average, red — negative. Click a cell to see the median, the share of
positive years and the number of years observed.

**Skip dimmed cells.** Years per month are countable, and a cell with a small
sample is noise, not a pattern. In FX, seasonality is weaker than in equities
or gas: there is no harvest or heating season here.

**Read structure, not single cells.** If AUDUSD has a strong January — check
whether NZDUSD shows the same January. Two adjacent cells with the same sign
can serve as background; a single bright cell is almost always one random year.

## How to use it (and how not to)

- ✅ **Background for a plan.** A “historically cautious month” is a reason to
  reduce risk, not a reason to “definitely short”.
- ✅ **A question for the data.** A strong cell is a reason to check which
  events those months contained (CPI, rates) — not a signal by itself.
- ❌ **No calendar entries.** An average over 5–20 years does not promise this
  month. Half of “seasonal patterns” do not survive the next decade.

## Updates

The map is recomputed with one command from fresh quotes:

```bash
python tools/fetch_quotes.py && python tools/build_seasonality.py
```

## Further reading

- [Volatility and correlations](market-analytics.md) — when pairs move within the day.
- [The week on the market](weekly-review.md) — what actually happened last week.
- [Economic calendar](../extras/market-data-sources.md) — where to find the causes of strong months.

!!! danger "Not financial advice"
    Seasonality is statistics of the past, not a schedule of the future. A
    month that rose 4 years out of 5 fell in the fifth — and this year may be
    the fifth.
