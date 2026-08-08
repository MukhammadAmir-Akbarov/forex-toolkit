---
widgets: [compound]
---

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
