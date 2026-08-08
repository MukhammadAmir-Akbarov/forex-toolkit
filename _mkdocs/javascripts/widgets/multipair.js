/*
 * Переносится ли настройка стратегии с одной пары на другие.
 *
 * Соседняя мысль к странице про переобучение. Там настройка не переносилась во
 * времени, здесь — между рынками. И снова читатель сначала отвечает сам:
 * «на скольких парах из N эти параметры остались в плюсе?». Ответ вслух дороже
 * прочитанного вывода: своя ошибка запоминается, чужое утверждение — нет.
 *
 * Числа посчитаны на реальных котировках (tools/multipair_scan.py) и
 * зафиксированы в data/multipair.json. Сводка — зеркало
 * forex_toolkit/multipair.py, сверка в тестах.
 */
(function () {
  var root = document.getElementById("multipair");
  if (!root || !window.FXW) return;

  var F = window.FXW;

  var T = F.pick({
    ru: {
      loading: "Загружаю результаты по парам…",
      loadError: "Не удалось загрузить данные. Обнови страницу.",
      intro: function (pair, params) {
        return (
          "Параметры, оказавшиеся лучшими на " + pair + ": " + params +
          ". Дальше они применяются без изменений к остальным парам."
        );
      },
      guess: function (n) {
        return "На скольких из " + n + " пар эти параметры остались в плюсе?";
      },
      colPair: "Пара",
      colTransferred: "Перенос, R",
      colTrades: "Сделок",
      colOwn: "Своё лучшее, R",
      colOwnParams: "Свои лучшие параметры",
      home: "опорная",
      tooFew: "мало сделок",
      answer: function (guessed, real, total) {
        return guessed === real
          ? "Точно: " + real + " из " + total + "."
          : "Ты сказал " + guessed + ", на самом деле " + real + " из " + total + ".";
      },
      spread: function (best, bestR, worst, worstR) {
        return "Лучшая пара — " + best + " (" + bestR + "), худшая — " + worst + " (" + worstR + ").";
      },
      ownDiffer: function (n, total) {
        return "У " + n + " пар из " + total + " свои лучшие параметры — не те, что на опорной паре.";
      },
      lesson:
        "Если у каждой пары свои «лучшие» параметры, то «лучшие» — свойство не " +
        "стратегии, а выборки. Это то же переобучение, только вдоль другой оси.",
      again: "Ответить заново",
    },
    en: {
      loading: "Loading the per-pair results…",
      loadError: "Could not load the data. Refresh the page.",
      intro: function (pair, params) {
        return (
          "The parameters that came out best on " + pair + ": " + params +
          ". They are then applied unchanged to the other pairs."
        );
      },
      guess: function (n) {
        return "On how many of the " + n + " pairs did these parameters stay profitable?";
      },
      colPair: "Pair",
      colTransferred: "Transferred, R",
      colTrades: "Trades",
      colOwn: "Its own best, R",
      colOwnParams: "Its own best parameters",
      home: "home",
      tooFew: "too few trades",
      answer: function (guessed, real, total) {
        return guessed === real
          ? "Exactly: " + real + " out of " + total + "."
          : "You said " + guessed + "; it is " + real + " out of " + total + ".";
      },
      spread: function (best, bestR, worst, worstR) {
        return "Best pair — " + best + " (" + bestR + "), worst — " + worst + " (" + worstR + ").";
      },
      ownDiffer: function (n, total) {
        return n + " of " + total + " pairs prefer different parameters than the home pair.";
      },
      lesson:
        "If every pair has its own «best» parameters, then «best» is a property " +
        "of the sample, not of the strategy. Same overfitting, another axis.",
      again: "Answer again",
    },
    uz: {
      loading: "Juftliklar bo'yicha natijalar yuklanmoqda…",
      loadError: "Ma'lumotni yuklab bo'lmadi. Sahifani yangilang.",
      intro: function (pair, params) {
        return (
          pair + " da eng yaxshi chiqqan parametrlar: " + params +
          ". Keyin ular o'zgarishsiz boshqa juftliklarga qo'llanadi."
        );
      },
      guess: function (n) {
        return n + " ta juftlikdan nechtasida bu parametrlar foydada qoldi?";
      },
      colPair: "Juftlik",
      colTransferred: "Ko'chirish, R",
      colTrades: "Savdolar",
      colOwn: "O'zining eng yaxshisi, R",
      colOwnParams: "O'z eng yaxshi parametrlari",
      home: "tayanch",
      tooFew: "savdolar kam",
      answer: function (guessed, real, total) {
        return guessed === real
          ? "Aniq: " + total + " tadan " + real + " ta."
          : "Siz " + guessed + " dedingiz, aslida " + total + " tadan " + real + " ta.";
      },
      spread: function (best, bestR, worst, worstR) {
        return "Eng yaxshi juftlik — " + best + " (" + bestR + "), eng yomoni — " + worst + " (" + worstR + ").";
      },
      ownDiffer: function (n, total) {
        return total + " juftlikdan " + n + " tasi tayanch juftlikdan boshqa parametrlarni afzal ko'radi.";
      },
      lesson:
        "Agar har bir juftlikning o'z «eng yaxshi» parametrlari bo'lsa, «eng yaxshi» — " +
        "strategiyaning emas, tanlanmaning xossasi. Bu o'sha qayta o'qitish, boshqa o'qda.",
      again: "Qayta javob berish",
    },
  });

  // ── Расчёт: зеркало forex_toolkit/multipair.py ───────────────────────────

  var MIN_TRADES = 20;

  function toResults(document_, minTrades) {
    var limit = minTrades == null ? MIN_TRADES : minTrades;
    return ((document_ || {}).pairs || []).map(function (entry) {
      var transferred = entry.transferred || {};
      var own = entry.own_best || {};
      var ownResult = own.result || {};
      // null, а не ноль: «сделок не хватило» и «результат нулевой» — разное.
      var ownTotal = ownResult.total_r == null ? null : Number(ownResult.total_r);
      var trades = Number(transferred.trades) || 0;
      var moved = Number(transferred.total_r) || 0;
      return {
        pair: String(entry.pair || "?"),
        transferred_r: moved,
        transferred_trades: trades,
        own_best_r: ownTotal,
        own_params: own.params || {},
        enough: trades >= limit,
        gap: ownTotal === null ? null : ownTotal - moved,
      };
    });
  }

  function median(values) {
    if (!values.length) return 0;
    var ordered = values.slice().sort(function (a, b) { return a - b; });
    var middle = Math.floor(ordered.length / 2);
    return ordered.length % 2
      ? ordered[middle]
      : (ordered[middle - 1] + ordered[middle]) / 2;
  }

  function sameParams(a, b) {
    var keys = Object.keys(a || {});
    if (keys.length !== Object.keys(b || {}).length) return false;
    return keys.every(function (k) { return a[k] === b[k]; });
  }

  function summarize(document_, minTrades) {
    var results = toResults(document_, minTrades);
    // Пара без сделок не может быть «худшей» — она просто не участвовала.
    var measurable = results.filter(function (r) { return r.enough; });
    if (!measurable.length) return null;

    var meta = (document_ || {}).meta || {};
    var homeParams = meta.home_params || {};
    var values = measurable.map(function (r) { return r.transferred_r; });

    var best = measurable[0], worst = measurable[0];
    measurable.forEach(function (r) {
      if (r.transferred_r > best.transferred_r) best = r;
      if (r.transferred_r < worst.transferred_r) worst = r;
    });

    return {
      home_pair: String(meta.home_pair || ""),
      home_params: homeParams,
      results: results,
      best: best,
      worst: worst,
      median_r: median(values),
      profitable: values.filter(function (v) { return v > 0; }).length,
      pairs: results.length,
      measurable: measurable.length,
      thin: results.length - measurable.length,
      own_params_differ: results.filter(function (r) {
        return Object.keys(r.own_params || {}).length &&
          !sameParams(r.own_params, homeParams);
      }).length,
      spread: best.transferred_r - worst.transferred_r,
    };
  }

  window.__fxMultiPair = summarize;

  // ── Страница ────────────────────────────────────────────────────────────

  var data = null, summary = null, answered = null;

  root.innerHTML = '<p id="mp-loading">' + F.escape(T.loading) + "</p>";

  fetch(root.getAttribute("data-src"))
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (document_) {
      data = document_;
      summary = summarize(data);
      if (!summary) throw new Error("empty");
      render();
    })
    .catch(function () {
      root.innerHTML =
        '<p class="calc-result calc-error">' + F.escape(T.loadError) + "</p>";
    });

  function r(value) {
    return (value >= 0 ? "+" : "") + value.toFixed(1) + "R";
  }

  function describe(params) {
    return Object.keys(params || {})
      .map(function (k) { return k + " " + params[k]; })
      .join(", ");
  }

  function render() {
    // Спрашиваем про измеримые пары: пара, где сделок не набралось, не может
    // ни «остаться в плюсе», ни «выпасть» — она не участвовала.
    var buttons = "";
    for (var i = 0; i <= summary.measurable; i++) {
      buttons +=
        '<button type="button" class="mp-guess" data-n="' + i + '">' + i + "</button>";
    }

    root.innerHTML =
      "<p>" + F.escape(T.intro(summary.home_pair, describe(summary.home_params))) + "</p>" +
      (answered === null
        ? "<p><strong>" + F.escape(T.guess(summary.measurable)) + "</strong></p>" +
          '<div class="mp-guesses">' + buttons + "</div>"
        : table()) +
      '<div id="mp-verdict" role="status" aria-live="polite"></div>';

    root.querySelectorAll(".mp-guess").forEach(function (button) {
      button.addEventListener("click", function () {
        answered = parseInt(button.getAttribute("data-n"), 10);
        render();
        verdict();
      });
    });
  }

  function table() {
    var rows = summary.results
      .map(function (item) {
        var isHome = item.pair === summary.home_pair;
        // Пара без достаточного числа сделок показывается словами, а не
        // числом: «+0.0R» читалось бы как результат, которого нет.
        var moved = item.enough
          ? '<td class="mp-num ' + (item.transferred_r < 0 ? "mp-bad" : "mp-good") +
            '">' + r(item.transferred_r) + "</td>"
          : '<td class="mp-thin">' + F.escape(T.tooFew) + "</td>";
        var own = item.own_best_r === null
          ? '<td class="mp-thin">' + F.escape(T.tooFew) + "</td>"
          : '<td class="mp-num">' + r(item.own_best_r) + "</td>";
        return (
          '<tr' + (isHome ? ' class="mp-home"' : "") + "><td>" +
          F.escape(item.pair) + (isHome ? " <small>(" + F.escape(T.home) + ")</small>" : "") +
          "</td>" + moved +
          '<td class="mp-num">' + item.transferred_trades + "</td>" + own +
          "<td>" + F.escape(describe(item.own_params)) + "</td></tr>"
        );
      })
      .join("");

    return (
      '<div class="mp-scroll"><table class="mp-table"><thead><tr><th>' +
      F.escape(T.colPair) + "</th><th>" + F.escape(T.colTransferred) + "</th><th>" +
      F.escape(T.colTrades) + "</th><th>" + F.escape(T.colOwn) + "</th><th>" +
      F.escape(T.colOwnParams) + "</th></tr></thead><tbody>" + rows +
      "</tbody></table></div>"
    );
  }

  function verdict() {
    var lines = [
      "<p><strong>" +
        F.escape(T.answer(answered, summary.profitable, summary.measurable)) +
        "</strong></p>",
      "<p>" +
        F.escape(
          T.spread(
            summary.best.pair, r(summary.best.transferred_r),
            summary.worst.pair, r(summary.worst.transferred_r)
          )
        ) + "</p>",
      "<p>" + F.escape(T.ownDiffer(summary.own_params_differ, summary.pairs)) + "</p>",
      '<p class="mp-lesson">' + F.escape(T.lesson) + "</p>",
      '<button type="button" class="calc-button" id="mp-again">' +
        F.escape(T.again) + "</button>",
    ];
    var box = document.getElementById("mp-verdict");
    box.innerHTML = lines.join("");
    document.getElementById("mp-again").addEventListener("click", function () {
      answered = null;
      render();
    });
    if (window.fxTrack) window.fxTrack("multipair_answered", { once: false });
  }
})();
