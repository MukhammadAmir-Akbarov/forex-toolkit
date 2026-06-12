# 📡 Yangiliklar asosida savdo — xavfsiz kirish protokoli

!!! abstract "Nima uchun bu muhim"
    Yangiliklar — **pozitsion treyder uchun eng xavfli lahza** va **impuls trejderi uchun
    eng yaxshi lahza**. Zarar va foyda o'rtasidagi farq — bu **protokol**: NIMA savdo qilish,
    QANDAY savdo qilish va QACHON umuman savdo qilmaslikni bilish.

!!! danger "Xavf haqida ogohlantirish"
    Yangiliklar asosida savdo **ekstremal o'zgaruvchanlik**, spredning kengayishi, slippage
    va boʻshliqlar bilan bog'liq. Yangi boshlovchilarga 3+ oy demo hisob tajribasi to'planmaguncha
    yirik relizlardan 30 daqiqa oldin/keyin savdo qilmaslik **tavsiya etiladi**.

---

## Mundarija

1. [Nima uchun yangiliklar bozor uchun shunchalik xavfli](#1-nima-uchun-yangiliklar-bozor-uchun-shunchalik-xavfli)
2. [Iqtisodiy kalendar — o'qish usuli](#2-iqtisodiy-kalendar--oqish-usuli)
3. [Asosiy voqealar — muhimlik ierarxiyasi](#3-asosiy-voqealar--muhimlik-ierarxiyasi)
4. [Xavfsiz yangiliklar savdo strategiyalari](#4-xavfsiz-yangiliklar-savdo-strategiyalari)
5. [NFP taktikasi](#5-nfp-taktikasi)
6. [FOMC (Fed majlisi) taktikasi](#6-fomc-fed-majlisi-taktikasi)
7. [Yangiliklar savdosida Stop-Loss](#7-yangiliklar-savdosida-stop-loss)
8. [Kirishdan oldingi tekshiruv ro'yxati](#8-kirishdan-oldingi-tekshiruv-royxati)

---

## 1. Nima uchun yangiliklar bozor uchun shunchalik xavfli

Asosiy ma'lumotlar e'lon qilinganda quyidagilar sodir bo'ladi:

1. **Algoritm treyderlar** (HFT-botlar) ma'lumotlarni **millisekundlar ichida** o'qiydi va kotirovkalarni darhol qayta belgilaydi
2. **Spred kengayadi** — ba'zi juftliklarda reliz paytida 0,5 pipdan 20–50 pipga qadar
3. **Likvidlik yo'qoladi** — brokerlar savdoning «noto'g'ri» tomonida qolmaslik uchun orderlarni kitobdan olib tashlaydi
4. **Slippage** — Market-orderlar kutilgandan 5–30 pip yomonroq bajariladi

```
Misol: NFP prognozdan ancha kuchli chiqdi
Relizdan oldin: EUR/USD bid/ask = 1.08450 / 1.08453 (spred 0.3 pip)
Reliz lahzasi: spred 1.07900 / 1.09000 ga kengayadi (!!!!)
2–3 soniyadan keyin: 1.07980 / 1.07990 — bozor yangi narxni «topdi»
```

Agar 1.08100 da Sell-stop turgan bo'lsa — u 1.07920 da bajariladi (18 pip slippage).

---

## 2. Iqtisodiy kalendar — o'qish usuli

Asosiy manbalar (bepul, tarix va prognozlar bilan):
- **Forex Factory** (forexfactory.com) — sanoat standarti
- **Investing.com** — mamlakat bo'yicha filtrlar bilan
- **Dailyfx.com** — tahlil bilan

### Forex Factory rang maʼnolari:

| Rang | Muhimlik | Nima qilish kerak |
|---|---|---|
| 🔴 Qizil | Yuqori — bozor 50–300+ pip harakat qilishi mumkin | **Pozitsiyalarni yoping** yoki kirmang |
| 🟠 To'q sariq | O'rta — 10–50 pip harakat | Ehtiyot bo'ling, hajmni kamaytiring |
| 🟡 Sariq | Past — 10 pipdan kam | Odatda e'tiborsiz qoldirish mumkin |

### Kalendarndagi uch raqam:

```
Voqea: Non-Farm Payrolls (NFP)
Oldingi: 175K  ← o'tgan oy (qayta ko'rib chiqilishi mumkin)
Prognoz: 180K  ← analitiklar konsensusi
Haqiqiy: 220K  ← reliz paytida paydo bo'ladi
```

**Bozor reaktsiyasi mantiqi:**
- Haqiqiy >> Prognoz → **ijobiy kutilmagan natija** → mamlakat valyutasi kuchayadi
- Haqiqiy << Prognoz → **salbiy kutilmagan natija** → mamlakat valyutasi zaiflashadi
- Haqiqiy ≈ Prognoz → zaif reaktsiya yoki «yangilikda sotish»

!!! warning "«Mish-mishda sotib ol, yangilikda sot»"
    Bozor ko'pincha kutilgan ma'lumotlarni narxga **allaqachon kiritgan** bo'ladi.
    NFP prognoz bo'yicha chiqsa — reaktsiya bo'lmasligi yoki teskari yo'nalishi mumkin.

---

## 3. Asosiy voqealar — muhimlik ierarxiyasi

### 1-daraja (🔴🔴🔴 — pozitsiyalarni albatta yoping)

| Voqea | Valyuta | Chastotasi | Kutilgan harakat |
|---|---|---|---|
| **NFP** (Non-Farm Payrolls) | USD | Har oyning 1-juma kuni | 80–200 pip |
| **FOMC foiz stavkasi qarori** | USD | Yiliga 8× | 100–300 pip |
| **FOMC Matbuot anjumani** | USD | Yiliga 8× | 50–150 pip |
| **ECB stavka qarori** | EUR | Yiliga 8× | 80–200 pip |
| **BoE stavka qarori** | GBP | Yiliga 8× | 80–200 pip |
| **AQSh CPI** (inflyatsiya) | USD | Har oy | 50–150 pip |
| **AQSh YIM** | USD | Har chorak | 30–100 pip |

### 2-daraja (🟠🟠 — ehtiyotkorlik)

- PMI Ishlab chiqarish va Xizmatlar (EUR, USD, GBP)
- Chakana savdo (USD, EUR)
- Iste'molchilar ishonchi (USD)
- Ishsizlik nafaqasi arizalari (USD, haftalik)

---

## 4. Xavfsiz yangiliklar savdo strategiyalari

### A-strategiya: «Chang cho'kishini kut» (yangi boshlovchilar uchun tavsiya etiladi)

```
1. Yangilik 13:30 UTC da chiqdi
2. 5–15 daqiqa kutyapsiz (spred normallanadi, shovqin tinadi)
3. Impuls YO'NALISHINI ko'rib chiqasiz
4. Impuls yo'nalishida pullback da kirasiz (Limit order)
5. SL — birinchi 5 daqiqaning qarama-qarshi ekstremumi orqasida
```

Afzalligi: kam slippage xavfi, prognozni emas faktni savdo qilasiz.

### B-strategiya: Yangilik oldidan Straddle

```
1. Relizdan 30 daqiqa oldin bozor bir yon harakatni shakllantiryapti
2. Yon harakat USTIGA Buy Stop + PASTIGA Sell Stop qo'yasiz
3. Narx istalgan tomonga yorilib chiqadi — orderlardan biri ishga tushadi
4. Ikkinchisini qo'lda bekor qilasiz yoki OCA dan foydalanasiz
```

!!! warning "Straddle xavfi"
    Agar ikkala order ham ishga tushsa (birinchi bir tomonga, keyin qaytish) — zarar × 2.
    Har bir order uchun **SL o'rnating**. Keng spredli juftliklarda ishlatmang.

---

## 5. NFP taktikasi

NFP — AQShning eng muhim oylik hisoboti. **Har oyning birinchi juma kuni 13:30 UTC da** e'lon qilinadi.

### NFP atrofida EUR/USD xulq-atvori:

```
30 daqiqa oldin: yon harakat, kam hajm, spred kengay boshlaydi
Reliz paytida: 1–3 soniyada 50–200 pip harakat
1–5 daqiqadan keyin: dastlabki harakatning 30–50% ga teskari qaytish (shakeout)
15–30 daqiqadan keyin: kun yo'nalishi shakllanadi
```

### NFP protokoli:

1. **13:00 UTC** — ochiq pozitsiyalarni tekshiring. Bor bo'lsa — yoping yoki qattiq SL qo'ying.
2. **13:25 UTC** — yangi pozitsiya ochmaslik. Spred allaqachon kengaymoqda.
3. **13:30 UTC** — HECH NARSA QILMAYSIZ. Ma'lumotlarga qarang.
4. **13:32–13:35 UTC** — «birinchi shakeout» ni (teskari tomonga soxta harakat) kutasiz.
5. **13:35–13:45 UTC** — **ikkinchi** harakat yo'nalishida pullback da Limit order bilan kirasiz.
6. **SL** — relizdan keyin dastlabki 10 daqiqaning pasti/yuqorisidan nariroqda.
7. **TP** — SLning 1,5–2 barobari (min RR 1:1,5).

---

## 6. FOMC (Fed majlisi) taktikasi

FOMC — **yiliga 8 marta**, odatda chorshanba. Qaror 18:00 UTC da, matbuot anjumani 18:30 UTC da.

### Uch reaktsiya stsenariyasi:

| Stsenariy | Nima bo'ldi | USD reaktsiyasi |
|---|---|---|
| **Hawkish kutilmagan natija** | Stavka prognozdan yuqori ko'tarildi yoki ritorika qattiq | USD kuchayadi |
| **Dovish kutilmagan natija** | Stavka tushirildi yoki kelajakdagi tushirish ishoralari | USD zaiflashadi |
| **Kutilgandek** | Stavka va ritorika prognoz bo'yicha | USD neytral yoki «yangilikda sot» |

!!! tip "FOMC ni qanday savdo qilish"
    18:00 UTC da savdo qilish shart emas. Eng yaxshi vaqt — matbuot anjumanidan **20–30 daqiqa keyin**,
    bozor ma'lumotni hazm qilgach. Spred normallanadi, yo'nalish ko'rinadi.

---

## 7. Yangiliklar savdosida Stop-Loss

Kengaygan spred = **SL narxga yetishidan oldin ishga tushishi mumkin**.

```
SL 1.0810 da turgan (1.0830 Sell kirishidan 20 pip)
Yangilik paytida Ask 1.0812 ga yetadi (Bid = 1.0806 bo'lsa)
Ask bo'yicha SL = 1.0812 → ishga tushadi
Haqiqiy harakat: narx 1.0760 ga tushdi — lekin siz allaqachon pozitsiyasiz
```

### Yangiliklar uchun SL qoidalari:

1. Yangilikdan oldin **SLni kamida 1,5 barobarga oshiring**
2. **SLni hech qachon to'g'ridan-to'g'ri darajaga qo'ymang** — faqat undan nari (+3–5 pip bufer)
3. **OCO** — ikkala tomonni qo'ysangiz, ikkovi ham SL ga ega bo'lishi kerak
4. **«Yaxshi» bajarilishni kutmang** — keng spredda haqiqatni qabul qiling

---

## 8. Kirishdan oldingi tekshiruv ro'yxati

- [ ] Keyingi 4 soat uchun iqtisodiy kalendarni tekshirdimmi?
- [ ] Ochiq pozitsiyalarni yopdim yoki stoplarni uzoqroqqa ko'chirdimmi?
- [ ] Prognozni va qaysi raqam «yaxshi» yoki «yomon» ekanligini bilamanmi?
- [ ] Relizdan keyin kirish oldidan 5–15 daqiqa kutayapmanmi?
- [ ] SLim kengaygan spredni hisobga oladimi (oddiy spredning +30–50%)?
- [ ] Pozitsiya hajmim kamaytirilganmi (bitimga hisobning maksimal 0,5%)?
- [ ] Narx boshqa tomonga ketsa «B rejam» bormi?

!!! quote "Tajribali treyderning qoidasi"
    *«Har bir yangilikni savdo qilish shart emas. Eng yaxshi savdo — o'tkazib yuborgan savdoyingiz,
    hisobingizni quritgan savdoyingiz emas.»*

---

*← [Savdo sessiyalari](trading-sessions.uz.md) · [Texnik tahlil →](../docs/technical-analysis.uz.md)*
