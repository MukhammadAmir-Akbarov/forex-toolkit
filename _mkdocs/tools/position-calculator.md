# 📐 Калькулятор размера позиции

!!! abstract "Зачем это нужно"
    Размер позиции — главное, что определяет, **выживешь ли ты на рынке**. Если рискуешь 0.5% депозита на сделку, ты можешь проиграть 10 раз подряд и потерять только 5%. Если рискуешь 5%, та же серия 10 убытков **обнулит счёт**.

    Этот калькулятор гарантирует, что ты ставишь **именно то**, что запланировал — никаких импровизаций и эмоций.

## Формула

```
Размер риска ($)  =  Депозит × Риск% / 100
Лотов            =  Размер риска / (Стоп в пипсах × Стоимость пипса)
Округление       ←  вниз до 0.01 (минимум брокера) — реальный риск никогда
                     не больше планового
```

---

<div class="pos-calc-widget" id="pos-calc">

<style>
.pos-calc-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}
.pos-calc-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.2rem;
}
@media (max-width: 600px) {
  .pos-calc-form { grid-template-columns: 1fr; }
}
.pos-calc-form label {
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--md-default-fg-color);
}
.pos-calc-form input[type=number],
.pos-calc-form select {
  margin-top: 0.3rem;
  padding: 0.55rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.pos-calc-form input:focus,
.pos-calc-form select:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.pos-calc-form .pc-row-wide { grid-column: 1 / -1; }
.pos-calc-form .pc-checkbox {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  cursor: pointer;
}
.pos-calc-form .pc-checkbox input { margin: 0; }
#pc-result {
  margin-top: 1.5rem;
  padding: 1.2rem;
  background: var(--md-default-bg-color);
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
}
#pc-result.warn { border-left-color: #f59e0b; }
#pc-result.danger { border-left-color: #dc2626; }
.pc-result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 1.5rem;
  margin-bottom: 0.7rem;
}
@media (max-width: 600px) {
  .pc-result-grid { grid-template-columns: 1fr; }
}
.pc-result-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.92rem;
  padding: 0.2rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}
