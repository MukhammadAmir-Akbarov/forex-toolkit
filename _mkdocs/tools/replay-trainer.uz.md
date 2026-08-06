---
widgets: [replay]
---

# 🎮 Replay Mashqi — tarixiy bozorda savdo qiling

!!! abstract "Bu nima"
    Mashqchi **EURUSD, GBPUSD, USDJPY va EURJPY** uchun **H1 va D1** arxiv
    shamlarini ko'rsatadi. Bozor va yo'nalishni tanlab, **Entry / SL / TP ni
    grafikning o'zida** belgilang. Keyin vidjet kelajak shamlarini ijro etadi
    va natijani **R-ko'paytmada** ko'rsatadi.

    **R-ko'paytma = foyda / stop hajmi.** Maqsadingiz: izchil +R olish
    (take-profit 2R, stop 1R → nisbat 1:2).

!!! tip "To'g'ri mashq qilish"
    1. Faqat shamlarga qarang — "buni ko'rganman…" deb o'ylamang
    2. Buy/Sell ni tanlang, keyin Entry, SL va TP darajalarini bosing
    3. Replayni boshlashdan oldin darajalar tartibini tekshiring
    4. Sessiyadan keyin zararli epizodlarni alohida tugma bilan takrorlang

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
    Sessiya xulosasi, zaif bozor kategoriyasi va xato epizodlar `localStorage`da
    saqlanadi. O'quv kabineti keyingi tavsiya uchun ulardan foydalanadi.

!!! info "Klaviatura va qulaylik"
    Buy uchun **B**, Sell uchun **S**, o'tkazib yuborish uchun **Space** ni
    bosing; darajalarni tanlash va siljitish uchun strelkalardan foydalaning.
    Grafik ostida matnli tavsif va so'nggi shamlar jadvali mavjud. Ko'rinadigan
    kontur fokus grafikda ekanini bildiradi.

Jurnal shaxsiy vazifa yaratsa, Replay uni grafik ustida ko'rsatadi va mos
mashqlardan keyin progressni oshiradi.

---

## Epizodlar to'plamini qayta yaratish

Epizodlar [`tools/replay_cutter.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/replay_cutter.py)
skripti yordamida `data/EURUSD_1h.csv` arxividan yaratilgan:

```bash
python tools/replay_cutter.py \
  --pairs EURUSD,GBPUSD,USDJPY,EURJPY \
  --timeframes 1h,1d \
  --episodes 6 --context 30 --outcome 15 \
  --output _mkdocs/data/replay-episodes.json
```

`--episodes` har bir bozor va taymfreym uchun epizodlar sonini belgilaydi.
Skript JPY pip hajmini to'g'ri ishlatadi va kategoriyalarni muvozanatlaydi.
