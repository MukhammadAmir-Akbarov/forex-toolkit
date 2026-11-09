/*
 * Дрель позиционного сайзинга — скорость счёта лота в голове.
 *
 * Разрыв, который она закрывает: калькулятор считает за тебя, экзамен спрашивает
 * «когда рисковать», а между ними на живом рынке есть секунды, в которые лот
 * надо назвать вслух. Здесь: 10 задач по 20 секунд, четыре варианта, честный
 * разбор формулы после каждого ответа.
 *
 * Формула одна и та же во всех задачах (пары с котировкой в USD, пипс лота =
 * $10): лот = (депозит × риск%) / (стоп × $10). Дистракторы — типовые ошибки:
 * ×10 (забыл про пипс), ÷10 (перепутал лот с мини) и удвоение риска.
 */
(function () {
  var root = document.getElementById("sizing-drill");
  if (!root || !window.FXW) return;

  var F = window.FXW;

  var T = F.pick({
    ru: {
      intro: "10 задач по 20 секунд: депозит, риск и стоп — назови лот. Считаем в уме, как на живом рынке.",
      start: "▶ Начать серию",
      question: function (dep, risk, stop) {
        return "Депозит $" + F.int(dep) + ", риск " + risk + "%, стоп " + stop + " пипсов. Какой лот?";
      },
      timeLeft: function (s) { return "⏱ " + s + " с"; },
      q: function (n, total) { return "Задача " + n + " из " + total; },
      correct: "✅ Верно",
      wrong: function (lot) { return "❌ Правильный ответ: " + lot; },
      timeout: function (lot) { return "⏱ Время вышло. Правильный ответ: " + lot; },
      formula: function (riskUsd, stop, lot) {
        return "Риск $" + riskUsd + " ÷ (" + stop + " пипсов × $10) = " + lot + " лота";
      },
      next: "Дальше",
      verdictGreat: "9–10 из 10 — сайзинг у тебя в пальцах. На рынке останется не ошибиться в спешке.",
      verdictOk: "6–8 из 10 — формула есть, скорости нет. Погоняй ещё серию: лот должен считаться быстрее, чем открывается терминал.",
      verdictBad: "Меньше 6 из 10 — пока считает калькулятор, а не ты. Разбери формулу под виджетом и вернись.",
      score: function (hits, done) { return "Счёт: " + hits + " из " + done; },
      best: function (v) { return "🏆 Лучшая серия: " + v + " из 10"; },
      again: "↻ Новая серия",
    },
    en: {
      intro: "10 problems, 20 seconds each: deposit, risk and stop — name the lot size. Mental math, like on a live market.",
      start: "▶ Start series",
      question: function (dep, risk, stop) {
        return "Deposit $" + F.int(dep) + ", risk " + risk + "%, stop " + stop + " pips. What is the lot size?";
      },
      timeLeft: function (s) { return "⏱ " + s + " s"; },
      q: function (n, total) { return "Problem " + n + " of " + total; },
      correct: "✅ Correct",
      wrong: function (lot) { return "❌ The right answer: " + lot; },
      timeout: function (lot) { return "⏱ Time is up. The right answer: " + lot; },
      formula: function (riskUsd, stop, lot) {
        return "Risk $" + riskUsd + " ÷ (" + stop + " pips × $10) = " + lot + " lots";
      },
      next: "Next",
      verdictGreat: "9–10 out of 10 — sizing is in your fingers. On the market, all that remains is not slipping in a hurry.",
      verdictOk: "6–8 out of 10 — the formula is there, the speed is not. Run another series: the lot should compute faster than the terminal opens.",
      verdictBad: "Under 6 out of 10 — the calculator is doing the thinking, not you. Read the formula below the widget and come back.",
      score: function (hits, done) { return "Score: " + hits + " of " + done; },
      best: function (v) { return "🏆 Best series: " + v + " of 10"; },
      again: "↻ New series",
    },
    uz: {
      intro: "10 ta masala, har biri 20 soniya: depozit, risk va stop — lotni ayting. Jonli bozordagidek, yoddan hisoblaymiz.",
      start: "▶ Seriyani boshlash",
      question: function (dep, risk, stop) {
        return "Depozit $" + F.int(dep) + ", risk " + risk + "%, stop " + stop + " pips. Lot qancha?";
      },
      timeLeft: function (s) { return "⏱ " + s + " s"; },
      q: function (n, total) { return total + " masaladan " + n + "-masala"; },
      correct: "✅ To'g'ri",
      wrong: function (lot) { return "❌ To'g'ri javob: " + lot; },
      timeout: function (lot) { return "⏱ Vaqt tugadi. To'g'ri javob: " + lot; },
      formula: function (riskUsd, stop, lot) {
        return "Risk $" + riskUsd + " ÷ (" + stop + " pips × $10) = " + lot + " lot";
      },
      next: "Keyingi",
      verdictGreat: "10 dan 9–10 — sayzing barmoqlaringizda. Bozorda shoshilinchda xato qilmaslik qoladi, xolos.",
      verdictOk: "10 dan 6–8 — formula bor, tezlik yo'q. Yana bir seriya: lot terminal ochilganidan tezroq hisoblanishi kerak.",
      verdictBad: "10 dan 6 dan kam — hozircha siz emas, kalkulyator o'ylayapti. Vidjet ostidagi formulani o'qing va qayting.",
      score: function (hits, done) { return done + " tadan " + hits + " ball"; },
      best: function (v) { return "🏆 Eng yaxshi seriya: 10 tadan " + v; },
      again: "↻ Yangi seriya",
    },
  });

  var QUESTIONS = 10;
  var SECONDS = 20;
  var STORE_KEY = "ftk_drill_best";

  var style = document.createElement("style");
  style.textContent = [
    "#sizing-drill{max-width:640px;margin:1.2rem 0}",
    ".sd-status{font-size:1.05rem;font-weight:700;margin:.6rem 0;min-height:1.6rem}",
    ".sd-meta{display:flex;justify-content:space-between;font-size:.8rem;color:var(--md-default-fg-color--light);margin:.3rem 0}",
    ".sd-timer{height:6px;border-radius:3px;background:var(--md-default-fg-color--lightest);overflow:hidden;margin:.4rem 0}",
    ".sd-timer-bar{height:100%;background:#3b82f6;transition:width .2s linear}",
    ".sd-timer-bar.sd-low{background:#f87171}",
    ".sd-options{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin:.7rem 0}",
    "@media(max-width:560px){.sd-options{grid-template-columns:1fr}}",
    ".sd-opt{padding:.8rem;border-radius:8px;cursor:pointer;font-weight:700;font-size:1.05rem;text-align:center;border:1px solid var(--md-default-fg-color--lighter);background:var(--md-code-bg-color);font-variant-numeric:tabular-nums}",
    ".sd-opt:not(:disabled):hover{border-color:#3b82f6}",
    ".sd-opt:disabled{cursor:default;opacity:.55}",
    ".sd-opt.sd-hit{background:rgba(45,212,191,.25);border-color:#2dd4bf;opacity:1}",
    ".sd-opt.sd-miss{background:rgba(248,113,113,.25);border-color:#f87171;opacity:1}",
    ".sd-explain{font-size:.84rem;color:var(--md-default-fg-color--light);min-height:1.3rem}",
    ".sd-btn{padding:.55rem 1.2rem;border-radius:6px;border:none;cursor:pointer;font-weight:700;font-size:.95rem;background:#3b82f6;color:#fff}",
    ".sd-verdict{margin-top:.7rem;padding:.7rem .9rem;border-left:3px solid #8b5cf6;background:rgba(139,92,246,.08);font-size:.88rem}",
  ].join("");
  document.head.appendChild(style);

  var best = 0;
  try { best = Number(localStorage.getItem(STORE_KEY)) || 0; } catch (e) {}

  var state = null; // {q, hits, problem, timer, left}
  var timer = null;

  function stopTimer() {
    if (timer !== null) {
      clearInterval(timer);
      timer = null;
    }
  }

  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  function makeProblem() {
    var dep = pick([500, 1000, 2000, 2500, 5000, 10000]);
    var risk = pick([0.5, 1, 1.5, 2]);
    var stop = pick([10, 15, 20, 25, 30, 40, 50]);
    var riskUsd = dep * risk / 100;
    var lot = Math.round((riskUsd / (stop * 10)) * 100) / 100;
    if (lot <= 0) lot = 0.01;
    var options = {};
    options[lot] = true;
    [lot * 10, lot / 10, lot * 2, lot / 2].forEach(function (v) {
      var rounded = Math.round(v * 100) / 100;
      if (rounded > 0) options[rounded] = true;
    });
    // Добиваем до четырёх вариантов правдоподобными соседями.
    var extra = lot;
    while (Object.keys(options).length < 4) {
      extra = Math.round((extra + 0.05) * 100) / 100;
      options[extra] = true;
    }
    return {
      dep: dep, risk: risk, stop: stop, riskUsd: Math.round(riskUsd),
      lot: lot,
      options: Object.keys(options).map(Number).sort(function (a, b) { return a - b; }).slice(0, 4),
    };
  }

  function fmtLot(v) {
    return (Math.round(v * 100) / 100).toFixed(2);
  }

  function startQuestion() {
    state.problem = makeProblem();
    state.left = SECONDS;
    render();
    timer = setInterval(function () {
      state.left -= 1;
      if (state.left <= 0) {
        answer(null);
      } else {
        var bar = document.getElementById("sd-timer-bar");
        var clock = document.getElementById("sd-clock");
        if (bar) {
          bar.style.width = (state.left / SECONDS * 100) + "%";
          bar.className = "sd-timer-bar" + (state.left <= 5 ? " sd-low" : "");
        }
        if (clock) clock.textContent = T.timeLeft(state.left);
      }
    }, 1000);
  }

  function answer(choice) {
    stopTimer();
    var problem = state.problem;
    var hit = choice === problem.lot;
    if (hit) state.hits++;
    state.last = { hit: hit, timeout: choice === null };
    state.phase = "feedback";
    render();
  }

  function render() {
    var problem = state.problem;
    if (state.phase === "feedback" || state.q > QUESTIONS) stopTimer();

    if (state.q > QUESTIONS) {
      if (state.hits > best) {
        best = state.hits;
        try { localStorage.setItem(STORE_KEY, String(best)); } catch (e) {}
      }
      var verdict = state.hits >= 9 ? T.verdictGreat : state.hits >= 6 ? T.verdictOk : T.verdictBad;
      root.innerHTML =
        '<div class="sd-status">' + F.escape(T.score(state.hits, QUESTIONS)) + "</div>" +
        '<div class="sd-verdict">' + F.escape(verdict) + "</div>" +
        '<div class="sd-meta"><span>' + (best ? F.escape(T.best(best)) : "") + "</span></div>" +
        '<button type="button" class="sd-btn" id="sd-again">' + F.escape(T.again) + "</button>";
      document.getElementById("sd-again").addEventListener("click", startSeries);
      return;
    }

    var status = "";
    var explain = "";
    var optionsHtml = "";
    var controls = "";

    if (state.phase === "ask") {
      status = F.escape(T.question(problem.dep, problem.risk, problem.stop));
      optionsHtml = problem.options.map(function (v) {
        return '<button type="button" class="sd-opt" data-v="' + v + '">' + fmtLot(v) + "</button>";
      }).join("");
    } else {
      var last = state.last;
      status = last.hit
        ? F.escape(T.correct)
        : F.escape(last.timeout ? T.timeout(fmtLot(problem.lot)) : T.wrong(fmtLot(problem.lot)));
      explain = F.escape(T.formula(problem.riskUsd, problem.stop, fmtLot(problem.lot)));
      optionsHtml = problem.options.map(function (v) {
        var cls = v === problem.lot ? " sd-hit" : (!last.hit && v === state.lastChoice ? " sd-miss" : "");
        return '<button type="button" class="sd-opt' + cls + '" disabled>' + fmtLot(v) + "</button>";
      }).join("");
      controls = '<button type="button" class="sd-btn" id="sd-next">' + F.escape(T.next) + "</button>";
    }

    root.innerHTML =
      '<div class="sd-meta"><span>' + F.escape(T.q(state.q, QUESTIONS)) + "</span>" +
      '<span id="sd-clock">' + F.escape(T.timeLeft(state.left)) + "</span></div>" +
      '<div class="sd-timer"><div class="sd-timer-bar' + (state.left <= 5 ? " sd-low" : "") +
      '" id="sd-timer-bar" style="width:' + (state.left / SECONDS * 100) + '%"></div></div>' +
      '<div class="sd-status">' + status + "</div>" +
      '<div class="sd-options">' + optionsHtml + "</div>" +
      '<div class="sd-explain">' + explain + "</div>" +
      '<div class="sd-meta"><span>' + F.escape(T.score(state.hits, state.phase === "feedback" ? state.q : state.q - 1)) + "</span><span>" +
      (best ? F.escape(T.best(best)) : "") + "</span></div>" +
      controls;

    root.querySelectorAll(".sd-opt[data-v]").forEach(function (button) {
      button.addEventListener("click", function () {
        state.lastChoice = Number(button.getAttribute("data-v"));
        answer(state.lastChoice);
      });
    });
    var next = document.getElementById("sd-next");
    if (next) {
      next.addEventListener("click", function () {
        state.q++;
        state.phase = "ask";
        startQuestion();
      });
    }
  }

  function startSeries() {
    stopTimer();
    state = { q: 1, hits: 0, phase: "ask", left: SECONDS, last: null, lastChoice: null };
    startQuestion();
  }

  root.innerHTML =
    "<p>" + F.escape(T.intro) + "</p>" +
    '<button type="button" class="sd-btn" id="sd-start">' + F.escape(T.start) + "</button>" +
    (best ? '<div class="sd-meta"><span>' + F.escape(T.best(best)) + "</span></div>" : "");
  document.getElementById("sd-start").addEventListener("click", startSeries);
})();
