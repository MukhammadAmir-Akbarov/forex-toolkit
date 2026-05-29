# 🚦 Предторговый чек-лист (зелёный свет)

!!! abstract "Зачем нужен этот чек-лист?"
    Большинство убытков у новичков случаются не потому что сетап «плохой» — а потому что сделка была открыта **без проверки базовых условий**: без стопа, с завышенным риском, на эмоциях или ради «отыгрыша».

    Этот чек-лист работает как **предполётная проверка пилота**: скучная, но обязательная. Если хотя бы одна галочка не стоит — **сделка не открывается**.

!!! warning "Образовательный материал — не финансовый совет"
    Эта страница — часть учебного проекта. Всё описанное является образовательным контентом и не является финансовой рекомендацией. Торговля сопряжена с реальными рисками.

---

## 🚦 Чек-лист перед входом в сделку

<style>
.pretrade-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.pretrade-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 0.9rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  cursor: pointer;
  transition: border-color 0.18s, background 0.18s;
  user-select: none;
}

.pretrade-item:hover {
  border-color: var(--md-primary-fg-color);
}

.pretrade-item.checked {
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.06);
}

.pretrade-item input[type="checkbox"] {
  margin-top: 3px;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  accent-color: #22c55e;
  cursor: pointer;
}

.pretrade-item-text {
  flex: 1;
  font-size: 0.96rem;
}

.pretrade-item-title {
  font-weight: 600;
  margin-bottom: 0.15rem;
}

.pretrade-item-hint {
  font-size: 0.82rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.1rem;
}

.pretrade-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1.2rem;
  flex-wrap: wrap;
}

.pretrade-reset {
  background: none;
  border: 1px solid var(--md-default-fg-color--lighter);
  color: var(--md-default-fg-color--light);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
}

.pretrade-reset:hover {
  border-color: var(--md-primary-fg-color);
  color: var(--md-primary-fg-color);
}

.pretrade-result {
  margin-top: 1.2rem;
  padding: 1.1rem 1.3rem;
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
  background: var(--md-default-bg-color);
}

.pretrade-green {
  border-left-color: #22c55e;
  background: rgba(34, 197, 94, 0.07);
}

.pretrade-green .pt-verdict {
  color: #16a34a;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.4rem;
}

.pretrade-red {
  border-left-color: #dc2626;
  background: rgba(220, 38, 38, 0.07);
}

.pretrade-red .pt-verdict {
  color: #dc2626;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.4rem;
}

.pt-failed-list {
  margin: 0.6rem 0 0;
  padding-left: 1.2rem;
  font-size: 0.92rem;
}

.pt-failed-list li {
  margin-bottom: 0.3rem;
}

.pretrade-stats {
  margin-top: 1.2rem;
  padding: 0.9rem 1.2rem;
  background: var(--md-code-bg-color);
  border-radius: 8px;
  border: 1px solid var(--md-default-fg-color--lightest);
  font-size: 0.88rem;
}

