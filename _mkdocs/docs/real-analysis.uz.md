# EUR/USD bo'yicha haqiqiy texnik tahlil

!!! info "🌐 Tarjima / Перевод"
    Bu — sahifaning oʻzbekcha versiyasi. Asl nusxasi rus tilida; tilni sahifa yuqorisidagi til tanlagich orqali almashtirish mumkin.
    *Это узбекская версия страницы; оригинал доступен на русском.*

> Quyidagi barcha grafiklar **EUR/USD H1 bo'yicha haqiqiy tarixiy ma'lumotlar** asosida (1 soatlik shamlar), yfinance orqali yuklab olingan. Hech qanday sintetik ma'lumot yo'q.

---

## EMA 50 / EMA 200 — Trend

Ikki harakatlanuvchi o'rtacha — trend savdosining asosi. EMA50 EMA200 dan yuqori bo'lganda — buqalar trendi. Past bo'lganda — ayiqlar trendi.

![EMA 50/200 haqiqiy ma'lumotlarda](images/real/ema-real.png)

**Nima ko'ramiz:**
- Ko'k chiziq (EMA50) harakatga tezroq munosabat bildiradi
- Qizil (EMA200) — trendning sekin filtri
- Pastdan yuqoriga kesib o'tish = sotib olish signali (Golden Cross)
- Yuqoridan pastga kesib o'tish = sotish signali (Death Cross)

---

## RSI(14) — Ortiqcha sotib olingan / Ortiqcha sotilgan

RSI harakatning kuchini o'lchaydi. 70 dan yuqori — bozor ortiqcha sotib olingan (pastga qaytish mumkin). 30 dan past — ortiqcha sotilgan (yuqoriga sakrash mumkin).

![RSI haqiqiy ma'lumotlarda](images/real/rsi-real.png)

**Nima ko'ramiz:**
- Yuqoridagi qizil zonalar (>70) = xaridorlar uchun ehtiyotkorlik signali
- Quyi yashil zonalar (<30) = sotib olish uchun qiziqish zonasi
- RSI yonma-yon harakatda yaxshi ishlaydi, kuchli trendda noto'g'ri signallar beradi

---

## Bollinger Bands (20, 2) — Volatillik

Bollinger tasmalari narxning «normal» diapazonini ko'rsatadi. Tasmadan chiqish = ekstremal holat, narx ko'pincha o'rtaga qaytadi.

![Bollinger Bands haqiqiy ma'lumotlarda](images/real/bollinger-real.png)

**Nima ko'ramiz:**
- Tasmalar kuchli harakatdan oldin torayadi (volatillik siqilishi)
- Trend davrida kengayadi
- Yuqori tasmaga tegish ≠ sotish signali, tasdiq kerak

---

## MACD (12, 26, 9) — Trend impulsi

MACD ikki EMA o'rtasidagi farqni ko'rsatadi. MACD va signal chizig'ining kesishishi — kirish signallari.

![MACD haqiqiy ma'lumotlarda](images/real/macd-real.png)

**Nima ko'ramiz:**
- Ko'k chiziq (MACD) to'q sariq (signal) ni pastdan yuqoriga kesib o'tsa → buqali signal
- Yashil gistogramma = o'suvchi impuls, qizil = tushuvchi
- Narx va MACD o'rtasidagi farq (divergensiya) = kuchli teskari yo'nalish signali

---

## Haqiqiy savdo signali — Kirish, SL, TP

EMA50 pullback signali qanday ko'rinishini mana shu erda ko'rish mumkin: narx buqalar trendida, EMA50 ga qaytdi, sham kirish ni tasdiqlaydi.

![Haqiqiy EMA50 pullback signali](images/real/strategy-real.png)

**Nima ko'ramiz:**
- Yashil punktir chiziq = kirish narxi
- Qizil punktir chiziq = stop-loss (eng yaqin ekstremum orqasida)
- Yashil punktir chiziq = take-profit (R:R 1:2)

---

## Equity Curves — 8 ta Valyuta Juftligi (Halol natija)

Bu **bitta strategiya (EMA50 pullback)** ning 8 ta turli juftlikda ~2 yillik haqiqiy ma'lumotlar bo'yicha bektest natijasidir.

![Equity curves 8 ta juftlik](images/real/equity-multi-pair-real.png)

!!! warning "Muhim saboq"
    O'rtacha Profit Factor = **1.07** — bu deyarli zararsizlik. Birorta ham juftlik PF ≥ 1.5 ga erishmadi.
    
    **Xulosa:** EUR/USD da yaxshi ishlaydigan strategiya boshqa juftliklarda ham ishlaydi deb bo'lmaydi. Shuning uchun faqat bitta juftlikdagi bektest natijasiga ishonib bo'lmaydi.

---

## Tahlilni o'zingiz qanday ishga tushirish mumkin

Barcha skriptlar allaqachon loyihada mavjud:

```bash
# Yangi ma'lumotlarni yuklab olish (8 juftlik × 2 vaqt oralig'i)
python advanced/download_all_pairs.py

# Yangi ma'lumotlar asosida barcha 6 ta grafikni qayta yaratish
python tools/chart_generator_real.py

# Ko'p juftlikli bektest ishga tushirish
python advanced/multi_pair_backtest.py

# Bugungi iqtisodiy taqvim (Forex Factory)
python tools/news_scraper.py
```

---

## Iqtisodiy taqvim (Forex Factory)

Bizda `tools/news_scraper.py` skripti mavjud — u bugungi muhim voqealarni yuklab oladi:

```bash
# Bugungi muhim voqealarni ko'rsatish
python tools/news_scraper.py

# Ertaga
python tools/news_scraper.py --date tomorrow

# Shu hafta uchun
python tools/news_scraper.py --date this-week
```

Qizil belgili voqealar (yuqori ta'sir) — eng muhimlari. Bular:
- **NFP** (Non-Farm Payrolls) — har oyning birinchi juma kunida
- **FRS / YMB** tomonidan foiz stavkasi bo'yicha **qarorlar**
- **CPI** (inflyatsiya)
- **GDP** (YIM)

!!! tip "Yangi boshlovchilar uchun qoida"
    Qizil voqealardan 30 daqiqa oldin va 30 daqiqa keyin savdo qilmang. Volatillik keskin oshadi va stop-loss normal harakat bo'lmasdan uchirib yuborilishi mumkin.
