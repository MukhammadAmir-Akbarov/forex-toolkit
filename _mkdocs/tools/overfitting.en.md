---
widgets: [overfitting]
---

# 🎣 Why a beautiful backtest promises nothing

!!! abstract "Not a slogan — a measurement"
    Below is a real sweep of 54 parameter combinations of one strategy on
    **real** EUR/USD H1 candles: 12,346 hourly bars over two years. The history
    is split by time: parameters are chosen on the first part and checked on the
    second. Exactly what a "robot" seller does — except they show you the first
    half and stay quiet about the second.

    Pick a row yourself first. Then look at what happened next.

<div id="overfitting" data-src="../../../data/overfitting.json"></div>

---

## What came out on this sample

| Question | Answer |
|---|---|
| Best combination on the past | **+29.6R** over 92 trades |
| The same one on the future | **−12.5R** over 66 trades |
| Its rank on the future | **40th out of 54** |
| Median of all combinations on the future | −7.7R |
| Correlation between past and future | **−0.09** |

The last row matters most. A correlation near zero means the result on history
tells you **nothing** about the result ahead. Not "little" — nothing, within
this sample.

The combination that looked best turned out worse than forty others. Choosing
"by the backtest" did **worse** here than choosing at random.

## An honest caveat

The median on the future is negative too: −7.7R. In this period the strategy
lost money under any parameters, not only the "best" ones. That does **not**
mean the strategy is bad, and it does not mean it is good — the period is short
and there is one pair.

The lesson of this page is different and does not depend on the period:
**tuning the parameters did not improve the outcome.** The best of the past did
not become the best of the future.

## Why this happens

Sweeping 54 combinations means tossing a coin 54 times and keeping the best
toss. It will look excellent — but looking excellent and being good are
different things.

The rule worth remembering:

> The more combinations you try, the better the winner looks and the less it
> means.

That is why "a robot with 300% on history" is not an achievement but a
description of a selection procedure. One question checks it: **how many
variants did you try before you found this one?**

## What to do about it

1. **Split the history.** Choose parameters on one part, verify on another you
   have not seen. That is what is done above.
2. **Look for stability, not for the peak.** If neighbouring parameters on the
   grid give a completely different result, you found randomness, not a pattern.
3. **Count the attempts.** One good result out of 54 tries is ordinary luck.
4. **Run the skill-or-luck check.** The project has a
   [Monte Carlo check](monte-carlo.md) for that.

## How to recompute it yourself

The quotes are not in the repository (they are large and not ours), so the set
was computed once and frozen. If you have your own CSV files:

```bash
python tools/overfit_scan.py --csv data/EURUSD_1h.csv --out _mkdocs/data/overfitting.json
```

A test holds the numbers on this page: if a recomputation changes the
conclusion, it fails instead of leaving a stale claim on the site.

## Next

- [Skill or luck](monte-carlo.md) — the same idea about randomness, applied to
  your own series of trades.
- [Why a backtest lies](../docs/strategy-details.md) — the other ways to fool
  yourself with history.
- [Pattern trainer](pattern-trainer.md) — what the shapes actually did.

!!! danger "Not financial advice"
    Every number here is measured on one pair over one period. On another
    sample they will differ — which is precisely the point of the page.
