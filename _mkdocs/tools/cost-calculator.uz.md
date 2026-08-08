---
widgets: [cost]
---

# 💸 Savdo xarajatlari kalkulyatori

!!! abstract "Nima uchun bu kerak"
    Har bir savdo bozor harakat qilmasdan **oldin ham** pul talab qiladi: spred,
    broker komissiyasi, pozitsiyani kechaga o'tkazish uchun svop. Alohida olganda — mayda
    xarajatlar. Yuzlab savdolar masofasida — bu **depozitning jim qotili**.

    Bu kalkulyator bir savdo uchun qancha to'lashingizni, narx **faqat zarar ko'rmaslik
    nuqtasiga yetish uchun** qancha punkt o'tishi kerakligini va bir oylik overtreydingning
    qancha turishini ko'rsatadi.

## Formula

```
Spred              =  Spred (punktlar) × Punkt qiymati × Lotlar
Komissiya          =  Lot uchun komissiya × Lotlar × 2   (kirish + chiqish)
Svop               =  Lot/kecha svopi × Lotlar × Kechalar
Jami/savdo         =  Spred + Komissiya + Svop

Zarar ko'rmaslik nuqtasi (punktlar) =  Jami / (Punkt qiymati × Lotlar)
Oylik xarajat                       =  Jami/savdo × Oylik savdolar soni
```

---

