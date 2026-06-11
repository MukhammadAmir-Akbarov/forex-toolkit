# 🎲 Barbodlik xavfi (Monte-Karlo)

!!! abstract "Nima uchun bu kerak"
    Daromadlilik kalkulyatori **o'rtacha kutishni** ko'rsatadi. Lekin o'rtacha — bu xayol: bir xil strategiyaga ega ikki treyderning 100 savdodagi natijalari faqat **g'alabalar va mag'lubiyatlar tartibi** tufayli butunlay farq qilishi mumkin.

    Monte-Karlo sizning strategiyangizni **2 000 marta** turli savdo tartiblari bilan ishlatib, **real natijalar diapazonini** ko'rsatadi: eng yaxshidan eng yomongacha. Bu xavfning halol manzarasi.

---

## 🧮 Monte-Karlo simulyatori

<style>
.mc-canvas-wrap {
  margin-top: 1.2rem;
  border-radius: 8px;
  overflow: hidden;
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
}
#mc-canvas {
  display: block;
  width: 100%;
  height: auto;
}
.mc-progress-bar-wrap {
  background: var(--md-default-fg-color--lightest);
  border-radius: 4px;
  height: 6px;
  margin: 0.6rem 0 0.2rem;
  overflow: hidden;
  display: none;
}
.mc-progress-bar {
  height: 100%;
  background: var(--md-primary-fg-color);
  width: 0%;
  transition: width 0.1s linear;
}
.mc-running-msg {
  font-size: 0.82rem;
  color: var(--md-default-fg-color--light);
  display: none;
  margin-bottom: 0.4rem;
}
.mc-verdict {
  margin-top: 1rem;
  padding: 1rem 1.2rem;
  border-radius: 8px;
  border-left: 4px solid #dc2626;
  background: rgba(220,38,38,0.07);
  font-size: 0.95rem;
  line-height: 1.6;
}
.mc-verdict.ok   { border-left-color: #22c55e; background: rgba(34,197,94,0.07); }
.mc-verdict.warn { border-left-color: #f59e0b; background: rgba(245,158,11,0.07); }
.mc-verdict.bad  { border-left-color: #dc2626; background: rgba(220,38,38,0.07); }
.mc-verdict strong { display: block; font-size: 1.05rem; margin-bottom: 0.4rem; }
</style>

<div class="calc-widget">

<div class="calc-row">
  <label>Win Rate (foydali savdolar %)</label>
  <input type="number" id="mc-wr" min="1" max="99" step="1" value="50">
  <span>%</span>
</div>

<div class="calc-row">
  <label>Risk-Reward Ratio (RR)</label>
  <input type="number" id="mc-rr" min="0.1" max="20" step="0.1" value="2.0">
  <span>mas. 2.0 = 1:2</span>
</div>

<div class="calc-row">
  <label>Savdo boshiga xavf (depozit %)</label>
  <input type="number" id="mc-risk" min="0.1" max="20" step="0.1" value="1.0">
  <span>%</span>
</div>

<div class="calc-row">
  <label>Savdolar soni</label>
  <input type="number" id="mc-trades" min="20" max="500" step="10" value="100">
</div>

<button class="calc-button" onclick="runMC()">Simulyatsiya qilish</button>

<div class="mc-progress-bar-wrap" id="mc-pbwrap"><div class="mc-progress-bar" id="mc-pb"></div></div>
<div class="mc-running-msg" id="mc-msg">2 000 yo'l simulyatsiya qilinmoqda...</div>

<div id="mc-result" class="calc-result" style="display:none"></div>

<div class="mc-canvas-wrap" id="mc-canvas-wrap" style="display:none">
  <canvas id="mc-canvas"></canvas>
</div>

<div id="mc-verdict" class="mc-verdict" style="display:none"></div>

</div>

<script>
(function () {

  /* ─── Константы ─── */
  var N_SIM   = 2000;   // кол-во симуляций
  var N_FAN   = 50;     // кривых на canvas

  /* ─── Одна симуляция (точная копия monte_carlo.py: simulate_one) ─── */
  function simulateOne(nTrades, winRate, rr, risk) {
    var equity  = 1.0;
    var history = [equity];
    var peak    = equity;
    var maxDD   = 0.0;
    for (var i = 0; i < nTrades; i++) {
      if (Math.random() < winRate) {
        equity *= (1 + risk * rr);
      } else {
        equity *= (1 - risk);
      }
      history.push(equity);
      if (equity > peak) peak = equity;
      var dd = (peak - equity) / peak;
      if (dd > maxDD) maxDD = dd;
    }
    return { history: history, maxDD: maxDD };
  }

  /* ─── Перцентиль (линейная интерполяция) ─── */
  function percentile(sorted, p) {
    if (sorted.length === 0) return 0;
    var idx = p / 100 * (sorted.length - 1);
    var lo  = Math.floor(idx);
    var hi  = Math.ceil(idx);
    if (lo === hi) return sorted[lo];
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo);
  }

  /* ─── Медиана ─── */
  function median(sorted) { return percentile(sorted, 50); }

  /* ─── Рисуем equity-веер на canvas ─── */
  function drawFan(histories, nTrades) {
    var wrap   = document.getElementById('mc-canvas-wrap');
    var canvas = document.getElementById('mc-canvas');
    wrap.style.display = 'block';

    var W = wrap.clientWidth || 680;
    var H = Math.round(W * 0.42);
    canvas.width  = W;
    canvas.height = H;

    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, W, H);

    /* Определяем диапазон Y */
    var allVals = [];
    for (var i = 0; i < histories.length; i++) {
      var h = histories[i];
      for (var j = 0; j < h.length; j++) allVals.push(h[j]);
    }
    var yMin = Math.min.apply(null, allVals);
    var yMax = Math.max.apply(null, allVals);
    yMin = Math.max(0, yMin * 0.95);
    yMax = yMax * 1.05;

    var PAD = { top: 18, right: 18, bottom: 30, left: 46 };
    var plotW = W - PAD.left - PAD.right;
    var plotH = H - PAD.top  - PAD.bottom;

    function xPx(t) { return PAD.left + t / nTrades * plotW; }
    function yPx(v) { return PAD.top  + (1 - (v - yMin) / (yMax - yMin)) * plotH; }

    /* Сетка */
    ctx.strokeStyle = 'rgba(128,128,128,0.15)';
    ctx.lineWidth   = 1;
    for (var g = 0; g <= 4; g++) {
      var gy = PAD.top + g / 4 * plotH;
      ctx.beginPath(); ctx.moveTo(PAD.left, gy); ctx.lineTo(W - PAD.right, gy); ctx.stroke();
    }

    /* Линия y=1.0 (безубыток) */
    ctx.strokeStyle = 'rgba(220,38,38,0.55)';
    ctx.lineWidth   = 1.5;
    ctx.setLineDash([5, 4]);
    var y1 = yPx(1.0);
    ctx.beginPath(); ctx.moveTo(PAD.left, y1); ctx.lineTo(W - PAD.right, y1); ctx.stroke();
    ctx.setLineDash([]);

    /* Подпись безубытка */
    ctx.fillStyle   = 'rgba(220,38,38,0.75)';
    ctx.font        = '11px var(--md-text-font-family, sans-serif)';
    ctx.textAlign   = 'right';
    ctx.fillText('1.0x', PAD.left - 4, y1 + 4);

    /* Фановые кривые */
    ctx.lineWidth = 0.9;
    for (var s = 0; s < histories.length; s++) {
      var h2 = histories[s];
      var fe = h2[h2.length - 1];
      /* Цвет: зелёный если финал >1, красный иначе */
      if (fe >= 1.0) {
        ctx.strokeStyle = 'rgba(59,130,246,0.18)';
      } else {
        ctx.strokeStyle = 'rgba(239,68,68,0.25)';
      }
      ctx.beginPath();
      ctx.moveTo(xPx(0), yPx(h2[0]));
      for (var t = 1; t < h2.length; t++) {
        ctx.lineTo(xPx(t), yPx(h2[t]));
      }
      ctx.stroke();
    }

    /* Медианная кривая */
    var medianCurve = [];
    for (var t2 = 0; t2 <= nTrades; t2++) {
      var col = [];
      for (var si = 0; si < histories.length; si++) col.push(histories[si][t2]);
      col.sort(function(a,b){return a-b;});
      medianCurve.push(median(col));
    }
    ctx.strokeStyle = '#1e40af';
    ctx.lineWidth   = 2.5;
    ctx.beginPath();
    ctx.moveTo(xPx(0), yPx(medianCurve[0]));
    for (var t3 = 1; t3 <= nTrades; t3++) {
      ctx.lineTo(xPx(t3), yPx(medianCurve[t3]));
    }
    ctx.stroke();

    /* Подписи осей */
    ctx.fillStyle = 'rgba(128,128,128,0.8)';
    ctx.font      = '11px var(--md-text-font-family, sans-serif)';
    ctx.textAlign = 'center';
    ctx.fillText('Savdo raqami', PAD.left + plotW / 2, H - 4);
    ctx.textAlign = 'right';
    var steps = 4;
    for (var step = 0; step <= steps; step++) {
      var val = yMin + (yMax - yMin) * step / steps;
      ctx.fillText(val.toFixed(2) + 'x', PAD.left - 6, yPx(val) + 4);
    }

    /* Легенда */
    ctx.font = '11px var(--md-text-font-family, sans-serif)';
    ctx.textAlign = 'left';
    var lx = PAD.left + 8, ly = PAD.top + 14;
    ctx.strokeStyle = '#1e40af'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(lx + 22, ly); ctx.stroke();
    ctx.fillStyle = 'rgba(128,128,128,0.9)';
    ctx.fillText('Mediana', lx + 26, ly + 4);
  }

  /* ─── Основная функция ─── */
  window.runMC = function () {
    var wr    = parseFloat(document.getElementById('mc-wr').value)    / 100;
    var rr    = parseFloat(document.getElementById('mc-rr').value);
    var risk  = parseFloat(document.getElementById('mc-risk').value)  / 100;
    var nT    = parseInt(document.getElementById('mc-trades').value);

    var errEl = document.getElementById('mc-result');
    if (isNaN(wr) || isNaN(rr) || isNaN(risk) || isNaN(nT) ||
        wr <= 0 || wr >= 1 || rr <= 0 || risk <= 0 || nT < 20) {
      errEl.style.display = 'block';
      errEl.innerHTML = '<div class="calc-warn">Barcha maydonlarni to\'g\'ri to\'ldiring. Win Rate: 1–99%, RR > 0, Xavf > 0, Savdolar ≥ 20.</div>';
      document.getElementById('mc-verdict').style.display = 'none';
      document.getElementById('mc-canvas-wrap').style.display = 'none';
      return;
    }

    /* Прогресс */
    var pbWrap = document.getElementById('mc-pbwrap');
    var pb     = document.getElementById('mc-pb');
    var msg    = document.getElementById('mc-msg');
    pbWrap.style.display = 'block';
    msg.style.display    = 'block';
    pb.style.width       = '0%';

    /* Запускаем симуляцию асинхронно чтобы браузер успел перерисовать прогресс */
    setTimeout(function () {
      var finalEquities = [];
      var drawdowns     = [];
      var fanHistories  = [];      // N_FAN кривых для рисования
      var fanStep       = Math.floor(N_SIM / N_FAN);

      for (var s = 0; s < N_SIM; s++) {
        var res = simulateOne(nT, wr, rr, risk);
        finalEquities.push(res.history[res.history.length - 1]);
        drawdowns.push(res.maxDD);
        if (s % fanStep === 0) fanHistories.push(res.history);

        /* Обновляем прогресс каждые 200 симуляций */
        if (s % 200 === 0) pb.style.width = (s / N_SIM * 100).toFixed(0) + '%';
      }
      pb.style.width       = '100%';
      pbWrap.style.display = 'none';
      msg.style.display    = 'none';

      /* Сортируем для перцентилей */
      var feSort = finalEquities.slice().sort(function(a,b){return a-b;});
      var ddSort = drawdowns.slice().sort(function(a,b){return a-b;});

      var feMean  = finalEquities.reduce(function(a,b){return a+b;},0) / N_SIM;
      var feMed   = median(feSort);
      var feP5    = percentile(feSort, 5);
      var feP1    = percentile(feSort, 1);
      var feP95   = percentile(feSort, 95);
      var feP99   = percentile(feSort, 99);

      var ddMean  = drawdowns.reduce(function(a,b){return a+b;},0) / N_SIM;
      var ddMed   = median(ddSort);
      var ddP95   = percentile(ddSort, 95);
      var ddP99   = percentile(ddSort, 99);

      function pct(arr, fn) {
        var cnt = 0;
        for (var i = 0; i < arr.length; i++) if (fn(arr[i])) cnt++;
        return cnt / arr.length * 100;
      }

      var probLoss   = pct(finalEquities, function(v){return v < 1.0;});
      var probHalf   = pct(finalEquities, function(v){return v < 0.5;});
      var probPlus50 = pct(finalEquities, function(v){return v > 1.5;});
      var probDouble = pct(finalEquities, function(v){return v > 2.0;});

      var probDD10   = pct(drawdowns, function(v){return v >= 0.10;});
      var probDD20   = pct(drawdowns, function(v){return v >= 0.20;});
      var probDD30   = pct(drawdowns, function(v){return v >= 0.30;});
      var probDD50   = pct(drawdowns, function(v){return v >= 0.50;});

      /* Формат числа */
      function f2(v){ return v.toFixed(2); }
      function f1(v){ return v.toFixed(1); }
      function p1(v){ return v.toFixed(1) + '%'; }

      /* Цветовой класс финального результата */
      function resultClass(v) {
        if (v >= 1.5) return 'calc-ok';
        if (v >= 1.0) return 'calc-warn';
        return 'calc-error';
      }

      var html = '<div class="' + resultClass(feMed) + '">'
        + '<h4>Monte-Karlo: ' + N_SIM + ' simulyatsiya × ' + nT + ' savdo</h4>'
        + '<table class="calc-table">'
        + '<tr><td colspan="2"><strong>Yakuniy kapital (ko\'paytuvchi)</strong></td></tr>'
        + '<tr><td>O\'rtacha</td><td>' + f2(feMean) + 'x</td></tr>'
        + '<tr><td>Mediana</td><td>' + f2(feMed)  + 'x</td></tr>'
        + '<tr><td>Eng yomon 5%</td><td>' + f2(feP5)  + 'x</td></tr>'
        + '<tr><td>Eng yomon 1%</td><td>' + f2(feP1)  + 'x</td></tr>'
        + '<tr><td>Eng yaxshi 95%</td><td>' + f2(feP95) + 'x</td></tr>'
        + '<tr><td>Eng yaxshi 99%</td><td>' + f2(feP99) + 'x</td></tr>'
        + '<tr><td colspan="2" style="padding-top:0.7rem"><strong>Maksimal tushish (drawdown)</strong></td></tr>'
        + '<tr><td>O\'rtacha</td><td>'            + p1(ddMean*100) + '</td></tr>'
        + '<tr><td>Mediana</td><td>'              + p1(ddMed*100)  + '</td></tr>'
        + '<tr><td>Eng yomon 5% holatda</td><td>' + p1(ddP95*100) + '</td></tr>'
        + '<tr><td>Eng yomon 1% holatda</td><td>' + p1(ddP99*100) + '</td></tr>'
        + '<tr><td colspan="2" style="padding-top:0.7rem"><strong>Tushish ehtimoli</strong></td></tr>'
        + '<tr><td>≥ 10%</td><td>' + p1(probDD10) + ' holat</td></tr>'
        + '<tr><td>≥ 20%</td><td>' + p1(probDD20) + ' holat</td></tr>'
        + '<tr><td>≥ 30%</td><td>' + p1(probDD30) + ' holat</td></tr>'
        + '<tr><td>≥ 50%</td><td>' + p1(probDD50) + ' holat</td></tr>'
        + '<tr><td colspan="2" style="padding-top:0.7rem"><strong>Yakuniy natija ehtimoli</strong></td></tr>'
        + '<tr><td>1.0x dan past tugash (zarar)</td><td>' + p1(probLoss)   + '</td></tr>'
        + '<tr><td>0.5x dan past tugash (−50%)</td><td>'  + p1(probHalf)   + '</td></tr>'
        + '<tr><td>1.5x dan yuqori tugash (+50%)</td><td>' + p1(probPlus50) + '</td></tr>'
        + '<tr><td>2.0x dan yuqori tugash (+100%)</td><td>' + p1(probDouble) + '</td></tr>'
        + '</table></div>';

      errEl.style.display = 'block';
      errEl.innerHTML     = html;

      /* Рисуем веер */
      drawFan(fanHistories, nT);

      /* ─── Вердикт ─── */
      var verdictEl = document.getElementById('mc-verdict');
      verdictEl.style.display = 'block';

      var riskPct = (risk * 100).toFixed(1);
      var verdictClass, verdictTitle, verdictBody;

      if (probLoss >= 50) {
        verdictClass = 'bad';
        verdictTitle = 'XAVFLI: strategiya daromaddan ko\'proq yo\'qotadi';
        verdictBody  = 'Savdo boshiga ' + riskPct + '% xavf va sizning parametrlaringiz bilan '
          + f1(probLoss) + '% treyderlar ' + nT + ' savdoda zarar bilan tugaydi. '
          + 'Bu omadsizlik emas — bu matematika. '
          + (probHalf > 10 ? 'Depozitning yarmini yo\'qotish ehtimoli: ' + f1(probHalf) + '%. ' : '')
          + 'Real pul bilan savdo qilishdan oldin muammoni hal qiling: '
          + 'RR ni oshiring, Win Rate ni ko\'taring yoki savdo boshiga xavfni kamaytiring.';
      } else if (probLoss >= 30) {
        verdictClass = 'warn';
        verdictTitle = 'OGOHLANTIRISH: har uchinchi senariy — zarar';
        verdictBody  = 'Strategiya rasman foydali (EV > 0), lekin ' + f1(probLoss)
          + '% simulyatsiyalar ' + nT + ' savdoda zarar bilan tugaydi. '
          + 'To\'g\'ri tizim bilan ham savdo boshiga ' + riskPct + '% xavf '
          + f1(probDD30) + '% holatlarda ≥30% tushishni beradi. '
          + 'Xavfni 0.5–1% gacha kamaytirish haqida o\'ylab ko\'ring — bu egri chiziqlarni ancha tekislaydi.';
      } else if (probLoss >= 10) {
        verdictClass = 'warn';
        verdictTitle = 'Strategiya ishlamoqda, lekin tushishlar bo\'ladi';
        verdictBody  = 'Ko\'pchilik senariylar foydali (faqat ' + f1(probLoss)
          + '% holatlarda zarar). Mediana: ' + f2(feMed) + 'x. '
          + 'Biroq vaqtinchalik tushishlarga tayyor bo\'ling: ≥20% tushish ' + f1(probDD20) + '% simulyatsiyalarda uchraydi. '
          + 'Ruhiy jihatdan bu og\'ir. Oldindan rejalashtiring va tushishda vahimaga tushmang.';
      } else {
        verdictClass = 'ok';
        verdictTitle = 'Yaxshi parametrlar — strategiya barqaror';
        verdictBody  = 'Faqat ' + f1(probLoss) + '% simulyatsiyalar zarar bilan tugadi. '
          + 'Kapital medianas: ' + f2(feMed) + 'x — ' + nT + ' savdoda. '
          + '≥30% tushish faqat ' + f1(probDD30) + '% holatlarda uchraydi. '
          + 'Intizomni saqlang: bu raqamlar faqat qoidalarni buzmagan taqdirdagina ishlaydi.';
      }

      verdictEl.className = 'mc-verdict ' + verdictClass;
      verdictEl.innerHTML = '<strong>' + verdictTitle + '</strong>' + verdictBody;

      /* Сохраняем последний запрос в localStorage */
      try {
        localStorage.setItem('ftk-mc-last', JSON.stringify({
          wr: wr, rr: rr, risk: risk, nT: nT,
          probLoss: probLoss, feMed: feMed,
          ts: Date.now()
        }));
      } catch(e) {}

    }, 30); /* конец setTimeout */
  }; /* конец runMC */

  /* Запускаем сразу при загрузке с дефолтными значениями */
  document.addEventListener('DOMContentLoaded', function () {
    window.runMC();
  });

})();
</script>

---

## 📖 Natijalarni qanday o'qish kerak

| Ko'rsatkich | Bu nimani anglatadi |
|---|---|
| **Kapital medianas** | Treyderlarning yarmi bu ko'rsatkichdan yuqori, yarmi — past natija oladi |
| **Eng yomon 5%** | Sizning strategiyangiz bilan har 20-chi treyder shu holatda bo'ladi |
| **1.0x dan past ehtimoli** | Strategiya N ta savdoda qancha tez-tez zarar beradi |
| **Tushish ≥ 20%** | Nechta senariylarda cho'qqidan -20% ko'rasiz |

!!! warning "Nima uchun mediana va o'rtacha farq qiladi"
    Kapitalning multiplikativ o'sishi (geometrik o'sish) tufayli **o'rtacha har doim oshirib ko'rsatiladi**. Misol: 90% holatlarda -10% yo'qotsangiz, 10% holatlarda +100% olsangiz, o'rtacha = +1%, lekin mediana = -10%. **Medianaga qarang** — bu oddiy treyderning haqiqiy tajribasi.

