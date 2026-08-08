---
verified: 2026-08-05
widgets: [tax]
---

# 🧾 Soliq kalkulyatori (O'zbekiston)

!!! abstract "Nima uchun kerak"
    Xorijiy broker orqali savdodan olingan daromadni O'zbekiston rezidenti **o'zi deklaratsiya qiladi**.
    Bu kalkulyator yillik foyda bo'yicha **qancha JShDS** to'lash kerakligini va bu qancha so'mga
    teng bo'lishini taxmin qiladi — aprelda kutilmagan surprise bo'lmasligi uchun.

!!! danger "Bu soliq maslahati emas"
    Hisob **soddalashtirilgan va o'quv maqsadli**. Stavkalar va deklaratsiya tartibi o'zgarib turadi —
    dolzarb ma'lumotni [soliq.uz](https://soliq.uz) va shaxsiy kabinetingizda
    [my.soliq.uz](https://my.soliq.uz) tekshiring; katta summalar bo'lsa — buxgalterga murojaat qiling.
    JShDS stavkasi 12% — tekshirildi 2026-08-05.

## Formula

```
Sof natija ($)   =  Yillik foyda − Yillik zarar
Soliq ($)        =  Sof natija × 12%   (faqat natija > 0 bo'lsa)
So'mda           =  Summa ($) × USD→UZS kursi
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
    Yillik foyda (USD)
    <input type="number" id="tax-profit" value="5000" min="0" step="any" autocomplete="off">
    <span class="tax-meta">Yil davomida barcha foydali bitimlar summasi.</span>
  </label>
  <label>
    Yillik zarar (USD)
    <input type="number" id="tax-loss" value="1000" min="0" step="any" autocomplete="off">
    <span class="tax-meta">Yil davomida barcha zararli bitimlar summasi (musbat son sifatida).</span>
  </label>
  <label>
    Kurs USD → UZS
    <input type="number" id="tax-rate" value="12500" min="1000" max="99000" step="any" autocomplete="off">
    <span class="tax-meta">Dolzarb kursni <a href="https://cbu.uz" target="_blank" rel="noopener">cbu.uz</a> saytida tekshiring.</span>
  </label>
  <button type="button" id="tax-calc-btn" class="tax-row-wide">Hisoblash</button>
</form>

<div id="tax-result" style="display: none;">
  <div class="tax-headline" id="tax-headline">—</div>
  <div class="tax-subhead" id="tax-subhead">to'lanadigan soliq</div>
  <div class="tax-result-grid">
    <div class="tax-result-row"><span>Sof natija</span><span id="tax-out-net">—</span></div>
    <div class="tax-result-row"><span>Sof natija (so'm)</span><span id="tax-out-net-uzs">—</span></div>
    <div class="tax-result-row"><span>JShDS stavkasi</span><span id="tax-out-rate">12%</span></div>
    <div class="tax-result-row"><span>To'lanadigan soliq</span><span id="tax-out-tax">—</span></div>
    <div class="tax-result-row"><span>Soliq (so'm)</span><span id="tax-out-tax-uzs">—</span></div>
    <div class="tax-result-row"><span>Soliqdan keyin</span><span id="tax-out-after">—</span></div>
    <div class="tax-result-row"><span>Soliqdan keyin (so'm)</span><span id="tax-out-after-uzs">—</span></div>
  </div>
  <div class="tax-warnings" id="tax-warnings"></div>
</div>


</div>

---

## Nima deklaratsiya qilish kerak

- **Kim:** O'zbekiston soliq rezidenti (yilda 183+ kun mamlakatda yashaydigan).
- **Nima:** xorijiy broker orqali savdodan olingan yillik sof daromad (kalendar yil uchun foydalar − zararlar).
- **Qancha:** sof foydadan JShDS **12%** (tekshirildi 2026).
- **Qachon:** deklaratsiya — hisobot yilidan keyingi yilning **1 aprelgacha**.
- **Qayerda:** [my.soliq.uz](https://my.soliq.uz) shaxsiy kabineti yoki soliq inspeksiyasi bo'limi.

Rasmiy tekshiruv manbalari: Soliq qo'mitasining [2025 yil deklaratsiyasi haqidagi xabari](https://gov.uz/ru/soliq/news/view/144996)
va [12% stavka bo'yicha tushuntirishi](https://gov.uz/ru/soliq/news/view/42496).

## Nima saqlash kerak (kamida 3 yil)

- 📄 Brokerning yillik foyda/zarar hisoboti (statement).
- 📄 Mablag' kiritish va yechib olishlarni tasdiqlovchi hujjatlar.
- 📄 So'm o'tkazilganini ko'rsatuvchi karta ko'chirmasi.

## Qachon buxgalter kerak

- Bir nechta broker, valyuta yoki xorijiy daromad turi mavjud.
- Qaysi xarajat va zararlarni hisobga olish mumkinligi noaniq.
- To'ldirishga ishonchingiz yo'q yoki **soliq idorasidan so'rov** keldi.

## Misol

Yillik foyda **$5 000**, zarar **$1 000**, kurs **12 500**:

- Sof natija: **$4 000** (50 000 000 so'm)
- JShDS 12%: **$480** (6 000 000 so'm)
- Soliqdan keyin: **$3 520** (44 000 000 so'm)

!!! warning "O'quv materiali, moliyaviy va soliq maslahati emas"
    Aniq stavkalar va qoidalar — [soliq.uz](https://soliq.uz) da. Hisob manba kodi:
    [tax-calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/uz/tax-calculator.py).

---

[← O'zbekiston uchun brokerlar](brokers-uz.md) · [Pul yechib olish →](withdrawal-guide.md)
