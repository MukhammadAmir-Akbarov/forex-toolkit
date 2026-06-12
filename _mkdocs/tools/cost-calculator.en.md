# 💸 Trading Cost Calculator

!!! abstract "Why this matters"
    Every trade costs money **before the market moves at all**: the spread,
    the broker's commission, the overnight swap. Individually — pocket change.
    Over hundreds of trades — this is the **silent killer of your deposit**.

    This calculator shows how much you pay per trade, how many pips the price
    must move **just to break even**, and what overtrading costs you per month.

## Formula

```
Spread        =  Spread (pips) × Pip value × Lots
Commission    =  Commission per lot × Lots × 2   (entry + exit)
Swap          =  Swap per lot/night × Lots × Nights
Total/trade   =  Spread + Commission + Swap

Break-even (pips) =  Total / (Pip value × Lots)
Monthly cost      =  Total/trade × Trades per month
```

---

<div class="calc-widget" id="co-widget">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Deposit (USD)
    <input type="number" id="co-deposit" value="1000" min="1" step="any" autocomplete="off">
    <span class="pc-meta">Used to show costs as a % of your account.</span>
  </label>
  <label>
    Currency pair
    <select id="co-pair">
      <option value="EURUSD">EUR / USD</option>
      <option value="GBPUSD">GBP / USD</option>
      <option value="AUDUSD">AUD / USD</option>
      <option value="NZDUSD">NZD / USD</option>
      <option value="USDJPY">USD / JPY</option>
      <option value="USDCHF">USD / CHF</option>
      <option value="USDCAD">USD / CAD</option>
      <option value="EURJPY">EUR / JPY</option>
      <option value="GBPJPY">GBP / JPY</option>
      <option value="EURGBP">EUR / GBP</option>
    </select>
  </label>
  <label>
    Lots
    <input type="number" id="co-lots" value="0.10" min="0.01" step="0.01" autocomplete="off">
    <span class="pc-meta">1.0 = standard lot (100,000).</span>
  </label>
  <label>
    Spread (pips)
    <input type="number" id="co-spread" value="1.0" min="0" step="0.1" autocomplete="off">
    <span class="pc-meta">Ask − Bid difference from your terminal.</span>
  </label>
  <label>
    Commission per lot, one side (USD)
    <input type="number" id="co-commission" value="0" min="0" step="0.5" autocomplete="off">
    <span class="pc-meta">ECN accounts: ~$3.5/lot per side. Market accounts: 0.</span>
  </label>
  <label>
    Trades per month
    <input type="number" id="co-trades" value="40" min="1" step="1" autocomplete="off">
    <span class="pc-meta">How many trades you open per month.</span>
  </label>
  <label>
    Nights held
    <input type="number" id="co-nights" value="0" min="0" step="1" autocomplete="off">
    <span class="pc-meta">0 — intraday (no swap).</span>
  </label>
  <label>
    Swap per lot/night (USD)
    <input type="number" id="co-swap" value="-2" step="0.1" autocomplete="off">
    <span class="pc-meta">Negative = you pay, positive = you receive.</span>
  </label>
  <button type="button" id="co-calc-btn" class="pc-row-wide">Calculate</button>
</form>

<div id="co-result" style="display: none;">
  <div class="pc-headline" id="co-headline">— USD</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Spread</span><span id="co-out-spread">—</span></div>
    <div class="pc-result-row"><span>Commission (entry+exit)</span><span id="co-out-commission">—</span></div>
    <div class="pc-result-row"><span>Swap (× nights)</span><span id="co-out-swap">—</span></div>
    <div class="pc-result-row"><span>Total per trade</span><span id="co-out-total">—</span></div>
    <div class="pc-result-row"><span>Break-even</span><span id="co-out-breakeven">—</span></div>
    <div class="pc-result-row"><span>Monthly cost</span><span id="co-out-monthly">—</span></div>
    <div class="pc-result-row"><span>Monthly cost (% of deposit)</span><span id="co-out-monthly-pct">—</span></div>
    <div class="pc-result-row"><span>Yearly cost</span><span id="co-out-yearly">—</span></div>
  </div>
  <div class="pc-warnings" id="co-warnings"></div>
</div>

</div>

---

## Key concepts

### Spread

**Spread** — the difference between the Ask (buy) price and the Bid (sell) price. This is the first and most frequent cost: the moment you open a trade you are already in the red by the spread amount. A tight spread on EUR/USD is around 0.1–1.0 pip; on exotic pairs and around news releases it can widen several times over.

### Commission

On **ECN/Raw** accounts the spread is near zero, but the broker charges a fixed commission — typically around **$3.5 per lot per side** (≈ $7 round-trip). On **Market** accounts there is no commission, but the spread is wider. Always compare by **total** cost, not by a single parameter.

### Swap (overnight)

**Swap** — the fee for holding a position overnight (on Wednesdays it is often triple — covering the weekend). It depends on the interest-rate differential between the two currencies. It can be negative (you pay) or positive (you receive). For intraday trading swap = 0.

### Break-even

**Break-even** — how many pips the price must travel in your direction just to **cover trading costs**. If break-even is 3 pips and your take-profit is 10, then 30% of your potential gain is consumed by costs before counting any losing trades.

---

## Example

Deposit **$1,000**, EUR/USD, **0.10 lots**, spread **1.0** pip, commission **0**,
**40** trades per month, intraday:

```
Pip value (0.10 lots) = $1.00
Spread     = 1.0 × $1.00 = $1.00
Commission = 0
Swap       = 0
Total      = $1.00 per trade
Break-even = $1.00 / $1.00 = 1.0 pip
Per month  = $1.00 × 40 = $40.00 = 4.0% of deposit
Per year   ≈ $480 ≈ 48% of deposit
```

Forty small trades per month "eat up" nearly half the deposit per year **in costs alone** — even if you didn't lose on a single trade. This is exactly why overtrading is dangerous.

---

## How to use

1. Enter your account parameters (take the spread and commission from your broker's instrument specification).
2. Look at **"Break-even"** — if it is close to your average take-profit, the strategy is not viable: costs are too high.
3. Look at **"Yearly cost (% of deposit)"** — this is the price of your trading style.
   Want to lower it? Trade less often, aim for larger take-profits, and choose pairs with tight spreads.

All calculations happen entirely in your browser — your numbers are never sent anywhere.

---

!!! danger "Not financial advice"
    This is an educational tool. Actual spreads, commissions, and swaps depend on your broker,
    account type, and time of day. Always check your broker's instrument specification.
