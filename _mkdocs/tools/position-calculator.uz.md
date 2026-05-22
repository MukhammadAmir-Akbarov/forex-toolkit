# 📐 Pozitsiya hajmi kalkulyatori

!!! abstract "Nima uchun bu kerak"
    Pozitsiya hajmi — bozorda **tirik qolish-qolmasligingizning** asosiy omili. Agar har savdoda depozitning 0.5% xavf ostiga qo'ysangiz, ketma-ket 10 marta yo'qotsangiz ham faqat 5% yo'qotasiz. Agar 5% xavf ostiga qo'ysangiz, xuddi shu 10 yo'qotish **hisobni nolga tushiradi**.

    Bu kalkulyator siz xohlagan miqdorda **aniq** xavf ostiga qo'yishingizni kafolatlaydi — improvizatsiya va his-tuyg'ularsiz.

## Formula

```
Xavf miqdori ($)  =  Depozit × Xavf% / 100
Lotlar            =  Xavf miqdori / (Stop pipsda × Pip qiymati)
Yumalash          ←  pastga 0.01 gacha (broker minimumi) — real xavf
                     hech qachon rejalanganidan ortmaydi
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
    Hisob balansi (USD)
    <input type="number" id="pc-balance" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Savdoga xavf (%)
    <input type="number" id="pc-risk" value="0.5" min="0.01" max="10" step="any" autocomplete="off">
    <span class="pc-meta">Yangi boshlovchi: 0.5%. Tajribali: 2% gacha.</span>
  </label>
  <label>
    Stop-loss (pips)
    <input type="number" id="pc-stop" value="25" min="1" step="any" autocomplete="off">
    <span class="pc-meta">Kirish nuqtasidan stopgacha bo'lgan masofa.</span>
  </label>
  <label>
    Valyuta jufti
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
    <span>Jonli kursdan foydalanish (Frankfurter / ECB) — USDJPY, USDCHF, USDCAD va kross-juftliklar uchun aniqroq</span>
  </label>
  <button type="button" id="pc-calc-btn" class="pc-row-wide">Hisoblash</button>
</form>

<div id="pc-result" style="display: none;">
  <div class="pc-headline" id="pc-headline">— lot</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Balans</span><span id="pc-out-balance">—</span></div>
    <div class="pc-result-row"><span>Rejalashtirilgan xavf</span><span id="pc-out-risk-plan">—</span></div>
    <div class="pc-result-row"><span>Stop-loss</span><span id="pc-out-stop">—</span></div>
    <div class="pc-result-row"><span>Juftlik</span><span id="pc-out-pair">—</span></div>
    <div class="pc-result-row"><span>Pip qiymati</span><span id="pc-out-pip">—</span></div>
    <div class="pc-result-row"><span>Hajm (aniq)</span><span id="pc-out-lots-exact">—</span></div>
    <div class="pc-result-row"><span>Hajm (yumalangan)</span><span id="pc-out-lots-rounded">—</span></div>
    <div class="pc-result-row"><span>Real xavf</span><span id="pc-out-actual">—</span></div>
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
      return { value: pipSize * lot, source: 'doimiy' };
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
    if (!(balance > 0)) errors.push('Balans 0 dan katta bo\'lishi kerak.');
    if (!(riskPct > 0 && riskPct <= 10)) errors.push('Xavf 0 < x ≤ 10% oraliqda bo\'lishi kerak.');
    if (!(stopPips > 0)) errors.push('Stop-loss 0 dan katta pips bo\'lishi kerak.');
    if (errors.length) {
      result.style.display = 'block';
      result.className = 'danger';
      document.getElementById('pc-headline').textContent = '—';
      warnings.innerHTML = errors.map(e => `<div class="pc-warn pc-danger">⛔ ${e}</div>`).join('');
      return;
    }

    let pipValue = PIP_VALUES_STATIC[pair];
    let pipSource = 'jadval';
    if (live && LIVE_SENSITIVE.has(pair)) {
      document.getElementById('pc-headline').textContent = 'Kurs yuklanmoqda…';
      result.style.display = 'block';
      const live_pv = await livePipValue(pair);
      if (live_pv && live_pv.value > 0) {
        pipValue = live_pv.value;
        pipSource = live_pv.source;
      } else {
        warnings.innerHTML += `<div class="pc-warn">⚠️ Jonli kursni olib bo'lmadi — jadval qiymatidan foydalanildi.</div>`;
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
      warnings.innerHTML += `<div class="pc-warn pc-danger">⛔ ${fmtPct(r.actualRiskPct)} xavf — juda yuqori. Statistikaga ko'ra, bunday xavflar bir oy ichida hisobni nolga keltiradi.</div>`;
    } else if (r.actualRiskPct > 2) {
      cls = 'warn';
      warnings.innerHTML += `<div class="pc-warn">⚠️ ${fmtPct(r.actualRiskPct)} xavf yangi boshlovchi uchun tavsiya etilgan ≤ 2% dan yuqori. Kichikroq xavf yoki kengroq stop haqida o'ylab ko'ring.</div>`;
    }
    if (r.actualRisk > r.riskAmount * 1.05) {
      cls = cls === 'ok' ? 'warn' : cls;
      warnings.innerHTML += `<div class="pc-warn">⚠️ Yumalashdan keyin real xavf ${fmt$(r.actualRisk)} rejalashtirilgan ${fmt$(r.riskAmount)} dan ortdi — terminalda lotni 0.01 ga qo'lda kamaytiring.</div>`;
    }
    if (r.lotsRounded === 0.01 && r.lots < 0.005) {
      warnings.innerHTML += `<div class="pc-warn pc-info">ℹ️ Hisob 0.01 lotdan kam beradi — broker minimumi qo'llanildi. Stopni qisqartiring yoki depozit oshiring.</div>`;
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

## Qanday foydalanish kerak

1. **Balans** — joriy hisob balansi USD da (yoki valyutangizning USD ekvivalenti).
2. **Savdoga xavf** — bir savdoda yo'qotishga tayyor bo'lgan balans foizi. Yangi boshlovchi: **0.5%**.
3. **Stop-loss** — kirish nuqtasidan stopgacha bo'lgan masofa, grafik tahlilingizdan (long uchun oxirgi minimumdan past, short uchun oxirgi maksimumdan yuqori).
4. **Juftlik** — nima bilan savdo qilyapsiz.
5. **Jonli kursdan foydalanish** — USDJPY va pip qiymati kursga bog'liq bo'lgan boshqa juftliklar uchun. Bepul ro'yxatdan o'tmasdan ishlovchi API orqali ECB kurslarini oladi.

Terminalda **faqat yumalangan lot qiymatini** kiriting — bu real ochish mumkin bo'lgan miqdor.

---

## Misol

| Parametr | Qiymat |
|---|---|
| Balans | $1 000 |
| Xavf | 0.5% = $5.00 |
| Stop-loss | 25 pips |
| Juftlik | EUR/USD (pip qiymati = $10) |
| **Pozitsiya hajmi** | **0.02 lot** (standartning 1/50) |

Yo'qotish vaqtida: 25 pips × $10/pip × 0.02 lot = **$5** = balansning 0.5%. Aniq.

---

## Eng yaxshi amaliyot

!!! warning "Stopsiz hisoblamang"
    Agar **qayerda** stopingiz ekanini bilmasangiz, pozitsiya hajmini hisoblay olmaysiz. Bu — savdongizni tushunmasligingiz degani. Ochmang.

!!! danger "Qaytarib olish uchun hajmni oshirmang"
    Bu — **tilt**. Yo'qotishdan keyin hajm **o'zgarmaydi** yoki **kamayadi**. Hech qachon oshmaydi.

!!! tip "Stopni o'zgartiring, hajmni emas"
    Ko'proq potensial foyda istasangiz — **take-profit** ni o'zgartiring yoki piramidlash usulidan foydalaning. Pozitsiya hajmi — xavf funksiyasi, ishonchnikidan emas.

---

## Python versiyasi

Bu kalkulyator [`tools/position_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/position_calculator.py) ning aniq JS portidir. Xuddi shu formula, qiymatlar va ogohlantirishlar. Terminaldan:

```bash
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD
# yoki jonli kurs bilan:
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair USDJPY --live
```

Qulay bo'lganidan foydalaning. Saytdagi kalkulyator to'liq oflayn ishlaydi (birinchi yuklashdan keyin) va sizning raqamlaringizni hech qayerga yubormaydi — barcha hisoblash brauzerda.
