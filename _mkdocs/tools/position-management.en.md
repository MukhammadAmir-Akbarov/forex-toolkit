---
widgets: [position-management]
---

# 🎚️ What to do while the trade is open

!!! abstract "This was the hole in the learning path"
    "Before the trade" sizes the risk. The journal reviews the result. But the
    decisions are made **in between** — and those are exactly what the journal
    later flags: moved the stop, closed early, held too long. There was nothing
    to practise the cause on.

    Here the trade is already open. Stop is one ATR, target is 2R, fifteen real
    archive candles ahead. Choose what you will do and you get two numbers: what
    happened on this trade, and what the same plan did across all 160 trades.

<div id="position-management" data-src="../../../data/replay-episodes.json"></div>

---

## What the archive showed

80 episodes in both directions — 160 trades. Same entry, same stop, different
behaviour afterwards.

| Plan | Total | Against "just hold" | Helped | Hurt |
|---|---|---|---|---|
| Just hold | −10.9R | — | — | — |
| Breakeven at +1R | **−16.5R** | **−5.5R** | 25 | 18 |
| Half off at +1R | **−3.5R** | **+7.5R** | 32 | **41** |
| Trail 1R | −9.2R | +1.8R | 28 | 24 |

## Three conclusions, two of them not obvious

**Breakeven — the most popular advice — was the worst.** It knocks you out of
trades that would have reached the target: price went +1R, came back to entry,
and only then went where it was going. It saved 25 trades and spoiled fewer —
18 — but what it spoiled cost more than what it saved.

**Partial closing hurt more often than it helped — and still won.** 41 cases
against 32. That happens: many small losses against a rare large rescue. You
have to count the sum, not the number of cases. This is probably the most
useful thing on the page.

**Trailing changed almost nothing.** +1.8R over 160 trades is within noise.

## An honest caveat

"Just hold" gives **−10.9R** on this set. The scheme itself — stop of one ATR,
target 2R, entry in an arbitrary direction — is unprofitable; it is a common
ruler for all four plans, not a working system. The table does **not** say you
should close half. It says only that **management changes the result a lot**,
and which way is not obvious in advance.

As on the [overfitting page](overfitting.md): one archive, one period. Another
set will give other numbers.

## How it is counted

The rule without which the numbers would flatter: **if a candle touched both
the stop and the target, the stop counts.** The order of movement inside a
candle is unknown, so the worse case is taken. Plan triggers are checked after
the stop — otherwise a candle that reached both breakeven and the stop would
look like a win.

R is measured against the original risk: a partial close reduces size but does
not rebase the arithmetic.

## Next

- [Replay trainer](replay-trainer.md) — entry and stop placement.
- [Trading journal](../journal/web-journal.md) — the same journal that flags a
  moved stop; now there is somewhere to practise the cause.
- [Skill or luck](monte-carlo.md) — why one series proves nothing.

!!! danger "Not financial advice"
    Measured on 3600 candles of four pairs. Another set will give other numbers
    — that is part of the lesson, not a disclaimer for form's sake.
