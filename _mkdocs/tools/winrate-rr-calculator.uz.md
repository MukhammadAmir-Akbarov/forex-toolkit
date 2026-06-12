# 📊 Win Rate × Risk-Reward — daromadlilik kalkulyatori

!!! abstract "Trejdingning asosiy matematikasi"
    Tajribali treyderning amaliyotidan: «Bu eng ko'p beriladigan savol — nega men minsudaman?»

    **Javob:** sizning Win Rate (foydali savdolar %) va RR (Risk-Reward Ratio) — qat'iy matematika bilan bog'liq. Agar siz bu nisbatni saqlamasangiz — siz **matematika bo'yicha** minusdasiz, «omadsizlik» emas.

---

## 🧮 Interaktiv kalkulyator

<div class="calc-widget">

<div class="calc-row">
  <label>Win Rate (foydali savdolar %)</label>
  <input type="number" id="wr-input" min="1" max="99" step="1" value="50">
  <span>%</span>
</div>

<div class="calc-row">
  <label>Risk-Reward Ratio (RR)</label>
  <input type="number" id="rr-input" min="0.1" max="20" step="0.1" value="1.5">
  <span>(1 xavf : N mukofot)</span>
</div>

<div class="calc-row">
  <label>Savdolar soni (prognoz uchun)</label>
  <input type="number" id="trades-input" min="10" max="1000" step="10" value="100">
</div>

<div class="calc-row">
  <label>Bir savdodagi xavf (% depozit)</label>
  <input type="number" id="risk-input" min="0.1" max="10" step="0.1" value="1">
  <span>%</span>
</div>

<button class="calc-button" id="wr-calc-btn">Hisoblash</button>

<div id="wr-result" class="calc-result"></div>

</div>


---

## 📋 «WR va minimal RR» etalon jadvali

| Win Rate | Nol uchun minimal RR | Savdoga 1% uchun RR (xavf 1%) | Yangi boshlovchi uchun real? |
|---|---|---|---|
| 30% | 2.33 | 3.5+ | ❌ Qiyin |
| 40% | 1.50 | 2.5 | ⚠️ Real |
| **50%** | **1.00** | **2.0** | ✅ Real |
| 60% | 0.67 | 1.5 | ✅ Real |
| 70% | 0.43 | 1.0 | ✅ Juda real |
| 80% | 0.25 | 0.75 | ⚠️ Shubhali yuqori |
| 90% | 0.11 | 0.5 | ❌ Ko'pincha aldov |

!!! warning "75% dan yuqori Win Rate — qizil bayroq"
    Agar kimdir 85-90% Win Rate va'da qilsa — bu **matematikada mumkin**, ammo **faqat juda kichik TP va ulkan SL bilan** (RR < 0.5). Uzoq muddatda bunday strategiya **baribir** zararli, chunki 1 ta katta stop 5-10 ta kichik foydani yutib yuboradi.

    **Foydali strategiya uchun haqiqiy adolatli Win Rate: 45-65%** RR ≥ 1.5 da.

---

## 💡 Bu amalda nima anglatadi

### 1-misol: Yangi boshlagan «ko'p to'g'ri» deb o'ylaydi

```
WR = 70% (uning his-tuyg'usi bo'yicha)
RR = 0.5 (u foydani erta yopadi, zararni uzoq ushlab turadi)

Xavf 1% da 100 savdo:
- 70 g'alaba × 0.5% = +35%
- 30 yutqizuv × 1% = -30%
- Jami: +5% 100 savdoda

⚠️ Foyda bor, lekin mikroskopik. Bir bor qoidani buzish → minus.
```

### 2-misol: Intizomli

```
WR = 45% (u ko'pincha stop oladi)
RR = 2.0 (lekin u katta TP gacha sabr qiladi)

Xavf 1% da 100 savdo:
- 45 g'alaba × 2% = +90%
- 55 yutqizuv × 1% = -55%
- Jami: +35% 100 savdoda

✅ Past Win Rate bilan ham strategiya plyusda.
```

### 3-misol: Ochko'z

```
WR = 50%
RR = 0.8 (foydani erta oladi, yaxshi narx kutadi)

Xavf 1% da 100 savdo:
- 50 g'alaba × 0.8% = +40%
- 50 yutqizuv × 1% = -50%
- Jami: -10% 100 savdoda

❌ Strategiya minusda. Ochko'zlik o'ldiradi.
```

---

## 🎯 Asosiy xulosalar

1. **Win Rate asosiy emas** — asosiy WR + RR juftligi
2. **RR 1:2 yoki yuqori** — yangi boshlovchi uchun oltin standart
3. **TP ni hech qachon yaqinlashtirmang** «narx sekinlashdi deb»
4. **SL ni hech qachon uzoqlashtirmang** «bir oz yetmaydi deb»
5. **EV ni hisoblang** boshidan, «u yoqda ko'rarsan» emas

---

## 💬 Amaliyotchi sitatasi

!!! quote
    *«Nega daromadga chiqmayapman degan savolga javob bo'ladigan — oddiy, lekin barcha bilishi zarur bo'lgan balans jadvali. Daromadga chiqish uchun ushbu jadval orqali siz Win rate ga qarab Risk rewardni qancha ushlashingiz kerakligi ko'rsatilgan.»*

    **Tarjima:** «"Nega minsudaman?" degan savolga javob — oddiy, lekin hamma bilishi shart bo'lgan jadval. Win Rate ga qarab Risk-Reward ni qancha ushlab turish kerakligini ko'rsatadi.»

---

## 🔗 Keyingi o'qish uchun

- [LOT-intizomi](../practice/lot-discipline.md) — usiz WR ham, RR ham yordam bermaydi
- [Seyf (Move to BE)](../practice/breakeven-protocol.md) — erishilgan RR ni himoya qilish
- [Pozitsiya kalkulyatori](position-calculator.md) — to'g'ri lotni hisoblang
- [Trejding psixologiyasi](../extras/psychology.md) — nega RR ni kamaytirmoqchi bo'ladi
- [O'quv strategiyasi](../docs/strategy-details.md) — EMA50 Pullback va belgilangan RR=2
