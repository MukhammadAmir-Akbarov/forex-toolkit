/*
 * Держится ли рейтинг стратегий при переходе из прошлого в будущее.
 *
 * Третий вопрос той же семьи: переобучение во времени, перенос между парами и
 * вот это — устойчивость самого рейтинга. Читатель видит результаты шести
 * стратегий на первой половине истории и выбирает, кто будет первым на второй.
 *
 * Числа посчитаны на реальных котировках (tools/strategy_scan.py) и
 * зафиксированы в data/strategies.json. Сводка — зеркало
 * forex_toolkit/strategy_ranking.py, сверка в тестах.
 */
(function () {
  var root = document.getElementById("strategy-ranking");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var MIN_TRADES = 20;

  var T = F.pick({
    ru: {
      loading: "Загружаю результаты стратегий…",
      loadError: "Не удалось загрузить данные. Обнови страницу.",
      intro: function (n, pair, tf) {
        return n + " стратегий на реальных котировках " + pair + " " + tf +
          ". Показана только первая половина истории.";
      },
      task: "Какая из них будет первой на второй половине?",
      colName: "Стратегия",
      colPast: "Прошлое, R",
      colTrades: "Сделок",
      colFuture: "Будущее, R",
      colPlace: "Место: прошлое → будущее",
      pick: "Выбрать",
      right: "Угадал.",
      wrong: function (name) { return "Первой оказалась не она, а " + name + "."; },
      bestPast: function (name, past, future, rank, total) {
        return "Лучшая на прошлом — " + name + " (" + past + "). На будущем " +
          future + " и " + rank + "-е место из " + total + ".";
      },
      kept: function (n, total) {
        return "Своё место сохранили " + n + " из " + total + ".";
      },
      corr: function (value) { return "Совпадение порядка: " + value + "."; },
      corrNone: "Около нуля — рейтинг по истории не переносится в будущее.",
      corrNeg: "Меньше нуля — порядок ещё и частично перевернулся.",
      corrSome: "Порядок частично сохранился.",
      lesson:
        "Выбрать лучшую из шести стратегий — это тот же отбор, что выбрать " +
        "лучшую из 54 наборов параметров. Красивый результат достаётся тому, " +
        "кто перебрал больше вариантов, а не тому, кто нашёл закономерность.",
      again: "Выбрать заново",
      caution:
        "Шесть стратегий — маленькая выборка. Это не доказывает, что порядок " +
        "переворачивается всегда; это показывает, что опираться на него нельзя.",
    },
    en: {
      loading: "Loading the strategy results…",
      loadError: "Could not load the data. Refresh the page.",
      intro: function (n, pair, tf) {
        return n + " strategies on real " + pair + " " + tf +
          " candles. Only the first half of the history is shown.";
      },
      task: "Which one will come first on the second half?",
      colName: "Strategy",
      colPast: "Past, R",
      colTrades: "Trades",
      colFuture: "Future, R",
      colPlace: "Place: past → future",
      pick: "Pick",
      right: "Correct.",
      wrong: function (name) { return "It was not that one, it was " + name + "."; },
      bestPast: function (name, past, future, rank, total) {
        return "The best of the past — " + name + " (" + past + "). In the future " +
          future + " and place " + rank + " out of " + total + ".";
      },
      kept: function (n, total) {
        return n + " out of " + total + " kept their place.";
      },
      corr: function (value) { return "Order agreement: " + value + "."; },
      corrNone: "Near zero — a ranking on history does not carry into the future.",
      corrNeg: "Below zero — the order partly inverted as well.",
      corrSome: "The order partly held.",
      lesson:
        "Picking the best of six strategies is the same selection as picking " +
        "the best of 54 parameter sets. A beautiful result goes to whoever " +
        "tried more variants, not to whoever found a pattern.",
      again: "Pick again",
      caution:
        "Six strategies is a small sample. This does not prove the order always " +
        "inverts; it shows you cannot lean on it.",
    },
    uz: {
      loading: "Strategiya natijalari yuklanmoqda…",
      loadError: "Ma'lumotni yuklab bo'lmadi. Sahifani yangilang.",
      intro: function (n, pair, tf) {
        return "Haqiqiy " + pair + " " + tf + " shamlarida " + n +
          " ta strategiya. Faqat tarixning birinchi yarmi ko'rsatilgan.";
      },
      task: "Ikkinchi yarmida qaysi biri birinchi bo'ladi?",
      colName: "Strategiya",
      colPast: "O'tmish, R",
      colTrades: "Savdolar",
      colFuture: "Kelajak, R",
      colPlace: "O'rin: o'tmish → kelajak",
      pick: "Tanlash",
      right: "To'g'ri topdingiz.",
      wrong: function (name) { return "U emas, " + name + " birinchi bo'ldi."; },
      bestPast: function (name, past, future, rank, total) {
        return "O'tmishdagi eng yaxshisi — " + name + " (" + past + "). Kelajakda " +
          future + " va " + total + " tadan " + rank + "-o'rin.";
      },
      kept: function (n, total) {
        return total + " tadan " + n + " tasi o'z o'rnini saqladi.";
      },
      corr: function (value) { return "Tartib mosligi: " + value + "."; },
      corrNone: "Nolga yaqin — tarixdagi reyting kelajakka ko'chmaydi.",
      corrNeg: "Noldan kichik — tartib qisman teskari ham bo'lgan.",
      corrSome: "Tartib qisman saqlangan.",
      lesson:
        "Oltita strategiyadan eng yaxshisini tanlash — bu 54 ta parametr " +
        "to'plamidan eng yaxshisini tanlash bilan bir xil saralash. Chiroyli " +
        "natija qonuniyat topganga emas, ko'proq variant sinaganga tegadi.",
      again: "Qayta tanlash",
      caution:
        "Oltita strategiya — kichik tanlanma. Bu tartib doim teskari bo'ladi " +
        "degani emas; bunga tayanib bo'lmasligini ko'rsatadi.",
    },
  });

  // ── Расчёт: зеркало forex_toolkit/strategy_ranking.py ────────────────────

  function ranks(values) {
    var order = values
      .map(function (v, i) { return i; })
      .sort(function (a, b) { return values[b] - values[a]; });
    var out = new Array(values.length);
    var i = 0;
    while (i < order.length) {
      var j = i;
      while (j + 1 < order.length && values[order[j + 1]] === values[order[i]]) j++;
      var shared = (i + j) / 2 + 1;
      for (var k = i; k <= j; k++) out[order[k]] = shared;
      i = j + 1;
    }
    return out;
  }

  function rankCorrelation(xs, ys) {
    var n = xs.length;
    if (n < 2 || n !== ys.length) return 0;
    var rx = ranks(xs), ry = ranks(ys);
    var mx = rx.reduce(function (a, b) { return a + b; }, 0) / n;
    var my = ry.reduce(function (a, b) { return a + b; }, 0) / n;
    var cov = 0, vx = 0, vy = 0;
    for (var i = 0; i < n; i++) {
      cov += (rx[i] - mx) * (ry[i] - my);
      vx += (rx[i] - mx) * (rx[i] - mx);
      vy += (ry[i] - my) * (ry[i] - my);
    }
    if (vx <= 0 || vy <= 0) return 0;
    return cov / Math.sqrt(vx * vy);
  }

  function summarize(document_, minTrades) {
    var limit = minTrades == null ? MIN_TRADES : minTrades;
    var results = [], skipped = 0;
    ((document_ || {}).strategies || []).forEach(function (entry) {
      var past = entry.past || {}, future = entry.future || {};
      var pastTrades = Number(past.trades) || 0;
      var futureTrades = Number(future.trades) || 0;
      if (pastTrades < limit || futureTrades < limit) { skipped++; return; }
      results.push({
        name: String(entry.name || "?"),
        past_r: Number(past.total_r) || 0,
        past_trades: pastTrades,
        future_r: Number(future.total_r) || 0,
        future_trades: futureTrades,
      });
    });
    if (results.length < 2) return null;

    var pastValues = results.map(function (r) { return r.past_r; });
    var futureValues = results.map(function (r) { return r.future_r; });
    var pastRanks = ranks(pastValues), futureRanks = ranks(futureValues);

    var bestPast = results[0], bestFuture = results[0];
    results.forEach(function (r) {
      if (r.past_r > bestPast.past_r) bestPast = r;
      if (r.future_r > bestFuture.future_r) bestFuture = r;
    });
    var bestIndex = results.indexOf(bestPast);

    var kept = 0;
    for (var i = 0; i < results.length; i++) {
      if (pastRanks[i] === futureRanks[i]) kept++;
    }
    var corr = rankCorrelation(pastValues, futureValues);

    return {
      results: results,
      past_ranks: pastRanks,
      future_ranks: futureRanks,
      best_past: bestPast,
      best_future: bestFuture,
      best_past_rank_future: futureRanks[bestIndex],
      considered: results.length,
      kept_place: kept,
      rank_correlation: corr,
      skipped: skipped,
      order_held: corr >= 0.5,
    };
  }

  window.__fxStrategyRanking = summarize;
  window.__fxRankCorrelation = rankCorrelation;

  // ── Страница ────────────────────────────────────────────────────────────

  var data = null, summary = null, picked = null;

  root.innerHTML = '<p id="sr-loading">' + F.escape(T.loading) + "</p>";

  fetch(root.getAttribute("data-src"))
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (document_) {
      data = document_;
      summary = summarize(data, (data.meta || {}).min_trades);
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

  function render() {
    var meta = data.meta || {};
    var order = summary.results
      .map(function (item, i) { return i; })
      .sort(function (a, b) {
        return summary.results[b].past_r - summary.results[a].past_r;
      });

    var rows = order
      .map(function (i) {
        var item = summary.results[i];
        return (
          "<tr><td>" + F.escape(item.name) + "</td>" +
          '<td class="sr-num">' + r(item.past_r) + "</td>" +
          '<td class="sr-num">' + item.past_trades + "</td>" +
          (picked === null
            ? '<td><button type="button" class="sr-pick" data-i="' + i + '">' +
              F.escape(T.pick) + "</button></td>"
            : '<td class="sr-num ' + (item.future_r < 0 ? "sr-bad" : "sr-good") +
              '">' + r(item.future_r) + "</td>" +
              '<td class="sr-num">' + summary.past_ranks[i] + " → " +
              summary.future_ranks[i] + "</td>")
          + "</tr>"
        );
      })
      .join("");

    root.innerHTML =
      "<p>" +
      F.escape(T.intro(summary.considered, meta.pair || "", meta.timeframe || "")) +
      "</p>" +
      (picked === null ? "<p><strong>" + F.escape(T.task) + "</strong></p>" : "") +
      '<div class="sr-scroll"><table class="sr-table"><thead><tr><th>' +
      F.escape(T.colName) + "</th><th>" + F.escape(T.colPast) + "</th><th>" +
      F.escape(T.colTrades) + "</th><th>" +
      (picked === null
        ? F.escape(T.task)
        : F.escape(T.colFuture) + "</th><th>" + F.escape(T.colPlace)) +
      "</th></tr></thead><tbody>" + rows + "</tbody></table></div>" +
      '<div id="sr-verdict" role="status" aria-live="polite"></div>';

    root.querySelectorAll(".sr-pick").forEach(function (button) {
      button.addEventListener("click", function () {
        picked = summary.results[parseInt(button.getAttribute("data-i"), 10)];
        render();
        verdict();
      });
    });
  }

  function verdict() {
    var corr = summary.rank_correlation;
    var hint = corr <= -0.2 ? T.corrNeg : Math.abs(corr) < 0.5 ? T.corrNone : T.corrSome;
    var lines = [
      "<p><strong>" +
        F.escape(
          picked.name === summary.best_future.name
            ? T.right
            : T.wrong(summary.best_future.name)
        ) + "</strong></p>",
      "<p>" +
        F.escape(
          T.bestPast(
            summary.best_past.name,
            r(summary.best_past.past_r),
            r(summary.best_past.future_r),
            summary.best_past_rank_future,
            summary.considered
          )
        ) + "</p>",
      "<p>" + F.escape(T.kept(summary.kept_place, summary.considered)) + "</p>",
      "<p>" + F.escape(T.corr(corr.toFixed(2))) + " " + F.escape(hint) + "</p>",
      '<p class="sr-lesson">' + F.escape(T.lesson) + "</p>",
      '<p class="sr-caution">' + F.escape(T.caution) + "</p>",
      '<button type="button" class="calc-button" id="sr-again">' +
        F.escape(T.again) + "</button>",
    ];
    var box = document.getElementById("sr-verdict");
    box.innerHTML = lines.join("");
    document.getElementById("sr-again").addEventListener("click", function () {
      picked = null;
      render();
    });
    if (window.fxTrack) window.fxTrack("strategy_ranking_revealed", { once: false });
  }
})();
