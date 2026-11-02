/*
 * Диагностика для дорожной карты: 20 вопросов, 4 на уровень (0–4).
 *
 * Зачем: roadmap одинаков для всех, а новички приходят с разной базой —
 * кто-то год смотрел графики и знает свечи, но всё равно тратит месяц на
 * «Уровень 1». Диагностика вычёркивает из карты то, что уже известно
 * (≥3 из 4 по уровню), и оставляет честный маршрут по остальному.
 *
 * Вопросы лежат в #diag-questions на самой странице (переведены в каждой
 * локали, как у экзамена). Результат — localStorage ftk_roadmap_diag_v1;
 * отметки ставятся на элементы .fx-rm__item[data-level] при каждом визите.
 * Уровни 5–6 не проверяются вопросами: реальный счёт не «знают», его
 * проторговывают.
 */
(function () {
  var root = document.getElementById("roadmap-diag");
  if (!root) return;
  var bankEl = document.getElementById("diag-questions");
  if (!bankEl) return;

  var lang = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (lang !== "en" && lang !== "uz") lang = "ru";

  var S = ({
    ru: {
      intro:
        "Уже что-то знаешь? 20 вопросов, ~5 минут — и карта сама вычеркнет " +
        "уровни, которые можно пропустить.",
      start: "🧭 Пройти диагностику",
      retake: "↻ Пройти заново",
      reset: "Сбросить отметки",
      counter: function (i, n) { return "Вопрос " + i + " из " + n; },
      level: function (n) { return "Уровень " + n; },
      resultTitle: "Итог диагностики",
      known: function (done, total) { return "знаешь " + done + " из " + total; },
      skipped: "✓ вычеркнут из маршрута",
      toLearn: "← начни отсюда",
      savedLine: function (date, passed, total) {
        return "Диагностика от " + date + ": вычеркнуто " + passed + " из " + total + " уровней.";
      },
      caveat:
        "Вычеркнутый уровень — не бесплатный пропуск: пробежись по его " +
        "контрольным точкам и убедись, что закрываешь их без подглядываний.",
    },
    en: {
      intro:
        "Already know some of this? 20 questions, ~5 minutes — and the map " +
        "crosses out the levels you can skip.",
      start: "🧭 Take the diagnostic",
      retake: "↻ Retake",
      reset: "Clear the marks",
      counter: function (i, n) { return "Question " + i + " of " + n; },
      level: function (n) { return "Level " + n; },
      resultTitle: "Diagnostic result",
      known: function (done, total) { return "known: " + done + " of " + total; },
      skipped: "✓ crossed out of the route",
      toLearn: "← start here",
      savedLine: function (date, passed, total) {
        return "Diagnostic from " + date + ": " + passed + " of " + total + " levels crossed out.";
      },
      caveat:
        "A crossed-out level is not a free pass: skim its checkpoints and " +
        "make sure you can tick them without peeking.",
    },
    uz: {
      intro:
        "Bir qismini allaqachon bilasizmi? 20 savol, ~5 daqiqa — xarita " +
        "o'tkazib yuborish mumkin bo'lgan bosqichlarni o'zi chizib tashlaydi.",
      start: "🧭 Diagnostikadan o'tish",
      retake: "↻ Qayta topshirish",
      reset: "Belgilarni tozalash",
      counter: function (i, n) { return i + " / " + n + " savol"; },
      level: function (n) { return n + " bosqich"; },
      resultTitle: "Diagnostika natijasi",
      known: function (done, total) { return total + " tadan " + done + " tasini bilasiz"; },
      skipped: "✓ marshrutdan chizildi",
      toLearn: "← shu yerdan boshlang",
      savedLine: function (date, passed, total) {
        return date + " dagi diagnostika: " + total + " bosqichdan " + passed + " tasi chizilgan.";
      },
      caveat:
        "Chizilgan bosqich — bepul o'tkazib yuborish emas: nazorat " +
        "nuqtalarini ko'zdan kechiring va ularni yodlamasdan bajara " +
        "olishingizga ishonch hosil qiling.",
    },
  })[lang];

  var PASS_OF = 3; // ≥3 из 4 вопросов уровня
  var STORE_KEY = "ftk_roadmap_diag_v1";

  var bank;
  try {
    bank = JSON.parse(bankEl.textContent);
  } catch (error) {
    return;
  }
  if (!Array.isArray(bank) || !bank.length) return;

  var style = document.createElement("style");
  style.textContent = [
    "#roadmap-diag{margin:1rem 0 1.4rem;padding:.9rem 1.1rem;border:1px solid var(--md-default-fg-color--lighter);border-radius:9px;background:var(--md-code-bg-color)}",
    ".rd-intro{margin:.2rem 0 .7rem;font-size:.88rem}",
    ".rd-btn{padding:.48rem .95rem;border-radius:6px;border:1px solid transparent;cursor:pointer;font-weight:650;background:#3b82f6;color:#fff}",
    ".rd-btn:hover{filter:brightness(1.08)}",
    ".rd-btn--ghost{background:transparent;color:var(--md-default-fg-color);border-color:var(--md-default-fg-color--lighter)}",
    ".rd-counter{font-size:.8rem;color:var(--md-default-fg-color--light);margin-bottom:.35rem}",
    ".rd-q{font-weight:650;margin:.25rem 0 .6rem}",
    ".rd-opts{display:grid;gap:.45rem}",
    ".rd-opt{text-align:left;padding:.55rem .8rem;border-radius:7px;border:1px solid var(--md-default-fg-color--lighter);background:var(--md-default-bg-color);color:var(--md-default-fg-color);cursor:pointer;font-size:.88rem}",
    ".rd-opt:hover{border-color:#3b82f6}",
    ".rd-levels{display:grid;gap:.35rem;margin:.6rem 0}",
    ".rd-row{display:flex;justify-content:space-between;gap:.6rem;font-size:.88rem;padding:.35rem .6rem;border-radius:6px;background:var(--md-default-bg-color)}",
    ".rd-row--pass{border-left:3px solid #2dd4bf}",
    ".rd-row--fail{border-left:3px solid #facc15}",
    ".rd-caveat{font-size:.8rem;color:var(--md-default-fg-color--light);margin:.6rem 0}",
    ".rd-saved{font-size:.82rem;margin:.15rem 0 .6rem}",
    ".rd-actions{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.5rem}",
    ".fx-rm__item--known{opacity:.55}",
    ".fx-rm__item--known .fx-rm__title{text-decoration:line-through}",
    ".fx-rm__known{display:inline-block;margin-left:.45rem;padding:.05rem .45rem;border-radius:9px;background:#2dd4bf;color:#0d1117;font-size:.68rem;font-weight:700;vertical-align:middle}",
  ].join("");
  document.head.appendChild(style);

  var questions = [];
  var idx = 0;
  var perLevel = {}; // level -> {got, total}

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function load() {
    try {
      var saved = JSON.parse(localStorage.getItem(STORE_KEY) || "null");
      if (saved && saved.v === 1 && saved.passed) return saved;
    } catch (error) {}
    return null;
  }

  function store(passed, scores) {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        v: 1,
        passed: passed,
        scores: scores,
        date: new Date().toISOString().slice(0, 10),
      }));
    } catch (error) {}
  }

  function levelsInBank() {
    var seen = {};
    bank.forEach(function (q) { seen[q.level] = true; });
    return Object.keys(seen).map(Number).sort(function (a, b) { return a - b; });
  }

  /* Отметки на карте: вычеркивание + бейдж. Бейдж — не только зачёркивание:
     дальтоник и печать не различают «бледнее», а слово «знаешь» видно всем. */
  function applyMarks(passed) {
    document.querySelectorAll(".fx-rm__item[data-level]").forEach(function (item) {
      var level = Number(item.getAttribute("data-level"));
      var known = passed.indexOf(level) >= 0;
      item.classList.toggle("fx-rm__item--known", known);
      var title = item.querySelector(".fx-rm__title");
      if (!title) return;
      var badge = title.querySelector(".fx-rm__known");
      if (known && !badge) {
        badge = document.createElement("span");
        badge.className = "fx-rm__known";
        badge.textContent = "✓";
        title.appendChild(badge);
      } else if (!known && badge) {
        badge.remove();
      }
    });
  }

  function shuffle(items) {
    var copy = items.slice();
    for (var i = copy.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = copy[i];
      copy[i] = copy[j];
      copy[j] = tmp;
    }
    return copy;
  }

  function renderIntro() {
    var saved = load();
    applyMarks(saved ? saved.passed : []);
    var levels = levelsInBank();
    root.innerHTML =
      '<p class="rd-intro">' + esc(S.intro) + "</p>" +
      (saved
        ? '<p class="rd-saved"><strong>' +
          esc(S.savedLine(saved.date, saved.passed.length, levels.length)) +
          "</strong></p>"
        : "") +
      '<div class="rd-actions">' +
      '<button class="rd-btn" id="rd-start">' + esc(saved ? S.retake : S.start) + "</button>" +
      (saved
        ? '<button class="rd-btn rd-btn--ghost" id="rd-reset">' + esc(S.reset) + "</button>"
        : "") +
      "</div>";
    document.getElementById("rd-start").addEventListener("click", startQuiz);
    if (saved) {
      document.getElementById("rd-reset").addEventListener("click", function () {
        try { localStorage.removeItem(STORE_KEY); } catch (error) {}
        applyMarks([]);
        renderIntro();
      });
    }
  }

  function startQuiz() {
    questions = shuffle(bank);
    idx = 0;
    perLevel = {};
    levelsInBank().forEach(function (level) {
      perLevel[level] = { got: 0, total: 0 };
    });
    renderQuestion();
  }

  function renderQuestion() {
    var q = questions[idx];
    var options = shuffle(
      q.options.map(function (text, optionIdx) {
        return { text: text, correct: optionIdx === q.answer };
      })
    );
    root.innerHTML =
      '<div class="rd-counter">' + esc(S.counter(idx + 1, questions.length)) +
      " · " + esc(S.level(q.level)) + "</div>" +
      '<div class="rd-q">' + esc(q.q) + "</div>" +
      '<div class="rd-opts">' +
      options.map(function (option, i) {
        return '<button class="rd-opt" data-i="' + i + '">' + esc(option.text) + "</button>";
      }).join("") +
      "</div>";
    root.querySelectorAll(".rd-opt").forEach(function (button) {
      button.addEventListener("click", function () {
        var option = options[Number(button.getAttribute("data-i"))];
        perLevel[q.level].total++;
        if (option.correct) perLevel[q.level].got++;
        idx++;
        if (idx < questions.length) renderQuestion();
        else renderResult();
      });
    });
  }

  function renderResult() {
    var levels = levelsInBank();
    var passed = levels.filter(function (level) {
      return perLevel[level].got >= PASS_OF;
    });
    store(passed, perLevel);
    applyMarks(passed);

    var rows = levels.map(function (level) {
      var ok = passed.indexOf(level) >= 0;
      return (
        '<div class="rd-row ' + (ok ? "rd-row--pass" : "rd-row--fail") + '"><span>' +
        esc(S.level(level)) + " — " + esc(S.known(perLevel[level].got, perLevel[level].total)) +
        "</span><span>" + esc(ok ? S.skipped : S.toLearn) + "</span></div>"
      );
    }).join("");

    root.innerHTML =
      '<div class="rd-q">' + esc(S.resultTitle) + "</div>" +
      '<div class="rd-levels">' + rows + "</div>" +
      '<p class="rd-caveat">' + esc(S.caveat) + "</p>" +
      '<div class="rd-actions"><button class="rd-btn" id="rd-again">' + esc(S.retake) + "</button></div>";
    document.getElementById("rd-again").addEventListener("click", startQuiz);
    if (window.fxTrack) window.fxTrack("roadmap_diag_done");
  }

  renderIntro();
})();
