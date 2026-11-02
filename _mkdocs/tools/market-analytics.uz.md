---
widgets: [market-analytics]
---

# 📊 Bozor qachon harakatlanadi va nima birga yuradi

!!! abstract "Savdodan oldin hal qilinadigan ikki savol"
    **Terminalga qachon o'tirish kerak?** «Qulay paytda» emas — narx haqiqatan
    yurgan paytda. Aks holda yassi bozorda o'tirib, zerikkanlikdan savdolar
    o'ylab topasiz.

    **Aslida nechta pozitsiyam ochiq?** Uch xil juftlikdagi uchta bitim bitta
    garovning uch marta takrorlanishi bo'lib chiqishi mumkin.

    Ikkala xarita ham sakkiz juftlikning ikki yillik soatlik shamlaridan
    hisoblangan — bu fikr emas, o'lchov.

<div id="market-analytics" data-src="../../../data/market-analytics.json"></div>

---

## Birinchi xaritada nima ko'rinadi

**Sakkiz juftlikning barchasida cho'qqi bir xil: 14:00 UTC (Toshkentda 19:00).**
Bu London va Nyu-York kesishmasi: ikki yirik bozor bir vaqtda ochiq, o'rtacha
soatlik sham tunnagiga qaraganda ikki-uch baravar ko'proq yo'l yuradi.
Sessiyalarning to'liq jadvali — [Savdo sessiyalari](../practice/trading-sessions.md)
sahifasida.

**Iyena juftliklari ikki baravar keng yuradi.** GBP/JPY cho'qqida bir shamda
48 pips, EUR/USD da esa 20. Iyena juftligida pipsdagi xuddi shu stop narx
bo'yicha ancha kichik — va uni oddiy shovqin urib tashlaydi. Pozitsiya
hajmi stopdan hisoblanadi, shuning uchun
[pozitsiya kalkulyatori](position-calculator.md) bu yerda formalitas emas.

**Tun (22:00–06:00 UTC) hammasida tinch.** Bu «yomon» emas — bu fakt:
proboy strategiyalari bu soatlarda tanlanmaning o'ziga qarshi ishlaydi.

## Ikkinchi xaritada nima ko'rinadi

**AUD/USD va NZD/USD 0.87 bilan birga yuradi. EUR/JPY va GBP/JPY — 0.87.**
0.87 korrelyatsiya shuni anglatadiki, ikkala juftlikni ochsangiz, bu ikki
pozitsiya emas — ikki baravar lotli bitta pozitsiya. Har bir bitimda risk
1% bo'lsa, bitta g'oyadagi haqiqiy risk deyarli 2%.

**CAD bilan salbiy korrelyatsiyalar (−0.67 gacha).** AUD/USD long va USDCAD
bir vaqtda bir-birini qisman o'chiradi: bitta instrumentdagi foyda
ikkinchisida zarar bo'lib tug'iladi, spred esa ikkalasiga ham to'lanadi.

Ochiq bitimlarning umumiy riskini umumiy valyutalarni hisobga olgan holda
[ekspozitsiya kalkulyatori](risk-exposure-calculator.md) hisoblaydi — u
aynan shu haqda.

## Buning bilan nima qilish kerak

1. **Strategiyangiz soatlarida savdo qiling.** Proboy — sessiyalar
   kesishmasida, otkat sokin soatlarda ham yashay oladi. Xarita qaysi
   qayerda ekanini ko'rsatadi.
2. **Korrelyatsiyalashgan pozitsiyalarni bitta deb hisoblang.** EUR/USD +
   GBP/USD (0.79) — bu diversifikatsiya emas, ko'paytirish.
3. **Xaritani har olti oyda qayta tekshiring.** Ma'lumotlar yangi
   kotirovkalardan skript bilan qayta hisoblanadi — matritsa suzadi va bu
   normal.

## Keyingi o'qish

- [Savdo sessiyalari](../practice/trading-sessions.md) — jadval va kesishmalar mexanikasi.
- [Portfel ekspozitsiyasi](risk-exposure-calculator.md) — qancha risk allaqachon ochiq.
- [Juftliklar orasida ko'chirish](multipair.md) — nega «hammaga bitta sozlama» ishlamaydi.

!!! danger "Moliyaviy maslahat emas"
    Korrelyatsiya va volatillik — aniq davr (2024-yil may → 2026-yil may)
    statistikasi. Inqirozlar va stavka o'zgarishlari atrofida matritsa
    o'zgaradi: birga yurgan juftliklar tarqalib ketishi mumkin. Bu mahalliy
    xarita, ob-havo bashorati emas.
