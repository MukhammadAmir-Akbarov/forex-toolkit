---
widgets: [chapter-quiz]
---

# 🛡️ Seyf (Move to Breakeven) — stop-lossni zararsizlik nuqtasiga ko'chirish

!!! abstract "Amaliyotdan (arxivda 509 ta eslatma)"
    «Seyf» — MDH treyderlik doiralarida ishlatiladigan o'zbek-rus atamasi. **Stop Loss ni kirish nuqtasiga ko'chirish** demak — shu tarzda pozitsiyada yo'qotish imkonsiz bo'lib qoladi.

    2 yillik amaliyot arxivida bu texnikaning **509 ta eslatmasi** bor. Bu eng ko'p ishlatiladigan himoya usuli.

---

## 🎯 «Seyf» nima

```
BUY 1.0850 da ochdik
Stop Loss: 1.0800 (50 pip xavf)
Take Profit: 1.0950 (100 pip maqsad)

Narx yuqoriga 1.0900 ga bordi (+50 pip foyda)

→ Stop Loss ni 1.0800 dan 1.0850 ga (kirish nuqtasiga) ko'chiramiz
→ Endi narx qaytsa ham — BIZ YO'QOTMAYMIZ

Bu — «seyf», zararsiz pozitsiya.
```

!!! tip "Psixologik samara"
    BU ga ko'chirgandan so'ng **mutlaqo xotirjamsan**. Savdo yangi stop narxida kichik foydada yopilishi yoki to'liq TP ga yetishi mumkin. **Minus imkonsiz.**

    Bu katta stressni olib tashlaydi va keyingi savdolarga e'tibor qaratishga imkon beradi.

---

## 📐 Seyfga qachon ko'chirish — aniq qoidalar

### 1-qoida: TP gacha bo'lgan masofaning 50% ga yetildi

```
Kirish: 1.0850
SL: 1.0800 (50 pip xavf)
TP: 1.0950 (100 pip maqsad)

→ Narx 1.0900 ga yetganda (TP yo'lining 50%) — SL ni BU ga ko'chir
```

### 2-qoida: 1:1 RR darajasiga yetildi

Foyda dastlabki xavf hajmiga tenglaship ketishi bilanoq (RR=1), BU ga ko'chir.

```
Agar SL = 30 pip bo'lsa, +30 pip foydadan keyin BU ga ko'chir
Agar SL = 50 pip bo'lsa, +50 pip foydadan keyin BU ga ko'chir
```

### 3-qoida: Narx eng yaqin qarshilik darajasiga yetdi

TP yo'lida **kuchli qarshilik** (BUY uchun) yoki **qo'llab-quvvatlash** (SELL uchun) mavjud bo'lsa — undan oldin albatta BU ga ko'chir. Narxning orqaga qaytish ehtimoli yuqori.

### 4-qoida: Qizil yangilikdan oldin

**Muhim yangilikdan 15-30 daqiqa oldin** (NFP, CPI, FOMC) — barcha ochiq pozitsiyalarni albatta BU ga ko'chiring yoki qisman yoping.

---

## ⚠️ Seyfga qachon ko'chirmaslik kerak

### ❌ Juda erta

SL ni BU ga narx TP ga boradigan yo'lning atigi 10-20% ni bosib o'tganda ko'chirsangiz — **orqaga qaytishda chiqarib yuboradi** va siz o'sishni o'tkazib yuborasiz.

Bozor nafas oladi. **Unga orqaga qaytish uchun joy bering.**

### ❌ Harakatdan oldingi konsolidatsiyada

Narx +20 pip o'tib, konsolidatsiyada (flat) to'xtab qolgan bo'lsa — darhol ko'chirmang. Ko'chirishni o'z tomoning darajasi **singanidan keyin** bajaring.

### ❌ Strukturaviy jihatdan savdo harakatni hali isbotlamagan bo'lsa

BU ga ko'chirish kirish nuqtasidan kamida bitta HH (BUY uchun Higher High) yoki LL (SELL uchun Lower Low) shakllanganidan **keyin** bo'lishi kerak.

---

## 🔢 «Seyf» matematikasi

### Seyfsiz:

```
Bir xil lot bilan 10 ta savdo
Xavf: savdoga 1%, RR = 1:2

Ssenariy: 5 g'alaba, 5 mag'lubiyat
Win: +5 × 2% = +10%
Loss: -5 × 1% = -5%
Jami: +5%
```

### Seyf bilan (to'g'ri qo'llanilganda):

```
10 ta savdo, xavf 1%, RR = 1:2, TP ga +50% da seyf
5 «g'alaba»dan — 2 tasi BU ga chiqdi (seyfdan keyin qaytdi) = +0%
5 «mag'lubiyat»dan — 0 ta zarar (ba'zilari ham BU ga chiqdi)

3 g'alaba × 2% = +6%
3 BU × 0% = 0%
4 mag'lubiyat × 1% = -4%
Jami: +2%

⚠️ Juda erta ko'chirilsa — natija yomonroq bo'lishi mumkin!
```

