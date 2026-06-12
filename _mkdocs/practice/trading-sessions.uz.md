# 🕐 Savdo sessiyalari va bozor soatlari

!!! abstract "Nima uchun buni bilish muhim"
    Forex haftada 5 kun, 24 soat ishlaydi, lekin **faollik hamma vaqt bir xil emas**.
    O'zgaruvchanlik, spred va narx harakatining xarakteri qaysi sessiya ochiq ekanligiga
    bog'liq. Sessiya soatlarini bilsangiz, juftligingiz haqiqatan harakat qiladigan vaqtni
    tanlay olasiz — va «o'lik» bozorda bekorga o'tirmasiz.

## To'rtta sessiya

| Sessiya | Soatlar (UTC) | Toshkent (UTC+5) | Xarakter |
|---|---|---|---|
| 🇦🇺 Sidney | 22:00–07:00 | 03:00–12:00 | Tinch, haftani ochadi |
| 🇯🇵 Tokio (Osiyo) | 00:00–09:00 | 05:00–14:00 | JPY, AUD; o'rtacha |
| 🇬🇧 London (Evropa) | 08:00–17:00 | 13:00–22:00 | Eng yuqori hajm, tor spredlar |
| 🇺🇸 Nyu-York (AQSh) | 13:00–22:00 | 18:00–03:00 | Yuqori o'zgaruvchanlik, AQSh yangiliklari |

!!! warning "Yozgi vaqt (DST)"
    London va Nyu-York yozgi/qishgi vaqtga o'tishda **bir soatga siljiydi**
    (O'zbekistonda bunday o'tish yo'q). Shuning uchun yuqoridagi soatlar ±1 soat taxminiy
    ko'rsatkich. Quyidagi vidjet haqiqiy UTC va sizning vaqt mintaqangizga qarab
    avtomatik hisoblab beradi.

---

<div class="calc-widget" id="ts-widget">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Sizning vaqt mintaqangiz
    <select id="ts-tz">
      <option value="Asia/Tashkent" selected>Toshkent (UTC+5)</option>
      <option value="Asia/Almaty">Olmaota / Ostona (UTC+5)</option>
      <option value="Europe/Moscow">Moskva (UTC+3)</option>
      <option value="Europe/London">London</option>
      <option value="America/New_York">Nyu-York</option>
      <option value="Asia/Tokyo">Tokio</option>
      <option value="UTC">UTC</option>
    </select>
  </label>
</form>

<div id="ts-result">
  <div class="pc-headline" id="ts-clock">—</div>
  <div class="pc-result-grid" id="ts-sessions"></div>
  <div class="pc-warnings" id="ts-warnings"></div>
</div>

</div>

---

## Kesishishlar — pul shu yerda

Eng kuchli harakatlar **ikki sessiya bir vaqtda ochiq** bo'lganda yuz beradi:

- **London + Nyu-York** (13:00–17:00 UTC / 18:00–22:00 Toshkent) — **asosiy deraza**.
  Maksimal hajm, eng tor spredlar, EUR/USD, GBP/USD bo'yicha eng yaxshi likvidlik.
- **Tokio + London** (08:00–09:00 UTC) — qisqa deraza, Evropa ochilishini jonlantiradi.

Vaqtingiz cheklangan bo'lsa — **London/Nyu-York kesishishida** savdo qiling. Major
juftliklar bo'yicha kunlik o'zgaruvchanlikning asosiy qismi aynan shu vaqtga to'g'ri keladi.

## Qaysi juftliklar qachon faol

| Sessiya | Faol juftliklar |
|---|---|
| Tokio | USD/JPY, AUD/USD, NZD/USD, JPY bilan krosslar |
| London | EUR/USD, GBP/USD, EUR/GBP, USD/CHF |
| Nyu-York | EUR/USD, GBP/USD, USD/CAD, oltin (XAU/USD) |

## Amaliy xulosalar

1. **Osiyo sessiyasi EUR/GBP major juftliklari uchun tinch.** Flätni va soxta yorilishlarni
   o'tkazib yuborishingiz mumkin.
2. **Juma yopilishida va Dushanba ochilishida savdo qilmang** — spredlar kengroq, gaplar
   bo'ladi.
3. **AQSh yangiliklari Nyu-York sessiyasida chiqadi** — [kalendarni](../docs/technical-analysis.md)
   tekshiring va relizdan oldin pozitsiyaga kirmang.
4. **Tor spred = kam xarajat.** London/Nyu-York ga kirish tinch Osiyo sessiyasiga qaraganda
   arzonroq. Farqni [xarajat kalkulyatorida](../tools/cost-calculator.md) hisoblang.

---

!!! danger "Moliyaviy maslahat emas"
    Sessiya soatlari — yo'l-yo'riq. Haqiqiy faollik hafta kuniga, bayramlarga va yangiliklar
    foniga bog'liq. Har doim joriy bozorga qarang, faqat jadvalga emas.
