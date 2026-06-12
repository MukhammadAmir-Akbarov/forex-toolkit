# 💰 Marja kalkulyatori

!!! abstract "Nima uchun bu kerak"
    Marja — broker ochiq pozitsiya uchun hisobingizda **muzlatib qo'yadigan garov**. U yo'qolmaydi, lekin boshqa maqsadlar uchun ham ishlatib bo'lmaydi: pozitsiya ochiq bo'lganda u shu yerda bog'liq turadi.

    Bu kalkulyator pozitsiyani ochishda **qancha mablag' muzlatilishini** va bu depozitning qancha foizini tashkil etishini ko'rsatadi — shunda siz juda katta hajmda ochib Margin Call olmasligingiz uchun.

## Formula

```
Marja ($)          =  Lotlar × Kontrakt × Narx / Richak
Foydalanish (%)    =  Marja / Depozit × 100

Kontrakt = 100 000 (standart lot)
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
    Hisob balansi (USD)
    <input type="number" id="mc-deposit" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Lotlar soni
    <input type="number" id="mc-lots" value="0.01" min="0.01" step="0.01" autocomplete="off">
    <span class="mc-meta">Minimum 0.01 (mikrolot). 1.0 = standart lot.</span>
  </label>
  <label>
    Juftlik joriy narxi
    <input type="number" id="mc-price" value="1.0800" min="0.0001" step="any" autocomplete="off">
    <span class="mc-meta">Broker terminalidagi Ask narxi.</span>
  </label>
  <label>
    Richak (1:X)
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
    Valyuta jufti
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
    Lot turi
    <select id="mc-type">
      <option value="standard">Standart lot (100 000)</option>
      <option value="mini">Mini lot (10 000)</option>
      <option value="micro">Mikro lot (1 000)</option>
    </select>
    <span class="mc-meta">Ko'pchilik forex brokerlar standart lot ishlatadi.</span>
  </label>
  <button type="button" id="mc-calc-btn" class="mc-row-wide">Hisoblash</button>
</form>

<div id="mc-result" style="display: none;">
  <div class="mc-headline" id="mc-headline">— USD</div>
  <div class="mc-result-grid">
    <div class="mc-result-row"><span>Balans</span><span id="mc-out-deposit">—</span></div>
    <div class="mc-result-row"><span>Lotlar</span><span id="mc-out-lots">—</span></div>
    <div class="mc-result-row"><span>Juftlik narxi</span><span id="mc-out-price">—</span></div>
    <div class="mc-result-row"><span>Richak</span><span id="mc-out-leverage">—</span></div>
    <div class="mc-result-row"><span>Kontrakt hajmi</span><span id="mc-out-contract">—</span></div>
    <div class="mc-result-row"><span>Talab qilinadigan marja</span><span id="mc-out-margin">—</span></div>
    <div class="mc-result-row"><span>Erkin marja</span><span id="mc-out-free">—</span></div>
    <div class="mc-result-row"><span>Marja foydalanishi</span><span id="mc-out-pct">—</span></div>
  </div>
  <div class="mc-warnings" id="mc-warnings"></div>
</div>


</div>

---

## Asosiy tushunchalar

### Marja nima?

**Talab qilinadigan marja** (Required Margin) — broker ochiq pozitsiya uchun garov sifatida muzlatib qo'yadigan summa. Savdo yopilganda hisobga to'liq qaytariladi. Marja **yo'qotish emas** — savdo zarardan yopilmaguncha pul yo'qolmaydi.

### Erkin marja

**Erkin marja** = Balans - Foydalanilgan marja

Bu sizga hozir **mavjud** bo'lgan pul: yangi pozitsiyalar ochish yoki mavjud pozitsiyalar bo'yicha suzuvchi zararni qoplash uchun.

### Marja darajasi

**Marja darajasi** = (Kapital / Foydalanilgan marja) × 100%

Bunda Kapital = Balans + Suzuvchi P&L.

Odatiy broker chegaralari:

- **Margin Call** — daraja ~100%: broker mablag'lar tugayotganini ogohlantiradi. Yangi pozitsiyalar ochib bo'lmaydi.
- **Stop Out** — daraja ~50%: broker eng zararli pozitsiyadan boshlab **majburiy yopadi**.

### Margin Call va Stop Out

| Hodisa | Nima bo'ladi |
|---|---|
| Margin Call | Marja darajasi ogohlantirish chegarasiga yetdi (~100%). Broker xabar beradi. Yangi pozitsiyalar yo'q. |
| Stop Out | Marja darajasi kritik chegara ostiga tushdi (~50%). Broker sizning roziligingizni olmay pozitsiyalarni yopadi. |

Aniq darajalarni o'z brokeringizda tekshirib oling — ular har xil bo'lishi mumkin.

---

## Hisob misoli

Boshlang'ich sharoitlar:

- Depozit: **$1 000**
- Juftlik: **EUR/USD**, narxi **1.0800**
- Hajm: **0.01 lot** (mikrolot)
- Richak: **1:30**

```
Marja = 0.01 × 100 000 × 1.0800 / 30 = $36.00
Foydalanish = 36.00 / 1 000 × 100 = 3.60%
Erkin marja = 1 000 - 36 = $964.00
```

Yuqoridagi kalkulyator bir xil natija beradi: **$36.00**. Bu Python vositasi natijasiga mos keladi:

```bash
.venv/bin/python tools/margin_calculator.py --lots 0.01 --price 1.08 --leverage 30 --deposit 1000
# → Marja: $36.00
# → Marja foydalanishi: 3.60%
```

---

## Qanday foydalanish kerak

1. **Balans** — joriy hisob balansi USD da.
2. **Lotlar** — ochmoqchi bo'lgan pozitsiya hajmi.
3. **Narx** — terminaldan joriy Ask narxi.
4. **Richak** — hisobingizning richagi (brokerda tekshirib oling; Yevropada 1:30 keng tarqalgan).
5. **Lot turi** — ko'pchilik forex brokerlar uchun standart lot.

**Marja foydalanishiga** alohida e'tibor bering:

- 20% gacha — qulay, zaxira bor.
- 20-50% — yuqori yuklanish, ehtiyot bo'ling.
- 50% dan yuqori — xavfli; Stop Out ehtimoli yuqori.

---

## Python versiyasi

Bu [`tools/margin_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/margin_calculator.py) ning aniq JS portidir. Bir xil formula, bir xil chegaralar. Terminaldan:

```bash
.venv/bin/python tools/margin_calculator.py --lots 0.1 --price 1.08 --leverage 30 --deposit 1000
```

Barcha hisoblashlar brauzeringizda amalga oshiriladi — raqamlaringiz hech qayerga yuborilmaydi.

---

!!! danger "Moliyaviy maslahat emas"
    Bu kalkulyator ta'lim vositasi. Margin Call / Stop Out darajalari brokerlar o'rtasida farq qiladi. Pozitsiya ochishdan oldin har doim brokeringiz shartlarini tekshirib oling.
