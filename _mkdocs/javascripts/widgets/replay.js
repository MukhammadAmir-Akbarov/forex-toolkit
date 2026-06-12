/**
 * Replay Trainer widget (I9).
 *
 * Загружает /data/replay-episodes.json, показывает N свечей истории на Canvas,
 * просит выбрать Buy / Sell / Skip + выставить стоп, затем проигрывает будущие
 * свечи и считает результат в R.
 *
 * Не зависит от window.FXW чтобы работать независимо от PR #22.
 */
(function () {
  var CONTAINER = document.getElementById("replay-widget");
  if (!CONTAINER) return;

  /* ── Локализация ── */
  var lang = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (lang !== "en" && lang !== "uz") lang = "ru";

  var T = {
    ru: {
      loading: "Загрузка эпизодов…",
      episode: "Эпизод",
      of: "из",
      pair: "EURUSD H1",
      question: "Что вы делаете?",
      buy: "▲ Buy",
      sell: "▼ Sell",
      skip: "— Пропустить",
      stop_label: "Стоп-лосс (в пипсах от входа):",
      stop_hint: "Обязательно! Введите число пипсов",
      stop_err: "Введите стоп (минимум 1 пипс)",
      reveal: "Показать результат",
      result_win: "✅ Прибыль",
      result_loss: "❌ Убыток",
      result_skip: "⏭ Пропущен",
      next: "Следующий эпизод →",
      finish: "Посмотреть статистику",
      stats_title: "Ваша статистика",
      stats_trades: "Сделок",
      stats_wins: "Побед",
      stats_losses: "Поражений",
      stats_skips: "Пропусков",
      stats_rr: "Средний R",
      stats_wr: "WinRate",
      restart: "Начать заново",
      atr: "ATR",
      pips: "пипс",
      cat_u: "Восходящий тренд",
      cat_d: "Нисходящий тренд",
      cat_s: "Флэт",
      candles_left: "Осталось свечей",
      err_load: "Ошибка загрузки данных. Обновите страницу.",
    },
    en: {
      loading: "Loading episodes…",
      episode: "Episode",
      of: "of",
      pair: "EURUSD H1",
      question: "What do you do?",
      buy: "▲ Buy",
      sell: "▼ Sell",
      skip: "— Skip",
      stop_label: "Stop-loss (pips from entry):",
      stop_hint: "Required! Enter number of pips",
      stop_err: "Enter stop (min 1 pip)",
      reveal: "Show result",
      result_win: "✅ Profit",
      result_loss: "❌ Loss",
      result_skip: "⏭ Skipped",
      next: "Next episode →",
      finish: "View statistics",
      stats_title: "Your statistics",
      stats_trades: "Trades",
      stats_wins: "Wins",
      stats_losses: "Losses",
      stats_skips: "Skips",
      stats_rr: "Avg R",
      stats_wr: "WinRate",
      restart: "Start over",
      atr: "ATR",
      pips: "pips",
      cat_u: "Uptrend",
      cat_d: "Downtrend",
      cat_s: "Sideways",
      candles_left: "Candles left",
      err_load: "Error loading data. Please refresh.",
    },
    uz: {
      loading: "Epizodlar yuklanmoqda…",
      episode: "Epizod",
      of: "dan",
      pair: "EURUSD H1",
      question: "Nima qilasiz?",
      buy: "▲ Sotib ol",
      sell: "▼ Sot",
      skip: "— O'tkazib yubor",
      stop_label: "Stop-loss (entry dan pipslarda):",
      stop_hint: "Majburiy! Pip sonini kiriting",
      stop_err: "Stop kiriting (kamida 1 pip)",
      reveal: "Natijani ko'rsat",
      result_win: "✅ Foyda",
      result_loss: "❌ Zarar",
      result_skip: "⏭ O'tkazildi",
      next: "Keyingi epizod →",
      finish: "Statistikani ko'r",
      stats_title: "Sizning statistikangiz",
      stats_trades: "Savdolar",
      stats_wins: "G'alabalar",
      stats_losses: "Mag'lubiyatlar",
      stats_skips: "O'tkazilganlar",
      stats_rr: "O'rtacha R",
      stats_wr: "WinRate",
      restart: "Qaytadan boshlash",
      atr: "ATR",
      pips: "pip",
      cat_u: "Ko'tariluvchi trend",
      cat_d: "Tushuvchi trend",
      cat_s: "Yon harakat",
      candles_left: "Shamlar qoldi",
      err_load: "Ma'lumotlarni yuklashda xato. Sahifani yangilang.",
    },
  }[lang];

  /* ── Стили ── */
  var style = document.createElement("style");
  style.textContent = [
    "#replay-widget{font-family:inherit;max-width:720px;margin:1.5rem 0}",
    "#replay-canvas{width:100%;border-radius:8px;background:#0d1117;display:block}",
    ".rp-controls{margin-top:1rem;display:flex;gap:.6rem;flex-wrap:wrap;align-items:center}",
    ".rp-btn{padding:.5rem 1.1rem;border:none;border-radius:6px;cursor:pointer;font-size:.95rem;font-weight:600;transition:opacity .15s}",
    ".rp-btn:hover{opacity:.85}",
    ".rp-buy{background:#2dd4bf;color:#0d1117}",
    ".rp-sell{background:#f87171;color:#fff}",
    ".rp-skip{background:#6b7280;color:#fff}",
    ".rp-next{background:#3b82f6;color:#fff}",
    ".rp-btn:disabled{opacity:.4;cursor:not-allowed}",
    ".rp-stop-row{display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;margin-top:.8rem}",
    ".rp-stop-row label{font-size:.85rem;color:var(--md-default-fg-color)}",
    ".rp-stop-input{width:70px;padding:.4rem .5rem;border:1px solid var(--md-default-fg-color--lighter);border-radius:5px;background:var(--md-default-bg-color);color:var(--md-default-fg-color);font-size:.95rem}",
    ".rp-result{margin-top:.8rem;padding:.7rem 1rem;border-radius:7px;font-size:1rem;font-weight:600}",
    ".rp-result-win{background:rgba(45,212,191,.15);border:1px solid #2dd4bf;color:#2dd4bf}",
    ".rp-result-loss{background:rgba(248,113,113,.15);border:1px solid #f87171;color:#f87171}",
    ".rp-result-skip{background:rgba(107,114,128,.15);border:1px solid #6b7280;color:#9ca3af}",
    ".rp-meta{font-size:.8rem;color:var(--md-default-fg-color--light);margin-bottom:.4rem}",
    ".rp-stats{background:var(--md-code-bg-color);border-radius:10px;padding:1.2rem 1.5rem}",
    ".rp-stats h3{margin:0 0 .8rem;font-size:1.1rem}",
    ".rp-stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem}",
    ".rp-stat{text-align:center}",
    ".rp-stat-val{font-size:1.5rem;font-weight:700;color:#2dd4bf}",
    ".rp-stat-lbl{font-size:.75rem;color:var(--md-default-fg-color--light)}",
    ".rp-progress{font-size:.8rem;color:var(--md-default-fg-color--light);margin-top:.5rem}",
  ].join("");
  document.head.appendChild(style);

  /* ── State ── */
  var episodes = [];
  var order = [];
  var idx = 0;
  var action = null; // "buy" | "sell" | "skip"
  var stopPips = 0;
  var revealed = false;
  var stats = { trades: 0, wins: 0, losses: 0, skips: 0, totalR: 0 };

  /* ── DOM ── */
  CONTAINER.innerHTML =
    '<p id="rp-loading">' + T.loading + "</p>";

  /* ── Загрузка данных ──
     URL берём из data-src на контейнере — разные значения для RU (2 уровня)
     и EN/UZ (3 уровня) чтобы путь к /data/ был одинаков везде.
  */
  var dataUrl = CONTAINER.getAttribute("data-src");
  if (!dataUrl) { showError(); return; }
  var req = new XMLHttpRequest();
  req.open("GET", dataUrl, true);
  req.onload = function () {
    if (req.status >= 200 && req.status < 300) {
      try {
        var data = JSON.parse(req.responseText);
        episodes = data.episodes || [];
        order = episodes.map(function (_, i) { return i; });
        for (var i = order.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          var tmp = order[i]; order[i] = order[j]; order[j] = tmp;
        }
        buildUI();
      } catch (e) {
        showError();
      }
    } else {
      showError();
    }
  };
  req.onerror = showError;
  req.send();

  function showError() {
    CONTAINER.innerHTML = '<p style="color:#f87171">' + T.err_load + "</p>";
  }

  /* ── Построение UI ── */
  function buildUI() {
    CONTAINER.innerHTML = [
      '<div class="rp-meta" id="rp-meta"></div>',
      '<canvas id="replay-canvas" height="300"></canvas>',
      '<div class="rp-stop-row">',
      '  <label for="rp-stop">' + T.stop_label + "</label>",
      '  <input id="rp-stop" class="rp-stop-input" type="number" min="1" max="500" placeholder="10" />',
      '  <span id="rp-stop-err" style="color:#f87171;font-size:.8rem;display:none">' + T.stop_err + "</span>",
      "</div>",
      '<div class="rp-controls" id="rp-controls">',
      '  <button class="rp-btn rp-buy" id="rp-buy">' + T.buy + "</button>",
      '  <button class="rp-btn rp-sell" id="rp-sell">' + T.sell + "</button>",
      '  <button class="rp-btn rp-skip" id="rp-skip">' + T.skip + "</button>",
      "</div>",
      '<div id="rp-result" style="display:none"></div>',
      '<div class="rp-progress" id="rp-progress"></div>',
    ].join("");

    document.getElementById("rp-buy").addEventListener("click", function () { choose("buy"); });
    document.getElementById("rp-sell").addEventListener("click", function () { choose("sell"); });
    document.getElementById("rp-skip").addEventListener("click", function () { choose("skip"); });

    showEpisode();
  }

  function showEpisode() {
    revealed = false;
    action = null;
    var ep = episodes[order[idx]];
    var canvas = document.getElementById("replay-canvas");
    var meta = document.getElementById("rp-meta");
    var resultEl = document.getElementById("rp-result");
    var ctrlEl = document.getElementById("rp-controls");
    var stopErr = document.getElementById("rp-stop-err");
    var progress = document.getElementById("rp-progress");

    resultEl.style.display = "none";
    stopErr.style.display = "none";
    document.getElementById("rp-stop").value = "";
    setButtonsEnabled(true);

    var catMap = { u: T.cat_u, d: T.cat_d, s: T.cat_s };
    meta.textContent =
      T.episode + " " + (idx + 1) + " " + T.of + " " + order.length +
      "  |  " + T.pair +
      "  |  " + T.atr + ": " + ep.atr + " " + T.pips;

    progress.textContent =
      T.stats_wins + ": " + stats.wins +
      "  " + T.stats_losses + ": " + stats.losses +
      "  " + T.stats_skips + ": " + stats.skips;

    drawChart(canvas, ep, ep.ctx - 1, false);
  }

  function choose(dir) {
    if (dir === "skip") {
      stats.skips++;
      stats.trades++;
      showResult(dir, 0);
      return;
    }
    var stopInput = document.getElementById("rp-stop");
    var stopErr = document.getElementById("rp-stop-err");
    var s = parseInt(stopInput.value, 10);
    if (!s || s < 1) {
      stopErr.style.display = "inline";
      return;
    }
    stopErr.style.display = "none";
    action = dir;
    stopPips = s;
    setButtonsEnabled(false);
    revealOutcome();
  }

  function revealOutcome() {
    var ep = episodes[order[idx]];
    var canvas = document.getElementById("replay-canvas");

    // Анимируем проигрыш свечей
    var futureStart = ep.ctx;
    var futureEnd = ep.k.length;
    var current = futureStart;

    var entry = ep.base + ep.k[futureStart - 1][3] * ep.pip;
    var sl = action === "buy"
      ? entry - stopPips * ep.pip
      : entry + stopPips * ep.pip;
    var tp = action === "buy"
      ? entry + stopPips * 2 * ep.pip   // RR 1:2
      : entry - stopPips * 2 * ep.pip;

    var hitResult = null;
    var hitR = 0;

    function step() {
      if (current >= futureEnd || hitResult) {
        // Итог
        if (!hitResult) {
          // Не дошли до SL/TP — незакрытая позиция: считаем по последней цене
          var lastClose = ep.base + ep.k[futureEnd - 1][3] * ep.pip;
          var pnlPips = action === "buy"
            ? (lastClose - entry) / ep.pip
            : (entry - lastClose) / ep.pip;
          hitR = pnlPips / stopPips;
          hitResult = hitR >= 0 ? "win" : "loss";
        }
        stats.trades++;
        if (hitResult === "win") stats.wins++;
        else stats.losses++;
        stats.totalR += hitR;
        drawChart(canvas, ep, futureEnd - 1, true, entry, sl, tp, hitResult);
        showResult(hitResult, hitR);
        return;
      }

      drawChart(canvas, ep, current, false, entry, sl, tp, null);

      // Проверяем хит на этой свече
      var c = ep.k[current];
      var high = ep.base + c[1] * ep.pip;
      var low  = ep.base + c[2] * ep.pip;

      if (action === "buy") {
        if (low <= sl) { hitResult = "loss"; hitR = -1; }
        else if (high >= tp) { hitResult = "win"; hitR = 2; }
      } else {
        if (high >= sl) { hitResult = "loss"; hitR = -1; }
        else if (low <= tp) { hitResult = "win"; hitR = 2; }
      }

      current++;
      setTimeout(step, 120);
    }

    step();
  }

  function showResult(type, r) {
    var el = document.getElementById("rp-result");
    var isLast = idx >= order.length - 1;

    var rText = r !== 0 ? " (" + (r > 0 ? "+" : "") + r.toFixed(1) + "R)" : "";
    var cls = type === "win" ? "rp-result-win" : type === "loss" ? "rp-result-loss" : "rp-result-skip";
    var label = type === "win" ? T.result_win : type === "loss" ? T.result_loss : T.result_skip;
    var nextLabel = isLast ? T.finish : T.next;

    el.className = "rp-result " + cls;
    el.innerHTML =
      label + rText +
      '&nbsp;&nbsp;<button class="rp-btn rp-next" id="rp-next">' + nextLabel + "</button>";
    el.style.display = "block";

    document.getElementById("rp-next").addEventListener("click", function () {
      if (isLast) {
        showStats();
      } else {
        idx++;
        showEpisode();
      }
    });
  }

  function showStats() {
    var wr = stats.trades > 0 ? Math.round((stats.wins / stats.trades) * 100) : 0;
    var avgR = stats.trades - stats.skips > 0
      ? (stats.totalR / (stats.trades - stats.skips)).toFixed(2)
      : "0.00";

    CONTAINER.innerHTML = [
      '<div class="rp-stats">',
      "  <h3>" + T.stats_title + "</h3>",
      '  <div class="rp-stats-grid">',
      stat(stats.trades, T.stats_trades),
      stat(stats.wins, T.stats_wins),
      stat(stats.losses, T.stats_losses),
      stat(stats.skips, T.stats_skips),
      stat(wr + "%", T.stats_wr),
      stat(avgR + "R", T.stats_rr),
      "  </div>",
      '  <button class="rp-btn rp-next" id="rp-restart" style="margin-top:1rem">' + T.restart + "</button>",
      "</div>",
    ].join("");

    document.getElementById("rp-restart").addEventListener("click", function () {
      stats = { trades: 0, wins: 0, losses: 0, skips: 0, totalR: 0 };
      idx = 0;
      for (var i = order.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = order[i]; order[i] = order[j]; order[j] = tmp;
      }
      buildUI();
    });

    // Сохранить в localStorage
    try {
      localStorage.setItem("forex_replay_stats", JSON.stringify({
        trades: stats.trades, wins: stats.wins, losses: stats.losses,
        totalR: stats.totalR, wr: wr, avgR: avgR,
        date: new Date().toISOString().slice(0, 10),
      }));
    } catch (e) {}
  }

  function stat(val, label) {
    return '<div class="rp-stat"><div class="rp-stat-val">' + val +
      '</div><div class="rp-stat-lbl">' + label + "</div></div>";
  }

  function setButtonsEnabled(on) {
    ["rp-buy", "rp-sell", "rp-skip"].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.disabled = !on;
    });
    var stopEl = document.getElementById("rp-stop");
    if (stopEl) stopEl.disabled = !on;
  }

  /* ── Canvas Chart ── */
  var BULL_COLOR  = "#2dd4bf";
  var BEAR_COLOR  = "#f87171";
  var SL_COLOR    = "#f87171";
  var TP_COLOR    = "#2dd4bf";
  var ENTRY_COLOR = "#facc15";
  var FUTURE_ALPHA = 0.5;
  var PAD = { top: 20, right: 16, bottom: 20, left: 52 };

  function drawChart(canvas, ep, upTo, showFuture, entry, sl, tp, outcome) {
    var dpr = window.devicePixelRatio || 1;
    var w = canvas.offsetWidth || 640;
    canvas.width  = w * dpr;
    canvas.height = 300 * dpr;
    var ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);

    var cw = w;
    var ch = 300;

    // Диапазон свечей для отрисовки
    var from = Math.max(0, upTo - ep.ctx + 1);
    var to   = showFuture ? ep.k.length - 1 : upTo;
    var slice = ep.k.slice(from, to + 1);

    // Определить min/max
    var minP = Infinity, maxP = -Infinity;
    slice.forEach(function (c) {
      minP = Math.min(minP, c[2]);
      maxP = Math.max(maxP, c[1]);
    });
    if (sl !== undefined) {
      minP = Math.min(minP, Math.round((sl - ep.base) / ep.pip));
      maxP = Math.max(maxP, Math.round((tp - ep.base) / ep.pip));
    }
    var range = maxP - minP || 1;
    var pad = range * 0.1;
    minP -= pad; maxP += pad;

    function y(pipVal) {
      return PAD.top + (ch - PAD.top - PAD.bottom) * (1 - (pipVal - minP) / (maxP - minP));
    }
    var barW = Math.max(2, (cw - PAD.left - PAD.right) / slice.length - 1);
    var x0 = PAD.left;

    // Фон
    ctx.fillStyle = "#0d1117";
    ctx.fillRect(0, 0, cw, ch);

    // Сетка
    ctx.strokeStyle = "#21262d";
    ctx.lineWidth = 1;
    for (var g = 0; g <= 4; g++) {
      var gy = PAD.top + ((ch - PAD.top - PAD.bottom) * g) / 4;
      ctx.beginPath(); ctx.moveTo(PAD.left, gy); ctx.lineTo(cw - PAD.right, gy); ctx.stroke();
      var pVal = maxP - ((maxP - minP) * g) / 4;
      ctx.fillStyle = "#6b7280";
      ctx.font = "10px monospace";
      ctx.fillText((ep.base + pVal * ep.pip).toFixed(4), 0, gy + 4);
    }

    // Линии SL/TP/Entry
    if (entry !== undefined) {
      var entryPips = Math.round((entry - ep.base) / ep.pip);
      var slPips    = Math.round((sl    - ep.base) / ep.pip);
      var tpPips    = Math.round((tp    - ep.base) / ep.pip);
      drawHLine(ctx, y(entryPips), PAD.left, cw - PAD.right, ENTRY_COLOR, "- - -", "Entry");
      drawHLine(ctx, y(slPips),    PAD.left, cw - PAD.right, SL_COLOR,    ".",     "SL");
      drawHLine(ctx, y(tpPips),    PAD.left, cw - PAD.right, TP_COLOR,    ".",     "TP");
    }

    // Свечи
    slice.forEach(function (c, i) {
      var isFuture = (from + i) >= ep.ctx;
      var isBull = c[3] >= c[0];
      var baseColor = isBull ? BULL_COLOR : BEAR_COLOR;
      ctx.globalAlpha = isFuture ? FUTURE_ALPHA : 1;
      ctx.strokeStyle = baseColor;
      ctx.fillStyle   = baseColor;
      ctx.lineWidth   = 1;

      var cx = x0 + i * (barW + 1) + barW / 2;
      // Тень
      ctx.beginPath();
      ctx.moveTo(cx, y(c[1]));
      ctx.lineTo(cx, y(c[2]));
      ctx.stroke();
      // Тело
      var oy = y(Math.max(c[0], c[3]));
      var cy_h = Math.max(1, Math.abs(y(c[0]) - y(c[3])));
      ctx.fillRect(x0 + i * (barW + 1), oy, barW, cy_h);
    });

    ctx.globalAlpha = 1;

    // Метка разделителя (где кончается история)
    if (showFuture) {
      var sepX = x0 + ep.ctx * (barW + 1);
      ctx.strokeStyle = "#facc15";
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 3]);
      ctx.beginPath(); ctx.moveTo(sepX, PAD.top); ctx.lineTo(sepX, ch - PAD.bottom); ctx.stroke();
      ctx.setLineDash([]);
    }

    // Бейдж результата
    if (outcome) {
      ctx.fillStyle = outcome === "win" ? BULL_COLOR : BEAR_COLOR;
      ctx.font = "bold 13px sans-serif";
      ctx.fillText(outcome === "win" ? "✓ WIN" : "✗ LOSS", cw - 70, 36);
    }
  }

  function drawHLine(ctx, yPos, x1, x2, color, dash, label) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 1;
    ctx.setLineDash(dash === "- - -" ? [6, 3] : [2, 2]);
    ctx.beginPath();
    ctx.moveTo(x1, yPos);
    ctx.lineTo(x2, yPos);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = color;
    ctx.font = "10px monospace";
    ctx.fillText(label, x2 - 28, yPos - 3);
  }
})();
