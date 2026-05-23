# 📡 Ma'lumotlar va signallar manbalari

!!! warning "«Signallar» haqida muhim"
    Forexda «signal» ko'pincha **«guru»dan to'lovli maslahatni** anglatadi — masalan, «EURUSD ni hozir SOTIB OLING». **Bu asosan firibgarlik.** Agar kimdir aniq signallarni bilgan bo'lsa, ularni $50/oyga sotmasdi, balki o'zi savdo qilardi.

    Bu sahifa boshqa narsa haqida: **mustaqil qaror qabul qilishingizga yordam beradigan saytlar.**

## 📅 1. Iqtisodiy taqvim (eng asosiy)

| Sayt | Tavsif |
|---|---|
| **[ForexFactory.com](https://www.forexfactory.com/calendar)** | Sanoat standarti. Impact bo'yicha filtr (🔴 high). Savdo ochishdan **24 soat oldin** qarang. |
| **[Investing.com](https://www.investing.com/economic-calendar/)** | Rus tilidagi muqobil. |
| **[FxStreet.com](https://www.fxstreet.com/economic-calendar)** | Prognozlar va tahlil bilan. |

**Asosiy hodisalar**: NFP (birinchi juma), FOMC, ECB, BoE, CPI, GDP.

!!! danger "Qoida"
    **Yuqori ta'sirli hodisadan 30 daqiqa oldin va keyin savdo qilmang.** Spred 5-10 marta kengayadi, sirpanish stoplaringizni yo'q qiladi.

## 📈 2. Grafiklar va tahlil

| Sayt | Nima uchun |
|---|---|
| **[TradingView.com](https://www.tradingview.com/chart/)** | Oltin standart, bepul. Barcha indikatorlar, multi-taymfreymlar, ogohlantirishlar. |
| **MT5 brokeringizda** | Real savdolar, kirishlar, stop/take ogohlantirishlari uchun. |
| **[Finviz.com/forex](https://finviz.com/forex.ashx)** | Barcha juftliklar bo'yicha issiqlik xaritasi — qaerda kuchli harakat borligini darhol ko'rish. |

## 📊 3. Kayfiyat / pozitsiyalash

«Olomon nima qilyapti? Institutlar nima qilyapti?»

| Sayt | Nimani ko'rsatadi |
|---|---|
| **[IG Client Sentiment](https://www.dailyfx.com/sentiment)** | Chakana treyderlarning % long vs short. 80%+ chakana bir tomonda bo'lsa, bozor ko'pincha **ularga qarshi** boradi (qarama-qarshi indikator). |
| **[CFTC COT Report](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)** | Yirik institutsional pozitsiyalar bo'yicha haftalik hisobot. 3 kunlik kechikish, lekin «aqlli pul» qayerga qaraganini ko'rsatadi. |
| **[Myfxbook Community Outlook](https://www.myfxbook.com/community/outlook)** | IG bilan o'xshash, brokerlar bo'yicha jamlangan. |

## 📰 4. Yangiliklar va makro

| Sayt | Nima uchun |
|---|---|
| **[ForexLive.com](https://www.forexlive.com/)** | Forex uchun eng yaxshi breaking news. Bepul. |
| **[Reuters Markets](https://www.reuters.com/markets/)** | Rasmiy bozor tahlili. |
| **[Federal Reserve calendar](https://www.federalreserve.gov/newsevents/calendar.htm)** | Fed nutqlari jadvali. ECB / BoE / BoJ ham mavjud. |
| **[CentralBanks.io](https://www.centralbanks.io/)** | Barcha markaziy banklarning kalit stavkalari bir joyda. |

## 🔗 5. Korrelyatsiyalar

Juda muhim, lekin baholanmagan mavzu. **Agar EURUSD long va GBPUSD long savdo qilayotgan bo'lsangiz, bu mohiyatan bitta savdo** (ikkalasi USD ga teskari korrelyatsiyada).

| Sayt | Tavsif |
|---|---|
| **[Mataf Currency Correlation](https://www.mataf.net/en/forex/tools/correlation)** | Real vaqt rejimida korrelyatsiya matritsasi. |
| **[Myfxbook Correlation](https://www.myfxbook.com/forex-market/correlation)** | Muqobil. |
| `tools/market_correlations.py` (sizning loyihangiz) | DXY / gold / SPY bilan mahalliy korrelyatsiya. |

## ⚡ 6. Volatillik

«Bu juftlik odatda qancha harakatlanadi? Adekvat stop qancha?»

| Sayt | Nima uchun |
|---|---|
| **[Mataf Volatility](https://www.mataf.net/en/forex/tools/volatility)** | Har bir juftlikning o'rtacha kunlik diapazoni pipsda. |
| **[CBOE VIX](https://www.cboe.com/tradable_products/vix/)** | S&P bo'yicha «qo'rquv indeksi». Yuqori VIX = asabiy bozor = forex ham titraydi. |

## 🏦 7. Markaziy banklar taqvimi

| Sayt | Tavsif |
|---|---|
| **[ForexLive Central Bank section](https://www.forexlive.com/CentralBank/)** | Kim va qachon nutq so'zlaydi, nima deydi. |
| **[CentralBanks.io](https://www.centralbanks.io/)** | Joriy stavkalar. |

---

## 🚫 Nimani kuzatish KERAK EMAS

| Manba | Nima uchun |
|---|---|
| ❌ Pulli «signal services» | 99% — yutqazadigan signallarni sotadi. Agar ular ishlasa, sotuvchilar o'zlari savdo qilardi. |
| ❌ Telegram «gurular» 10× va'da bilan | Tanlash effekti: faqat g'alabalarni ko'rsatadi, mag'lubiyatlardan jim chiqib ketadi. |
| ❌ Twitter/X chaqiruvchilar «BUY EURUSD NOW» | Mantiqsiz tushuntirish — bu shovqin, signal emas. |
| ❌ YouTube «Forexda $50K topdim» | YouTube reklamasi uchun klikbait, siz uchun emas. |
| ❌ Brokerlarning research desk | Manfaatlar to'qnashuvi: ko'proq savdo qilsangiz, ularga ko'proq komissiya. |

## 🛠️ Sizning o'z asboblaringiz

Loyihada avtomatlashtirilgan asboblar mavjud:

```bash
# News scraper — bugungi yuqori ta'sirli hodisalar
.venv/bin/python tools/news_scraper.py --high-only

# Pattern scanner — CSV da sham patternlari
.venv/bin/python tools/pattern_scanner.py --csv data.csv

# Market correlations — DXY / gold / SPY bilan
.venv/bin/python tools/market_correlations.py

# Telegram alerts — EMA50 kesib o'tish ogohlantirishlari
.venv/bin/python advanced/telegram_alerts.py
```

---

## 🎯 Kunlik ish jarayoni (tavsiya)

| Vaqt | Nima | Qayerda |
|---|---|---|
| **Ertalab (09:00)** | Bugungi taqvim | ForexFactory |
| **Savdo oldidan** | Sentiment + COT | DailyFX + CFTC |
| **Pozitsiya ochish** | Hajm hisoblash | [Pozitsiya kalkulyatori](../tools/position-calculator.md) |
| **Kun davomida** | EMA50 kesib o'tish ogohlantirishlari | sizning Telegram-botingiz |
| **Kechqurun (22:00)** | Jurnal yozuvi | `tools/journal_cli.py` |
| **Haftada bir** | Sharh + COT yangilanishi | `tools/journal_analyzer.py` + CFTC |

!!! tip "Asosiy qoida"
    **Vaqtning 80% — kuzatish, 20% — harakat.** Aksariyat yangi boshlovchilar buning aksini qiladi: 5 daqiqa qarash, savdo ochish, keyin butun kun stoplarni hissiy ravishda ko'chirish.

---

## ⚠️ Mas'uliyatdan ozod qilish

Bu **o'quv** ko'rinish. Barcha havolalar — ochiq, bepul, hamkorlik havolalari yo'q. Uchinchi tomon xizmatlaridan foydalanishdan oldin ularni **o'zingiz tekshiring**. Savdo qarorlari faqat siznikidir.