<div class="calc-widget" id="co-widget">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Depozit (USD)
    <input type="number" id="co-deposit" value="1000" min="1" step="any" autocomplete="off">
    <span class="pc-meta">Xarajatlarni hisob foizi sifatida ko'rsatish uchun kerak.</span>
  </label>
  <label>
    Valyuta jufti
    <select id="co-pair">
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
    Lotlar
    <input type="number" id="co-lots" value="0.10" min="0.01" step="0.01" autocomplete="off">
    <span class="pc-meta">1.0 = standart lot (100 000).</span>
  </label>
  <label>
    Spred (punktlar)
    <input type="number" id="co-spread" value="1.0" min="0" step="0.1" autocomplete="off">
    <span class="pc-meta">Terminaldan Ask − Bid farqi.</span>
  </label>
  <label>
    Lot uchun komissiya, bir tomon (USD)
    <input type="number" id="co-commission" value="0" min="0" step="0.5" autocomplete="off">
    <span class="pc-meta">ECN hisoblar: ~$3.5/lot bir tomondan. Market hisoblar: 0.</span>
  </label>
  <label>
    Oylik savdolar soni
    <input type="number" id="co-trades" value="40" min="1" step="1" autocomplete="off">
    <span class="pc-meta">Bir oyda qancha savdo ochasiz.</span>
  </label>
  <label>
    Kechalar soni
    <input type="number" id="co-nights" value="0" min="0" step="1" autocomplete="off">
    <span class="pc-meta">0 — kunlik savdo (svop yo'q).</span>
  </label>
  <label>
    Lot/kecha svopi (USD)
    <input type="number" id="co-swap" value="-2" step="0.1" autocomplete="off">
    <span class="pc-meta">Manfiy = to'laysiz, musbat = olasiz.</span>
  </label>
  <button type="button" id="co-calc-btn" class="pc-row-wide">Hisoblash</button>
</form>

<div id="co-result" style="display: none;">
  <div class="pc-headline" id="co-headline">— USD</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Spred</span><span id="co-out-spread">—</span></div>
    <div class="pc-result-row"><span>Komissiya (kirish+chiqish)</span><span id="co-out-commission">—</span></div>
    <div class="pc-result-row"><span>Svop (× kechalar)</span><span id="co-out-swap">—</span></div>
    <div class="pc-result-row"><span>Savdo uchun jami</span><span id="co-out-total">—</span></div>
    <div class="pc-result-row"><span>Zarar ko'rmaslik nuqtasi</span><span id="co-out-breakeven">—</span></div>
    <div class="pc-result-row"><span>Oylik xarajat</span><span id="co-out-monthly">—</span></div>
    <div class="pc-result-row"><span>Oylik xarajat (% depozit)</span><span id="co-out-monthly-pct">—</span></div>
    <div class="pc-result-row"><span>Yillik xarajat</span><span id="co-out-yearly">—</span></div>
  </div>
  <div class="pc-warnings" id="co-warnings"></div>
</div>

</div>

---

## Asosiy tushunchalar

### Spred

**Spred** — Ask (sotib olish) va Bid (sotish) narxlari orasidagi farq. Bu birinchi va eng tez-tez uchraydigan xarajat: savdoni ochganingizda siz darhol spred miqdorida minusda bo'lasiz. EUR/USD bo'yicha tor spred — taxminan 0.1–1.0 punkt; ekzotik juftliklarda va yangiliklar vaqtida u bir necha baravar kengayadi.

### Komissiya

**ECN/Raw** hisoblarda spred deyarli nolga teng, lekin broker doimiy komissiya oladi — odatda **bir tomondan lot uchun ~$3.5** (≈ ikki tomonga $7). **Market** hisoblarda komissiya yo'q, lekin spred kengroq. Har doim **to'liq** xarajat bo'yicha solishtiring, bitta parametr bo'yicha emas.

### Svop (kechaga o'tkazish)

**Svop** — pozitsiyani kechaga o'tkazish uchun to'lov (chorshanba kechasida ko'pincha uch barobar — dam olish kunlari uchun). Juftlik valyutalarining foiz stavkalari farqiga bog'liq. Manfiy (siz to'laysiz) ham, musbat (sizga to'lashadi) ham bo'lishi mumkin. Kunlik savdoda svop = 0.

### Zarar ko'rmaslik nuqtasi

**Zarar ko'rmaslik nuqtasi** — narx faqat **xarajatlarni qoplash uchun** sizning tomoningizda qancha punkt o'tishi kerak. Agar bu ko'rsatkich 3 punkt bo'lsa va sizning teyk-profitingiz 10 punkt bo'lsa, potensialning 30% yutqazgan savdolarni hisobga olmasdan ham xarajatlarga ketadi.

---

## Misol

Depozit **$1 000**, EUR/USD, **0.10 lot**, spred **1.0** punkt, komissiya **0**,
oyiga **40** savdo, kunlik:

```
Punkt qiymati (0.10 lot) = $1.00
Spred     = 1.0 × $1.00 = $1.00
Komissiya = 0
Svop      = 0
Jami      = $1.00 bir savdo uchun
Zarar ko'rmaslik nuqtasi = $1.00 / $1.00 = 1.0 punkt
Oyiga     = $1.00 × 40 = $40.00 = depozitning 4.0%
Yiliga    ≈ $480 ≈ depozitning 48%
```

Oyiga qirqta kichik savdo yiliga depozitning deyarli yarmini **faqat xarajatlarga** "yeydi" —
hatto birorta savdoda ham yutqazmagan bo'lsangiz ham. Aynan shuning uchun overtreydning xavfli.

---

## Qanday foydalanish kerak

1. Hisob parametrlarini kiriting (spred va komissiyani broker spetsifikatsiyasidan oling).
2. **"Zarar ko'rmaslik nuqtasi"** ga e'tibor bering — agar u o'rtacha teyk-profitingizga yaqin
   bo'lsa, strategiya yaroqsiz: xarajatlar juda yuqori.
3. **"Yillik xarajat (% depozit)"** ga qarang — bu sizning savdo uslubingizning narxi.
   Kamaytirmoqchimisiz? Kamroq savdo qiling, kattaroq teyk-profit bilan, tor spredli juftliklarda.

Barcha hisoblashlar brauzeringizda amalga oshiriladi — raqamlaringiz hech qayerga yuborilmaydi.

---

!!! danger "Moliyaviy maslahat emas"
    Bu ta'lim vositasi. Haqiqiy spredlar, komissiyalar va svoplar brokerga,
    hisob turiga va kun vaqtiga bog'liq. Har doim o'z brokeringizning spetsifikatsiyasini
    tekshirib oling.
