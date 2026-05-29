# Гид по выводу денег от брокера в Узбекистан

> ⚠️ Информация общая, на момент составления (2026). Конкретные комиссии и сроки меняются — уточняй перед операцией.

---

## Калькулятор комиссии вывода

!!! info "Образовательный материал, не финансовый совет"
    Расчёт ориентировочный: комиссии могут меняться в любой момент. Всегда проверяй актуальные условия на сайте брокера и платёжной системы перед реальным переводом.

<style>
.wd-calc-select {
  flex: 1 1 200px;
  padding: 0.45rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.wd-calc-select:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.wd-best-row {
  margin-top: 0.9rem;
  padding: 0.65rem 0.9rem;
  border-radius: 6px;
  background: rgba(34, 197, 94, 0.1);
  border-left: 3px solid #22c55e;
  font-size: 0.92rem;
}
.wd-rate-hint {
  font-size: 0.78rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.25rem;
}
</style>

<div class="calc-widget">

<div class="calc-row">
  <label>Сумма вывода (USD)</label>
  <input type="number" id="wd-amount" min="1" max="100000" step="1" value="500">
  <span>USD</span>
</div>

<div class="calc-row">
  <label>Метод вывода</label>
  <select id="wd-method" class="wd-calc-select">
    <option value="usdt">💰 USDT TRC-20</option>
    <option value="visa">💳 Visa / Mastercard (USD)</option>
    <option value="swift">🏦 SWIFT в банк Узбекистана</option>
    <option value="wise">📲 Wise</option>
    <option value="skrill">💵 Skrill / Neteller</option>
  </select>
</div>

<div class="calc-row">
  <label>Курс USD → UZS</label>
  <input type="number" id="wd-rate" min="1000" max="99000" step="100" value="12600">
  <span>сум</span>
</div>
<div class="wd-rate-hint" style="margin-left:0; padding: 0 0 0.5rem 0;">
  Курс примерный — проверь сам на <a href="https://cbu.uz" target="_blank" rel="noopener">cbu.uz</a> или у своего банка
</div>

<button class="calc-button" onclick="calcWithdrawal()">Рассчитать</button>

<div id="wd-result" class="calc-result"></div>

</div>

<script>
(function() {
  var METHODS = {
    usdt: {
      label: 'USDT TRC-20',
      feeFixed: 4,
      feePct: 0,
      p2pSlippage: 0.02,
      speed: '5–30 мин',
      note: 'Комиссия брокера ~$3 + сеть TRC-20 ~$1. На P2P теряется ещё ~2% на курсе.'
    },
    visa: {
      label: 'Visa / Mastercard',
      feeFixed: 0,
      feePct: 0.02,
      p2pSlippage: 0,
      speed: '1–5 дней',
      note: 'Комиссия 1–3% от суммы. Взята середина 2%.'
    },
    swift: {
      label: 'SWIFT в банк Узбекистана',
      feeFixed: 52,
      feePct: 0,
      p2pSlippage: 0,
      speed: '3–7 рабочих дней',
      note: 'Фиксированная сумма: брокер $0–30 + банк-посредник $15–25 + твой банк $0–20. Взята середина $52.'
    },
    wise: {
      label: 'Wise',
      feeFixed: 3,
      feePct: 0.0075,
      p2pSlippage: 0,
      speed: '1–3 дня',
      note: 'Фиксированная ~$3 + 0.5–1% за конвертацию. Взята середина 0.75%.'
    },
    skrill: {
      label: 'Skrill / Neteller',
      feeFixed: 0,
      feePct: 0.025,
      p2pSlippage: 0,
      speed: '1–2 дня',
      note: 'Комиссия 2–3% от суммы. Взята середина 2.5%.'
    }
  };

  function calcFee(amount, methodKey) {
    var m = METHODS[methodKey];
    var fee = m.feeFixed + amount * m.feePct + amount * m.p2pSlippage;
    return fee;
  }

  function findCheapest(amount) {
    var best = null;
    var bestFee = Infinity;
    Object.keys(METHODS).forEach(function(key) {
      var fee = calcFee(amount, key);
      if (fee < bestFee) {
        bestFee = fee;
        best = key;
      }
    });
    return { key: best, fee: bestFee };
  }

  function fmt(n) {
    return n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  function fmtUZS(n) {
    return Math.round(n).toLocaleString('ru-RU');
  }

  window.calcWithdrawal = function() {
    var amount = parseFloat(document.getElementById('wd-amount').value);
    var methodKey = document.getElementById('wd-method').value;
    var rate = parseFloat(document.getElementById('wd-rate').value);
    var resultEl = document.getElementById('wd-result');

    if (!amount || amount <= 0) {
      resultEl.innerHTML = '<div class="calc-warn"><h4>Укажи сумму вывода</h4></div>';
      return;
    }
    if (!rate || rate < 1000) {
      resultEl.innerHTML = '<div class="calc-warn"><h4>Укажи курс USD → UZS</h4></div>';
      return;
    }

    var m = METHODS[methodKey];
    var fee = calcFee(amount, methodKey);
    var net = Math.max(0, amount - fee);
    var netUZS = net * rate;
    var feePct = (fee / amount) * 100;

    var statusClass = feePct <= 2 ? 'calc-ok' : feePct <= 4 ? 'calc-warn' : 'calc-error';
    var statusLabel = feePct <= 2 ? 'Низкие комиссии' : feePct <= 4 ? 'Средние комиссии' : 'Высокие комиссии';

    var cheapest = findCheapest(amount);
    var cheapestLabel = METHODS[cheapest.key].label;
    var isCheapestSelected = cheapest.key === methodKey;

    var cheapestHtml;
    if (isCheapestSelected) {
      cheapestHtml = '<div class="wd-best-row">Самый дешёвый метод для <strong>$' + fmt(amount) + '</strong> — это <strong>' + cheapestLabel + '</strong> (уже выбран). Комиссия ~$' + fmt(cheapest.fee) + '.</div>';
    } else {
      cheapestHtml = '<div class="wd-best-row">Самый дешёвый метод для <strong>$' + fmt(amount) + '</strong> — <strong>' + cheapestLabel + '</strong> (~$' + fmt(cheapest.fee) + ' комиссии). Ты выбрал другой вариант — он обходится дороже на $' + fmt(fee - cheapest.fee) + '.</div>';
    }

    var html = '<div class="' + statusClass + '">'
      + '<h4>' + statusLabel + ' — ' + m.label + '</h4>'
      + '<table class="calc-table">'
      + '<tr><td><strong>Сумма вывода</strong></td><td>$' + fmt(amount) + '</td></tr>'
      + '<tr><td><strong>Ориентировочная комиссия</strong></td><td>−$' + fmt(fee) + ' (' + feePct.toFixed(1) + '%)</td></tr>'
      + '<tr><td><strong>Получишь на руки (USD)</strong></td><td><strong>$' + fmt(net) + '</strong></td></tr>'
      + '<tr><td><strong>Примерно в сумах</strong></td><td><strong>' + fmtUZS(netUZS) + ' сум</strong></td></tr>'
      + '<tr><td><strong>Скорость</strong></td><td>' + m.speed + '</td></tr>'
      + '</table>'
      + '<p style="margin:0.7rem 0 0; font-size:0.85rem; color:var(--md-default-fg-color--light);">Примечание: ' + m.note + '</p>'
      + '</div>'
      + cheapestHtml;

    resultEl.innerHTML = html;
  };

  document.addEventListener('DOMContentLoaded', function() {
    window.calcWithdrawal();
    document.getElementById('wd-amount').addEventListener('input', window.calcWithdrawal);
    document.getElementById('wd-method').addEventListener('change', window.calcWithdrawal);
    document.getElementById('wd-rate').addEventListener('input', window.calcWithdrawal);
  });
})();
</script>

---

## Главное правило

**Никогда не выводи всё одним переводом.** Раздели на 2-3 части, проверь на маленькой сумме сначала.

---

## Способы вывода — обзор

| Способ | Скорость | Комиссия | Сумма | Сложность |
|---|---|---|---|---|
| 💰 USDT (TRC-20) | 5-30 мин | 1-5 USD | без лимита | 🟢 простая |
| 💳 Visa/Mastercard USD | 1-5 дней | 1-3% | до $5k | 🟢 простая |
| 🏦 SWIFT в УЗС банк | 3-7 дней | $25-50 | $1k+ | 🟡 средняя |
| 📲 Wise / Payeer | 1-3 дня | 1-2% | до $10k | 🟡 средняя |
| 💵 Skrill / Neteller | 1-2 дня | 2-3% | до $5k | 🟢 простая |

---

## Способ 1: USDT (рекомендую большинству)

Самый простой и быстрый путь для Узбекистана.

### Шаги

#### 1. У брокера: вывод в USDT
- Личный кабинет → Вывод средств → USDT TRC-20
- Указываешь свой USDT-адрес (получишь из шага 2)
- Брокер обычно списывает 1-5 USD комиссию + сетевая комиссия TRC-20 ≈ $1
- Срок: обычно **5-30 минут**, иногда до 24 часов

#### 2. Криптобиржа (Binance / Bybit / KuCoin / OKX)
- Заранее зарегистрируйся и пройди верификацию (KYC)
- В разделе Wallet → Deposit → выбери USDT TRC-20 → скопируй свой адрес
- Этот адрес отдаёшь брокеру

#### 3. P2P в сум
- На бирже → P2P → Sell USDT → выбери UZS / Card
- Выбери продавца (читай отзывы, ищи 100+ сделок и >99% рейтинг)
- Курс обычно 95-99% от официального (комиссия P2P)
- Получишь сумы на свою карту HUMO/UZCARD за 5-30 минут

### Стоимость пути USDT → сум

Пример вывод $1 000:
- Брокер → USDT: −$3 комиссия
- TRC-20 сеть: −$1
- P2P курс 98% от рынка: −$20
- **Итого «съедается»: ~$24 (2.4%)**

### Плюсы
- Самый быстрый
- Анонимность сделок (но всё равно отчёт нужно)
- Низкие комиссии

### Минусы
- Нужна верификация на бирже (паспорт + селфи)
- Риск мошенничества в P2P → выбирай продавцов с историей

---

## Способ 2: SWIFT в банк Узбекистана

### Шаги

1. Открыть **долларовый счёт** в банке: Капиталбанк, Hamkorbank, Asaka, Anorbank, Узпромстройбанк
2. У брокера: Вывод → Bank Wire → ввести SWIFT-реквизиты
3. Срок: **3-7 рабочих дней**, иногда дольше

### Стоимость

- Комиссия брокера: $0-30 (зависит от брокера)
- Комиссия посредника-банка: $15-25
- Комиссия твоего банка: $0-20
- **Итого: $30-75** независимо от суммы (фиксированная)

**Выгодно при сумме от $2 000+.**

### Минусы
- Долго
- Может быть запрос документов от банка (происхождение средств)
- При выводе через ИП — проще; через физлицо — иногда задержки

---

## Способ 3: Wise (бывший TransferWise)

### Шаги

1. Регистрируешь Wise-счёт (USD)
2. У брокера: Вывод → Wise (если поддерживается) или SWIFT на Wise
3. На Wise меняешь USD на UZS
4. Wise переводит на твою карту HUMO/UZCARD

### Стоимость
- Wise: 0.5-1% за перевод USD → UZS
- + $2-5 фиксированная комиссия

### Минусы
- Не все брокеры выводят на Wise напрямую
- Лимиты Wise зависят от верификации

---

## ⚠️ Чего НЕ делать

### Не используй обменники в Telegram «без КYC»
- Часто мошенники
- Курс может быть отличным, но риск 100% потери высокий

### Не выводи на «чужие» USDT-кошельки
- Друг, родственник, «менеджер» — нет
- Только на свой кошелёк на бирже

### Не делай большие переводы одним платежом
- Сумма >$3000-5000 за раз может привлечь внимание банка
- Раздели на 2-3 транзакции с интервалом

### Не выводи всё под одну дату
- Регулярные переводы выглядят естественно
- Резкий вывод в конце года — менее естественно

---

## Документы для хранения

После каждого вывода сохраняй:

- 📄 **Подтверждение от брокера** (выписка о выводе)
- 📄 **TXID транзакции** USDT (если через крипту)
- 📄 **Скриншот P2P-сделки** (продавец, время, сумма)
- 📄 **Выписку с карты** с зачислением сумов
- 📄 **Чек ATM** при снятии налички

Храни **минимум 3 года** на случай вопросов от налоговой.

---

## Налоги — кратко

См. [tax-calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/uz/tax-calculator.py) для расчёта.

Основное:
- Декларируется **чистый годовой доход** (прибыли − убытки)
- НДФЛ 12% (актуально на 2026)
- Подача декларации до 1 апреля следующего года
- Платится не от каждой сделки, а **итого за год**

---

## Когда стоит подключить бухгалтера

- Доход от трейдинга **> $5 000 / год**
- Есть основная работа с белой зарплатой → нужна правильная общая декларация
- Не уверен в правильности заполнения
- Получил **запрос от налоговой** — обязательно к специалисту

---

## Контакты для проверки (не рекомендация, для справки)

| Где | Что |
|---|---|
| soliq.uz | Официальный сайт Налогового комитета |
| Личный кабинет налогоплательщика | my.soliq.uz |
| Контакт-центр soliq | 1198 |

---

[← К главному гайду](../forex-guide.md)
