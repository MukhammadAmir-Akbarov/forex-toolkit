# ⚙️ Brokerning haqiqiy mexanikasi — «sahna ortida» nima bo'ladi

!!! abstract "Nima uchun bu muhim"
    Ko'pchilik yangi boshlovchilar shunday o'ylaydi: «EUR/USD sotib oldim — bozor reaksiya
    ko'rsatdi». Haqiqatda sizning orderingiz «bozorga» hech qachon yetib bormasligi mumkin —
    broker savdoning qarama-qarshi tomonini o'zi olishi mumkin. Buni tushunish **slippage,
    requote, spredning kengayishi** ni tushuntiradi va reklamaga emas, haqiqiy shartlarga
    qarab broker tanlashga yordam beradi.

> **Ta'lim materiali.** Tavsiflangan mexanizmlar — sanoatning umumiy ma'lum faktlari,
> muayyan brokerlar haqidagi da'volar emas.

---

## Mundarija

1. [Ikki bajarish modeli: MM va ECN/STP](#1-ikki-bajarish-modeli-mm-va-ecnstp)
2. [Slippage: qaerdan va nima uchun](#2-slippage-qaerdan-va-nima-uchun)
3. [Requote — nima va qanday qochish](#3-requote--nima-va-qanday-qochish)
4. [Spred: Qat'iy va suzuvchi](#4-spred-qatiy-va-suzuvchi)
5. [Svop — pozitsiyani kechasi ushlab turishning narxi](#5-svop--pozitsiyani-kechasi-ushlab-turishning-narxi)
6. [Marja va Margin Call: mexanika](#6-marja-va-margin-call-mexanika)
7. [Haqiqiy manfaatlar to'qnashuvi](#7-haqiqiy-manfaatlar-toqnashuvi)
8. [Broker qanday tanlash: ob'ektiv mezonlar](#8-broker-qanday-tanlash-obektiv-mezonlar)

---

## 1. Ikki bajarish modeli: MM va ECN/STP

### Market Maker (MM) — «Oshxona»

Broker **sizning savdoingizning qarama-qarshi tomonini o'zi oladi**. Siz EUR/USD sotib oldingiz — broker sotdi.

```
Siz: Buy 0.1 lot EUR/USD 1.08463 da
Broker ichida: 0.1 lot «sotish» ni qabul qildi

Broker bu xavf bilan nima qiladi:
A) Likvidlik provayderida hedgelaydi (halol MM)
B) Hedgelamas, siz yutqazasiz deb «umid qiladi» (manfaatlar to'qnashuvi)
```

**MM broker belgilari:**
- Qat'iy spred (EUR/USD da kechasi ham 2–3 pip)
- Tez bozorda requotelar
- Minimal depozit $10–50
- «Instant Execution»

### ECN (Elektron aloqa tarmog'i)

Sizning orderingiz **haqiqatan bozorga chiqadi** — banklar, boshqa brokerlar va institutsional
o'yinchilardan iborat likvidlik havzasiga.

```
Siz: Buy 0.1 lot EUR/USD
Broker: ECN platformasiga yuboradi
ECN: sotuvchi topadi (boshqa treyder, bank, LP)
Bajarish: eng yaxshi mavjud narx bo'yicha
```

**ECN broker belgilari:**
- Suzuvchi spred (0,0 pipdan + lotiga $3–5 komissiya)
- Requotelar yo'q (har doim Market Execution)
- Minimal depozit $200–1000
- Shaffof narx belgilash

### STP (To'g'ridan-to'g'ri o'tkazish)

Gibrid: orderlar avtomatik ravishda likvidlik provayderiga o'tadi, lekin broker komissiya
o'rniga **spredga ustama** qo'shishi mumkin.

| Mezon | Market Maker | ECN/STP |
|---|---|---|
| Bajarish | Instant / Requote | Market (requotesiz) |
| Spred | Qat'iy, keng | Suzuvchi, tor + komissiya |
| Manfaatlar to'qnashuvi | Mumkin | Minimal |
| Minimal depozit | Past ($10–100) | Yuqoriroq ($200+) |
| Kim uchun | Ta'lim, kichik hisoblar | Faol savdo |

---

## 2. Slippage: qaerdan va nima uchun

**Slippage** — order yuborilgan paytdagi narx va bajarish narxi o'rtasidagi farq.

### Sabablari:

1. **Tezlik**: bozor orderingiz yetib borguncha tezroq harakat qiladi (10–100 ms)
2. **Likvidlik**: katta hajmda bir narxda yetarli kontragent yo'q
3. **O'zgaruvchanlik**: yangiliklar paytida narx millisekundlarda tiklarga sakraydi

```
Ijobiy slippage misoli (siz foydasiga):
Buy Market 1.08463 da yuborildi
1.08459 da bajarildi → 0,4 pip yaxshiroq
(ECN da bu order yo'lda bo'lgan paytda narx SIZGA FOYDALI tomonga harakat qilganda bo'ladi)

Salbiy slippage misoli (zarar):
Buy Market 1.08463 da yuborildi
1.08481 da bajarildi → 1,8 pip yomonroq
(Order bajarilayotganda narx sakrab ketdi)
```

### Slippageni qanday minimallashtirishlik:

- **Likvid vaqtlarda** savdo qiling (London/Nyu-York, Osiyo sessiyasi emas)
- **Market o'rniga Limit** ishlating — narxni kafolatlaydi, lekin bajarilishni emas
- **Yangiliklar chiqishi paytida Market** ishlatmang
- Brokerning **bajarish sifati hisobotlarida** o'rtacha slippageni tekshiring

---

## 3. Requote — nima va qanday qochish

**Requote** — broker sizning narxingizni rad etib, yangi narx taklif qiladi.

```
1.08463 da «Buy» ni bosdingiz
Oyna: «Narx o'zgardi. Yangi narx: 1.08471. Qabul qilasizmi?»
```

Bu MM brokerlarda **Instant Execution** uchun odatiy holat. Market Execution da requotelar
yo'q — order har doim bajariladi, lekin bozor narxida.

### Requotelardan qanday qochish:

1. **Market Execution** li broker tanlang
2. **Yangiliklar chiqishi lahzasida Market** ishlatmang
3. Statistikani tekshiring: brokerlar requote foizini e'lon qilishi shart

---

## 4. Spred: Qat'iy va suzuvchi

**Spred** — Ask (sotib olish) va Bid (sotish) o'rtasidagi farq. Savdoning asosiy «solig'i».

```
EUR/USD: Bid = 1.08450, Ask = 1.08453
Spred = 0,3 pip (yoki 0,1 lot uchun $0,30)
```

### Spred qachon kengayadi:

| Vaqt / Voqea | EUR/USD spredi |
|---|---|
| London+NY qoplaması (15:00–17:00 UTC) | 0,1–0,5 pip |
| Osiyo sessiyasi | 0,5–1,5 pip |
| 🔴 yangilikdan 5 daqiqa oldin/keyin | 3–50+ pip |
| Juma kechasi / dam olish kunlari | 2–5 pip |
| Hafta boshlanishi (Yakshanba 22:00 UTC) | 5–15 pip |

### Spredning haqiqiy narxi

```
Strategiya: kuniga 10 savdo, 0,1 lot EUR/USD, spred = 0,5 pip
Bir savdoda spred narxi = 0,5 pip × $1 = $0,50
Kuniga = $0,50 × 10 = $5,00
Oyiga (22 kun) = $110,00
```

Bu har bir savdodagi **zarar ko'rmaslik narxi** — narx hech bo'lmaganda spred qaytguncha
harakat qilishi kerak.

---

## 5. Svop — pozitsiyani kechasi ushlab turishning narxi

**Svop (Rollover)** — **pozitsiyani yarim kechadan o'tkazib saqlash (22:00 UTC) uchun** to'lov
yoki hisoblash.

Mantiq: siz bir valyutani ushlamoqdasiz va boshkasini «qarzga oldingiz». Bu ikki valyutaning
foiz stavkalari farqi — mana svop.

```
Long EUR/USD (EUR ushlab, USD qarzga olgan):
EUR stavkasi = 4,0%, USD stavkasi = 5,5%
4,0% olasiz, 5,5% to'laysiz
Svop = salbiy (to'laysiz)

Short EUR/USD (USD ushlab, EUR qarzga olgan):
5,5% olasiz, 4,0% to'laysiz
Svop = ijobiy (hisoblanadi)
```

### Chorshanba kuni uch baravar svop

Forex T+2 da hisob-kitob qiladi. Chorshanba kuni 22:00 dan o'tkazib saqlangan pozitsiya
uch kunlik svop ko'taradi (chorshanba + shanba + yakshanba). Skalperlar uchun muhim.

!!! warning "Ekzotik juftliklarda svop"
    USD/TRY, USD/ZAR, USD/BRL kabi juftliklarda longlar uchun svop **kuniga lotiga −$10–30**
    ga yetishi mumkin. 10+ kun ushlab turilsa, narx harakat qilmasdan ham sezilarli zarar.

### Svopsiz hisoblar (islomiy)

Brokerlar musulmonlar uchun **svopsiz** hisoblar taklif qiladi. Lekin odatda svopni
3+ kun ushlagach **ma'muriy to'lov** bilan almashtiradi. Har doim haqiqiy shartlarni tekshiring.

---

## 6. Marja va Margin Call: mexanika

**Marja** — pozitsiya ochilganda broker blokirovka qiladigan garov.

```
Hisob: $1000, leverage 1:100, 0,1 lot EUR/USD ochasiz
Pozitsiya qiymati = 10 000 EUR ≈ $10 800
Marja = $10 800 / 100 = $108 → broker $1000 dan $108 ni bloklaydi
Erkin marja = $1000 − $108 = $892
```

### Margin Call va Stop Out

| Daraja | Nima bo'ladi |
|---|---|
| **Margin Call** (~100% marja darajasi) | Broker ogohlantiradi: hisob to'ldiring |
| **Stop Out** (~50% marja darajasi) | Broker pozitsiyalarni majburiy yopadi |

```
Stop Out misoli:
Marja = $108, Stop Out 50% da
Stop Out triggeri = $108 × 50% = $54 equity
Pozitsiyadagi zarar = $946 ($1000 dan $54 qoldi)
→ Broker pozitsiyani majburiy yopadi
```

!!! danger "Hech qachon marjada hisobning 10% dan ko'prog'ini oluvchi pozitsiya ochmang"
    Qoida: bitta pozitsiya marjasi ≤ depozitning 2–5%. Aks holda bir necha ekstremal harakat → Stop Out.

---

## 7. Haqiqiy manfaatlar to'qnashuvi

### «B-kitob» va «A-kitob»

Har bir brokerda mijozlarning ichki bo'linishi bor:

**A-kitob** — foydali, tajribali treyderlar. Ularning orderlari haqiqiy bozorga chiqadi.
Broker komissiya/spreddan daromad oladi.

**B-kitob** — chakana treyderlarning aksariyati. Ularning orderlari **bozorga chiqmaydi** —
broker savdoni o'zi «oladi». Siz yutqazganingizda → broker daromad oladi.

```
Statistika: chakana treyderlarning 70–80% pul yo'qotadi.
B-kitobli MM broker uchun bu degani:
Broker foydasi ≈ mijozlar zararlari (bozorga chiqmasdan)
```

!!! warning "Bu MM brokerlar «aldaydi» degani emas"
    Litsenziyalangan MM broker narxlarni o'zboshimchalik bilan harakat ettira olmaydi —
    ular likvidlik provayderlarining kotirovkalarini ko'rsatadi. To'qnashuv **motivatsiyada**:
    MMga siz yutqazganingiz foydali. ECN sizning natijangizga befarq (hajmdan daromad oladi).

---

## 8. Broker qanday tanlash: ob'ektiv mezonlar

| Mezon | Qizil bayroq | Yaxshi belgi |
|---|---|---|
| Litsenziya | Yo'q / offshor Vanuatu/Beliz | FCA, ASIC, CySEC, FSA |
| EUR/USD spredi | Ish vaqtida > 2 pip | < 0,5 pip (ECN) yoki < 1 pip (MM) |
| Bajarish | Requotelar, spredni majburiy kengaytirish | Market Execution, shaffof statistika |
| Depozit/yechib olish | > 3% komissiya, > 3 kun kechikish | 0% komissiya, 24 soat ichida yechib olish |
| Minimal depozit | > $1000 asossiz | Standart $100–500 |
| Qo'llab-quvvatlash | Bosimchi «menejerlar», qo'ng'iroqlar | Neytral qo'llab-quvvatlash |
| Bonuslar | «Depozitga 100% bonus» (ko'pincha yechib bo'lmaydi) | Bonussiz yoki shaffof shartlar |

!!! success "O'zbekiston dan yangi boshlovchilar uchun tavsiya"
    [O'zbekiston uchun brokerlar](../uz/brokers-uz.uz.md) sahifasiga qarang — u yerda
    VISA/Mastercard UZS orqali qulay to'ldirish va Telegram qo'llab-quvvatlashi bilan
    brokerlar tanlangan.

---

*← [Fundamental tahlil](fundamental-analysis-guide.uz.md) · [Order turlari →](order-types-mechanics.uz.md)*
