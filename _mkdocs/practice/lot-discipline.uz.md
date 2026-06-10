# 🎯 LOT — seni yo'q qiladigan yoki qutqaradigan narsa

!!! abstract "Real treyderning amaliyotidan (2 yil, ~8000 signal)"
    Bu bob darsliklardan olingan nazariya emas. Bu — tajribali treyderning 2 yil kunlik oltin savdosi va statistika yuritish davomida chiqargan **eng muhim kuzatuvi**:

    > **«Pip, SL, TP — bularning hammasi ikkinchi darajali. Asosiy e'tibor LOTga qaratilishi kerak. Seni yaratadiganı ham, sindiradigan ham — aynan LOT, kirish nuqtasi emas.»**

---

## 🚨 Nima uchun treyderlarning 68% minusda?

Minglab obunachilik kanaldan real statistika:

```
22% — plusda (to'g'ri risk tanlash)
68% — minusda (haddan tashqari katta lot)
10% — nolda / endigina boshlaganlar
```

68% ning sababi **har doim bir xil**: ular **maydalab** sent-sentlab foyda to'plashadI, keyin esa **bir katta lotli savdo** bir oylik natijani nolga tushiradi.

!!! danger "Amaliyotdan misol"
    Depozit $100. Treyder oltinda (XAUUSD) **0.1 lot** pozitsiya ochadi.

    - 1 pip = ~$1 (0.1 lot uchun)
    - 50 pipslik stop-loss = **$50 zarar** = **bir savdoda depozitning 50%**
    - Ketma-ket 2 ta stop = depozit yarmiga tushadi

    **Bu savdo emas. Bu — loteriya.**

---

## 📐 Amaliyotchidan lot hajmi qoidasi

Uning o'z so'zlari bilan aniq formula:

> **«$100 баланси - 0,01 дан максимал 3-4 та очинг ундан кўп эмас. Мусилмончилик аста секинли билан.»**
>
> *Tarjima: $100 balansga — maksimum 3-4 ta pozitsiyani 0.01 lotdan oching. Xotirjam, shoshmasdan.*

### «LOT va Balans» jadvali (amaliyotdan)

| Balans | Pozitsiyaga maks. lot | Bir vaqtda maks. pozitsiyalar | Maks. jami lot |
|---|---|---|---|
| $100 | 0.01 | 3-4 | 0.04 |
| $300 | 0.03 | 3-4 | 0.12 |
| $500 | 0.05 | 3-4 | 0.20 |
| $1,000 | 0.10 | 3-4 | 0.40 |
| $5,000 | 0.50 | 3-4 | 2.00 |
| $10,000 | 1.00 | 3-4 | 4.00 |

!!! warning "Bu «ko'proq bo'ladi» emas. Bu — eng yuqori chegara."
    Agar $100 balansda 0.05 lot ochgan bo'lsang — savdo qilmayapsan, kazino o'ynayapsan.

!!! danger "Bu jadval — stopdan risk hisoblashning o'rnini bosmaydi"
    Jadvalda stop-loss ham, instrument ham yo'q — real risk esa aynan
    shularga bog'liq. Misol: XAUUSD da 0.01 lot, stop 150 pips — bu
    taxminan **$15** risk. $100 depozitda bu **bir savdoda 15%**, 3-4 ta pozitsiya esa
    allaqachon o'nlab foiz. Bu loyihaning «risk ≤ 1%» qoidasini **qo'pol buzadi**.

    Doimo lotni riskdan va stopdan hisoblang, balansdan emas:
    **risk ($) = lot × stop (pips) × pip qiymati**. Hisoblash uchun
    [pozitsiya kalkulyatori](../tools/position-calculator.md)dan foydalaning. Yuqoridagi jadval — faqat
    lotning yuqori chegarasi; riskdan hisoblash allaqachon bajarilgan bo'lsa ishlatiladi.

---

## 🎯 Nima uchun shuncha kam?

### 1. Turli lot hajmlarida psixologik qarorlar

