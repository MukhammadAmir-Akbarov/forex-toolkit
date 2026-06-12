# 💰 Калькулятор маржи

!!! abstract "Зачем это нужно"
    Маржа — это **залог**, который брокер «замораживает» на твоём счёте, пока сделка открыта. Она не теряется, но она не работает: пока она «под позицией», ты не можешь использовать её для других сделок.

    Этот калькулятор показывает, **сколько денег заморозится** при открытии позиции и какую долю депозита это составляет — чтобы ты не открылся слишком крупно и не получил Margin Call.

## Формула

```
Маржа ($)          =  Лоты × Контракт × Цена / Плечо
Использование (%)  =  Маржа / Депозит × 100

Контракт = 100 000 (стандартный лот)
```

---

<div class="mc-widget" id="mc-widget">

<style>
.mc-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}
.mc-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.2rem;
}
@media (max-width: 600px) {
  .mc-form { grid-template-columns: 1fr; }
}
.mc-form label {
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--md-default-fg-color);
}
.mc-form input[type=number],
.mc-form select {
  margin-top: 0.3rem;
  padding: 0.55rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.mc-form input:focus,
.mc-form select:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.mc-form .mc-row-wide { grid-column: 1 / -1; }
.mc-form button {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.mc-form button:hover { filter: brightness(1.1); }
.mc-meta { font-size: 0.78rem; color: var(--md-default-fg-color--light); margin-top: 0.4rem; }
#mc-result {
  margin-top: 1.5rem;
  padding: 1.2rem;
  background: var(--md-default-bg-color);
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
}
#mc-result.warn { border-left-color: #f59e0b; }
#mc-result.danger { border-left-color: #dc2626; }
.mc-result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 1.5rem;
  margin-bottom: 0.7rem;
}
@media (max-width: 600px) {
  .mc-result-grid { grid-template-columns: 1fr; }
}
.mc-result-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.92rem;
  padding: 0.2rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}
.mc-result-row span:first-child { color: var(--md-default-fg-color--light); }
.mc-result-row span:last-child { font-weight: 600; font-family: var(--md-code-font-family); }
.mc-headline {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  text-align: center;
  margin: 0.5rem 0 1rem;
  font-family: var(--md-code-font-family);
}
#mc-result.warn .mc-headline { color: #d97706; }
#mc-result.danger .mc-headline { color: #dc2626; }
.mc-warnings {
  margin-top: 0.8rem;
  font-size: 0.88rem;
}
.mc-warnings .mc-warn {
  padding: 0.5rem 0.75rem;
  margin-top: 0.4rem;
  border-radius: 6px;
  background: rgba(245, 158, 11, 0.1);
  border-left: 3px solid #f59e0b;
}
.mc-warnings .mc-danger {
  background: rgba(220, 38, 38, 0.1);
  border-left-color: #dc2626;
}
.mc-warnings .mc-info {
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3b82f6;
}
</style>

<form class="mc-form" onsubmit="return false">
  <label>
    Депозит (USD)
    <input type="number" id="mc-deposit" value="1000" min="1" step="any" autocomplete="off">
  </label>
  <label>
    Лотов
    <input type="number" id="mc-lots" value="0.01" min="0.01" step="0.01" autocomplete="off">
    <span class="mc-meta">Минимум 0.01 (микролот). 1.0 = стандартный лот.</span>
  </label>
  <label>
    Текущая цена пары
    <input type="number" id="mc-price" value="1.0800" min="0.0001" step="any" autocomplete="off">
    <span class="mc-meta">Цена Ask из терминала брокера.</span>
  </label>
  <label>
    Плечо (1:X)
    <select id="mc-leverage">
      <option value="10">1:10</option>
      <option value="20">1:20</option>
      <option value="30" selected>1:30</option>
      <option value="50">1:50</option>
      <option value="100">1:100</option>
      <option value="200">1:200</option>
      <option value="500">1:500</option>
    </select>
  </label>
  <label>
    Валютная пара
    <select id="mc-pair">
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
    Тип позиции
    <select id="mc-type">
      <option value="standard">Стандартный лот (100 000)</option>
      <option value="mini">Мини-лот (10 000)</option>
      <option value="micro">Микро-лот (1 000)</option>
    </select>
    <span class="mc-meta">Большинство форекс-брокеров: стандартный.</span>
  </label>
  <button type="button" id="mc-calc-btn" class="mc-row-wide">Рассчитать</button>
