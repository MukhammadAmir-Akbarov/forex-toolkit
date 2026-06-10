# «EMA50 ga orqaga qaytish trend bo'yicha» strategiyasi — batafsil tahlil

!!! info "🌐 Tarjima / Перевод"
    Bu — sahifaning oʻzbekcha versiyasi. Asl nusxasi rus tilida; tilni sahifa yuqorisidagi til tanlagich orqali almashtirish mumkin.
    *Это узбекская версия страницы; оригинал доступен на русском.*

> **Bu o'quv strategiyasi, Graal emas.** Maqsad — savdo yondashuvining tuzilishini ko'rsatish: qoidalar, risk-menejment, tekshirish. Har qanday strategiyani real savdodan oldin **demoda kamida 100 ta savdoda** sinab ko'rishingiz shart.

## Mundarija

1. [Strategiya g'oyasi](#1-strategiya-goyasi)
2. [To'liq savdo tizimi nima](#2-toliq-savdo-tizimi-nima)
3. [Strategiya parametrlari](#3-strategiya-parametrlari)
4. [Long kirish shartlari](#4-long-kirish-shartlari)
5. [Short kirish shartlari](#5-short-kirish-shartlari)
6. [Savdodan chiqish](#6-savdodan-chiqish)
7. [Pozitsiyani boshqarish](#7-pozitsiyani-boshqarish)
8. [Grafikdagi ko'rgazma](#8-grafikdagi-korgazma)
9. [Bektest va forward-test](#9-bektest-va-forward-test)
10. [Strategiya ISHLAMAYDIGAN holatlar](#10-strategiya-ishlamaydigan-holatlar)
11. [Jurnal orqali strategiyani takomillashtirish](#11-jurnal-orqali-strategiyani-takomillashtirish)

---

## 1. Strategiya g'oyasi

**Arzonroqqa sotib ol, qimmatroqqa sot** — oddiy tuyuladi, ammo strategiyaning mantiqiy asosi aynan shu.

**Kuchli trendda narx to'g'ri chiziq bo'ylab ketmaydi**: u impulslar va orqaga qaytishlar (pullback) hosil qiladi. Bu strategiya **trend yo'nalishidagi orqaga qaytishlarni** ushlaydi, ekstremal nuqtalarni emas.

Mantiq:
- Agar trend yuqoriga yo'nalgan bo'lsa (H4 da narx EMA200 dan yuqori) — **faqat sotib olamiz**.
- Cho'qqilarda emas, **dinamik qo'llab-quvvatlash darajasiga** (EMA50) orqaga qaytganda sotib olamiz.
- Orqaga qaytish tugaganini tasdiqlash uchun sham patternidan foydalanamiz.

Bu **trend-following** (trendga ergashuvchi) strategiya. Yonma-yon harakatda yutqizadi, lekin trendda yaxshi R:R beradi.

---

## 2. To'liq savdo tizimi nima

Har qanday strategiya — bu **6 ta aniq qoidalar** to'plami:

| # | Nima aniqlanadi | Bizning strategiyamizdan misol |
|---|---|---|
| 1 | **Qachon bozorga qarash** | Har bir H1 shamning yopilishidan keyin |
| 2 | **Qaysi bozorda savdo qilish** | EUR/USD, GBP/USD — majorlar |
| 3 | **Qaysi yo'nalishda savdo qilish** | Faqat H4 trendi bo'yicha |
| 4 | **Kirish shartlari** | EMA50 ga orqaga qaytish + buqali pattern |
| 5 | **Stop-loss qayerda** | Oxirgi swing-minimum orqasida + 5 pips |
| 6 | **Take-profit qayerda** | Stopgacha bo'lgan masofaning 2×, R:R 1:2 |

**Barcha 6 qoida bo'lmasasaving — bu strategiya emas, bu improvizatsiya.**

---

## 3. Strategiya parametrlari

```yaml
Nomi: "EMA50 Pullback by Trend"
Turi: Trend-following
Bozorlar: EUR/USD, GBP/USD (faqat majorlar, past spred)
Savdo vaqti: London + Amerika sessiyasi (12:00–22:00 UTC+3)
             Osiyo sessiyasidan qoching (past likvidlik), juma kechqurunidan qoching

Taymfreymlar:
  - Trend: H4
  - Kirish nuqtasi: H1

Indikatorlar:
  - EMA(50) H1 da — dinamik qo'llab-quvvatlash/qarshilik
  - EMA(200) H4 da — asosiy yo'nalish filtri
  - RSI(14) H1 da — qizib ketish filtri

Risk-menejment:
  - Savdoga xavf: depozitning 0.5% (yangi boshlovchi) yoki 1% (tajriba ≥ 6 oy)
  - R:R kamida 1:2
  - Bir vaqtda maksimal 2 ta ochiq savdo
  - Kunda maksimal 3 ta zarar → kun uchun to'xtatish
  - Haftada maksimal 6% drawdown → dushanbagacha pauza
```

---

## 4. Long kirish shartlari

**BARCHA shartlar bajarilishi shart. Hatto bittasi bajarilmasa — savdo YO'Q.**

### Qadam 1. Trend filtri (H4)
- ☐ Joriy narx **H4 da EMA(200) dan yuqori**
- ☐ H4 tuzilmasi — ketma-ket yuqori maksimumlar / yuqori minimumlar (yuqoriga trend)
- ☐ H4 da yuqorida yaqin 50 pips ichida jiddiy qarshilik yo'q

### Qadam 2. H1 da orqaga qaytish
- ☐ Narx H1 da EMA(50) ga tushdi — tegish yoki yaqin (10 pips chegarasida)
- ☐ Orqaga qaytish **yuqoriga impulsdan keyin** yuz berdi, yonma-yon harakatdan emas

### Qadam 3. H1 da sham signali
EMA50 yonida **kamida bittasi** buqali patternlar kerak:
- ☐ Bolg'a (uzun pastki soya, yuqorida kichik tanasi, istalgan rang)
- ☐ Buqali qamrab olish (yashil sham qizil sham tanasini qopladi)
- ☐ EMA50 da doji + keyingi yashil sham
- ☐ Buqali pin-bar

### Qadam 4. RSI filtri
- ☐ H1 da RSI(14) **40–65** zonasida
  - 40 dan kam — tuzilma juda zaif, o'tkazish yaxshiroq
  - 65 dan ko'p — allaqachon qizib ketgan, stop juda katta bo'ladi

### Qadam 5. Yangiliklar filtri
- ☐ Keyingi 2 soatda EUR yoki USD bo'yicha **qizil** yangiliklar yo'q
- ☐ Bu UTC+3 da 18:00 dan keyin juma emas

### Agar BARCHA 5 qadam ☑ — long ochamiz.

---

## 5. Short kirish shartlari

Long ning ko'zgu aksi:

### Qadam 1. Trend filtri (H4)
- ☐ Narx **H4 da EMA(200) dan past**
- ☐ H4 tuzilmasi — ketma-ket past maksimumlar / past minimumlar

### Qadam 2. H1 da orqaga qaytish
- ☐ Narx H1 da EMA(50) ga pastdan ko'tarildi

### Qadam 3. H1 da sham signali
- ☐ Tushuvchi yulduz (uzun yuqori soya)
- ☐ Ayiqli qamrab olish
- ☐ Doji + keyingi qizil sham
- ☐ Ayiqli pin-bar

### Qadam 4. RSI filtri
- ☐ RSI(14) **35–60** zonasida

### Qadam 5. Yangiliklar filtri
- ☐ Keyingi 2 soatda qizil yangiliklar yo'q

---

## 6. Savdodan chiqish

### Stop Loss

**Long uchun:**
- Signaldan oldingi oxirgi swing-minimumdan (oxirgi mahalliy tub) **5 pips past**
- Kirish nuqtasidan stopgacha bo'lgan masofa = `Stop Distance` (pipslarda)

**Short uchun:**
- Oxirgi swing-maksimumdan 5 pips yuqori

> **⚠️ Stop «xohlaganim uchun 20 pips» deb qo'yilmaydi.** Stop — bu **texnik daraja**, uning buzilishi sizning trend haqidagi farazingiz noto'g'ri ekanini bildiradi.

### Take Profit — uch variant

**A varianti: Qat'iy R:R = 1:2 (yangi boshlovchilar uchun)**
```
TP = kirish + 2 × Stop Distance  (long uchun)
TP = kirish − 2 × Stop Distance  (short uchun)
```

**B varianti: H4 dagi eng yaqin muhim qarshilik darajasigacha**
- Oldinda aniq to'siq bo'lganda ishlatiladi
- R:R kamida 1:1.5 ekanini tekshiring

**V varianti: Trailing stop**
- 1R foyda o'tgandan keyin — stopni zararsizbandlikka (kirish narxiga) ko'chirish
- 2R o'tgandan keyin — stopni oxirgi swing-low/high ostiga/ustiga ko'chirish

**Tavsiya:** birinchi 50 savdo — faqat **A varianti**. Bu statistika uchun toza ma'lumot beradi.

### Savdoda vaqt

- Agar savdo **6 soat** davomida hech qaysi tomonga siljiymasa → qo'lda yoping. Impuls so'ndi.
- Pozitsiyani dam olish kunlariga qoldirmang (juma UTC+3 22:00 gacha yoping) — dushanba gapi stopni urib ketishi mumkin.

---

## 7. Pozitsiyani boshqarish

### Pozitsiya hajmini hisoblash

Formula:

```
Pozitsiya hajmi (lotlar) = (Depozit × Xavf%) / (Stop Distance × 1 lot uchun pip qiymati)
```

**Misol:**
- Depozit: $1 000
- Xavf: 0.5% = $5
- Stop Distance: 25 pips
- EUR/USD da 1 lot uchun 1 pip qiymati: $10

```
Hajm = $5 / (25 × $10) = $5 / $250 = 0.02 lot
```

**0.02 lot** ochamiz (mini × 0.02 = mikro 0.02).

**Kalkulyatordan foydalaning:** `tools/position_calculator.py` (ushbu papkada bor) — siz uchun hisoblab beradi.

### Valyutalar bo'yicha pip qiymati (taxminan, USD hisobidan)

| Juftlik | 1 lot uchun 1 pip qiymati |
|---|---|
| EUR/USD | $10 |
| GBP/USD | $10 |
| AUD/USD | $10 |
| USD/JPY | ~$6.7 (kursga bog'liq) |
| USD/CHF | ~$11 (kursga bog'liq) |

**Aniq hisob kalkulyator yoki terminal ichidagi asbob orqali bajarilishi yaxshiroq.**

### QILINMAYDIGANLARI

- ❌ Bir vaqtda 2 tadan ko'p pozitsiya ochish
- ❌ Zarar ko'rayotgan pozitsiyani o'rtalashtirish («o'rtacha narx yaxshilash uchun ko'proq sotib olish»)
- ❌ Stopni narxdan **uzoqroqqa** ko'chirish, «savdoga imkon berish uchun»
- ❌ Foydali savdoni TP ga yetmasdan yopish «burilib ketishidan qo'rqaman» deb (qoidalarga ko'ra bo'lsa — TP yoki SL gacha ushlaymiz)

---

## 8. Grafikdagi ko'rgazma

Aniq signal bo'lgan o'quv misoli:

![Strategiya — ko'rgazma](images/strategy-example.png)

**Ko'rganlarimiz:**

1. **Yuqoriga trend:** narx 1.0820 dan 1.097+ ga harakat qilmoqda, EMA50 (ko'k) va EMA200 (qizil) yuqoriga qarab ajralyapti — klassik trend tuzilmasi.
2. **EMA50 ga orqaga qaytish:** 52–55-shamlarda narx yuqoriga impulsdan keyin EMA50 ga tushdi.
3. **Tasdiqlash buqali shami** 55-shamda.
4. **Kirish nuqtasi:** 1.0961 (signal shami yopilgandan keyin).
5. **Stop Loss:** 1.0936 (25 pips xavf, oxirgi swing-minimumdan past).
6. **Take Profit:** 1.1011 (50 pips, R:R = 1:2).

$1000 depozitdan 0.5% xavf (= $5) va 25 pips stop bilan:
```
Pozitsiya hajmi = 5 / (25 × 10) = 0.02 lot
Potensial foyda = 50 × 10 × 0.02 = $10
Nisbat = $5 xavf / $10 foyda = 1:2 ✓
```

---

## 9. Bektest va forward-test

Demoda savdo qilishdan oldin, strategiyani tarix bo'ylab ishga tushiring.

### TradingView da qo'lda bektest (bepul)

1. EUR/USD ni H1 da so'nggi 3 oy uchun oching.
2. **Davr boshiga qaytib o'ting** (Replay — «Orqaga o'tish» asbobidan foydalaning).
3. Shamlarni birma-bir o'tkazing. Har bir shamda o'zingizga savol bering:
   > Strategiyaning barcha 5 sharti bajarilganmi?
4. Ha bo'lsa — grafik ustiga kirish (o'q), stop, take belgilang.
5. Natijani jurnalga yozing.

**Maqsad:** 3–6 oylik tarix bo'yicha kamida 50 ta savdo.

### Bektest dan keyin hisoblanadigan ko'rsatkichlar

| Metrika | Formula | Yaxshi qiymat |
|---|---|---|
| **Win rate** | Foydali / Jami | ≥ 40% |
| **Avg Win** | Foydalar yig'indisi / Foydali savdolar soni | — |
| **Avg Loss** | Zararlar yig'indisi / Zarar savdolar soni | — |
| **Profit Factor** | Foydalar yig'indisi / Zararlar yig'indisi | ≥ 1.5 |
| **Expectancy** | (Win Rate × Avg Win) − (Loss Rate × Avg Loss) | > 0 |
| **Max Drawdown** | Cho'qqidan maksimal drawdown | Depozitning < 15% |

Agar **Profit Factor < 1.2 yoki Expectancy < 0** — strategiya joriy ko'rinishda ishlamayapti, qayta ishlang.

### Demoda forward-test

Yaxshi bektest dan keyin:
- Real vaqtda demoda kamida **30 ta savdo**
- Natija bektest bilan mos bo'lsa → realga o'tish
- Yomonroq bo'lsa → aniqlashtiring: ehtimol, realda o'z qoidalaringizni buzyapsiz

---

## 10. Strategiya ISHLAMAYDIGAN holatlar

**Hech qanday strategiya har doim ishlamaydi.** Har qanday trend-following strategiya quyidagilarda yomon ishlaydi:

### Yonma-yon harakat (flat)
- H4 da EMA50 va EMA200 bir-biriga o'ralashib, gorizontal ketadi
- Narx darajalar orasida sakraydi
- Soxta signallar seriyasi → zararlar seriyasi

**Yechim:** bunday davrlarda savdo qilmang. Flat belgisi — H4 da EMA200 ning 2–3 kun davomida **5° dan kam qiyaligi**.

### Yangiliklar kunlari (FOMC, NFP)
- Minutda 50–100 pips keskin harakatlar
- Stoplar spayklar bilan urib chiqariladi
- Spredlar 3–5 marta kengayadi

**Yechim:** qizil yangiliklar oldidan va keyin 2 soat ichida savdo ochmang. Foyda allaqachon olingan bo'lsa, NFP oldidan ochiq pozitsiyalarni yoping.

### Past likvidlik
- H4 da EUR/USD da Osiyo sessiyasi (22:00–08:00 UTC+3)
- Juma kechqurun
- Bayramlar (Rojdestvo, Yangi yil, Harvest kunlari)

**Yechim:** faqat London-Amerika oynasida savdo qiling.

### Bozor rejimining o'zgarishi
Ba'zan bozor «xarakter» ini o'zgartiradi — masalan, trend bo'lgan, shovqinli flatga aylandi. So'nggi 20 ta savdoda Profit Factor 1.0 dan past bo'lsa:
- Strategiyani to'xtatib turing
- Yangi ma'lumotlarda bektest ni qayta tekshiring
- Parametrlarni sozlash talab etilishi mumkin

---

## 11. Jurnal orqali strategiyani takomillashtirish

**Savdo jurnali (`journal/` ga qarang) — o'sishning eng kuchli vositasi.**

### Har haftada
- Hafta uchun win rate, profit factor hisoblang
- **Eng yomon 3 ta savdo** ni toping — ularda nima umumiy?
- **Eng yaxshi 3 ta savdo** ni toping — ularda nima umumiy?

### Har oyda
- So'nggi 20 ta savdoni oching va ajrating:
  - Qoidalarga ko'ra, foyda
  - Qoidalarga ko'ra, zarar
  - Qoida buzilishi, foyda (xavfli — «tasodifan omad keldi»)
  - Qoida buzilishi, zarar (klassik)
- Ko'p buzilishlar bo'lsa → muammo strategiyada emas, intizomda

### Har 3 oyda
- Parametrlarni qayta ko'rib chiqing: ehtimol, RSI filtri juda qattiq va yaxshi setaplarni kesib tashlamoqda?
- O'zgarishlarni **faqat yangi savdolarda** sinab ko'ring (qog'ozda yoki demoda)
- Bir vaqtda bir parametrdan ko'pini o'zgartirmang

### Strategiya yetuk ekanining belgilari

- Oydan oyga barqaror win rate ± 5%
- Profit Factor barqaror ≥ 1.3
- Drawdown nazorat ostida (−15% «muvaffaqiyatsizlik oyi» yo'q)
- Savdo «ideal emas» bo'lsa, uni tinch o'tkazib yuborishingiz mumkin

---

[← Asosiy qo'llanmaga qaytish](../forex-guide.md) · [← Texnik tahlil](technical-analysis.md)