.pc-result-row span:first-child { color: var(--md-default-fg-color--light); }
.pc-result-row span:last-child { font-weight: 600; font-family: var(--md-code-font-family); }
.pc-headline {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  text-align: center;
  margin: 0.5rem 0 1rem;
  font-family: var(--md-code-font-family);
}
#pc-result.warn .pc-headline { color: #d97706; }
#pc-result.danger .pc-headline { color: #dc2626; }
.pc-warnings {
  margin-top: 0.8rem;
  font-size: 0.88rem;
}
.pc-warnings .pc-warn {
  padding: 0.5rem 0.75rem;
  margin-top: 0.4rem;
  border-radius: 6px;
  background: rgba(245, 158, 11, 0.1);
  border-left: 3px solid #f59e0b;
}
.pc-warnings .pc-danger {
  background: rgba(220, 38, 38, 0.1);
  border-left-color: #dc2626;
}
.pc-warnings .pc-info {
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3b82f6;
}
.pos-calc-form button {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.pos-calc-form button:hover { filter: brightness(1.1); }
.pc-meta { font-size: 0.78rem; color: var(--md-default-fg-color--light); margin-top: 0.4rem; }
</style>

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Депозит (USD)
    <input type="number" id="pc-balance" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Риск на сделку (%)
    <input type="number" id="pc-risk" value="0.5" min="0.01" max="10" step="any" autocomplete="off">
    <span class="pc-meta">Новичку рекомендуется 0.5%, опытному — до 2%.</span>
  </label>
  <label>
    Стоп-лосс (пипсов)
    <input type="number" id="pc-stop" value="25" min="1" step="any" autocomplete="off">
    <span class="pc-meta">Расстояние от входа до стопа в пипсах.</span>
  </label>
  <label>
    Валютная пара
    <select id="pc-pair">
      <option value="EURUSD">EUR / USD</option>
      <option value="GBPUSD">GBP / USD</option>
      <option value="AUDUSD">AUD / USD</option>
      <option value="NZDUSD">NZD / USD</option>
      <option value="USDJPY">USD / JPY</option>
      <option value="USDCHF">USD / CHF</option>
      <option value="USDCAD">USD / CAD</option>
      <option value="EURJPY">EUR / JPY</option>
      <option value="GBPJPY">GBP / JPY</option>
      <option value="EURGBP">EUR / GBP</option>
    </select>
  </label>
  <label class="pc-checkbox pc-row-wide">
    <input type="checkbox" id="pc-live">
    <span>Подтянуть актуальный курс (Frankfurter / ECB) — точнее для USDJPY, USDCHF, USDCAD, кросс-пар</span>
  </label>
  <button type="button" id="pc-calc-btn" class="pc-row-wide">Рассчитать</button>
</form>

<div id="pc-result" style="display: none;">
  <div class="pc-headline" id="pc-headline">— лот</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Депозит</span><span id="pc-out-balance">—</span></div>
    <div class="pc-result-row"><span>План риска</span><span id="pc-out-risk-plan">—</span></div>
    <div class="pc-result-row"><span>Стоп-лосс</span><span id="pc-out-stop">—</span></div>
    <div class="pc-result-row"><span>Пара</span><span id="pc-out-pair">—</span></div>
    <div class="pc-result-row"><span>Стоимость пипса</span><span id="pc-out-pip">—</span></div>
    <div class="pc-result-row"><span>Размер (точный)</span><span id="pc-out-lots-exact">—</span></div>
    <div class="pc-result-row"><span>Размер (округлён)</span><span id="pc-out-lots-rounded">—</span></div>
    <div class="pc-result-row"><span>Реальный риск</span><span id="pc-out-actual">—</span></div>
  </div>
  <div class="pc-warnings" id="pc-warnings"></div>
</div>

<script>
(function() {
  // Статичные значения стоимости пипса для $1 USD-аккаунта, 1 стандартный лот.
  // Для USD-quote пар (EURUSD...) это константа $10. Для пар, где USD — base,
  // и кросс-пар — зависит от курса (см. live-режим).
  const PIP_VALUES_STATIC = {
    EURUSD: 10.00, GBPUSD: 10.00, AUDUSD: 10.00, NZDUSD: 10.00,
    USDJPY: 6.70, USDCHF: 11.30, USDCAD: 7.30,
    EURJPY: 6.70, GBPJPY: 6.70, EURGBP: 12.70,
  };

  // Пары, у которых стоимость пипса критично зависит от курса
  const LIVE_SENSITIVE = new Set([
    'USDJPY', 'USDCHF', 'USDCAD', 'EURJPY', 'GBPJPY', 'EURGBP',
  ]);

  // Получить курс через Frankfurter API (ECB rates, free, no API key)
  // Возвращает Promise<number> — курс 1 USD в quote-валюте, или null
  async function fetchRate(pair) {
    const base = pair.slice(0, 3);
    const quote = pair.slice(3, 6);
    try {
      const r = await fetch(`https://api.frankfurter.app/latest?from=${base}&to=${quote}`);
      if (!r.ok) return null;
      const d = await r.json();
      return d.rates && d.rates[quote] ? d.rates[quote] : null;
    } catch (e) {
      return null;
    }
  }

  // Расчёт live pip value для конкретной пары
  // Возвращает Promise<{value: number, source: string}>
  async function livePipValue(pair) {
    const base = pair.slice(0, 3);
    const quote = pair.slice(3, 6);
    const pipSize = quote === 'JPY' ? 0.01 : 0.0001;
    const lot = 100000;

    if (quote === 'USD') {
      return { value: pipSize * lot, source: 'константа' };
    }

    if (base === 'USD') {
      const rate = await fetchRate(pair);
      if (!rate) return null;
      return { value: pipSize * lot / rate, source: `ECB: 1 USD = ${rate.toFixed(4)} ${quote}` };
    }

    // Кросс: pip value в quote → конвертим в USD через quote/USD
    const pipValueQuote = pipSize * lot;
    const quoteToUsd = await fetchRate(`${quote}USD`);
    if (!quoteToUsd) {
      const usdToQuote = await fetchRate(`USD${quote}`);
      if (!usdToQuote) return null;
      return { value: pipValueQuote / usdToQuote, source: `ECB: USD/${quote} = ${usdToQuote.toFixed(4)}` };
    }
    return { value: pipValueQuote * quoteToUsd, source: `ECB: ${quote}/USD = ${quoteToUsd.toFixed(4)}` };
  }

  // Основной расчёт
  function compute(balance, riskPct, stopPips, pipValue) {
    const riskAmount = balance * riskPct / 100;
    const lots = riskAmount / (stopPips * pipValue);
    let lotsRounded = Math.floor(lots * 100 + 1e-9) / 100;
    if (lotsRounded < 0.01) lotsRounded = 0.01;
    const actualRisk = lotsRounded * stopPips * pipValue;
    const actualRiskPct = actualRisk / balance * 100;
    return { riskAmount, lots, lotsRounded, actualRisk, actualRiskPct };
  }

  const fmt$ = v => '$' + v.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const fmtPct = v => v.toFixed(2) + '%';
  const fmtLots = v => v.toFixed(4);
  const fmtLotsR = v => v.toFixed(2);

  async function recalc() {
    const balance = parseFloat(document.getElementById('pc-balance').value);
    const riskPct = parseFloat(document.getElementById('pc-risk').value);
    const stopPips = parseFloat(document.getElementById('pc-stop').value);
    const pair = document.getElementById('pc-pair').value;
    const live = document.getElementById('pc-live').checked;

    const result = document.getElementById('pc-result');
    const warnings = document.getElementById('pc-warnings');
    warnings.innerHTML = '';

    // Валидация
    const errors = [];
    if (!(balance > 0)) errors.push('Депозит должен быть больше 0.');
    if (!(riskPct > 0 && riskPct <= 10)) errors.push('Риск должен быть в диапазоне 0 < x ≤ 10%.');
    if (!(stopPips > 0)) errors.push('Стоп-лосс должен быть больше 0 пипсов.');
    if (errors.length) {
      result.style.display = 'block';
      result.className = 'danger';
      document.getElementById('pc-headline').textContent = '—';
      warnings.innerHTML = errors.map(e => `<div class="pc-warn pc-danger">⛔ ${e}</div>`).join('');
      return;
    }

    // Pip value: static или live
    let pipValue = PIP_VALUES_STATIC[pair];
    let pipSource = 'таблица';
    if (live && LIVE_SENSITIVE.has(pair)) {
      document.getElementById('pc-headline').textContent = 'Загрузка курса…';
      result.style.display = 'block';
      const live_pv = await livePipValue(pair);
      if (live_pv && live_pv.value > 0) {
        pipValue = live_pv.value;
        pipSource = live_pv.source;
      } else {
        warnings.innerHTML += `<div class="pc-warn">⚠️ Не удалось получить актуальный курс — использую табличное значение.</div>`;
      }
    }

    const r = compute(balance, riskPct, stopPips, pipValue);

    // Заполняем результат
    document.getElementById('pc-out-balance').textContent = fmt$(balance);
    document.getElementById('pc-out-risk-plan').textContent = `${fmtPct(riskPct)} = ${fmt$(r.riskAmount)}`;
    document.getElementById('pc-out-stop').textContent = stopPips + ' пипсов';
    document.getElementById('pc-out-pair').textContent = pair;
    document.getElementById('pc-out-pip').textContent = fmt$(pipValue) + '/пипс (' + pipSource + ')';
    document.getElementById('pc-out-lots-exact').textContent = fmtLots(r.lots);
    document.getElementById('pc-out-lots-rounded').textContent = fmtLotsR(r.lotsRounded);
    document.getElementById('pc-out-actual').textContent = `${fmt$(r.actualRisk)} (${fmtPct(r.actualRiskPct)})`;
    document.getElementById('pc-headline').textContent = `${fmtLotsR(r.lotsRounded)} лот`;
    result.style.display = 'block';

    // Уровни предупреждений
    let cls = 'ok';
    if (r.actualRiskPct > 5) {
      cls = 'danger';
      warnings.innerHTML += `<div class="pc-warn pc-danger">⛔ Риск ${fmtPct(r.actualRiskPct)} депозита — это очень много. По статистике, такие риски приводят к обнулению счёта в течение месяца.</div>`;
    } else if (r.actualRiskPct > 2) {
      cls = 'warn';
      warnings.innerHTML += `<div class="pc-warn">⚠️ Риск ${fmtPct(r.actualRiskPct)} депозита — выше рекомендованного для новичка (≤ 2%). Подумай о меньшем риске или большем стопе.</div>`;
    }
    if (r.actualRisk > r.riskAmount * 1.05) {
      cls = cls === 'ok' ? 'warn' : cls;
      warnings.innerHTML += `<div class="pc-warn">⚠️ После округления реальный риск ${fmt$(r.actualRisk)} больше планового ${fmt$(r.riskAmount)} — уменьши лот вручную в терминале до 0.01.</div>`;
    }
    if (r.lotsRounded === 0.01 && r.lots < 0.005) {
      warnings.innerHTML += `<div class="pc-warn pc-info">ℹ️ Расчёт даёт меньше 0.01 лота — установлен минимум брокера. Для соблюдения риска уменьши стоп-лосс или увеличь депозит.</div>`;
    }
    result.className = cls === 'ok' ? '' : cls;
  }

  // Auto-recalc на изменение любого поля
  const inputs = ['pc-balance', 'pc-risk', 'pc-stop', 'pc-pair', 'pc-live'];
  inputs.forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener('input', recalc);
    el.addEventListener('change', recalc);
  });
  document.getElementById('pc-calc-btn').addEventListener('click', recalc);

  // Первый расчёт
  recalc();
})();
</script>

