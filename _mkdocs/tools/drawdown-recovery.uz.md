---
widgets: [drawdown]
---

# 🩹 Tushishdan (drawdown) tiklanish kalkulyatori

!!! abstract "Nega −50% «shunchaki +50% qaytarish» emas"
    Tushish (drawdown) — bu depozitning cho'qqisidan pasayishi. Yangi boshlovchilarning asosiy tuzog'i shundaki, foizdagi zarar va foyda **assimetrik**: hisobning yarmini yo'qotgandan keyin nolga qaytish uchun qoldiqni **ikki baravar** oshirish kerak bo'ladi.

    Bu kalkulyator joriy chuqurlik qanday foyda talab qilishini — va «tezda qoplab olish» matematik jihatdan nega erishib bo'lmas ekanini ko'rsatadi.

---

## 🧮 Interaktiv kalkulyator

<div class="calc-widget">

<div class="calc-row">
  <label>Joriy tushish (depozit cho'qqisidan %)</label>
  <input type="number" id="dd-input" min="0" max="95" step="1" value="20">
  <span>%</span>
</div>

<button class="calc-button" id="dd-calc-btn">Hisoblash</button>

<div id="dd-result" class="calc-result"></div>

</div>

---

## 📐 Formula (kalkulyatorsiz ham ishlaydi)

Agar depozit `d` foizga tushgan bo'lsa, cho'qqidan `100 − d` qoladi. Boshlang'ich summaga qaytish uchun qoldiqni shuncha oshirish kerak:

```
talab qilinadigan foyda % = d / (100 − d) × 100
```

Misol: 20% tushish → 80% qoldi → qoldiqdan `20 / 80 × 100 = +25%` foyda kerak.

---

## 📋 Shpargalka-jadval

| Tushish | Depozit qoldig'i | Tiklanish uchun kerak foyda | Tushishdan necha baravar ko'p |
|---|---|---|---|
| −5% | 95% | +5.3% | ×1.05 |
| −10% | 90% | +11.1% | ×1.11 |
| −20% | 80% | +25.0% | ×1.25 |
| −30% | 70% | +42.9% | ×1.43 |
| −40% | 60% | +66.7% | ×1.67 |
| −50% | 50% | +100.0% | ×2.00 |

!!! warning "Xavfli zona 30% tushishdan boshlanadi"
    −30% dan chuqurroqda talab qilinadigan foyda tushishning o'zidan **tezroq** o'sadi va chuqurlikning har bir keyingi foizi tobora qimmatlashadi. Kuchaytirilgan risk bilan «qoplab olish» odatda yanada chuqur chuqurlik bilan tugaydi — hisoblar aynan shunday yo'qotiladi.

---

## 🎯 Bundan qanday xulosa chiqadi

1. **Chuqurlikka tushmaslik — undan chiqishdan arzon.** −10% tushish deyarli simmetrik qoplanadi (+11.1%), −50% esa jasorat talab qiladi (+100%).
2. **Savdo boshiga 1–2% risk — chuqur tushishdan himoya.** Ketma-ket 10 ta stop 1% riskda depozitning −10% ini beradi (tiklanadi). 10% riskda esa −65% (tiklanish uchun +186% kerak).
3. **Tushishdan keyin risk kamaytiriladi, oshirilmaydi.** Kattalashtirilgan lot bilan «qoplash» −20% ni −50% ga aylantirishning eng ishonchli usuli.

---

## 🔗 Keyin nima o'qish kerak

- [Vayron bo'lish xavfi (Monte-Karlo)](risk-of-ruin.md) — tushishlar stsenariylar bo'yicha qanday taqsimlanadi
- [WinRate × RR kalkulyatori](winrate-rr-calculator.md) — strategiyangizning matematik kutilmasi
- [Pozitsiya kalkulyatori](position-calculator.md) — riskni 1–2% chegarasida ushlab turish
- [LOT intizomi](../practice/lot-discipline.md) — nega lot hajmi hammani hal qiladi
- [Treyding psixologiyasi](../extras/psychology.md) — nega qoplab olishga shoshilgisi keladi

---

!!! note "O'quv materiali"
    Kalkulyator **faqat o'qitish** va risk matematikasini tushunish uchun mo'ljallangan. Bu moliyaviy maslahat emas va natijani kafolatlamaydi. Haqiqiy savdo har doim kiritilgan mablag'ning to'liq yo'qotilishi xavfini o'z ichiga oladi.
