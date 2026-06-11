# Order Flow va Volume Profile — ilg'or texnik tahlil

> Bu — **«asosdan keyin»** daraja. Avval shamlar, EMA, RSI va asosiy strategiyani o'zlashtirib oling. Bu bo'limni **6+ oylik** amaliyotdan so'ng, bozor staqanida nima bo'layotganini chuqurroq tushunmoqchi bo'lganingizda oching.

## Nima uchun kerak

Klassik TA (shamlar, indikatorlar) — bu **narx bilan nima bo'lganini** ko'rsatadi.
Order Flow / Volume Profile — bu **kim savdo qilganini va qanday hajmlarda** ko'rsatadi.

Professional treyderlar **hajmlarga qaraydi**, chunki hajmsiz narx — bu aldamchi tasvir. Hajmsiz darajani sinishi ko'pincha soxta, katta hajm bilan sinishi esa haqiqiy sinish.

---

## 1. Tushunchalar

### 1.1 Order Book (staqan)

Real vaqt rejimida birja **narx darajalari bo'yicha bid/ask ni** ko'rsatadi:

```
                ASK (sotuvchilar)
   1.0855  ┃ 2 500 000 lot
   1.0854  ┃ 1 800 000 lot
   1.0853  ┃   500 000 lot
─── joriy narx ────
   1.0852  ┃   400 000 lot
   1.0851  ┃ 1 200 000 lot
   1.0850  ┃ 3 000 000 lot
                BID (xaridorlar)
```

- **Xaridorlarning katta devori** joriy narxdan pastda → qo'llab-quvvatlash
- **Sotuvchilarning katta devori** tepada → qarshilik
- **Yupqa likvidlik** → narx darajani tez o'tib ketadi

⚠️ **Muhim:** Forexda staqan chakana treyderlar uchun **mavjud emas** (bu OTC bozor). Kriptobirzha va fond bozoridan farqli o'laroq.

### 1.2 Volume Profile (hajm profili)

Grafikning o'ng tomonidagi vertikal gistogramma, har bir narx darajasida **qancha hajm o'tganini** davr uchun ko'rsatadi:

```
Narx │
1.090 ┃▓▓
1.088 ┃▓▓▓▓▓
1.086 ┃▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ← POC (Point of Control)
1.084 ┃▓▓▓▓▓▓▓▓▓▓
1.082 ┃▓▓▓
1.080 ┃▓
      └────────────
```

Asosiy atamalar:
- **POC (Point of Control)** — maksimal hajmli daraja. Eng «adolatli» narx.
- **Value Area (VA)** — hajmning 70% o'tgan diapazon
- **Value Area High (VAH)** — Value Areaning yuqori chegarasi
- **Value Area Low (VAL)** — Value Areaning quyi chegarasi
- **HVN (High Volume Node)** — yuqori hajmli zona — qo'llab-quvvatlash/qarshilik
- **LVN (Low Volume Node)** — past hajmli zona — narx undan tez o'tib ketadi

### 1.3 ICT tushunchalari (Inner Circle Trader)

Mashhur metodologiya (Maykl Xaddlston). Asosiy tushunchalar:

- **Liquidity** — ko'pchilik treyderlarning stoplari turgan joy (swing high tepasida / swing low pastida)
- **Liquidity sweep** — bozor burilishdan oldin bu stoplarni yig'ib oladi
- **Order Block** — kuchli impulsdan oldingi oxirgi sham, ko'pincha qo'llab-quvvatlash/qarshilik sifatida ishlaydi
- **Fair Value Gap (FVG)** — shamlar orasidagi bo'shliq, bozor uni ko'pincha to'ldiradi
- **Smart Money Concept (SMC)** — katta o'yinchilar narxni manipulyatsiya qiladi degan nazariya

⚠️ **ICT — bahsli maktab.** Ko'pchilik «oddiy narsalarning ortiqcha murakkab tushuntirilishi» deb tanqid qiladi. Tanqidiy fikr bilan o'rganing.

---

## 2. Forexda hajmni qayerdan olish

Forex markazlashtirilmagan bo'lganligi sababli, **haqiqiy hajm mavjud emas**. Vositachi ko'rsatkichlardan foydalaniladi:

### 2.1 Tick Volume

Har bir narx o'zgarishi = 1 tik. Tik hajm = sham uchun tik soni. Bu faollikning **bilvosita** ko'rsatkichi.

MT5 da: grafik ustida o'ng tugma → **Volumes** → **Tick Volume**.

### 2.2 Futures Volume (aniqroq)

**Fyuchers bozoridan** (CME) real hajm:
- **6E** — EUR/USD fyuchersi
- **6B** — GBP/USD fyuchersi
- **6J** — JPY fyuchersi

CME data (pullik) yoki TradingView (Pro obuna) orqali yuklab olish mumkin.

### 2.3 Ma'lumot agregatorlari

Bir necha brokerdan hajmlarni agregirlash xizmatlari:
- **Volfix** (pullik)
- **ATAS** (pullik, prop-treyderlar uchun)
- **Sierra Chart** (pullik, nisbatan arzonroq)

Ko'pchilik chakana treyderlar uchun — **tick volume yetarli**.

---

## 3. Volume Profile bilan oddiy strategiyalar

### 3.1 POC Magnet

**G'oya:** Narx oldingi kun/hafta POC siga «magnit kabi tortiladi».

