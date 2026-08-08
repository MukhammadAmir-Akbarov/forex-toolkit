---
widgets: [margin]
---

# 💰 Margin Calculator

!!! abstract "Why this matters"
    Margin is the **collateral** your broker locks up while a trade is open. It isn't lost — but it isn't available either: while it's tied to the position, you can't use it for other trades or to cover losses.

    This calculator shows **exactly how much cash gets locked** when you open a position and what share of your account that represents — so you never open too large and hit a Margin Call.

## Formula

```
Margin ($)       =  Lots × Contract × Price / Leverage
Usage (%)        =  Margin / Balance × 100

Contract = 100,000 (standard lot)
```

---

<div class="mc-widget" id="mc-widget">

<style>
.mc-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}
.mc-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.2rem;
}
@media (max-width: 600px) {
  .mc-form { grid-template-columns: 1fr; }
}
.mc-form label {
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--md-default-fg-color);
}
.mc-form input[type=number],
.mc-form select {
  margin-top: 0.3rem;
  padding: 0.55rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.mc-form input:focus,
.mc-form select:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.mc-form .mc-row-wide { grid-column: 1 / -1; }
.mc-form button {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.mc-form button:hover { filter: brightness(1.1); }
.mc-meta { font-size: 0.78rem; color: var(--md-default-fg-color--light); margin-top: 0.4rem; }
#mc-result {
  margin-top: 1.5rem;
  padding: 1.2rem;
  background: var(--md-default-bg-color);
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
}
#mc-result.warn { border-left-color: #f59e0b; }
#mc-result.danger { border-left-color: #dc2626; }
.mc-result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 1.5rem;
  margin-bottom: 0.7rem;
}
@media (max-width: 600px) {
  .mc-result-grid { grid-template-columns: 1fr; }
}
.mc-result-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.92rem;
  padding: 0.2rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}
.mc-result-row span:first-child { color: var(--md-default-fg-color--light); }
.mc-result-row span:last-child { font-weight: 600; font-family: var(--md-code-font-family); }
.mc-headline {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  text-align: center;
  margin: 0.5rem 0 1rem;
  font-family: var(--md-code-font-family);
}
#mc-result.warn .mc-headline { color: #d97706; }
#mc-result.danger .mc-headline { color: #dc2626; }
.mc-warnings {
  margin-top: 0.8rem;
  font-size: 0.88rem;
}
.mc-warnings .mc-warn {
  padding: 0.5rem 0.75rem;
  margin-top: 0.4rem;
  border-radius: 6px;
  background: rgba(245, 158, 11, 0.1);
  border-left: 3px solid #f59e0b;
}
.mc-warnings .mc-danger {
  background: rgba(220, 38, 38, 0.1);
  border-left-color: #dc2626;
}
.mc-warnings .mc-info {
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3b82f6;
}
</style>

<form class="mc-form" onsubmit="return false">
  <label>
    Account balance (USD)
    <input type="number" id="mc-deposit" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Lot size
    <input type="number" id="mc-lots" value="0.01" min="0.01" step="0.01" autocomplete="off">
    <span class="mc-meta">Minimum 0.01 (micro lot). 1.0 = standard lot.</span>
  </label>
  <label>
    Current pair price
    <input type="number" id="mc-price" value="1.0800" min="0.0001" step="any" autocomplete="off">
    <span class="mc-meta">Ask price from your broker terminal.</span>
  </label>
  <label>
    Leverage (1:X)
    <select id="mc-leverage">
      <option value="10">1:10</option>
      <option value="20">1:20</option>
      <option value="30" selected>1:30</option>
      <option value="50">1:50</option>
      <option value="100">1:100</option>
      <option value="200">1:200</option>
      <option value="500">1:500</option>
    </select>
  </label>
  <label>
    Currency pair
    <select id="mc-pair">
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
    Lot type
    <select id="mc-type">
      <option value="standard">Standard lot (100,000)</option>
      <option value="mini">Mini lot (10,000)</option>
      <option value="micro">Micro lot (1,000)</option>
    </select>
    <span class="mc-meta">Most forex brokers use the standard lot.</span>
  </label>
  <button type="button" id="mc-calc-btn" class="mc-row-wide">Calculate</button>
