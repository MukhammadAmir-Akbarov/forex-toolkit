# 💲 Калькулятор стоимости пипса

!!! abstract "Зачем нужно"
    1 пипс — это **самая мелкая единица движения цены**. Сколько денег ты выигрываешь или теряешь на каждом пипсе — зависит от **размера позиции** и **пары**. Без понимания стоимости пипса невозможно правильно посчитать риск.

## Формула

```
Размер 1 лота         =  100 000 единиц base-валюты
Размер пипса          =  0.0001 для большинства пар, 0.01 для JPY-пар
Стоимость пипса (USD) =  размер_пипса × лот / курс (если USD — quote или base)
```

---

<div class="pos-calc-widget" id="pip-calc">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Валютная пара
    <select id="pp-pair">
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
      <option value="AUDJPY">AUD / JPY</option>
      <option value="CHFJPY">CHF / JPY</option>
      <option value="EURAUD">EUR / AUD</option>
      <option value="EURCHF">EUR / CHF</option>
    </select>
  </label>
  <label>
    Размер позиции (лот)
    <input type="number" id="pp-lots" value="0.10" min="0.01" step="0.01" autocomplete="off">
    <span class="pc-meta">0.01 = микро-лот, 0.1 = мини, 1.0 = стандартный.</span>
  </label>
  <label>
    Курс USD→UZS (сум, необязательно)
    <input type="number" id="pp-uzs" value="12600" min="0" step="any" autocomplete="off">
    <span class="pc-meta">Нужен только для дополнительного результата в сумах.</span>
  </label>
  <label class="pc-checkbox pc-row-wide">
    <input type="checkbox" id="pp-live" checked>
    <span>Использовать актуальный курс ECB (рекомендуется)</span>
  </label>
  <button type="button" id="pp-calc-btn" class="pc-row-wide">Рассчитать</button>
</form>

<div id="pp-result" class="pc-result" style="display: none;">
  <div class="pc-headline" id="pp-headline">— $ / пипс</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Пара</span><span id="pp-out-pair">—</span></div>
    <div class="pc-result-row"><span>Размер позиции</span><span id="pp-out-lots">—</span></div>
    <div class="pc-result-row"><span>Размер пипса</span><span id="pp-out-pipsize">—</span></div>
    <div class="pc-result-row"><span>Курс (для расчёта)</span><span id="pp-out-rate">—</span></div>
    <div class="pc-result-row"><span>Стоимость 1 пипса</span><span id="pp-out-pip">—</span></div>
    <div class="pc-result-row"><span>На 10 пипсах</span><span id="pp-out-10">—</span></div>
    <div class="pc-result-row" id="pp-out-uzs-row"><span>1 пипс в сумах</span><span id="pp-out-uzs">—</span></div>
    <div class="pc-result-row" id="pp-out-uzs-10-row"><span>10 пипсов в сумах</span><span id="pp-out-uzs-10">—</span></div>
  </div>
  <div class="pc-warnings" id="pp-warnings"></div>
</div>


</div>

---

## Примеры

| Пара | 1 пипс на 0.1 лот | 1 пипс на 1 лот (стандарт) |
|---|---|---|
| EUR/USD | $1.00 | $10.00 |
| GBP/USD | $1.00 | $10.00 |
| USD/JPY (курс ~150) | $0.67 | $6.67 |
| USD/CHF (курс ~0.88) | $1.14 | $11.36 |
| EUR/JPY (курс EUR/JPY ~162) | $0.67 | $6.67 |
| EUR/GBP (курс GBP/USD ~1.27) | $1.27 | $12.70 |

## Зачем это знать

- **Проверка калькулятора брокера** — на некоторых платформах указана неточная стоимость пипса
- **Сравнение пар** — почему один и тот же 25-пипсовый стоп на USDJPY стоит меньше, чем на EURUSD
- **Конверсия валют счёта** — если депозит не в USD, нужна доп. конверсия

## Связь с Python-версией

См. [`tools/pip_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/pip_calculator.py).
