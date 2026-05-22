# 📐 Position Size Calculator

!!! abstract "Why this matters"
    Position size is **the single biggest factor** in whether you survive in the market. If you risk 0.5% of your account per trade, you can lose 10 trades in a row and only lose 5%. If you risk 5%, that same 10-loss streak **wipes you out**.

    This calculator guarantees you risk **exactly** what you planned — no improvisation, no emotion.

## Formula

```
Risk amount ($)  =  Balance × Risk% / 100
Lots             =  Risk amount / (Stop in pips × Pip value)
Round            ←  down to 0.01 (broker minimum) so actual risk never
                    exceeds planned
```

---

<div class="pos-calc-widget" id="pos-calc">

<style>
.pos-calc-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}
.pos-calc-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.2rem;
}
@media (max-width: 600px) {
  .pos-calc-form { grid-template-columns: 1fr; }
}
.pos-calc-form label {
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--md-default-fg-color);
}
.pos-calc-form input[type=number],
.pos-calc-form select {
  margin-top: 0.3rem;
  padding: 0.55rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.pos-calc-form input:focus,
.pos-calc-form select:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.pos-calc-form .pc-row-wide { grid-column: 1 / -1; }
.pos-calc-form .pc-checkbox {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  cursor: pointer;
}
.pos-calc-form .pc-checkbox input { margin: 0; }
#pc-result {
  margin-top: 1.5rem;
  padding: 1.2rem;
  background: var(--md-default-bg-color);
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
}
#pc-result.warn { border-left-color: #f59e0b; }
#pc-result.danger { border-left-color: #dc2626; }
.pc-result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 1.5rem;
  margin-bottom: 0.7rem;
}
@media (max-width: 600px) {
  .pc-result-grid { grid-template-columns: 1fr; }
}
.pc-result-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.92rem;
  padding: 0.2rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}
