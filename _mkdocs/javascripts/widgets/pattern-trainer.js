/*
 * Тренажёр свечных паттернов — с исходом, а не только с названием.
 *
 * Зачем именно так. Своя же страница проекта говорит: «никогда не торговать
 * только по паттерну», а экзамен — что стабильно угадывать направление не
 * получается ни у кого. Тренажёр вида «назови фигуру» учил бы обратному:
 * распознал молот — значит знаешь, куда пойдёт цена.
 *
 * Поэтому здесь два шага. Сначала студент называет фигуру (навык чтения
 * графика полезен). Затем сразу видит, чем такие фигуры кончались на этих же
 * архивных котировках — обычно около половины. Именно второе число делает
 * урок честным.
 *
 * Свечи берутся из тех же эпизодов, что и Replay: реальный архив, никакой
 * синтетики. Правила распознавания — зеркало forex_toolkit/candles.py,
 * статистика — зеркало forex_toolkit/pattern_outcomes.py; сверка в тестах.
 */
(function () {
  var root = document.getElementById("pattern-trainer");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var HORIZON = 5;      // через сколько свечей смотрим исход
  var MIN_MATCHES = 5;  // меньше — статистику не показываем
  var CONTEXT = 12;     // сколько свечей показываем вокруг фигуры

  var T = F.pick({
    ru: {
      loading: "Загружаю архивные свечи…",
      loadError: "Не удалось загрузить эпизоды. Обнови страницу.",
      question: "Какая фигура на последней свече?",
      none: "Ничего из перечисленного",
      check: "Ответить",
      next: "Следующая →",
      correct: "✅ Верно",
      wrong: "❌ Неверно",
      wasHere: function (name) { return "Здесь была фигура: " + name + "."; },
      wasNothing: "Здесь не было ни одной из перечисленных фигур.",
      outcomeTitle: "А теперь главное — чем такие фигуры кончались",
      outcome: function (name, worked, found, rate) {
        return name + ": в этом архиве найдена " + found + " раз, и цена ушла в «обещанную» сторону " +
          worked + " раз — это " + rate + ".";
      },
      thisOne: function (result) {
        return "Конкретно здесь через " + HORIZON + " свечей цена ушла " + result + ".";
      },
      up: "вверх", down: "вниз", flat: "в ноль",
      lesson: "Около половины — это и есть ответ на вопрос, предсказывает ли фигура движение. Распознать её полезно: она отмечает место, где стоит посмотреть внимательнее. Но вход по одной фигуре — это ставка на монетку с комиссией.",
      score: function (right, total) { return "Верно: " + right + " из " + total; },
      table: "Таблица свечей",
      candle: "Свеча", open: "Открытие", high: "Максимум", low: "Минимум", close: "Закрытие",
      names: {
        hammer: "Молот",
        shooting_star: "Падающая звезда",
        doji: "Доджи",
        bullish_engulfing: "Бычье поглощение",
        bearish_engulfing: "Медвежье поглощение"
      },
      dojiNote: function (share) {
        return "Доджи по стандартному правилу — " + share + " всех свечей архива. Фигура, которая встречается в каждой второй свече, ничего не выделяет.";
      }
    },
    en: {
      loading: "Loading archive candles…",
      loadError: "Could not load the episodes. Refresh the page.",
      question: "Which pattern is on the last candle?",
      none: "None of these",
      check: "Answer",
      next: "Next →",
      correct: "✅ Correct",
      wrong: "❌ Wrong",
      wasHere: function (name) { return "The pattern here was: " + name + "."; },
      wasNothing: "None of the listed patterns was here.",
      outcomeTitle: "And now the point — how these patterns resolved",
      outcome: function (name, worked, found, rate) {
        return name + ": found " + found + " times in this archive, and price went the promised way " +
          worked + " times — that is " + rate + ".";
      },
      thisOne: function (result) {
        return "Here specifically, " + HORIZON + " candles later price went " + result + ".";
      },
      up: "up", down: "down", flat: "nowhere",
      lesson: "About half — that is the answer to whether a shape predicts the move. Recognising it is useful: it marks a place worth a closer look. But entering on the shape alone is a coin flip with commission.",
      score: function (right, total) { return "Correct: " + right + " of " + total; },
      table: "Candle table",
      candle: "Candle", open: "Open", high: "High", low: "Low", close: "Close",
      names: {
        hammer: "Hammer",
        shooting_star: "Shooting star",
        doji: "Doji",
        bullish_engulfing: "Bullish engulfing",
        bearish_engulfing: "Bearish engulfing"
      },
      dojiNote: function (share) {
        return "By the standard rule a doji is " + share + " of every candle in the archive. A shape that appears in every other candle singles nothing out.";
      }
    },
    uz: {
      loading: "Arxiv shamlari yuklanmoqda…",
      loadError: "Epizodlarni yuklab bo'lmadi. Sahifani yangilang.",
      question: "Oxirgi shamda qaysi figura?",
      none: "Sanab o'tilganlardan hech biri",
      check: "Javob berish",
      next: "Keyingisi →",
      correct: "✅ To'g'ri",
      wrong: "❌ Noto'g'ri",
      wasHere: function (name) { return "Bu yerdagi figura: " + name + "."; },
      wasNothing: "Bu yerda sanab o'tilgan figuralardan hech biri bo'lmagan.",
      outcomeTitle: "Endi eng muhimi — bunday figuralar nima bilan tugagan",
      outcome: function (name, worked, found, rate) {
        return name + ": bu arxivda " + found + " marta topilgan va narx «va'da qilingan» tomonga " +
          worked + " marta ketgan — bu " + rate + ".";
      },
      thisOne: function (result) {
        return "Aynan shu yerda " + HORIZON + " ta shamdan keyin narx " + result + " ketgan.";
      },
      up: "yuqoriga", down: "pastga", flat: "nolga",
      lesson: "Taxminan yarmi — figura harakatni bashorat qiladimi degan savolga javob shu. Uni tanish foydali: u diqqat bilan qaraladigan joyni belgilaydi. Lekin faqat figura bo'yicha kirish — komissiyali tanga tashlash.",
      score: function (right, total) { return "To'g'ri: " + total + " dan " + right; },
      table: "Shamlar jadvali",
      candle: "Sham", open: "Ochilish", high: "Maksimum", low: "Minimum", close: "Yopilish",
      names: {
        hammer: "Bolg'a",
        shooting_star: "Uchayotgan yulduz",
        doji: "Doji",
        bullish_engulfing: "Buqa yutishi",
        bearish_engulfing: "Ayiq yutishi"
      },
      dojiNote: function (share) {
        return "Standart qoida bo'yicha doji — arxivdagi barcha shamlarning " + share + " qismi. Har ikkinchi shamda uchraydigan figura hech narsani ajratmaydi.";
      }
    }
  });

  // ── Правила распознавания: зеркало forex_toolkit/candles.py ──────────────
  function body(c) { return Math.abs(c.close - c.open); }
  function isBullish(c) { return c.close > c.open; }
  function isBearish(c) { return c.close < c.open; }
  function upperShadow(c) { return c.high - Math.max(c.open, c.close); }
  function lowerShadow(c) { return Math.min(c.open, c.close) - c.low; }

  function isHammer(c) {
    var b = body(c);
    if (b === 0) return false;
    return lowerShadow(c) >= 2 * b && upperShadow(c) < b;
  }
  function isShootingStar(c) {
    var b = body(c);
    if (b === 0) return false;
    return upperShadow(c) >= 2 * b && lowerShadow(c) < b;
  }
  function isDoji(c) {
    var range = c.high - c.low;
    if (range === 0) return false;
    return body(c) / range < 0.1;
  }
  function isBullishEngulfing(prev, curr) {
    return isBearish(prev) && isBullish(curr) &&
      curr.close > prev.open && curr.open < prev.close && body(curr) > body(prev);
  }
  function isBearishEngulfing(prev, curr) {
    return isBullish(prev) && isBearish(curr) &&
      curr.close < prev.open && curr.open > prev.close && body(curr) > body(prev);
  }

  // ключ -> куда фигура «обещает» движение
  var PROMISE = {
    hammer: "up", shooting_star: "down", doji: "none",
    bullish_engulfing: "up", bearish_engulfing: "down"
  };

  function findPatterns(candles) {
    var found = [];
    for (var i = 0; i < candles.length; i++) {
      var c = candles[i];
      if (isHammer(c)) found.push({ index: i, key: "hammer" });
      if (isShootingStar(c)) found.push({ index: i, key: "shooting_star" });
      if (isDoji(c)) found.push({ index: i, key: "doji" });
      if (i >= 1) {
        var p = candles[i - 1];
        if (isBullishEngulfing(p, c)) found.push({ index: i, key: "bullish_engulfing" });
        if (isBearishEngulfing(p, c)) found.push({ index: i, key: "bearish_engulfing" });
      }
    }
    return found;
  }

  function outcomeAfter(candles, index, horizon) {
    var target = index + horizon;
    if (target >= candles.length) return "";
    var start = candles[index].close, finish = candles[target].close;
    if (finish > start) return "up";
    if (finish < start) return "down";
    return "flat";
  }

  function collectStats(series, horizon) {
    var counters = {};
    Object.keys(PROMISE).forEach(function (k) { counters[k] = { found: 0, worked: 0, flat: 0 }; });
    series.forEach(function (candles) {
      findPatterns(candles).forEach(function (m) {
        var result = outcomeAfter(candles, m.index, horizon);
        if (!result) return;
        var promised = PROMISE[m.key];
        counters[m.key].found++;
        if (result === "flat") counters[m.key].flat++;
        else if (promised !== "none" && result === promised) counters[m.key].worked++;
      });
    });
    Object.keys(counters).forEach(function (k) {
      var c = counters[k];
      var moved = c.found - c.flat;
      c.rate = moved ? c.worked / moved : 0;
      c.key = k;
    });
    return counters;
  }

  function decodeEpisode(episode) {
    var base = episode.base, pip = episode.pip;
    return episode.k.map(function (c) {
      return { open: base + c[0] * pip, high: base + c[1] * pip, low: base + c[2] * pip, close: base + c[3] * pip };
    });
  }

  window.__fxPatternStats = function (series, horizon) {
    return collectStats(series || [], horizon || HORIZON);
  };
  window.__fxFindPatterns = findPatterns;
  window.__fxPatternOutcome = function (candles, index, horizon) {
    return outcomeAfter(candles, index, horizon || HORIZON);
  };

  // ── Тренажёр ────────────────────────────────────────────────────────────
  var series = [], stats = null, questions = [], current = 0, right = 0, answered = false;

  root.innerHTML = '<p id="pt-loading">' + F.escape(T.loading) + "</p>";

  var source = root.getAttribute("data-src");
  fetch(source)
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (document_) {
      series = (document_.episodes || []).map(decodeEpisode);
      if (!series.length) throw new Error("empty");
      stats = collectStats(series, HORIZON);
      questions = buildQuestions();
      render();
    })
    .catch(function () {
      root.innerHTML = '<p class="calc-result calc-error">' + F.escape(T.loadError) + "</p>";
    });

  function shuffled(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function buildQuestions() {
    // Берём места, где фигура есть, и места, где её нет: иначе «что-то есть
    // всегда» становится выигрышной стратегией, и упражнение обесценивается.
    var withPattern = [], without = [];
    series.forEach(function (candles, episode) {
      var marks = {};
      findPatterns(candles).forEach(function (m) {
        // Доджи встречается почти в каждой второй свече — в вопросы его не
        // берём, иначе он забьёт выборку. В статистике ниже он остаётся.
        if (m.key !== "doji") (marks[m.index] = marks[m.index] || []).push(m.key);
      });
      Object.keys(marks).forEach(function (index) {
        index = parseInt(index, 10);
        if (index >= CONTEXT && index + HORIZON < candles.length && marks[index].length === 1) {
          withPattern.push({ episode: episode, index: index, key: marks[index][0] });
        }
      });
      for (var i = CONTEXT; i + HORIZON < candles.length; i += 7) {
        if (!marks[i] && !findPatterns(candles.slice(i - 1, i + 1)).length) {
          without.push({ episode: episode, index: i, key: null });
        }
      }
    });
    return shuffled(shuffled(withPattern).slice(0, 8).concat(shuffled(without).slice(0, 2)));
  }

  function candleTable(candles, from, to, markIndex) {
    var rows = "";
    for (var i = from; i <= to; i++) {
      var c = candles[i];
      var digits = c.close > 50 ? 3 : 5;
      rows += "<tr" + (i === markIndex ? ' class="pt-mark"' : "") + "><th scope=\"row\">" +
        (i - from + 1) + (i === markIndex ? " ←" : "") + "</th>" +
        "<td>" + c.open.toFixed(digits) + "</td><td>" + c.high.toFixed(digits) + "</td>" +
        "<td>" + c.low.toFixed(digits) + "</td><td>" + c.close.toFixed(digits) + "</td></tr>";
    }
    return '<div class="pt-scroll"><table class="pt-table"><caption>' + F.escape(T.table) +
      "</caption><thead><tr><th>" + F.escape(T.candle) + "</th><th>" + F.escape(T.open) +
      "</th><th>" + F.escape(T.high) + "</th><th>" + F.escape(T.low) + "</th><th>" +
      F.escape(T.close) + "</th></tr></thead><tbody>" + rows + "</tbody></table></div>";
  }

  function render() {
    answered = false;
    if (current >= questions.length) return renderSummary();
    var q = questions[current];
    var candles = series[q.episode];
    var options = shuffled(Object.keys(PROMISE).filter(function (k) { return k !== "doji"; }));

    root.innerHTML =
      '<p class="pt-progress">' + F.escape(T.score(right, questions.length)) + " · " +
      (current + 1) + " / " + questions.length + "</p>" +
      candleTable(candles, q.index - CONTEXT + 1, q.index, q.index) +
      "<h3>" + F.escape(T.question) + "</h3>" +
      '<div class="pt-options">' +
      options.map(function (key) {
        return '<button type="button" class="pt-option" data-key="' + key + '">' +
          F.escape(T.names[key]) + "</button>";
      }).join("") +
      '<button type="button" class="pt-option" data-key="">' + F.escape(T.none) + "</button>" +
      "</div><div id=\"pt-verdict\" role=\"status\" aria-live=\"polite\"></div>";

    root.querySelectorAll(".pt-option").forEach(function (button) {
      button.addEventListener("click", function () { answer(button.getAttribute("data-key")); });
    });
  }

  function answer(key) {
    if (answered) return;
    answered = true;
    var q = questions[current];
    var candles = series[q.episode];
    var correct = (key || null) === q.key;
    if (correct) right++;

    root.querySelectorAll(".pt-option").forEach(function (button) {
      button.disabled = true;
      if ((button.getAttribute("data-key") || null) === q.key) button.classList.add("pt-correct");
      else if (button.getAttribute("data-key") === key) button.classList.add("pt-wrong");
    });

    var result = outcomeAfter(candles, q.index, HORIZON);
    var lines = ["<p><strong>" + (correct ? F.escape(T.correct) : F.escape(T.wrong)) + ".</strong> " +
      F.escape(q.key ? T.wasHere(T.names[q.key]) : T.wasNothing) + "</p>"];

    if (q.key) {
      var s = stats[q.key];
      lines.push("<h4>" + F.escape(T.outcomeTitle) + "</h4>");
      lines.push("<p>" + F.escape(T.thisOne(T[result] || result)) + "</p>");
      if (s.found >= MIN_MATCHES) {
        lines.push("<p><strong>" + F.escape(T.outcome(
          T.names[q.key], s.worked, s.found, F.pct(Math.round(s.rate * 1000) / 10)
        )) + "</strong></p>");
      }
      lines.push('<p class="pt-lesson">' + F.escape(T.lesson) + "</p>");
    }
    lines.push('<button type="button" class="calc-button" id="pt-next">' + F.escape(T.next) + "</button>");

    var verdict = document.getElementById("pt-verdict");
    verdict.innerHTML = lines.join("");
    document.getElementById("pt-next").addEventListener("click", function () {
      current++;
      render();
    });
    if (window.fxTrack) window.fxTrack("pattern_trainer_answered", { once: false });
  }

  function renderSummary() {
    var total = 0, dojiFound = stats.doji ? stats.doji.found : 0;
    series.forEach(function (c) { total += c.length; });
    var rows = Object.keys(PROMISE).filter(function (k) { return PROMISE[k] !== "none"; })
      .map(function (key) {
        var s = stats[key];
        return "<tr><th scope=\"row\">" + F.escape(T.names[key]) + "</th><td>" + s.found +
          "</td><td>" + s.worked + "</td><td>" + F.pct(Math.round(s.rate * 1000) / 10) + "</td></tr>";
      }).join("");

    root.innerHTML =
      '<div class="calc-result calc-warn"><h3>' + F.escape(T.score(right, questions.length)) + "</h3>" +
      "<h4>" + F.escape(T.outcomeTitle) + "</h4>" +
      '<div class="pt-scroll"><table class="pt-table"><thead><tr><th></th><th>n</th><th>✓</th><th>%</th></tr></thead><tbody>' +
      rows + "</tbody></table></div>" +
      "<p>" + F.escape(T.dojiNote(F.pct(Math.round(dojiFound / total * 1000) / 10))) + "</p>" +
      '<p class="pt-lesson">' + F.escape(T.lesson) + "</p>" +
      '<button type="button" class="calc-button" id="pt-restart">↻</button></div>';

    document.getElementById("pt-restart").addEventListener("click", function () {
      current = 0; right = 0; questions = buildQuestions(); render();
    });
  }
})();
