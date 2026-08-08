---
widgets: [pattern-trainer]
---

# 🕯️ Candlestick pattern trainer — and what the patterns actually did

!!! abstract "What makes this trainer different"
    A usual pattern trainer checks one thing: did you recognise the shape. This
    one checks the same, and then **immediately shows how those shapes
    resolved** on the very same archive candles.

    That matters more than the recognition. The handbook says plainly: never
    trade on a pattern alone. A trainer that praises recognition and stays
    quiet about the outcome teaches the opposite.

!!! warning "Educational material — not financial advice"
    The figures below are a measurement on one archive sample, not a law of the
    market. Coincidence is not cause.

<div id="pattern-trainer" data-src="../../../data/replay-episodes.json"></div>

---

## What came out of our archive

80 episodes, 3600 real candles (EURUSD, GBPUSD, USDJPY, EURJPY on H1 and D1).
The outcome is read 5 candles after the pattern.

| Pattern | Found | Worked | Rate |
|---|---|---|---|
| Hammer | 106 | 40 | **38.8%** |
| Shooting star | 91 | 37 | 41.1% |
| Bullish engulfing | 35 | 15 | 45.5% |
| Bearish engulfing | 38 | 19 | 52.8% |

The hammer — the best-known reversal shape — worked **less often than a coin
flip** on this sample. That does not make patterns useless: it means they do
**not predict direction**.

## One more honest number

By the standard rule (body under 10% of the candle range) a doji was found
**1739 times out of 3600 candles** — in almost every other one.

A shape that shows up half the time singles nothing out. That is why doji is
not among the trainer's questions: it would swamp the sample. It stays in the
statistics as a reminder that "found a pattern" and "found a signal" are
different things.

## So why learn them at all

A pattern is not a forecast, it is **a marker of a place**. It says "buyers and
sellers fought here, look closer", not "price goes up from here".

What actually gives an edge, in order:

1. **Context** — where the shape is. On a level after a long move it means more
   than in the middle of a range.
2. **Confirmation** — the next candle closing your way.
3. **Risk** — position size and stop decide the outcome of a series, not entry
   accuracy. The [position calculator](position-calculator.md) does that maths.

This is exactly why the project ships no signals and no "robots": see
[why a backtest lies](../docs/strategy-details.md) and the
[skill-or-luck check](monte-carlo.md).

## Next

- [Replay trainer](replay-trainer.md) — the same archive candles, but a full
  trade: entry, stop, take and a result in R.
- [Technical analysis](../docs/technical-analysis.md) — the candlestick section
  with the rules for using patterns.
- [Final exam](exam.md) — 20 questions drawn from 45, over half of them
  calculations.

!!! danger "Not financial advice"
    The rates above are measured on 3600 candles of four pairs. On another
    sample they will differ — and that is part of the lesson too.