---

## 🧮 Matematika (monte_carlo.py ning aniq nusxasi)

Har bir simulyatsiya `equity = 1.0` dan boshlanadi va har bir savdoda:

```
agar random() < win_rate:
    equity = equity × (1 + risk × rr)   # g'alaba
aks holda:
    equity = equity × (1 - risk)          # mag'lubiyat
```

Maksimal tushish cho'qqidan hisoblanadi:
```
peak  = max(peak, equity)
dd    = (peak - equity) / peak
```

Bu `tools/monte_carlo.py` dagi `simulate_one()` funksiyasining aniq tarjimasi.

---

## 💡 Yangi boshlovchi uchun asosiy xulosalar

### 1. Savdo boshiga 2–5% xavf — «o'rtacha» emas

!!! danger "5% xavf — bu tajovuzkor"
    Savdo boshiga 5% xavf va Win Rate 50% / RR 2.0 bilan 100 ta savdoda **kutilgan median tushish** 25–35% dan oshadi. Ko'pchilik yangi boshlovchilar buni ko'tarolmay hisobni yopadi. Proflarning standarti — savdo boshiga 0.5–1%.

### 2. Savdolar tartibi muhim

!!! info "Yomon seriya yaxshisi kelishidan oldin halok qiladi"
    Musbat EV bilan ham, agar dastlabki 10–20 savdo yutqizish bo'lsa (bu muntazam sodir bo'ladi), tushish qo'rqitib to'xtatishi mumkin. Monte-Karlo bu tarqalish qanchalik keng ekanini ko'rsatadi.

