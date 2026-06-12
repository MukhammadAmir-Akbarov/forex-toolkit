# 🎮 Replay Mashqi — tarixiy bozorda savdo qiling

!!! abstract "Bu nima"
    Mashqchi arxivdan **real EURUSD H1 shamlarini** ko'rsatadi — siz X nuqtasigacha
    bo'lgan tarixni ko'rasiz, qaror qabul qilasiz (Buy / Sell / O'tkazib yubor)
    va stop-loss qo'yasiz. Keyin vidjet kelajakdagi shamlarni ijro etadi va
    natijani **R-ko'paytmada** ko'rsatadi.

    **R-ko'paytma = foyda / stop hajmi.** Maqsadingiz: izchil +R olish
    (take-profit 2R, stop 1R → nisbat 1:2).

!!! tip "To'g'ri mashq qilish"
    1. Faqat shamlarga qarang — "buni ko'rganman…" deb o'ylamang
    2. Stop-lossni Buy/Sell bosishdan **oldin** qo'ying — bu majburiy shart
    3. Maqsad taxmin qilish emas, balki **o'z qoidalaringiz** asosida qaror qabul qilish
    4. 20 epizoddan so'ng statistikangizni kutilayotgan EV bilan solishtiring

!!! warning "Ta'limiy material — moliyaviy maslahat emas"
    Barcha epizodlar arxiv ma'lumotlaridan olingan. O'tgan samaradorlik kelajakdagi
    natijalarni kafolatlamaydi. Forex savdosi katta yo'qotish xavfi bilan birga keladi.

---

<div id="replay-widget" data-src="../../../data/replay-episodes.json"></div>

---

## Natijani o'qish

| Ko'rsatkich | Ma'nosi |
|---|---|
| **+2.0R** | Foyda stop hajmidan ikki baravar ko'p (2R take-profit ishladi) |
| **-1.0R** | Stop-loss ishladi (yo'qotish stop hajmiga teng) |
| **WinRate** | Barcha kirishlardan foydali savdolar foizi (skiplar hisobsiz) |
| **Avg R** | Sessiya uchun o'rtacha R — 0 dan katta bo'lishi kerak |

!!! note "Statistika brauzerda saqlanadi"
    Har bir sessiya natijalari `localStorage`da saqlanadi. Keyingi tashrifda
    progress saqlanmaydi — har bir sessiya noldan boshlanadi.

---

## Epizodlar to'plamini qayta yaratish

Epizodlar [`tools/replay_cutter.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/replay_cutter.py)
skripti yordamida `data/EURUSD_1h.csv` arxividan yaratilgan:

```bash
python tools/replay_cutter.py \
  --pair EURUSD --tf 1h \
  --episodes 20 --context 30 --outcome 15 \
  --output _mkdocs/data/replay-episodes.json
```

`--context` (tarix shamlari) va `--outcome` (kelajak shamlari) bayroqlarini o'zgartirish mumkin.
Skript kategoriyalarni avtomatik muvozanatlaydi: ≈1/3 ko'tariluvchi, 1/3 tushuvchi, 1/3 yon harakat.