</form>

<div id="mc-result" style="display: none;">
  <div class="mc-headline" id="mc-headline">— USD</div>
  <div class="mc-result-grid">
    <div class="mc-result-row"><span>Депозит</span><span id="mc-out-deposit">—</span></div>
    <div class="mc-result-row"><span>Лотов</span><span id="mc-out-lots">—</span></div>
    <div class="mc-result-row"><span>Цена пары</span><span id="mc-out-price">—</span></div>
    <div class="mc-result-row"><span>Плечо</span><span id="mc-out-leverage">—</span></div>
    <div class="mc-result-row"><span>Контракт</span><span id="mc-out-contract">—</span></div>
    <div class="mc-result-row"><span>Маржа</span><span id="mc-out-margin">—</span></div>
    <div class="mc-result-row"><span>Свободная маржа</span><span id="mc-out-free">—</span></div>
    <div class="mc-result-row"><span>Использование маржи</span><span id="mc-out-pct">—</span></div>
  </div>
  <div class="mc-warnings" id="mc-warnings"></div>
</div>


</div>

---

## Ключевые понятия

### Что такое маржа?

**Маржа** (Required Margin) — сумма, которую брокер «замораживает» как залог за открытую позицию. Она возвращается на счёт полностью после закрытия сделки. Маржа — это **не потеря**: ты не теряешь маржу, пока сделка не закрыта с убытком.

### Свободная маржа

**Свободная маржа** = Баланс − Использованная маржа

Это деньги, которые **доступны** тебе прямо сейчас: для открытия новых позиций или для покрытия плавающего убытка по уже открытым.

### Уровень маржи

**Уровень маржи** = (Equity / Использованная маржа) × 100%

Где Equity = Баланс + Плавающий P&L.

Брокеры обычно устанавливают:

- **Margin Call** — уровень ~100%: брокер предупреждает, что деньги кончаются.
- **Stop Out** — уровень ~50%: брокер **принудительно закрывает** позиции, начиная с наиболее убыточной.

### Margin Call и Stop Out

| Событие | Что происходит |
|---|---|
| Margin Call | Уровень маржи достиг порога (~100%). Брокер предупреждает. Новые позиции открыть нельзя. |
| Stop Out | Уровень маржи упал ниже критического (~50%). Брокер принудительно закрывает позиции без твоего согласия. |

Проверь конкретные уровни у своего брокера — они различаются.

---

## Пример расчёта

Допустим, у тебя:

- Депозит: **$1 000**
- Пара: **EUR/USD**, цена **1.0800**
- Объём: **0.01 лот** (микролот)
- Плечо: **1:30**

```
Маржа = 0.01 × 100 000 × 1.0800 / 30 = $36.00
Использование = 36.00 / 1000 × 100 = 3.60%
Свободная маржа = 1000 − 36 = $964.00
```

Браузерный калькулятор выше даст тот же результат: **$36.00** при стандартных значениях. Это соответствует выводу Python-инструмента:

```bash
.venv/bin/python tools/margin_calculator.py --lots 0.01 --price 1.08 --leverage 30 --deposit 1000
# → Маржа: $36.00
# → Использование маржи: 3.60%
```

---

## Как пользоваться

1. **Депозит** — текущий баланс в USD.
2. **Лотов** — объём позиции, которую планируешь открыть.
3. **Цена пары** — текущая цена Ask (берётся из терминала).
4. **Плечо** — плечо твоего счёта (уточни у брокера, например 1:30 в ЕС).
5. **Тип лота** — для большинства форекс-брокеров это «Стандартный лот (100 000)».

Смотри в первую очередь на **Использование маржи**:

- До 20% — комфортно, есть запас.
- 20–50% — высокая нагрузка, осторожно.
- Выше 50% — опасно, риск Stop Out велик.

---

## Связь с Python-версией

Это точная JS-копия [`tools/margin_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/margin_calculator.py). Одинаковая формула, одинаковые пороги. Из терминала:

```bash
.venv/bin/python tools/margin_calculator.py --lots 0.1 --price 1.08 --leverage 30 --deposit 1000
```

Расчёт происходит полностью в браузере — твои цифры никуда не отправляются.

---

!!! danger "Не финансовый совет"
    Этот калькулятор — образовательный инструмент. Реальные уровни Margin Call / Stop Out различаются у разных брокеров. Всегда уточняй условия своего брокера перед открытием позиций.
