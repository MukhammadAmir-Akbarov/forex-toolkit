# Tools — yordamchi skriptlar

| Skript | Maqsad |
|---|---|
| [`position_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/position_calculator.py) | Risk-menedjment asosida pozitsiya hajmini (lotlarda) hisoblash |
| [`margin_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/margin_calculator.py) | Marja kalkulyatori: ochiq pozitsiya depozitning qancha qismini bloklashini ko'rsatadi |
| [`chart_generator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/chart_generator.py) | Hujjatlar uchun o'quv grafiklarini yaratish |

## position_calculator.py

Risk-menedjmentingizga asoslanib pozitsiya hajmini lotlarda hisoblaydi.

### Interaktiv rejim

```bash
.venv/bin/python tools/position_calculator.py
```

```
=== Kalькулятор размера позиции ===

Депозит ($): 1000
Риск на сделку (%, например 0.5): 0.5
Стоп-лосс (в пипсах): 25
Пара (EURUSD / GBPUSD / USDJPY / ...): EURUSD

╭─────────────────────────────────────────╮
│  КАЛЬКУЛЯТОР РАЗМЕРА ПОЗИЦИИ            │
╰─────────────────────────────────────────╯

Входные данные:
  Депозит:           $1,000.00
  Риск:              0.50% = $5.00
  Стоп-лосс:         25 пипсов
  Пара:              EURUSD
  Стоимость пипса:   $10.00 за 1 лот

Расчёт:
  Размер (точный):   0.0200 лота
  Размер (округл.):  0.02 лота
  Реальный риск:     $5.00 (0.50%)

→ Выстави в терминале: 0.02 лота
```

### Bir qatorli rejim

```bash
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD
```

### Parametrlar

| Flag | Ma'nosi |
|---|---|
| `--balance` / `-b` | Depozit USD da |
| `--risk` / `-r` | Xavf foizi (0.5 = 0.5%) |
| `--stop` / `-s` | Stop-lossgacha bo'lgan masofa (pipsda) |
| `--pair` / `-p` | Valyuta juftligi (sukut bo'yicha EURUSD) |
| `--list-pairs` | Qo'llab-quvvatlanadigan juftliklar ro'yxatini ko'rsatish |

### Yaxlitlash mantig'i

Hajm har doim **pastga** 0.01 gacha yaxlitlanadi (ko'pchilik brokerlardagi minimal qadam). Bu **real xavf rejalanganidan kamroq** bo'lishini anglatadi — bu xavfsizroq.

Minimum 0.01 lot. Agar hisoblash undan kichik natija bersa (kichik depozit + katta stop), skript ogohlantiradi: real xavf belgilangan chegaradan oshib ketishi mumkin.

### Ogohlantirishlar

- ⚠️ Agar real xavf rejalanganidan katta bo'lsa (yaxlitlash tufayli) — pozitsiyani qo'lda kamaytirish taklif qilinadi.
- ⚠️ Agar real xavf depozitning 2% dan oshsa — yangi boshlovchilar uchun bu ko'p ekanligiga doir ogohlantirish chiqadi.

---

## chart_generator.py

Hujjatlar uchun PNG-rasmlar yaratadi. Bir marta ishlatiladi — barcha rasmlar allaqachon `docs/images/` papkasida yaratilgan. Qayta ishga tushirish faqat vizual uslubni o'zgartirmoqchi bo'lsangiz yoki yangi illyustratsiyalar qo'shmoqchi bo'lsangiz kerak bo'ladi.

```bash
.venv/bin/python tools/chart_generator.py
```

Yaratiladi:

- `candle-anatomy.png` — yapon shamining anatomiyasi
- `candle-patterns.png` — bolg'a, yutish, doji, tushayotgan yulduz
- `trend-types.png` — trend turlari (yuqoriga / pastga / flat)
- `support-resistance.png` — qo'llab-quvvatlash va qarshilik darajalari
- `ema-example.png` — EMA 50 va EMA 200
- `rsi-example.png` — RSI indikatori
- `macd-example.png` — MACD indikatori
- `bollinger-example.png` — Bollinger Bands
- `chart-patterns.png` — bosh va yelkalar, uchburchak, ikki tepa
- `strategy-example.png` — strategiya setupining illyustratsiyasi
- `risk-reward.png` — win rate × R:R jadvali
- `drawdown-math.png` — barbod bo'lish matematikasi

Barcha ma'lumotlar **sintetik** — tushunchalarni ko'rsatish uchun, real kotirovkalar emas.

---

[← Asosiy qo'llanmaga qaytish](../forex-guide.md)
