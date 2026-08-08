/*
 * Переобучение: выбери лучшие параметры по прошлому и посмотри на будущее.
 *
 * Зачем именно так. Сказать «бэктест врёт» — это лозунг, его пролистывают.
 * Поэтому здесь читатель делает то же самое, что делает продавец «робота»:
 * смотрит на таблицу результатов за прошлое и выбирает лучшую строку. И только
 * после выбора видит вторую половину истории.
 *
 * Числа не выдуманы и не синтетические: перебор посчитан на реальных котировках
 * (tools/overfit_scan.py), зафиксирован в data/overfitting.json вместе с парой,
 * таймфреймом и периодом. Сводка — зеркало forex_toolkit/overfitting.py,
 * сверка в tests/test_widget_logic.py и в браузерных тестах.
 */
(function () {
  var root = document.getElementById("overfitting");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var MIN_TRADES = 20;

  var T = F.pick({
    ru: {
      loading: "Загружаю результаты перебора…",
      loadError: "Не удалось загрузить данные. Обнови страницу.",
      intro: function (n, pair, tf) {
        return (
          "Ниже " + n + " комбинаций параметров одной и той же стратегии, " +
          "посчитанных на реальных котировках " + pair + " " + tf + "."
        );
      },
      task: "Выбери строку, на которую поставил бы деньги. Видно только прошлое.",
      period: function (from, split, to) {
        return "Прошлое: " + from + " — " + split + ". Будущее: " + split + " — " + to + ".";
      },
      colParams: "Параметры",
      colPast: "Прошлое, R",
      colTrades: "Сделок",
      colFuture: "Будущее, R",
      pick: "Выбрать",
      yourPick: "Твой выбор",
      reveal: "Что было дальше",
      yours: function (past, future) {
        return "Ты выбрал комбинацию с " + past + " на прошлом. На будущем она дала " + future + ".";
      },
      bestWas: function (rank, total) {
        return "Лучшая по прошлому заняла на будущем " + rank + "-е место из " + total + ".";
      },
      medianWas: function (median) {
        return "Медиана всех комбинаций на будущем: " + median + ". Это и есть «выбрать наугад».";
      },
      corr: function (value) {
        return "Связь результата на прошлом и на будущем: " + value + ".";
      },
      corrNone: "Около нуля — значит подбор ловил шум, а не закономерность.",
      corrSome: "Связь есть, но её одной мало для решения о деньгах.",
      lesson:
        "Красивый бэктест — это результат выбора лучшего из многих. Чем больше " +
        "перебрал, тем красивее будет лучший и тем меньше он значит.",
      again: "Выбрать заново",
      loss: "убыток",
    },
    en: {
      loading: "Loading the sweep results…",
      loadError: "Could not load the data. Refresh the page.",
      intro: function (n, pair, tf) {
        return (
          "Below are " + n + " parameter combinations of one strategy, " +
          "measured on real " + pair + " " + tf + " candles."
        );
      },
      task: "Pick the row you would put money on. Only the past is shown.",
      period: function (from, split, to) {
        return "Past: " + from + " — " + split + ". Future: " + split + " — " + to + ".";
      },
      colParams: "Parameters",
      colPast: "Past, R",
      colTrades: "Trades",
      colFuture: "Future, R",
      pick: "Pick",
      yourPick: "Your pick",
      reveal: "What happened next",
      yours: function (past, future) {
        return "You picked the combination with " + past + " in the past. In the future it made " + future + ".";
      },
      bestWas: function (rank, total) {
        return "The best of the past ranked " + rank + " out of " + total + " in the future.";
      },
      medianWas: function (median) {
        return "Median of all combinations in the future: " + median + ". That is what picking at random gives.";
      },
      corr: function (value) {
        return "Correlation between past and future results: " + value + ".";
      },
      corrNone: "Near zero — the tuning was fitting noise, not a pattern.",
      corrSome: "There is some link, but not enough to bet money on.",
      lesson:
        "A beautiful backtest is the best of many tries. The more you try, the " +
        "better the winner looks and the less it means.",
      again: "Pick again",
      loss: "a loss",
    },
    uz: {
      loading: "Saralash natijalari yuklanmoqda…",
      loadError: "Ma'lumotni yuklab bo'lmadi. Sahifani yangilang.",
      intro: function (n, pair, tf) {
        return (
          "Quyida bitta strategiyaning " + n + " ta parametr birikmasi — haqiqiy " +
          pair + " " + tf + " shamlarida hisoblangan."
        );
      },
      task: "Pulingizni qo'yadigan qatorni tanlang. Faqat o'tmish ko'rinadi.",
      period: function (from, split, to) {
        return "O'tmish: " + from + " — " + split + ". Kelajak: " + split + " — " + to + ".";
      },
      colParams: "Parametrlar",
      colPast: "O'tmish, R",
      colTrades: "Savdolar",
      colFuture: "Kelajak, R",
      pick: "Tanlash",
      yourPick: "Sizning tanlovingiz",
      reveal: "Keyin nima bo'ldi",
      yours: function (past, future) {
        return "Siz o'tmishda " + past + " bergan birikmani tanladingiz. Kelajakda u " + future + " berdi.";
      },
      bestWas: function (rank, total) {
        return "O'tmishdagi eng yaxshisi kelajakda " + total + " tadan " + rank + "-o'rinni egalladi.";
      },
      medianWas: function (median) {
        return "Barcha birikmalarning kelajakdagi medianasi: " + median + ". Tasodifiy tanlash shuni beradi.";
      },
      corr: function (value) {
        return "O'tmish va kelajak natijalari bog'liqligi: " + value + ".";
      },
      corrNone: "Nolga yaqin — saralash qonuniyatni emas, shovqinni topgan.",
      corrSome: "Bog'liqlik bor, lekin pul qarori uchun yetarli emas.",
      lesson:
        "Chiroyli bektest — bu ko'p urinishdan eng yaxshisi. Qancha ko'p " +
        "sinasangiz, g'olib shuncha chiroyli va shuncha kam ma'noli bo'ladi.",
      again: "Qayta tanlash",
      loss: "zarar",
    },
  });

  // ── Расчёт: зеркало forex_toolkit/overfitting.py ─────────────────────────

  function toCombos(rows, minTrades) {
    var limit = minTrades == null ? MIN_TRADES : minTrades;
    var combos = [];
    (rows || []).forEach(function (row) {
      var inside = row.in || {}, outside = row.out || {};
      var inTrades = Number(inside.trades) || 0;
      var outTrades = Number(outside.trades) || 0;
      if (inTrades < limit || outTrades < limit) return;
      combos.push({
        params: row.params || {},
        in_total_r: Number(inside.total_r) || 0,
        in_trades: inTrades,
        out_total_r: Number(outside.total_r) || 0,
        out_trades: outTrades,
      });
    });
    return combos;
  }

  function median(values) {
    if (!values.length) return 0;
    var ordered = values.slice().sort(function (a, b) { return a - b; });
    var middle = Math.floor(ordered.length / 2);
    return ordered.length % 2
      ? ordered[middle]
      : (ordered[middle - 1] + ordered[middle]) / 2;
  }

  function correlation(xs, ys) {
    var n = xs.length;
    if (n < 2 || n !== ys.length) return 0;
    var meanX = xs.reduce(function (a, b) { return a + b; }, 0) / n;
    var meanY = ys.reduce(function (a, b) { return a + b; }, 0) / n;
    var cov = 0, varX = 0, varY = 0;
    for (var i = 0; i < n; i++) {
      cov += (xs[i] - meanX) * (ys[i] - meanY);
      varX += (xs[i] - meanX) * (xs[i] - meanX);
      varY += (ys[i] - meanY) * (ys[i] - meanY);
    }
    if (varX <= 0 || varY <= 0) return 0;
    return cov / Math.sqrt(varX * varY);
  }

  function summarize(rows, minTrades) {
    var combos = toCombos(rows, minTrades);
    if (!combos.length) return null;

    var bestIn = combos[0], bestOut = combos[0];
    combos.forEach(function (c) {
      if (c.in_total_r > bestIn.in_total_r) bestIn = c;
      if (c.out_total_r > bestOut.out_total_r) bestOut = c;
    });

    var outs = combos.map(function (c) { return c.out_total_r; });
    var ranked = combos.slice().sort(function (a, b) {
      return b.out_total_r - a.out_total_r;
    });
    var rank = 0;
    for (var i = 0; i < ranked.length; i++) {
      if (same(ranked[i].params, bestIn.params)) { rank = i + 1; break; }
    }

    return {
      best_in: bestIn,
      best_out: bestOut,
      rank_out: rank,
      considered: combos.length,
      median_out: median(outs),
      mean_out: outs.reduce(function (a, b) { return a + b; }, 0) / outs.length,
      correlation: correlation(combos.map(function (c) { return c.in_total_r; }), outs),
      degradation: bestIn.in_total_r - bestIn.out_total_r,
      beat_median: bestIn.out_total_r > median(outs),
    };
  }

  function same(a, b) {
    var keys = Object.keys(a);
    if (keys.length !== Object.keys(b).length) return false;
    return keys.every(function (k) { return a[k] === b[k]; });
  }

  window.__fxOverfitSummary = summarize;
  window.__fxOverfitCorrelation = correlation;

  // ── Страница ────────────────────────────────────────────────────────────

  var data = null, summary = null, revealed = false;

  root.innerHTML = '<p id="of-loading">' + F.escape(T.loading) + "</p>";

  fetch(root.getAttribute("data-src"))
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (document_) {
      data = document_;
      summary = summarize(data.rows, data.meta && data.meta.min_trades);
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

  function day(stamp) {
    return String(stamp || "").slice(0, 10);
  }

  function combos() {
    return toCombos(data.rows, data.meta && data.meta.min_trades);
  }

  function describe(params) {
    return Object.keys(params)
      .map(function (k) { return k + " " + params[k]; })
      .join(", ");
  }

  function render() {
    var meta = data.meta || {};
    var list = combos();
    var rows = list
      .map(function (c, i) {
        return (
          '<tr><td>' + F.escape(describe(c.params)) + "</td>" +
          '<td class="of-num">' + r(c.in_total_r) + "</td>" +
          '<td class="of-num">' + c.in_trades + "</td>" +
          (revealed
            ? '<td class="of-num' + (c.out_total_r < 0 ? " of-bad" : " of-good") +
              '">' + r(c.out_total_r) + "</td>"
            : '<td><button type="button" class="of-pick" data-i="' + i + '">' +
              F.escape(T.pick) + "</button></td>") +
          "</tr>"
        );
      })
      .join("");

    root.innerHTML =
      "<p>" + F.escape(T.intro(list.length, meta.pair || "", meta.timeframe || "")) + "</p>" +
      '<p class="of-period">' +
      F.escape(T.period(day(meta.from), day(meta.split_at), day(meta.to))) + "</p>" +
      (revealed ? "" : "<p><strong>" + F.escape(T.task) + "</strong></p>") +
      '<div class="of-scroll"><table class="of-table"><thead><tr><th>' +
      F.escape(T.colParams) + "</th><th>" + F.escape(T.colPast) + "</th><th>" +
      F.escape(T.colTrades) + "</th><th>" +
      F.escape(revealed ? T.colFuture : T.yourPick) +
      "</th></tr></thead><tbody>" + rows + "</tbody></table></div>" +
      '<div id="of-verdict" role="status" aria-live="polite"></div>';

    root.querySelectorAll(".of-pick").forEach(function (button) {
      button.addEventListener("click", function () {
        reveal(list[parseInt(button.getAttribute("data-i"), 10)]);
      });
    });
  }

  function reveal(chosen) {
    revealed = true;
    render();

    var corr = summary.correlation;
    var lines = [
      "<h4>" + F.escape(T.reveal) + "</h4>",
      "<p>" + F.escape(T.yours(r(chosen.in_total_r), r(chosen.out_total_r))) + "</p>",
      "<p>" + F.escape(T.bestWas(summary.rank_out, summary.considered)) + "</p>",
      "<p>" + F.escape(T.medianWas(r(summary.median_out))) + "</p>",
      "<p>" + F.escape(T.corr(corr.toFixed(2))) + " " +
        F.escape(Math.abs(corr) < 0.3 ? T.corrNone : T.corrSome) + "</p>",
      '<p class="of-lesson">' + F.escape(T.lesson) + "</p>",
      '<button type="button" class="calc-button" id="of-again">' +
        F.escape(T.again) + "</button>",
    ];

    var verdict = document.getElementById("of-verdict");
    verdict.innerHTML = lines.join("");
    verdict.scrollIntoView({ block: "nearest" });
    document.getElementById("of-again").addEventListener("click", function () {
      revealed = false;
      render();
    });
    if (window.fxTrack) window.fxTrack("overfitting_revealed", { once: false });
  }
})();
