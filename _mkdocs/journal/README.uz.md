# Trading Journal — qanday foydalanish

Shablonning ikki formati:

- [`trading-journal-template.md`](trading-journal-template.md) — Markdown'da yuritish uchun (Obsidian, Notion, VSCode). Batafsil tahlil uchun qulay.
- [`trading-journal-template.csv`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/journal/trading-journal-template.csv) — Google Sheets / Excel'ga import qilish uchun. Statistika va grafiklar uchun qulay.

## Qanday boshlash

### 1-variant: Google Sheets (boshlovchilar uchun tavsiya etiladi)

1. [sheets.google.com](https://sheets.google.com) ni oching
2. Fayl → Import → Yuklash → `trading-journal-template.csv` ni tanlang
3. Import turi: «Varaqni almashtirish»
4. Ikkinchi varaqda tahlil uchun formula sarlavhalarini yarating:

```
B2: =COUNTIF(Trades!U:U,"Win")                 // g'alabalar soni
B3: =COUNTIF(Trades!U:U,"Loss")                // yutqiziqlar soni
B4: =B2/(B2+B3)                                // win rate
B5: =SUMIF(Trades!U:U,"Win",Trades!S:S)        // foydalar yig'indisi
B6: =-SUMIF(Trades!U:U,"Loss",Trades!S:S)      // zararlar yig'indisi (mutlaq qiymat)
B7: =B5/B6                                     // profit factor
B8: =B5+SUMIF(Trades!U:U,"Loss",Trades!S:S)    // sof P&L
```

### 2-variant: Obsidian / VSCode'da Markdown

1. `trading-journal-template.md` ni o'z papkangizga ko'chiring
2. Har bir savdodan keyin: «Yangi savdo shabloni» blokini ko'chirib to'ldiring
3. Oyiga bitta fayl (`2026-05.md`, `2026-06.md`…)
4. Har hafta oxirida — haftalik hisobot qo'shing

### 3-variant: Notion

Quyidagi maydonlar bilan baza yarating:

| Maydon | Turi |
|---|---|
| ID | Number |
| Sana | Date |
| Juftlik | Select |
| Yo'nalish | Select (Long / Short) |
| Setup | Text |
| Kirish / SL / TP | Number |
| Lot hajmi | Number |
| Xavf $ | Number |
| Natija $ | Number |
| R-natija | Number |
| Yakun | Select (Win / Loss / BE) |
| Qoidalarga rioya? | Checkbox |
| His-tuyg'ular | Multi-select |
| Xatolar | Text |
| Xulosa | Text |
| Skrinshot | Files |

## Mutlaq majburiy maydonlar

Har bir savdo uchun minimum:

1. **Sana + vaqt** — kun ichidagi vaqt bo'yicha tahlil uchun
2. **Juftlik + yo'nalish**
3. **Kirish narxi / SL / TP / lot**
4. **Natija** (pips va $ majburiy, R ixtiyoriy)
5. **Qoidalarga rioya qildingizmi?** (ha/yo'q) — xulq-atvor bo'yicha eng muhim belgilash
6. **1–2 jumla xulosa**

Batafsil maydonlar (his-tuyg'ular, skrinshot, keng ko'lamli tahlil) — istalgan, lekin blokerlar emas. Minimumdan boshlang, odatlanib borgan sari qo'shing.

## Har haftada hisoblanadigan ko'rsatkichlar

Google Sheets ni oching va hisoblang:

| Ko'rsatkich | Yaxshi natija |
|---|---|
| Win rate | ≥ 40% (R:R 1:2 uchun) |
| Profit Factor | ≥ 1.5 |
| Avg Win / Avg Loss | ≥ 2.0 |
| Sof P&L | > 0 |
| Haftadagi maks. drawdown | < 6% depozit |
| Qoidalarga rioya qilingan savdolar | ≥ 95% |

Agar **qoidalarga rioya qilingan savdolar < 95%** bo'lsa — muammo **strategiyada emas, intizomda**. Birinchi navbatda shuni tuzating.

## Tahlilda nima qidirish kerak

30+ savdodan keyin jurnalni oching va savol bering:

- **Kunning qaysi vaqtida** ko'proq foydali bo'lasiz? (masalan, ertalabki savdolar = plus, kechkilari = minus)
- **Haftaning qaysi kunida** yomonroq? (masalan, juma = plus, dushanba = minus)
- **Qaysi juftliklarda** ko'proq yutasiz?
- Qoidalarga asoslangan setuplar va «intuitiv» savdolar — natijalarda farq bormi?
- **Qaysi his-tuyg'u holatida** pul yo'qotasiz?

Bu xulosalar har qanday indikatordan muhimroq.
