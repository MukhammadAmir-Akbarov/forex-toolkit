---
widgets: [readiness]
---

# 🚦 Готов ли я к реалу? — вердикт по демо

!!! abstract "Честный ответ вместо «вроде получается»"
    Введи статистику своего демо-счёта — инструмент сверит её с чек-листом [перехода на реал](../journal/demo-vs-real-comparison.md) и скажет прямо: **готов** или **рано, и вот что подтянуть**. Промежуточного «почти» нет: невыполненный пункт на реале стоит денег.

    Цифры возьми из [журнала сделок](../journal/README.md) или отчёта MT5. Ничего не отправляется на сервер.

---

## 🧮 Твоя демо-статистика

<div class="calc-widget">

<div class="calc-row"><label>Сколько месяцев торгуешь на демо</label><input type="number" id="rd-months" min="0" step="1" value="1"></div>
<div class="calc-row"><label>Сколько сделок закрыто</label><input type="number" id="rd-trades" min="0" step="1" value="20"></div>
<div class="calc-row"><label>Winrate (доля прибыльных сделок)</label><input type="number" id="rd-winrate" min="0" max="100" step="1" value="45"><span>%</span></div>
<div class="calc-row"><label>Средний RR (средняя прибыль / средний убыток)</label><input type="number" id="rd-rr" min="0.1" step="0.1" value="1.5"></div>
<div class="calc-row"><label>Максимальная просадка демо-счёта</label><input type="number" id="rd-dd" min="0" max="100" step="1" value="12"><span>%</span></div>
<div class="calc-row"><label>Сделок с нарушением своих правил</label><input type="number" id="rd-viol" min="0" max="100" step="1" value="10"><span>%</span></div>
<div class="calc-row"><label><input type="checkbox" id="rd-journal"> Веду журнал по каждой сделке</label></div>
<div class="calc-row"><label><input type="checkbox" id="rd-canlose"> Сумму для реала не жалко потерять полностью</label></div>

<button class="calc-button" id="rd-calc-btn">Проверить</button>

<div id="rd-result" class="calc-result"></div>

</div>

---

## 📋 Критерии и почему они такие

| Пункт | Порог | Зачем |
|---|---|---|
| Срок на демо | ≥ 3 месяца | Один удачный месяц не отличить от системы |
| Число сделок | ≥ 50 | На 10–20 сделках статистика — шум |
| Winrate | ≥ 40% | Ниже — серии стопов психологически тяжелы даже при хорошем RR |
| Profit Factor | ≥ 1.5 | Запас, который съедят спред, комиссия и проскальзывание на реале |
| Макс. просадка | ≤ 20% | Глубже — [восстановление](drawdown-recovery.md) требует несоразмерной прибыли |
| Нарушения правил | < 5% сделок | Результат должен давать система, а не импровизация |
| Журнал + «не жалко потерять» | да | Без журнала нечего чинить, без подушки — давление на каждую сделку |

Profit Factor считается из winrate и RR: `PF = winrate × RR / (1 − winrate)`. Матожидание в R на сделку: `winrate × RR − (1 − winrate)`. Подробнее — в [калькуляторе WinRate × RR](winrate-rr-calculator.md).

---

## 🔗 Что дальше

- [Тест готовности](risk-profile.md) — психология и финансовая подушка (дополняет этот вердикт)
- [Demo vs Real](../journal/demo-vs-real-comparison.md) — как переходить на реал постепенно
- [Риск разорения](risk-of-ruin.md) — как твоя статистика переживает плохие серии

---

!!! note "Образовательный материал"
    Вердикт — **учебный ориентир**, а не финансовый совет и не гарантия результата. Выполненный чек-лист не защищает от убытков: реальная торговля всегда несёт риск полной потери вложенных средств.
