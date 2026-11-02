---
widgets: [market-analytics]
---

# 📊 When the market moves and what moves together

!!! abstract "Two questions to settle before the trade"
    **When should you sit down to trade?** Not "when it's convenient" — when
    price actually moves. Otherwise you sit through a flat market and invent
    trades out of boredom.

    **How many positions do I really have open?** Three trades on three
    different pairs can turn out to be a single bet repeated three times.

    Both maps are computed from hourly candles of eight pairs over two
    years — these are measurements, not opinions.

<div id="market-analytics" data-src="../../../data/market-analytics.json"></div>

---

## What the first map shows

**All eight pairs peak at the same hour: 14:00 UTC (19:00 in Tashkent).**
That is the London–New York overlap: the two largest markets are open at
once, and the average hourly candle covers two to three times more ground
than at night. The full session schedule is on the
[Trading sessions](../practice/trading-sessions.md) page.

**Yen pairs move twice as far.** GBP/JPY covers 48 pips per candle at the
peak, versus 20 for EUR/USD. The same stop in pips on a yen pair is a much
smaller stop in price terms — and ordinary noise takes it out. Position
size is derived from the stop, so the
[position calculator](position-calculator.md) is not a formality here.

**The night (22:00–06:00 UTC) is quiet across the board.** Not "bad" —
just a fact: breakout strategies trading those hours are fighting the
sample itself.

## What the second map shows

**AUD/USD and NZD/USD move together at 0.87. EUR/JPY and GBP/JPY — at 0.87.**
A 0.87 correlation means: opening both pairs is not two positions but one
position with double the lot. If each trade risks 1%, the real risk on that
one idea is nearly 2%.

**Negative correlations with CAD (down to −0.67).** Being long AUD/USD and
USDCAD at the same time partly cancels itself out: profit on one leg shows
up as a loss on the other, while spread and swap are paid on both.

The total risk across all open trades, counting shared currencies, is what
the [exposure calculator](risk-exposure-calculator.md) computes — that is
exactly its job.

## What to do with this

1. **Trade your strategy's hours.** Breakout systems belong to the session
   overlap; pullback systems can live in the quiet hours. The map shows
   which is which.
2. **Count correlated positions as one.** EUR/USD + GBP/USD (0.79) is not
   diversification — it is doubling up.
3. **Re-check the map every six months.** The data is recomputed from fresh
   quotes by a script — the matrix drifts, and that is normal.

## Further reading

- [Trading sessions](../practice/trading-sessions.md) — the schedule and the mechanics of the overlaps.
- [Portfolio exposure](risk-exposure-calculator.md) — how much risk is already open.
- [Transfer between pairs](multipair.md) — why "one setup for everything" fails.

!!! danger "Not financial advice"
    Correlations and volatility are statistics for a specific period
    (May 2024 → May 2026). Around crises and rate shifts the matrix
    changes: pairs that moved together can drift apart. This is a map of
    the terrain, not a weather forecast.