### 3. Foydali strategiya ≠ barqaror o'sish

!!! example "Misol"
    WR = 55%, RR = 2.0, xavf = savdo boshiga 2%:

    - Matematik kutish: **+EV** (foydali strategiya)
    - Lekin ~20% simulyatsiyalar 100 ta savdoda zarar bilan tugaydi
    - Median tushish ≥ 20% ~60% holatlarda uchraydi

    Bu **normal** — lekin vahimaga tushmaslik uchun buni oldindan bilishingiz kerak.

---

## 🔗 Keyingi o'qish uchun

- [WinRate × RR kalkulyatori](winrate-rr-calculator.md) — matematik kutishni tushunish
- [LOT-intizomi](../practice/lot-discipline.md) — nima uchun lot hajmi muhim
- [Xavfsizlik (Move to BE)](../practice/breakeven-protocol.md) — tushishlarni kamaytirish
- [Treyding psixologiyasi](../extras/psychology.md) — tushishni yengish

---

!!! note "O'quv materiali"
    Ushbu simulyator faqat **o'quv maqsadida** va xavf matematikasini tushunish uchun mo'ljallangan. Bu moliyaviy maslahat emas va natija kafolati ham emas. Haqiqiy savdo har doim kiritilgan mablag'larning to'liq yo'qotilishi xavfini o'z ichiga oladi.
