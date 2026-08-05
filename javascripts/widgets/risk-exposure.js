(function () {
  "use strict";
  var root = document.getElementById("risk-exposure-widget");
  if (!root || !window.FXW) return;
  var F = window.FXW;
  var T = F.pick({
    ru: { deposit: "Депозит, USD", limit: "Общий лимит, %", rate: "Курс USD -> UZS", allocation: "Распределение", equal: "Поровну", weighted: "По стопу", pair: "Пара", direction: "Направление", long: "Long", short: "Short", stop: "Стоп, пипсы", pip: "USD/пипс на 1 лот", add: "+ Добавить позицию", calc: "Рассчитать портфель", nominal: "Номинальный риск", effective: "Корреляционная оценка", remaining: "Остаток лимита", budget: "Лимит", lots: "Риск и лот по позициям", exposure: "Валютная экспозиция", warning: "Лимит превышен. Уменьши риск или число позиций.", corr: "Сильная связь", note: "Корреляции статические и ориентировочные, а не live-сигнал." },
    en: { deposit: "Balance, USD", limit: "Total limit, %", rate: "USD -> UZS rate", allocation: "Allocation", equal: "Equal", weighted: "By stop", pair: "Pair", direction: "Direction", long: "Long", short: "Short", stop: "Stop, pips", pip: "USD/pip per lot", add: "+ Add position", calc: "Calculate portfolio", nominal: "Nominal risk", effective: "Correlation estimate", remaining: "Limit remaining", budget: "Limit", lots: "Risk and lot by position", exposure: "Currency exposure", warning: "Limit exceeded. Reduce risk or the number of positions.", corr: "Strong relationship", note: "Correlations are static estimates, not a live signal." },
    uz: { deposit: "Depozit, USD", limit: "Umumiy limit, %", rate: "USD -> UZS kursi", allocation: "Taqsimlash", equal: "Teng", weighted: "Stop bo'yicha", pair: "Juftlik", direction: "Yo'nalish", long: "Long", short: "Short", stop: "Stop, pip", pip: "1 lot uchun USD/pip", add: "+ Pozitsiya qo'shish", calc: "Portfelni hisoblash", nominal: "Nominal risk", effective: "Korrelyatsion baho", remaining: "Qolgan limit", budget: "Limit", lots: "Pozitsiyalar bo'yicha risk va lot", exposure: "Valyuta ekspozitsiyasi", warning: "Limit oshdi. Riskni yoki pozitsiyalar sonini kamaytiring.", corr: "Kuchli bog'lanish", note: "Korrelyatsiyalar statik taxmin, live signal emas." }
  });
  var correlations = { "EURUSD|GBPUSD": .85, "EURUSD|AUDUSD": .75, "EURUSD|NZDUSD": .70, "EURUSD|USDCHF": -.95, "EURUSD|USDJPY": -.30, "GBPUSD|AUDUSD": .65, "GBPUSD|USDCHF": -.85, "USDJPY|USDCHF": .40, "AUDUSD|NZDUSD": .90, "EURJPY|GBPJPY": .85, "EURUSD|EURJPY": .55 };
  var pairs = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "NZDUSD", "EURJPY", "GBPJPY", "XAUUSD"];

  root.innerHTML = '<div class="fx-tool-grid">' +
    field(T.deposit, '<input id="rx-deposit" type="number" min="1" value="1000">') +
    field(T.limit, '<input id="rx-limit" type="number" min="0.1" step="0.1" value="2">') +
    field(T.rate, '<input id="rx-rate" type="number" min="1" value="12500">') +
    field(T.allocation, '<select id="rx-allocation"><option value="equal">' + T.equal + '</option><option value="weighted">' + T.weighted + '</option></select>') +
    '</div><div id="rx-rows"></div><div class="fx-tool-actions"><button type="button" class="fx-secondary" id="rx-add">' + T.add + '</button><button type="button" id="rx-calc">' + T.calc + '</button></div><div id="rx-result" class="fx-result" hidden></div><p class="fx-tool-note">' + T.note + '</p>';

  function field(label, control) { return '<label><span>' + label + '</span>' + control + '</label>'; }
  function pairOptions(selected) { return pairs.map(function (pair) { return '<option' + (pair === selected ? ' selected' : '') + '>' + pair + '</option>'; }).join(''); }
  function addRow(pair) {
    var rows = document.getElementById("rx-rows");
    if (rows.children.length >= 6) return;
    var row = document.createElement("div");
    row.className = "fx-position-row";
    row.innerHTML = field(T.pair, '<select class="rx-pair">' + pairOptions(pair || pairs[rows.children.length]) + '</select>') + field(T.direction, '<select class="rx-direction"><option value="long">' + T.long + '</option><option value="short">' + T.short + '</option></select>') + field(T.stop, '<input class="rx-stop" type="number" min="0.1" value="' + (20 + rows.children.length * 5) + '">') + field(T.pip, '<input class="rx-pip" type="number" min="0.01" step="0.01" value="10">') + '<button type="button" class="fx-remove" aria-label="Remove">x</button>';
    row.querySelector(".fx-remove").addEventListener("click", function () { if (rows.children.length > 1) row.remove(); });
    rows.appendChild(row);
  }
  function corr(a, b) { if (a === b) return 1; return correlations[a + "|" + b] || correlations[b + "|" + a] || 0; }
  function money(value) { return F.money(value); }
  function calculate() {
    var deposit = Number(document.getElementById("rx-deposit").value);
    var limit = Number(document.getElementById("rx-limit").value);
    var rate = Number(document.getElementById("rx-rate").value);
    var rows = Array.prototype.map.call(document.querySelectorAll(".fx-position-row"), function (row) { return { pair: row.querySelector(".rx-pair").value, direction: row.querySelector(".rx-direction").value, stop: Number(row.querySelector(".rx-stop").value), pip: Number(row.querySelector(".rx-pip").value) }; });
    if (!(deposit > 0 && limit > 0 && rate > 0) || rows.some(function (row) { return !(row.stop > 0 && row.pip > 0); })) return;
    var budget = deposit * limit / 100;
    var weights = rows.map(function (row) { return document.getElementById("rx-allocation").value === "weighted" ? 1 / row.stop : 1; });
    var weightTotal = weights.reduce(function (sum, value) { return sum + value; }, 0);
    rows.forEach(function (row, index) { row.risk = budget * weights[index] / weightTotal; row.lot = row.risk / (row.stop * row.pip); });
    var variance = rows.reduce(function (sum, row) { return sum + row.risk * row.risk; }, 0);
    var strong = [], exposure = {};
    rows.forEach(function (row, index) {
      var sign = row.direction === "long" ? 1 : -1;
      exposure[row.pair.slice(0, 3)] = (exposure[row.pair.slice(0, 3)] || 0) + sign * row.risk;
      exposure[row.pair.slice(3)] = (exposure[row.pair.slice(3)] || 0) - sign * row.risk;
      rows.slice(index + 1).forEach(function (other) {
        var rho = corr(row.pair, other.pair);
        variance += 2 * rho * sign * (other.direction === "long" ? 1 : -1) * row.risk * other.risk;
        if (Math.abs(rho) >= .7) strong.push(row.pair + " / " + other.pair + " (" + (rho > 0 ? "+" : "") + rho.toFixed(2) + ")");
      });
    });
    var nominal = rows.reduce(function (sum, row) { return sum + row.risk; }, 0);
    var effective = Math.sqrt(Math.max(0, variance));
    var positions = rows.map(function (row) { return '<li><strong>' + row.pair + ' ' + row.direction + '</strong>: ' + money(row.risk) + ' / ' + (row.risk * rate).toLocaleString(F.numLocale, { maximumFractionDigits: 0 }) + ' UZS; ' + row.lot.toFixed(3) + ' lot</li>'; }).join('');
    var currencies = Object.keys(exposure).filter(function (key) { return Math.abs(exposure[key]) > .001; }).sort().map(function (key) { return '<li>' + key + ': ' + (exposure[key] > 0 ? "+" : "") + money(exposure[key]) + '</li>'; }).join('');
    var result = document.getElementById("rx-result");
    result.innerHTML = '<div class="fx-metrics"><div><span>' + T.nominal + '</span><strong>' + money(nominal) + ' / ' + (nominal / deposit * 100).toFixed(2) + '%</strong></div><div><span>' + T.effective + '</span><strong>' + money(effective) + ' / ' + (effective / deposit * 100).toFixed(2) + '%</strong></div><div><span>' + T.remaining + '</span><strong>' + money(Math.max(0, budget - nominal)) + '</strong></div><div><span>' + T.budget + ' UZS</span><strong>' + (budget * rate).toLocaleString(F.numLocale, { maximumFractionDigits: 0 }) + '</strong></div></div>' + (nominal > budget + .001 ? '<p class="fx-warning">' + T.warning + '</p>' : '') + '<h3>' + T.lots + '</h3><ul>' + positions + '</ul><h3>' + T.exposure + '</h3><ul>' + currencies + '</ul>' + (strong.length ? '<p><strong>' + T.corr + ':</strong> ' + strong.join(', ') + '</p>' : '');
    result.hidden = false;
    if (window.fxTrack) window.fxTrack("risk_exposure_completed");
  }
  document.getElementById("rx-add").addEventListener("click", function () { addRow(); });
  document.getElementById("rx-calc").addEventListener("click", calculate);
  addRow("EURUSD"); addRow("GBPUSD");
})();
