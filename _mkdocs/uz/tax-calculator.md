# 🧾 Калькулятор налога (Узбекистан)

!!! abstract "Зачем это нужно"
    Доход от торговли у зарубежного брокера резидент Узбекистана **декларирует сам**.
    Этот калькулятор прикидывает, **сколько НДФЛ** придётся заплатить с годовой прибыли
    и сколько это в сумах — чтобы не было сюрпризов в апреле.

!!! danger "Это не налоговая консультация"
    Расчёт **упрощённый и образовательный**. Ставки и порядок декларирования меняются —
    проверяй актуальное на [soliq.uz](https://soliq.uz) и в личном кабинете
    [my.soliq.uz](https://my.soliq.uz), при больших суммах — у бухгалтера.
    Ставка НДФЛ 12% — на момент проверки 2026-06-11.

## Формула

```
Чистый результат ($) =  Годовая прибыль − Годовой убыток
Налог ($)            =  Чистый результат × 12%   (только если результат > 0)
В сумах              =  Сумма ($) × Курс USD→UZS
```

---

<div class="tax-widget" id="tax-widget">

<style>
.tax-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}
.tax-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.2rem;
}
@media (max-width: 600px) {
  .tax-form { grid-template-columns: 1fr; }
}
.tax-form label {
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--md-default-fg-color);
}
.tax-form input[type=number] {
  margin-top: 0.3rem;
  padding: 0.55rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.tax-form input:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.tax-form .tax-row-wide { grid-column: 1 / -1; }
.tax-form button {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.tax-form button:hover { filter: brightness(1.1); }
.tax-meta { font-size: 0.78rem; color: var(--md-default-fg-color--light); margin-top: 0.4rem; }
#tax-result {
  margin-top: 1.5rem;
  padding: 1.2rem;
  background: var(--md-default-bg-color);
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
}
#tax-result.ok { border-left-color: #22c55e; }
.tax-result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 1.5rem;
  margin-bottom: 0.7rem;
}
@media (max-width: 600px) {
  .tax-result-grid { grid-template-columns: 1fr; }
}
.tax-result-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.92rem;
  padding: 0.2rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}
.tax-result-row span:first-child { color: var(--md-default-fg-color--light); }
.tax-result-row span:last-child { font-weight: 600; font-family: var(--md-code-font-family); }
.tax-headline {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  text-align: center;
  margin: 0.5rem 0 0.2rem;
  font-family: var(--md-code-font-family);
}
.tax-subhead { text-align: center; font-size: 0.85rem; color: var(--md-default-fg-color--light); margin-bottom: 1rem; }
.tax-warnings { margin-top: 0.8rem; font-size: 0.88rem; }
.tax-warnings .tax-note {
  padding: 0.5rem 0.75rem;
  margin-top: 0.4rem;
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3b82f6;
}
.tax-warnings .tax-ok {
  background: rgba(34, 197, 94, 0.1);
  border-left: 3px solid #22c55e;
}
.tax-warnings .tax-danger {
  background: rgba(220, 38, 38, 0.1);
  border-left: 3px solid #dc2626;
}
</style>

<form class="tax-form" onsubmit="return false">
  <label>
    Годовая прибыль (USD)
    <input type="number" id="tax-profit" value="5000" min="0" step="any" autocomplete="off">
    <span class="tax-meta">Сумма всех прибыльных сделок за год.</span>
  </label>
  <label>
    Годовой убыток (USD)
    <input type="number" id="tax-loss" value="1000" min="0" step="any" autocomplete="off">
    <span class="tax-meta">Сумма всех убыточных сделок за год (как положительное число).</span>
  </label>
  <label>
    Курс USD → UZS
    <input type="number" id="tax-rate" value="12500" min="1000" max="99000" step="any" autocomplete="off">
    <span class="tax-meta">Проверь актуальный курс на <a href="https://cbu.uz" target="_blank" rel="noopener">cbu.uz</a>.</span>
  </label>
  <button type="button" id="tax-calc-btn" class="tax-row-wide">Рассчитать</button>
</form>

<div id="tax-result" style="display: none;">
  <div class="tax-headline" id="tax-headline">—</div>
  <div class="tax-subhead" id="tax-subhead">налог к уплате</div>
  <div class="tax-result-grid">
    <div class="tax-result-row"><span>Чистый результат</span><span id="tax-out-net">—</span></div>
    <div class="tax-result-row"><span>Чистый результат (сум)</span><span id="tax-out-net-uzs">—</span></div>
    <div class="tax-result-row"><span>Ставка НДФЛ</span><span id="tax-out-rate">12%</span></div>
    <div class="tax-result-row"><span>Налог к уплате</span><span id="tax-out-tax">—</span></div>
    <div class="tax-result-row"><span>Налог (сум)</span><span id="tax-out-tax-uzs">—</span></div>
    <div class="tax-result-row"><span>После налога</span><span id="tax-out-after">—</span></div>
    <div class="tax-result-row"><span>После налога (сум)</span><span id="tax-out-after-uzs">—</span></div>
  </div>
  <div class="tax-warnings" id="tax-warnings"></div>
</div>

