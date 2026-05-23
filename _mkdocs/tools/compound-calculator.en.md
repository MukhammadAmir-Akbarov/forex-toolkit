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

<script>
(function() {
  function calc() {
    const initial = parseFloat(document.getElementById('cc-initial').value);
    const roiPct = parseFloat(document.getElementById('cc-roi').value);
    const months = parseInt(document.getElementById('cc-months').value);
    const monthlyDeposit = parseFloat(document.getElementById('cc-deposit').value) || 0;
    const result = document.getElementById('cc-result');
    const warnings = document.getElementById('cc-warnings');
    warnings.innerHTML = '';
    const errors = [];
    if (!(initial > 0)) errors.push('Starting capital must be > 0.');
    if (isNaN(roiPct)) errors.push('Return must be a number.');
    if (!(months > 0)) errors.push('Period must be > 0 months.');
    if (errors.length) {
      result.style.display = 'block';
      result.className = 'pc-result danger';
      document.getElementById('cc-headline').textContent = '—';
      warnings.innerHTML = errors.map(e => `<div class="pc-warn pc-danger">⛔ ${e}</div>`).join('');
      return;
    }
    const r = roiPct / 100;
    let balance = initial;
    let totalDeposited = initial;
    const series = [{ month: 0, balance, gain: 0, profit: 0 }];
    for (let m = 1; m <= months; m++) {
      const gain = balance * r;
      balance = balance * (1 + r) + monthlyDeposit;
      if (m > 1) totalDeposited += monthlyDeposit;
      const profit = balance - totalDeposited;
      series.push({ month: m, balance, gain, profit });
    }
    const finalBalance = series[series.length - 1].balance;
    const profit = finalBalance - totalDeposited;
    const annualEquivalent = (Math.pow(1 + r, 12) - 1) * 100;
    const totalRoi = (finalBalance - initial) / initial * 100;
    const fmt$ = v => '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const fmtPct = v => v.toFixed(2) + '%';
    document.getElementById('cc-out-initial').textContent = fmt$(initial);
    document.getElementById('cc-out-roi').textContent = fmtPct(roiPct);
    document.getElementById('cc-out-months').textContent = months + ' months (' + (months / 12).toFixed(1) + ' years)';
    document.getElementById('cc-out-deposited').textContent = fmt$(totalDeposited);
    document.getElementById('cc-out-profit').textContent = fmt$(profit);
    document.getElementById('cc-out-final').textContent = fmt$(finalBalance);
    document.getElementById('cc-out-annual').textContent = fmtPct(annualEquivalent);
    document.getElementById('cc-out-roi-total').textContent = fmtPct(totalRoi);
    document.getElementById('cc-headline').textContent = fmt$(finalBalance);
    result.style.display = 'block';
    result.className = 'pc-result';
    const checkpoints = [1, 3, 6, 12, 24, 60, 120].filter(m => m <= months);
    if (!checkpoints.includes(months)) checkpoints.push(months);
    const tbody = document.getElementById('cc-tbody');
    tbody.innerHTML = checkpoints.map(m => {
      const s = series[m];
      return `<tr><td>Month ${m}</td><td>${fmt$(s.balance)}</td><td>${fmt$(s.gain)}</td><td>${fmt$(s.profit)}</td></tr>`;
    }).join('');
    if (roiPct > 10) {
      warnings.innerHTML += `<div class="pc-warn pc-danger">⛔ ${fmtPct(roiPct)} per month = ${fmtPct(annualEquivalent)} per year. This is <strong>not realistic</strong>. If someone promises this, it's a scam.</div>`;
    } else if (roiPct > 5) {
      warnings.innerHTML += `<div class="pc-warn">⚠️ ${fmtPct(roiPct)}/month is very optimistic. The best hedge funds do 20-30%/year ≈ 2%/month. Verify any promises.</div>`;
    } else if (roiPct < 0) {
      warnings.innerHTML += `<div class="pc-warn">📉 Negative return — drawdown scenario. After ${months} months you'd lose ${fmt$(initial - finalBalance)} from the starting capital.</div>`;
    }
    if (roiPct >= 1 && roiPct <= 5) {
      warnings.innerHTML += `<div class="pc-warn pc-info">ℹ️ ${fmtPct(roiPct)}/month is a realistic range for experienced traders. Most are content with 1-3%.</div>`;
    }
  }
  ['cc-initial', 'cc-roi', 'cc-months', 'cc-deposit'].forEach(id => {
    document.getElementById(id).addEventListener('input', calc);
  });
  document.getElementById('cc-calc-btn').addEventListener('click', calc);
  calc();
})();
</script>

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
