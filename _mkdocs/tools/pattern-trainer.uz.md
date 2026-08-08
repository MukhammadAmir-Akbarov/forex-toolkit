---
widgets: [pattern-trainer]
---

# 🕯️ Sham figuralari trenajyori — va ular aslida nima berdi

!!! abstract "Bu trenajyor nimasi bilan farq qiladi"
    Odatdagi trenajyor bitta narsani tekshiradi: figurani tanidingizmi. Bu esa
    xuddi shuni tekshiradi va keyin **darhol ko'rsatadi, bunday figuralar nima
    bilan tugagan** — o'sha arxiv shamlarida.

    Bu tanishning o'zidan muhimroq. Darslik ochiq aytadi: «hech qachon faqat
    figura bo'yicha savdo qilmang». Tanigani uchun maqtab, natija haqida jim
    turadigan trenajyor teskarisiga o'rgatadi.

!!! warning "O'quv materiali — moliyaviy maslahat emas"
    Quyidagi raqamlar — bitta arxiv tanlanmasidagi o'lchov, bozor qonuni emas.
    Mos kelish sabab degani emas.

<div id="pattern-trainer" data-src="../../../data/replay-episodes.json"></div>

---

## Bizning arxivda nima chiqdi

80 epizod, 3600 ta haqiqiy sham (EURUSD, GBPUSD, USDJPY, EURJPY, H1 va D1).
Natija figuradan 5 ta shamdan keyin o'qiladi.

| Figura | Topilgan | Ishlagan | Ulush |
|---|---|---|---|
| Bolg'a | 106 | 40 | **38.8%** |
| Uchayotgan yulduz | 91 | 37 | 41.1% |
| Buqa yutishi | 35 | 15 | 45.5% |
| Ayiq yutishi | 38 | 19 | 52.8% |

Bolg'a — eng mashhur burilish figurasi — bu tanlanmada **tangadan ham kamroq**
ishladi. Bu figuralar foydasiz degani emas: bu ular **yo'nalishni bashorat
qilmaydi** degani.

## Yana bitta halol raqam

Standart qoida bo'yicha (tanasi sham diapazonining 10% idan kam) doji **3600
shamdan 1739 martasida** topildi — deyarli har ikkinchisida.

Yarim holatda uchraydigan figura hech narsani ajratmaydi. Shuning uchun doji
trenajyor savollariga kirmaydi: u tanlanmani bosib ketardi. Statistikada esa
qoladi — «figura topdim» va «signal topdim» boshqa-boshqa narsa ekanini
eslatib turish uchun.

## Unda ularni nega o'rganish kerak

Figura — bashorat emas, **joyning belgisi**. U «bu yerda xaridorlar va
sotuvchilar kurashgan, diqqat bilan qara» deydi, «bu yerdan yuqoriga ketadi»
emas.

Ustunlikni nima beradi, muhimlik tartibida:

1. **Kontekst** — figura qayerda. Uzoq harakatdan keyingi darajada u yon
   harakat o'rtasidagidan ko'proq narsani anglatadi.
2. **Tasdiq** — keyingi shamning kerakli tomonga yopilishi.
3. **Risk** — seriya natijasini pozitsiya hajmi va stop hal qiladi, kirish
   aniqligi emas. Buni [pozitsiya kalkulyatori](position-calculator.md) hisoblaydi.

Loyihada signallar ham, «robotlar» ham yo'qligining sababi aynan shu:
[bektest nega yolg'on gapiradi](../docs/strategy-details.md) va
[«mahorat yoki omad» tekshiruvi](monte-carlo.md).

## Keyingi qadam

- [Replay trenajyori](replay-trainer.md) — o'sha arxiv shamlari, lekin to'liq
  savdo bilan: kirish, stop, teyk va R dagi natija.
- [Texnik tahlil](../docs/technical-analysis.md) — sham figuralari bo'limi va
  ulardan foydalanish qoidalari.
- [Yakuniy imtihon](exam.md) — 45 tadan 20 ta savol, yarmidan ko'pi hisobga.

!!! danger "Moliyaviy maslahat emas"
    Yuqoridagi ulushlar to'rtta juftlikning 3600 shamida o'lchangan. Boshqa
    tanlanmada ular boshqacha bo'ladi — bu ham darsning bir qismi.
