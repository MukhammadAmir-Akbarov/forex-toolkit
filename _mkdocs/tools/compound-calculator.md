# 📈 Калькулятор сложного процента

!!! abstract "Зачем нужно"
    **Сложный процент — главная сила в долгосрочном росте депозита.** Маленькие, **стабильные** проценты на длинной дистанции дают больше, чем разовые крупные выигрыши с просадками. Этот калькулятор показывает, чего реально ждать.

!!! danger "Реальность"
    **Не реклама гуру.** Стабильные 5% в месяц — это **исключительно** редко на forex. Большинство профи довольны 1-3% в месяц. Используй этот калькулятор как **проверку обещаний** «гуру» — если кто-то говорит «удвою депозит за год», посмотри, что это значит в месячных %.

## Формула

```
Финал = Начальный × (1 + r/100)^n

где r — % в месяц, n — число месяцев
```

---

<div class="pos-calc-widget" id="compound-calc">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Начальный депозит (USD)
    <input type="number" id="cc-initial" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Месячная доходность (%)
    <input type="number" id="cc-roi" value="3" min="-50" max="100" step="0.1" autocomplete="off">
    <span class="pc-meta">Реалистично: 1-3% для начинающего, 3-5% для опытного.</span>
  </label>
  <label>
    Срок (месяцев)
    <input type="number" id="cc-months" value="24" min="1" max="600" step="1" autocomplete="off">
    <span class="pc-meta">12 = 1 год, 60 = 5 лет.</span>
  </label>
  <label>
    Ежемесячное пополнение (USD)
    <input type="number" id="cc-deposit" value="0" min="0" step="any" autocomplete="off">
    <span class="pc-meta">Опционально: сколько докидываешь каждый месяц.</span>
  </label>
  <button type="button" id="cc-calc-btn" class="pc-row-wide">Рассчитать</button>
</form>

<div id="cc-result" class="pc-result" style="display: none;">
  <div class="pc-headline" id="cc-headline">—</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Стартовый капитал</span><span id="cc-out-initial">—</span></div>
    <div class="pc-result-row"><span>Доходность в месяц</span><span id="cc-out-roi">—</span></div>
    <div class="pc-result-row"><span>Срок</span><span id="cc-out-months">—</span></div>
    <div class="pc-result-row"><span>Пополнений всего</span><span id="cc-out-deposited">—</span></div>
    <div class="pc-result-row"><span>Прибыль</span><span id="cc-out-profit">—</span></div>
    <div class="pc-result-row"><span>Финальный депозит</span><span id="cc-out-final">—</span></div>
    <div class="pc-result-row"><span>Эквивалент годовой</span><span id="cc-out-annual">—</span></div>
    <div class="pc-result-row"><span>ROI на стартовый капитал</span><span id="cc-out-roi-total">—</span></div>
  </div>

  <h4>Контрольные точки</h4>
  <table class="pc-compound-table" id="cc-table">
    <thead><tr><th>Месяц</th><th>Депозит</th><th>+ за месяц</th><th>Прибыль с начала</th></tr></thead>
    <tbody id="cc-tbody"></tbody>
  </table>

  <div class="pc-warnings" id="cc-warnings"></div>
</div>

