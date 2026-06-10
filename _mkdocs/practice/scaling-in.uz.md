# 📈 Qo'shimcha kirish (Scaling-in) — pozitsiyaga qachon qo'shish kerak

!!! abstract "Amaliyotdan (arxivda 229 ta eslatma)"
    «Dolivka» (Qo'shimcha kirish) — **allaqachon foydali** pozitsiyani kattalashtirish uchun unga qo'shimcha kirish.

    Muhim: bu **zarardagi pozitsiyani o'rtalashtirish emas** (o'sha usul depozitlarni yo'q qiladi).

---

## 🎯 To'g'ri qo'shimcha kirish nima

### ❌ NOTO'G'RI (zararni o'rtalashtirish)

```
BUY 0.01 @ 1.0850   ← ochildi
Narx PASTGA 1.0820 ga boradi (minus 30 pips)
BUY 0.02 @ 1.0820   ← "o'rtacha yaxshilash uchun" qo'shildi
Narx 1.0790 ga boradi (yana minus 30)
BUY 0.04 @ 1.0790   ← yana qo'shildi
...

Natija: depozit yo'q qilindi.
Bu kazino, savdo emas.
```

### ✅ TO'G'RI (foydaga qo'shimcha kirish)

```
BUY 0.01 @ 1.0850   ← ochildi, depozitning 1% xavfi
Narx YUQORIGA 1.0875 ga boradi (+25 pip foyda)
SL avval BU ga ko'chiriladi ("Seyf" ga qarang)
Endi xavf = 0
BUY 0.01 @ 1.0875   ← 1-qo'shimcha HH parbozida

Narx 1.0900 ga yetadi
Ikkalasining SL qo'shimcha kirish nuqtasidan yuqoriga siljitiladi
BUY 0.01 @ 1.0900   ← 2-qo'shimcha kirish

Trend to'xtaganda — to'liq yopiladi.
```

---

## 📐 Qo'shimcha kirish qoidalari

### 1-qoida: Avval «Seyf», keyin qo'shimcha kirish

**Hali zarari bo'lgan pozitsiyaga qo'shimcha kirmang.**

Avval:
1. Asosiy pozitsiyaning SL ni BU ga ko'chiring
2. Harakat tasdiqlangach kuting (yangi HH / LL)
3. Shundagina — qo'shimcha kirish

### 2-qoida: Qo'shimcha kirish loti = birinchi pozitsiya loti (yoki undan kam)

```
Asosiy: 0.01
1-qo'shimcha: 0.01 (yoki 0.005)
2-qo'shimcha: 0.005 (yanada kichikroq)
```

**Qo'shimcha kirishda lotni hech qachon oshirmang!** «Ishonchim komil, 0.05 qo'yaman» = katta xato.

### 3-qoida: Faqat daraja parbozida qo'shimcha kirish

«His-tuyg'u bilan» emas, **struktura bo'yicha**:
- BUY uchun: oldingi HH (Higher High) parbozi
- SELL uchun: oldingi LL (Lower Low) parbozi

### 4-qoida: 2-3 ta qo'shimcha kirishdan ko'p emas

```
Asosiy pozitsiya → 1-qo'shimcha → 2-qo'shimcha → TO'XTASH
```

Agar bir to'lqinda 4-5 ta qo'shimcha kirish qilsangiz — bu **kibr va ochko'zlik**, strategiya emas.

### 5-qoida: Oxirgi qo'shimcha kirishda SL oldingi ostiga tortiladi

```
Asosiy @ 1.0850 → SL 1.0850 (BU)
1-qo'shimcha @ 1.0875 → ikkalasining SL 1.0865 (asosiyda 15 pip himoya)
2-qo'shimcha @ 1.0900 → barchasining SL 1.0885 (foyda himoyasi 25 pip)
```

---

## 🎯 Qachon qo'shimcha kirish, qachon YO'Q

### ✅ Qo'shimcha kirishning MANTIQLI bo'lgan holatlari:

- Kuchli trend kuni (masalan, FOMC dan keyin)
- Tasdiqlangan kalit daraja parbozi
- Swing da (H4+) konsolidatsiyadan keyin
- Asosiy pozitsiya allaqachon BU da
- Bozorda yuqori volatillik (oltin, EUR/USD yangilik vaqtida)

### ❌ Qo'shimcha kirishning MANTIQSIZ bo'lgan holatlari:

- Flatsda, yonbosh bozorda
- Juma kechqurunida (pozitsiya yaqinda yopiladi)
- Asosiy pozitsiya hali BU da bo'lmasa
- Qizil yangilikdan 1-2 soat oldin
- Eyforiyadasiz va «hamma narsani tushunaman» deb o'ylasangiz

---

## 🔢 Qo'shimcha kirish matematikasi

### Qo'shimcha kirishsiz:

```
1 pozitsiya, lot 0.01
Harakat: +100 pip
Foyda: $10 (1 pip = $0.10 uchun)
```

### To'g'ri qo'shimcha kirish bilan:

```
Asosiy 0.01 @ 1.0850 → +100 pip = $10
1-qo'shimcha (0.01) @ 1.0875 → +75 pip = $7.50
2-qo'shimcha (0.005) @ 1.0900 → +50 pip = $2.50

Jami: $20 xuddi shu xavfda (chunki asosiy BU da)
```

**To'g'ri himoya bilan qo'shimcha kirish daromadni ikkilantiradi.**

### Noto'g'ri qo'shimcha kirish (o'rtalashtirish) bilan:

```
Asosiy 0.01 @ 1.0850 → -30 pip = -$3
"O'rtalashtiraman" 0.02 @ 1.0820 → -30 pip = -$6
"Yana o'rtalashtiraman" 0.04 @ 1.0790 → -30 pip = -$12
Narx yana -50 ga boradi → barchasi bo'yicha STOP = -$50+

JAMI: bitta savdoda -$71, holbuki xavf $3 bo'lishi kerak edi.
```

---

## ⚠️ Qo'shimcha kirishning asosiy xatolari

### ❌ «Ishonchim komil, ulkan qo'shimcha qo'yaman»

Bu hissiy qaror. Qo'shimcha kirish loti **qat'iy ≤** asosiy lotga teng.

### ❌ SL ko'chirmasdan qo'shimcha kirish

Eng xavfli xato: qo'shildi, SL ni tortmadi, bozor buruldi — bir vaqtning o'zida ikki pozitsiyani yo'qotasiz.

### ❌ «Xedjlash uchun» teskari tomonga qo'shimcha kirish

Bu boshda tartibsizlik yaratadi. Xedj istasangiz — pozitsiyani yoping va teskari tomonga yangi oching.

### ❌ Tahlilsiz uchinchi-to'rtinchi marta qo'shimcha kirish

2 ta qo'shimcha kirishdan keyin **albatta** baholash kerak:
- Depozit haddan ziyod yuklanganmi?
- Harakatning cho'qqisida turibmizmi?
- Texnik tahlil nima deydi?

---

## 📊 Qo'shimcha kirish vs Pyramiding vs Martingale

| Usul | Bu nima | Xavfsizmi? |
|---|---|---|
| **Qo'shimcha kirish (to'g'ri)** | Himoyalangan asos bilan foydaga qo'shish | ✅ Ha |
| **Pyramiding** | Treyder adabiyotida qo'shimcha kirish bilan bir xil | ✅ Ha |
| **Martingale** | Zarardan keyin lotni ikkilantirish | ❌ Depozitning kafolatlangan o'limi |
| **O'rtalashtirish** | Zarariga qo'shish | ❌ Depozitlarni yo'q qiladi |
| **Hedge-grid** | Ikki tomonga ham orderlar to'ri | ⚠️ Yangi boshlovchi uchun juda xavfli |

**Yangi boshlovchi uchun: FAQAT himoyalangan asos bilan foydaga qo'shimcha kirish. Nuqta.**

---

## ✅ To'g'ri qo'shimcha kirishning nazorat ro'yxati

Har bir qo'shimcha kirishdan oldin:

- [ ] Asosiy pozitsiya allaqachon BU da (SL = kirish)
- [ ] Qo'shimcha kirish loti ≤ asosiy lot
- [ ] Bu daraja parbozida qo'shimcha kirish (HH / LL), «his bilan» emas
- [ ] Men 3+ qo'shimcha kirishda emasman (maksimum 2)
- [ ] Qizil yangilikkacha 1 soatdan ko'proq vaqt bor
- [ ] Qo'shimcha kirishdan keyin darhol ikki pozitsiyaning ham SL ni tortaman
- [ ] Umumiy xavf hali ham depozitning 2-3% chegarasida

---

## 💬 Amaliyotchi iqtibosi

!!! quote
    *«ТП1 +30 пипс ✅✅ сейф киламиз ... доливка @ 1965.»*

    **Tarjima:** «Take Profit 1 +30 pip ga yetdi ✅✅ seyf qilamiz ... @ 1965 da qo'shimcha kirish.»

Tartib: **foyda → seyf → qo'shimcha kirish**. Aksincha emas.

---

## 🔗 Keyingi nima o'qish kerak

- [Seyf (Move to BE)](breakeven-protocol.md) — majburiy oldindan shart
- [LOT-disciplina](lot-discipline.md) — barcha pozitsiyalar hajmining asosi
- [Bozor sikllari](cycle-theory.md) — qo'shimcha kirish uchun trend qanchalik kuchli
- [Pozitsiya kalkulyatori](../tools/position-calculator.md) — umumiy xavfni hisoblash
