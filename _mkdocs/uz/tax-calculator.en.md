# 🧾 Tax Calculator (Uzbekistan)

!!! abstract "Why you need this"
    An Uzbekistan tax resident who trades with a foreign broker **files their own tax return**.
    This calculator estimates **how much personal income tax (NDFL)** you will owe on your
    annual profit and converts the amount into UZS — so there are no surprises in April.

!!! danger "This is not tax advice"
    The calculation is **simplified and educational**. Rates and filing procedures change —
    always verify the current rules at [soliq.uz](https://soliq.uz) and in your personal
    account at [my.soliq.uz](https://my.soliq.uz); for large amounts consult an accountant.
    NDFL rate 12% — verified as of 2026-06-11.

## Formula

```
Net result ($)  =  Annual profit − Annual loss
Tax ($)         =  Net result × 12%   (only if net result > 0)
In UZS          =  Amount ($) × USD→UZS rate
```

---

<div class="tax-widget" id="tax-widget">

<style>
.tax-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}
.tax-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.2rem;
}
@media (max-width: 600px) {
  .tax-form { grid-template-columns: 1fr; }
}
.tax-form label {
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--md-default-fg-color);
}
.tax-form input[type=number] {
  margin-top: 0.3rem;
  padding: 0.55rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.tax-form input:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.tax-form .tax-row-wide { grid-column: 1 / -1; }
.tax-form button {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.tax-form button:hover { filter: brightness(1.1); }
.tax-meta { font-size: 0.78rem; color: var(--md-default-fg-color--light); margin-top: 0.4rem; }
#tax-result {
  margin-top: 1.5rem;
  padding: 1.2rem;
  background: var(--md-default-bg-color);
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
}
#tax-result.ok { border-left-color: #22c55e; }
.tax-result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 1.5rem;
  margin-bottom: 0.7rem;
}
@media (max-width: 600px) {
  .tax-result-grid { grid-template-columns: 1fr; }
}
.tax-result-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.92rem;
  padding: 0.2rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}
.tax-result-row span:first-child { color: var(--md-default-fg-color--light); }
.tax-result-row span:last-child { font-weight: 600; font-family: var(--md-code-font-family); }
.tax-headline {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  text-align: center;
  margin: 0.5rem 0 0.2rem;
  font-family: var(--md-code-font-family);
}
.tax-subhead { text-align: center; font-size: 0.85rem; color: var(--md-default-fg-color--light); margin-bottom: 1rem; }
.tax-warnings { margin-top: 0.8rem; font-size: 0.88rem; }
.tax-warnings .tax-note {
  padding: 0.5rem 0.75rem;
  margin-top: 0.4rem;
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3b82f6;
}
.tax-warnings .tax-ok {
  background: rgba(34, 197, 94, 0.1);
  border-left: 3px solid #22c55e;
}
.tax-warnings .tax-danger {
  background: rgba(220, 38, 38, 0.1);
  border-left: 3px solid #dc2626;
}
</style>

<form class="tax-form" onsubmit="return false">
  <label>
    Annual profit (USD)
    <input type="number" id="tax-profit" value="5000" min="0" step="any" autocomplete="off">
    <span class="tax-meta">Total of all profitable trades for the year.</span>
  </label>
  <label>
    Annual loss (USD)
    <input type="number" id="tax-loss" value="1000" min="0" step="any" autocomplete="off">
    <span class="tax-meta">Total of all losing trades for the year (enter as a positive number).</span>
  </label>
  <label>
    USD → UZS rate
    <input type="number" id="tax-rate" value="12500" min="1000" max="99000" step="any" autocomplete="off">
    <span class="tax-meta">Check the current rate at <a href="https://cbu.uz" target="_blank" rel="noopener">cbu.uz</a>.</span>
  </label>
  <button type="button" id="tax-calc-btn" class="tax-row-wide">Calculate</button>
</form>

<div id="tax-result" style="display: none;">
  <div class="tax-headline" id="tax-headline">—</div>
  <div class="tax-subhead" id="tax-subhead">tax due</div>
  <div class="tax-result-grid">
    <div class="tax-result-row"><span>Net result</span><span id="tax-out-net">—</span></div>
    <div class="tax-result-row"><span>Net result (UZS)</span><span id="tax-out-net-uzs">—</span></div>
    <div class="tax-result-row"><span>NDFL rate</span><span id="tax-out-rate">12%</span></div>
    <div class="tax-result-row"><span>Tax due</span><span id="tax-out-tax">—</span></div>
    <div class="tax-result-row"><span>Tax (UZS)</span><span id="tax-out-tax-uzs">—</span></div>
    <div class="tax-result-row"><span>After tax</span><span id="tax-out-after">—</span></div>
    <div class="tax-result-row"><span>After tax (UZS)</span><span id="tax-out-after-uzs">—</span></div>
  </div>
  <div class="tax-warnings" id="tax-warnings"></div>
</div>


</div>

---

## What to declare

- **Who:** a tax resident of Uzbekistan (you live in the country 183+ days per year).
- **What:** net annual income from trading with a foreign broker (profits − losses for the calendar year).
- **How much:** personal income tax (NDFL) **12%** of net profit (rate verified as of 2026).
- **When:** tax return due **by April 1** of the year following the reporting year.
- **Where:** personal account at [my.soliq.uz](https://my.soliq.uz) or a local tax office.

## What to keep (minimum 3 years)

- 📄 Annual broker statement showing profit/loss.
- 📄 Confirmation of deposits and withdrawals.
- 📄 Bank statements showing UZS credits to your account.

## When you need an accountant

- Trading income **> $5,000 / year**.
- You also have a formal salaried job → a combined tax return is required.
- You are unsure how to file or have received **a request from the tax authority**.

## Example

Annual profit **$5,000**, loss **$1,000**, rate **12,500**:

- Net result: **$4,000** (50,000,000 UZS)
- NDFL 12%: **$480** (6,000,000 UZS)
- After tax: **$3,520** (44,000,000 UZS)

!!! warning "Educational material — not financial or tax advice"
    Exact rates and rules are on [soliq.uz](https://soliq.uz). Calculation source:
    [tax-calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/uz/tax-calculator.py).

---

[← Brokers for UZ](brokers-uz.md) · [Withdrawal guide →](withdrawal-guide.md)