<script>
(function() {
  function calc() {
    const initial = parseFloat(document.getElementById('cc-initial').value);
    const roiPct = parseFloat(document.getElementById('cc-roi').value);
    const months = parseInt(document.getElementById('cc-months').value);
    const monthlyDeposit = parseFloat(document.getElementById('cc-deposit').value) || 0;
    const result = document.getElementById('cc-result');
    const warnings = document.getElementById('cc-warnings');
    warnings.innerHTML = '';

    const errors = [];
    if (!(initial > 0)) errors.push('Стартовый капитал должен быть больше 0.');
    if (isNaN(roiPct)) errors.push('Доходность — число.');
    if (!(months > 0)) errors.push('Срок должен быть больше 0 месяцев.');
    if (errors.length) {
      result.style.display = 'block';
      result.className = 'pc-result danger';
      document.getElementById('cc-headline').textContent = '—';
      warnings.innerHTML = errors.map(e => `<div class="pc-warn pc-danger">⛔ ${e}</div>`).join('');
      return;
    }

    const r = roiPct / 100;
    let balance = initial;
    let totalDeposited = initial;
    const series = [{ month: 0, balance, gain: 0, profit: 0 }];

    for (let m = 1; m <= months; m++) {
      const gain = balance * r;
      balance = balance * (1 + r) + monthlyDeposit;
      if (m > 1) totalDeposited += monthlyDeposit;
      const profit = balance - totalDeposited;
      series.push({ month: m, balance, gain, profit });
    }

    const finalBalance = series[series.length - 1].balance;
    const profit = finalBalance - totalDeposited;
    const annualEquivalent = (Math.pow(1 + r, 12) - 1) * 100;
    const totalRoi = (finalBalance - initial) / initial * 100;

    const fmt$ = v => '$' + v.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const fmtPct = v => v.toFixed(2) + '%';

    document.getElementById('cc-out-initial').textContent = fmt$(initial);
    document.getElementById('cc-out-roi').textContent = fmtPct(roiPct);
    document.getElementById('cc-out-months').textContent = months + ' мес. (' + (months / 12).toFixed(1) + ' лет)';
    document.getElementById('cc-out-deposited').textContent = fmt$(totalDeposited);
    document.getElementById('cc-out-profit').textContent = fmt$(profit);
    document.getElementById('cc-out-final').textContent = fmt$(finalBalance);
    document.getElementById('cc-out-annual').textContent = fmtPct(annualEquivalent);
    document.getElementById('cc-out-roi-total').textContent = fmtPct(totalRoi);
    document.getElementById('cc-headline').textContent = fmt$(finalBalance);
    result.style.display = 'block';
    result.className = 'pc-result';

    // Таблица контрольных точек
    const checkpoints = [1, 3, 6, 12, 24, 60, 120].filter(m => m <= months);
    if (!checkpoints.includes(months)) checkpoints.push(months);
    const tbody = document.getElementById('cc-tbody');
    tbody.innerHTML = checkpoints.map(m => {
      const s = series[m];
      return `<tr><td>${m} мес</td><td>${fmt$(s.balance)}</td><td>${fmt$(s.gain)}</td><td>${fmt$(s.profit)}</td></tr>`;
    }).join('');

    // Предупреждения
    if (roiPct > 10) {
      warnings.innerHTML += `<div class="pc-warn pc-danger">⛔ ${fmtPct(roiPct)} в месяц = ${fmtPct(annualEquivalent)} в год. Это **не реалистично**. Если кто-то это обещает — это скам.</div>`;
    } else if (roiPct > 5) {
      warnings.innerHTML += `<div class="pc-warn">⚠️ ${fmtPct(roiPct)}/мес — очень оптимистично. Лучшие хедж-фонды делают 20-30% в год = ~2%/мес. Проверь обещания.</div>`;
    } else if (roiPct < 0) {
      warnings.innerHTML += `<div class="pc-warn">📉 Отрицательная доходность — сценарий просадки. Через ${months} мес. потеряешь ${fmt$(initial - finalBalance)} от стартового.</div>`;
    }
    if (roiPct >= 1 && roiPct <= 5) {
      warnings.innerHTML += `<div class="pc-warn pc-info">ℹ️ ${fmtPct(roiPct)}/мес — реалистичный диапазон для опытных трейдеров. Большинство довольны 1-3%.</div>`;
    }
  }

  ['cc-initial', 'cc-roi', 'cc-months', 'cc-deposit'].forEach(id => {
    document.getElementById(id).addEventListener('input', calc);
  });
  document.getElementById('cc-calc-btn').addEventListener('click', calc);
  calc();
})();
</script>

</div>

---

## Калибровка ожиданий

| Месячная ROI | Годовая ROI | Реалистично? |
|---|---|---|
| 1% | 12.7% | ✅ Опытный трейдер, низкий риск |
| 2% | 26.8% | ✅ Возможно для опытного |
| 3% | 42.6% | ⚠️ Очень хорошо, требует таланта |
| 5% | 79.6% | 🟡 Топ-1% трейдеров |
| 10% | 213.8% | 🔴 Нереалистично долгосрочно |
| 20% | 791.6% | ⛔ Это скам |

## Связь с Python-версией

См. [`tools/compound_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/compound_calculator.py).