.pretrade-stats-title {
  font-weight: 700;
  font-size: 0.92rem;
  margin-bottom: 0.5rem;
  color: var(--md-default-fg-color--light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pt-stat-row {
  display: flex;
  justify-content: space-between;
  padding: 0.22rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}

.pt-stat-row:last-child { border-bottom: none; }

.pt-stat-value {
  font-family: var(--md-code-font-family);
  font-weight: 700;
}

.pt-stat-green { color: #16a34a; }
.pt-stat-red { color: #dc2626; }

.pt-discipline-bar-wrap {
  margin-top: 0.6rem;
}

.pt-discipline-label {
  font-size: 0.82rem;
  color: var(--md-default-fg-color--light);
  margin-bottom: 0.2rem;
}

.pt-discipline-bar-bg {
  width: 100%;
  height: 8px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 99px;
  overflow: hidden;
}

.pt-discipline-bar-fill {
  height: 100%;
  border-radius: 99px;
  background: #22c55e;
  transition: width 0.4s ease;
}
</style>

<div class="pretrade-widget">

<div id="pt-item-0" class="pretrade-item" onclick="ptToggle(0)">
  <input type="checkbox" id="pt-cb-0" onclick="event.stopPropagation(); ptToggle(0)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🛑 Стоп-лосс выставлен</div>
    <div class="pretrade-item-hint">Уровень SL определён до входа и выставлен в терминале — не «в голове»</div>
  </div>
</div>

<div id="pt-item-1" class="pretrade-item" onclick="ptToggle(1)">
  <input type="checkbox" id="pt-cb-1" onclick="event.stopPropagation(); ptToggle(1)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">💰 Риск ≤ 1% от депозита</div>
    <div class="pretrade-item-hint">Размер лота рассчитан так, что потеря по этой сделке не превысит 1% счёта</div>
  </div>
</div>

<div id="pt-item-2" class="pretrade-item" onclick="ptToggle(2)">
  <input type="checkbox" id="pt-cb-2" onclick="event.stopPropagation(); ptToggle(2)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🧮 Размер позиции посчитан калькулятором</div>
    <div class="pretrade-item-hint">Лот взят из калькулятора — не «на глаз» и не «как обычно»</div>
  </div>
</div>

<div id="pt-item-3" class="pretrade-item" onclick="ptToggle(3)">
  <input type="checkbox" id="pt-cb-3" onclick="event.stopPropagation(); ptToggle(3)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">😤 Это не отыгрыш (revenge trade)</div>
    <div class="pretrade-item-hint">Я не вхожу потому что только что получил стоп и хочу «вернуть деньги»</div>
  </div>
</div>

<div id="pt-item-4" class="pretrade-item" onclick="ptToggle(4)">
  <input type="checkbox" id="pt-cb-4" onclick="event.stopPropagation(); ptToggle(4)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📅 Проверен экономический календарь</div>
    <div class="pretrade-item-hint">В ближайшие 30 минут нет важных новостей (NFP, решение по ставке, CPI и т.д.)</div>
  </div>
</div>

<div id="pt-item-5" class="pretrade-item" onclick="ptToggle(5)">
  <input type="checkbox" id="pt-cb-5" onclick="event.stopPropagation(); ptToggle(5)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📋 Сетап соответствует торговому плану</div>
    <div class="pretrade-item-hint">Этот вход описан в моём трейдинг-плане. Я не торгую «новую идею» с ходу</div>
  </div>
</div>

<div id="pt-item-6" class="pretrade-item" onclick="ptToggle(6)">
  <input type="checkbox" id="pt-cb-6" onclick="event.stopPropagation(); ptToggle(6)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📐 RR ≥ 1.5 (потенциальная прибыль в 1.5× и более от риска)</div>
    <div class="pretrade-item-hint">Расстояние до TP как минимум в 1.5 раза больше расстояния до SL</div>
  </div>
</div>

<div id="pt-item-7" class="pretrade-item" onclick="ptToggle(7)">
  <input type="checkbox" id="pt-cb-7" onclick="event.stopPropagation(); ptToggle(7)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🔢 Дневной лимит сделок не превышен</div>
    <div class="pretrade-item-hint">Сегодня я ещё не достиг своего максимума сделок за день (обычно 2–3 максимум)</div>
  </div>
</div>

<div class="pretrade-actions">
  <button class="calc-button" onclick="ptCheck()">Проверить</button>
  <button class="pretrade-reset" onclick="ptReset()">Сбросить</button>
</div>

<div id="pt-result" class="pretrade-result" style="display:none;"></div>

<div id="pt-stats" class="pretrade-stats">
  <div class="pretrade-stats-title">Статистика дисциплины (этот браузер)</div>
  <div class="pt-stat-row">
    <span>Зелёных проверок (всё ОК)</span>
    <span class="pt-stat-value pt-stat-green" id="pt-green-count">—</span>
  </div>
  <div class="pt-stat-row">
    <span>Красных попыток (не всё ОК)</span>
    <span class="pt-stat-value pt-stat-red" id="pt-red-count">—</span>
  </div>
  <div class="pt-stat-row">
    <span>Коэффициент дисциплины</span>
    <span class="pt-stat-value" id="pt-discipline-pct">—</span>
  </div>
  <div class="pt-discipline-bar-wrap">
    <div class="pt-discipline-label">% нажатий при полном чек-листе</div>
    <div class="pt-discipline-bar-bg">
      <div class="pt-discipline-bar-fill" id="pt-disc-bar" style="width:0%"></div>
    </div>
  </div>
</div>

</div>

<script>
(function () {
  var TOTAL = 8;
  var KEY_RED = 'ftk-pretrade-redattempts';
  var KEY_GREEN = 'ftk-pretrade-greenattempts';

  function getCount(key) {
    return parseInt(localStorage.getItem(key) || '0', 10);
  }

  function incCount(key) {
    localStorage.setItem(key, getCount(key) + 1);
  }

  function ptToggle(idx) {
    var cb = document.getElementById('pt-cb-' + idx);
    var item = document.getElementById('pt-item-' + idx);
    cb.checked = !cb.checked;
    item.classList.toggle('checked', cb.checked);
  }

  window.ptToggle = ptToggle;

  window.ptCheck = function () {
    var failed = [];
    var labels = [
      'Стоп-лосс выставлен',
      'Риск ≤ 1% от депозита',
      'Размер позиции посчитан калькулятором',
      'Это не отыгрыш (revenge trade)',
      'Проверен экономический календарь',
      'Сетап соответствует торговому плану',
      'RR ≥ 1.5',
      'Дневной лимит сделок не превышен'
    ];

    for (var i = 0; i < TOTAL; i++) {
      if (!document.getElementById('pt-cb-' + i).checked) {
        failed.push(labels[i]);
      }
    }

    var resultEl = document.getElementById('pt-result');
    resultEl.style.display = 'block';

    if (failed.length === 0) {
      incCount(KEY_GREEN);
      resultEl.className = 'pretrade-result pretrade-green';
      resultEl.innerHTML =
        '<div class="pt-verdict">✅ Можно открывать</div>' +
        '<p style="margin:0;font-size:0.93rem;">Все условия соблюдены. Открывай сделку строго по плану, без изменений стопа и тейка после входа.</p>';
    } else {
      incCount(KEY_RED);
      var listItems = failed.map(function (f) { return '<li>' + f + '</li>'; }).join('');
      resultEl.className = 'pretrade-result pretrade-red';
      resultEl.innerHTML =
        '<div class="pt-verdict">🛑 НЕ открывай</div>' +
        '<p style="margin:0 0 0.5rem;font-size:0.93rem;">Не выполнено <strong>' + failed.length + '</strong> из ' + TOTAL + ' условий:</p>' +
        '<ul class="pt-failed-list">' + listItems + '</ul>' +
        '<p style="margin:0.7rem 0 0;font-size:0.85rem;color:var(--md-default-fg-color--light);">Исправь все пункты, затем нажми «Проверить» ещё раз.</p>';
    }

    updateStats();
    resultEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  window.ptReset = function () {
    for (var i = 0; i < TOTAL; i++) {
      var cb = document.getElementById('pt-cb-' + i);
      var item = document.getElementById('pt-item-' + i);
      cb.checked = false;
      item.classList.remove('checked');
    }
    var resultEl = document.getElementById('pt-result');
    resultEl.style.display = 'none';
    resultEl.innerHTML = '';
  };

  function updateStats() {
    var green = getCount(KEY_GREEN);
    var red = getCount(KEY_RED);
    var total = green + red;

    document.getElementById('pt-green-count').textContent = green;
    document.getElementById('pt-red-count').textContent = red;

    if (total === 0) {
      document.getElementById('pt-discipline-pct').textContent = '—';
      document.getElementById('pt-disc-bar').style.width = '0%';
    } else {
      var pct = Math.round((green / total) * 100);
      document.getElementById('pt-discipline-pct').textContent = pct + '%';
      document.getElementById('pt-disc-bar').style.width = pct + '%';
      var bar = document.getElementById('pt-disc-bar');
      if (pct >= 80) {
        bar.style.background = '#22c55e';
      } else if (pct >= 50) {
        bar.style.background = '#f59e0b';
      } else {
        bar.style.background = '#dc2626';
      }
    }
  }

  window.addEventListener('DOMContentLoaded', updateStats);
}());
</script>

---

## 📖 Зачем каждый пункт

### 1. Стоп-лосс выставлен

Стоп в терминале — не «в голове». Профессионал выставляет его **до** открытия позиции. Без стопа ты не знаешь, сколько можешь потерять: это уже не трейдинг, это казино.

### 2. Риск ≤ 1%

При серии из 10 убытков подряд (редко, но бывает) ты потеряешь ~10% депозита — и счёт жив. При риске 5% за сделку — 10 убытков = -50% депозита, и психика сломана.

### 3. Размер позиции калькулятором

«На глаз» и «как обычно» — главная причина нарушения риска 1%. [Используй калькулятор позиции](../tools/position-calculator.md). 30 секунд, которые сохраняют деньги.

### 4. Это не отыгрыш

Получил стоп — возникло желание «вернуть деньги прямо сейчас»? Это **revenge trade**. Такие сделки статистически убыточны: ты входишь на эмоциях, не на логике. [Anti-Tilt протокол](anti-tilt-protocol.md) — твой инструмент.

### 5. Экономический календарь

NFP, решение ФРС, CPI — это «ядерные» новости. В момент выхода спред расширяется, стопы проскальзывают. Новичкам — **не торговать за 15–30 минут до и после** крупных новостей.

!!! tip "Где смотреть"
    [Investing.com/economic-calendar](https://www.investing.com/economic-calendar/) или [ForexFactory.com](https://www.forexfactory.com/calendar) — бесплатно, фильтруй события «High Impact».

### 6. Сетап по плану

Если этого сетапа нет в твоём [торговом плане](trading-plan-template.md) — значит ты его не тестировал. Не торгуй то, что не проверено хотя бы на демо. «Выглядит как хороший вход» — не торговый план.

### 7. RR ≥ 1.5

При Win Rate 50% и RR = 1.5 → математическое ожидание **положительное**. При RR = 0.8 — отрицательное. [Калькулятор WinRate × RR](../tools/winrate-rr-calculator.md) покажет точные цифры.

| RR | Нужный WR для выхода в ноль |
|---|---|
| 0.5 | 67% |
| 1.0 | 50% |
| **1.5** | **40%** |
| 2.0 | 33% |

### 8. Дневной лимит сделок

Больше сделок — не значит больше прибыли. У новичков «перегруз» (overtrading) — одна из топ-3 причин слива. Реши заранее: максимум **2–3 сделки в день**. Если лимит достигнут — компьютер закрыт.

---

## 🧠 Что делать, если не можешь поставить галочку?

!!! danger "Красный флаг: «Я знаю, что нарушаю правило, но всё равно войду»"
    Если ты осознанно игнорируешь чек-лист — это не «уверенность опытного трейдера». Это начало тильта.

    Закрой терминал. Прочитай [Anti-Tilt Protocol](anti-tilt-protocol.md).

**Не выставить SL** — значит либо платформа не позволяет в данный момент (технически — реши это сначала), либо ты надеешься «выйти вручную». Так не работает.

**Риск > 1%** — соблазн «увеличить размер, потому что сетап очень хороший» — ловушка. Хорошие сетапы случаются регулярно. Этот — не последний.

**Revenge trade** — единственный правильный ответ: пауза 30 минут после стопа. Встань, попей воды. Рынок никуда не убежит.

---

## 📋 Быстрая справочная карточка

```
ПРЕДТОРГОВЫЙ ЧЕК-ЛИСТ — коротко

☐  Стоп-лосс выставлен в терминале
☐  Риск ≤ 1% депозита
☐  Лот посчитан калькулятором
☐  Это НЕ отыгрыш
☐  Новости проверены (≥ 30 мин до события)
☐  Сетап есть в торговом плане
☐  RR ≥ 1.5
☐  Дневной лимит сделок не превышен

ВСЕ 8 — зелёный свет ✅
Хоть один НЕТ — стоп 🛑
```

> **Распечатай и положи рядом с монитором.**
> Пока чек-лист не в привычке — используй бумажную версию.

---

## 🔗 Связанные страницы

- [Anti-Tilt Protocol](anti-tilt-protocol.md) — что делать, если хочется нарушить правила
- [Emergency Card](emergency-card.md) — экстренная помощь в кризис
- [Калькулятор позиции](../tools/position-calculator.md) — рассчитай корректный лот
- [WinRate × RR калькулятор](../tools/winrate-rr-calculator.md) — проверь математику сетапа
- [Торговый план — шаблон](trading-plan-template.md) — если у тебя ещё нет плана
- [Психология трейдинга](psychology.md) — почему мозг саботирует правила
