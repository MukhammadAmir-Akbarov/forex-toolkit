/*
 * Student dashboard: one local page that connects progress, exam, replay and journal.
 * Reads localStorage only; no network, no server state.
 */
(function () {
  var root = document.getElementById("student-dashboard");
  if (!root) return;

  var lang = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (lang !== "en" && lang !== "uz") lang = "ru";

  var T = {
    ru: {
      title: "Твой учебный цикл",
      subtitle: "Учусь -> тренируюсь -> веду журнал -> исправляю слабые места.",
      level: "Уровень",
      score: "Готовность",
      progress: "Обучение",
      exam: "Экзамен",
      replay: "Replay",
      journal: "Журнал",
      next: "Следующий шаг",
      profileTitle: "Тест готовности",
      profileMeta: "Отвечает на вопрос, стоит ли тебе торговать вообще.",
      profileBands: {
        excellent: "Отличный профиль", good: "Хороший профиль",
        borderline: "Пограничный профиль — сначала укрепи слабые зоны",
        high_risk: "Высокий риск — пока не начинай",
        critical: "Критический риск — торговать сейчас не стоит"
      },
      read: "Пройдено страниц",
      best: "Лучший результат",
      notPassed: "не сдан",
      passed: "сдан",
      trades: "сделок",
      noData: "нет данных",
      winrate: "Win Rate",
      avgR: "средний R",
      weak: "слабость",
      replayCats: { u: "восходящий тренд", d: "нисходящий тренд", s: "флэт" },
      discipline: "дисциплина",
      pnl: "P&L",
      export: "Экспорт JSON",
      import: "Импорт JSON",
      importReady: "Резервная копия восстановлена.",
      importBad: "Не удалось прочитать backup: файл повреждён или имеет неизвестную версию.",
      previewTitle: "Проверь перед восстановлением",
      previewVersion: "Версия backup",
      previewDate: "Дата экспорта",
      previewProgress: "Пройденные страницы",
      previewJournal: "Сделки в журнале",
      previewPlans: "Планы сделок",
      previewReplay: "Replay-сделки",
      previewSettings: "Настройки инструментов",
      previewStrategies: "Версии стратегий", previewTraining: "Упражнения Replay",
      present: "есть",
      absent: "нет",
      restore: "Восстановить данные",
      cancel: "Отмена",
      dataTitle: "Защита локальных данных", lastBackup: "Последний backup", never: "ещё не создавался",
      backupFresh: "Резервная копия свежая.", backupStale: "Сделай новый backup: прошло 30 дней или данные ещё не сохранялись.",
      storageStatus: "Хранилище браузера", storagePersistent: "постоянное", storageTemporary: "может быть очищено браузером",
      requestStorage: "Запросить постоянное хранение",
      reset: "Очистить данные кабинета",
      confirmReset: "Очистить прогресс, экзамен, Replay, полный журнал, планы и настройки в этом браузере?",
      beginner: "Beginner",
      demo: "Demo Ready",
      riskReady: "Risk Ready",
      liveCaution: "Live Caution",
      steps: {
        profile: "Пройди тест готовности — он отвечает, стоит ли тебе торговать вообще.",
        progress: "Прочитай базовые разделы и отмечай страницы как пройденные.",
        exam: "Пройди итоговый экзамен минимум на 80%.",
        replay: "Сделай Replay-тренировку и сохрани статистику.",
        journal: "Загрузи CSV в веб-журнал, чтобы увидеть дисциплину.",
        discipline: "Сначала исправь нарушения правил. Цель: дисциплина 95%+.",
        replayWeak: "Повтори ошибочные Replay-эпизоды в категории: {category}.",
        risk: "Переходи только через демо и маленький риск. Реал не должен быть первым тестом.",
        good: "Продолжай цикл: журнал -> вывод -> одно правило на следующую неделю."
      },
      links: {
        profile: "Пройти тест",
        progress: "Открыть прогресс",
        exam: "Открыть экзамен",
        replay: "Открыть Replay",
        journal: "Открыть веб-журнал"
      }
    },
    en: {
      title: "Your Learning Loop",
      subtitle: "Learn -> practise -> journal -> fix weak spots.",
      level: "Level",
      score: "Readiness",
      progress: "Learning",
      exam: "Exam",
      replay: "Replay",
      journal: "Journal",
      next: "Next step",
      profileTitle: "Readiness test",
      profileMeta: "Answers whether you should be trading at all.",
      profileBands: {
        excellent: "Excellent profile", good: "Good profile",
        borderline: "Borderline — close the weak areas first",
        high_risk: "High risk — do not start yet",
        critical: "Critical risk — trading now is a bad idea"
      },
      read: "Pages completed",
      best: "Best score",
      notPassed: "not passed",
      passed: "passed",
      trades: "trades",
      noData: "no data",
      winrate: "Win Rate",
      avgR: "avg R",
      weak: "weak spot",
      replayCats: { u: "uptrend", d: "downtrend", s: "sideways" },
      discipline: "discipline",
      pnl: "P&L",
      export: "Export JSON",
      import: "Import JSON",
      importReady: "Backup restored.",
      importBad: "Could not read the backup: the file is damaged or uses an unknown version.",
      previewTitle: "Review before restoring",
      previewVersion: "Backup version",
      previewDate: "Export date",
      previewProgress: "Completed pages",
      previewJournal: "Journal trades",
      previewPlans: "Trade plans",
      previewReplay: "Replay trades",
      previewSettings: "Tool settings",
      previewStrategies: "Strategy versions", previewTraining: "Replay exercises",
      present: "present",
      absent: "absent",
      restore: "Restore data",
      cancel: "Cancel",
      dataTitle: "Local data protection", lastBackup: "Last backup", never: "not created yet",
      backupFresh: "The backup is recent.", backupStale: "Create a new backup: 30 days passed or no backup exists.",
      storageStatus: "Browser storage", storagePersistent: "persistent", storageTemporary: "may be cleared by the browser",
      requestStorage: "Request persistent storage",
      reset: "Clear dashboard data",
      confirmReset: "Clear progress, exam, Replay, full journal, trade plans and settings in this browser?",
      beginner: "Beginner",
      demo: "Demo Ready",
      riskReady: "Risk Ready",
      liveCaution: "Live Caution",
      steps: {
        profile: "Take the readiness test — it answers whether you should be trading at all.",
        progress: "Read the core sections and mark pages as completed.",
        exam: "Pass the final exam with at least 80%.",
        replay: "Complete a Replay session and save the statistics.",
        journal: "Upload a CSV to the web journal to see discipline.",
        discipline: "Fix rule violations first. Target: 95%+ discipline.",
        replayWeak: "Repeat failed Replay episodes in: {category}.",
        risk: "Move through demo and tiny risk only. Live money must not be the first test.",
        good: "Keep the loop going: journal -> insight -> one rule for next week."
      },
      links: {
        profile: "Take the test",
        progress: "Open progress",
        exam: "Open exam",
        replay: "Open Replay",
        journal: "Open web journal"
      }
    },
    uz: {
      title: "Sizning o'quv siklingiz",
      subtitle: "O'rganish -> mashq -> jurnal -> zaif joylarni tuzatish.",
      level: "Daraja",
      score: "Tayyorlik",
      progress: "O'qish",
      exam: "Imtihon",
      replay: "Replay",
      journal: "Jurnal",
      next: "Keyingi qadam",
      profileTitle: "Tayyorlik testi",
      profileMeta: "Umuman savdo qilish kerakmi degan savolga javob beradi.",
      profileBands: {
        excellent: "A'lo profil", good: "Yaxshi profil",
        borderline: "Chegarada — avval zaif tomonlarni yoping",
        high_risk: "Yuqori risk — hozircha boshlamang",
        critical: "Kritik risk — hozir savdo qilish yaxshi fikr emas"
      },
      read: "O'qilgan sahifalar",
      best: "Eng yaxshi natija",
      notPassed: "topshirilmagan",
      passed: "topshirildi",
      trades: "savdo",
      noData: "ma'lumot yo'q",
      winrate: "Win Rate",
      avgR: "o'rtacha R",
      weak: "zaiflik",
      replayCats: { u: "ko'tarilish trendi", d: "pasayish trendi", s: "flet" },
      discipline: "intizom",
      pnl: "P&L",
      export: "JSON eksport",
      import: "JSON import",
      importReady: "Zaxira nusxasi tiklandi.",
      importBad: "Backup o'qilmadi: fayl buzilgan yoki versiyasi noma'lum.",
      previewTitle: "Tiklashdan oldin tekshiring",
      previewVersion: "Backup versiyasi",
      previewDate: "Eksport sanasi",
      previewProgress: "O'qilgan sahifalar",
      previewJournal: "Jurnaldagi savdolar",
      previewPlans: "Savdo rejalari",
      previewReplay: "Replay savdolari",
      previewSettings: "Asbob sozlamalari",
      previewStrategies: "Strategiya versiyalari", previewTraining: "Replay mashqlari",
      present: "bor",
      absent: "yo'q",
      restore: "Ma'lumotlarni tiklash",
      cancel: "Bekor qilish",
      dataTitle: "Mahalliy ma'lumotlarni himoyalash", lastBackup: "Oxirgi backup", never: "hali yaratilmagan",
      backupFresh: "Zaxira nusxasi yangi.", backupStale: "Yangi backup yarating: 30 kun o'tdi yoki backup yo'q.",
      storageStatus: "Brauzer xotirasi", storagePersistent: "doimiy", storageTemporary: "brauzer tomonidan tozalanishi mumkin",
      requestStorage: "Doimiy saqlashni so'rash",
      reset: "Kabinet ma'lumotlarini tozalash",
      confirmReset: "Bu brauzerdagi progress, imtihon, Replay, to'liq jurnal, rejalar va sozlamalar tozalansinmi?",
      beginner: "Beginner",
      demo: "Demo Ready",
      riskReady: "Risk Ready",
      liveCaution: "Live Caution",
      steps: {
        profile: "Tayyorlik testini topshiring — u umuman savdo qilish kerakmi degan savolga javob beradi.",
        progress: "Asosiy bo'limlarni o'qing va sahifalarni o'qilgan deb belgilang.",
        exam: "Yakuniy imtihonni kamida 80% bilan topshiring.",
        replay: "Replay mashqini bajaring va statistikani saqlang.",
        journal: "Intizomni ko'rish uchun veb-jurnalga CSV yuklang.",
        discipline: "Avval qoidabuzarliklarni tuzating. Maqsad: 95%+ intizom.",
        replayWeak: "Replaydagi xato epizodlarni takrorlang: {category}.",
        risk: "Faqat demo va kichik risk orqali o'ting. Real pul birinchi test bo'lmasin.",
        good: "Siklni davom ettiring: jurnal -> xulosa -> keyingi hafta uchun bitta qoida."
      },
      links: {
        profile: "Testni topshirish",
        progress: "Progressni ochish",
        exam: "Imtihonni ochish",
        replay: "Replayni ochish",
        journal: "Veb-jurnalni ochish"
      }
    }
  }[lang];

  var BACKUP_VERSION = 3;
  var KEYS = [
    "fx-progress-v1",
    "forex_exam_passed",
    "forex_exam_best",
    "forex_replay_stats",
    "forex_journal_summary",
    "forex_journal_data_v2",
    "forex_trade_drafts_v1",
    "forex_tool_settings_v1",
    "forex_first15_v1",
    "forex_journal_risk_history_v1",
    "forex_strategy_playbooks_v1",
    "forex_training_queue_v1",
    "forex_data_meta_v1",
    "fx-uz-script"
  ];
  var JSON_KEYS = {
    "fx-progress-v1": "array",
    "forex_replay_stats": "object",
    "forex_journal_summary": "object",
    "forex_journal_data_v2": "object",
    "forex_trade_drafts_v1": "array",
    "forex_tool_settings_v1": "object",
    "forex_first15_v1": "object",
    "forex_journal_risk_history_v1": "array",
    "forex_strategy_playbooks_v1": "array",
    "forex_training_queue_v1": "array",
    "forex_data_meta_v1": "object"
  };
  var pendingRestore = null;

  function readJSON(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function readNumber(key) {
    try {
      var n = parseFloat(localStorage.getItem(key) || "0");
      return isFinite(n) ? n : 0;
    } catch (e) {
      return 0;
    }
  }

  function safeText(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function page(path) {
    var sameSection = path.indexOf("extras/") === 0;
    return sameSection ? "../" + path.replace(/^extras\//, "") : "../../" + path;
  }

  function navTotal() {
    var paths = {};
    Array.prototype.slice.call(document.querySelectorAll(".md-nav--primary .md-nav__link[href]")).forEach(function (a) {
      try {
        var url = new URL(a.getAttribute("href"), location.href);
        if (url.host === location.host) paths[url.pathname] = true;
      } catch (e) {}
    });
    return Math.max(1, Object.keys(paths).length);
  }

  function pct(value, digits) {
    return (value || 0).toFixed(digits == null ? 0 : digits) + "%";
  }

  function money(value) {
    var n = parseFloat(value || 0);
    var sign = n > 0 ? "+" : "";
    return sign + "$" + n.toFixed(2);
  }

  function collect() {
    var done = readJSON("fx-progress-v1", []);
    if (!Array.isArray(done)) done = [];
    var total = navTotal();
    var progressPct = Math.min(100, done.length / total * 100);
    var examBest = readNumber("forex_exam_best");
    var examPassed = false;
    try { examPassed = localStorage.getItem("forex_exam_passed") === "1"; } catch (e) {}
    var replay = readJSON("forex_replay_stats", null);
    var journal = readJSON("forex_journal_summary", null);
    var profile = readJSON("forex_risk_profile_v1", null);
    if (profile && typeof profile.percent !== "number") profile = null;

    var readiness = 0;
    readiness += Math.min(35, progressPct * 0.35);
    readiness += examPassed ? 25 : Math.min(20, examBest * 0.2);
    readiness += replay && replay.trades ? 20 : 0;
    readiness += journal && journal.trades ? 20 : 0;
    readiness = Math.round(Math.min(100, readiness));

    var discipline = journal && isFinite(parseFloat(journal.discipline)) ? parseFloat(journal.discipline) : 0;
    var level = T.beginner;
    if (readiness >= 35 && examPassed) level = T.demo;
    if (readiness >= 70 && examPassed && replay && replay.trades && journal && journal.trades) level = T.riskReady;
    if (readiness >= 85 && discipline >= 95) level = T.liveCaution;

    var next = T.steps.good;
    // Тест готовности — первый шаг для новичка. У того, кто уже ведёт журнал,
    // конкретный совет полезнее; непройденный тест всё равно виден карточкой.
    if (!profile && !(journal && journal.trades)) next = T.steps.profile;
    else if (progressPct < 20) next = T.steps.progress;
    else if (!examPassed) next = T.steps.exam;
    else if (!replay || !replay.trades) next = T.steps.replay;
    else if (!journal || !journal.trades) next = T.steps.journal;
    else if (discipline && discipline < 95) next = T.steps.discipline;
    else if (replay && replay.weakCategory) {
      next = T.steps.replayWeak.replace(
        "{category}",
        T.replayCats[replay.weakCategory] || replay.weakCategory
      );
    }
    else if (level === T.liveCaution || level === T.riskReady) next = T.steps.risk;

    return { done: done, total: total, progressPct: progressPct, examBest: examBest, examPassed: examPassed, replay: replay, journal: journal, profile: profile, readiness: readiness, level: level, next: next };
  }

  function card(title, value, meta, href, linkText, status) {
    return [
      '<section class="sd-card sd-card--' + status + '">',
      '  <div class="sd-card__title">' + safeText(title) + '</div>',
      '  <div class="sd-card__value">' + safeText(value) + '</div>',
      '  <div class="sd-card__meta">' + safeText(meta) + '</div>',
      href ? '  <a class="sd-card__link" href="' + href + '">' + safeText(linkText) + '</a>' : '',
      '</section>'
    ].join("");
  }

  function render() {
    var s = collect();
    var meta = readJSON("forex_data_meta_v1", {});
    var lastBackup = meta && meta.lastBackupAt ? new Date(meta.lastBackupAt) : null;
    var backupAge = lastBackup && !isNaN(lastBackup.getTime()) ? Date.now() - lastBackup.getTime() : Infinity;
    var backupStale = backupAge > 30 * 24 * 60 * 60 * 1000;
    var replayMeta = s.replay && s.replay.trades
      ? s.replay.trades + " " + T.trades + " · " + T.winrate + " " + (s.replay.wr || 0) + "% · " + T.avgR + " " + (s.replay.avgR || "0.00") + "R"
      : T.noData;
    if (s.replay && s.replay.weakCategory) {
      replayMeta += " · " + T.weak + ": " +
        (T.replayCats[s.replay.weakCategory] || s.replay.weakCategory);
    }
    var journalMeta = s.journal && s.journal.trades
      ? s.journal.trades + " " + T.trades + " · " + T.discipline + " " + pct(parseFloat(s.journal.discipline || 0), 1) + " · " + T.pnl + " " + money(s.journal.pnl || 0)
      : T.noData;

    root.innerHTML = [
      '<style>',
      '.student-dashboard{margin:1.4rem 0}.sd-hero{padding:1.2rem 1.4rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:14px;background:linear-gradient(135deg,rgba(59,130,246,.16),rgba(45,212,191,.08));margin-bottom:1rem}.sd-hero h2{margin:.1rem 0 .3rem}.sd-hero p{margin:.2rem 0;color:var(--md-default-fg-color--light)}.sd-level{display:flex;gap:1rem;flex-wrap:wrap;margin-top:1rem}.sd-pill{background:var(--md-default-bg-color);border:1px solid var(--md-default-fg-color--lightest);border-radius:999px;padding:.45rem .8rem;font-weight:700}.sd-bar{height:12px;background:var(--md-default-fg-color--lightest);border-radius:99px;overflow:hidden;margin-top:.8rem}.sd-fill{height:100%;background:linear-gradient(90deg,#3b82f6,#22c55e);border-radius:99px}.sd-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin:1rem 0}@media(max-width:700px){.sd-grid{grid-template-columns:1fr}}.sd-card{background:var(--md-code-bg-color);border:1px solid var(--md-default-fg-color--lightest);border-radius:12px;padding:1rem}.sd-card--ok{border-left:4px solid #22c55e}.sd-card--warn{border-left:4px solid #f59e0b}.sd-card__title{font-size:.82rem;text-transform:uppercase;letter-spacing:.04em;color:var(--md-default-fg-color--light);font-weight:700}.sd-card__value{font-size:1.55rem;font-weight:800;margin:.25rem 0;color:var(--md-primary-fg-color)}.sd-card__meta{font-size:.86rem;color:var(--md-default-fg-color--light);min-height:2.1em}.sd-card__link{display:inline-block;margin-top:.65rem;font-weight:700}.sd-next{border:1px solid rgba(45,212,191,.45);background:rgba(45,212,191,.08);border-radius:12px;padding:1rem 1.2rem;margin-top:1rem}.sd-actions{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1rem}.sd-actions button,.sd-actions label{display:inline-flex;align-items:center;gap:.35rem;border:0;border-radius:7px;padding:.58rem .9rem;background:var(--md-primary-fg-color);color:var(--md-primary-bg-color);font-weight:700;cursor:pointer;font:inherit}.sd-actions .sd-secondary{background:var(--md-code-bg-color);color:var(--md-default-fg-color);border:1px solid var(--md-default-fg-color--lightest)}.sd-actions input{display:none}.sd-note{font-size:.82rem;color:var(--md-default-fg-color--light);margin-top:.7rem}.sd-restore,.sd-data-health{margin-top:1rem;padding:1rem 1.1rem;border:1px solid rgba(59,130,246,.45);border-radius:12px;background:rgba(59,130,246,.07)}.sd-data-health.is-warning{border-color:#f59e0b;background:rgba(245,158,11,.08)}.sd-data-health h3,.sd-restore h3{margin:0 0 .65rem}.sd-preview{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.4rem 1rem;margin:.6rem 0 1rem;padding:0;list-style:none}.sd-preview li{padding:.35rem 0;border-bottom:1px solid var(--md-default-fg-color--lightest)}@media(max-width:600px){.sd-preview{grid-template-columns:1fr}}',
      '</style>',
      '<div class="sd-hero">',
      '  <h2>' + safeText(T.title) + '</h2>',
      '  <p>' + safeText(T.subtitle) + '</p>',
      '  <div class="sd-level"><span class="sd-pill">' + safeText(T.level) + ': ' + safeText(s.level) + '</span><span class="sd-pill">' + safeText(T.score) + ': ' + s.readiness + '%</span></div>',
      '  <div class="sd-bar" aria-hidden="true"><div class="sd-fill" style="width:' + s.readiness + '%"></div></div>',
      '</div>',
      '<div class="sd-grid">',
      card(T.profileTitle,
        s.profile ? s.profile.percent.toFixed(1) + '%' : T.noData,
        s.profile ? T.profileBands[s.profile.band] || '' : T.profileMeta,
        page('tools/risk-profile/'), T.links.profile,
        s.profile && s.profile.percent >= 50 ? 'ok' : 'warn'),
      card(T.progress, Math.round(s.progressPct) + '%', T.read + ': ' + s.done.length + ' / ' + s.total, page('extras/progress/'), T.links.progress, s.progressPct >= 20 ? 'ok' : 'warn'),
      card(T.exam, s.examPassed ? T.passed : T.notPassed, T.best + ': ' + s.examBest + '%', page('tools/exam/'), T.links.exam, s.examPassed ? 'ok' : 'warn'),
      card(T.replay, s.replay && s.replay.trades ? s.replay.trades + ' ' + T.trades : T.noData, replayMeta, page('tools/replay-trainer/'), T.links.replay, s.replay && s.replay.trades ? 'ok' : 'warn'),
      card(T.journal, s.journal && s.journal.trades ? s.journal.trades + ' ' + T.trades : T.noData, journalMeta, page('journal/web-journal/'), T.links.journal, s.journal && s.journal.trades ? 'ok' : 'warn'),
      '</div>',
      '<div class="sd-next"><strong>' + safeText(T.next) + ':</strong> <span id="sd-next-text">' + safeText(s.next) + '</span></div>',
      '<div class="sd-actions">',
      '  <button type="button" id="sd-export">' + safeText(T.export) + '</button>',
      '  <label class="sd-secondary">' + safeText(T.import) + '<input type="file" id="sd-import" accept="application/json,.json"></label>',
      '  <button type="button" id="sd-reset" class="sd-secondary">' + safeText(T.reset) + '</button>',
      '</div>',
      '<section class="sd-data-health ' + (backupStale ? 'is-warning' : '') + '">',
      '<h3>' + safeText(T.dataTitle) + '</h3>',
      '<p><strong>' + safeText(T.lastBackup) + ':</strong> ' + safeText(lastBackup && !isNaN(lastBackup.getTime()) ? lastBackup.toLocaleDateString() : T.never) + '</p>',
      '<p>' + safeText(backupStale ? T.backupStale : T.backupFresh) + '</p>',
      '<p><strong>' + safeText(T.storageStatus) + ':</strong> <span id="sd-storage-status">...</span></p>',
      '<div class="sd-actions"><button type="button" id="sd-persist" class="sd-secondary">' + safeText(T.requestStorage) + '</button></div>',
      '</section>',
      '<section class="sd-restore" id="sd-restore" hidden></section>',
      '<div class="sd-note" id="sd-note"></div>'
    ].join("");

    document.getElementById("sd-export").addEventListener("click", exportData);
    document.getElementById("sd-import").addEventListener("change", importData);
    document.getElementById("sd-reset").addEventListener("click", resetData);
    document.getElementById("sd-persist").addEventListener("click", requestPersistentStorage);
    updateStorageStatus();
  }

  function updateStorageStatus() {
    var target = document.getElementById("sd-storage-status");
    if (!target || !navigator.storage || !navigator.storage.persisted) {
      if (target) target.textContent = T.storageTemporary;
      return;
    }
    navigator.storage.persisted().then(function (persistent) {
      target.textContent = persistent ? T.storagePersistent : T.storageTemporary;
    });
  }

  function requestPersistentStorage() {
    if (!navigator.storage || !navigator.storage.persist) return updateStorageStatus();
    navigator.storage.persist().then(updateStorageStatus);
    if (window.fxTrack) window.fxTrack("storage_persistence_requested");
  }

  function exportData() {
    var exportedAt = new Date().toISOString();
    try {
      var meta = readJSON("forex_data_meta_v1", {});
      meta.lastBackupAt = exportedAt;
      localStorage.setItem("forex_data_meta_v1", JSON.stringify(meta));
    } catch (e) {}
    var data = {};
    KEYS.forEach(function (key) {
      try { data[key] = localStorage.getItem(key); } catch (e) { data[key] = null; }
    });
    var blob = new Blob([JSON.stringify({ schema: "forex-toolkit-backup", version: BACKUP_VERSION, exported_at: exportedAt, localStorage: data }, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "forex-dashboard-backup.json";
    a.click();
    URL.revokeObjectURL(url);
    if (window.fxTrack) window.fxTrack("backup_exported", { once: false });
    render();
  }

  function parsedValue(data, key, fallback) {
    if (!Object.prototype.hasOwnProperty.call(data, key) || data[key] == null) return fallback;
    try { return JSON.parse(String(data[key])); } catch (e) { return fallback; }
  }

  function validatePayload(payload) {
    if (!payload || typeof payload !== "object" || Array.isArray(payload)) throw new Error("invalid payload");
    var version = payload.version == null ? 1 : Number(payload.version);
    if (!Number.isInteger(version) || version < 1 || version > BACKUP_VERSION) throw new Error("unsupported version");
    if (payload.schema && payload.schema !== "forex-toolkit-backup") throw new Error("invalid schema");
    var data = payload.localStorage || payload;
    if (!data || typeof data !== "object" || Array.isArray(data)) throw new Error("invalid storage");
    KEYS.forEach(function (key) {
      if (!Object.prototype.hasOwnProperty.call(data, key) || data[key] == null || !JSON_KEYS[key]) return;
      var value = JSON.parse(String(data[key]));
      var expected = JSON_KEYS[key];
      if (expected === "array" && !Array.isArray(value)) throw new Error("invalid " + key);
      if (expected === "object" && (!value || typeof value !== "object" || Array.isArray(value))) throw new Error("invalid " + key);
    });
    return { version: version, exportedAt: payload.exported_at || "-", data: data };
  }

  function showPreview(backup) {
    pendingRestore = backup;
    var data = backup.data;
    var progress = parsedValue(data, "fx-progress-v1", []);
    var replay = parsedValue(data, "forex_replay_stats", {});
    var journalSummary = parsedValue(data, "forex_journal_summary", {});
    var journalData = parsedValue(data, "forex_journal_data_v2", {});
    var plans = parsedValue(data, "forex_trade_drafts_v1", []);
    var settings = parsedValue(data, "forex_tool_settings_v1", null);
    var strategies = parsedValue(data, "forex_strategy_playbooks_v1", []);
    var training = parsedValue(data, "forex_training_queue_v1", []);
    var journalCount = Number(journalSummary.trades || 0);
    if (!journalCount && journalData && Array.isArray(journalData.rows)) journalCount = journalData.rows.length;
    var panel = document.getElementById("sd-restore");
    panel.innerHTML = [
      '<h3>' + safeText(T.previewTitle) + '</h3>',
      '<ul class="sd-preview">',
      '<li><strong>' + safeText(T.previewVersion) + ':</strong> ' + backup.version + '</li>',
      '<li><strong>' + safeText(T.previewDate) + ':</strong> ' + safeText(backup.exportedAt) + '</li>',
      '<li><strong>' + safeText(T.previewProgress) + ':</strong> ' + (Array.isArray(progress) ? progress.length : 0) + '</li>',
      '<li><strong>' + safeText(T.previewJournal) + ':</strong> ' + journalCount + '</li>',
      '<li><strong>' + safeText(T.previewPlans) + ':</strong> ' + (Array.isArray(plans) ? plans.length : 0) + '</li>',
      '<li><strong>' + safeText(T.previewReplay) + ':</strong> ' + Number(replay.trades || 0) + '</li>',
      '<li><strong>' + safeText(T.previewSettings) + ':</strong> ' + safeText(settings ? T.present : T.absent) + '</li>',
      '<li><strong>' + safeText(T.previewStrategies) + ':</strong> ' + (Array.isArray(strategies) ? strategies.length : 0) + '</li>',
      '<li><strong>' + safeText(T.previewTraining) + ':</strong> ' + (Array.isArray(training) ? training.length : 0) + '</li>',
      '</ul>',
      '<div class="sd-actions">',
      '<button type="button" id="sd-confirm-restore">' + safeText(T.restore) + '</button>',
      '<button type="button" id="sd-cancel-restore" class="sd-secondary">' + safeText(T.cancel) + '</button>',
      '</div>'
    ].join("");
    panel.hidden = false;
    document.getElementById("sd-confirm-restore").addEventListener("click", restoreData);
    document.getElementById("sd-cancel-restore").addEventListener("click", function () {
      pendingRestore = null;
      panel.hidden = true;
      document.getElementById("sd-import").value = "";
    });
  }

  function importData(event) {
    var file = event.target.files && event.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () {
      try {
        showPreview(validatePayload(JSON.parse(reader.result)));
      } catch (e) {
        pendingRestore = null;
        document.getElementById("sd-note").textContent = T.importBad;
      }
    };
    reader.readAsText(file);
  }

  function restoreData() {
    if (!pendingRestore) return;
    var data = pendingRestore.data;
    KEYS.forEach(function (key) {
      if (!Object.prototype.hasOwnProperty.call(data, key)) return;
      try {
        if (data[key] == null) localStorage.removeItem(key);
        else localStorage.setItem(key, String(data[key]));
      } catch (e) {}
    });
    pendingRestore = null;
    render();
    document.getElementById("sd-note").textContent = T.importReady;
    if (window.fxTrack) window.fxTrack("backup_restored", { once: false });
  }

  function resetData() {
    if (!window.confirm(T.confirmReset)) return;
    KEYS.forEach(function (key) {
      try { localStorage.removeItem(key); } catch (e) {}
    });
    render();
  }

  render();
})();
