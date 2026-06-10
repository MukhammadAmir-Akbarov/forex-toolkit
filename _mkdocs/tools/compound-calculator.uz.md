# 📈 Murakkab foiz kalkulyatori

!!! abstract "Nima uchun bu kerak"
    **Murakkab foiz — uzoq muddatli depozit o'sishining asosiy kuchi.** Kichik, **barqaror** foizlar uzoq masofada bir martalik yirik yutish va yo'qotishlardan ko'proq foyda beradi. Bu kalkulyator nima kutish mumkinligini realistik ko'rsatadi.

!!! danger "Haqiqat"
    **Bu guru reklamasi emas.** Forexda oyiga barqaror 5% — bu **istisno** holat. Ko'pchilik proflar oyiga 1-3% dan mamnun. Bu kalkulyatordan «guru» va'dalarini **tekshirish uchun** foydalaning — agar kimdir «depozitingizni bir yilda ikki baravar qilaman» desa, bu oylik foizda nimani anglatishini ko'ring.

## Formula

```
Final = Boshlang'ich × (1 + r/100)^n

bu yerda r — oylik %, n — oylar soni
```

---

<div class="pos-calc-widget" id="compound-calc">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Boshlang'ich depozit (USD)
    <input type="number" id="cc-initial" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Oylik daromadlilik (%)
    <input type="number" id="cc-roi" value="3" min="-50" max="100" step="0.1" autocomplete="off">
    <span class="pc-meta">Realistik: yangi boshlovchi uchun 1-3%, tajribali uchun 3-5%.</span>
  </label>
  <label>
    Muddat (oylar)
    <input type="number" id="cc-months" value="24" min="1" max="600" step="1" autocomplete="off">
    <span class="pc-meta">12 = 1 yil, 60 = 5 yil.</span>
  </label>
  <label>
    Oylik to'ldirish (USD)
    <input type="number" id="cc-deposit" value="0" min="0" step="any" autocomplete="off">
    <span class="pc-meta">Ixtiyoriy: har oy qo'shadigan miqdoringiz.</span>
  </label>
  <button type="button" id="cc-calc-btn" class="pc-row-wide">Hisoblash</button>
</form>

<div id="cc-result" class="pc-result" style="display: none;">
  <div class="pc-headline" id="cc-headline">—</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Boshlang'ich kapital</span><span id="cc-out-initial">—</span></div>
    <div class="pc-result-row"><span>Oylik daromadlilik</span><span id="cc-out-roi">—</span></div>
    <div class="pc-result-row"><span>Muddat</span><span id="cc-out-months">—</span></div>
    <div class="pc-result-row"><span>Jami to'ldirishlar</span><span id="cc-out-deposited">—</span></div>
    <div class="pc-result-row"><span>Foyda</span><span id="cc-out-profit">—</span></div>
    <div class="pc-result-row"><span>Yakuniy depozit</span><span id="cc-out-final">—</span></div>
    <div class="pc-result-row"><span>Yillik ekvivalent</span><span id="cc-out-annual">—</span></div>
    <div class="pc-result-row"><span>Boshlang'ich kapitalga ROI</span><span id="cc-out-roi-total">—</span></div>
  </div>

  <h4>Nazorat nuqtalari</h4>
  <table class="pc-compound-table" id="cc-table">
    <thead><tr><th>Oy</th><th>Depozit</th><th>+ oyda</th><th>Boshidan foyda</th></tr></thead>
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
    if (!(initial > 0)) errors.push('Boshlang\'ich kapital 0 dan katta bo\'lishi kerak.');
    if (isNaN(roiPct)) errors.push('Daromadlilik — son bo\'lishi kerak.');
    if (!(months > 0)) errors.push('Muddat 0 dan katta bo\'lishi kerak.');
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

    const fmt$ = v => '$' + v.toLocaleString('uz-UZ', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const fmtPct = v => v.toFixed(2) + '%';

    document.getElementById('cc-out-initial').textContent = fmt$(initial);
    document.getElementById('cc-out-roi').textContent = fmtPct(roiPct);
    document.getElementById('cc-out-months').textContent = months + ' oy (' + (months / 12).toFixed(1) + ' yil)';
    document.getElementById('cc-out-deposited').textContent = fmt$(totalDeposited);
    document.getElementById('cc-out-profit').textContent = fmt$(profit);
    document.getElementById('cc-out-final').textContent = fmt$(finalBalance);
    document.getElementById('cc-out-annual').textContent = fmtPct(annualEquivalent);
    document.getElementById('cc-out-roi-total').textContent = fmtPct(totalRoi);
    document.getElementById('cc-headline').textContent = fmt$(finalBalance);
    result.style.display = 'block';
    result.className = 'pc-result';

    // Nazorat nuqtalari jadvali
    const checkpoints = [1, 3, 6, 12, 24, 60, 120].filter(m => m <= months);
    if (!checkpoints.includes(months)) checkpoints.push(months);
    const tbody = document.getElementById('cc-tbody');
    tbody.innerHTML = checkpoints.map(m => {
      const s = series[m];
      return `<tr><td>${m} oy</td><td>${fmt$(s.balance)}</td><td>${fmt$(s.gain)}</td><td>${fmt$(s.profit)}</td></tr>`;
    }).join('');

    // Ogohlantirishlar
    if (roiPct > 10) {
      warnings.innerHTML += `<div class="pc-warn pc-danger">⛔ Oyiga ${fmtPct(roiPct)} = yiliga ${fmtPct(annualEquivalent)}. Bu **real emas**. Agar kimdir buni va'da qilsa — bu firibgarlik.</div>`;
    } else if (roiPct > 5) {
      warnings.innerHTML += `<div class="pc-warn">⚠️ ${fmtPct(roiPct)}/oy — juda optimistik. Eng yaxshi xedj-fondlar yiliga 20-30% = ~2%/oy qiladi. Va'dalarni tekshiring.</div>`;
    } else if (roiPct < 0) {
      warnings.innerHTML += `<div class="pc-warn">📉 Salbiy daromadlilik — drawdown stsenariyi. ${months} oydan so'ng boshlang'ichdan ${fmt$(initial - finalBalance)} yo'qotasiz.</div>`;
    }
    if (roiPct >= 1 && roiPct <= 5) {
      warnings.innerHTML += `<div class="pc-warn pc-info">ℹ️ ${fmtPct(roiPct)}/oy — tajribali treyderlar uchun realistik diapazon. Ko'pchilik 1-3% dan mamnun.</div>`;
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

## Kutilmalarni sozlash

| Oylik ROI | Yillik ROI | Realistikmi? |
|---|---|---|
| 1% | 12.7% | ✅ Tajribali treyder, past xavf |
| 2% | 26.8% | ✅ Tajribali uchun mumkin |
| 3% | 42.6% | ⚠️ Juda yaxshi, iste'dod talab qiladi |
| 5% | 79.6% | 🟡 Treyderlarning top 1% |
| 10% | 213.8% | 🔴 Uzoq muddatli uchun realistik emas |
| 20% | 791.6% | ⛔ Bu firibgarlik |

## Python versiyasi bilan bog'liqlik

Qarang: [`tools/compound_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/compound_calculator.py).