```
Harakatlar:
1. Kecha uchun Volume Profile quring (D1)
2. POC ni toping
3. Agar bugun narx POC dan uzoqda bo'lsa — qaytishni kuting
4. POC ni test qilgandan + sham patternidan keyin kirish
```

### 3.2 Value Area Rejection

**G'oya:** Narx VAH / VAL dan qaytadi.

```
Harakatlar:
1. Kechagi kunning VAH va VAL ini toping
2. Narx pastdan VAL ga yaqinlashib qaytsa → long
3. Narx tepadan VAH ga yaqinlashib qaytsa → short
4. Stop VA tashqarisida
5. Maqsad — POC
```

### 3.3 LVN Breakout

**G'oya:** Narx past hajmli zonalardan tez o'tib ketadi.

```
Harakatlar:
1. LVN ni toping (yupqa ustunli zonalar)
2. Narx LVN tomonga harakatlana boshlasa — u ko'pincha tez o'tadi
3. Harakat yo'nalishida kirish, maqsad — keyingi HVN
4. Stop oxirgi swing ostida
```

---

## 4. MT5 ga Volume Profile qo'shish

MT5 da o'rnatilgan Volume Profile yo'q. Quyidagilar kerak:

### A variant: bepul indikator
1. mql5.com dan yuklab olish: «Volume Profile» (bepul versiyalari mavjud)
2. MetaEditor orqali: File → Open Data Folder → MQL5/Indicators
3. .mq5 / .ex5 faylni joylash
4. MT5 da: Refresh → grafik ustiga sudrab olib borish

### B variant: TradingView (tavsiya etaman)
1. TradingView da: Indicators → Volume Profile Visible Range
2. Asosiy versiya uchun bepul
3. MT5 ga qaraganda ancha ko'rgazmali

### V variant: ATAS / Sierra Chart
- Professional platformalar
- $50-200/oy
- To'liq Order Flow + Volume Profile + Footprint

---

## 5. Footprint Charts (Order Flow Bars)

Bu — shamlarning evolyutsiyasi: har bir sham ichida **har bir darajada qancha xarid va sotuv bo'lganini** ko'rsatadi:

```
EUR/USD H1 — Footprint:

1.0855  10 × 50       (10 xarid, 50 sotuv — ayiqlar bosimda)
1.0854  120 × 80      (balans)
1.0853  200 × 150     (buqalar biroz oldinda)
1.0852  50 × 300      (ayiqlar bosimda)
```

Shamning faqat natijasini emas, balki **sham ichidagi** xaridorlar va sotuvchilar **nomutanosibligini** ko'rishga yordam beradi.

Mavjud: **ATAS, Sierra Chart, TradingView (Pro+)**.

---

## 6. Buni o'rganish kerakmi?

### O'rganish kerak, agar:
- Asoslar bo'yicha 1+ yil muvaffaqiyatli savdo qilgan bo'lsangiz
- Klassik indikatorlar kamlik qilayotganini his qilsangiz
- Yangi tizimni 6+ oy o'rganishga tayyor bo'lsangiz
- Sifatli ma'lumotlar uchun $50-200/oy to'lashga tayyor bo'lsangiz

### O'rganmaslik kerak, agar:
- Yangi boshlovchisiz (6 oydan kam tajriba)
- Asosiy strategiyalar hali foyda bermayapti
- Intizom o'rniga «sir» izlayotgan bo'lsangiz
- Uzoq o'rganishga tayyor bo'lmasangiz

---

## 7. Order Flow / Volume Profile bo'yicha kitoblar

1. **«Mind Over Markets»** — Peter Steidlmayer (Market Profile ning yaratuvchisi)
2. **«Trading with Market Statistics»** — Tom Alexander
3. **«The Daily Trading Coach»** — Brett Steenbarger (professional psixologiyasi haqida)
4. **«Reading Price Charts Bar by Bar»** — Al Brooks

---

## 8. Bepul resurslar

- **YouTube kanali «AxiaFutures»** — institutsional qarashlar
- **Volumetrica blog** — hajmlar bo'yicha maqolalar
- **r/Daytrading subreddit** — professional muhokamalar
- **TradingView Education**

---

## 9. Realistik kutishlar

Order Flow va Volume Profile — bu **vositalar**, sehrli narsa emas.

Ular BERMAYDI:
- «Aniq kirish/chiqish signallari»
- 90% aniqlik
- Stopsiz savdo qilish imkoniyati
- Har qanday taymfreymda foyda

Ular BERADI:
- Bozor kontekstini yaxshiroq tushunish
- Likvidlik haqida fikrlar
- Klassik setaplar uchun qo'shimcha filtr
- Qaror qabul qilishda ishonch (uzoq o'rganishdan so'ng)

---

## 10. Boshlash uchun qadamlar

1. **Bugun:** TradingView ni o'rnating, EUR/USD da Volume Profile Visible Range ni qo'shing
2. **Bir hafta:** kuzating — har kuni POC, VAH, VAL qayerda. Darajalarni yozib oling.
3. **Bir oy:** bu darajalar va narx harakatlari orasidagi bog'liqlikni toping
4. **3 oy:** oddiy strategiyani sinab ko'ring (masalan, POC Magnet) demoda
5. **6 oy:** agar ishlasa — asosiy strategiyangizga **filtr** sifatida qo'shing

**Shoshilmang.** Volume Profile sizda ishlayotgan narsani almashtirmasdan, **to'ldirishi** kerak.

---

[← Texnik tahlilga](../docs/technical-analysis.md) · [← Asosiy qo'llanmaga](../forex-guide.md)
