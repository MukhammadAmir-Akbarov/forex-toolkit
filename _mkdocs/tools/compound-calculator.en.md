# 📈 Compound Interest Calculator

!!! abstract "Why it matters"
    **Compound interest is the main force in long-term account growth.** Small but **consistent** percentages over time produce more than occasional big wins followed by drawdowns. This calculator shows what to realistically expect.

!!! danger "Reality check"
    **Not guru hype.** A consistent 5% per month is **extremely** rare in forex. Most professionals are happy with 1-3% per month. Use this calculator as a **promise checker** — if someone says "I'll double your account in a year," check what that means in monthly %.

## Formula

```
Final = Initial × (1 + r/100)^n

where r = monthly %, n = number of months
```

---

<div class="pos-calc-widget" id="compound-calc">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Starting balance (USD)
    <input type="number" id="cc-initial" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Monthly return (%)
    <input type="number" id="cc-roi" value="3" min="-50" max="100" step="0.1" autocomplete="off">
    <span class="pc-meta">Realistic: 1-3% for beginners, 3-5% for experienced.</span>
  </label>
  <label>
    Period (months)
    <input type="number" id="cc-months" value="24" min="1" max="600" step="1" autocomplete="off">
    <span class="pc-meta">12 = 1 year, 60 = 5 years.</span>
  </label>
  <label>
    Monthly contribution (USD)
    <input type="number" id="cc-deposit" value="0" min="0" step="any" autocomplete="off">
    <span class="pc-meta">Optional: how much you add each month.</span>
  </label>
  <button type="button" id="cc-calc-btn" class="pc-row-wide">Calculate</button>
</form>

<div id="cc-result" class="pc-result" style="display: none;">
  <div class="pc-headline" id="cc-headline">—</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Starting capital</span><span id="cc-out-initial">—</span></div>
    <div class="pc-result-row"><span>Monthly return</span><span id="cc-out-roi">—</span></div>
    <div class="pc-result-row"><span>Period</span><span id="cc-out-months">—</span></div>
    <div class="pc-result-row"><span>Total deposited</span><span id="cc-out-deposited">—</span></div>
    <div class="pc-result-row"><span>Profit</span><span id="cc-out-profit">—</span></div>
    <div class="pc-result-row"><span>Final balance</span><span id="cc-out-final">—</span></div>
    <div class="pc-result-row"><span>Annual equivalent</span><span id="cc-out-annual">—</span></div>
    <div class="pc-result-row"><span>Total ROI on initial</span><span id="cc-out-roi-total">—</span></div>
  </div>

  <h4>Checkpoints</h4>
  <table class="pc-compound-table" id="cc-table">
    <thead><tr><th>Month</th><th>Balance</th><th>Gain that month</th><th>Profit-to-date</th></tr></thead>
    <tbody id="cc-tbody"></tbody>
  </table>

  <div class="pc-warnings" id="cc-warnings"></div>
</div>


</div>

---

## Calibrating expectations

| Monthly ROI | Annual ROI | Realistic? |
|---|---|---|
| 1% | 12.7% | ✅ Experienced trader, low risk |
| 2% | 26.8% | ✅ Achievable for experienced |
| 3% | 42.6% | ⚠️ Very good, requires skill |
| 5% | 79.6% | 🟡 Top 1% of traders |
| 10% | 213.8% | 🔴 Not realistic long-term |
| 20% | 791.6% | ⛔ This is a scam |

## Python equivalent

See [`tools/compound_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/compound_calculator.py).