</form>

<div id="mc-result" style="display: none;">
  <div class="mc-headline" id="mc-headline">— USD</div>
  <div class="mc-result-grid">
    <div class="mc-result-row"><span>Balance</span><span id="mc-out-deposit">—</span></div>
    <div class="mc-result-row"><span>Lot size</span><span id="mc-out-lots">—</span></div>
    <div class="mc-result-row"><span>Pair price</span><span id="mc-out-price">—</span></div>
    <div class="mc-result-row"><span>Leverage</span><span id="mc-out-leverage">—</span></div>
    <div class="mc-result-row"><span>Contract size</span><span id="mc-out-contract">—</span></div>
    <div class="mc-result-row"><span>Required margin</span><span id="mc-out-margin">—</span></div>
    <div class="mc-result-row"><span>Free margin</span><span id="mc-out-free">—</span></div>
    <div class="mc-result-row"><span>Margin usage</span><span id="mc-out-pct">—</span></div>
  </div>
  <div class="mc-warnings" id="mc-warnings"></div>
</div>


</div>

---

## Key concepts

### What is margin?

**Required Margin** is the amount your broker locks up as collateral for an open position. It is returned to your account in full when the trade closes. Margin is **not a loss** — you only lose money when the trade closes at a loss.

### Free margin

**Free Margin** = Balance − Used Margin

This is the cash available to you right now: to open new positions or to absorb floating losses on existing ones.

### Margin level

**Margin Level** = (Equity / Used Margin) × 100%

Where Equity = Balance + Floating P&L.

Typical broker thresholds:

- **Margin Call** — level ~100%: broker warns that funds are running low; no new positions can be opened.
- **Stop Out** — level ~50%: broker **forcibly closes** your positions, starting with the most losing one.

### Margin Call and Stop Out

| Event | What happens |
|---|---|
| Margin Call | Margin level hit the warning threshold (~100%). Broker alerts you. No new positions allowed. |
| Stop Out | Margin level fell below the critical level (~50%). Broker closes positions automatically without your consent. |

Check the exact levels with your broker — they vary.

---

## Worked example

Starting conditions:

- Balance: **$1,000**
- Pair: **EUR/USD**, price **1.0800**
- Size: **0.01 lot** (micro lot)
- Leverage: **1:30**

```
Margin = 0.01 × 100,000 × 1.0800 / 30 = $36.00
Usage  = 36.00 / 1,000 × 100 = 3.60%
Free   = 1,000 − 36 = $964.00
```

The calculator above gives the same result: **$36.00**. This matches the Python tool output:

```bash
.venv/bin/python tools/margin_calculator.py --lots 0.01 --price 1.08 --leverage 30 --deposit 1000
# → Margin: $36.00
# → Margin usage: 3.60%
```

---

## How to use

1. **Balance** — current account balance in USD.
2. **Lot size** — size of the position you plan to open.
3. **Price** — current Ask price from your terminal.
4. **Leverage** — your account leverage (check with your broker; 1:30 is common in the EU).
5. **Lot type** — standard for most forex brokers.

Pay most attention to **Margin usage**:

- Up to 20% — comfortable, plenty of buffer.
- 20–50% — high load, be careful.
- Above 50% — dangerous; Stop Out risk is real.

---

## Python equivalent

This is an exact JS port of [`tools/margin_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/margin_calculator.py). Same formula, same thresholds. From the terminal:

```bash
.venv/bin/python tools/margin_calculator.py --lots 0.1 --price 1.08 --leverage 30 --deposit 1000
```

All calculations happen in your browser — your numbers are never sent anywhere.

---

!!! danger "Not financial advice"
    This calculator is an educational tool. Actual Margin Call / Stop Out levels differ between brokers. Always verify your broker's specific terms before opening positions.