<script>
(function() {
  // Математика идентична uz/tax-calculator.py:calculate_tax:
  //   net   = profit - loss
  //   tax   = net * 0.12  (только если net > 0, иначе 0)
  //   after = net - tax
  const NDFL_RATE = 0.12;  // 12% НДФЛ для физлиц-резидентов (проверять на soliq.uz)

  function calcTax(profit, loss, rate) {
    const net = profit - loss;
    if (net <= 0) {
      return { net, netUzs: net * rate, tax: 0, taxUzs: 0,
               after: net, afterUzs: net * rate, isLoss: true };
    }
    const tax = net * NDFL_RATE;
    return { net, netUzs: net * rate, tax, taxUzs: tax * rate,
             after: net - tax, afterUzs: (net - tax) * rate, isLoss: false };
  }

  const fmt$ = v => '$' + v.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const fmtUZS = v => Math.round(v).toLocaleString('ru-RU') + ' сум';

  function recalc() {
    const profit = parseFloat(document.getElementById('tax-profit').value);
    const loss   = parseFloat(document.getElementById('tax-loss').value);
    const rate   = parseFloat(document.getElementById('tax-rate').value);

    const result   = document.getElementById('tax-result');
    const warnings = document.getElementById('tax-warnings');
    warnings.innerHTML = '';

    const errors = [];
    if (!(profit >= 0)) errors.push('Прибыль не может быть отрицательной.');
    if (!(loss >= 0))   errors.push('Убыток укажи как положительное число.');
    if (!(rate > 0))    errors.push('Укажи курс USD → UZS.');
    if (errors.length) {
      result.style.display = 'block';
      result.className = '';
      document.getElementById('tax-headline').textContent = '—';
      warnings.innerHTML = errors.map(e => `<div class="tax-note tax-danger">⛔ ${e}</div>`).join('');
      return;
    }

    const r = calcTax(profit, loss, rate);

    document.getElementById('tax-out-net').textContent      = fmt$(r.net);
    document.getElementById('tax-out-net-uzs').textContent  = fmtUZS(r.netUzs);
    document.getElementById('tax-out-tax').textContent      = fmt$(r.tax);
    document.getElementById('tax-out-tax-uzs').textContent  = fmtUZS(r.taxUzs);
    document.getElementById('tax-out-after').textContent    = fmt$(r.after);
    document.getElementById('tax-out-after-uzs').textContent = fmtUZS(r.afterUzs);
    document.getElementById('tax-headline').textContent     = fmt$(r.tax);
    result.style.display = 'block';
    result.className = r.isLoss ? 'ok' : '';

    const nextYear = new Date().getFullYear() + 1;
    if (r.isLoss) {
      document.getElementById('tax-subhead').textContent = 'налога нет — убыток за год';
      warnings.innerHTML += `<div class="tax-note tax-ok">✅ За год убыток (${fmt$(r.net)}) — НДФЛ платить не нужно. Сохрани отчёт брокера минимум 3 года на случай вопросов.</div>`;
    } else {
      document.getElementById('tax-subhead').textContent = 'налог к уплате (НДФЛ 12%)';
      warnings.innerHTML += `<div class="tax-note">📌 Задекларируй чистую прибыль до <strong>1 апреля ${nextYear}</strong> года в личном кабинете my.soliq.uz.</div>`;
      warnings.innerHTML += `<div class="tax-note">💡 Декларируется итог за год (прибыли − убытки), а не каждая сделка отдельно.</div>`;
    }
    warnings.innerHTML += `<div class="tax-note">⚠️ Ставку и порядок уточни на soliq.uz — это образовательная оценка, не налоговая консультация.</div>`;
  }

  ['tax-profit','tax-loss','tax-rate'].forEach(function(id) {
    var el = document.getElementById(id);
    el.addEventListener('input', recalc);
    el.addEventListener('change', recalc);
  });
  document.getElementById('tax-calc-btn').addEventListener('click', recalc);

  recalc();
})();
</script>

</div>

---

## Что декларировать

- **Кто:** налоговый резидент Узбекистана (живёшь в стране 183+ дней в году).
- **Что:** чистый годовой доход от торговли у зарубежного брокера (прибыли − убытки за календарный год).
- **Сколько:** НДФЛ **12%** от чистой прибыли (на момент проверки 2026).
- **Когда:** декларация — **до 1 апреля** года, следующего за отчётным.
- **Где:** личный кабинет [my.soliq.uz](https://my.soliq.uz) или отделение налоговой.

## Что хранить (минимум 3 года)

- 📄 Годовой отчёт брокера (statement) о прибылях/убытках.
- 📄 Подтверждения ввода и вывода средств.
- 📄 Выписки с карты о зачислении сумов.

## Когда нужен бухгалтер

- Доход от трейдинга **> $5 000 / год**.
- Есть основная работа с «белой» зарплатой → нужна общая декларация.
- Не уверен в заполнении или получил **запрос от налоговой**.

## Пример

Прибыль за год **$5 000**, убыток **$1 000**, курс **12 500**:

- Чистый результат: **$4 000** (50 000 000 сум)
- НДФЛ 12%: **$480** (6 000 000 сум)
- После налога: **$3 520** (44 000 000 сум)

!!! warning "Образовательный материал, не финансовый и не налоговый совет"
    Точные ставки и правила — на [soliq.uz](https://soliq.uz). Исходник расчёта:
    [tax-calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/uz/tax-calculator.py).

---

[← Брокеры для УЗ](brokers-uz.md) · [Вывод денег →](withdrawal-guide.md)
