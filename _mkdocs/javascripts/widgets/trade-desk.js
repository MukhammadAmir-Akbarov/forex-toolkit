(function () {
  "use strict";

  var root = document.getElementById("trade-desk-widget");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var STORAGE_KEY = "forex_trade_drafts_v1";
  var SETTINGS_KEY = "forex_tool_settings_v1";
  var T = F.pick({
    ru: {
      balance: "Депозит, USD", risk: "Риск, %", pair: "Пара", direction: "Направление",
      stop: "Стоп, пипсы", pip: "USD/пипс на 1 лот", rate: "USD -> UZS", setup: "Сетап",
      notes: "Первоначальная причина входа", calculate: "1. Рассчитать", checks: "2. Проверить план",
      save: "3. Добавить план", journal: "Открыть план в журнале", download: "Скачать CSV",
      riskAmount: "Риск", lot: "Размер позиции", all: "Отметь все пункты перед сохранением.",
      saved: "План сохранён со статусом «План». Теперь его можно открыть в журнале.",
      checklist: ["Сетап соответствует торговому плану", "Стоп определён до входа", "Нет важной новости рядом со входом", "Совокупный риск остаётся в лимите", "Принимаю полный убыток без переноса стопа"]
    },
    en: {
      balance: "Balance, USD", risk: "Risk, %", pair: "Pair", direction: "Direction",
      stop: "Stop, pips", pip: "USD/pip per lot", rate: "USD -> UZS", setup: "Setup",
      notes: "Original entry reason", calculate: "1. Calculate", checks: "2. Verify the plan",
      save: "3. Add plan", journal: "Open plan in journal", download: "Download CSV",
      riskAmount: "Risk", lot: "Position size", all: "Check every item before saving.",
      saved: "Saved with Plan status. You can now open it in the journal.",
      checklist: ["Setup matches the trading plan", "Stop is defined before entry", "No major news near the entry", "Aggregate risk remains within the limit", "I accept the full loss without moving the stop"]
    },
    uz: {
      balance: "Depozit, USD", risk: "Risk, %", pair: "Juftlik", direction: "Yo'nalish",
      stop: "Stop, pip", pip: "1 lot uchun USD/pip", rate: "USD -> UZS", setup: "Setap",
      notes: "Kirishning dastlabki sababi", calculate: "1. Hisoblash", checks: "2. Rejani tekshirish",
      save: "3. Rejani qo'shish", journal: "Rejani jurnalda ochish", download: "CSV yuklash",
      riskAmount: "Risk", lot: "Pozitsiya hajmi", all: "Saqlashdan oldin barcha bandlarni belgilang.",
      saved: "Reja «Plan» holatida saqlandi. Uni endi jurnalda ochish mumkin.",
      checklist: ["Setap savdo rejasiga mos", "Stop kirishdan oldin belgilangan", "Kirish yaqinida muhim yangilik yo'q", "Umumiy risk limit ichida", "Stopni ko'chirmasdan to'liq zararni qabul qilaman"]
    }
  });

  root.innerHTML = [
    '<div class="fx-tool-grid">',
    field(T.balance, '<input id="td-balance" type="number" min="1" value="1000">'),
    field(T.risk, '<input id="td-risk" type="number" min="0.1" max="10" step="0.1" value="1">'),
    field(T.pair, '<input id="td-pair" value="EURUSD" maxlength="7">'),
    field(T.direction, '<select id="td-direction"><option value="long">Long</option><option value="short">Short</option></select>'),
    field(T.stop, '<input id="td-stop" type="number" min="0.1" value="20">'),
    field(T.pip, '<input id="td-pip" type="number" min="0.01" step="0.01" value="10">'),
    field(T.rate, '<input id="td-rate" type="number" min="1" value="12500">'),
    field(T.setup, '<input id="td-setup" value="pullback">'),
    '</div>',
    field(T.notes, '<textarea id="td-notes" rows="3"></textarea>'),
    '<div class="fx-tool-actions"><button type="button" id="td-calc">' + T.calculate + '</button></div>',
    '<div id="td-result" class="fx-result" hidden></div>',
    '<h3>' + T.checks + '</h3>',
    '<div id="td-checks" class="fx-checks">',
    T.checklist.map(function (item, index) {
      return '<label><input type="checkbox" data-check="' + index + '"> <span>' + item + '</span></label>';
    }).join(""),
    '</div>',
    '<div class="fx-tool-actions">',
    '<button type="button" id="td-save">' + T.save + '</button>',
    '<button type="button" id="td-journal" class="fx-secondary" disabled>' + T.journal + '</button>',
    '<button type="button" id="td-download" class="fx-secondary" disabled>' + T.download + '</button>',
    '</div>',
    '<p id="td-status" class="fx-tool-note" aria-live="polite"></p>'
  ].join("");

  var current = null;

  function field(label, control) {
    return '<label><span>' + label + '</span>' + control + '</label>';
  }

  function value(id) {
    return Number(document.getElementById(id).value);
  }

  function uid() {
    if (window.crypto && typeof window.crypto.randomUUID === "function") return window.crypto.randomUUID();
    return "plan-" + Date.now() + "-" + Math.random().toString(16).slice(2);
  }

  function localDate(date) {
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, "0");
    var day = String(date.getDate()).padStart(2, "0");
    return year + "-" + month + "-" + day;
  }

  function calculate() {
    var balance = value("td-balance");
    var riskPct = value("td-risk");
    var stop = value("td-stop");
    var pip = value("td-pip");
    var rate = value("td-rate");
    if (!(balance > 0 && riskPct > 0 && stop > 0 && pip > 0 && rate > 0)) return;

    var risk = balance * riskPct / 100;
    var lot = Math.floor(risk / (stop * pip) * 100) / 100;
    var now = new Date();
    current = {
      id: uid(),
      version: 2,
      status: "plan",
      date: localDate(now),
      created_at: now.toISOString(),
      updated_at: now.toISOString(),
      pair: document.getElementById("td-pair").value.toUpperCase().replace("/", "").trim(),
      direction: document.getElementById("td-direction").value,
      lot_size: lot,
      risk_usd: risk,
      risk_pct: riskPct,
      stop_pips: stop,
      usd_uzs: rate,
      setup: document.getElementById("td-setup").value.trim(),
      planned_reason: document.getElementById("td-notes").value.trim()
    };

    var result = document.getElementById("td-result");
    result.innerHTML = '<div class="fx-metrics"><div><span>' + T.riskAmount + '</span><strong>' +
      F.money(risk) + ' / ' + Math.round(risk * rate).toLocaleString(F.numLocale) +
      ' UZS</strong></div><div><span>' + T.lot + '</span><strong>' + lot.toFixed(2) +
      ' lot</strong></div></div>';
    result.hidden = false;
  }

  function allChecked() {
    return Array.prototype.every.call(document.querySelectorAll("#td-checks input"), function (input) {
      return input.checked;
    });
  }

  function readArray(key) {
    try {
      var value = JSON.parse(localStorage.getItem(key) || "[]");
      return Array.isArray(value) ? value : [];
    } catch (error) {
      return [];
    }
  }

  function saveSettings() {
    try {
      var settings = JSON.parse(localStorage.getItem(SETTINGS_KEY) || "{}");
      settings.tradeDesk = {
        balance: value("td-balance"), riskPct: value("td-risk"), pipValue: value("td-pip"),
        usdUzs: value("td-rate"), updatedAt: new Date().toISOString()
      };
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
    } catch (error) {}
  }

  function markFirst15() {
    try {
      var progress = JSON.parse(localStorage.getItem("forex_first15_v1") || "{}");
      progress.plan = true;
      progress.updatedAt = new Date().toISOString();
      localStorage.setItem("forex_first15_v1", JSON.stringify(progress));
    } catch (error) {}
  }

  function save() {
    if (!current) calculate();
    if (!current || !allChecked()) {
      document.getElementById("td-status").textContent = T.all;
      return;
    }
    var drafts = readArray(STORAGE_KEY).filter(function (item) { return item.id !== current.id; });
    drafts.unshift(current);
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(drafts.slice(0, 100))); } catch (error) {}
    saveSettings();
    markFirst15();
    document.getElementById("td-status").textContent = T.saved;
    document.getElementById("td-journal").disabled = false;
    document.getElementById("td-download").disabled = false;
    if (window.fxTrack) window.fxTrack("trade_plan_saved", { once: false });
  }

  function csvCell(value) {
    var text = String(value == null ? "" : value);
    return /[",\n]/.test(text) ? '"' + text.replace(/"/g, '""') + '"' : text;
  }

  function download() {
    if (!current) return;
    var headers = ["id", "date", "pair", "direction", "lot_size", "risk_usd", "outcome", "followed_rules", "setup", "notes"];
    var row = [current.id, current.date, current.pair, current.direction, current.lot_size, current.risk_usd, "open", "yes", current.setup, current.planned_reason];
    var blob = new Blob([headers.join(",") + "\n" + row.map(csvCell).join(",") + "\n"], { type: "text/csv;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "trade-plan-" + current.date + ".csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  document.getElementById("td-calc").addEventListener("click", calculate);
  document.getElementById("td-save").addEventListener("click", save);
  document.getElementById("td-journal").addEventListener("click", function () {
    window.location.href = "../../journal/web-journal/?plans=1";
  });
  document.getElementById("td-download").addEventListener("click", download);
})();
