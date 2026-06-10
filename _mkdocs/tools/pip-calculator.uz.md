# 💲 Pip qiymati kalkulyatori

!!! abstract "Nima uchun bu kerak"
    Pip — bu **narx harakatining eng kichik birligi**. Har bir pipda qancha pul yutish yoki yo'qotishingiz **pozitsiya hajmi** va **juftlik**ka bog'liq. Pip qiymatini tushunmasdan xavfni to'g'ri hisoblash mumkin emas.

## Formula

```
1 lot hajmi           =  100 000 ta asosiy valyuta birligi
Pip o'lchami          =  Ko'pchilik juftliklar uchun 0.0001, JPY-juftliklar uchun 0.01
Pip qiymati (USD)     =  pip_o'lchami × lot / kurs (agar USD — quote yoki base bo'lsa)
```

---

<div class="pos-calc-widget" id="pip-calc">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Valyuta jufti
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
    Pozitsiya hajmi (lot)
    <input type="number" id="pp-lots" value="0.10" min="0.01" step="0.01" autocomplete="off">
    <span class="pc-meta">0.01 = mikro-lot, 0.1 = mini, 1.0 = standart.</span>
  </label>
  <label class="pc-checkbox pc-row-wide">
    <input type="checkbox" id="pp-live" checked>
    <span>Joriy ECB kursidan foydalanish (tavsiya etiladi)</span>
  </label>
  <button type="button" id="pp-calc-btn" class="pc-row-wide">Hisoblash</button>
</form>

<div id="pp-result" class="pc-result" style="display: none;">
  <div class="pc-headline" id="pp-headline">— $ / pip</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Juftlik</span><span id="pp-out-pair">—</span></div>
    <div class="pc-result-row"><span>Pozitsiya hajmi</span><span id="pp-out-lots">—</span></div>
    <div class="pc-result-row"><span>Pip o'lchami</span><span id="pp-out-pipsize">—</span></div>
    <div class="pc-result-row"><span>Kurs (hisoblash uchun)</span><span id="pp-out-rate">—</span></div>
    <div class="pc-result-row"><span>1 pip qiymati</span><span id="pp-out-pip">—</span></div>
    <div class="pc-result-row"><span>10 pipda</span><span id="pp-out-10">—</span></div>
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

  // Statik kurslar fallback sifatida
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
    if (STATIC_RATES[key]) return { value: STATIC_RATES[key], source: 'jadval' };
    const rev = `${quote}-${base}`;
    if (STATIC_RATES[rev]) return { value: 1 / STATIC_RATES[rev], source: 'jadval (teskari)' };
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
      warnings.innerHTML = '<div class="pc-warn pc-danger">⛔ Pozitsiya hajmi 0 dan katta bo\'lishi kerak.</div>';
      return;
    }

    const base = pair.slice(0, 3);
    const quote = pair.slice(3, 6);
    const pipSize = quote === 'JPY' ? 0.01 : 0.0001;
    const lotUnits = 100000;
    const pipValueQuote = pipSize * lotUnits * lots;

    let pipValueUSD, rateInfo, rateUsed = '—';

    if (quote === 'USD') {
      pipValueUSD = pipValueQuote;
      rateUsed = '— (USD — quote)';
    } else if (base === 'USD') {
      document.getElementById('pp-headline').textContent = 'Kurs yuklanmoqda…';
      result.style.display = 'block';
      const r = await getRate(base, quote, live);
      if (!r) {
        warnings.innerHTML = '<div class="pc-warn">⚠️ Kursni olib bo\'lmadi. Keyinroq urinib ko\'ring.</div>';
        return;
      }
      pipValueUSD = pipValueQuote / r.value;
      rateUsed = `1 USD = ${r.value.toFixed(4)} ${quote} (${r.source})`;
    } else {
      // Kross-juftlik: quote → USD ga o'giramiz
      document.getElementById('pp-headline').textContent = 'Kurs yuklanmoqda…';
      result.style.display = 'block';
      let r = await getRate(quote, 'USD', live);
      if (r) {
        pipValueUSD = pipValueQuote * r.value;
        rateUsed = `1 ${quote} = ${r.value.toFixed(4)} USD (${r.source})`;
      } else {
        r = await getRate('USD', quote, live);
        if (!r) {
          warnings.innerHTML = '<div class="pc-warn">⚠️ Kursni olib bo\'lmadi. Keyinroq urinib ko\'ring.</div>';
          return;
        }
        pipValueUSD = pipValueQuote / r.value;
        rateUsed = `1 USD = ${r.value.toFixed(4)} ${quote} (${r.source})`;
      }
    }

    const fmt$ = v => '$' + v.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 4 });
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

## Misollar

| Juftlik | 0.1 lot uchun 1 pip | 1 lot (standart) uchun 1 pip |
|---|---|---|
| EUR/USD | $1.00 | $10.00 |
| GBP/USD | $1.00 | $10.00 |
| USD/JPY (kurs ~150) | $0.67 | $6.67 |
| USD/CHF (kurs ~0.88) | $1.14 | $11.36 |
| EUR/JPY (kurs EUR/JPY ~162) | $0.67 | $6.67 |
| EUR/GBP (kurs GBP/USD ~1.27) | $1.27 | $12.70 |

## Nima uchun buni bilish kerak

- **Broker kalkulyatorini tekshirish** — ba'zi platformalarda pip qiymati noto'g'ri ko'rsatiladi
- **Juftliklarni taqqoslash** — nima uchun USDJPY dagi xuddi shu 25-piplik stop EURUSD ga qaraganda arzonroq tushadi
- **Hisob valyutasini konvertatsiya qilish** — agar depozit USD da bo'lmasa, qo'shimcha konvertatsiya kerak bo'ladi

## Python versiyasi

[`tools/pip_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/pip_calculator.py) ga qarang.
