# 💲 Pip Value Calculator

!!! abstract "Why it matters"
    A pip is the **smallest unit of price movement**. How much money you win or lose per pip depends on your **position size** and the **pair**. Without understanding pip value, you can't correctly calculate risk.

## Formula

```
Lot size       =  100,000 base-currency units
Pip size       =  0.0001 for most pairs, 0.01 for JPY pairs
Pip value (USD)=  pip_size × lot × position_size  /  rate (if USD is quote or base)
```

---

<div class="pos-calc-widget" id="pip-calc">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Currency pair
    <select id="pp-pair">
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
      <option value="AUDJPY">AUD / JPY</option>
      <option value="CHFJPY">CHF / JPY</option>
      <option value="EURAUD">EUR / AUD</option>
      <option value="EURCHF">EUR / CHF</option>
    </select>
  </label>
  <label>
    Position size (lots)
    <input type="number" id="pp-lots" value="0.10" min="0.01" step="0.01" autocomplete="off">
    <span class="pc-meta">0.01 = micro, 0.1 = mini, 1.0 = standard.</span>
  </label>
  <label class="pc-checkbox pc-row-wide">
    <input type="checkbox" id="pp-live" checked>
    <span>Use live ECB rate (recommended)</span>
  </label>
  <button type="button" id="pp-calc-btn" class="pc-row-wide">Calculate</button>
</form>

<div id="pp-result" class="pc-result" style="display: none;">
  <div class="pc-headline" id="pp-headline">— $ / pip</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Pair</span><span id="pp-out-pair">—</span></div>
    <div class="pc-result-row"><span>Position size</span><span id="pp-out-lots">—</span></div>
    <div class="pc-result-row"><span>Pip size</span><span id="pp-out-pipsize">—</span></div>
    <div class="pc-result-row"><span>Rate used</span><span id="pp-out-rate">—</span></div>
    <div class="pc-result-row"><span>1 pip value</span><span id="pp-out-pip">—</span></div>
    <div class="pc-result-row"><span>10 pips</span><span id="pp-out-10">—</span></div>
  </div>
  <div class="pc-warnings" id="pp-warnings"></div>
</div>

<script>
(function() {
  async function fetchRate(base, quote) {
    try {
      const r = await fetch(`https://api.frankfurter.app/latest?from=${base}&to=${quote}`);
      if (!r.ok) return null;
      const d = await r.json();
      return d.rates && d.rates[quote] ? d.rates[quote] : null;
    } catch (e) { return null; }
  }
  const STATIC_RATES = {
    'USD-JPY': 150, 'USD-CHF': 0.88, 'USD-CAD': 1.37,
    'EUR-USD': 1.08, 'GBP-USD': 1.27, 'AUD-USD': 0.66,
    'NZD-USD': 0.60, 'EUR-GBP': 0.85,
  };
  async function getRate(base, quote, live) {
    if (live) {
      const r = await fetchRate(base, quote);
      if (r) return { value: r, source: 'ECB live' };
    }
    const key = `${base}-${quote}`;
    if (STATIC_RATES[key]) return { value: STATIC_RATES[key], source: 'static' };
    const rev = `${quote}-${base}`;
    if (STATIC_RATES[rev]) return { value: 1 / STATIC_RATES[rev], source: 'static (inv)' };
    return null;
  }
  async function calculate() {
    const pair = document.getElementById('pp-pair').value;
    const lots = parseFloat(document.getElementById('pp-lots').value);
    const live = document.getElementById('pp-live').checked;
    const result = document.getElementById('pp-result');
    const warnings = document.getElementById('pp-warnings');
    warnings.innerHTML = '';
    if (!(lots > 0)) {
      result.style.display = 'block';
      result.className = 'pc-result danger';
      document.getElementById('pp-headline').textContent = '—';
      warnings.innerHTML = '<div class="pc-warn pc-danger">⛔ Position size must be greater than 0.</div>';
      return;
    }
    const base = pair.slice(0, 3);
    const quote = pair.slice(3, 6);
    const pipSize = quote === 'JPY' ? 0.01 : 0.0001;
    const lotUnits = 100000;
    const pipValueQuote = pipSize * lotUnits * lots;
    let pipValueUSD, rateUsed = '—';
    if (quote === 'USD') {
      pipValueUSD = pipValueQuote;
      rateUsed = '— (USD is quote)';
    } else if (base === 'USD') {
      document.getElementById('pp-headline').textContent = 'Loading rate…';
      result.style.display = 'block';
      const r = await getRate(base, quote, live);
      if (!r) { warnings.innerHTML = '<div class="pc-warn">⚠️ Could not fetch rate.</div>'; return; }
      pipValueUSD = pipValueQuote / r.value;
      rateUsed = `1 USD = ${r.value.toFixed(4)} ${quote} (${r.source})`;
    } else {
      document.getElementById('pp-headline').textContent = 'Loading rate…';
      result.style.display = 'block';
      let r = await getRate(quote, 'USD', live);
      if (r) {
        pipValueUSD = pipValueQuote * r.value;
        rateUsed = `1 ${quote} = ${r.value.toFixed(4)} USD (${r.source})`;
      } else {
        r = await getRate('USD', quote, live);
        if (!r) { warnings.innerHTML = '<div class="pc-warn">⚠️ Could not fetch rate.</div>'; return; }
        pipValueUSD = pipValueQuote / r.value;
        rateUsed = `1 USD = ${r.value.toFixed(4)} ${quote} (${r.source})`;
      }
    }
    const fmt$ = v => '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 4 });
    document.getElementById('pp-out-pair').textContent = pair;
    document.getElementById('pp-out-lots').textContent = lots.toFixed(2);
    document.getElementById('pp-out-pipsize').textContent = pipSize.toString();
    document.getElementById('pp-out-rate').textContent = rateUsed;
    document.getElementById('pp-out-pip').textContent = fmt$(pipValueUSD);
    document.getElementById('pp-out-10').textContent = fmt$(pipValueUSD * 10);
    document.getElementById('pp-headline').textContent = fmt$(pipValueUSD) + ' / pip';
    result.style.display = 'block';
    result.className = 'pc-result';
  }
  ['pp-pair', 'pp-lots', 'pp-live'].forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener('input', calculate);
    el.addEventListener('change', calculate);
  });
  document.getElementById('pp-calc-btn').addEventListener('click', calculate);
  calculate();
})();
</script>

</div>

---

## Examples

| Pair | 1 pip on 0.1 lot | 1 pip on 1 lot (std) |
|---|---|---|
| EUR/USD | $1.00 | $10.00 |
| GBP/USD | $1.00 | $10.00 |
| USD/JPY (rate ~150) | $0.67 | $6.67 |
| USD/CHF (rate ~0.88) | $1.14 | $11.36 |
| EUR/JPY (rate EUR/JPY ~162) | $0.67 | $6.67 |
| EUR/GBP (GBP/USD ~1.27) | $1.27 | $12.70 |

## Why it matters

- **Verify broker calculator** — some platforms display inaccurate pip value
- **Compare pairs** — why the same 25-pip stop costs less on USDJPY than on EURUSD
- **Account currency conversion** — if your account isn't in USD, an extra step is needed

## Python equivalent

See [`tools/pip_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/pip_calculator.py).
