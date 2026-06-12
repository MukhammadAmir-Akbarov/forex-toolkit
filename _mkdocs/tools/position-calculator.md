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