.pc-result-row span:first-child { color: var(--md-default-fg-color--light); }
.pc-result-row span:last-child { font-weight: 600; font-family: var(--md-code-font-family); }
.pc-headline {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  text-align: center;
  margin: 0.5rem 0 1rem;
  font-family: var(--md-code-font-family);
}
#pc-result.warn .pc-headline { color: #d97706; }
#pc-result.danger .pc-headline { color: #dc2626; }
.pc-warnings {
  margin-top: 0.8rem;
  font-size: 0.88rem;
}
.pc-warnings .pc-warn {
  padding: 0.5rem 0.75rem;
  margin-top: 0.4rem;
  border-radius: 6px;
  background: rgba(245, 158, 11, 0.1);
  border-left: 3px solid #f59e0b;
}
.pc-warnings .pc-danger {
  background: rgba(220, 38, 38, 0.1);
  border-left-color: #dc2626;
}
.pc-warnings .pc-info {
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3b82f6;
}
.pos-calc-form button {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.pos-calc-form button:hover { filter: brightness(1.1); }
.pc-meta { font-size: 0.78rem; color: var(--md-default-fg-color--light); margin-top: 0.4rem; }
</style>

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Account balance (USD)
    <input type="number" id="pc-balance" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Risk per trade (%)
    <input type="number" id="pc-risk" value="0.5" min="0.01" max="10" step="any" autocomplete="off">
    <span class="pc-meta">Beginner: 0.5%. Experienced: up to 2%.</span>
  </label>
  <label>
    Stop-loss (pips)
    <input type="number" id="pc-stop" value="25" min="1" step="any" autocomplete="off">
    <span class="pc-meta">Distance from entry to stop in pips.</span>
  </label>
  <label>
    Currency pair
    <select id="pc-pair">
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
  <label class="pc-checkbox pc-row-wide">
    <input type="checkbox" id="pc-live">
    <span>Use live rate (Frankfurter / ECB) — more accurate for USDJPY, USDCHF, USDCAD, cross pairs</span>
  </label>
  <button type="button" id="pc-calc-btn" class="pc-row-wide">Calculate</button>
</form>

<div id="pc-result" style="display: none;">
  <div class="pc-headline" id="pc-headline">— lot</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Balance</span><span id="pc-out-balance">—</span></div>
    <div class="pc-result-row"><span>Planned risk</span><span id="pc-out-risk-plan">—</span></div>
    <div class="pc-result-row"><span>Stop-loss</span><span id="pc-out-stop">—</span></div>
    <div class="pc-result-row"><span>Pair</span><span id="pc-out-pair">—</span></div>
    <div class="pc-result-row"><span>Pip value</span><span id="pc-out-pip">—</span></div>
    <div class="pc-result-row"><span>Size (exact)</span><span id="pc-out-lots-exact">—</span></div>
    <div class="pc-result-row"><span>Size (rounded)</span><span id="pc-out-lots-rounded">—</span></div>
    <div class="pc-result-row"><span>Actual risk</span><span id="pc-out-actual">—</span></div>
  </div>
  <div class="pc-warnings" id="pc-warnings"></div>
</div>

<script>
(function() {
  const PIP_VALUES_STATIC = {
    EURUSD: 10.00, GBPUSD: 10.00, AUDUSD: 10.00, NZDUSD: 10.00,
    USDJPY: 6.70, USDCHF: 11.30, USDCAD: 7.30,
    EURJPY: 6.70, GBPJPY: 6.70, EURGBP: 12.70,
  };

  const LIVE_SENSITIVE = new Set([
    'USDJPY', 'USDCHF', 'USDCAD', 'EURJPY', 'GBPJPY', 'EURGBP',
  ]);

  async function fetchRate(pair) {
    const base = pair.slice(0, 3);
    const quote = pair.slice(3, 6);
    try {
      const r = await fetch(`https://api.frankfurter.app/latest?from=${base}&to=${quote}`);
      if (!r.ok) return null;
      const d = await r.json();
      return d.rates && d.rates[quote] ? d.rates[quote] : null;
    } catch (e) {
      return null;
    }
  }

  async function livePipValue(pair) {
    const base = pair.slice(0, 3);
    const quote = pair.slice(3, 6);
    const pipSize = quote === 'JPY' ? 0.01 : 0.0001;
    const lot = 100000;

    if (quote === 'USD') {
      return { value: pipSize * lot, source: 'constant' };
    }
    if (base === 'USD') {
      const rate = await fetchRate(pair);
      if (!rate) return null;
      return { value: pipSize * lot / rate, source: `ECB: 1 USD = ${rate.toFixed(4)} ${quote}` };
    }
    const pipValueQuote = pipSize * lot;
    const quoteToUsd = await fetchRate(`${quote}USD`);
    if (!quoteToUsd) {
      const usdToQuote = await fetchRate(`USD${quote}`);
      if (!usdToQuote) return null;
      return { value: pipValueQuote / usdToQuote, source: `ECB: USD/${quote} = ${usdToQuote.toFixed(4)}` };
    }
    return { value: pipValueQuote * quoteToUsd, source: `ECB: ${quote}/USD = ${quoteToUsd.toFixed(4)}` };
  }

  function compute(balance, riskPct, stopPips, pipValue) {
    const riskAmount = balance * riskPct / 100;
    const lots = riskAmount / (stopPips * pipValue);
    let lotsRounded = Math.floor(lots * 100 + 1e-9) / 100;
    if (lotsRounded < 0.01) lotsRounded = 0.01;
    const actualRisk = lotsRounded * stopPips * pipValue;
    const actualRiskPct = actualRisk / balance * 100;
    return { riskAmount, lots, lotsRounded, actualRisk, actualRiskPct };
  }

  const fmt$ = v => '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const fmtPct = v => v.toFixed(2) + '%';
  const fmtLots = v => v.toFixed(4);
  const fmtLotsR = v => v.toFixed(2);

  async function recalc() {
    const balance = parseFloat(document.getElementById('pc-balance').value);
    const riskPct = parseFloat(document.getElementById('pc-risk').value);
    const stopPips = parseFloat(document.getElementById('pc-stop').value);
    const pair = document.getElementById('pc-pair').value;
    const live = document.getElementById('pc-live').checked;

    const result = document.getElementById('pc-result');
    const warnings = document.getElementById('pc-warnings');
    warnings.innerHTML = '';

    const errors = [];
    if (!(balance > 0)) errors.push('Balance must be greater than 0.');
    if (!(riskPct > 0 && riskPct <= 10)) errors.push('Risk must be in 0 < x ≤ 10%.');
    if (!(stopPips > 0)) errors.push('Stop-loss must be greater than 0 pips.');
    if (errors.length) {
      result.style.display = 'block';
      result.className = 'danger';
      document.getElementById('pc-headline').textContent = '—';
      warnings.innerHTML = errors.map(e => `<div class="pc-warn pc-danger">⛔ ${e}</div>`).join('');
      return;
    }

    let pipValue = PIP_VALUES_STATIC[pair];
    let pipSource = 'static table';
    if (live && LIVE_SENSITIVE.has(pair)) {
      document.getElementById('pc-headline').textContent = 'Loading rate…';
      result.style.display = 'block';
      const live_pv = await livePipValue(pair);
      if (live_pv && live_pv.value > 0) {
        pipValue = live_pv.value;
        pipSource = live_pv.source;
      } else {
        warnings.innerHTML += `<div class="pc-warn">⚠️ Could not fetch live rate — using static table value.</div>`;
      }
    }

    const r = compute(balance, riskPct, stopPips, pipValue);

    document.getElementById('pc-out-balance').textContent = fmt$(balance);
    document.getElementById('pc-out-risk-plan').textContent = `${fmtPct(riskPct)} = ${fmt$(r.riskAmount)}`;
    document.getElementById('pc-out-stop').textContent = stopPips + ' pips';
    document.getElementById('pc-out-pair').textContent = pair;
    document.getElementById('pc-out-pip').textContent = fmt$(pipValue) + '/pip (' + pipSource + ')';
    document.getElementById('pc-out-lots-exact').textContent = fmtLots(r.lots);
    document.getElementById('pc-out-lots-rounded').textContent = fmtLotsR(r.lotsRounded);
    document.getElementById('pc-out-actual').textContent = `${fmt$(r.actualRisk)} (${fmtPct(r.actualRiskPct)})`;
    document.getElementById('pc-headline').textContent = `${fmtLotsR(r.lotsRounded)} lot`;
    result.style.display = 'block';

    let cls = 'ok';
    if (r.actualRiskPct > 5) {
      cls = 'danger';
      warnings.innerHTML += `<div class="pc-warn pc-danger">⛔ Risk of ${fmtPct(r.actualRiskPct)} is very high. Statistically this leads to account blowups within a month.</div>`;
    } else if (r.actualRiskPct > 2) {
      cls = 'warn';
      warnings.innerHTML += `<div class="pc-warn">⚠️ Risk of ${fmtPct(r.actualRiskPct)} is above the beginner-recommended ≤ 2%. Consider smaller risk or wider stop.</div>`;
    }
    if (r.actualRisk > r.riskAmount * 1.05) {
      cls = cls === 'ok' ? 'warn' : cls;
      warnings.innerHTML += `<div class="pc-warn">⚠️ Rounding pushed actual risk ${fmt$(r.actualRisk)} above planned ${fmt$(r.riskAmount)} — manually lower lot to 0.01.</div>`;
    }
    if (r.lotsRounded === 0.01 && r.lots < 0.005) {
      warnings.innerHTML += `<div class="pc-warn pc-info">ℹ️ Calculation gives less than 0.01 lot — broker minimum applied. Tighten your stop or grow your account to stay within the planned risk.</div>`;
    }
    result.className = cls === 'ok' ? '' : cls;
  }

  const inputs = ['pc-balance', 'pc-risk', 'pc-stop', 'pc-pair', 'pc-live'];
  inputs.forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener('input', recalc);
    el.addEventListener('change', recalc);
  });
  document.getElementById('pc-calc-btn').addEventListener('click', recalc);

  recalc();
})();
</script>

