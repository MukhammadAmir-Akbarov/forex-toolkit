/*
 * Рыночная аналитика: когда рынок двигается и какие пары ходят вместе.
 *
 * Две тепловые карты из data/market-analytics.json (tools/build_market_analytics.py):
 *   1. Волатильность по часам UTC — средний True Range в пипсах. Отвечает на
 *      вопрос «когда садиться за терминал», а не «когда удобно».
 *   2. Корреляции 8×8 по часовым доходностям. Отвечает на вопрос «сколько
 *      на самом деле открыто позиций», когда их формально три.
 *
 * Цвета считаются инлайн от значения, без темы: полупрозрачный акцент читается
 * и на светлом, и на тёмном фоне; насыщенные ячейки получают белый текст.
 */
(function () {
  var root = document.getElementById("market-analytics");
  if (!root || !window.FXW) return;

  var F = window.FXW;

  var T = F.pick({
    ru: {
      loading: "Считаю волатильность и корреляции…",
      loadError: "Не удалось загрузить данные. Обнови страницу.",
      volTitle: "Волатильность по часам (средний ход свечи, пипсы)",
      corrTitle: "Корреляция пар (часовые доходности, −1…+1)",
      hoursUtc: "Часы — UTC. Ташкент = UTC+5: прибавь 5 часов к номеру колонки.",
      calm: "тихо",
      hot: "горячо",
      opposite: "вразнобой",
      together: "вместе",
      noData: "—",
      peak: function (pair, hour, pips) {
        return "Пик выборки: " + pair + " в " + hour + ":00 UTC — в среднем " + pips + " пипсов за свечу.";
      },
      range: function (from, to, stamp) {
        return "Часовые свечи восьми пар, " + from + " → " + to + ". Пересчёт: " + stamp + ".";
      },
    },
    en: {
      loading: "Computing volatility and correlations…",
      loadError: "Could not load the data. Refresh the page.",
      volTitle: "Volatility by hour (average candle range, pips)",
      corrTitle: "Pair correlations (hourly returns, −1…+1)",
      hoursUtc: "Hours are UTC. Tashkent is UTC+5: add 5 hours to the column number.",
      calm: "quiet",
      hot: "hot",
      opposite: "opposite",
      together: "together",
      noData: "—",
      peak: function (pair, hour, pips) {
        return "Sample peak: " + pair + " at " + hour + ":00 UTC — " + pips + " pips per candle on average.";
      },
      range: function (from, to, stamp) {
        return "Hourly candles of eight pairs, " + from + " → " + to + ". Recomputed: " + stamp + ".";
      },
    },
    uz: {
      loading: "Volatillik va korrelyatsiyalar hisoblanmoqda…",
      loadError: "Ma'lumotni yuklab bo'lmadi. Sahifani yangilang.",
      volTitle: "Soatlar bo'yicha volatillik (shamning o'rtacha xodi, pips)",
      corrTitle: "Juftliklar korrelyatsiyasi (soatlik daromadlar, −1…+1)",
      hoursUtc: "Soatlar — UTC. Toshkent = UTC+5: ustun raqamiga 5 soat qo'shing.",
      calm: "tinch",
      hot: "faol",
      opposite: "qarama-qarshi",
      together: "birga",
      noData: "—",
      peak: function (pair, hour, pips) {
        return "Tanlanma cho'qqisi: " + pair + " soat " + hour + ":00 UTC — o'rtacha " + pips + " pips.";
      },
      range: function (from, to, stamp) {
        return "Sakkiz juftlikning soatlik shamlari, " + from + " → " + to + ". Qayta hisob: " + stamp + ".";
      },
    },
  });

  root.innerHTML = '<p class="ma-loading">' + F.escape(T.loading) + "</p>";

  fetch(root.getAttribute("data-src"))
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (document_) { render(document_); })
    .catch(function () {
      root.innerHTML =
        '<p class="calc-result calc-error">' + F.escape(T.loadError) + "</p>";
    });

  /* Полупрозрачный акцент с интенсивностью 0…1; насыщенная ячейка — с белым
     текстом. Читается на обеих темах без переключения палитры. */
  function heatStyle(intensity, hue) {
    var a = (0.06 + 0.7 * intensity).toFixed(2);
    var color = intensity > 0.6 ? "color:#fff;" : "";
    return 'style="background:hsl(' + hue + " 80% 55% / " + a + ');' + color + '"';
  }

  function volatilityTable(vol) {
    var pairs = vol.pairs, values = vol.values, hours = vol.hours_utc;
    var max = 0;
    pairs.forEach(function (p) {
      values[p].forEach(function (v) { if (v > max) max = v; });
    });
    var head = "<tr><th></th>" + hours.map(function (h) {
      return "<th>" + h + "</th>";
    }).join("") + "</tr>";
    var rows = pairs.map(function (p) {
      var cells = values[p].map(function (v) {
        return "<td " + heatStyle(max ? v / max : 0, 222) + ">" +
          v.toFixed(v >= 100 ? 0 : 1) + "</td>";
      }).join("");
      return "<tr><th>" + F.escape(p) + "</th>" + cells + "</tr>";
    }).join("");
    return (
      '<div class="ma-scroll"><table class="ma-table ma-vol"><thead>' + head +
      "</thead><tbody>" + rows + "</tbody></table></div>"
    );
  }

  function correlationTable(corr) {
    var pairs = corr.pairs, values = corr.values;
    var head = "<tr><th></th>" + pairs.map(function (p) {
      return "<th>" + F.escape(p) + "</th>";
    }).join("") + "</tr>";
    var rows = pairs.map(function (rowPair, i) {
      var cells = pairs.map(function (_, j) {
        var v = values[i][j];
        if (v == null) return '<td class="ma-none">' + T.noData + "</td>";
        var diag = i === j ? ' class="ma-diag"' : "";
        // +1 красное («дублируешь риск»), −1 синее, 0 — пусто.
        var hue = v >= 0 ? 4 : 222;
        return "<td" + diag + " " + heatStyle(Math.abs(v), hue) + ">" +
          v.toFixed(2) + "</td>";
      }).join("");
      return "<tr><th>" + F.escape(rowPair) + "</th>" + cells + "</tr>";
    }).join("");
    return (
      '<div class="ma-scroll"><table class="ma-table ma-corr"><thead>' + head +
      "</thead><tbody>" + rows + "</tbody></table></div>"
    );
  }

  function render(document_) {
    var vol = document_.volatility || {};
    var corr = document_.correlations || {};
    var meta = document_.meta || {};
    var range = meta.range || {};

    var peakPair = "", peakHour = 0, peakValue = 0;
    (vol.pairs || []).forEach(function (p) {
      (vol.values[p] || []).forEach(function (v, h) {
        if (v > peakValue) { peakValue = v; peakPair = p; peakHour = h; }
      });
    });

    root.innerHTML =
      '<h3 class="ma-title">' + F.escape(T.volTitle) + "</h3>" +
      volatilityTable(vol) +
      '<p class="ma-legend"><span class="ma-chip" ' + heatStyle(0.05, 222) + "></span>" +
      F.escape(T.calm) + ' &rarr; <span class="ma-chip" ' + heatStyle(1, 222) + "></span>" +
      F.escape(T.hot) + " · " + F.escape(T.hoursUtc) + "</p>" +
      "<p><strong>" + F.escape(T.peak(peakPair, peakHour, peakValue.toFixed(1))) + "</strong></p>" +
      '<h3 class="ma-title">' + F.escape(T.corrTitle) + "</h3>" +
      correlationTable(corr) +
      '<p class="ma-legend"><span class="ma-chip" ' + heatStyle(1, 222) + "></span>" +
      F.escape(T.opposite) + ' · <span class="ma-chip" ' + heatStyle(1, 4) + "></span>" +
      F.escape(T.together) + "</p>" +
      '<p class="ma-range">' +
      F.escape(T.range(String(range.from || "?").slice(0, 10), String(range.to || "?").slice(0, 10), meta.generated_at || "?")) +
      "</p>";

    if (window.fxTrack) window.fxTrack("market_analytics_viewed", { once: true });
  }
})();
