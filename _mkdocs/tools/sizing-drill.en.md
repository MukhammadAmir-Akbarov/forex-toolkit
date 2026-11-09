---
widgets: [sizing-drill]
---

# ⏱️ Sizing Drill: Name the Lot in 20 Seconds

!!! abstract "What this is"
    A speed trainer: 10 problems, 20 seconds each — deposit, risk percent,
    stop in pips — name the lot size. The calculator computes for you, the
    exam asks “when”, and this drill closes the gap in between: **saying the
    lot out loud faster than the terminal opens**.

<div id="sizing-drill"></div>

---

## The formula that must live in your fingers

All problems use USD-quote pairs (EURUSD, GBPUSD, AUDUSD, NZDUSD), where one
pip of a standard lot is worth **$10**:

```
risk in $  = deposit × risk %
lot        = risk in $ ÷ (stop in pips × $10)
```

Example: $1000 deposit, 1% risk, 25-pip stop → $10 risk →
$10 ÷ (25 × $10) = **0.04 lots**.

## Typical mistakes (they are the distractor options)

- **×10** — forgot the pip is worth $10, not $1. The drill's most expensive
  mistake: on an account it turns 1% risk into 10%.
- **÷10** — confused a lot with a mini lot. The opposite extreme: a token
  trade that fails to monetise even a correct forecast.
- **Doubled risk** — computed off 2% instead of 1%. Worth remembering: risk
  grows linearly, drawdown psychology does not.

## How to train

1. First series — no rush; read the formula breakdown after each answer.
2. Next series — for speed: target **9–10 out of 10** at 20 seconds per problem.
3. Once stable at 10 out of 10 — level up: the
   [position calculator](position-calculator.md) for pairs with a floating
   pip value (USDJPY, crosses).

## Further reading

- [Position calculator](position-calculator.md) — the full version with every pair.
- [Pips and their price](pip-calculator.md) — where those $10 come from.
- [Final exam](exam.md) — sizing appears inside full scenarios there.

!!! danger "Not financial advice"
    The drill teaches risk arithmetic, not earning. A correct lot size does
    not make a losing strategy profitable — it makes its losses predictable.
