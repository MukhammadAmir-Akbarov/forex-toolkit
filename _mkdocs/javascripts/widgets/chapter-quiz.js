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
      retake: "↻ Пройти заново"
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
      retake: "↻ Retake"
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
      retake: "↻ Qayta topshirish"
    }
  };

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
      else btn.classList.add("chapter-quiz__option--wrong");
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
        if (window.fxTrack) window.fxTrack("chapter_quiz_passed");
      }
      var result = el("cq-result");
      result.innerHTML =
        '<div class="chapter-quiz__verdict ' + (passed ? "is-pass" : "is-fail") + '">' +
        "<strong>" + (passed ? S.passedTitle : S.failTitle(score)) + "</strong>" +
        "<p>" + (passed ? S.passedBody : S.failBody) + "</p>" +
        '<button type="button" class="chapter-quiz__btn" id="cq-retake">' + S.retake + "</button>" +
        "</div>";
      result.hidden = false;
      el("cq-retake").addEventListener("click", start);
      showBest();
      return record;
    }

    el("cq-start-btn").addEventListener("click", start);
    el("cq-next").addEventListener("click", function () {
      idx++;
      if (idx < questions.length) render();
      else finish();
    });
    showBest();
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(build);
  } else if (document.readyState !== "loading") {
    build();
  } else {
    document.addEventListener("DOMContentLoaded", build);
  }
})();