</div>

---

## Как пользоваться

1. **Депозит** — текущий баланс счёта в USD (или эквивалент твоей валюты счёта в USD).
2. **Риск на сделку** — какой процент депозита ты готов потерять на одной сделке. Новичку: **0.5%**.
3. **Стоп-лосс** — расстояние от точки входа до стоп-лосса в пипсах. Это берётся из твоего анализа графика (ниже последнего минимума для long, выше максимума для short).
4. **Пара** — что торгуешь.
5. **«Подтянуть актуальный курс»** — для USDJPY и других пар, где стоимость пипса зависит от курса. Тянет рейты ECB через бесплатный API без регистрации.

В результат пиши **только округлённое значение лотов** в терминал брокера — это то, что реально можно открыть.

---

## Пример расчёта

| Параметр | Значение |
|---|---|
| Депозит | $1 000 |
| Риск | 0.5% = $5.00 |
| Стоп-лосс | 25 пипсов |
| Пара | EUR/USD (стоимость пипса = $10) |
| **Размер позиции** | **0.02 лота** (1/50 стандартного) |

При проигрыше: 25 пипсов × $10/пипс × 0.02 лот = **$5** = 0.5% депозита. Всё точно.

---

## Best practices

!!! warning "Без стопа не считай"
    Если ты не знаешь, **где** твой стоп, ты не можешь посчитать размер позиции. Это значит: ты не понимаешь свою сделку. Не открывай.

!!! danger "Не «увеличивай позицию, чтобы отыграться»"
    Это **тильт**. После убытка размер позиции **остаётся** тем же или **уменьшается**. Никогда не увеличивается.

!!! tip "Меняй стоп, не лоты"
    Если хочешь больше потенциальной прибыли — двигай не размер позиции, а **тейк-профит** или используй пирамидинг. Размер позиции — функция от риска, не от уверенности.

---

## Связь с Python-версией

Этот калькулятор — точная JS-копия [`tools/position_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/position_calculator.py) из репозитория. Та же формула, те же значения, те же предупреждения. Из терминала:

```bash
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD
# или с актуальным курсом:
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair USDJPY --live
```

Используй любой удобный вариант. Калькулятор на сайте полностью offline-friendly (после первой загрузки) и не отправляет твои цифры никуда — расчёт в браузере.
