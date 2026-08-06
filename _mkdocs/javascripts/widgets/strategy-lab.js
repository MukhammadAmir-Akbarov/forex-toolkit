(function () {
  "use strict";

  var root = document.getElementById("strategy-lab-widget");
  var KEY = "forex_strategy_playbooks_v1";

  function read() {
    try {
      var value = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(value) ? value : [];
    } catch (error) { return []; }
  }

  function write(items) {
    try { localStorage.setItem(KEY, JSON.stringify(items.slice(0, 50))); } catch (error) {}
  }

  function snapshot(item) {
    return {
      id: item.id, baseId: item.baseId, name: item.name, version: item.version,
      session: item.session, timeframe: item.timeframe, entryRules: item.entryRules,
      invalidation: item.invalidation, maxRiskPct: item.maxRiskPct,
      targetTrades: item.targetTrades
    };
  }

  window.FXStrategies = { key: KEY, read: read, snapshot: snapshot };
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var escapeHtml = F.escape;
  var T = F.pick({
    ru: {
      title: "Лаборатория стратегии", intro: "Зафиксируй правила до серии сделок. Изменение создаёт новую версию, поэтому статистика не смешивается.",
      name: "Название", session: "Сессия", timeframe: "Таймфрейм", entry: "Условия входа",
      invalidation: "Когда вход отменяется", risk: "Макс. риск, %", target: "Цель, сделок",
      save: "Сохранить новую версию", load: "Взять за основу", empty: "Стратегий пока нет.",
      required: "Заполни название, условия входа и отмены.", saved: "Сохранена версия",
      duplicate: "Такая версия уже существует.", active: "активная", archived: "архив",
      progress: "Прогресс", expectancy: "Expectancy", discipline: "Дисциплина", drawdown: "Просадка", result: "Результат"
    },
    en: {
      title: "Strategy lab", intro: "Freeze the rules before a trade sample. Any change creates a new version, so results are not mixed.",
      name: "Name", session: "Session", timeframe: "Timeframe", entry: "Entry conditions",
      invalidation: "Entry invalidation", risk: "Max risk, %", target: "Target trades",
      save: "Save new version", load: "Use as a base", empty: "No strategies yet.",
      required: "Enter a name, entry conditions and invalidation.", saved: "Saved version",
      duplicate: "This exact version already exists.", active: "active", archived: "archived",
      progress: "Progress", expectancy: "Expectancy", discipline: "Discipline", drawdown: "Drawdown", result: "Result"
    },
    uz: {
      title: "Strategiya laboratoriyasi", intro: "Savdolar seriyasidan oldin qoidalarni belgilang. Har bir o'zgarish yangi versiya yaratadi.",
      name: "Nomi", session: "Sessiya", timeframe: "Taymfreym", entry: "Kirish shartlari",
      invalidation: "Kirish qachon bekor qilinadi", risk: "Maks. risk, %", target: "Savdo maqsadi",
      save: "Yangi versiyani saqlash", load: "Asos sifatida olish", empty: "Strategiya hozircha yo'q.",
      required: "Nom, kirish shartlari va bekor qilish shartini kiriting.", saved: "Versiya saqlandi",
      duplicate: "Xuddi shu versiya mavjud.", active: "faol", archived: "arxiv",
      progress: "Jarayon", expectancy: "Expectancy", discipline: "Intizom", drawdown: "Pasayish", result: "Natija"
    }
  });

  root.innerHTML = '<div class="strategy-lab__head"><h2>' + T.title + '</h2><p>' + T.intro + '</p></div>' +
    '<div class="strategy-lab__grid">' +
    field(T.name, '<input id="sl-name" maxlength="80">') +
    field(T.session, '<select id="sl-session"><option>London</option><option>New York</option><option>Asian</option><option>Overlap</option></select>') +
    field(T.timeframe, '<select id="sl-timeframe"><option>M15</option><option>H1</option><option>H4</option><option>D1</option></select>') +
    field(T.risk, '<input id="sl-risk" type="number" min="0.1" max="10" step="0.1" value="0.5">') +
    field(T.target, '<input id="sl-target" type="number" min="5" max="500" step="5" value="30">') + '</div>' +
    field(T.entry, '<textarea id="sl-entry" rows="3"></textarea>') +
    field(T.invalidation, '<textarea id="sl-invalidation" rows="2"></textarea>') +
    '<div class="fx-tool-actions"><button type="button" id="sl-save">' + T.save + '</button></div>' +
    '<p id="sl-status" class="fx-tool-note" aria-live="polite"></p><div id="sl-list"></div>';

  function field(label, control) { return '<label><span>' + label + '</span>' + control + '</label>'; }
  function value(id) { return document.getElementById(id).value.trim(); }
  function uid(name) { return name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 30) || "strategy"; }
  function comparable(item) {
    return [item.name, item.session, item.timeframe, item.entryRules, item.invalidation,
      Number(item.maxRiskPct), Number(item.targetTrades)].join("|").toLowerCase();
  }

  function tradeStats(strategy) {
    var plans = [];
    try { plans = JSON.parse(localStorage.getItem("forex_trade_drafts_v1") || "[]"); } catch (error) {}
    var rows = plans.filter(function (plan) {
      return plan.status === "closed" && plan.strategy && plan.strategy.id === strategy.id;
    }).map(function (plan) {
      var risk = Number(plan.risk_usd);
      var net = Number(plan.result_usd) - Math.abs(Number(plan.commission_usd) || 0);
      return { r: risk > 0 ? net / risk : 0, valid: risk > 0, rules: plan.followed_rules };
    });
    var valid = rows.filter(function (row) { return row.valid; });
    var equity = 0, peak = 0, drawdown = 0;
    valid.forEach(function (row) { equity += row.r; peak = Math.max(peak, equity); drawdown = Math.max(drawdown, peak - equity); });
    var followed = rows.filter(function (row) { return row.rules === true; }).length;
    var answered = rows.filter(function (row) { return row.rules === true || row.rules === false; }).length;
    var totalR = valid.reduce(function (sum, row) { return sum + row.r; }, 0);
    return { count: rows.length, totalR: totalR, expectancy: valid.length ? totalR / valid.length : 0,
      discipline: answered ? followed / answered * 100 : 0, drawdown: drawdown };
  }

  function render() {
    var items = read().sort(function (a, b) { return b.createdAt.localeCompare(a.createdAt); });
    var list = document.getElementById("sl-list");
    if (!items.length) { list.innerHTML = '<p>' + T.empty + '</p>'; return; }
    list.innerHTML = '<div class="strategy-lab__list">' + items.map(function (item) {
      var stats = tradeStats(item);
      var full = stats.count >= item.targetTrades;
      return '<article class="strategy-card ' + (item.active ? "is-active" : "") + '" data-id="' + escapeHtml(item.id) + '">' +
        '<div class="strategy-card__head"><strong>' + escapeHtml(item.name) + ' v' + item.version + '</strong><span>' +
        (item.active ? T.active : T.archived) + '</span></div><p>' + escapeHtml(item.session + " · " + item.timeframe) +
        ' · ≤' + Number(item.maxRiskPct).toFixed(1) + '%</p><p>' + escapeHtml(item.entryRules) + '</p>' +
        '<div class="strategy-card__progress"><span>' + T.progress + ': ' + stats.count + ' / ' + item.targetTrades + '</span>' +
        '<progress max="' + item.targetTrades + '" value="' + Math.min(stats.count, item.targetTrades) + '"></progress></div>' +
        (full ? '<div class="strategy-card__metrics"><span>' + T.expectancy + ': ' + stats.expectancy.toFixed(2) +
        'R</span><span>' + T.discipline + ': ' + stats.discipline.toFixed(1) + '%</span><span>' + T.drawdown + ': ' +
        stats.drawdown.toFixed(2) + 'R</span><span>' + T.result + ': ' + stats.totalR.toFixed(2) + 'R</span></div>' : '') +
        '<button class="journal-button secondary" type="button" data-load="' + escapeHtml(item.id) + '">' + T.load + '</button></article>';
    }).join("") + '</div>';
  }

  function save() {
    var candidate = { name: value("sl-name"), session: value("sl-session"), timeframe: value("sl-timeframe"),
      entryRules: value("sl-entry"), invalidation: value("sl-invalidation"), maxRiskPct: Number(value("sl-risk")),
      targetTrades: Math.max(5, Number(value("sl-target")) || 30) };
    if (!candidate.name || !candidate.entryRules || !candidate.invalidation || !(candidate.maxRiskPct > 0)) {
      document.getElementById("sl-status").textContent = T.required; return;
    }
    var items = read();
    var sameName = items.filter(function (item) { return item.name.toLowerCase() === candidate.name.toLowerCase(); });
    if (sameName.some(function (item) { return comparable(item) === comparable(candidate); })) {
      document.getElementById("sl-status").textContent = T.duplicate; return;
    }
    var version = sameName.reduce(function (max, item) { return Math.max(max, item.version); }, 0) + 1;
    var baseId = sameName.length ? sameName[0].baseId : uid(candidate.name) + "-" + Date.now();
    items.forEach(function (item) { if (item.baseId === baseId) item.active = false; });
    var item = Object.assign(candidate, { id: baseId + "-v" + version, baseId: baseId, version: version,
      active: true, createdAt: new Date().toISOString() });
    items.unshift(item); write(items);
    document.getElementById("sl-status").textContent = T.saved + " " + version + ".";
    render(); window.dispatchEvent(new CustomEvent("fx:strategies-updated"));
    if (window.fxTrack) window.fxTrack("strategy_version_saved", { once: false });
  }

  document.getElementById("sl-save").addEventListener("click", save);
  document.getElementById("sl-list").addEventListener("click", function (event) {
    var button = event.target.closest("button[data-load]");
    if (!button) return;
    var item = read().find(function (strategy) { return strategy.id === button.dataset.load; });
    if (!item) return;
    document.getElementById("sl-name").value = item.name;
    document.getElementById("sl-session").value = item.session;
    document.getElementById("sl-timeframe").value = item.timeframe;
    document.getElementById("sl-entry").value = item.entryRules;
    document.getElementById("sl-invalidation").value = item.invalidation;
    document.getElementById("sl-risk").value = item.maxRiskPct;
    document.getElementById("sl-target").value = item.targetTrades;
    root.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  render();
})();
