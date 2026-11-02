/*
 * «Неделя на рынке»: три крупнейших движения последней полной недели.
 *
 * Рендерит data/weekly-review.json (tools/build_weekly_review.py): карточка
 * на движение — мини-график часовых свечей недели, ход в пипсах и в ATR,
 * день пика. Ход в ATR, а не в пипсах: 260 пипсов по GBP и по AUD —
 * разные события, а сравнивать недели хочется честно.
 */
(function () {
  var root = document.getElementById("weekly-review");
  if (!root || !window.FXW) return;

  var F = window.FXW;

  var T = F.pick({
    ru: {
      loading: "Считаю движения недели…",
      loadError: "Не удалось загрузить обзор. Обнови страницу.",
      week: function (from, to) { return "Неделя " + from + " → " + to; },
      move: "Ход недели",
      inAtr: "в ATR",
      peakDay: "День пика",
      range: "Диапазон",
      pips: "пипсов",
      others: "Остальные пары той же недели",
      colPair: "Пара",
      colMove: "Ход, пипсы",
      colAtr: "Ход, ATR",
      fresh: function (stamp) { return "Пересчёт: " + stamp + " (tools/build_weekly_review.py)"; },
    },
    en: {
      loading: "Computing the week's moves…",
      loadError: "Could not load the review. Refresh the page.",
      week: function (from, to) { return "Week " + from + " → " + to; },
      move: "Weekly move",
      inAtr: "in ATR",
      peakDay: "Peak day",
      range: "Range",
      pips: "pips",
      others: "The other pairs of the same week",
      colPair: "Pair",
      colMove: "Move, pips",
      colAtr: "Move, ATR",
      fresh: function (stamp) { return "Recomputed: " + stamp + " (tools/build_weekly_review.py)"; },
    },
    uz: {
      loading: "Hafta harakatlari hisoblanmoqda…",
      loadError: "Sharhni yuklab bo'lmadi. Sahifani yangilang.",
      week: function (from, to) { return from + " → " + to + " hafta"; },
      move: "Hafta xodi",
      inAtr: "ATR da",
      peakDay: "Pik kuni",
      range: "Diapazon",
      pips: "pips",
      others: "O'sha haftaning qolgan juftliklari",
      colPair: "Juftlik",
      colMove: "Xod, pips",
      colAtr: "Xod, ATR",
      fresh: function (stamp) { return "Qayta hisob: " + stamp + " (tools/build_weekly_review.py)"; },
    },
  });

  var style = document.createElement("style");
  style.textContent = [
    ".wr-week{font-size:.85rem;color:var(--md-default-fg-color--light);margin:.2rem 0 .8rem}",
    ".wr-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.9rem;margin:.8rem 0}",
    ".wr-card{border:1px solid var(--md-default-fg-color--lighter);border-radius:10px;padding:.8rem .9rem;background:var(--md-code-bg-color)}",
    ".wr-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.4rem}",
    ".wr-pair{font-weight:700;font-size:1.02rem}",
    ".wr-change{font-weight:750;font-variant-numeric:tabular-nums}",
    ".wr-up{color:#15803d}.wr-down{color:#b91c1c}",
    '[data-md-color-scheme="slate"] .wr-up{color:#4ade80}',
    '[data-md-color-scheme="slate"] .wr-down{color:#f87171}',
    ".wr-chart{width:100%;height:130px;border-radius:7px;background:#0d1117;display:block}",
    ".wr-stats{display:grid;grid-template-columns:1fr 1fr;gap:.3rem .7rem;font-size:.78rem;margin-top:.5rem}",
    ".wr-stats b{font-variant-numeric:tabular-nums}",
    ".wr-stats span{color:var(--md-default-fg-color--light)}",
    ".wr-others{margin-top:1.1rem}",
    ".wr-others table{width:100%;border-collapse:collapse;font-size:.83rem}",
    ".wr-others th,.wr-others td{padding:.3rem .6rem;border-bottom:1px solid var(--md-default-fg-color--lightest);text-align:right}",
    ".wr-others th:first-child,.wr-others td:first-child{text-align:left}",
    ".wr-fresh{font-size:.76rem;color:var(--md-default-fg-color--light);margin-top:.7rem}",
  ].join("");
  document.head.appendChild(style);

  root.innerHTML = "<p>" + F.escape(T.loading) + "</p>";

  fetch(root.getAttribute("data-src"))
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(render)
    .catch(function () {
      root.innerHTML =
        '<p class="calc-result calc-error">' + F.escape(T.loadError) + "</p>";
    });

  function fmtPips(value) {
    return (value > 0 ? "+" : "") + Number(value).toFixed(1);
  }

  function drawChart(canvas, candles) {
    var dpr = window.devicePixelRatio || 1;
    var width = canvas.offsetWidth || 260;
    var height = 130;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    var ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
    ctx.fillStyle = "#0d1117";
    ctx.fillRect(0, 0, width, height);

    var min = Infinity, max = -Infinity;
    candles.forEach(function (c) {
      min = Math.min(min, c[2]);
      max = Math.max(max, c[1]);
    });
    var pad = (max - min || 10) * 0.08;
    min -= pad;
    max += pad;

    function y(v) { return 6 + (height - 12) * (1 - (v - min) / (max - min)); }

    // Нулевая линия — открытие недели.
    ctx.strokeStyle = "#6b7280";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, y(0));
    ctx.lineTo(width, y(0));
    ctx.stroke();
    ctx.setLineDash([]);

    var step = width / candles.length;
    var bar = Math.max(1, step - 1);
    candles.forEach(function (c, i) {
      var up = c[3] >= c[0];
      ctx.strokeStyle = up ? "#2dd4bf" : "#f87171";
      ctx.fillStyle = ctx.strokeStyle;
      var x = i * step + step / 2;
      ctx.beginPath();
      ctx.moveTo(x, y(c[1]));
      ctx.lineTo(x, y(c[2]));
      ctx.stroke();
      var top = y(Math.max(c[0], c[3]));
      var h = Math.max(1, Math.abs(y(c[0]) - y(c[3])));
      ctx.fillRect(x - bar / 2, top, bar, h);
    });
  }

  function render(document_) {
    var meta = document_.meta || {};
    var week = meta.week || {};
    var moves = document_.moves || [];

    root.innerHTML =
      '<p class="wr-week"><strong>' + F.escape(T.week(week.from || "?", week.to || "?")) +
      "</strong></p>" +
      '<div class="wr-grid">' +
      moves.map(function (move, i) {
        var cls = move.change_pips >= 0 ? "wr-up" : "wr-down";
        return (
          '<div class="wr-card"><div class="wr-head"><span class="wr-pair">' +
          F.escape(move.pair) + '</span><span class="wr-change ' + cls + '">' +
          fmtPips(move.change_pips) + " " + F.escape(T.pips) + " · " +
          fmtPips(move.move_in_atr) + " " + F.escape(T.inAtr) + "</span></div>" +
          '<canvas class="wr-chart" id="wr-chart-' + i + '"></canvas>' +
          '<div class="wr-stats">' +
          "<span>" + F.escape(T.peakDay) + "</span><b>" + F.escape(move.biggest_day) + "</b>" +
          "<span>" + F.escape(T.range) + "</span><b>" +
          F.int(Math.round((move.high - move.low) / (move.pair.endsWith("JPY") ? 0.01 : 0.0001))) +
          " " + F.escape(T.pips) + "</b>" +
          "</div></div>"
        );
      }).join("") +
      "</div>" +
      '<div class="wr-others"><table><thead><tr><th>' + F.escape(T.colPair) +
      "</th><th>" + F.escape(T.colMove) + "</th><th>" + F.escape(T.colAtr) +
      "</th></tr></thead><tbody>" +
      (document_.others || []).map(function (m) {
        var cls = m.change_pips >= 0 ? "wr-up" : "wr-down";
        return '<tr><td>' + F.escape(m.pair) + '</td><td class="' + cls + '">' +
          fmtPips(m.change_pips) + '</td><td class="' + cls + '">' +
          fmtPips(m.move_in_atr) + "</td></tr>";
      }).join("") +
      "</tbody></table></div>" +
      '<p class="wr-fresh">' + F.escape(T.fresh(meta.generated_at || "?")) + "</p>";

    moves.forEach(function (move, i) {
      drawChart(document.getElementById("wr-chart-" + i), move.candles || []);
    });
    if (window.fxTrack) window.fxTrack("weekly_review_viewed", { once: true });
  }
})();
