---
widgets: [multipair]
---

# 🌍 Does the tuning carry over to other pairs

!!! abstract "The neighbouring question to overfitting"
    On the [previous page](overfitting.md) the tuning did not survive a move
    **through time**. Here the question runs along another axis: does it survive
    a move **between markets**?

    We take the parameters that came out best on EUR/USD and apply them without
    a single change to seven other pairs. Answer first — then look at the table.

<div id="multipair" data-src="../../../data/multipair.json"></div>

---

## What came out

Eight pairs, hourly candles, two years, 103 to 211 trades per pair.

| Pair | Transferred | Its own best |
|---|---|---|
| USDCAD | **+37.3R** | +37.3R |
| EURUSD *(home)* | +21.1R | +21.1R |
| GBPJPY | +20.4R | +42.1R |
| NZDUSD | +19.8R | +40.5R |
| AUDUSD | +3.4R | +14.7R |
| GBPUSD | +3.2R | +22.4R |
| USDJPY | +0.7R | +17.3R |
| EURJPY | **−30.2R** | +0.8R |

## The answer turned out subtler than expected

Honestly: I expected a collapse. It did not happen — **seven pairs out of eight
stayed positive**. The tuning carried over better than one might assume, and
that is a useful observation in itself: not everything that was fitted must
fall apart.

But the thing to look at is not the sign. It is these three.

**The spread is 67.6R.** From −30.2R on EUR/JPY to +37.3R on USD/CAD. Had you
picked the "wrong" pair, you would have lost while following the very same
rules.

**The home pair did not win.** EUR/USD, the one everything was tuned on, came
only second. So the parameters are not "sharpened for EUR/USD" — they are
simply one set among many.

**Fitting promises twice what transferring delivers.** Summed over all pairs:
transferred **+75.7R**, fitted per pair **+196.1R**. That 2.6× difference is
exactly the beautiful number shown in advertising — obtained by choosing after
the fact, which is what the [overfitting page](overfitting.md) is about.

**Six pairs out of eight prefer their own parameters.** If every pair has its
own "best", then "best" is a property of the sample, not of the strategy.

## The mistake I nearly published

The first run produced zero and four trades over two years on the JPY pairs. It
looked like a ready-made conclusion: "the strategy does not work on yen pairs."

The conclusion would have been false. The pip on JPY pairs is 0.01, not 0.0001,
and I was not passing it. The filter "price within N pips of the EMA" was
computed in units a hundred times too large and almost never triggered. After
the fix GBP/JPY produced 103 trades and **+20.4R**.

The moral is not only technical. Before explaining a weak result by properties
of the market, check whether the measurement is at fault. The test
`test_jpy_pairs_were_measured_with_their_own_pip` now fails if the pip size
becomes shared again.

## What to do about it

1. **Check a strategy on several pairs.** One pair is one sample.
2. **Do not tune parameters per pair.** It doubles the beauty of the report and
   adds nothing to the future result.
3. **Look at the worst pair, not the average one.** You do not trade the
   average; you trade a specific pair.

## Next

- [Why a backtest lies](overfitting.md) — the same trap along the time axis.
- [Skill or luck](monte-carlo.md) — a check on your own series of trades.

!!! danger "Not financial advice"
    The numbers are measured on eight pairs over one period. Over another period
    they will differ — which is the content of this page.