**Xulosa:** seyf xavfni kamaytiradi, lekin **foydani ham kamaytirishi mumkin**. Muvozanat aniq hisoblangan bo'lishi kerak.

---

## 🎯 Seyf vs Trailing Stop

| Parametr | Seyf (qat'iy BU) | Trailing Stop (suruvchi) |
|---|---|---|
| Murakkablik | ✅ Oddiy | ⚠️ Sozlash talab etadi |
| Qachon ishga tushadi | Oldindan belgilangan darajadan keyin | Narx ortidan doimo siljib turadi |
| «Shovqin» bilan chiqarib yuborish xavfi | Past | Yuqori (tor bo'lsa) |
| Mos keladi | Skalping, yangiliklar | Swing, trendli harakatlar |
| Hissiy yuklanma | Past | Past |

**Yangi boshlovchi uchun tavsiya:** oddiy «Seyf» dan boshlang. Trailing — 6+ oy amaliyotdan keyin.

---

## 📋 «Seyf qilsa bo'ladimi?» tekshiruv ro'yxati

SL ni BU ga ko'chirishdan oldin tekshiring:

- [ ] Kirishdan TP gacha bo'lgan yo'lning kamida 50% bosib o'tildi
- [ ] Narx yumaloq raqamda emas (1.0900, 2000.00) — u yerda tez-tez orqaga qaytishlar bo'ladi
- [ ] Orqamda yaqin qarshilik/qo'llab-quvvatlash yo'q
- [ ] Qizil yangilikgacha 30 daqiqadan ko'proq vaqt bor (yoki yangilik SABABLI ko'chirilyapman)
- [ ] SL ni ortiqcha foydaga ko'chirmayman (ya'ni «BU dan yaxshiroq») — faqat BU ga
- [ ] Broker SL o'zgartirishga ruxsat beradi (Trading Halt emas)

---

## 💬 Amaliyotchi iqtibosi

!!! quote
    *«+50 пипс ✅✅ сейф киламиз - сессия алмашадиган пайтга келиб колди»*

    **Tarjima:** «+50 pipda ✅✅ seyf qilamiz — sessiyalar almashadigan vaqt keldi.»

G'oya: **sessiya almashinuvi (London → NY, NY → Osiyo) = narx burilish xavfi**. Pozitsiyani himoyalash shart.

---

---

<div id="chapter-quiz" data-quiz-key="breakeven-protocol"></div>
<script type="application/json" id="chapter-quiz-questions">
[
  {
    "q": "«Seyf» (zararsizlikka o'tkazish) nima?",
    "options": [
      "Pozitsiyani qo'lda nolga yopish",
      "Stop Lossni kirish narxiga ko'chirish — pozitsiya bo'yicha zarar imkonsiz bo'ladi",
      "Pozitsiyani brokerda sug'urtalash",
      "Foydadan keyin lotni ikki baravar qilish"
    ],
    "answer": 1,
    "explain": "SL kirish nuqtasiga ko'chgach, narx qaytishi mumkin, lekin minus istisno: bitim nol yoki plyusda yopiladi."
  },
  {
    "q": "Stopni zararsizlikka qachon ko'chirish to'g'ri?",
    "options": [
      "Bitim ochilishi bilanoq",
      "Narx TPgacha yo'lning 10%ini o'tganda",
      "1:1 RRga yetganda, TPgacha yo'lning 50%ida yoki kuchli daraja oldida",
      "Faqat savdo kuni oxirida"
    ],
    "answer": 2,
    "explain": "Juda erta ko'chirish pozitsiyani oddiy korreksiya bilan urib tashlaydi. Mo'ljallar: TPgacha 50% yo'l, foyda = risk (1:1), kuchli daraja yoki oldinda qizil yangilik."
  },
  {
    "q": "Nega stopni zararsizlikka juda erta ko'chirmaslik kerak?",
    "options": [
      "Broker erta ko'chirishni taqiqlaydi",
      "Bozor «nafas oladi»: korreksiya asosiy harakatgacha pozitsiyani urib tashlaydi",
      "Ko'chirish komissiyasi oshadi",
      "Take-profit bekor qilinadi"
    ],
    "answer": 1,
    "explain": "Narxga erk bering: ko'chirish struktura harakatni tasdiqlagach (kirish nuqtasidan yangi HH/LL) amalga oshiriladi."
  }
]
</script>

## 🔗 Keyingi nima o'qish kerak

- [Qo'shimcha kirish](scaling-in.md) — teskari texnika: foydali pozitsiyaga qo'shilish
- [LOT-disciplina](lot-discipline.md) — hamma narsaning asosi
- [Treyding psixologiyasi](../extras/psychology.md) — nega BU ga juda erta ko'chirishdan qo'rqasan
- [Pozitsiya kalkulyatori](../tools/position-calculator.md) — to'g'ri hisoblangan pozitsiya seyf bo'yicha qarorlarni osonlashtiradi
