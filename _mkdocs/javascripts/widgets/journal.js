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
      invalid: "Не удалось прочитать CSV. Проверь заголовки и формат файла.",
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
    },
    en: {
      fileReady: function (name, count) { return name + ": " + count + " rows loaded"; },
      demo: "Demo journal",
      invalid: "Could not read the CSV. Check its headers and format.",
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
    },
    uz: {
      fileReady: function (name, count) { return name + ": " + count + " qator yuklandi"; },
      demo: "Demo jurnal",
      invalid: "CSV faylni o'qib bo'lmadi. Sarlavha va formatni tekshiring.",
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
    },
  });

  var state = { rows: [] };
  var fileInput = document.getElementById("journal-file");
  var drop = document.getElementById("journal-drop");
  var demoButton = document.getElementById("journal-demo");
  var error = document.getElementById("journal-error");
  var dashboard = document.getElementById("journal-dashboard");
  var fileName = document.getElementById("journal-file-name");
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
      return {
        id: first(row, ["id", "ticket"]) || String(index + 1),
        date: date,
        time: time,
        timestamp: Date.parse(date + "T" + (time || "00:00")) || index,
        pair: first(row, ["pair", "symbol"]).toUpperCase().replace("/", ""),
        direction: first(row, ["direction", "dir", "type"]).toLowerCase(),
        setup: first(row, ["setup", "strategy"]),
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
    drawChart(rows);
    renderTable(rows);
  }

  function loadText(text, name) {
    try {
      var raw = parseCSV(text);
      var rows = normalize(raw);
      if (!rows.length) throw new Error("empty");
      state.rows = rows;
      error.style.display = "none";
      dashboard.style.display = "block";
      fileName.textContent = T.fileReady(name, rows.length);
      setOptions();
      render();
    } catch (e) {
      dashboard.style.display = "none";
      error.textContent = T.invalid;
      error.style.display = "block";
    }
  }

  function readFile(file) {
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () { loadText(reader.result, file.name); };
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
    loadText(document.getElementById("journal-demo-data").textContent, T.demo);
  });
  filters.forEach(function (id) {
    document.getElementById(id).addEventListener("change", render);
  });
  window.addEventListener("resize", function () {
    if (dashboard.style.display !== "none") drawChart(filteredRows());
  });
})();
