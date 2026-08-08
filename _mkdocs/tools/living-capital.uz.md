---
widgets: [living-capital]
---

# 💼 Treyding bilan yashash uchun qancha kerak

!!! abstract "Bu hisob nima uchun"
    «Ishni tashla va treyding bilan yasha» — kurslar, signallar va «ustoz bilan
    o'qish» shu va'da ustiga sotiladi. U bilan so'z bilan bahslashish foydasiz.
    Hisoblash osonroq.

    Oylik xarajatlaringizni **yechib olish** uchun kapital ulardan taxminan
    **yetmish barobar** katta bo'lishi kerak. Bu pessimizm emas — bu
    xarajatlarni real oylik daromadga bo'lish.

!!! warning "O'quv materiali — moliyaviy maslahat emas"
    Hisob o'zingiz kiritgan daromad bo'yicha kattalik tartibini ko'rsatadi.
    Barqaror daromad mavjud emas.

<div id="living-capital-widget"></div>

---

## Raqam qayerdan keladi

Formula qisqa:

```
soliqqacha ishlash = xarajatlar ÷ (1 − soliq stavkasi)
kerakli kapital    = soliqqacha ishlash ÷ oylik daromad
```

Misol: oyiga qo'lga **$500** kerak, daromad oyiga **1.5%**, JShDS 12%.

- ishlash kerak: `500 ÷ 0.88 = $568` oyiga;
- kapital: `568 ÷ 0.015 = $37 900`.

Ustiga zaxira: agar har oy butun foydani yechib olsangiz, birinchi zararli oyni
kapitalning o'zidan qoplashga to'g'ri keladi va u kamaya boshlaydi. Shuning
uchun bir necha oylik xarajat savdo hisobidan **alohida** saqlanadi.

## Nega daromad maxrajda turadi

Kalkulyator ko'rsatadigan asosiy narsa shu. Daromad chiziqli ta'sir qilmaydi:

| Oylik daromad | $500 qo'lga olish uchun kapital |
|---|---|
| 3% (optimistik) | ≈ $18 900 |
| 1.5% (real) | ≈ $37 900 |
| 1% (zerikarli, lekin halol) | ≈ $56 800 |

«Oyiga 3%» va «oyiga 1%» orasidagi farq kichik eshitiladi. Kapitalda esa bu
**uch barobar**.

Shu yerdan «oyiga 30%» va'dasining ma'nosizligi ham ko'rinadi: bunday
daromadda $1 900 yetardi — va u odamga sizning pulingiz nega kerakligi
tushunarsiz bo'lib qoladi.

## Bu raqam bilan nima qilish kerak

1. **Daromad manbaini tashlamang.** Kapital yetarli bo'lgunicha treyding maosh
   o'rnini bosmaydi, u yonma-yon o'rganiladigan ko'nikma.
2. **Muddatni halol sanang.** Kalkulyator sizning jamg'armangiz bilan maqsadga
   necha oyda yetishni ko'rsatadi. Odatda bu yillar — va bu normal.
3. **Avval yo'qotmaslikni o'rganing.** Ishlaydigan strategiyasiz kapital
   shunchaki tezroq kamayadi. O'zingizni [tayyorlik testi](risk-profile.md) va
   [jurnal](../journal/web-journal.md) bilan tekshiring.

## Keyingi qadam

- [Murakkab foiz kalkulyatori](compound-calculator.md) — pul yechilmaganda
  depozit qanday o'sadi.
- [Vayron bo'lish riski](risk-of-ruin.md) — berilgan riskda hisobni yo'qotish
  ehtimoli.
- [Soliq kalkulyatori](../uz/tax-calculator.md) — yillik natijadan 12%.

!!! danger "Moliyaviy maslahat emas"
    Raqamlar o'zingiz kiritgan daromadga bog'liq. Haqiqiy daromad barqaror
    emas, zararli oylar esa hammada bo'ladi.
