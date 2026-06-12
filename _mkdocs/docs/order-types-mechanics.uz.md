# 📋 Order turlari va savdoga kirish mexanikasi

!!! abstract "Nima uchun bu muhim"
    Ko'pchilik yangi treyderlar Market va Limit orderni chalkashtirib yuboradi, Stop-Loss va
    Stop-Limit o'rtasidagi farqni tushunmaydi, pozitsiyani «qanday bo'lsa shunday» ochadi.
    Ushbu sahifada **barcha order turlari**, ularning mantiqi, keng tarqalgan xatolar va
    MT5 hamda TradingView'dagi misollar ko'rib chiqiladi.

> **Ta'lim materiali.** Narx misollari sintetik bo'lib, faqat tushuntirish maqsadida keltirilgan.

---

## Mundarija

1. [Market order (bozor orderi)](#1-market-order-bozor-orderi)
2. [Limit order](#2-limit-order)
3. [Stop order](#3-stop-order)
4. [MT5dagi kutilma orderlar](#4-mt5dagi-kutilma-orderlar)
5. [Trailing stop](#5-trailing-stop)
6. [Order qo'yishdagi keng tarqalgan xatolar](#6-order-qoyishdagi-keng-tarqalgan-xatolar)
7. [Order turini tanlash: qo'llanma](#7-order-turini-tanlash-qollanma)

---

## 1. Market order (bozor orderi)

**Hozirgi narxda darhol sotib olish/sotish** — aniqrog'i, bajarish paytidagi eng yaxshi
mavjud narx bo'yicha.

```
EUR/USD joriy narxi: Bid 1.08450 / Ask 1.08463
BUY Market ochasiz → bajarish Ask bo'yicha = 1.08463
SELL Market ochasiz → bajarish Bid bo'yicha = 1.08450
```

!!! warning "Slippage (narx siljishi)"
    Tez bozorda (yangiliklar, sessiya ochilishi) order brokerga yetib borguncha narx
    **siljishi** mumkin. 1.08463 da order yubordingiz, 1.08471 da bajarilib qoldi.
    ECN brokerda bu odatiy holat. Market-maker brokerda esa requote bo'lishi mumkin.

**Qachon ishlatish:**
- Kutmasdan **darhol** kirish kerak bo'lganda
- Quyi vaqt oralig'ida savdo qilganda, kutish imkoni yo'q
- Hajm kichik, yetarli likvidlik mavjud

**Qachon ISHLATMASLIK:**
- Yirik yangiliklar (NFP, FOMC) dan 30 daqiqa oldin/keyin
- Keng spredli ekzotik juftliklarda
- Narx kirish nuqtangizdan allaqachon o'tib ketgan bo'lsa

---

## 2. Limit order

**Ko'rsatilgan narxdan yomonroq bo'lmagan narxda kirish** — order bozor kelguncha
kitobda kutadi.

```
EUR/USD hozir: 1.08463
Buy Limit 1.08300 da qo'ying — narx 1.08300 ga TUSHGANDAGINA ishga tushadi
Sell Limit 1.08600 da qo'ying — narx 1.08600 ga KO'TARILGANDAGina ishga tushadi
```

**Mantiq:** narx siz qulay deb hisoblagan darajaga qaytishini kutasiz.

!!! success "Asosiy afzalligi"
    Kirish narxini **aniq bilasiz** — bajarish limitdan yomonroq emas (ECN da ko'pincha
    aynan shu narxda yoki undan yaxshiroq). Zararli tomonda slippage xavfi yo'q.

!!! danger "Tuzoq: bajarilib qolmaydigan limit"
    Narx darajangizga «yaqin keldi», lekin 1–2 pipdan yetmasdan qaytsa — order
    **bajarilib qolmaydi**. Bu odatiy holat — bozor sizga fill ta'minlashga majbur emas.
    Xato: limitni joriy narxga juda yaqin qo'yish — u har bir tik da bajariladigan
    psevdo-market orderga aylanadi.

**Qachon ishlatish:**
- Darajaga pullback bo'yicha kirish
- Qo'llab-quvvatlash/qarshilik dan savdo
- **Yaxshiroq narx** istaysiz va kutishga tayyorsiz

---

## 3. Stop order

**Narx darajani yorib o'tganda kirish/chiqish** — narxga yetganda «bozor bilan» ishga tushadi.

### Buy Stop
```
EUR/USD hozir: 1.08463
Buy Stop 1.08600 da qo'ying → narx 1.08600 ga KO'TARILGANda Market BUY sifatida ishga tushadi
Mantiq: yuqoriga breakout sotib olish, harakat davom etishini kutish
```

### Sell Stop
```
Sell Stop 1.08300 da qo'ying → narx 1.08300 ga TUSHGANda Market SELL sifatida ishga tushadi
Mantiq: pastga breakout sotish
```

!!! warning "Spred bo'yicha stop order"
    Sell Stop ni qo'llab-quvvatlash darajasiga qo'ysangiz, shuni esda tutingki:
    **Ask** darajaga **Bid** dan oldin yetadi. Misol: daraja 1.08300, spred 1.3 pip.
    - Bid = 1.08300 → order ishga tushadi
    - Lekin Ask shu payt = 1.08313 — pozitsiya allaqachon spred va slippage bo'yicha «zararda»

### Stop-Loss va Take-Profit

Bular ochiq pozitsiyaga **himoya orderlari**:

| Order | Tur | Nima qiladi |
|---|---|---|
| **Stop-Loss (SL)** | Stop | N pip zararda pozitsiyani yopadi |
| **Take-Profit (TP)** | Limit | N pip foyda bo'lganda pozitsiyani yopadi |

```
BUY EUR/USD 1.08463 da ochildi
SL = 1.08363 (xavf 10 pip)
TP = 1.08663 (maqsad 20 pip, RR = 1:2)
```

!!! danger "Hech qachon SL siz savdo qilmang"
    Bozor siz hisoblagan tomonga yuzlab pipga borishi mumkin. Stop-losssiz bir zararli kun
    haftalar davomidagi foydani yo'q qilishi mumkin.

---

## 4. MT5dagi kutilma orderlar

MT5 da 6 turdagi kutilma orderlar mavjud:

| Tur | Nima qiladi | Qachon ishlatish |
|---|---|---|
| **Buy Limit** | Joriy narxdan pastda sotib olish | Pasayishda kirish |
| **Sell Limit** | Joriy narxdan yuqorida sotish | Ko'tarilishda kirish |
| **Buy Stop** | Joriy narxdan yuqorida sotib olish | Yuqoriga breakout sotib olish |
| **Sell Stop** | Joriy narxdan pastda sotish | Pastga breakout sotish |
| **Buy Stop Limit** | Yuqoriga breakout bo'lganda aktiv. Buy Limit | Breakoutdan keyin pullback da kechiktirilgan kirish |
| **Sell Stop Limit** | Pastga breakout bo'lganda aktiv. Sell Limit | Breakdowndan keyin pullback da kechiktirilgan kirish |

### MT5 da order qo'yish

```
Grafik ustida o'ng tugma → «Savdo» → «Yangi order»
Yoki F9 tugmasi (tezkor)
Tur tanlang: Market Execution / Pending Order
To'ldiring: hajm (lotlar), narx, SL, TP, amal qilish muddati
```

!!! tip "Order muddati"
    Odatiy holda kutilma order **muddatsiz** saqlanadi (GTC — Good Till Cancelled).
    Sana/vaqt belgilash mumkin. Maslahat: dam olish kunlari yoki yirik yangiliklar oldidan
    **bajarilib qolmagan orderlarni o'chiring** — narx to'g'ridan-to'g'ri kirish nuqtangizga
    bo'shliq qilib sakrashi mumkin.

---

## 5. Trailing stop

**Stop-Lossni narx bilan birga avtomatik siljitadi**, foydani mustahkamlaydi.

```
BUY EUR/USD 1.08463 da ochildi, SL = 1.08363 (−10 pip)
Trailing Stop = 20 pip o'rnatildi

Narx ko'tariladi:
→ 1.08500: SL 1.08363 da qoladi (masofa hali yetmagan)
→ 1.08663: SL avtomatik 1.08463 ga ko'chadi (zarar ko'rmaslik nuqtasi!)
→ 1.08763: SL = 1.08563 (10 pip foydani mustahkamladi)
→ Narx 1.08720 ga qaytadi: SL 1.08563 da ishga tushadi — +10 pip da yopilinadi
```

!!! warning "Trailing stop tuzoqlari"
    1. **Faqat MT5 ochiq bo'lganda ishlaydi** — bu server orderi emas, balki mahalliy funksiya.
       MT5 ni yopsangiz, trailing stop to'xtaydi.
    2. **Bid/Ask tiklari bo'yicha ishga tushadi** — yon bozorlarda yoki shovqinda ko'p uchyb ketadi.
    3. Kichik qadam bilan yuqori o'zgaruvchan juftliklarda (Osiyo sessiyasida JPY krosslari) ishlatmang.

---

## 6. Order qo'yishdagi keng tarqalgan xatolar

### ❌ Xato 1: «Narx ketib qolgani uchun bozordan kiraman»

```
EUR/USD ni 1.08300 da (qo'llab-quvvatlashga pullback) sotib olmoqchi edingiz.
Narx 1.08550 ga ko'tarildi, «ulgurmadingiz».
1.08550 da Market Buy ochasiz — narxni quvlayapsiz.
```

Yaxshisi: kirishni **o'tkazib yuborishyoki keyingi mumkin bo'lgan pullback uchun limit qo'ying.

### ❌ Xato 2: SL narxga juda yaqin

```
EUR/USD: 1.08463, soatlik o'rtacha harakat (ATR H1) = 15 pip
SL = 1.08443 qo'ydingiz (atigi 2 pip!) — bozor shovqini uni albatta urib ketadi
```

Qoida: **SL ≥ joriy vaqt oralig'ining so'nggi 14 sham bo'yicha ATR** (MT5 da ATR indikatoriga qarang).

### ❌ Xato 3: Limitni spredsiz hisoblash

```
Qo'llab-quvvatlash darajasi 1.08300 da BUY kirmoqchisiz
Buy Limit 1.08300 da qo'ydingiz
ECN da Osiyo sessiyasida EUR/USD spredi 2-3 pip bo'lishi mumkin
Haqiqiy kirish = 1.08300 + 0.00003 = 1.08303 (ahamiyatsiz farq)
Lekin ANIQ darajada kirmoqchi bo'lsangiz — Limitni biroz pastroq qo'ying
```

### ❌ Xato 4: «Umid bilan» SL siz zararli pozitsiyani ushlab turish

Bu «psixologik stop» deb ataladi — va bu **stop emas**. Bozor siz qayerda kirganingizni
bilmaydi va sizni qutqarish uchun qaytmaydi.

### ❌ Xato 5: TP to'g'ridan-to'g'ri qarshilik darajasida

```
BUY ochildi, TP kuchli qarshilik 1.09000 da joylashgan.
Haqiqat: narx ko'pincha dumaloq darajaga 2–5 pip «yetmasdan» qaytadi.
```

Maslahat: TP ni eng yaqin qarshilikdan **3–5 pip pastroqqa** qo'ying (longlar uchun).

---

## 7. Order turini tanlash: qo'llanma

| Vaziyat | Tavsiya etilgan order |
|---|---|
| «Hozir kirmoqchiman» | Market |
| «Darajaga pullback kutaman» | Limit (Buy Limit yoki Sell Limit) |
| «Daraja breakoutini savdo qilaman» | Stop (Buy Stop yoki Sell Stop) |
| «Breakout savdosi, yaxshiroq kirish istaymanэ» | Stop Limit |
| «Foydani avtomatik mustahkamlamoqchiman» | Trailing Stop (MT5 ochiq bo'lganda) |
| «Aniq maqsadda chiqmoqchiman» | Take-Profit (Limit) |
| «Zararni cheklashim kerak» | Stop-Loss (majburiy!) |

---

*← [Texnik tahlil](technical-analysis.uz.md) · [Bozor tuzilmasi →](../practice/market-structure.uz.md)*
