/* ==========================================================================
   Forex Toolkit — мини-квиз в конце главы гайда
   3 вопроса по материалу страницы: мгновенная обратная связь с объяснением,
   лучший результат в localStorage (fx-quiz-v1). Глава, сданная на 3/3,
   автоматически отмечается прочитанной в трекере прогресса (fx-progress-v1) —
   так результат квиза виден и в общем кабинете.

   Вопросы лежат в JSON-блоке страницы (#chapter-quiz-questions), уже в
   локали страницы. Варианты перемешиваются на каждую попытку (как на
   экзамене), правильный ищется по тексту после перемешивания — поэтому
   тексты вариантов внутри вопроса не должны повторяться (держит unit-тест).
   ========================================================================== */

(function () {
  "use strict";

  var STORAGE_KEY = "fx-quiz-v1";

  var LABELS = {
    ru: {
      title: "Проверь себя: 3 вопроса по главе",
      start: "▶ Начать квиз",
      counter: function (i, n) { return "Вопрос " + i + " из " + n; },
      next: "Дальше",
      best: function (s, n) { return "Лучший результат: " + s + " из " + n; },
      notYet: "Квиз ещё не пройден — ответь на все три верно.",
      passedTitle: "✅ Глава усвоена — 3 из 3!",
      passedBody: "Глава отмечена прочитанной. Результат виден в общем кабинете.",
      failTitle: function (s) { return "Пока " + s + " из 3 — нужно 3 из 3."; },
      failBody: "Перечитай разделы по ошибкам выше и попробуй снова — это займёт минуту.",
      retake: "↻ Пройти заново",
      mistakes: function (n) { return "🔁 Ошибки добавлены во флеш-карточки: " + n + "."; },
      mistakesLink: "Повторить →",
      nextTitle: "🧭 Что дальше",
      nextChapter: "Следующая глава по маршруту:",
      quizzes: function (n, t) { return "Квизов глав сдано: " + n + " из " + t + "."; },
      refresh: "Освежи:",
      refreshWhy: "квиз сдан больше трёх недель назад.",
      examTime: "Все главы с квизами усвоены — пора на итоговый экзамен:",
      practice: "Главы и экзамен пройдены. Теперь — практика:",
      cabinet: "Весь прогресс — в личном кабинете →"
    },
    en: {
      title: "Check yourself: 3 questions on this chapter",
      start: "▶ Start the quiz",
      counter: function (i, n) { return "Question " + i + " of " + n; },
      next: "Next",
      best: function (s, n) { return "Best result: " + s + " of " + n; },
      notYet: "Quiz not passed yet — answer all three correctly.",
      passedTitle: "✅ Chapter mastered — 3 out of 3!",
      passedBody: "The chapter is marked as read. The result shows up in your dashboard.",
      failTitle: function (s) { return s + " of 3 so far — you need 3 of 3."; },
      failBody: "Re-read the sections behind the misses above and try again — it takes a minute.",
      retake: "↻ Retake",
      mistakes: function (n) { return "🔁 Misses added to your flashcards: " + n + "."; },
      mistakesLink: "Review them →",
      nextTitle: "🧭 What's next",
      nextChapter: "Next chapter on the route:",
      quizzes: function (n, t) { return "Chapter quizzes passed: " + n + " of " + t + "."; },
      refresh: "Refresh:",
      refreshWhy: "you passed this quiz more than three weeks ago.",
      examTime: "Every chapter with a quiz is mastered — time for the final exam:",
      practice: "Chapters and the exam are done. Now — practice:",
      cabinet: "All your progress is in the dashboard →"
    },
    uz: {
      title: "O'zingni sinash: bob bo'yicha 3 ta savol",
      start: "▶ Viktorinani boshlash",
      counter: function (i, n) { return i + " / " + n + " savol"; },
      next: "Keyingi",
      best: function (s, n) { return "Eng yaxshi natija: " + n + " dan " + s + " ta"; },
      notYet: "Viktorina hali topshirilmadi — uchtalasiga ham to'g'ri javob bering.",
      passedTitle: "✅ Bob o'zlashtirildi — 3 dan 3!",
      passedBody: "Bob o'qilgan deb belgilandi. Natija umumiy kabinetda ko'rinadi.",
      failTitle: function (s) { return "Hozircha 3 dan " + s + " — 3 dan 3 kerak."; },
      failBody: "Yuqoridagi xatolar bo'limga qarab qayta o'qing va yana urinib ko'ring — bir daqiqa oladi.",
      retake: "↻ Qayta topshirish",
      mistakes: function (n) { return "🔁 Xatolar flesh-kartochkalarga qo'shildi: " + n + " ta."; },
      mistakesLink: "Takrorlash →",
      nextTitle: "🧭 Keyingi qadam",
      nextChapter: "Yo'nalish bo'yicha keyingi bob:",
      quizzes: function (n, t) { return "Bob kvizlari topshirildi: " + t + " tadan " + n + " ta."; },
      refresh: "Yangilang:",
      refreshWhy: "kviz uch haftadan oldin topshirilgan.",
      examTime: "Kvizli barcha boblar o'zlashtirildi — yakuniy imtihon vaqti:",
      practice: "Boblar va imtihon topshirildi. Endi — amaliyot:",
      cabinet: "Barcha natijalar — shaxsiy kabinetda →"
    }
  };

  /* «Что дальше» в конце главы: вместо статичных ссылок — следующий шаг по
     маршруту с учётом сданных квизов. Маршрут — 21 глава с квизом в порядке
     навигации сайта (mkdocs.yml). dashboard.js держит ту же карту в
     CHAPTER_PATHS; синхронность и порядок проверяет tests/test_whats_next.py. */
  var ROUTE = [
    ["technical-analysis", "docs/technical-analysis/"],
    ["strategy-details", "docs/strategy-details/"],
    ["real-analysis", "docs/real-analysis/"],
    ["order-types-mechanics", "docs/order-types-mechanics/"],
    ["fundamental-analysis-guide", "docs/fundamental-analysis-guide/"],
    ["broker-mechanics-101", "docs/broker-mechanics-101/"],
    ["gold-trading", "practice/gold-trading/"],
    ["lot-discipline", "practice/lot-discipline/"],
    ["breakeven-protocol", "practice/breakeven-protocol/"],
    ["scaling-in", "practice/scaling-in/"],
    ["cycle-theory", "practice/cycle-theory/"],
    ["market-structure", "practice/market-structure/"],
    ["news-trading-protocol", "practice/news-trading-protocol/"],
    ["trading-sessions", "practice/trading-sessions/"],
    ["order-flow-volume-profile", "growth/order-flow-volume-profile/"],
    ["crypto-trading-guide", "growth/crypto-trading-guide/"],
    ["stocks-basics", "growth/stocks-basics/"],
    ["withdrawal-guide", "uz/withdrawal-guide/"],
    ["scam-protection", "uz/scam-protection/"],
    ["law-faq", "uz/law-faq/"],
    ["swap-free", "uz/swap-free/"]
  ];
  var RETAKE_AFTER_DAYS = 21; // как в кабинете: столько дней квиз считается свежим

  // results — fx-quiz-v1, current — ключ квиза этой страницы, nowMs — сейчас.
  // Пока квиз главы не сдан, шаг один — сдать его («quiz»). Дальше — первая
  // несданная глава после текущей (потом пропущенные раньше), а когда все
  // сданы — «done». refresh — сданная давно глава, которую стоит освежить.
  function nextStep(results, current, nowMs) {
    function passed(k) { return !!(results[k] && results[k].passed); }
    if (!passed(current)) return { kind: "quiz", key: current, refresh: null, passed: 0 };
    var keys = ROUTE.map(function (r) { return r[0]; });
    var at = keys.indexOf(current);
    var order = keys.slice(at + 1).concat(keys.slice(0, Math.max(at, 0)));
    var next = order.filter(function (k) { return !passed(k); })[0] || null;
    var refresh = keys.filter(function (k) {
      var when = results[k] && results[k].passed ? new Date(results[k].updatedAt).getTime() : NaN;
      return k !== current && nowMs - when > RETAKE_AFTER_DAYS * 864e5;
    })[0] || null;
    return { kind: next ? "next" : "done", key: next, refresh: refresh, passed: keys.filter(passed).length };
  }
  window.__fxNextStep = nextStep;

  // Ссылка и заголовок — из навигации страницы: так они в локали читателя.
  function navLink(path) {
    var plain = path.replace(/\/+$/, "");
    var anchors = document.querySelectorAll(".md-nav--primary .md-nav__link[href]");
    for (var i = 0; i < anchors.length; i++) {
      try {
        var url = new URL(anchors[i].getAttribute("href"), location.href);
        if (url.pathname.replace(/\/+$/, "").slice(-plain.length - 1) === "/" + plain) {
          return { href: url.pathname, title: anchors[i].textContent.trim() };
        }
      } catch (e) {}
    }
    return null;
  }

  // Ссылка на страницу из навигации; text — своя подпись вместо заголовка.
  function anchor(path, text) {
    var l = navLink(path);
    return l ? '<a href="' + escHtml(l.href) + '">' + escHtml(text || l.title) + "</a>" : null;
  }

  function routePath(key) {
    var hit = ROUTE.filter(function (r) { return r[0] === key; })[0];
    return hit ? hit[1] : "";
  }

  function renderNext(box, S, quizKey) {
    var out = box.querySelector(".chapter-quiz__next");
    if (!out) {
      out = document.createElement("div");
      out.className = "chapter-quiz__next";
      out.setAttribute("aria-live", "polite");
      box.appendChild(out);
    }
    var step = nextStep(readResults(), quizKey, Date.now());
    if (step.kind === "quiz") { out.hidden = true; return; }
    var lines = [];
    if (step.kind === "next") {
      var link = anchor(routePath(step.key));
      if (link) lines.push(S.nextChapter + " " + link);
    } else {
      var examPassed = false;
      try { examPassed = localStorage.getItem("forex_exam_passed") === "1"; } catch (e) {}
      var tools = examPassed
        ? [anchor("tools/news-simulator/"), anchor("tools/demo-readiness/")].filter(Boolean).join(" · ")
        : anchor("tools/exam/");
      if (tools) lines.push((examPassed ? S.practice : S.examTime) + " " + tools);
    }
    var refresh = step.refresh && anchor(routePath(step.refresh));
    if (refresh) lines.push(S.refresh + " " + refresh + " — " + S.refreshWhy);
    lines.push(S.quizzes(step.passed, ROUTE.length));
    var cabinet = anchor("extras/dashboard/", S.cabinet);
    if (cabinet) lines.push(cabinet);
    out.innerHTML = "<strong>" + S.nextTitle + "</strong>" +
      lines.map(function (l) { return "<p>" + l + "</p>"; }).join("");
    out.hidden = false;
  }

  function t() {
    var code = (document.documentElement.lang || "ru").slice(0, 2);
    return LABELS[code] || LABELS.ru;
  }

  function readResults() {
    try {
      var parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
    } catch (e) {
      return {};
    }
  }

  function saveResult(key, score, total) {
    var results = readResults();
    var prev = results[key];
    var passed = score === total;
    results[key] = {
      score: Math.max(score, prev && prev.score ? prev.score : 0),
      total: total,
      passed: Boolean(passed || (prev && prev.passed)),
      attempts: (prev && prev.attempts ? prev.attempts : 0) + 1,
      updatedAt: new Date().toISOString()
    };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(results)); } catch (e) {}
    return results[key];
  }

  /* Глава, сданная на 3/3, считается прочитанной: нажимаем кнопку трекера
     прогресса (если она на странице и глава ещё не отмечена), чтобы не
     дублировать его логику хранения. */
  function markChapterRead() {
    try {
      var done = JSON.parse(localStorage.getItem("fx-progress-v1") || "[]");
      if (done.indexOf(location.pathname) >= 0) return;
    } catch (e) { return; }
    var btn = document.querySelector(".fx-progress__btn");
    if (btn) btn.click();
  }

  // Адрес колоды берётся из DOM (ссылка логотипа) — перед вставкой в HTML экранируем.
  function escHtml(v) {
    return String(v).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function shuffled(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = a[i];
      a[i] = a[j];
      a[j] = tmp;
    }
    return a;
  }

  function build() {
    var host = document.getElementById("chapter-quiz");
    if (!host || host.dataset.ready === "1") return;
    var bankEl = document.getElementById("chapter-quiz-questions");
    if (!bankEl) return;
    var bank;
    try { bank = JSON.parse(bankEl.textContent); } catch (e) { return; }
    if (!Array.isArray(bank) || !bank.length) return;
    host.dataset.ready = "1";

    var S = t();
    var quizKey = host.getAttribute("data-quiz-key") || location.pathname;
    var questions = [];
    var idx = 0;
    var score = 0;
    var answered = false;
    var missed = [];

    host.innerHTML =
      '<div class="chapter-quiz__box">' +
      '<h2 class="chapter-quiz__title">' + S.title + "</h2>" +
      '<p class="chapter-quiz__best" id="cq-best"></p>' +
      '<div class="chapter-quiz__start" id="cq-start">' +
      '<button type="button" class="chapter-quiz__btn" id="cq-start-btn">' + S.start + "</button>" +
      "</div>" +
      '<div class="chapter-quiz__play" id="cq-play" hidden>' +
      '<p class="chapter-quiz__counter" id="cq-counter"></p>' +
      '<p class="chapter-quiz__question" id="cq-question"></p>' +
      '<div class="chapter-quiz__options" id="cq-options"></div>' +
      '<p class="chapter-quiz__explain" id="cq-explain" hidden></p>' +
      '<button type="button" class="chapter-quiz__btn" id="cq-next" hidden>' + S.next + "</button>" +
      "</div>" +
      '<div class="chapter-quiz__result" id="cq-result" hidden></div>' +
      "</div>";

    var el = function (id) { return document.getElementById(id); };

    function showBest() {
      var results = readResults();
      var r = results[quizKey];
      el("cq-best").textContent = r && r.passed
        ? S.best(r.score, r.total)
        : S.notYet;
      el("cq-best").classList.toggle("chapter-quiz__best--done", Boolean(r && r.passed));
    }

    function start() {
      // Каждая попытка перемешивает варианты: ответ запоминают по смыслу,
      // а не по позиции кнопки.
      questions = bank.map(function (item) {
        var correct = item.options[item.answer];
        var options = shuffled(item.options);
        return { q: item.q, options: options, answer: options.indexOf(correct), explain: item.explain };
      });
      idx = 0;
      score = 0;
      missed = [];
      el("cq-start").hidden = true;
      el("cq-result").hidden = true;
      el("cq-play").hidden = false;
      render();
    }

    function render() {
      answered = false;
      var q = questions[idx];
      el("cq-counter").textContent = S.counter(idx + 1, questions.length);
      el("cq-question").textContent = q.q;
      el("cq-explain").hidden = true;
      el("cq-next").hidden = true;
      var box = el("cq-options");
      box.innerHTML = "";
      q.options.forEach(function (text, i) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "chapter-quiz__option";
        btn.textContent = text;
        btn.addEventListener("click", function () { choose(i, btn); });
        box.appendChild(btn);
      });
    }

    function choose(i, btn) {
      if (answered) return;
      answered = true;
      var q = questions[idx];
      var buttons = el("cq-options").querySelectorAll(".chapter-quiz__option");
      for (var j = 0; j < buttons.length; j++) {
        buttons[j].disabled = true;
        if (j === q.answer) buttons[j].classList.add("chapter-quiz__option--correct");
      }
      if (i === q.answer) score++;
      else {
        btn.classList.add("chapter-quiz__option--wrong");
        missed.push({ q: q.q, a: q.options[q.answer], explain: q.explain, src: "quiz" });
      }
      var explain = el("cq-explain");
      explain.textContent = q.explain;
      explain.hidden = false;
      el("cq-next").hidden = false;
    }

    function finish() {
      el("cq-play").hidden = true;
      var total = questions.length;
      var record = saveResult(quizKey, score, total);
      var passed = score === total;
      if (passed) {
        markChapterRead();
        // Глава могла быть отмечена прочитанной раньше — тогда клик по
        // кнопке прогресса не происходит, а день в стрик записать надо.
        if (window.fxActivity) window.fxActivity();
        if (window.fxTrack) window.fxTrack("chapter_quiz_passed");
      }
      // Промахи уходят в персональные флеш-карточки (_mistake-cards.js).
      var saved = missed.length && window.FXMistakes ? window.FXMistakes.add(missed) : 0;
      var result = el("cq-result");
      result.innerHTML =
        '<div class="chapter-quiz__verdict ' + (passed ? "is-pass" : "is-fail") + '">' +
        "<strong>" + (passed ? S.passedTitle : S.failTitle(score)) + "</strong>" +
        "<p>" + (passed ? S.passedBody : S.failBody) + "</p>" +
        (saved ? "<p>" + S.mistakes(saved) + ' <a href="' + escHtml(window.FXMistakes.deckUrl()) + '">' + S.mistakesLink + "</a></p>" : "") +
        '<button type="button" class="chapter-quiz__btn" id="cq-retake">' + S.retake + "</button>" +
        "</div>";
      result.hidden = false;
      el("cq-retake").addEventListener("click", start);
      showBest();
      renderNext(host.querySelector(".chapter-quiz__box"), S, quizKey);
      return record;
    }

    el("cq-start-btn").addEventListener("click", start);
    el("cq-next").addEventListener("click", function () {
      idx++;
      if (idx < questions.length) render();
      else finish();
    });
    showBest();
    renderNext(host.querySelector(".chapter-quiz__box"), S, quizKey);
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(build);
  } else if (document.readyState !== "loading") {
    build();
  } else {
    document.addEventListener("DOMContentLoaded", build);
  }
})();