**Depozitning 2% ini** pozitsiyada tutganda shunday o'ylaysan:
> «Yaxshi, bozor menga qarshi ketdi. Stopimni kutaman — u o'z joyida turibdi.»

**Depozitning 20% ini** pozitsiyada tutganda shunday o'ylaysan:
> «Bu zararga chidolmayman! Hozir stopni surib yuboraman, narx qaytadi...»

**Katta lot → vahimali qarorlar → siljitilgan stop → halokat.**

### 2. Drawdown bardoshli bo'lishi kerak

Ketma-ket 5 ta zararli savdo — yaxshi strategiya uchun ham **normal** holat.

- 0.01 lotda (risk 1%): drawdown = -5% → omon qolasan, savdoni davom ettirasan
- 0.05 lotda (risk 5%): drawdown = -25% → psixologik jihatdan og'ir, qoidalarni buza boshlaysan
- 0.1 lotda (risk 10%): drawdown = -50% → depozit deyarli yo'q qilingan

---

## 💡 Tajribali treyderning lot haqidagi iqtiboslari

!!! quote "Lot haqida — asosiy"
    *«Трайдингда 1-устивор ахамият бериш керак бўлган ягона нарса бу - ЛОТ!!! Сизни бор хам йўқ хам қиладиганни шу - ЛОТ!!!»*

    **Tarjima:** Treydinvda birinchi navbatda e'tibor berilishi kerak bo'lgan yagona narsa — bu LOT. Seni boy ham, hech narsasiz ham qiladigan — aynan LOT.

!!! quote "Yaxshi strategiya haqida"
    *«Нима учун яхши даромадда бўлган пайтингиздаги стратегиянгизни доимий ишлатмайсиз майдалаб бўлса хам - муҳими фойдадасизку.»*

    **Tarjima:** Nega sizga yaxshi daromad keltirgan strategiyangizni doimo ishlatmaysiz, mayda bo'lsa ham — muhimi, plusdasiz-ku.

!!! quote "Intizom haqida"
    *«ЛОТни хурмат қилишни ўрганмас экансиз, ишонинг лучше трейдингдан кетиш керак.»*

    **Tarjima:** Agar LOTni hurmat qilishni o'rganmasang — ishon, treydinvdan ketganing ma'qul.

---

## ✅ «LOTga hurmat qilyapmanmi?» tekshiruv ro'yxati

Har bir savdodan oldin o'zingni tekshir:

- [ ] Lotim har $100 balansga ≤ 0.01
- [ ] Bir vaqtda 3-4 tadan ko'p pozitsiya ochmayapman
- [ ] Bu savdodagi potensial zararm balansning ≤ 1%
- [ ] Yo'qotsam — bu yoqimsiz bo'ladi, lekin halokatli emas
- [ ] Zararli savdodan keyin «o'rnini qoplash» uchun lotni oshirmayapman
- [ ] Eyforiyada daromadli savdodan keyin lotni oshirmayapman

!!! danger "Agar kamida bitta band — YO'Q bo'lsa, savdoni ochma."

---

## 🔗 Keyingi nima o'qish kerak

- [Pozitsiya kalkulyatori](../tools/position-calculator.md) — to'g'ri lotingni hisoblang
- [Win Rate × Risk-Reward](../tools/winrate-rr-calculator.md) — qanday matematikaga rioya qilishingiz kerak
- [Treyding psixologiyasi](../extras/psychology.md) — nega miya lot qoidalarini buzishni xohlaydi
- [Anti-Tilt protokoli](../extras/anti-tilt-protocol.md) — agar allaqachon buzdingiz — nima qilish kerak

---

!!! info "Kuzatuvlar manbasi"
    Bu bob tajribali o'zbek treyderning 2 yillik ommaviy xabarlar arxivini tahlil qilish asosida tuzilgan. Barcha umumlashmalar ~8000 signal va kanalning ommaviy statistikasida tekshirilgan. Bu **aniq signallarni qayta hikoya qilish emas**, balki ajratib olingan metodologiya.
