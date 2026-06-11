# Trading Journal — shablon

> Har bir savdoni yoz. Jurnal bo'lmasa — taraqqiyot yo'q.

---

## 1-savdo — namuna

### Kontekst
- **Sana / vaqt:** 2026-05-13, 14:30 (UTC+5)
- **Juftlik:** EUR/USD
- **Taymfreym:** H1 (tahlil), H4 (trend)
- **Setup:** EMA50 ga qaytish + o'yinchi shamdon yutishi (bullish engulfing)
- **Yo'nalish:** Long

### Savdo oldidan tahlil
- **H4 trendi:** o'suvchi, narx EMA200 dan yuqori ✓
- **H1 tuzilmasi:** higher highs, higher lows ✓
- **Signal:** 14:00 shamdon — EMA50 da to'g'ridan-to'g'ri bullish engulfing ✓
- **RSI(14):** 52 (neytral, chegaralarda emas) ✓
- **Yangiliklar:** yaqin 2 soatda qizil yangilik yo'q ✓
- **Chek-list:** barcha 5 ta ☑

### Savdo parametrlari
| Parametr | Qiymat |
|---|---|
| Kirish narxi | 1.0852 |
| Stop Loss | 1.0827 (−25 pips) |
| Take Profit | 1.0902 (+50 pips) |
| R:R | 1:2 |
| Pozitsiya hajmi | 0.02 lot |
| Xavf ($) | $5.00 ($1000 dan 0.5%) |

### Natija
| | |
|---|---|
| Yopilish narxi | 1.0902 |
| Yopilish vaqti | 16:45 |
| Pips natijasi | +50 |
| $ natijasi | +$10.00 |
| R-natija | +2R |
| **Yakun** | **WIN** |

### Sharh
- **Qoidalarga rioya qildingizmi?** Ha (chek-listning barcha 5 bandi)
- **Savdo oldidagi his-tuyg'ular:** xotirjam
- **Savdo davomidagi his-tuyg'ular:** −10 pips ga qaytishda ozgina hayajon, stopni qimirlatmadim
- **Savdodan keyingi his-tuyg'ular:** qoniqish
- **Yaxshi qilgan narsam:** signal shamdonining yopilishini kutdim, shakllanayotganda kirmadam
- **Xatolar:** yo'q
- **Xulosa:** intizom + sabr = rejalashtirilgan foyda. Takrorlash kerak.

### Grafik skrinshotlari
*(Notion / Obsidian / Google Doc da yuritayotgan bo'lsangiz — havola yoki rasm qo'shing)*

---

## 2-savdo — namuna (rejalashtirilgan zarar)

### Kontekst
- **Sana / vaqt:** 2026-05-13, 18:20
- **Juftlik:** GBP/USD
- **Taymfreym:** H1 / H4
- **Setup:** H4 qarshilik darajasidagi pin-bar
- **Yo'nalish:** Short

### Parametrlar
| | |
|---|---|
| Kirish | 1.2655 |
| SL | 1.2680 (+25 pips) |
| TP | 1.2605 (−50 pips) |
| R:R | 1:2 |
| Lot | 0.02 |
| Xavf | $5.00 |

### Natija
| | |
|---|---|
| Yopilish | 1.2680 (stop) |
| Vaqt | 20:10 |
| Natija | −25 pips, −$5.00, −1R |
| **Yakun** | **LOSS** |

### Sharh
- **Qoidalarga rioya qildingizmi?** Ha
- **His-tuyg'ular:** hafsalasizlik, lekin tilt yo'q
- **Yaxshi qilgan narsam:** setupni to'g'ri tanidim, stopni qimirlatmadim
- **Xatolar:** yo'q — reja bo'yicha toza zarar
- **Xulosa:** reja bo'yicha zararlar statistikaning normal qismi. R:R 1:2 va win rate 40% da ham foydalidamiz. **Qoplanishga urinmang** — keyingi savdo faqat signal bo'lganda.

---

## Yangi savdo shabloni (ko'chirish uchun)

```markdown
## Savdo №___

### Kontekst
- **Sana / vaqt:**
- **Juftlik:**
- **Taymfreym:**
- **Setup:**
- **Yo'nalish:** Long / Short

### Savdo oldidan tahlil
- **H4 trendi:**
- **H1 tuzilmasi:**
- **Signal:**
- **RSI(14):**
- **Yangiliklar:**
- **Chek-list o'tildi:** ha / yo'q

### Parametrlar
| Parametr | Qiymat |
|---|---|
| Kirish narxi | |
| Stop Loss | |
| Take Profit | |
| R:R | |
| Pozitsiya hajmi | |
| Xavf ($) | |

### Natija
| | |
|---|---|
| Yopilish narxi | |
| Yopilish vaqti | |
| Pips natijasi | |
| $ natijasi | |
| R-natija | |
| **Yakun** | WIN / LOSS / BREAKEVEN |

### Sharh
- **Qoidalarga rioya qildingizmi?**
- **His-tuyg'ular:**
- **Yaxshi qilgan narsam:**
- **Xatolar:**
- **Xulosa:**
```

---

## Haftalik hisobot

Hafta oxirida quyidagilarni yig'ing:

```
Hafta ___ (sanadan sanagacha)

Jami savdolar: ___
Foydali: ___ (___%)
Zararli: ___
Beziyon: ___

Foyda yig'indisi: $___
Zarar yig'indisi: $___
Sof natija: $___ (depozitning ___%)

Profit Factor: ___ (foyda ÷ zarar)
O'rtacha foyda (Avg Win): $___
O'rtacha zarar (Avg Loss): $___

Eng yaxshi savdo: №___ (+$___)
Eng yomon savdo: №___ (−$___)

Qoida buzilishlari: ___
  - Qanday:
  - Nima uchun:

Haftaning asosiy xulosalari:
1.
2.
3.

Keyingi hafta uchun reja:
1.
2.
```
