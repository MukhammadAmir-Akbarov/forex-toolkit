# Bot — signal detektori va bektest

> **⚠️ MUHIM: bu JONLI savdo boti EMAS.**
>
> Bu kod brokerga ulanmaydi va haqiqiy orderlar ochmaydi. Bu quyidagilar uchun **o'quv vositasi**:
> - Strategiyaning kodda qanday ifodalanishini tushunish
> - Strategiyani tarixiy ma'lumotlarda ishlatish (bektest)
> - Statistikani hisoblash: win rate, profit factor, expectancy, drawdown
>
> Haqiqiy hisobga biror narsa ulashdan oldin, kamida quyidagilar kerak: demo savdoda bir yil tajriba, broker API ni tushunish, xatolarni qayta ishlash, buglardan himoya, risk cheklashlari, testlar.

## Ichida nima bor

| Fayl | Maqsad |
|---|---|
| [`strategy.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/bot/strategy.py) | Strategiya logikasi: indikatorlar, patternlar, signal detektori |
| [`backtest.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/bot/backtest.py) | Ma'lumotlarni yuklash, bitimlarni simulyatsiya qilish, statistika, equity curve |

## Ishga tushirish

```bash
# Loyiha ildizidan, venv faollashtirilgandan so'ng
.venv/bin/python bot/backtest.py

# Bitimlar ro'yxati va grafik saqlash bilan
.venv/bin/python bot/backtest.py --out my-curve.png --trades-csv my-trades.csv

# O'z CSV-ma'lumotlaringizda
.venv/bin/python bot/backtest.py --csv ../data/eurusd_h1.csv

# Boshqa R:R bilan
.venv/bin/python bot/backtest.py --rr 3.0
```

## Natija nima anglatadi

```
Jami bitimlar:        9
Foydali:              5
Zararli:              4
Win rate:             55.6%
O'rtacha win:         +2.00R
O'rtacha loss:        −1.00R
Profit Factor:        2.50
Expectancy:           +0.67R / bitim
Jami:                 +6.00R
Maks. drawdown:       1.00R
```

- **R** — risk birligi (1R = sizning stop). +2R demak «riskingizdan 2 barobar ko'p oldingiz».
- **Win rate 55.6%** — foydali bitimlar ulushi.
- **Profit Factor 2.50** — har $1 zararga $2.50 foyda to'g'ri keladi. Yaxshi.
- **Expectancy +0.67R** — **bitta** bitimning kutilgan natijasi. 100 bitimda = +67R foyda.
- **Max drawdown 1.00R** — cho'qqidan maksimal pasayish.

## Equity curve

Ishga tushirilgandan so'ng skript yonida `bot/equity-curve.png` fayli kumulyativ
natija bilan paydo bo'ladi. Bu yerda rasm ataylab yo'q: egri chiziq sening
ma'lumotlaring bo'yicha hisoblanadi va repozitoriyga qo'shilmaydi — birovnikiga
emas, o'zingnikiga qara.

Yaxshi equity curve **chapdan pastdan o'ngga yuqoriga boshqariladigan drawdownlar bilan ketadi**. Keskin tushishlar, nol yoki salbiy dinamika — strategiya ishlamayotganining belgisi.

## Bu bot nima QILMAYDI (ataylab)

- ❌ MetaTrader / cTrader / broker API ga ulanmaydi
- ❌ Haqiqiy orderlar ochmaydi
- ❌ Spread, komissiya, slippage, svoplarni hisobga olmaydi (soddalashtirilgan)
- ❌ Ko'p vaqt oralig'i tahlilini ishlatmaydi (soddalashtirilgan — joriy TF da EMA200 ishlatadi)
- ❌ Yangiliklar filtri yo'q

Bu cheklovlar muhim: **hisobdagi haqiqiy natija har doim bektest dan yomonroq bo'ladi**. Buni hisobga oling.

## Bektest ni halol «yaxshilash» usullari

1. **Parametrlarni moslashtirmang**. Agar siz RSI chegaralarini ideal grafik chiqmaguncha aylantirsangiz — bu **overfitting**, haqiqatda ishlamaydi.
2. **In-sample / out-of-sample**: bir yarmi ma'lumotlarda sozlang, ikkinchisida tekshiring.
3. **Walk-forward**: ketma-ket tarix oynalarida test qiling, bittasida emas.
4. **Spreadni hisobga oling**: har bir bitim foydasidan 1–2 pips ayiring.
5. **Demoda haqiqiy win rate odatda bektest dan 5–10% past bo'ladi** — psixologiya va ijro sababli.

## O'z ma'lumotlaringiz uchun CSV formati

Tarixiy ma'lumotlarni bepul yuklab olish mumkin:
- [Dukascopy Historical Data](https://www.dukascopy.com/swiss/english/marketwatch/historical/)
- MT5 terminalida: F2 → CSV ga eksport qiling
- TradingView: o'ng panel → Ma'lumotlarni eksport qilish (Pro obuna uchun)

Kutilayotgan ustunlar:

```csv
datetime,open,high,low,close
2026-01-01 00:00:00,1.08500,1.08620,1.08480,1.08590
2026-01-01 01:00:00,1.08590,1.08650,1.08550,1.08610
...
```

## Bu skriptdan haqiqiy botga yo'l

**Bu uzun yo'l.** Agar qachondir hal qilsangiz:

1. **Kamida 6–12 oy** xuddi shu strategiya bilan demoda qo'lda savdo. Qo'lda plus bermasa — algoritm ham saqlamaydi.
2. **Broker API ni o'rganing**: MetaTrader 5 ning Python paketi bor [`MetaTrader5`](https://pypi.org/project/MetaTrader5/) — lekin faqat Windows da ishlaydi.
3. **Avval** kamida 3 oy **faqat demoda** bot orqali savdo qiling.
4. **Faqat demo-botda barqaror musbat savdodan so'ng** — minimal depozit bilan haqiqiy hisob.
5. **Hech qachon** botni nazoaratsiz qoldirmang. Xatoliklar, MT5 yangilanishlari, koddagi buglar — bularning barchasi depozitni bir soatda yiqitishi mumkin.

## Disclaimer

O'quv kodi. Joriy holatda haqiqiy hisoblarda ishlatmang. Bektest ning o'tgan statistikasi kelajakdagi natijalarni kafolatlamaydi. Kod muallifi uning asosida qabul qilingan qarorlar uchun javobgar emas.

---

[← Asosiy qo'llanmaga qaytish](../forex-guide.md)
