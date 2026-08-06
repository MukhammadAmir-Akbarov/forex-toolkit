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
      plansTitle: "Планы и открытые сделки",
      plansEmpty: "Планов пока нет. Создай первый на экране «Перед сделкой».",
      statusPlan: "План", statusOpen: "Открыта", statusClosed: "Закрыта",
      openTrade: "Отметить открытой", closeTrade: "Закрыть сделку", cancel: "Отмена",
      originalReason: "Исходная причина", resultUsd: "Результат до комиссии, USD",
      commission: "Комиссия, USD", emotion: "Эмоция", rulesKept: "Первоначальный план соблюдён?",
      stopMoved: "Стоп передвигался?", lesson: "Что повторить или исключить",
      answerYes: "Да", answerNo: "Нет",
      saveReview: "Сохранить разбор", nextFocus: "Задача на следующую неделю",
      focusStop: "Не передвигать стоп после входа ни при каких обстоятельствах.",
      focusRules: "Брать только сделки, прошедшие первоначальный чек-лист.",
      focusEmotion: "После сильной эмоции делать паузу минимум 15 минут.",
      focusProcess: "Сохранить тот же риск и собрать ещё 5 сделок по этому процессу.",
      simulate: "Смоделировать мои результаты",
      sampleWarning: function (count) { return "Для персональной модели пока мало данных: " + count + " из рекомендуемых 30 сделок."; },
      weekdays: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
      insightSample: function (count) { return "Пока только " + count + " сделок. Для устойчивых выводов желательно 30+ в одной стратегии."; },
      insightExpectancy: function (value) { return "Средний результат на сделку: " + value + "R."; },
      insightEvening: function (count, value) { return "Вечером (после 18:00) " + count + " сделок дали " + value + "R. Проверь лимит на вечернюю торговлю."; },
      insightRules: function (count, value) { return count + " нарушений правил стоили " + value + "R. Это первая зона для исправления."; },
      insightWorst: function (label, value) { return "Слабейшая группа: " + label + " (" + value + "R). Временно сократи её или пересмотри условия входа."; },
      insightBest: function (label, value) { return "Сильнейшая группа: " + label + " (" + value + "R). Проверь, можно ли формализовать её условия."; },
      insightDiscipline: function (value) { return "Дисциплина " + value + "%. Цель перед увеличением риска — не ниже 95%."; },
      restoredName: "Сохранённый журнал",
      qualityTitle: "Проверка качества импорта", qualityFound: "Найдено", qualityValid: "Можно импортировать",
      qualityProblems: "Проблемных", qualityDuplicates: "Дубликатов", qualityMissingRisk: "Без надёжного R",
      qualityUnknown: "Неизвестные колонки", qualityPreview: "Первые 10 строк",
      qualityImportValid: "Исключить проблемы и импортировать", qualityImportAll: "Импортировать всё осознанно",
      qualityFix: "Вернуться и исправить файл", qualityIssues: "Проблемы", qualityNone: "Нет",
      issueDate: "неверная дата", issuePair: "не указан инструмент", issueResult: "нет результата",
      issueDuplicate: "дубликат", issueRisk: "нет risk_usd или result_r",
      weeklyTitle: "Автоматический недельный отчёт", weeklyEmpty: "Для недельного отчёта пока нет сделок.",
      weeklyPeriod: "Период", weeklyPrevious: "Предыдущая неделя", weeklyChange: "Изменение",
      weeklyBest: "Лучшая стратегия", weeklyWorst: "Слабейшая стратегия",
      weeklyRuleCost: "Цена нарушений", weeklyEmotion: "Слабая эмоция", weeklyFocus: "Задача на неделю",
      weeklyExport: "Скачать Markdown", weeklyPrint: "Распечатать",
      focusWeeklyRules: "Следующую неделю брать только сделки, прошедшие чек-лист.",
      focusWeeklyRisk: "Снизить риск и остановиться при достижении дневного лимита.",
      focusWeeklyEmotion: "После сильной эмоции делать паузу минимум 15 минут.",
      focusWeeklyKeep: "Не менять правила и собрать ещё 5 сделок по тому же процессу.",
      trainingTitle: "Персональная очередь Replay", trainingEmpty: "Новых упражнений из журнала пока нет.",
      trainingOpen: "Открыть Replay", trainingStop: "10 постановок стопа до входа",
      trainingFomo: "10 осознанных пропусков без FOMO", trainingRules: "10 решений строго по процессу",
      trainingStructure: "10 упражнений по слабой структуре рынка",
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
      plansTitle: "Plans and open trades",
      plansEmpty: "No plans yet. Create the first one on the Pre-trade screen.",
      statusPlan: "Plan", statusOpen: "Open", statusClosed: "Closed",
      openTrade: "Mark as open", closeTrade: "Close trade", cancel: "Cancel",
      originalReason: "Original reason", resultUsd: "Result before commission, USD",
      commission: "Commission, USD", emotion: "Emotion", rulesKept: "Was the original plan followed?",
      stopMoved: "Was the stop moved?", lesson: "What to repeat or remove",
      answerYes: "Yes", answerNo: "No",
      saveReview: "Save review", nextFocus: "Task for next week",
      focusStop: "Do not move the stop after entry under any circumstances.",
      focusRules: "Take only trades that pass the original checklist.",
      focusEmotion: "Pause for at least 15 minutes after a strong emotion.",
      focusProcess: "Keep the same risk and collect 5 more trades with this process.",
      simulate: "Simulate my results",
      sampleWarning: function (count) { return "The personal model has only " + count + " of the recommended 30 trades."; },
      weekdays: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      insightSample: function (count) { return "Only " + count + " trades so far. Aim for 30+ trades in one strategy for stable conclusions."; },
      insightExpectancy: function (value) { return "Average result per trade: " + value + "R."; },
      insightEvening: function (count, value) { return count + " evening trades (after 18:00) produced " + value + "R. Consider an evening trading limit."; },
      insightRules: function (count, value) { return count + " rule violations cost " + value + "R. This is the first area to fix."; },
      insightWorst: function (label, value) { return "Weakest group: " + label + " (" + value + "R). Reduce it temporarily or review its entry conditions."; },
      insightBest: function (label, value) { return "Strongest group: " + label + " (" + value + "R). Check whether its conditions can be formalized."; },
      insightDiscipline: function (value) { return "Discipline is " + value + "%. Target at least 95% before increasing risk."; },
      restoredName: "Saved journal",
      qualityTitle: "Import quality check", qualityFound: "Found", qualityValid: "Ready to import",
      qualityProblems: "Problem rows", qualityDuplicates: "Duplicates", qualityMissingRisk: "Without reliable R",
      qualityUnknown: "Unknown columns", qualityPreview: "First 10 rows",
      qualityImportValid: "Exclude problems and import", qualityImportAll: "Import everything explicitly",
      qualityFix: "Go back and fix the file", qualityIssues: "Issues", qualityNone: "None",
      issueDate: "invalid date", issuePair: "missing instrument", issueResult: "missing result",
      issueDuplicate: "duplicate", issueRisk: "missing risk_usd or result_r",
      weeklyTitle: "Automatic weekly report", weeklyEmpty: "There are no trades for a weekly report yet.",
      weeklyPeriod: "Period", weeklyPrevious: "Previous week", weeklyChange: "Change",
      weeklyBest: "Best strategy", weeklyWorst: "Weakest strategy",
      weeklyRuleCost: "Rule violation cost", weeklyEmotion: "Weak emotion", weeklyFocus: "Weekly focus",
      weeklyExport: "Download Markdown", weeklyPrint: "Print",
      focusWeeklyRules: "Take only trades that pass the checklist next week.",
      focusWeeklyRisk: "Reduce risk and stop when the daily limit is reached.",
      focusWeeklyEmotion: "Pause for at least 15 minutes after a strong emotion.",
      focusWeeklyKeep: "Keep the rules unchanged and collect 5 more trades with the same process.",
      trainingTitle: "Personal Replay queue", trainingEmpty: "No new journal-based exercises yet.",
      trainingOpen: "Open Replay", trainingStop: "10 stop placements before entry",
      trainingFomo: "10 intentional skips without FOMO", trainingRules: "10 decisions strictly by process",
      trainingStructure: "10 exercises on the weak market structure",
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
      plansTitle: "Rejalar va ochiq savdolar",
      plansEmpty: "Hozircha reja yo'q. Birinchi rejani «Savdodan oldin» ekranida yarating.",
      statusPlan: "Plan", statusOpen: "Ochiq", statusClosed: "Yopiq",
      openTrade: "Ochiq deb belgilash", closeTrade: "Savdoni yopish", cancel: "Bekor qilish",
      originalReason: "Dastlabki sabab", resultUsd: "Komissiyadan oldingi natija, USD",
      commission: "Komissiya, USD", emotion: "Hissiyot", rulesKept: "Dastlabki rejaga amal qilindimi?",
      stopMoved: "Stop ko'chirildimi?", lesson: "Nimani takrorlash yoki chiqarish kerak",
      answerYes: "Ha", answerNo: "Yo'q",
      saveReview: "Tahlilni saqlash", nextFocus: "Keyingi hafta vazifasi",
      focusStop: "Kirishdan keyin stopni hech qanday holatda ko'chirmaslik.",
      focusRules: "Faqat dastlabki checklistdan o'tgan savdolarni olish.",
      focusEmotion: "Kuchli hissiyotdan keyin kamida 15 daqiqa tanaffus qilish.",
      focusProcess: "Riskni o'zgartirmasdan shu jarayon bo'yicha yana 5 savdo yig'ish.",
      simulate: "Natijalarimni modellashtirish",
      sampleWarning: function (count) { return "Shaxsiy model uchun hozircha " + count + "/30 savdo bor."; },
      weekdays: ["Du", "Se", "Cho", "Pa", "Ju", "Sha", "Ya"],
      insightSample: function (count) { return "Hozircha " + count + " ta savdo bor. Barqaror xulosa uchun bitta strategiyada 30+ savdo to'plang."; },
      insightExpectancy: function (value) { return "Har bir savdoning o'rtacha natijasi: " + value + "R."; },
      insightEvening: function (count, value) { return "Kechqurun (18:00 dan keyin) " + count + " ta savdo " + value + "R berdi. Kechki savdoga limit qo'yishni tekshiring."; },
      insightRules: function (count, value) { return count + " ta qoida buzilishi " + value + "R ga tushdi. Avval shu joyni tuzating."; },
      insightWorst: function (label, value) { return "Eng zaif guruh: " + label + " (" + value + "R). Uni vaqtincha kamaytiring yoki kirish shartlarini ko'rib chiqing."; },
      insightBest: function (label, value) { return "Eng kuchli guruh: " + label + " (" + value + "R). Uning shartlarini aniq qoidaga aylantirishni tekshiring."; },
      insightDiscipline: function (value) { return "Intizom " + value + "%. Riskni oshirishdan oldin maqsad kamida 95%."; },
      restoredName: "Saqlangan jurnal",
      qualityTitle: "Import sifatini tekshirish", qualityFound: "Topildi", qualityValid: "Importga tayyor",
      qualityProblems: "Muammoli", qualityDuplicates: "Dublikat", qualityMissingRisk: "Ishonchli R yo'q",
      qualityUnknown: "Noma'lum ustunlar", qualityPreview: "Dastlabki 10 qator",
      qualityImportValid: "Muammolarni chiqarib import qilish", qualityImportAll: "Hammasini ongli import qilish",
      qualityFix: "Faylni tuzatishga qaytish", qualityIssues: "Muammolar", qualityNone: "Yo'q",
      issueDate: "sana noto'g'ri", issuePair: "instrument yo'q", issueResult: "natija yo'q",
      issueDuplicate: "dublikat", issueRisk: "risk_usd yoki result_r yo'q",
      weeklyTitle: "Avtomatik haftalik hisobot", weeklyEmpty: "Haftalik hisobot uchun hozircha savdo yo'q.",
      weeklyPeriod: "Davr", weeklyPrevious: "Oldingi hafta", weeklyChange: "O'zgarish",
      weeklyBest: "Eng yaxshi strategiya", weeklyWorst: "Eng zaif strategiya",
      weeklyRuleCost: "Qoida buzilishi narxi", weeklyEmotion: "Zaif hissiyot", weeklyFocus: "Hafta vazifasi",
      weeklyExport: "Markdown yuklash", weeklyPrint: "Chop etish",
      focusWeeklyRules: "Keyingi hafta faqat checklistdan o'tgan savdolarni olish.",
      focusWeeklyRisk: "Riskni kamaytirish va kunlik limitga yetganda to'xtash.",
      focusWeeklyEmotion: "Kuchli hissiyotdan keyin kamida 15 daqiqa tanaffus qilish.",
      focusWeeklyKeep: "Qoidalarni o'zgartirmasdan shu jarayonda yana 5 savdo yig'ish.",
      trainingTitle: "Shaxsiy Replay navbati", trainingEmpty: "Jurnaldan yangi mashq hozircha yo'q.",
      trainingOpen: "Replayni ochish", trainingStop: "Kirishdan oldin 10 marta stop qo'yish",
      trainingFomo: "FOMOsiz 10 ta ongli o'tkazish", trainingRules: "Jarayon bo'yicha 10 ta qaror",
      trainingStructure: "Zaif bozor tuzilmasi bo'yicha 10 mashq",
    },
  });

  var STORAGE_KEY = "forex_journal_data_v2";
  var PLANS_KEY = "forex_trade_drafts_v1";
  var SETTINGS_KEY = "forex_tool_settings_v1";
  var RISK_HISTORY_KEY = "forex_journal_risk_history_v1";
  var state = { rows: [], importedRows: [], sourceText: "", sourceName: "" };
  var pendingImport = null;
  var weeklyMarkdown = "";
  var fileInput = document.getElementById("journal-file");
  var drop = document.getElementById("journal-drop");
  var demoButton = document.getElementById("journal-demo");
  var error = document.getElementById("journal-error");
  var dashboard = document.getElementById("journal-dashboard");
  var fileName = document.getElementById("journal-file-name");
  var status = document.getElementById("journal-status");
  var filters = ["journal-from", "journal-to", "journal-pair", "journal-direction", "journal-rules"];

  var plansPanel = document.createElement("section");
  plansPanel.id = "journal-plans";
  plansPanel.className = "journal-plans";
  dashboard.parentNode.insertBefore(plansPanel, dashboard);
  var monteCarloButton = document.createElement("button");
  monteCarloButton.id = "journal-monte-carlo";
  monteCarloButton.type = "button";
  monteCarloButton.className = "journal-button secondary";
  monteCarloButton.textContent = T.simulate;
  document.querySelector(".journal-toolbar").appendChild(monteCarloButton);

  var qualityPanel = document.createElement("section");
  qualityPanel.id = "journal-quality";
  qualityPanel.className = "journal-quality";
  qualityPanel.hidden = true;
  error.parentNode.insertBefore(qualityPanel, dashboard);

  var weeklyPanel = document.createElement("section");
  weeklyPanel.id = "journal-weekly-report";
  weeklyPanel.className = "journal-weekly-report";
  var insightsPanel = document.querySelector(".journal-insights");
  insightsPanel.parentNode.insertBefore(weeklyPanel, insightsPanel.nextSibling);

  var trainingPanel = document.createElement("section");
  trainingPanel.id = "journal-training-queue";
  trainingPanel.className = "journal-training-queue";
  weeklyPanel.parentNode.insertBefore(trainingPanel, weeklyPanel.nextSibling);

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

  function optionalNumber(value) {
    var text = String(value == null ? "" : value).trim().replace(/\s/g, "");
    if (!text) return null;
    if (text.indexOf(",") >= 0 && text.indexOf(".") < 0) text = text.replace(",", ".");
    var result = Number(text);
    return isFinite(result) ? result : null;
  }

  function validDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(value || ""))) return false;
    var parsed = new Date(value + "T12:00:00");
    return !isNaN(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
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
      var rawPnl = first(row, ["result_usd", "pnl", "profit", "profit_usd"]);
      var rawRisk = first(row, ["risk_usd", "risk"]);
      var parsedPnl = optionalNumber(rawPnl);
      var parsedRisk = optionalNumber(rawRisk);
      var pnl = parsedPnl === null ? 0 : parsedPnl;
      var risk = parsedRisk === null ? 0 : parsedRisk;
      var rawR = first(row, ["result_r", "r_result", "pnl_r"]);
      var parsedR = optionalNumber(rawR);
      var date = first(row, ["date", "open_date"]);
      var time = first(row, ["time", "open_time"]);
      var pair = first(row, ["pair", "symbol"]).toUpperCase().replace("/", "");
      var hourMatch = String(time).match(/^(\d{1,2})/);
      var parsedDate = date ? new Date(date + "T12:00:00") : null;
      var issues = [];
      if (!validDate(date)) issues.push("date");
      if (!/^[A-Z0-9._-]{3,12}$/.test(pair)) issues.push("pair");
      if (parsedPnl === null && parsedR === null) issues.push("result");
      var rValid = parsedR !== null || (parsedRisk !== null && parsedRisk > 0 && parsedPnl !== null);
      return {
        id: first(row, ["id", "ticket"]) || String(index + 1),
        date: date,
        time: time,
        timestamp: Date.parse(date + "T" + (time || "00:00")) || index,
        pair: pair,
        direction: first(row, ["direction", "dir", "type"]).toLowerCase(),
        setup: first(row, ["setup", "strategy"]),
        emotion: first(row, ["emotions", "emotion", "mood"]),
        hour: hourMatch ? Math.min(23, parseInt(hourMatch[1], 10)) : null,
        weekday: parsedDate && !isNaN(parsedDate.getTime()) ? (parsedDate.getDay() + 6) % 7 : null,
        pnl: pnl,
        risk: risk,
        r: parsedR !== null ? parsedR : (risk > 0 ? pnl / risk : 0),
        rValid: rValid,
        qualityIssues: issues,
        sourceIndex: index + 1,
        outcome: normalizeOutcome(first(row, ["outcome", "result"]), pnl),
        rules: normalizeRules(first(row, ["followed_rules", "rules"])),
      };
    }).filter(function (row) {
      return row.date || row.pair || row.pnl || row.outcome;
    }).sort(function (a, b) { return a.timestamp - b.timestamp; });
  }

  var KNOWN_HEADERS = [
    "id", "ticket", "date", "open_date", "time", "open_time", "pair", "symbol",
    "direction", "dir", "type", "setup", "strategy", "emotions", "emotion", "mood",
    "result_usd", "pnl", "profit", "profit_usd", "risk_usd", "risk", "result_r",
    "r_result", "pnl_r", "outcome", "result", "followed_rules", "rules", "entry_price",
    "lot_size", "close_price", "close_time", "lesson"
  ];

  function qualityReport(raw, rows) {
    var seen = {};
    var duplicates = 0;
    rows.forEach(function (row) {
      var fingerprint = [row.id, row.date, row.time, row.pair, row.pnl].join("|");
      row.duplicate = Boolean(seen[fingerprint]);
      if (row.duplicate) duplicates++;
      seen[fingerprint] = true;
    });
    var headers = raw.length ? Object.keys(raw[0]) : [];
    var unknown = headers.filter(function (header) { return KNOWN_HEADERS.indexOf(header) < 0; });
    var problems = rows.filter(function (row) { return row.qualityIssues.length || row.duplicate; }).length;
    return {
      found: rows.length,
      valid: rows.length - problems,
      problems: problems,
      duplicates: duplicates,
      missingRisk: rows.filter(function (row) { return !row.rValid; }).length,
      unknown: unknown
    };
  }

  function issueLabels(row) {
    var labels = row.qualityIssues.map(function (issue) {
      return issue === "date" ? T.issueDate : issue === "pair" ? T.issuePair : T.issueResult;
    });
    if (row.duplicate) labels.push(T.issueDuplicate);
    if (!row.rValid) labels.push(T.issueRisk);
    return labels;
  }

  function readPlans() {
    try {
      var value = JSON.parse(localStorage.getItem(PLANS_KEY) || "[]");
      if (!Array.isArray(value)) return [];
      return value.map(function (plan, index) {
        var copy = Object.assign({}, plan);
        copy.id = copy.id || "legacy-plan-" + index + "-" + (copy.date || "unknown");
        copy.status = ["plan", "open", "closed"].indexOf(copy.status) >= 0 ? copy.status : "plan";
        if (copy.planned_reason == null) copy.planned_reason = copy.notes || "";
        return copy;
      });
    } catch (e) {
      return [];
    }
  }

  function writePlans(plans) {
    try { localStorage.setItem(PLANS_KEY, JSON.stringify(plans.slice(0, 100))); } catch (e) {}
  }

  function planRows(plans) {
    return plans.filter(function (plan) { return plan.status === "closed"; }).map(function (plan, index) {
      var gross = number(plan.result_usd);
      var commission = Math.abs(number(plan.commission_usd));
      var pnl = gross - commission;
      var risk = number(plan.risk_usd);
      var closed = plan.closed_at ? new Date(plan.closed_at) : null;
      return {
        id: plan.id,
        date: plan.date || (closed ? closed.toISOString().slice(0, 10) : ""),
        time: closed ? closed.toTimeString().slice(0, 5) : "",
        timestamp: closed && !isNaN(closed.getTime()) ? closed.getTime() : index,
        pair: String(plan.pair || "").toUpperCase().replace("/", ""),
        direction: String(plan.direction || "").toLowerCase(),
        setup: plan.setup || "",
        emotion: plan.emotion || "",
        hour: closed && !isNaN(closed.getTime()) ? closed.getHours() : null,
        weekday: closed && !isNaN(closed.getTime()) ? (closed.getDay() + 6) % 7 : null,
        pnl: pnl,
        risk: risk,
        r: risk > 0 ? pnl / risk : 0,
        rValid: risk > 0,
        outcome: pnl > 0 ? "win" : pnl < 0 ? "loss" : "be",
        rules: plan.followed_rules === false ? "no" : plan.followed_rules === true ? "yes" : "",
        plannedReason: plan.planned_reason || "",
        reviewFocus: plan.review_focus || "",
        strategyId: plan.strategy && plan.strategy.id || "",
        strategyVersion: plan.strategy && plan.strategy.version || null
      };
    });
  }

  function syncRows(plans) {
    plans = plans || readPlans();
    var lifecycle = planRows(plans);
    var lifecycleIds = {};
    lifecycle.forEach(function (row) { lifecycleIds[row.id] = true; });
    state.rows = state.importedRows.filter(function (row) { return !lifecycleIds[row.id]; })
      .concat(lifecycle)
      .sort(function (a, b) { return a.timestamp - b.timestamp; });
  }

  function statusLabel(value) {
    return value === "open" ? T.statusOpen : value === "closed" ? T.statusClosed : T.statusPlan;
  }

  function reviewFocus(plan) {
    if (plan.moved_stop) return T.focusStop;
    if (plan.followed_rules === false) return T.focusRules;
    if (["anxious", "frustrated", "fomo", "angry"].indexOf(String(plan.emotion || "").toLowerCase()) >= 0) return T.focusEmotion;
    return T.focusProcess;
  }

  function closeForm(plan) {
    return [
      '<form class="journal-review" data-plan-id="' + escapeHtml(plan.id) + '" hidden>',
      '<div class="journal-review-grid">',
      '<label><span>' + T.resultUsd + '</span><input name="result" type="number" step="0.01" required></label>',
      '<label><span>' + T.commission + '</span><input name="commission" type="number" min="0" step="0.01" value="0"></label>',
      '<label><span>' + T.emotion + '</span><select name="emotion"><option value="calm">calm</option><option value="anxious">anxious</option><option value="frustrated">frustrated</option><option value="fomo">FOMO</option></select></label>',
      '<label><span>' + T.rulesKept + '</span><select name="rules"><option value="yes">' + T.yes + '</option><option value="no">' + T.no + '</option></select></label>',
      '<label><span>' + T.stopMoved + '</span><select name="stop"><option value="no">' + T.answerNo + '</option><option value="yes">' + T.answerYes + '</option></select></label>',
      '<label class="journal-review-wide"><span>' + T.lesson + '</span><textarea name="lesson" rows="2"></textarea></label>',
      '</div>',
      '<div class="journal-actions"><button class="journal-button" type="submit">' + T.saveReview + '</button><button class="journal-button secondary" type="button" data-action="cancel-review" data-id="' + escapeHtml(plan.id) + '">' + T.cancel + '</button></div>',
      '</form>'
    ].join("");
  }

  function renderPlans() {
    var plans = readPlans();
    if (!plans.length) {
      plansPanel.innerHTML = '<h3>' + T.plansTitle + '</h3><p class="journal-plans-empty">' + T.plansEmpty + '</p>';
      return plans;
    }
    plansPanel.innerHTML = '<h3>' + T.plansTitle + '</h3><div class="journal-plan-list">' + plans.slice(0, 30).map(function (plan) {
      var action = "";
      if (plan.status === "plan") {
        action = '<button class="journal-button" type="button" data-action="open" data-id="' + escapeHtml(plan.id) + '">' + T.openTrade + '</button>';
      } else if (plan.status === "open") {
        action = '<button class="journal-button" type="button" data-action="show-review" data-id="' + escapeHtml(plan.id) + '">' + T.closeTrade + '</button>' + closeForm(plan);
      }
      var focus = plan.review_focus ? '<p class="journal-plan-focus"><strong>' + T.nextFocus + ':</strong> ' + escapeHtml(plan.review_focus) + '</p>' : "";
      var closedSummary = plan.status === "closed"
        ? '<p><strong>' + T.pnl + ':</strong> ' + F.money(number(plan.result_usd) - Math.abs(number(plan.commission_usd))) + ' · ' + escapeHtml(plan.emotion || T.unknown) + '</p>'
        : "";
      return [
        '<article class="journal-plan-card" data-status="' + escapeHtml(plan.status) + '">',
        '<div class="journal-plan-head"><strong>' + escapeHtml(plan.pair || "-") + ' · ' + escapeHtml(plan.direction || "-") + '</strong><span>' + statusLabel(plan.status) + '</span></div>',
        '<p>' + escapeHtml(plan.date || "-") + ' · ' + escapeHtml(plan.setup || "-") + ' · ' + F.money(number(plan.risk_usd)) + '</p>',
        '<p><strong>' + T.originalReason + ':</strong> ' + escapeHtml(plan.planned_reason || "-") + '</p>',
        closedSummary,
        focus,
        '<div class="journal-plan-actions">' + action + '</div>',
        '</article>'
      ].join("");
    }).join("") + '</div>';
    return plans;
  }

  function refreshFromPlans() {
    var plans = renderPlans();
    syncRows(plans);
    setOptions();
    if (state.rows.length) {
      dashboard.style.display = "block";
      render();
    } else {
      dashboard.style.display = "none";
    }
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

  function isoDate(date) {
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, "0");
    var day = String(date.getDate()).padStart(2, "0");
    return year + "-" + month + "-" + day;
  }

  function weekRange(anchor) {
    var endAnchor = new Date(anchor + "T12:00:00");
    var start = new Date(endAnchor);
    start.setDate(start.getDate() - ((start.getDay() + 6) % 7));
    var end = new Date(start);
    end.setDate(end.getDate() + 6);
    var previousStart = new Date(start);
    previousStart.setDate(previousStart.getDate() - 7);
    var previousEnd = new Date(start);
    previousEnd.setDate(previousEnd.getDate() - 1);
    return {
      start: isoDate(start), end: isoDate(end),
      previousStart: isoDate(previousStart), previousEnd: isoDate(previousEnd)
    };
  }

  function groupExtreme(rows, key, best) {
    var groups = groupRows(rows, key).filter(function (group) { return group.label !== T.unknown; });
    if (!groups.length) return null;
    groups.sort(function (a, b) { return a.metrics.totalR - b.metrics.totalR; });
    return best ? groups[groups.length - 1] : groups[0];
  }

  function weeklyFocus(rows, m) {
    if (m.discipline < 95) return T.focusWeeklyRules;
    var emotional = rows.filter(function (row) {
      return ["anxious", "frustrated", "fomo", "angry"].indexOf(String(row.emotion).toLowerCase()) >= 0;
    });
    if (emotional.length && metrics(emotional).totalR < 0) return T.focusWeeklyEmotion;
    if (m.totalR < 0) return T.focusWeeklyRisk;
    return T.focusWeeklyKeep;
  }

  function renderWeeklyReport(rows) {
    var dated = rows.filter(function (row) { return validDate(row.date); });
    if (!dated.length) {
      weeklyPanel.innerHTML = '<h3>' + T.weeklyTitle + '</h3><p>' + T.weeklyEmpty + '</p>';
      weeklyMarkdown = "";
      return;
    }
    var latest = dated.reduce(function (value, row) { return row.date > value ? row.date : value; }, dated[0].date);
    var range = weekRange(latest);
    var current = dated.filter(function (row) { return row.date >= range.start && row.date <= range.end; });
    var previous = dated.filter(function (row) { return row.date >= range.previousStart && row.date <= range.previousEnd; });
    var currentM = metrics(current);
    var previousM = metrics(previous);
    var best = groupExtreme(current.filter(function (row) { return row.rValid !== false; }), "setup", true);
    var worst = groupExtreme(current.filter(function (row) { return row.rValid !== false; }), "setup", false);
    var violations = current.filter(function (row) { return row.rules === "no" && row.rValid !== false; });
    var emotion = groupExtreme(current.filter(function (row) { return row.rValid !== false; }), "emotion", false);
    var settings = {};
    try { settings = JSON.parse(localStorage.getItem(SETTINGS_KEY) || "{}"); } catch (e) {}
    var rate = Number(settings.tradeDesk && settings.tradeDesk.usdUzs) || 12500;
    var change = currentM.totalR - previousM.totalR;
    var focus = weeklyFocus(current, currentM);
    function groupText(group) {
      return group ? group.label + " (" + group.metrics.totalR.toFixed(2) + "R)" : "-";
    }
    weeklyPanel.innerHTML = '<h3>' + T.weeklyTitle + '</h3>' +
      '<p><strong>' + T.weeklyPeriod + ':</strong> ' + range.start + ' — ' + range.end + '</p>' +
      '<div class="journal-weekly__metrics">' +
      qualityStat(T.trades, currentM.trades) +
      qualityStat(T.pnl, F.money(currentM.pnl) + " / " + Math.round(currentM.pnl * rate).toLocaleString(F.numLocale) + " UZS") +
      qualityStat(T.rTotal, currentM.totalR.toFixed(2) + "R") +
      qualityStat(T.discipline, F.pct(currentM.discipline, 1)) +
      qualityStat(T.weeklyPrevious, previousM.totalR.toFixed(2) + "R") +
      qualityStat(T.weeklyChange, (change > 0 ? "+" : "") + change.toFixed(2) + "R") + '</div>' +
      '<div class="journal-weekly__findings"><p><strong>' + T.weeklyBest + ':</strong> ' + escapeHtml(groupText(best)) + '</p>' +
      '<p><strong>' + T.weeklyWorst + ':</strong> ' + escapeHtml(groupText(worst)) + '</p>' +
      '<p><strong>' + T.weeklyRuleCost + ':</strong> ' + metrics(violations).totalR.toFixed(2) + 'R</p>' +
      '<p><strong>' + T.weeklyEmotion + ':</strong> ' + escapeHtml(groupText(emotion)) + '</p>' +
      '<p class="journal-weekly__focus"><strong>' + T.weeklyFocus + ':</strong> ' + escapeHtml(focus) + '</p></div>' +
      '<div class="journal-actions"><button class="journal-button secondary" type="button" data-weekly="markdown">' + T.weeklyExport + '</button>' +
      '<button class="journal-button secondary" type="button" data-weekly="print">' + T.weeklyPrint + '</button></div>';
    weeklyMarkdown = [
      "# " + T.weeklyTitle, "", "- " + T.weeklyPeriod + ": " + range.start + " - " + range.end,
      "- " + T.trades + ": " + currentM.trades,
      "- P&L: " + currentM.pnl.toFixed(2) + " USD / " + Math.round(currentM.pnl * rate) + " UZS",
      "- " + T.rTotal + ": " + currentM.totalR.toFixed(2) + "R",
      "- " + T.discipline + ": " + currentM.discipline.toFixed(1) + "%",
      "- " + T.weeklyPrevious + ": " + previousM.totalR.toFixed(2) + "R",
      "- " + T.weeklyBest + ": " + groupText(best),
      "- " + T.weeklyWorst + ": " + groupText(worst),
      "- " + T.weeklyRuleCost + ": " + metrics(violations).totalR.toFixed(2) + "R",
      "", "## " + T.weeklyFocus, "", focus, ""
    ].join("\n");
  }

  function trainingLabel(task) {
    if (task.type === "stop") return T.trainingStop;
    if (task.type === "fomo") return T.trainingFomo;
    if (task.type === "rules") return T.trainingRules;
    return T.trainingStructure + (task.category ? " (" + task.category.toUpperCase() + ")" : "");
  }

  function renderTrainingQueue() {
    if (!window.FXTrainingQueue) return;
    var replay = {};
    try { replay = JSON.parse(localStorage.getItem("forex_replay_stats") || "{}"); } catch (e) {}
    var tasks = window.FXTrainingQueue.sync(readPlans(), replay);
    var active = tasks.filter(function (task) { return task.progress < task.target; });
    trainingPanel.innerHTML = '<h3>' + T.trainingTitle + '</h3>' + (active.length
      ? '<div class="journal-training-list">' + active.map(function (task) {
        return '<div class="journal-training-card"><strong>' + escapeHtml(trainingLabel(task)) + '</strong>' +
          '<span>' + task.progress + ' / ' + task.target + '</span><progress max="' + task.target + '" value="' + task.progress + '"></progress></div>';
      }).join("") + '</div><a class="journal-button" href="../../tools/replay-trainer/?queue=1">' + T.trainingOpen + '</a>'
      : '<p>' + T.trainingEmpty + '</p>');
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
        avgR: m.trades ? m.totalR / m.trades : 0,
        maxDrawdown: m.maxDrawdown, discipline: m.discipline,
        updated: new Date().toISOString().slice(0, 10)
      }));
      localStorage.setItem(RISK_HISTORY_KEY, JSON.stringify(state.rows.filter(function (row) {
        return row.outcome !== "open" && row.rValid !== false && validDate(row.date);
      }).slice(-1000).map(function (row) {
        return { id: row.id, date: row.date, r: row.r };
      })));
    } catch (e) {}
    drawChart(rows);
    renderHeatmap(rows);
    renderBreakdown("journal-by-pair", groupRows(rows, "pair"));
    renderBreakdown("journal-by-setup", groupRows(rows, "setup"));
    renderBreakdown("journal-by-direction", groupRows(rows, "direction"));
    renderBreakdown("journal-by-emotion", groupRows(rows, "emotion"));
    renderInsights(rows);
    renderWeeklyReport(rows);
    renderTrainingQueue();
    renderTable(rows);
  }

  function saveSource(text, name, kind, acceptedRows) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        text: text,
        name: name,
        savedAt: new Date().toISOString(),
        kind: kind,
        rows: acceptedRows
      }));
      status.textContent = T.saved;
    } catch (e) {}
  }

  function activateRows(rows, text, name, persist, kind) {
    if (!rows.length) throw new Error("empty");
    state.importedRows = rows;
    syncRows(renderPlans());
    state.sourceText = String(text || "");
    state.sourceName = name;
    error.style.display = "none";
    qualityPanel.hidden = true;
    dashboard.style.display = "block";
    fileName.textContent = T.fileReady(name, rows.length);
    setOptions();
    render();
    if (persist !== false) saveSource(String(text), name, kind, rows);
    if (persist !== false && window.fxTrack) {
      window.fxTrack(name === T.demo ? "journal_demo_opened" : "journal_import_completed");
    }
  }

  function loadText(text, name, persist, kind, acceptedRows) {
    try {
      var isMT5 = kind === "mt5" || /^\s*(?:<!doctype\s+html|<html|<table)/i.test(String(text));
      var rows = Array.isArray(acceptedRows)
        ? acceptedRows
        : normalize(isMT5 ? parseMT5HTML(text) : parseCSV(text));
      activateRows(rows, text, name, persist, isMT5 ? "mt5" : "csv");
    } catch (e) {
      dashboard.style.display = "none";
      error.textContent = T.invalid;
      error.style.display = "block";
    }
  }

  function qualityStat(label, result) {
    return '<div><span>' + escapeHtml(label) + '</span><strong>' + escapeHtml(result) + '</strong></div>';
  }

  function renderQuality() {
    if (!pendingImport) return;
    var report = pendingImport.report;
    var unknown = report.unknown.length ? report.unknown.join(", ") : T.qualityNone;
    var preview = pendingImport.rows.slice(0, 10).map(function (row) {
      var issues = issueLabels(row);
      return '<tr class="' + (row.qualityIssues.length || row.duplicate ? "is-problem" : "") + '">' +
        '<td>' + row.sourceIndex + '</td><td>' + escapeHtml(row.date || "-") + '</td>' +
        '<td>' + escapeHtml(row.pair || "-") + '</td><td>' + F.money(row.pnl) + '</td>' +
        '<td>' + (row.rValid ? row.r.toFixed(2) + "R" : "-") + '</td>' +
        '<td>' + escapeHtml(issues.join(", ") || T.qualityNone) + '</td></tr>';
    }).join("");
    qualityPanel.innerHTML = '<h3>' + T.qualityTitle + '</h3>' +
      '<div class="journal-quality__metrics">' +
      qualityStat(T.qualityFound, report.found) + qualityStat(T.qualityValid, report.valid) +
      qualityStat(T.qualityProblems, report.problems) + qualityStat(T.qualityDuplicates, report.duplicates) +
      qualityStat(T.qualityMissingRisk, report.missingRisk) + '</div>' +
      '<p><strong>' + T.qualityUnknown + ':</strong> ' + escapeHtml(unknown) + '</p>' +
      '<h4>' + T.qualityPreview + '</h4><div class="journal-table-scroll"><table class="journal-table compact">' +
      '<thead><tr><th>#</th><th>Date</th><th>Pair</th><th>P&L</th><th>R</th><th>' + T.qualityIssues + '</th></tr></thead>' +
      '<tbody>' + preview + '</tbody></table></div><div class="journal-actions">' +
      '<button class="journal-button" type="button" data-quality="valid">' + T.qualityImportValid + '</button>' +
      '<button class="journal-button secondary" type="button" data-quality="all">' + T.qualityImportAll + '</button>' +
      '<button class="journal-button secondary" type="button" data-quality="fix">' + T.qualityFix + '</button>' +
      '</div>';
    qualityPanel.hidden = false;
    dashboard.style.display = "none";
    qualityPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function previewText(text, name, kind) {
    try {
      var isMT5 = kind === "mt5" || /^\s*(?:<!doctype\s+html|<html|<table)/i.test(String(text));
      var raw = isMT5 ? parseMT5HTML(text) : parseCSV(text);
      var rows = normalize(raw);
      if (!rows.length) throw new Error("empty");
      pendingImport = {
        text: String(text), name: name, kind: isMT5 ? "mt5" : "csv", raw: raw,
        rows: rows, report: qualityReport(raw, rows)
      };
      error.style.display = "none";
      renderQuality();
    } catch (e) {
      error.textContent = T.invalid;
      error.style.display = "block";
    }
  }

  function commitPendingImport(mode) {
    if (!pendingImport) return;
    var rows = pendingImport.rows;
    if (mode === "valid") {
      rows = rows.filter(function (row) { return !row.qualityIssues.length && !row.duplicate; });
    }
    var data = pendingImport;
    pendingImport = null;
    activateRows(rows, data.text, data.name, true, data.kind);
    if (window.fxTrack) window.fxTrack("journal_quality_imported", { once: false });
  }

  function readFile(file) {
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () {
      var isMT5 = /\.(?:html?|xls)$/i.test(file.name);
      previewText(reader.result, file.name, isMT5 ? "mt5" : "csv");
    };
    reader.onerror = function () {
      error.textContent = T.invalid;
      error.style.display = "block";
    };
    reader.readAsText(file);
  }

  function updatePlan(id, updater) {
    var plans = readPlans();
    var changed = false;
    plans = plans.map(function (plan) {
      if (plan.id !== id) return plan;
      changed = true;
      return updater(Object.assign({}, plan));
    });
    if (changed) {
      writePlans(plans);
      refreshFromPlans();
    }
  }

  plansPanel.addEventListener("click", function (event) {
    var button = event.target.closest("button[data-action]");
    if (!button) return;
    var action = button.dataset.action;
    var id = button.dataset.id;
    if (action === "open") {
      updatePlan(id, function (plan) {
        plan.status = "open";
        plan.opened_at = new Date().toISOString();
        plan.updated_at = plan.opened_at;
        return plan;
      });
      if (window.fxTrack) window.fxTrack("trade_plan_opened", { once: false });
    } else if (action === "show-review") {
      var form = plansPanel.querySelector('.journal-review[data-plan-id="' + CSS.escape(id) + '"]');
      if (form) form.hidden = false;
    } else if (action === "cancel-review") {
      var cancelForm = button.closest("form");
      if (cancelForm) cancelForm.hidden = true;
    }
  });

  plansPanel.addEventListener("submit", function (event) {
    var form = event.target.closest("form.journal-review");
    if (!form) return;
    event.preventDefault();
    var result = Number(form.elements.result.value);
    if (!isFinite(result)) return;
    updatePlan(form.dataset.planId, function (plan) {
      plan.status = "closed";
      plan.result_usd = result;
      plan.commission_usd = Math.abs(Number(form.elements.commission.value) || 0);
      plan.emotion = form.elements.emotion.value;
      plan.followed_rules = form.elements.rules.value === "yes";
      plan.moved_stop = form.elements.stop.value === "yes";
      plan.review_lesson = form.elements.lesson.value.trim();
      plan.closed_at = new Date().toISOString();
      plan.updated_at = plan.closed_at;
      plan.review_focus = reviewFocus(plan);
      return plan;
    });
    if (window.fxTrack) window.fxTrack("trade_review_completed", { once: false });
  });

  function openPersonalMonteCarlo() {
    var rows = state.rows.filter(function (row) { return row.outcome !== "open" && row.rValid !== false; });
    if (!rows.length) return;
    var m = metrics(rows);
    var wins = rows.filter(function (row) { return row.r > 0; });
    var losses = rows.filter(function (row) { return row.r < 0; });
    var avgWin = wins.length ? wins.reduce(function (sum, row) { return sum + row.r; }, 0) / wins.length : 1;
    var avgLoss = losses.length ? Math.abs(losses.reduce(function (sum, row) { return sum + row.r; }, 0) / losses.length) : 1;
    try {
      var settings = JSON.parse(localStorage.getItem(SETTINGS_KEY) || "{}");
      settings.monteCarlo = {
        source: "journal",
        sampleSize: rows.length,
        trades: Math.max(10, rows.length),
        winRate: m.winRate,
        rewardRisk: Math.max(0.1, avgWin / Math.max(0.01, avgLoss)),
        updatedAt: new Date().toISOString()
      };
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
    } catch (e) {}
    if (rows.length < 30) status.textContent = T.sampleWarning(rows.length);
    if (window.fxTrack) window.fxTrack("journal_monte_carlo_opened", { once: false });
    window.location.href = "../../tools/monte-carlo/?journal=1";
  }

  fileInput.addEventListener("change", function () { readFile(fileInput.files[0]); });
  qualityPanel.addEventListener("click", function (event) {
    var button = event.target.closest("button[data-quality]");
    if (!button) return;
    if (button.dataset.quality === "fix") {
      pendingImport = null;
      qualityPanel.hidden = true;
      fileInput.value = "";
      fileInput.click();
      return;
    }
    commitPendingImport(button.dataset.quality);
  });
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
    state = { rows: [], importedRows: [], sourceText: "", sourceName: "" };
    refreshFromPlans();
    fileInput.value = "";
    fileName.textContent = T.noFile;
    status.textContent = T.cleared;
  });
  document.getElementById("journal-export-csv").addEventListener("click", exportCsv);
  document.getElementById("journal-export-html").addEventListener("click", exportHtml);
  monteCarloButton.addEventListener("click", openPersonalMonteCarlo);
  weeklyPanel.addEventListener("click", function (event) {
    var button = event.target.closest("button[data-weekly]");
    if (!button) return;
    if (button.dataset.weekly === "markdown" && weeklyMarkdown) {
      download("forex-weekly-report.md", weeklyMarkdown, "text/markdown;charset=utf-8");
      if (window.fxTrack) window.fxTrack("weekly_report_exported", { once: false });
    } else if (button.dataset.weekly === "print") {
      document.body.classList.add("journal-print-weekly");
      window.print();
      window.setTimeout(function () { document.body.classList.remove("journal-print-weekly"); }, 500);
    }
  });
  filters.forEach(function (id) {
    document.getElementById(id).addEventListener("change", render);
  });
  window.addEventListener("resize", function () {
    if (dashboard.style.display !== "none") drawChart(filteredRows());
  });
  try {
    var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if (saved && saved.text) {
      loadText(saved.text, saved.name || T.restoredName, false, saved.kind, saved.rows);
      status.textContent = T.restored + ": " + (saved.name || T.restoredName);
    } else {
      refreshFromPlans();
    }
  } catch (e) { refreshFromPlans(); }
})();
