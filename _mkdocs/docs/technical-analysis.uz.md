# Texnik tahlil — kengaytirilgan qo'llanma

!!! info "🌐 Tarjima / Перевод"
    Bu — sahifaning oʻzbekcha versiyasi. Asl nusxasi rus tilida; tilni sahifa yuqorisidagi til tanlagich orqali almashtirish mumkin.
    *Это узбекская версия страницы; оригинал доступен на русском.*

> **O'quv materiali.** Barcha grafiklar — tushunchalarni tasvirlash uchun sintetik ma'lumotlar. Bu haqiqiy bozorning signallari yoki prognozlari emas.

## Mundarija

1. [Texnik tahlil g'oyasi](#1-texnik-tahlil-goyasi)
2. [Yapon shamlari: anatomiya](#2-yapon-shamlari-anatomiya)
3. [Reversal sham patternlari](#3-reversal-sham-patternlari)
4. [Trendlar](#4-trendlar)
5. [Qo'llab-quvvatlash va qarshilik](#5-qollab-quvvatlash-va-qarshilik)
6. [Harakatlanuvchi o'rtachalar (MA / EMA)](#6-harakatlanuvchi-ortachalar-ma--ema)
7. [RSI — nisbiy kuch indeksi](#7-rsi--nisbiy-kuch-indeksi)
8. [MACD](#8-macd)
9. [Bollinger Bands](#9-bollinger-bands)
10. [Grafik patternlar](#10-grafik-patternlar)
11. [Multi-timeframe analysis (MTF)](#11-multi-timeframe-analysis-mtf)
12. [Indikatorlarni ortiqcha to'plash haqida](#12-indikatorlarni-ortiqcha-toplash-haqida)
13. [Grafik tahlili tekshiruv ro'yxati](#13-grafik-tahlili-tekshiruv-royxati)

---

## 1. Texnik tahlil g'oyasi

Texnik tahlil (TA) Charlz Dounning uchta postulatiga asoslanadi:

1. **Narx hamma narsani hisobga oladi** — barcha yangiliklar, hisobotlar, his-tuyg'ular allaqachon joriy kotirovkaga kiritilgan.
2. **Narx trendlar bo'yicha harakatlanadi** — bozor tasodifiy emas, u yo'nalishlar hosil qiladi.
3. **Tarix takrorlanadi** — olomonning xulq-atvor patternlari qayta yuz beradi, chunki odamlar psixologiyasi 100+ yil ichida o'zgarmagan.

TA ni «sehrli narsa» deb ishonish shart emas. Bu narxning nima qilayotganini **tasvirlash tili**. Yaxshi treyder TA ni kristall shar sifatida emas, xarita sifatida ishlatadi.

---

## 2. Yapon shamlari: anatomiya

Sham — bir davr (M1, M5, H1, H4, D1…) uchun narxning grafik ko'rinishi.

![Sham anatomiyasi](images/candle-anatomy.png)

**Shamni hosil qiluvchi to'rtta narx — OHLC:**

| Qisq. | Bu nima |
|---|---|
| **O** (Open) | Davr ochilishi paytidagi narx |
| **H** (High) | Davr ichidagi maksimal narx |
| **L** (Low) | Davr ichidagi minimal narx |
| **C** (Close) | Davr yopilishi paytidagi narx |

**Tana** — Open va Close orasidagi to'rtburchak.
- Agar `Close > Open` — sham **buqali** (yashil/oq).
- Agar `Close < Open` — sham **ayiqli** (qizil/qora).

**Soyalar (fitillar)** — tananing yuqori va pastidagi chiziqlar, High va Low gacha. Ular **narx qaerga borgan, lekin o'sha yerda qolmagan**ini ko'rsatadi.

### Shamdan nima o'qish mumkin

- **Soyasiz katta tana** → kuchli harakat, bir tomonning nazorati
- **Uzun pastki soya + yuqorida kichik tana** → sotuvchilar bosdi, lekin xaridorlar narxni qaytardi → mumkin bo'lgan yuqoriga reversal
- **Uzun yuqori soya + pastda kichik tana** → xaridorlar ushlab turmadi → mumkin bo'lgan pastga reversal
- **Kichik tana, ikki tomondan uzun soyalar** → noaniqlik, kurash

---

## 3. Reversal sham patternlari

Patternlar **kontekstda** ishlaydi, mustaqil emas. Qo'llab-quvvatlash darajasida tushuvchi trendda bolg'a — signal. O'sha bolg'a yonma-yon harakatning o'rtasida — shovqin.

![Sham patternlari](images/candle-patterns.png)

### Bolg'a (Hammer)
- Yuqorida kichik tana, uzun pastki soya (≥ 2× tanadan)
- **Tushuvchi harakatning oxirida** paydo bo'ladi
- Xaridorlar nazoratni qo'lga oldi
- Tasdiqlash — keyingi buqali sham

### Buqali qamrab olish (Bullish Engulfing)
- Kichik ayiqli sham, keyin katta buqali sham, **tanasi oldingi shamning tanasini to'liq qoplaydi**
- **Tushuvchi harakatning oxirida** paydo bo'ladi
- Kayfiyat o'zgarishining kuchli signali

### Doji (Doji)
- Open ≈ Close, uzun soyalar
- **Noaniqlik** — buqali va ayiqli nazorat muvozanatga keldi
- Uzoq trenddan keyin asosiy darajadagi doji — ko'pincha reversalning oldindan belgisi
- Yonma-yon harakatdagi shovqindagi doji — e'tiborsiz qoldiring

### Tushuvchi yulduz (Shooting Star)
- Pastda kichik tana, uzun yuqori soya
- **Yuqoriga harakatning oxirida** paydo bo'ladi
- Bolg'aning ko'zgu aksi, pastga reversal signali

### Patternlardan foydalanish qoidalari

1. **Shakl emas, kontekst muhimroq.** Pattern to'g'ri joyda bo'lishi kerak: darajada, trenddan keyin.
2. **Tasdiqlashni kutish** — keyingi shamning to'g'ri tomonga yopilishi.
3. **Taymfreym qanchalik katta bo'lsa, pattern shunchalik ishonchli**. M1 da — shovqin. H4/D1 da — jiddiy signal.
4. **Faqat patternga asoslanib savdo qilmang** — indikatorlar va kontekst qo'shing.

---

## 4. Trendlar

Trend — davr ichida narxning yo'nalishi.

![Trend turlari](images/trend-types.png)

### Yuqoriga trend (Uptrend)
**Belgi:** **higher highs (HH) va higher lows (HL)** ketma-ketligi — har keyingi cho'qqi oldingisidan yuqori, har keyingi tub oldingisidan yuqori.

Strategiya: **faqat long** da savdo qilish, qo'llab-quvvatlash (trend chizig'i, EMA) ga orqaga qaytishlarda kirish.

### Pastga trend (Downtrend)
**Belgi:** **lower highs (LH) va lower lows (LL)** — har cho'qqi past, har tub past.

Strategiya: **faqat short** da savdo qilish, qarshilikka orqaga qaytishlarda kirish.

### Yonma-yon harakat / flat (Range)
**Belgi:** narx darajalar orasidagi gorizontal koridorda harakatlanadi.

Strategiya: qo'llab-quvvatlashda sotib olish, qarshilikda sotish. **Yangi boshlovchilar uchun xavfli** — o'tkazib yuborish ma'qulroq.

### Trendning asosiy qoidasi

> **The trend is your friend until it bends.**
>
> Trend — buzilgunga qadar do'stingiz.

**Tushuvchi trendda «tubini ushlashga» urinmang** — bu yangi boshlovchilar depozitini yo'qotishining asosiy sabablaridan biri. (Tizimli) reversalni kuting, keyin kiring.

### Trend o'zgarishini qanday aniqlash mumkin

Yuqoriga trend, narx oldingi minimumdan pastroq **lower low** qilganida buzilgan hisoblanadi. Tushuvchi trend uchun aksincha.

---

## 5. Qo'llab-quvvatlash va qarshilik

Bu bozor «eslab qoladigan» **narxning gorizontal darajalari**. Psixologik jihatdan: bu narxlarda o'tmishda ko'p bitimlar amalga oshirilgan → ko'p ishtirokchilar yana munosabat bildiradi.

![Qo'llab-quvvatlash va qarshilik](images/support-resistance.png)

- **Qo'llab-quvvatlash** — narx YUQORIGA sakragan daraja. Xaridorlar faol.
- **Qarshilik** — narx PASTGA sakragan daraja. Sotuvchilar faol.

### Darajalarni qanday topish mumkin

1. Kunlik (D1) yoki 4 soatlik (H4) grafikda kamida 2 marta narx burilgan **mahalliy maksimum va minimumlarni** toping.
2. Bu nuqtalar orqali **gorizontal chiziq** o'tkazing (yoki narx aniq nuqtada burilmagan bo'lsa, zona).
3. Teginishlar qanchalik ko'p bo'lsa, daraja shunchalik kuchli.

### Rol almashish printsipi

> **Proboydan keyin qo'llab-quvvatlash qarshilikka aylanadi va aksincha.**

Agar narx 1.0810 qo'llab-quvvatlashni pastga yorib o'tsa — 1.0810 endi qaytishda qarshilik sifatida ishlaydi.

### Darajalardan qanday savdo qilish

**1-variant: otisib ketish (rebound)**
- Narx kuchli darajaga yaqinlashmoqda
- Kichik taymfreymda — reversal sham patterni
- Darajadan narigi tomonda kichik stop bilan kirish

**2-variant: yorilish (breakout)**
- Narx darajani kuchli sham bilan yorib o'tadi (katta tana, katta hajm)
- **Retestni** kutish — darajaga pastdan/yuqoridan qaytish
- Yorilish yo'nalishida retestdan otib ketishda kirish

---

## 6. Harakatlanuvchi o'rtachalar (MA / EMA)

Harakatlanuvchi o'rtacha — so'nggi N davr uchun **silliqlangan narx**. Trendni va darajalarni aniqlashga yordam beradi.

![EMA misol](images/ema-example.png)

### Harakatlanuvchi o'rtachalar turlari

- **SMA (Simple Moving Average)** — yopilish narxlarining oddiy o'rtachasi. Sekin munosabat bildiradi.
- **EMA (Exponential Moving Average)** — eksponensial o'rtacha, **so'nggi shamlar ko'proq og'irlikka ega**. Tezroq munosabat bildiradi. **Treydingda ko'proq qo'llaniladi.**

### Mashhur davrlar

| Davr | Nima ko'rsatadi |
|---|---|
| EMA 9 / 21 | Qisqa muddatli trend, skalping uchun |
| **EMA 50** | O'rta muddatli trend, **dinamik qo'llab-quvvatlash/qarshilik** |
| **EMA 200** | Uzoq muddatli trend. **Asosiy «filtr»**: narx EMA200 dan yuqori = long-bias, past = short-bias |

### Qanday ishlatish

**1. Yo'nalish filtri**
- Narx > EMA200 → faqat long da savdo qilish
- Narx < EMA200 → faqat short da savdo qilish

**2. Dinamik qo'llab-quvvatlash/qarshilik**
- Yuqoriga trendda narx EMA50 ga qaytib, otib ketadi → kirish nuqtasi
- Tushuvchi trendda — aksincha

**3. Kesishishlar (Crossovers)**
- **Oltin xoch (Golden Cross):** EMA50 EMA200 ni pastdan yuqoriga kesib o'tadi → buqali signal
- **O'lim xochi (Death Cross):** EMA50 EMA200 ni yuqoridan pastga kesib o'tadi → ayiqli signal

> **⚠️ Kechikish.** MA har doim narxdan orqada qoladi, chunki o'tgan ma'lumotlar asosida hisoblanadi. Tez bozorlarda signal harakatdan keyin keladi. MA ni yagona filtr sifatida ishlatmang.

---

## 7. RSI — nisbiy kuch indeksi

**RSI (Relative Strength Index)** — 0 dan 100 gacha bo'lgan ossillyator. Narxning qanchalik «ortiqcha sotib olingan» yoki «ortiqcha sotilgan»ini ko'rsatadi.

![RSI misol](images/rsi-example.png)

### Formula (soddalashtirilgan)
```
RSI = 100 - 100 / (1 + RS)
RS  = N davr uchun o'rtacha o'sish / N davr uchun o'rtacha tushish
```

Standart davr — **14**.

### Zonalar

| Qiymat | Talqin |
|---|---|
| RSI > 70 | **Ortiqcha sotib olingan** — pastga orqaga qaytish mumkin |
| RSI 50–70 | Buqali bosim |
| RSI 30–50 | Ayiqli bosim |
| RSI < 30 | **Ortiqcha sotilgan** — yuqoriga sakrash mumkin |

### RSI dan qanday foydalanish kerak emas

❌ «RSI > 70 — sotamiz, RSI < 30 — sotib olamiz» — kuchli trendda RSI haftalar davomida 70+ zonasida qolishi mumkin, va u bo'yicha short = aniq mag'lubiyat.

### RSI dan to'g'ri foydalanish

**1. Orqaga qaytishdagi kirish nuqtasini tasdiqlash**
- Yuqoriga trendda orqaga qaytishni kutamiz
- Agar RSI 40–45 ga tushib, yuqoriga burila boshlasa → impuls tiklanmoqda → mumkin bo'lgan kirish

**2. Divergensiya (farqlanish)** — kuchli signal
- **Buqali divergensiya:** narx yangi minimumga tushadi, RSI esa yo'q (oldingi minimumdan yuqori). → Sotishlar zaiflashmoqda, yuqoriga reversal mumkin.
- **Ayiqli divergensiya:** narx yangi maksimumga chiqadi, RSI esa yo'q. → Xaridlar zaiflashmoqda, pastga reversal mumkin.

```
Narx:  /\    /\
      /  \  /  \      ← yangi maksimum (yuqorida)
     /    \/    \
                 \

RSI:   /\
      /  \  /\        ← oldingi maksimumdan PAST
     /    \/  \       = ayiqli divergensiya
              \
```

**3. Qizib ketish filtri**
- RSI > 75 bo'lsa long kirmaslik (signal bo'lsa ham)
- RSI < 25 bo'lsa short kirmaslik

---

## 8. MACD

**MACD (Moving Average Convergence Divergence)** — bitta vositada trend + momentum.

![MACD misol](images/macd-example.png)

### Komponentlar

```
MACD chizig'i = EMA(12) - EMA(26)
Signal chizig'i = MACD ning EMA(9) si
Gistogramma = MACD - signal
```

### Signallar

**1. MACD va signal kesishishi**
- MACD signal chizig'ini **pastdan yuqoriga** kesib o'tadi → buqali signal
- MACD signal chizig'ini **yuqoridan pastga** kesib o'tadi → ayiqli signal
- **Kuchli flatda noto'g'ri signallar beradi** — trend bilan filtrlang

**2. Nol chizig'ini kesib o'tish**
- MACD 0 dan yuqori → buqalar nazorat qilmoqda
- MACD 0 dan past → ayiqlar nazorat qilmoqda
- 0 ni pastdan yuqoriga kesib o'tish = buqali trendning kuchayishi

**3. Divergensiya** (RSI dagidek)
- Narx yangi ekstremumga chiqadi, MACD esa yo'q → zaiflashish, reversal mumkin

### MACD ishlamaydigan holatlar

- **Kichik taymfreymlarda** (M1–M15) — juda ko'p shovqin
- **Flat bozorda** — bir qator noto'g'ri kesishishlar beradi
- **Kuchli trendlarda** kirish bilan kechikadi

---

## 9. Bollinger Bands

**Bollinger Bands** — volatillik indikatori. Uch chiziq:

![Bollinger Bands](images/bollinger-example.png)

- **O'rta** — SMA(20) — oddiy harakatlanuvchi o'rtacha
- **Yuqori** = SMA(20) + 2 × narx standart og'ishi
- **Pastki** = SMA(20) − 2 × standart og'ish

Narx statistik jihatdan **vaqtning 95% ini tasmalar orasida o'tkazadi**.

### Tasmalar nima ko'rsatadi

- **Tor tasmalar (squeeze)** — past volatillik → tez orada **harakat portlashi** (lekin yo'nalish noma'lum!)
- **Kengaygan tasmalar** — yuqori volatillik → o'rtachaga qaytish mumkin
- **Yuqori tasmaga tegish** — joriy diapazon uchun nisbatan yuqori narx
- **Pastki tasmaga tegish** — nisbatan past narx

### Bollinger Bands strategiyalari

**1. O'rtachaga qaytish (mean reversion) — flat uchun**
- Narx pastki tasmaga tegdi → long qidirish
- Narx yuqori tasmaga tegdi → short qidirish
- Maqsad — o'rta chiziq
- **FAQAT flatda ishlaydi**, trendda zarar keltiradi

**2. Squeeze dan chiqish**
- Tasmalar maksimal darajada torayladi
- Tasmalardan birini yorib o'tadigan keskin shamni kutamiz
- Yorilish yo'nalishida kiramiz
- Stop — qarama-qarshi tasma orqasida

**3. «Tasma bo'ylab yurish» (walking the band)**
- Kuchli trend → narx yuqori (long) yoki pastki (short) tasma BO'YLAB ketadi
- Bu **trend kuchining belgisi**, reversal signali emas
- Yangi boshlovchilarning keng tarqalgan xatosi: «yuqori tasmaga tegdi» deb short qilish

---

## 10. Grafik patternlar

Bu narxning oy davomida ishtirokchilar psixologiyasi asosida grafikda chizadigan shakllari.

![Grafik patternlar](images/chart-patterns.png)

### Bosh va yelkalar (Head & Shoulders)
**Reversal** cho'qqi patterni:
- Chap yelka → orqaga qaytish → bosh (yuqoriroq) → orqaga qaytish → o'ng yelka (taxminan chap yelka darajasida)
- **Bo'yin chizig'i** (neckline) — yelkalar ostidagi qo'llab-quvvatlash
- Bo'yin chizig'ini pastga yorish = short signali
- **Maqsad** = bosh cho'qqisidan bo'yingacha bo'lgan masofa, bo'yndan pastga o'lchangan

Ko'zgu patterni — **teskari bosh va yelkalar** (pastda, o'sishdan oldin).

### Ikki cho'qqi / ikki tub
**Reversal**:
- Narx ikki marta darajani yorishga urinadi, uddasidan chiqa olmaydi
- Ikki cho'qqi = bo'yin chizig'ini yorishdan keyin short signali
- Ikki tub = long signali

Cho'qqilar/tublar orasidagi vaqt masofasi qanchalik katta bo'lsa, pattern shunchalik kuchli.

### Uchburchaklar
**Trend davomi:**
- **Yuqoriga uchburchak** — yuqorida gorizontal qarshilik, pastda yuqoriga yo'nalgan qo'llab-quvvatlash. Ko'pincha yuqoriga yorish.
- **Pastga uchburchak** — gorizontal qo'llab-quvvatlash, pastga yo'nalgan qarshilik. Ko'pincha pastga yorish.
- **Simmetrik uchburchak** — ikki tomon yaqinlashadi. Har qaysi tomonga yorish, yo'nalish oldindan aniqlanmaydi.

### Bayroq / vimpel
**Trend davomi:**
- Kuchli impuls → qisqa yonma-yon/qiyshiq konsolidatsiya → impuls yo'nalishida davom etish
- Intradey savdoda eng ko'p «savdo qilinadigan» pattern

### Patternlar haqida muhim

⚠️ **Patternlar sub'ektivdir.** Bir xil grafikni 5 treyder har xil ko'radi. Shuning uchun:

1. **Daraja yorilishi** bilan tasdiqlang («shakllanayotgan» patternga ishonmang)
2. Stopni **patternning qarama-qarshi tomoniga** qo'ying
3. Maqsad sifatida **pattern balandligini** yorilish nuqtasidan o'lchang
4. Chiziqlarni cho'zmang — agar pattern aniq ko'rinmasa, u yo'q, degan ma'no

---

## 11. Multi-timeframe analysis (MTF)

Bir xil grafik M1, H1 va D1 da har xil ko'rinadi. Profesionallar **kamida 3 ta taymfreymni** tahlil qiladi.

### Swing-treydingga tavsiya etilgan kombinatsiya

| Taymfreym | Nima aniqlanadi |
|---|---|
| **D1 (kunlik)** | Asosiy trend, qo'llab-quvvatlash/qarshilikninh asosiy darajalari |
| **H4 (4 soatlik)** | O'rta muddatli trend, ishchi darajalar, EMA200 |
| **H1 (soatlik)** | Kirish nuqtasi, sham patterni, EMA50 |
| ~~M5/M1~~ | **Yangi boshlovchi e'tiborga olmaydi** — shovqin, his-tuyg'ular |

### Moslashtirish qoidasi

**Savdoni faqat barcha taymfreymlar bir xil narsa ko'rsatayotganda oching.**

Long-setup misoli:
- D1: yuqoriga trend (HH/HL)
- H4: narx EMA200 dan yuqori, qo'llab-quvvatlash zonasiga orqaga qaytdi
- H1: EMA50 dan buqali pattern (bolg'a, qamrab olish)

Agar D1 tushuvchi, H1 esa «buqali reversal» chizayotgan bo'lsa — bu **kontrtrenddir** va deyarli har doim tuzoq.

---

## 12. Indikatorlarni ortiqcha to'plash haqida

Keng tarqalgan xato: platformani ochib, «ishonchlilik uchun» 7 ta indikator osish. Bu:
- qaror qabul qilishni sekinlashtiradi,
- **nazorat illuziyasi** yaratadi,
- qarama-qarshi signallar beradi (biri buy, boshqasi sell — falaj),
- aniqlikni oshirmaydi.

### Yangi boshlovchi uchun minimal to'plam

1. **Narx + shamlar** (har doim)
2. **EMA 50 va EMA 200** (trend va dinamik qo'llab-quvvatlash)
3. **RSI(14)** (qizib ketish filtri, divergensiyalar) YOKI **MACD** — bittasini tanlang
4. **Gorizontal qo'llab-quvvatlash/qarshilik darajalari** — o'zingiz chizasiz

Bu kamida bir yillik savdo uchun yetarli.

### Nima qo'shish mumkin (faqat asosni ishonchli egallagandan keyin)

- Fibonacci retracement — orqaga qaytish maqsadlarini aniqlash uchun (38.2%, 50%, 61.8%)
- Pivot Points — intradey darajalar
- Volume Profile — eng yuqori likvidlik qayerda bo'lgan
- ATR — volatillik bo'yicha stoplarni hisoblash uchun

---

## 13. Grafik tahlili tekshiruv ro'yxati

Har bir savdodan oldin bu ro'yxatni bajaring:

```
─── KONTEKST ───
☐ D1: asosiy trend qanday? (yuqori / past / flat)
☐ D1 da yaqinida asosiy darajalar bormi?

─── YO'NALISH ───
☐ H4: narx EMA200 dan yuqorimi yoki pastmi?
☐ H4 tuzilmasi trendni tasdiqlayaptimi (HH/HL yoki LH/LL)?

─── KIRISH NUQTASI ───
☐ H1: dinamik qo'llab-quvvatlashga (EMA50) orqaga qaytish bormi?
☐ H1: to'g'ri yo'nalishda sham patterni bormi?
☐ RSI ekstremal zonada emasmi?

─── BAJARISH ───
☐ Stop hisoblab qo'yildimi (swing / daraja orqasida)?
☐ Teyk hisoblandimi, R:R ≥ 1:2?
☐ Pozitsiya hajmi = 0.5–1% xavf?

─── YANGILIKLAR FILTRI ───
☐ Keyingi 2 soatda qizil yangiliklar yo'qmi?
☐ Juma kechqurun emasmi (bozor yopiladi)?

─── PSIXOLOGIYA ───
☐ Men tinchman, «o'ch olmoqchi» emasman?
☐ Bu qoidalarga asoslangan savdo, intuitsiyo emasmi?

BARCHA ☐ BELGILANGAN → ochish mumkin.
KAMIDA BITTASI YO'Q → savdo YO'Q.
```

Bu ro'yxatni chop etib, savdoning birinchi 6 oyi davomida kompyuter yoniga ilib qo'ying.

---

[← Asosiy qo'llanmaga qaytish](../forex-guide.md) · [Strategiya →](strategy-details.md)
