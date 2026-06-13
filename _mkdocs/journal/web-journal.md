# 📊 Веб-журнал сделок

!!! abstract "Что делает этот инструмент"
    Загрузи CSV-журнал — браузер сразу посчитает Win Rate, Profit Factor, P&L,
    результат в R, максимальную просадку и дисциплину. Можно фильтровать сделки
    по датам, паре, направлению и соблюдению правил.

!!! tip "Приватность"
    Файл обрабатывается **только в твоём браузере**. Он не загружается на сервер
    и не сохраняется после закрытия страницы.

Поддерживаются оба формата проекта: расширенный
[`trading-journal-template.csv`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/journal/trading-journal-template.csv)
и короткий CSV, который создаёт `forex-journal`.

<div class="journal-widget" id="journal-widget">
  <div class="journal-drop" id="journal-drop">
    <strong>Перетащи CSV-файл сюда</strong>
    <div class="journal-actions">
      <label class="journal-button" for="journal-file">Выбрать CSV</label>
      <input id="journal-file" type="file" accept=".csv,text/csv" hidden>
      <button class="journal-button secondary" id="journal-demo" type="button">Открыть демо</button>
    </div>
    <p class="journal-file-name" id="journal-file-name">Файл ещё не выбран</p>
    <p class="journal-privacy">🔒 Данные остаются на этом устройстве.</p>
  </div>
  <div class="journal-error" id="journal-error"></div>

  <div class="journal-dashboard" id="journal-dashboard">
    <div class="journal-filters">
      <label>С даты<input id="journal-from" type="date"></label>
      <label>По дату<input id="journal-to" type="date"></label>
      <label>Пара<select id="journal-pair"><option value="">Все</option></select></label>
      <label>Направление
        <select id="journal-direction">
          <option value="">Все</option><option value="long">Long</option><option value="short">Short</option>
        </select>
      </label>
      <label>Правила
        <select id="journal-rules">
          <option value="">Все</option><option value="yes">Да</option><option value="no">Нет</option>
        </select>
      </label>
    </div>

    <div class="journal-metrics">
      <div class="journal-card"><div class="journal-card-label">Сделок</div><div class="journal-card-value" id="journal-m-trades">0</div></div>
      <div class="journal-card"><div class="journal-card-label">Win Rate</div><div class="journal-card-value" id="journal-m-winrate">0%</div></div>
      <div class="journal-card"><div class="journal-card-label">Profit Factor</div><div class="journal-card-value" id="journal-m-pf">0</div></div>
      <div class="journal-card"><div class="journal-card-label">Чистый P&L</div><div class="journal-card-value" id="journal-m-pnl">$0</div></div>
      <div class="journal-card"><div class="journal-card-label">Итого R</div><div class="journal-card-value" id="journal-m-r">0R</div></div>
      <div class="journal-card"><div class="journal-card-label">Макс. просадка</div><div class="journal-card-value" id="journal-m-dd">$0</div></div>
      <div class="journal-card"><div class="journal-card-label">По правилам</div><div class="journal-card-value" id="journal-m-discipline">0%</div></div>
      <div class="journal-card"><div class="journal-card-label">Показано</div><div class="journal-card-value" id="journal-m-filtered">0 / 0</div></div>
    </div>

    <div class="journal-empty" id="journal-empty" style="display:none"></div>
    <div class="journal-chart-wrap"><h3>Equity curve</h3><canvas id="journal-equity"></canvas></div>
    <div class="journal-rules">
      <h3>Сделки по правилам и с нарушениями</h3>
      <div class="journal-rules-grid">
        <div class="journal-rule-card" id="journal-rules-yes"></div>
        <div class="journal-rule-card" id="journal-rules-no"></div>
      </div>
    </div>
    <div class="journal-table-wrap">
      <h3>Последние 30 сделок</h3>
      <div class="journal-table-scroll">
        <table class="journal-table">
          <thead><tr><th>Дата</th><th>Время</th><th>Пара</th><th>Dir</th><th>Сетап</th><th>Исход</th><th>P&L</th><th>R</th></tr></thead>
          <tbody id="journal-table-body"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script id="journal-demo-data" type="text/plain">
id,date,time,pair,direction,setup,risk_usd,result_usd,result_r,outcome,followed_rules
1,2026-05-11,09:15,EURUSD,long,EMA50 pullback,10,20,2,win,yes
2,2026-05-12,14:30,GBPUSD,short,Resistance rejection,10,-10,-1,loss,yes
3,2026-05-13,16:10,EURUSD,long,Breakout,10,-10,-1,loss,no
4,2026-05-14,10:40,USDJPY,short,London range,10,15,1.5,win,yes
5,2026-05-15,18:20,GBPUSD,long,FOMO entry,10,-12,-1.2,loss,no
6,2026-05-18,11:05,EURUSD,long,EMA50 pullback,10,20,2,win,yes
</script>

## Как читать результаты

- **Win Rate** считается только по Win/Loss; безубыток не искажает процент.
- **Profit Factor** = сумма прибылей / сумма убытков.
- **Итого R** берётся из `result_r`; если поля нет, считается как `result_usd / risk_usd`.
- **Максимальная просадка** — самое глубокое падение equity от предыдущего пика.
- **По правилам** — доля `yes` среди сделок, где это поле заполнено.

Для надёжных выводов накопи хотя бы **30 сделок одной стратегии**.