</div>

---

## How to use

1. **Balance** — current account balance in USD (or equivalent of your account currency).
2. **Risk per trade** — % of balance you accept to lose on one trade. Beginner: **0.5%**.
3. **Stop-loss** — distance from entry to stop in pips, from your chart analysis (below last swing low for longs, above swing high for shorts).
4. **Pair** — what you're trading.
5. **Use live rate** — for USDJPY and other pairs where pip value depends on the rate. Pulls ECB rates via a free no-auth API.

Type **only the rounded lot value** into your broker terminal — that's what you can actually open.

---

## Worked example

| Parameter | Value |
|---|---|
| Balance | $1,000 |
| Risk | 0.5% = $5.00 |
| Stop-loss | 25 pips |
| Pair | EUR/USD (pip value = $10) |
| **Position size** | **0.02 lot** (1/50 of standard) |

If stopped out: 25 pips × $10/pip × 0.02 lot = **$5** = 0.5% of balance. Exact.

---

## Best practices

!!! warning "No stop, no size"
    If you don't know **where** your stop is, you can't size the position. That means you don't understand your trade. Don't open it.

!!! danger "Don't increase size to recover"
    That's **tilt**. After a loss, size **stays** the same or **goes down**. Never up.

!!! tip "Move the stop, not the size"
    If you want more potential profit — adjust the **take-profit** or use pyramiding. Position size is a function of risk, not of confidence.

---

## Python equivalent

This calculator is an exact JS port of [`tools/position_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/position_calculator.py). Same formula, same values, same warnings. From the terminal:

```bash
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD
# or with live rate:
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair USDJPY --live
```

Use whichever is convenient. The web calculator is fully offline-friendly (after first load) and never transmits your numbers anywhere — all computation is in your browser.
