---
widgets: [multipair]
---

# 🌍 Sozlama boshqa juftliklarga ko'chadimi

!!! abstract "Qayta o'qitishga qo'shni savol"
    [Oldingi sahifada](overfitting.md) sozlama **vaqt** bo'ylab o'tishga
    bardosh bermadi. Bu yerda savol boshqa o'qda: u **bozorlar** orasida
    o'tishga bardosh beradimi?

    EUR/USD da eng yaxshi chiqqan parametrlarni olamiz va ularni bitta ham
    o'zgartirishsiz yetti boshqa juftlikka qo'llaymiz. Avval o'zingiz javob
    bering — keyin jadvalga qarang.

<div id="multipair" data-src="../../../data/multipair.json"></div>

---

## Nima chiqdi

Sakkiz juftlik, soatlik shamlar, ikki yil, juftlikka 103 tadan 211 tagacha savdo.

| Juftlik | Ko'chirish | O'zining eng yaxshisi |
|---|---|---|
| USDCAD | **+37.3R** | +37.3R |
| EURUSD *(tayanch)* | +21.1R | +21.1R |
| GBPJPY | +20.4R | +42.1R |
| NZDUSD | +19.8R | +40.5R |
| AUDUSD | +3.4R | +14.7R |
| GBPUSD | +3.2R | +22.4R |
| USDJPY | +0.7R | +17.3R |
| EURJPY | **−30.2R** | +0.8R |

## Javob kutilganidan nozikroq chiqdi

Halol aytaman: men to'liq yemirilishni kutgandim. U bo'lmadi — **sakkizdan
yettitasi foydada qoldi**. Sozlama kutilganidan yaxshiroq ko'chdi, va bu ham
foydali kuzatuv: saralangan hamma narsa ham albatta buzilib ketmaydi.

Lekin qaraydigan narsa ishora emas. Mana bu uchtasi.

**Tarqalish — 67.6R.** EUR/JPY dagi −30.2R dan USD/CAD dagi +37.3R gacha. Agar
siz «noto'g'ri» juftlikni tanlaganingizda, xuddi shu qoidalar bo'yicha ishlab
turib zarar ko'rgan bo'lardingiz.

**Tayanch juftlik yutmadi.** Hammasi sozlangan EUR/USD faqat ikkinchi o'rinni
egalladi. Demak parametrlar «EUR/USD ga moslangan» emas — ular ko'plardan
biri xolos.

**Moslash ko'chirishdan ikki barobar ko'p va'da qiladi.** Barcha juftliklar
bo'yicha yig'indi: ko'chirish **+75.7R**, har bir juftlikka moslash
**+196.1R**. Aynan shu 2.6 barobar farq reklamada ko'rsatiladigan chiroyli
raqam — u orqaga qarab tanlash bilan olingan, bu haqda
[qayta o'qitish sahifasi](overfitting.md).

**Sakkizdan oltitasi o'z parametrlarini afzal ko'radi.** Agar har bir
juftlikning o'z «eng yaxshisi» bo'lsa, «eng yaxshi» — strategiyaning emas,
tanlanmaning xossasi.

## Men chop etishimga oz qolgan xato

Birinchi hisob iyen juftliklarida ikki yil ichida nol va to'rtta savdo berdi.
Bu tayyor xulosaga o'xshardi: «strategiya iyen juftliklarida ishlamaydi».

Xulosa yolg'on bo'lardi. Iyen juftliklarida punkt 0.0001 emas, 0.01, men esa
uni uzatmagandim. «Narx EMA dan N punkt ichida» filtri yuz barobar katta
birlikda hisoblanib, deyarli hech qachon ishlamagan. Tuzatishdan keyin GBP/JPY
103 ta savdo va **+20.4R** berdi.

Saboq faqat texnik emas. Zaif natijani bozor xossalari bilan tushuntirishdan
oldin, o'lchov aybdor emasmi — shuni tekshirish kerak.
`test_jpy_pairs_were_measured_with_their_own_pip` testi endi punkt yana umumiy
bo'lib qolsa yiqiladi.

## Bu bilan nima qilish kerak

1. **Strategiyani bir necha juftlikda tekshiring.** Bitta juftlik — bitta
   tanlanma.
2. **Parametrlarni har bir juftlikka alohida moslamang.** Bu hisobotning
   chiroyini ikki barobar oshiradi va kelajakdagi natijaga hech narsa qo'shmaydi.
3. **O'rtachaga emas, eng yomon juftlikka qarang.** Siz o'rtacha bilan savdo
   qilmaysiz, aniq juftlik bilan qilasiz.

## Keyingi qadam

- [Bektest nega yolg'on gapiradi](overfitting.md) — o'sha tuzoq vaqt o'qi bo'ylab.
- [Mahorat yoki omad](monte-carlo.md) — o'z savdolar seriyangizni tekshirish.

!!! danger "Moliyaviy maslahat emas"
    Raqamlar sakkiz juftlikda bitta davr uchun o'lchangan. Boshqa davrda ular
    boshqacha bo'ladi — sahifaning mazmuni ham shu.
