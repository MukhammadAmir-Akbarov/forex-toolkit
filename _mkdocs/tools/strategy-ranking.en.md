---
widgets: [strategy-ranking]
---

# 🏁 Which strategy is better — and does that answer hold

!!! abstract "The third question of the same family"
    [Overfitting](overfitting.md) — does the tuning carry through time.
    [Carrying over to other pairs](multipair.md) — does it carry between
    markets. Here: **does the ranking of the strategies themselves hold**.

    Six strategies from the repository, real EUR/USD H1 candles. Only the first
    half of the history is shown. Pick who will come first on the second.

<div id="strategy-ranking" data-src="../../../data/strategies.json"></div>

---

## What came out

| Strategy | Past | Future | Place |
|---|---|---|---|
| EMA50 Pullback | **+22.2R** | −10.5R | 1 → 5 |
| Three Soldiers | +16.6R | +13.1R | 2 → 2 |
| Breakout | +9.8R | −8.3R | 3 → 4 |
| Mean Reversion | +5.8R | −12.1R | 4 → 6 |
| Breakout v2 | −4.6R | +11.9R | 5 → 3 |
| London Open Range | **−39.3R** | **+18.8R** | 6 → 1 |

The best of the past became **fifth out of six**. The worst of the past became
**first**. One strategy out of six kept its place. Order agreement: **−0.43**.

## What this means and what it does not

**It means:** a ranking of strategies built on history gives you no ground for
choosing. Neither first place nor last said anything about the next year.

**It does not mean:** that the order always inverts and you should pick the
worst. Six strategies is a small sample, and a negative correlation here can
easily be chance. The claim is exactly one: **you cannot lean on such a
ranking.**

This is the very same trap as on the overfitting page. Picking the best of six
strategies is the same selection as picking the best of 54 parameter sets. The
beautiful result goes to whoever tried more variants.

## Why not "comparison on synthetic data"

The repository has `strategies/compare.py`, which compares the same strategies
on **generated** candles. For illustrating the mechanics that is fine; for the
claim "this strategy is better" it is not — the numbers would be invented. So
here it is a real archive, with the time split stated explicitly.

## The mistake I nearly published

The first run produced **zero trades** for London Open Range on both halves. It
looked like a property of the strategy: "it finds no signals."

In fact `london_open.detect` first checks that the data index is a datetime
index and silently returns an empty list otherwise. No error — just "no signals
found". After the fix the strategy produced 256 and 174 trades — and turned out
to be the worst of the past and the best of the future, exactly the case this
page exists for.

The same trap twice in one day: **a zero result is more often a broken
measurement than a property of the thing measured.** The test
`test_every_strategy_actually_traded` now fails if a strategy stops receiving
the data it needs.

## What to do about it

1. **Do not choose a strategy from one backtest.** One run is one sample.
2. **Look at the logic, not the bottom line.** A clear reason why a trade should
   work survives a change of period better than a beautiful equity curve.
3. **Check stability.** Different periods, different pairs, different
   parameters. A result that holds in only one combination is not a result.

## Next

- [Why a backtest lies](overfitting.md) — the same trap on parameters.
- [Carrying over to other pairs](multipair.md) — the same on markets.
- [Skill or luck](monte-carlo.md) — a check on your own series.

!!! danger "Not financial advice"
    The numbers are measured on one pair over one period. None of the six
    strategies is recommended for trading — they exist as teaching examples.
