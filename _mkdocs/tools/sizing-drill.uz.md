---
widgets: [sizing-drill]
---

# ⏱️ Sayzing drilli: 20 soniyada lot

!!! abstract "Bu nima"
    Tezlik trenajyori: 10 ta masala, har biri 20 soniya — depozit, risk
    foizi, pipsdagi stop — lot hajmini ayting. Kalkulyator siz uchun hisoblaydi,
    imtihon «qachon» deb so'raydi, bu drill esa o'rtadagi bo'shliqni yopadi:
    **lotni terminal ochilganidan tezroq aytish**.

<div id="sizing-drill"></div>

---

## Barmoqlarda yashashi kerak bo'lgan formula

Barcha masalalar USD kotirovkali juftliklarda (EURUSD, GBPUSD, AUDUSD,
NZDUSD), bunda standart lot pipsi **$10** turadi:

```
$ dagi risk = depozit × risk %
lot         = $ dagi risk ÷ (pipsdagi stop × $10)
```

Misol: $1000 depozit, 1% risk, 25 pips stop → $10 risk →
$10 ÷ (25 × $10) = **0.04 lot**.

## Odatiy xatolar (ular javob variantlaridagi chalg'ituvchilar)

- **×10** — pips $1 emas, $10 turishini unutdingiz. Drillning eng qimmat
  xatosi: hisobda u 1% riskni 10% ga aylantiradi.
- **÷10** — lotni mini-lot bilan adashtirdingiz. Qarama-qarshi chekka: to'g'ri
  prognozni ham yutqazadigan «belgi uchun» bitim.
- **Ikki baravar risk** — 1% o'rniga 2% dan hisobladingiz. Esda tuting: risk
  chiziqli o'sadi, pasayish psixologiyasi — yo'q.

## Qanday mashq qilish kerak

1. Birinchi seriya — shoshilmasdan, har javobdan keyingi formula tahlilini o'qing.
2. Keyingilari — tezlikka: har masalaga 20 soniyada **10 dan 9–10** maqsad.
3. 10 dan 10 barqaror bo'lgach — qiyinlashtiring: suzuvchi pips narxi bilan
   [pozitsiya kalkulyatori](position-calculator.md) (USDJPY, krosslar).

## Keyingi o'qish

- [Pozitsiya kalkulyatori](position-calculator.md) — barcha juftliklar bilan to'liq versiya.
- [Pipslar va ularning narxi](pip-calculator.md) — bu $10 qayerdan keladi.
- [Yakuniy imtihon](exam.md) — u yerda sayzing to'liq stsenariylar ichida.

!!! danger "Moliyaviy maslahat emas"
    Drill risk arifmetikasini o'rgatadi, pul topishni emas. To'g'ri lot
    yutqazuvchi strategiyani foydali qilmaydi — u zararlarini bashorat
    qilinadigan qiladi.
