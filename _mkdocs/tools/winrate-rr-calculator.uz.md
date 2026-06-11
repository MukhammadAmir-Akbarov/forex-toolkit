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

<button class="calc-button" onclick="calcWRRR()">Hisoblash</button>

<div id="wr-result" class="calc-result"></div>

</div>

<script>
function calcWRRR() {
  const wr = parseFloat(document.getElementById('wr-input').value) / 100;
  const rr = parseFloat(document.getElementById('rr-input').value);
  const trades = parseInt(document.getElementById('trades-input').value);
  const risk = parseFloat(document.getElementById('risk-input').value);

  if (!wr || !rr || !trades || !risk) {
    document.getElementById('wr-result').innerHTML = '<div class="calc-warn">Barcha maydonlarni to\'ldiring</div>';
    return;
  }

  const wins = Math.round(trades * wr);
  const losses = trades - wins;
  const winPnL = wins * rr * risk;
  const lossPnL = losses * risk;
  const netPnL = winPnL - lossPnL;

  // Expected value per trade
  const ev = (wr * rr - (1 - wr)) * risk;
  const evSign = ev >= 0 ? '+' : '';

  // Required RR for breakeven at this WR
  const requiredRR = (1 - wr) / wr;

  // Status
  let status, statusClass;
  if (ev > 0.5) {
    status = '✅ Kuchli strategiya — barqaror plyus';
    statusClass = 'calc-ok';
  } else if (ev > 0.1) {
    status = '🟡 Strategiya plyusda, lekin plyus kuchsiz';
    statusClass = 'calc-warn';
  } else if (ev > -0.1) {
    status = '🟠 Strategiya chegarada — nolga yaqin';
    statusClass = 'calc-warn';
  } else {
    status = '🔴 Strategiya matematika bo\'yicha ZARARLI';
    statusClass = 'calc-error';
  }

  const html = `
    <div class="${statusClass}">
      <h4>${status}</h4>

      <table class="calc-table">
        <tr><td><strong>Foydali savdolar</strong></td><td>${wins} (${(wr*100).toFixed(0)}%)</td></tr>
        <tr><td><strong>Zararli savdolar</strong></td><td>${losses} (${((1-wr)*100).toFixed(0)}%)</td></tr>
        <tr><td><strong>G'alabalardan foyda</strong></td><td>+${winPnL.toFixed(2)}% depozit</td></tr>
        <tr><td><strong>Mag'lubiyatlardan zarar</strong></td><td>-${lossPnL.toFixed(2)}% depozit</td></tr>
        <tr><td><strong>${trades} savdo uchun jami</strong></td><td><strong>${netPnL >= 0 ? '+' : ''}${netPnL.toFixed(2)}% depozit</strong></td></tr>
        <tr><td><strong>EV (1 savdoga)</strong></td><td>${evSign}${ev.toFixed(3)}% depozit</td></tr>
        <tr><td><strong>Zarar ko'rmaslik uchun minimal RR</strong></td><td>${requiredRR.toFixed(2)}</td></tr>
      </table>

      <p><strong>Izoh:</strong></p>
      <ul>
        <li>EV (Expected Value) = bir savdoning matematik kutilmasi</li>
        <li>Agar EV > 0 — strategiya uzoq muddatda foydali</li>
        <li>Agar EV < 0 — million savdo ham yordam bermaydi</li>
        <li>Sizning WR <strong>${(wr*100).toFixed(0)}%</strong> bo'lganda nol uchun minimal RR = <strong>${requiredRR.toFixed(2)}</strong>. Siz RR=<strong>${rr.toFixed(1)}</strong> ishlatyapsiz, bu talab qilinganidan ${rr > requiredRR ? '✅ YUQORI' : '❌ PAST'}.</li>
      </ul>
    </div>
  `;

  document.getElementById('wr-result').innerHTML = html;
}

window.addEventListener('DOMContentLoaded', calcWRRR);
</script>

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
