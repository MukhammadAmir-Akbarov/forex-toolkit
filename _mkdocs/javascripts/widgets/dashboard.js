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
      importReady: "Данные импортированы. Обновляю кабинет.",
      importBad: "Не удалось импортировать JSON.",
      reset: "Очистить данные кабинета",
      confirmReset: "Очистить прогресс, экзамен, Replay и summary журнала в этом браузере?",
      beginner: "Beginner",
      demo: "Demo Ready",
      riskReady: "Risk Ready",
      liveCaution: "Live Caution",
      steps: {
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
      importReady: "Data imported. Refreshing dashboard.",
      importBad: "Could not import JSON.",
      reset: "Clear dashboard data",
      confirmReset: "Clear progress, exam, Replay and journal summary in this browser?",
      beginner: "Beginner",
      demo: "Demo Ready",
      riskReady: "Risk Ready",
      liveCaution: "Live Caution",
      steps: {
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
      importReady: "Ma'lumot import qilindi. Kabinet yangilanmoqda.",
      importBad: "JSON import qilib bo'lmadi.",
      reset: "Kabinet ma'lumotlarini tozalash",
      confirmReset: "Bu brauzerdagi progress, imtihon, Replay va jurnal summary tozalansinmi?",
      beginner: "Beginner",
      demo: "Demo Ready",
      riskReady: "Risk Ready",
      liveCaution: "Live Caution",
      steps: {
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
        progress: "Progressni ochish",
        exam: "Imtihonni ochish",
        replay: "Replayni ochish",
        journal: "Veb-jurnalni ochish"
      }
    }
  }[lang];

  var KEYS = ["fx-progress-v1", "forex_exam_passed", "forex_exam_best", "forex_replay_stats", "forex_journal_summary"];

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
    if (progressPct < 20) next = T.steps.progress;
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

    return { done: done, total: total, progressPct: progressPct, examBest: examBest, examPassed: examPassed, replay: replay, journal: journal, readiness: readiness, level: level, next: next };
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
      '.student-dashboard{margin:1.4rem 0}.sd-hero{padding:1.2rem 1.4rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:14px;background:linear-gradient(135deg,rgba(59,130,246,.16),rgba(45,212,191,.08));margin-bottom:1rem}.sd-hero h2{margin:.1rem 0 .3rem}.sd-hero p{margin:.2rem 0;color:var(--md-default-fg-color--light)}.sd-level{display:flex;gap:1rem;flex-wrap:wrap;margin-top:1rem}.sd-pill{background:var(--md-default-bg-color);border:1px solid var(--md-default-fg-color--lightest);border-radius:999px;padding:.45rem .8rem;font-weight:700}.sd-bar{height:12px;background:var(--md-default-fg-color--lightest);border-radius:99px;overflow:hidden;margin-top:.8rem}.sd-fill{height:100%;background:linear-gradient(90deg,#3b82f6,#22c55e);border-radius:99px}.sd-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin:1rem 0}@media(max-width:700px){.sd-grid{grid-template-columns:1fr}}.sd-card{background:var(--md-code-bg-color);border:1px solid var(--md-default-fg-color--lightest);border-radius:12px;padding:1rem}.sd-card--ok{border-left:4px solid #22c55e}.sd-card--warn{border-left:4px solid #f59e0b}.sd-card__title{font-size:.82rem;text-transform:uppercase;letter-spacing:.04em;color:var(--md-default-fg-color--light);font-weight:700}.sd-card__value{font-size:1.55rem;font-weight:800;margin:.25rem 0;color:var(--md-primary-fg-color)}.sd-card__meta{font-size:.86rem;color:var(--md-default-fg-color--light);min-height:2.1em}.sd-card__link{display:inline-block;margin-top:.65rem;font-weight:700}.sd-next{border:1px solid rgba(45,212,191,.45);background:rgba(45,212,191,.08);border-radius:12px;padding:1rem 1.2rem;margin-top:1rem}.sd-actions{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1rem}.sd-actions button,.sd-actions label{display:inline-flex;align-items:center;gap:.35rem;border:0;border-radius:7px;padding:.58rem .9rem;background:var(--md-primary-fg-color);color:var(--md-primary-bg-color);font-weight:700;cursor:pointer;font:inherit}.sd-actions .sd-secondary{background:var(--md-code-bg-color);color:var(--md-default-fg-color);border:1px solid var(--md-default-fg-color--lightest)}.sd-actions input{display:none}.sd-note{font-size:.82rem;color:var(--md-default-fg-color--light);margin-top:.7rem}',
      '</style>',
      '<div class="sd-hero">',
      '  <h2>' + safeText(T.title) + '</h2>',
      '  <p>' + safeText(T.subtitle) + '</p>',
      '  <div class="sd-level"><span class="sd-pill">' + safeText(T.level) + ': ' + safeText(s.level) + '</span><span class="sd-pill">' + safeText(T.score) + ': ' + s.readiness + '%</span></div>',
      '  <div class="sd-bar" aria-hidden="true"><div class="sd-fill" style="width:' + s.readiness + '%"></div></div>',
      '</div>',
      '<div class="sd-grid">',
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
      '<div class="sd-note" id="sd-note"></div>'
    ].join("");

    document.getElementById("sd-export").addEventListener("click", exportData);
    document.getElementById("sd-import").addEventListener("change", importData);
    document.getElementById("sd-reset").addEventListener("click", resetData);
  }

  function exportData() {
    var data = {};
    KEYS.forEach(function (key) {
      try { data[key] = localStorage.getItem(key); } catch (e) { data[key] = null; }
    });
    var blob = new Blob([JSON.stringify({ version: 1, exported_at: new Date().toISOString(), localStorage: data }, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "forex-dashboard-backup.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  function importData(event) {
    var file = event.target.files && event.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () {
      try {
        var payload = JSON.parse(reader.result);
        var data = payload.localStorage || payload;
        KEYS.forEach(function (key) {
          if (Object.prototype.hasOwnProperty.call(data, key) && data[key] != null) localStorage.setItem(key, String(data[key]));
        });
        document.getElementById("sd-note").textContent = T.importReady;
        render();
      } catch (e) {
        document.getElementById("sd-note").textContent = T.importBad;
      }
    };
    reader.readAsText(file);
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
