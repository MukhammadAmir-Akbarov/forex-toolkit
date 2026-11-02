---
widgets: [weekly-review]
---

# 📅 The week on the market: three biggest moves

!!! abstract "What this is"
    A review of the last full week across eight pairs: who moved the most,
    how big that is **in units of the pair's own volatility (ATR)**, and on
    which day it happened. Charts and numbers are computed by a script from
    real quotes — these are measurements, not impressions.

<div id="weekly-review" data-src="../../../data/weekly-review.json"></div>

---

## How to read the review

**The move in ATR matters more than the move in pips.** −266 pips on GBP/USD
and −112 on NZD/USD sound different, but in volatility units (−2.96 and
−2.10 ATR) you can see: both pairs travelled nearly three of their “usual
days”. A move beyond 2 ATR in a week is always an event with a cause, not
noise.

**The peak day hints at where to look for the cause.** If the whole move was
made in one day — check that day's news calendar: rates, CPI, NFP. A move
spread over the week is more often trend position reshuffling than a single
release.

**Did all three go the same way?** When GBP/USD, EUR/USD and NZD/USD move
together, the story is not the pound or the kiwi — it's the dollar. The
[correlation map](market-analytics.md) helps check this: linked pairs often
make a shared move, and three “different” trades on them would be one bet.

## How to hunt for the cause

1. Open the economic calendar on the peak day (links are on the
   [data sources](../extras/market-data-sources.md) page).
2. Mark the red events for both currencies of the pair.
3. Compare with the [news trading protocol](../practice/news-trading-protocol.md):
   where the entry would have been — and whether it was worth its risk.

Fifteen minutes of this review each week is what separates “watching charts”
from understanding the market.

## Updates

The page is recomputed with one command from fresh quotes:

```bash
python tools/fetch_quotes.py && python tools/build_weekly_review.py
```

## Further reading

- [Volatility and correlations](market-analytics.md) — when pairs move and who moves together.
- [Trading sessions](../practice/trading-sessions.md) — the hours such days happen in.
- [News protocol](../practice/news-trading-protocol.md) — what to do on the peak day.

!!! danger "Not financial advice"
    A review of last week is a learning exercise, not a forecast for the next
    one. A −3 ATR move does not “have to come back” just because it was big.
