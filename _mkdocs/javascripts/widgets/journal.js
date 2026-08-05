/*
 * Локальный веб-анализатор торгового журнала.
 * Поддерживает расширенный CSV-шаблон и короткий формат journal_cli.py.
 * Файл читается через FileReader и никогда не отправляется в сеть.
 */
(function () {
  var root = document.getElementById("journal-widget");
  if (!root) return;

  var F = window.FXW;
  var T = F.pick({
    ru: {
      fileReady: function (name, count) { return name + ": загружено строк " + count; },
      demo: "Демо-журнал",
      invalid: "Не удалось прочитать CSV или MT5 HTML. Проверь формат файла.",
      noRows: "В выбранном диапазоне нет закрытых сделок.",
      all: "Все",
      yes: "По правилам",
      no: "С нарушениями",
      unknown: "Не указано",
      trades: "Сделок",
      pnl: "P&L",
      rTotal: "Итого R",
      drawdown: "Макс. просадка",
      discipline: "Дисциплина",
      following: "По правилам",
      violating: "С нарушениями",
      n: "сделок",
      wr: "Win Rate",
      tableEmpty: "Нет сделок для показа.",
      saved: "Журнал сохранён на этом устройстве.",
      restored: "Восстановлен последний журнал",
      cleared: "Сохранённый журнал удалён.",
      noFile: "Файл ещё не выбран",
      exportReady: "Сводка экспортирована.",
      weekdays: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
      insightSample: function (count) { return "Пока только " + count + " сделок. Для устойчивых выводов желательно 30+ в одной стратегии."; },
      insightExpectancy: function (value) { return "Средний результат на сделку: " + value + "R."; },
      insightEvening: function (count, value) { return "Вечером (после 18:00) " + count + " сделок дали " + value + "R. Проверь лимит на вечернюю торговлю."; },
      insightRules: function (count, value) { return count + " нарушений правил стоили " + value + "R. Это первая зона для исправления."; },
      insightWorst: function (label, value) { return "Слабейшая группа: " + label + " (" + value + "R). Временно сократи её или пересмотри условия входа."; },
      insightBest: function (label, value) { return "Сильнейшая группа: " + label + " (" + value + "R). Проверь, можно ли формализовать её условия."; },
      insightDiscipline: function (value) { return "Дисциплина " + value + "%. Цель перед увеличением риска — не ниже 95%."; },
      restoredName: "Сохранённый журнал",
    },
    en: {
      fileReady: function (name, count) { return name + ": " + count + " rows loaded"; },
      demo: "Demo journal",
      invalid: "Could not read the CSV or MT5 HTML file. Check its format.",
      noRows: "There are no closed trades in the selected range.",
      all: "All",
      yes: "Followed rules",
      no: "Rule violations",
      unknown: "Not specified",
      trades: "Trades",
      pnl: "P&L",
      rTotal: "Total R",
      drawdown: "Max drawdown",
      discipline: "Discipline",
      following: "Followed rules",
      violating: "Rule violations",
      n: "trades",
      wr: "Win Rate",
      tableEmpty: "No trades to display.",
      saved: "Journal saved on this device.",
      restored: "Restored the latest journal",
      cleared: "Saved journal removed.",
      noFile: "No file selected",
      exportReady: "Summary exported.",
      weekdays: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      insightSample: function (count) { return "Only " + count + " trades so far. Aim for 30+ trades in one strategy for stable conclusions."; },
      insightExpectancy: function (value) { return "Average result per trade: " + value + "R."; },
      insightEvening: function (count, value) { return count + " evening trades (after 18:00) produced " + value + "R. Consider an evening trading limit."; },
      insightRules: function (count, value) { return count + " rule violations cost " + value + "R. This is the first area to fix."; },
      insightWorst: function (label, value) { return "Weakest group: " + label + " (" + value + "R). Reduce it temporarily or review its entry conditions."; },
      insightBest: function (label, value) { return "Strongest group: " + label + " (" + value + "R). Check whether its conditions can be formalized."; },
      insightDiscipline: function (value) { return "Discipline is " + value + "%. Target at least 95% before increasing risk."; },
      restoredName: "Saved journal",
    },
    uz: {
      fileReady: function (name, count) { return name + ": " + count + " qator yuklandi"; },
      demo: "Demo jurnal",
      invalid: "CSV yoki MT5 HTML faylni o'qib bo'lmadi. Formatni tekshiring.",
      noRows: "Tanlangan oraliqda yopilgan savdolar yo'q.",
      all: "Barchasi",
      yes: "Qoidaga rioya",
      no: "Qoida buzilgan",
      unknown: "Ko'rsatilmagan",
      trades: "Savdolar",
      pnl: "P&L",
      rTotal: "Jami R",
      drawdown: "Maks. pasayish",
      discipline: "Intizom",
      following: "Qoidaga rioya",
      violating: "Qoida buzilgan",
      n: "savdo",
      wr: "Win Rate",
      tableEmpty: "Ko'rsatish uchun savdo yo'q.",
      saved: "Jurnal shu qurilmada saqlandi.",
      restored: "Oxirgi jurnal tiklandi",
      cleared: "Saqlangan jurnal o'chirildi.",
      noFile: "Fayl tanlanmagan",
      exportReady: "Hisobot eksport qilindi.",
      weekdays: ["Du", "Se", "Cho", "Pa", "Ju", "Sha", "Ya"],
      insightSample: function (count) { return "Hozircha " + count + " ta savdo bor. Barqaror xulosa uchun bitta strategiyada 30+ savdo to'plang."; },
      insightExpectancy: function (value) { return "Har bir savdoning o'rtacha natijasi: " + value + "R."; },
      insightEvening: function (count, value) { return "Kechqurun (18:00 dan keyin) " + count + " ta savdo " + value + "R berdi. Kechki savdoga limit qo'yishni tekshiring."; },
      insightRules: function (count, value) { return count + " ta qoida buzilishi " + value + "R ga tushdi. Avval shu joyni tuzating."; },
      insightWorst: function (label, value) { return "Eng zaif guruh: " + label + " (" + value + "R). Uni vaqtincha kamaytiring yoki kirish shartlarini ko'rib chiqing."; },
      insightBest: function (label, value) { return "Eng kuchli guruh: " + label + " (" + value + "R). Uning shartlarini aniq qoidaga aylantirishni tekshiring."; },
      insightDiscipline: function (value) { return "Intizom " + value + "%. Riskni oshirishdan oldin maqsad kamida 95%."; },
      restoredName: "Saqlangan jurnal",
    },
  });

  var STORAGE_KEY = "forex_journal_data_v2";
  var state = { rows: [], sourceText: "", sourceName: "" };
  var fileInput = document.getElementById("journal-file");
  var drop = document.getElementById("journal-drop");
  var demoButton = document.getElementById("journal-demo");
  var error = document.getElementById("journal-error");
  var dashboard = document.getElementById("journal-dashboard");
  var fileName = document.getElementById("journal-file-name");
  var status = document.getElementById("journal-status");
  var filters = ["journal-from", "journal-to", "journal-pair", "journal-direction", "journal-rules"];

  function detectDelimiter(line) {
    var options = [",", ";", "\t"];
    var best = ",", max = -1;
    options.forEach(function (delimiter) {
      var count = 0, quoted = false;
      for (var i = 0; i < line.length; i++) {
        if (line[i] === '"') quoted = !quoted;
        else if (!quoted && line[i] === delimiter) count++;
      }
      if (count > max) { max = count; best = delimiter; }
    });
    return best;
  }

  function parseCSV(text) {
    text = String(text || "").replace(/^\uFEFF/, "");
    var delimiter = detectDelimiter((text.split(/\r?\n/, 1)[0] || ""));
    var matrix = [], row = [], field = "", quoted = false;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (quoted) {
        if (ch === '"' && text[i + 1] === '"') { field += '"'; i++; }
        else if (ch === '"') quoted = false;
        else field += ch;
      } else if (ch === '"') quoted = true;
      else if (ch === delimiter) { row.push(field); field = ""; }
      else if (ch === "\n") {
        row.push(field.replace(/\r$/, ""));
        if (row.some(function (v) { return v.trim() !== ""; })) matrix.push(row);
        row = []; field = "";
      } else field += ch;
    }
    row.push(field.replace(/\r$/, ""));
    if (row.some(function (v) { return v.trim() !== ""; })) matrix.push(row);
    if (matrix.length < 2) return [];
    var headers = matrix.shift().map(function (h) { return h.trim().toLowerCase(); });
    return matrix.map(function (values) {
      var item = {};
      headers.forEach(function (h, index) { item[h] = (values[index] || "").trim(); });
      return item;
    });
  }

  function parseMT5HTML(text) {
    var documentNode = new DOMParser().parseFromString(String(text), "text/html");
    var aliases = {
      time: ["time", "время"],
      deal: ["deal", "сделка", "ticket", "тикет"],
      symbol: ["symbol", "символ", "инструмент"],
      type: ["type", "тип"],
      entry: ["direction", "entry", "направление", "вход"],
      volume: ["volume", "объем", "объём"],
      price: ["price", "цена"],
      commission: ["commission", "комиссия"],
      fee: ["fee", "сбор"],
      swap: ["swap", "своп"],
      profit: ["profit", "прибыль"],
      comment: ["comment", "комментарий"],
    };
    function canonical(value) {
      var label = String(value || "").trim().toLowerCase().replace(/:$/, "");
      var found = "";
      Object.keys(aliases).some(function (key) {
        if (aliases[key].indexOf(label) >= 0) { found = key; return true; }
        return false;
      });
      return found;
    }
    function side(value) {
      var label = String(value || "").trim().toLowerCase();
      if (label === "buy" || label === "покупка") return "buy";
      if (label === "sell" || label === "продажа") return "sell";
      return "";
    }
    function entryType(value) {
      var label = String(value || "").trim().toLowerCase().replace(/\s/g, "");
      if (label === "in" || label === "вход") return "in";
      if (["out", "outby", "closeby", "выход"].indexOf(label) >= 0) return "out";
      return "";
    }
    var deals = [];
    Array.prototype.forEach.call(documentNode.querySelectorAll("table"), function (table) {
      var rows = Array.prototype.slice.call(table.querySelectorAll("tr"));
      var headerIndex = -1, columns = {};
      rows.some(function (tr, index) {
        var labels = Array.prototype.map.call(tr.querySelectorAll("th,td"), function (cell) {
          return cell.textContent.trim();
        });
        var mapped = {};
        labels.forEach(function (label, position) {
          var key = canonical(label);
          if (key) mapped[key] = position;
        });
        var required = ["time", "deal", "symbol", "type", "entry", "volume", "price"];
        if (required.every(function (key) { return mapped[key] != null; })) {
          headerIndex = index; columns = mapped; return true;
        }
        return false;
      });
      if (headerIndex < 0) return;
      rows.slice(headerIndex + 1).forEach(function (tr) {
        var cells = Array.prototype.map.call(tr.querySelectorAll("th,td"), function (cell) {
          return cell.textContent.trim();
        });
        function get(key) { return columns[key] == null ? "" : (cells[columns[key]] || ""); }
        var dealSide = side(get("type"));
        var dealEntry = entryType(get("entry"));
        var symbol = get("symbol").toUpperCase().replace(/[^A-Z0-9._-]/g, "");
        if (!dealSide || !dealEntry || !symbol) return;
        deals.push({
          ticket: get("deal"),
          timestamp: get("time"),
          symbol: symbol,
          side: dealSide,
          entry: dealEntry,
          volume: Math.abs(number(get("volume"))),
          price: number(get("price")),
          costs: number(get("commission")) + number(get("fee")) + number(get("swap")),
          profit: number(get("profit")),
          comment: get("comment"),
        });
      });
    });
    if (!deals.length) return [];
    deals.sort(function (a, b) { return a.timestamp.localeCompare(b.timestamp); });
    var open = {}, output = [], epsilon = 1e-9;
    deals.forEach(function (deal) {
      if (!open[deal.symbol]) open[deal.symbol] = [];
      var queue = open[deal.symbol];
      if (deal.entry === "in") {
        queue.push({ deal: deal, remaining: deal.volume, costs: deal.costs });
        return;
      }
      var closeRemaining = deal.volume;
      queue.forEach(function (lot) {
        if (closeRemaining <= epsilon || lot.deal.side === deal.side || lot.remaining <= epsilon) return;
        var matched = Math.min(closeRemaining, lot.remaining);
        var openRatio = matched / lot.remaining;
        var closeRatio = matched / deal.volume;
        var openCosts = lot.costs * openRatio;
        var result = openCosts + (deal.profit + deal.costs) * closeRatio;
        var openParts = lot.deal.timestamp.split(/\s+/);
        output.push({
          id: deal.ticket || lot.deal.ticket,
          date: (openParts[0] || "").replace(/\./g, "-"),
          time: (openParts[1] || "").slice(0, 5),
          pair: deal.symbol,
          direction: lot.deal.side === "buy" ? "long" : "short",
          entry_price: lot.deal.price,
          lot_size: matched,
          close_price: deal.price,
          close_time: deal.timestamp,
          result_usd: result,
          outcome: result > 0 ? "win" : result < 0 ? "loss" : "be",
          lesson: deal.comment || lot.deal.comment,
        });
        lot.remaining -= matched;
        lot.costs -= openCosts;
        closeRemaining -= matched;
      });
      open[deal.symbol] = queue.filter(function (lot) { return lot.remaining > epsilon; });
    });
    return output;
  }

  function first(row, names) {
    for (var i = 0; i < names.length; i++) {
      if (row[names[i]] != null && row[names[i]] !== "") return row[names[i]];
    }
    return "";
  }

  function number(value) {
    var text = String(value == null ? "" : value).trim().replace(/\s/g, "");
    if (text.indexOf(",") >= 0 && text.indexOf(".") < 0) text = text.replace(",", ".");
    var result = parseFloat(text);
    return isFinite(result) ? result : 0;
  }

  function normalizeOutcome(value, pnl) {
    var v = String(value || "").trim().toLowerCase();
    if (["win", "profit", "winner"].indexOf(v) >= 0) return "win";
    if (["loss", "lose", "loser"].indexOf(v) >= 0) return "loss";
    if (["be", "breakeven", "break-even"].indexOf(v) >= 0) return "be";
    if (["open", "opened"].indexOf(v) >= 0) return "open";
    return pnl > 0 ? "win" : pnl < 0 ? "loss" : "be";
  }

  function normalizeRules(value) {
    var v = String(value || "").trim().toLowerCase();
    if (["yes", "y", "true", "1", "да", "ha"].indexOf(v) >= 0) return "yes";
    if (["no", "n", "false", "0", "нет", "yo'q", "yoq"].indexOf(v) >= 0) return "no";
    return "";
  }

  function normalize(rows) {
    return rows.map(function (row, index) {
      var pnl = number(first(row, ["result_usd", "pnl", "profit", "profit_usd"]));
      var risk = number(first(row, ["risk_usd", "risk"]));
      var rawR = first(row, ["result_r", "r_result", "pnl_r"]);
      var date = first(row, ["date", "open_date"]);
      var time = first(row, ["time", "open_time"]);
      var hourMatch = String(time).match(/^(\d{1,2})/);
      var parsedDate = date ? new Date(date + "T12:00:00") : null;
      return {
        id: first(row, ["id", "ticket"]) || String(index + 1),
        date: date,
        time: time,
        timestamp: Date.parse(date + "T" + (time || "00:00")) || index,
        pair: first(row, ["pair", "symbol"]).toUpperCase().replace("/", ""),
        direction: first(row, ["direction", "dir", "type"]).toLowerCase(),
        setup: first(row, ["setup", "strategy"]),
        emotion: first(row, ["emotions", "emotion", "mood"]),
        hour: hourMatch ? Math.min(23, parseInt(hourMatch[1], 10)) : null,
        weekday: parsedDate && !isNaN(parsedDate.getTime()) ? (parsedDate.getDay() + 6) % 7 : null,
        pnl: pnl,
        risk: risk,
        r: rawR !== "" ? number(rawR) : (risk > 0 ? pnl / risk : 0),
        outcome: normalizeOutcome(first(row, ["outcome", "result"]), pnl),
        rules: normalizeRules(first(row, ["followed_rules", "rules"])),
      };
    }).filter(function (row) {
      return row.date || row.pair || row.pnl || row.outcome;
    }).sort(function (a, b) { return a.timestamp - b.timestamp; });
  }

  function setOptions() {
    var select = document.getElementById("journal-pair");
    var current = select.value;
    var pairs = {};
    state.rows.forEach(function (row) { if (row.pair) pairs[row.pair] = true; });
    select.innerHTML = '<option value="">' + T.all + "</option>";
    Object.keys(pairs).sort().forEach(function (pair) {
      var option = document.createElement("option");
      option.value = pair;
      option.textContent = pair.replace(/^(.{3})(.{3})$/, "$1/$2");
      select.appendChild(option);
    });
    select.value = current;
  }

  function filteredRows() {
    var from = document.getElementById("journal-from").value;
    var to = document.getElementById("journal-to").value;
    var pair = document.getElementById("journal-pair").value;
    var direction = document.getElementById("journal-direction").value;
    var rules = document.getElementById("journal-rules").value;
    return state.rows.filter(function (row) {
      return row.outcome !== "open" &&
        (!from || row.date >= from) &&
        (!to || row.date <= to) &&
        (!pair || row.pair === pair) &&
        (!direction || row.direction === direction) &&
        (!rules || row.rules === rules);
    });
  }

  function metrics(rows) {
    var wins = rows.filter(function (r) { return r.outcome === "win"; });
    var losses = rows.filter(function (r) { return r.outcome === "loss"; });
    var decisive = wins.length + losses.length;
    var grossWin = wins.reduce(function (s, r) { return s + Math.max(0, r.pnl); }, 0);
    var grossLoss = losses.reduce(function (s, r) { return s + Math.abs(Math.min(0, r.pnl)); }, 0);
    var pnl = rows.reduce(function (s, r) { return s + r.pnl; }, 0);
    var totalR = rows.reduce(function (s, r) { return s + r.r; }, 0);
    var equity = 0, peak = 0, maxDrawdown = 0;
    rows.forEach(function (r) {
      equity += r.pnl;
      peak = Math.max(peak, equity);
      maxDrawdown = Math.max(maxDrawdown, peak - equity);
    });
    var knownRules = rows.filter(function (r) { return r.rules; });
    var followed = knownRules.filter(function (r) { return r.rules === "yes"; });
    return {
      trades: rows.length,
      winRate: decisive ? wins.length / decisive * 100 : 0,
      pf: grossLoss ? grossWin / grossLoss : (grossWin ? Infinity : 0),
      pnl: pnl,
      totalR: totalR,
      maxDrawdown: maxDrawdown,
      discipline: knownRules.length ? followed.length / knownRules.length * 100 : 0,
    };
  }

  function setMetric(id, value, signed) {
    var el = document.getElementById(id);
    el.textContent = value;
    el.classList.remove("journal-positive", "journal-negative");
    if (signed > 0) el.classList.add("journal-positive");
    if (signed < 0) el.classList.add("journal-negative");
  }

  function drawChart(rows) {
    var canvas = document.getElementById("journal-equity");
    var width = Math.max(320, canvas.clientWidth || 800);
    var height = 260;
    var ratio = window.devicePixelRatio || 1;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    var ctx = canvas.getContext("2d");
    ctx.scale(ratio, ratio);
    ctx.clearRect(0, 0, width, height);
    if (!rows.length) return;
    var values = [0], total = 0;
    rows.forEach(function (row) { total += row.pnl; values.push(total); });
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
    if (min === max) { min -= 1; max += 1; }
    var pad = 24;
    function x(i) { return pad + i * (width - pad * 2) / Math.max(1, values.length - 1); }
    function y(v) { return pad + (max - v) * (height - pad * 2) / (max - min); }
    ctx.strokeStyle = "rgba(148,163,184,.45)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(pad, y(0)); ctx.lineTo(width - pad, y(0)); ctx.stroke();
    ctx.setLineDash([]);
    ctx.strokeStyle = total >= 0 ? "#22c55e" : "#ef4444";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    values.forEach(function (v, i) { if (i) ctx.lineTo(x(i), y(v)); else ctx.moveTo(x(i), y(v)); });
    ctx.stroke();
  }

  function ruleStats(rows, rule) {
    var subset = rows.filter(function (r) { return r.rules === rule; });
    var m = metrics(subset);
    return '<strong>' + (rule === "yes" ? T.following : T.violating) + "</strong>" +
      '<span>' + m.trades + " " + T.n + " · " + T.wr + " " + F.pct(m.winRate, 1) +
      " · " + F.money(m.pnl) + " · " + m.totalR.toFixed(2) + "R</span>";
  }

  function renderTable(rows) {
    var body = document.getElementById("journal-table-body");
    body.innerHTML = "";
    if (!rows.length) {
      body.innerHTML = '<tr><td colspan="8" class="journal-empty">' + T.tableEmpty + "</td></tr>";
      return;
    }
    rows.slice().reverse().slice(0, 30).forEach(function (row) {
      var tr = document.createElement("tr");
      [row.date, row.time, row.pair.replace(/^(.{3})(.{3})$/, "$1/$2"),
        row.direction, row.setup || "—", row.outcome,
        F.money(row.pnl), row.r.toFixed(2) + "R"].forEach(function (value, index) {
        var td = document.createElement("td");
        td.textContent = value || "—";
        if (index === 6 || index === 7) {
          if (row.pnl > 0) td.className = "journal-positive";
          if (row.pnl < 0) td.className = "journal-negative";
        }
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
  }

  function groupRows(rows, field) {
    var groups = {};
    rows.forEach(function (row) {
      var key = String(row[field] || T.unknown).trim() || T.unknown;
      if (!groups[key]) groups[key] = [];
      groups[key].push(row);
    });
    return Object.keys(groups).map(function (label) {
      return { label: label, rows: groups[label], metrics: metrics(groups[label]) };
    }).sort(function (a, b) {
      return b.rows.length - a.rows.length || b.metrics.totalR - a.metrics.totalR;
    });
  }

  function renderBreakdown(id, groups) {
    var body = document.getElementById(id);
    body.innerHTML = "";
    groups.slice(0, 12).forEach(function (group) {
      var tr = document.createElement("tr");
      var values = [group.label, group.metrics.trades, F.pct(group.metrics.winRate, 1),
        F.money(group.metrics.pnl), group.metrics.totalR.toFixed(2) + "R"];
      values.forEach(function (value, index) {
        var td = document.createElement("td");
        td.textContent = value;
        if (index >= 3) {
          var signed = index === 3 ? group.metrics.pnl : group.metrics.totalR;
          if (signed > 0) td.className = "journal-positive";
          if (signed < 0) td.className = "journal-negative";
        }
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
  }

  function renderHeatmap(rows) {
    var grid = document.getElementById("journal-heatmap");
    grid.innerHTML = "";
    var values = {}, maxAbs = 0;
    rows.forEach(function (row) {
      if (row.weekday == null || row.hour == null) return;
      var key = row.weekday + "-" + row.hour;
      if (!values[key]) values[key] = { r: 0, count: 0 };
      values[key].r += row.r;
      values[key].count++;
      maxAbs = Math.max(maxAbs, Math.abs(values[key].r));
    });
    var corner = document.createElement("span");
    corner.className = "journal-heatmap-label";
    grid.appendChild(corner);
    for (var hour = 0; hour < 24; hour++) {
      var hourLabel = document.createElement("span");
      hourLabel.className = "journal-heatmap-hour";
      hourLabel.textContent = hour < 10 ? "0" + hour : String(hour);
      grid.appendChild(hourLabel);
    }
    T.weekdays.forEach(function (day, dayIndex) {
      var dayLabel = document.createElement("strong");
      dayLabel.className = "journal-heatmap-label";
      dayLabel.textContent = day;
      grid.appendChild(dayLabel);
      for (var h = 0; h < 24; h++) {
        var item = values[dayIndex + "-" + h];
        var cell = document.createElement("span");
        cell.className = "journal-heatmap-cell";
        if (item) {
          cell.classList.add(item.r >= 0 ? "is-positive" : "is-negative");
          cell.style.opacity = String(0.3 + 0.7 * Math.abs(item.r) / Math.max(maxAbs, 0.01));
          cell.textContent = item.count;
          cell.title = day + " " + (h < 10 ? "0" + h : h) + ":00 · " +
            item.r.toFixed(2) + "R · " + item.count + " " + T.n;
        }
        grid.appendChild(cell);
      }
    });
  }

  function renderInsights(rows) {
    var list = document.getElementById("journal-insights-list");
    list.innerHTML = "";
    if (!rows.length) return;
    var result = [];
    var m = metrics(rows);
    if (rows.length < 30) result.push(T.insightSample(rows.length));
    result.push(T.insightExpectancy((m.totalR / rows.length).toFixed(2)));
    var evening = rows.filter(function (row) { return row.hour != null && row.hour >= 18; });
    var eveningM = metrics(evening);
    if (evening.length >= 3 && eveningM.totalR < 0) {
      result.push(T.insightEvening(evening.length, eveningM.totalR.toFixed(2)));
    }
    var violations = rows.filter(function (row) { return row.rules === "no"; });
    var violationM = metrics(violations);
    if (violations.length >= 2 && violationM.totalR < 0) {
      result.push(T.insightRules(violations.length, violationM.totalR.toFixed(2)));
    }
    var pairGroups = groupRows(rows, "pair").filter(function (group) {
      return group.rows.length >= 2;
    });
    if (pairGroups.length) {
      var ranked = pairGroups.slice().sort(function (a, b) {
        return a.metrics.totalR - b.metrics.totalR;
      });
      if (ranked[0].metrics.totalR < 0) {
        result.push(T.insightWorst(ranked[0].label, ranked[0].metrics.totalR.toFixed(2)));
      }
      var best = ranked[ranked.length - 1];
      if (best.metrics.totalR > 0) {
        result.push(T.insightBest(best.label, best.metrics.totalR.toFixed(2)));
      }
    }
    if (m.discipline < 95) result.push(T.insightDiscipline(m.discipline.toFixed(1)));
    result.slice(0, 5).forEach(function (message) {
      var li = document.createElement("li");
      li.textContent = message;
      list.appendChild(li);
    });
  }

  function summaryRows(rows) {
    var output = [["section", "group", "trades", "win_rate", "pnl", "total_r"]];
    var overall = metrics(rows);
    output.push(["overall", "all", overall.trades, overall.winRate.toFixed(1),
      overall.pnl.toFixed(2), overall.totalR.toFixed(2)]);
    [["pair", "pair"], ["setup", "setup"], ["direction", "direction"],
      ["emotion", "emotion"]].forEach(function (entry) {
      groupRows(rows, entry[1]).forEach(function (group) {
        output.push([entry[0], group.label, group.metrics.trades,
          group.metrics.winRate.toFixed(1), group.metrics.pnl.toFixed(2),
          group.metrics.totalR.toFixed(2)]);
      });
    });
    return output;
  }

  function csvCell(value) {
    var text = String(value == null ? "" : value);
    return /[",\n]/.test(text) ? '"' + text.replace(/"/g, '""') + '"' : text;
  }

  function download(name, content, type) {
    var blob = new Blob([content], { type: type });
    var link = document.createElement("a");
    var url = URL.createObjectURL(blob);
    link.href = url;
    link.download = name;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 0);
    status.textContent = T.exportReady;
  }

  function exportCsv() {
    var csv = summaryRows(filteredRows()).map(function (row) {
      return row.map(csvCell).join(",");
    }).join("\n");
    download("forex-journal-summary.csv", csv, "text/csv;charset=utf-8");
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function exportHtml() {
    var rows = summaryRows(filteredRows());
    var body = rows.slice(1).map(function (row) {
      return "<tr>" + row.map(function (value) {
        return "<td>" + escapeHtml(value) + "</td>";
      }).join("") + "</tr>";
    }).join("");
    var head = rows[0].map(function (value) {
      return "<th>" + escapeHtml(value) + "</th>";
    }).join("");
    var html = '<!doctype html><meta charset="utf-8"><title>Forex journal summary</title>' +
      "<style>body{font:15px system-ui;max-width:1000px;margin:40px auto;padding:0 20px}" +
      "table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:8px;text-align:left}" +
      "th{background:#f3f4f6}</style><h1>Forex journal summary</h1><p>" +
      escapeHtml(new Date().toLocaleString()) + "</p><table><thead><tr>" + head +
      "</tr></thead><tbody>" + body + "</tbody></table>";
    download("forex-journal-summary.html", html, "text/html;charset=utf-8");
  }

  function render() {
    var rows = filteredRows();
    var m = metrics(rows);
    setMetric("journal-m-trades", String(m.trades), 0);
    setMetric("journal-m-winrate", F.pct(m.winRate, 1), m.winRate - 40);
    setMetric("journal-m-pf", isFinite(m.pf) ? m.pf.toFixed(2) : "∞", m.pf - 1);
    setMetric("journal-m-pnl", F.money(m.pnl), m.pnl);
    setMetric("journal-m-r", m.totalR.toFixed(2) + "R", m.totalR);
    setMetric("journal-m-dd", F.money(m.maxDrawdown), -m.maxDrawdown);
    setMetric("journal-m-discipline", F.pct(m.discipline, 1), m.discipline - 95);
    document.getElementById("journal-m-filtered").textContent = rows.length + " / " + state.rows.length;
    document.getElementById("journal-rules-yes").innerHTML = ruleStats(rows, "yes");
    document.getElementById("journal-rules-no").innerHTML = ruleStats(rows, "no");
    document.getElementById("journal-empty").style.display = rows.length ? "none" : "block";
    document.getElementById("journal-empty").textContent = T.noRows;
    try {
      localStorage.setItem("forex_journal_summary", JSON.stringify({
        trades: m.trades, winRate: m.winRate, pnl: m.pnl, totalR: m.totalR,
        maxDrawdown: m.maxDrawdown, discipline: m.discipline,
        updated: new Date().toISOString().slice(0, 10)
      }));
    } catch (e) {}
    drawChart(rows);
    renderHeatmap(rows);
    renderBreakdown("journal-by-pair", groupRows(rows, "pair"));
    renderBreakdown("journal-by-setup", groupRows(rows, "setup"));
    renderBreakdown("journal-by-direction", groupRows(rows, "direction"));
    renderBreakdown("journal-by-emotion", groupRows(rows, "emotion"));
    renderInsights(rows);
    renderTable(rows);
  }

  function saveSource(text, name, kind) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        text: text,
        name: name,
        savedAt: new Date().toISOString(),
        kind: kind
      }));
      status.textContent = T.saved;
    } catch (e) {}
  }

  function loadText(text, name, persist, kind) {
    try {
      var isMT5 = kind === "mt5" || /^\s*(?:<!doctype\s+html|<html|<table)/i.test(String(text));
      var raw = isMT5 ? parseMT5HTML(text) : parseCSV(text);
      var rows = normalize(raw);
      if (!rows.length) throw new Error("empty");
      state.rows = rows;
      state.sourceText = String(text);
      state.sourceName = name;
      error.style.display = "none";
      dashboard.style.display = "block";
      fileName.textContent = T.fileReady(name, rows.length);
      setOptions();
      render();
      if (persist !== false) saveSource(String(text), name, isMT5 ? "mt5" : "csv");
      if (persist !== false && window.fxTrack) {
        window.fxTrack(name === T.demo ? "journal_demo_opened" : "journal_import_completed");
      }
    } catch (e) {
      dashboard.style.display = "none";
      error.textContent = T.invalid;
      error.style.display = "block";
    }
  }

  function readFile(file) {
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () {
      var isMT5 = /\.(?:html?|xls)$/i.test(file.name);
      loadText(reader.result, file.name, true, isMT5 ? "mt5" : "csv");
    };
    reader.onerror = function () {
      error.textContent = T.invalid;
      error.style.display = "block";
    };
    reader.readAsText(file);
  }

  fileInput.addEventListener("change", function () { readFile(fileInput.files[0]); });
  drop.addEventListener("dragover", function (event) {
    event.preventDefault(); drop.classList.add("is-dragging");
  });
  drop.addEventListener("dragleave", function () { drop.classList.remove("is-dragging"); });
  drop.addEventListener("drop", function (event) {
    event.preventDefault(); drop.classList.remove("is-dragging");
    readFile(event.dataTransfer.files[0]);
  });
  demoButton.addEventListener("click", function () {
    loadText(document.getElementById("journal-demo-data").textContent, T.demo, true, "csv");
  });
  document.getElementById("journal-clear").addEventListener("click", function () {
    try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
    state = { rows: [], sourceText: "", sourceName: "" };
    dashboard.style.display = "none";
    fileInput.value = "";
    fileName.textContent = T.noFile;
    status.textContent = T.cleared;
  });
  document.getElementById("journal-export-csv").addEventListener("click", exportCsv);
  document.getElementById("journal-export-html").addEventListener("click", exportHtml);
  filters.forEach(function (id) {
    document.getElementById(id).addEventListener("change", render);
  });
  window.addEventListener("resize", function () {
    if (dashboard.style.display !== "none") drawChart(filteredRows());
  });
  try {
    var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if (saved && saved.text) {
      loadText(saved.text, saved.name || T.restoredName, false, saved.kind);
      status.textContent = T.restored + ": " + (saved.name || T.restoredName);
    }
  } catch (e) {}
})();
