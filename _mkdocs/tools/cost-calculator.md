---
widgets: [cost]
---

# 💸 Калькулятор стоимости торговли

!!! abstract "Зачем это нужно"
    Каждая сделка стоит денег **ещё до того**, как рынок куда-то пойдёт: спред,
    комиссия брокера, своп за перенос позиции через ночь. По отдельности — копейки.
    На дистанции в сотни сделок — это **тихий убийца депозита**.

    Этот калькулятор показывает, сколько ты платишь за одну сделку, сколько пунктов
    нужно пройти **просто чтобы выйти в ноль**, и во что обходится овертрейдинг за месяц.

## Формула

```
Спред         =  Спред (пункты) × Стоимость пункта × Лоты
Комиссия      =  Комиссия за лот × Лоты × 2   (вход + выход)
Своп          =  Своп за лот/ночь × Лоты × Ночей
Итого/сделка  =  Спред + Комиссия + Своп

Безубыток (пункты) =  Итого / (Стоимость пункта × Лоты)
Издержки/месяц     =  Итого/сделка × Сделок в месяц
```

---

<div class="calc-widget" id="co-widget">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Депозит (USD)
    <input type="number" id="co-deposit" value="1000" min="1" step="any" autocomplete="off">
    <span class="pc-meta">Нужен, чтобы показать издержки в % от счёта.</span>
  </label>
  <label>
    Валютная пара
    <select id="co-pair">
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
  <label>
    Лотов
    <input type="number" id="co-lots" value="0.10" min="0.01" step="0.01" autocomplete="off">
    <span class="pc-meta">1.0 = стандартный лот (100 000).</span>
  </label>
  <label>
    Спред (пункты)
    <input type="number" id="co-spread" value="1.0" min="0" step="0.1" autocomplete="off">
    <span class="pc-meta">Разница Ask − Bid из терминала.</span>
  </label>
  <label>
    Комиссия за лот, одна сторона (USD)
    <input type="number" id="co-commission" value="0" min="0" step="0.5" autocomplete="off">
    <span class="pc-meta">ECN-счета: ~$3.5/лот за сторону. Market-счета: 0.</span>
  </label>
  <label>
    Сделок в месяц
    <input type="number" id="co-trades" value="40" min="1" step="1" autocomplete="off">
    <span class="pc-meta">Сколько сделок ты открываешь за месяц.</span>
  </label>
  <label>
    Ночей удержания
    <input type="number" id="co-nights" value="0" min="0" step="1" autocomplete="off">
    <span class="pc-meta">0 — внутри дня (свопа нет).</span>
  </label>
  <label>
    Своп за лот/ночь (USD)
    <input type="number" id="co-swap" value="-2" step="0.1" autocomplete="off">
    <span class="pc-meta">Отрицательный = платишь, положительный = получаешь.</span>
  </label>
  <button type="button" id="co-calc-btn" class="pc-row-wide">Рассчитать</button>
</form>

<div id="co-result" style="display: none;">
  <div class="pc-headline" id="co-headline">— USD</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Спред</span><span id="co-out-spread">—</span></div>
    <div class="pc-result-row"><span>Комиссия (вход+выход)</span><span id="co-out-commission">—</span></div>
    <div class="pc-result-row"><span>Своп (× ночей)</span><span id="co-out-swap">—</span></div>
    <div class="pc-result-row"><span>Итого за сделку</span><span id="co-out-total">—</span></div>
    <div class="pc-result-row"><span>Безубыток</span><span id="co-out-breakeven">—</span></div>
    <div class="pc-result-row"><span>Издержки за месяц</span><span id="co-out-monthly">—</span></div>
    <div class="pc-result-row"><span>Издержки за месяц (% депозита)</span><span id="co-out-monthly-pct">—</span></div>
    <div class="pc-result-row"><span>Издержки за год</span><span id="co-out-yearly">—</span></div>
  </div>
  <div class="pc-warnings" id="co-warnings"></div>
</div>

</div>

---

## Ключевые понятия

### Спред

**Спред** — разница между ценой покупки (Ask) и продажи (Bid). Это первая и самая
частая издержка: открыв сделку, ты сразу в минусе на величину спреда. Узкий спред по
EUR/USD — около 0.1–1.0 пункта; на экзотике и в новости он расширяется в разы.

### Комиссия

На **ECN/Raw**-счетах спред почти нулевой, но брокер берёт фиксированную комиссию —
обычно около **$3.5 за лот за сторону** (≈ $7 за круг). На **Market**-счетах комиссии
нет, но шире спред. Сравнивай по **полной** стоимости, а не по одному параметру.

### Своп (overnight)

**Своп** — плата за перенос позиции через ночь (по средам часто тройной — за выходные).
Зависит от разницы процентных ставок валют пары. Может быть как отрицательным (платишь
ты), так и положительным (платят тебе). Для внутридневной торговли своп = 0.

### Безубыток

**Безубыток** — сколько пунктов должна пройти цена в твою сторону, чтобы просто
**покрыть издержки**. Если безубыток 3 пункта, а твой тейк — 10, то 30% потенциала
съедают издержки ещё до учёта проигрышных сделок.

---

## Пример

Депозит **$1 000**, EUR/USD, **0.10 лота**, спред **1.0** пункт, комиссия **0**,
**40** сделок в месяц, внутри дня:

```
Стоимость пункта (0.10 лота) = $1.00
Спред     = 1.0 × $1.00 = $1.00
Комиссия  = 0
Своп      = 0
Итого     = $1.00 за сделку
Безубыток = $1.00 / $1.00 = 1.0 пункт
За месяц  = $1.00 × 40 = $40.00 = 4.0% депозита
За год    ≈ $480 ≈ 48% депозита
```

Сорок мелких сделок в месяц «съедают» почти половину депозита в год **только на
издержках** — даже если ты не потерял ни на одной сделке. Вот почему овертрейдинг опасен.

---

## Как пользоваться

1. Введи параметры своего счёта (спред и комиссию бери из спецификации брокера).
2. Смотри на **«Безубыток»** — если он близок к твоему среднему тейку, стратегия
   нежизнеспособна: издержки слишком велики.
3. Смотри на **«Издержки за год (% депозита)»** — это цена твоего стиля торговли.
   Хочешь снизить? Торгуй реже, крупнее по тейку, на узких спредах.

Расчёт идёт полностью в браузере — твои цифры никуда не отправляются.

---

!!! danger "Не финансовый совет"
    Образовательный инструмент. Реальные спреды, комиссии и свопы зависят от брокера,
    типа счёта и времени суток. Всегда сверяйся со спецификацией своего брокера.
