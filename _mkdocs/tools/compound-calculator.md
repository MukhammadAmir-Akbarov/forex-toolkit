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
