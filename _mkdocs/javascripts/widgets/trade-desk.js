(function () {
  "use strict";

  var root = document.getElementById("trade-desk-widget");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var STORAGE_KEY = "forex_trade_drafts_v1";
  var SETTINGS_KEY = "forex_tool_settings_v1";
  var HISTORY_KEY = "forex_journal_risk_history_v1";
  var T = F.pick({
    ru: {
      balance: "Депозит, USD", risk: "Риск, %", pair: "Пара", direction: "Направление",
      stop: "Стоп, пипсы", pip: "USD/пипс на 1 лот", rate: "USD -> UZS", setup: "Сетап",
      strategy: "Версия стратегии", manualStrategy: "Без сохранённой стратегии",
      notes: "Первоначальная причина входа", calculate: "1. Рассчитать", checks: "2. Проверить план",
      save: "3. Добавить план", journal: "Открыть план в журнале", download: "Скачать CSV",
      riskAmount: "Риск", lot: "Размер позиции", all: "Отметь все пункты перед сохранением.",
      saved: "План сохранён со статусом «План». Теперь его можно открыть в журнале.",
      checklist: ["Сетап соответствует торговому плану", "Стоп определён до входа", "Нет важной новости рядом со входом", "Принимаю полный убыток без переноса стопа"],
      budgetTitle: "Автоматический риск-бюджет", budgetSettings: "Настройки лимитов",
      maxOpen: "Макс. одновременный риск, %", dailyLimit: "Дневной лимит, R",
      weeklyLimit: "Недельный лимит, R", pauseAfter: "Пауза после убытков",
      plannedRisk: "Запланировано", openRisk: "Открыто", afterRisk: "После новой сделки",
      todayR: "Сегодня", weekR: "Эта неделя", remaining: "Остаток",
      lossStreak: "Серия убытков", budgetOk: "Лимиты соблюдены.",
      budgetWarn: "Один или несколько лимитов превышены. Сделай паузу и перепроверь план.",
      override: "Я вижу предупреждение и осознанно подтверждаю превышение лимита.",
      needOverride: "Лимит риска превышен. Подтверди превышение галочкой, чтобы сохранить план.",
      streakNote: "Серия убытков считается подряд по всей истории и не обнуляется в понедельник: три убытка в пятницу останутся серией и на следующей неделе. Прерывает её только сделка с результатом 0R или лучше."
    },
    en: {
      balance: "Balance, USD", risk: "Risk, %", pair: "Pair", direction: "Direction",
      stop: "Stop, pips", pip: "USD/pip per lot", rate: "USD -> UZS", setup: "Setup",
      strategy: "Strategy version", manualStrategy: "No saved strategy",
      notes: "Original entry reason", calculate: "1. Calculate", checks: "2. Verify the plan",
      save: "3. Add plan", journal: "Open plan in journal", download: "Download CSV",
      riskAmount: "Risk", lot: "Position size", all: "Check every item before saving.",
      saved: "Saved with Plan status. You can now open it in the journal.",
      checklist: ["Setup matches the trading plan", "Stop is defined before entry", "No major news near the entry", "I accept the full loss without moving the stop"],
      budgetTitle: "Automatic risk budget", budgetSettings: "Limit settings",
      maxOpen: "Max simultaneous risk, %", dailyLimit: "Daily limit, R",
      weeklyLimit: "Weekly limit, R", pauseAfter: "Pause after losses",
      plannedRisk: "Planned", openRisk: "Open", afterRisk: "After new trade",
      todayR: "Today", weekR: "This week", remaining: "Remaining",
      lossStreak: "Loss streak", budgetOk: "All limits are respected.",
      budgetWarn: "One or more limits are exceeded. Pause and review the plan.",
      override: "I understand the warning and explicitly confirm exceeding the limit.",
      needOverride: "Risk limit exceeded. Tick the confirmation box to save the plan.",
      streakNote: "The losing streak runs across the whole history and does not reset on Monday: three losses on Friday still count next week. Only a trade at 0R or better breaks it."
    },
    uz: {
      balance: "Depozit, USD", risk: "Risk, %", pair: "Juftlik", direction: "Yo'nalish",
      stop: "Stop, pip", pip: "1 lot uchun USD/pip", rate: "USD -> UZS", setup: "Setap",
      strategy: "Strategiya versiyasi", manualStrategy: "Saqlangan strategiyasiz",
      notes: "Kirishning dastlabki sababi", calculate: "1. Hisoblash", checks: "2. Rejani tekshirish",
      save: "3. Rejani qo'shish", journal: "Rejani jurnalda ochish", download: "CSV yuklash",
      riskAmount: "Risk", lot: "Pozitsiya hajmi", all: "Saqlashdan oldin barcha bandlarni belgilang.",
      saved: "Reja «Plan» holatida saqlandi. Uni endi jurnalda ochish mumkin.",
      checklist: ["Setap savdo rejasiga mos", "Stop kirishdan oldin belgilangan", "Kirish yaqinida muhim yangilik yo'q", "Stopni ko'chirmasdan to'liq zararni qabul qilaman"],
      budgetTitle: "Avtomatik risk byudjeti", budgetSettings: "Limit sozlamalari",
      maxOpen: "Maks. bir vaqtdagi risk, %", dailyLimit: "Kunlik limit, R",
      weeklyLimit: "Haftalik limit, R", pauseAfter: "Zarardan keyingi tanaffus",
      plannedRisk: "Rejalashtirilgan", openRisk: "Ochiq", afterRisk: "Yangi savdodan keyin",
      todayR: "Bugun", weekR: "Shu hafta", remaining: "Qoldiq",
      lossStreak: "Ketma-ket zarar", budgetOk: "Barcha limitlarga rioya qilindi.",
      budgetWarn: "Bir yoki bir nechta limit oshdi. Tanaffus qiling va rejani qayta tekshiring.",
      override: "Ogohlantirishni ko'rdim va limit oshishini ongli ravishda tasdiqlayman.",
      needOverride: "Risk limiti oshdi. Rejani saqlash uchun tasdiq katagini belgilang.",
      streakNote: "Zarar seriyasi butun tarix bo'yicha ketma-ket sanaladi va dushanbada nolga tushmaydi: juma kunidagi uchta zarar keyingi haftada ham seriya bo'lib qoladi. Uni faqat 0R yoki undan yaxshi natijali savdo uzadi."
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
    field(T.strategy, '<select id="td-strategy"><option value="">' + T.manualStrategy + '</option></select>'),
    field(T.setup, '<input id="td-setup" value="pullback">'),
    '</div>',
    field(T.notes, '<textarea id="td-notes" rows="3"></textarea>'),
    '<div class="fx-tool-actions"><button type="button" id="td-calc">' + T.calculate + '</button></div>',
    '<div id="td-result" class="fx-result" hidden></div>',
    '<section class="risk-budget" aria-labelledby="td-budget-title">',
    '<div class="risk-budget__head"><h3 id="td-budget-title">' + T.budgetTitle + '</h3>',
    '<details><summary>' + T.budgetSettings + '</summary><div class="risk-budget__settings">',
    field(T.maxOpen, '<input id="td-limit-open" type="number" min="0.1" step="0.1" value="2">'),
    field(T.dailyLimit, '<input id="td-limit-day" type="number" min="0.1" step="0.1" value="2">'),
    field(T.weeklyLimit, '<input id="td-limit-week" type="number" min="0.1" step="0.1" value="5">'),
    field(T.pauseAfter, '<input id="td-limit-streak" type="number" min="1" step="1" value="3">'),
    '<p class="risk-budget__note">' + T.streakNote + '</p>',
    '</div></details></div>',
    '<div id="td-risk-budget" class="risk-budget__body" aria-live="polite"></div>',
    '<label id="td-risk-override-wrap" class="risk-budget__override" hidden>',
    '<input id="td-risk-override" type="checkbox"> <span>' + T.override + '</span></label>',
    '</section>',
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
  var currentBudget = null;
  var currentStrategy = null;

  function field(label, control) {
    return '<label><span>' + label + '</span>' + control + '</label>';
  }

  function value(id) {
    return Number(document.getElementById(id).value);
  }

  function readObject(key, fallback) {
    try {
      var parsed = JSON.parse(localStorage.getItem(key) || "null");
      return parsed && typeof parsed === "object" ? parsed : fallback;
    } catch (error) {
      return fallback;
    }
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

  function riskPercent(plan, balance) {
    var percent = Number(plan.risk_pct);
    if (isFinite(percent) && percent >= 0) return percent;
    var usd = Number(plan.risk_usd);
    return balance > 0 && isFinite(usd) && usd >= 0 ? usd / balance * 100 : 0;
  }

  function dateOnly(value) {
    var match = String(value || "").match(/^\d{4}-\d{2}-\d{2}/);
    return match ? match[0] : "";
  }

  function startOfWeek(date) {
    var copy = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    copy.setDate(copy.getDate() - ((copy.getDay() + 6) % 7));
    return localDate(copy);
  }

  function closedHistory() {
    var byId = {};
    var history = readArray(HISTORY_KEY);
    history.forEach(function (trade, index) {
      var r = Number(trade.r);
      var day = dateOnly(trade.date || trade.closed_at);
      if (day && isFinite(r)) byId[String(trade.id || "history-" + index)] = { date: day, r: r };
    });
    readArray(STORAGE_KEY).forEach(function (plan, index) {
      if (plan.status !== "closed") return;
      var risk = Number(plan.risk_usd);
      var net = Number(plan.result_usd) - Math.abs(Number(plan.commission_usd) || 0);
      var day = dateOnly(plan.closed_at || plan.date);
      if (day && risk > 0 && isFinite(net)) {
        byId[String(plan.id || "plan-" + index)] = { date: day, r: net / risk };
      }
    });
    return Object.keys(byId).map(function (key) { return byId[key]; });
  }

  function riskLimits() {
    return {
      maxOpen: Math.max(0.1, value("td-limit-open") || 2),
      daily: Math.max(0.1, value("td-limit-day") || 2),
      weekly: Math.max(0.1, value("td-limit-week") || 5),
      streak: Math.max(1, Math.floor(value("td-limit-streak") || 3))
    };
  }

  function signed(value) {
    var number = Number(value) || 0;
    return (number > 0 ? "+" : "") + number.toFixed(2) + "R";
  }

  function renderRiskBudget() {
    var balance = Math.max(1, value("td-balance") || 1);
    var plans = readArray(STORAGE_KEY);
    var planned = plans.filter(function (plan) { return plan.status === "plan"; })
      .reduce(function (sum, plan) { return sum + riskPercent(plan, balance); }, 0);
    var open = plans.filter(function (plan) { return plan.status === "open"; })
      .reduce(function (sum, plan) { return sum + riskPercent(plan, balance); }, 0);
    var added = current ? Number(current.risk_pct) || 0 : value("td-risk") || 0;
    var after = open + added;
    var limits = riskLimits();
    var now = new Date();
    var today = localDate(now);
    var monday = startOfWeek(now);
    var history = closedHistory().sort(function (a, b) { return a.date.localeCompare(b.date); });
    var dailyR = history.filter(function (trade) { return trade.date === today; })
      .reduce(function (sum, trade) { return sum + trade.r; }, 0);
    var weeklyR = history.filter(function (trade) { return trade.date >= monday && trade.date <= today; })
      .reduce(function (sum, trade) { return sum + trade.r; }, 0);
    var streak = 0;
    for (var index = history.length - 1; index >= 0; index--) {
      if (history[index].r >= 0) break;
      streak++;
    }
    var reasons = [];
    if (after > limits.maxOpen) reasons.push("open");
    if (dailyR <= -limits.daily) reasons.push("daily");
    if (weeklyR <= -limits.weekly) reasons.push("weekly");
    if (streak >= limits.streak) reasons.push("streak");
    var remainingOpen = Math.max(0, limits.maxOpen - after);
    var remainingDay = Math.max(0, limits.daily + dailyR);
    var remainingWeek = Math.max(0, limits.weekly + weeklyR);
    currentBudget = {
      planned_percent: planned, open_percent: open, new_percent: added,
      after_percent: after, remaining_open_percent: remainingOpen,
      daily_r: dailyR, weekly_r: weeklyR,
      remaining_daily_r: remainingDay, remaining_weekly_r: remainingWeek,
      loss_streak: streak, limits: limits, requires_confirmation: reasons.length > 0,
      reasons: reasons
    };
    var body = document.getElementById("td-risk-budget");
    body.className = "risk-budget__body " + (reasons.length ? "is-warning" : "is-ok");
    body.innerHTML = '<div class="risk-budget__metrics">' +
      metric(T.plannedRisk, planned.toFixed(2) + "%") +
      metric(T.openRisk, open.toFixed(2) + "%") +
      metric(T.afterRisk, after.toFixed(2) + "%") +
      metric(T.todayR, signed(dailyR)) +
      metric(T.weekR, signed(weeklyR)) +
      metric(T.lossStreak, String(streak)) +
      '</div><p><strong>' + (reasons.length ? T.budgetWarn : T.budgetOk) + '</strong></p>' +
      '<p>' + T.remaining + ': ' + remainingOpen.toFixed(2) + '% / ' +
      remainingDay.toFixed(2) + 'R / ' + remainingWeek.toFixed(2) + 'R</p>';
    var override = document.getElementById("td-risk-override-wrap");
    override.hidden = !reasons.length;
    if (!reasons.length) document.getElementById("td-risk-override").checked = false;
    if (reasons.length && window.fxTrack) window.fxTrack("risk_limit_warning_shown");
    // Тот же расчёт есть в forex_toolkit/risk_budget.py. Публикуем результат,
    // чтобы e2e сверял две реализации целиком, а не только видимые цифры.
    window.__fxRiskBudget = currentBudget;
    return currentBudget;
  }

  function metric(label, result) {
    return '<div><span>' + label + '</span><strong>' + result + '</strong></div>';
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
      planned_reason: document.getElementById("td-notes").value.trim(),
      strategy: currentStrategy && window.FXStrategies
        ? window.FXStrategies.snapshot(currentStrategy) : null
    };

    var result = document.getElementById("td-result");
    result.innerHTML = '<div class="fx-metrics"><div><span>' + T.riskAmount + '</span><strong>' +
      F.money(risk) + ' / ' + Math.round(risk * rate).toLocaleString(F.numLocale) +
      ' UZS</strong></div><div><span>' + T.lot + '</span><strong>' + lot.toFixed(2) +
      ' lot</strong></div></div>';
    result.hidden = false;
    renderRiskBudget();
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
      settings.riskBudget = riskLimits();
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
    var budget = renderRiskBudget();
    var override = document.getElementById("td-risk-override").checked;
    var needsOverride = budget.requires_confirmation && !override;
    if (!current || !allChecked() || needsOverride) {
      document.getElementById("td-status").textContent =
        needsOverride && allChecked() ? T.needOverride : T.all;
      return;
    }
    current.risk_guard = Object.assign({}, budget, {
      confirmed_override: budget.requires_confirmation && override,
      checked_at: new Date().toISOString()
    });
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

  function restoreSettings() {
    var settings = readObject(SETTINGS_KEY, {});
    var tradeDesk = settings.tradeDesk || {};
    var budget = settings.riskBudget || {};
    if (tradeDesk.balance > 0) document.getElementById("td-balance").value = tradeDesk.balance;
    if (tradeDesk.riskPct > 0) document.getElementById("td-risk").value = tradeDesk.riskPct;
    if (tradeDesk.pipValue > 0) document.getElementById("td-pip").value = tradeDesk.pipValue;
    if (tradeDesk.usdUzs > 0) document.getElementById("td-rate").value = tradeDesk.usdUzs;
    if (budget.maxOpen > 0) document.getElementById("td-limit-open").value = budget.maxOpen;
    if (budget.daily > 0) document.getElementById("td-limit-day").value = budget.daily;
    if (budget.weekly > 0) document.getElementById("td-limit-week").value = budget.weekly;
    if (budget.streak > 0) document.getElementById("td-limit-streak").value = budget.streak;
  }

  function refreshStrategies() {
    var select = document.getElementById("td-strategy");
    var selected = select.value;
    var items = window.FXStrategies ? window.FXStrategies.read().filter(function (item) { return item.active; }) : [];
    select.innerHTML = '<option value="">' + T.manualStrategy + '</option>' + items.map(function (item) {
      return '<option value="' + F.escape(item.id) + '">' + F.escape(item.name) +
        ' v' + F.escape(item.version) + ' · ' + F.escape(item.timeframe) + '</option>';
    }).join("");
    if (items.some(function (item) { return item.id === selected; })) select.value = selected;
  }

  document.getElementById("td-strategy").addEventListener("change", function (event) {
    currentStrategy = window.FXStrategies
      ? window.FXStrategies.read().find(function (item) { return item.id === event.target.value; }) || null
      : null;
    if (currentStrategy) {
      document.getElementById("td-setup").value = currentStrategy.name + " v" + currentStrategy.version;
      document.getElementById("td-risk").value = currentStrategy.maxRiskPct;
      current = null;
      renderRiskBudget();
    }
  });
  window.addEventListener("fx:strategies-updated", refreshStrategies);

  ["td-balance", "td-risk", "td-limit-open", "td-limit-day", "td-limit-week", "td-limit-streak"].forEach(function (id) {
    document.getElementById(id).addEventListener("input", renderRiskBudget);
  });
  restoreSettings();
  refreshStrategies();
  renderRiskBudget();
})();
