/**
 * Replay Trainer 2.0.
 *
 * Loads compact historical episodes, lets the student place Entry/SL/TP on a
 * Canvas chart, replays future candles and stores weak categories locally.
 */
(function () {
  "use strict";

  var CONTAINER = document.getElementById("replay-widget");
  if (!CONTAINER) return;

  var lang = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (lang !== "en" && lang !== "uz") lang = "ru";

  var I18N = {
    ru: {
      loading: "Загрузка эпизодов...",
      loadError: "Не удалось загрузить эпизоды. Обновите страницу.",
      episode: "Эпизод",
      of: "из",
      pair: "Пара",
      timeframe: "Таймфрейм",
      direction: "1. Выбери направление",
      levels: "2. Поставь Entry, SL и TP кликами по графику",
      buy: "Buy",
      sell: "Sell",
      skip: "Пропустить",
      start: "3. Запустить Replay",
      entry: "Entry",
      sl: "SL",
      tp: "TP",
      chooseDirection: "Сначала выбери Buy или Sell.",
      clickLevel: "Выбери уровень и кликни по графику.",
      missingLevels: "Поставь все три уровня: Entry, SL и TP.",
      invalidBuy: "Для Buy должно быть: SL < Entry < TP.",
      invalidSell: "Для Sell должно быть: TP < Entry < SL.",
      minStop: "Расстояние от Entry до SL должно быть не меньше 1 пипса.",
      win: "Прибыль",
      loss: "Убыток",
      skipped: "Пропущен",
      notTriggered: "Entry не был активирован",
      next: "Следующий эпизод",
      finish: "Статистика",
      wins: "Побед",
      losses: "Убытков",
      skips: "Пропусков",
      trades: "Сделок",
      winrate: "WinRate",
      avgR: "Средний R",
      stats: "Результаты Replay",
      restart: "Новая сессия",
      repeat: "Повторить ошибки",
      weak: "Слабая категория",
      noWeak: "Критической слабости пока нет",
      errors: "Ошибочных эпизодов",
      atr: "ATR",
      pips: "пипс",
      cat_u: "восходящий тренд",
      cat_d: "нисходящий тренд",
      cat_s: "флэт",
      preview: "Уровни можно менять до запуска.",
    },
    en: {
      loading: "Loading episodes...",
      loadError: "Could not load episodes. Refresh the page.",
      episode: "Episode",
      of: "of",
      pair: "Pair",
      timeframe: "Timeframe",
      direction: "1. Choose direction",
      levels: "2. Place Entry, SL and TP by clicking the chart",
      buy: "Buy",
      sell: "Sell",
      skip: "Skip",
      start: "3. Start Replay",
      entry: "Entry",
      sl: "SL",
      tp: "TP",
      chooseDirection: "Choose Buy or Sell first.",
      clickLevel: "Select a level and click the chart.",
      missingLevels: "Place all three levels: Entry, SL and TP.",
      invalidBuy: "Buy requires: SL < Entry < TP.",
      invalidSell: "Sell requires: TP < Entry < SL.",
      minStop: "Entry-to-SL distance must be at least 1 pip.",
      win: "Profit",
      loss: "Loss",
      skipped: "Skipped",
      notTriggered: "Entry was not triggered",
      next: "Next episode",
      finish: "Statistics",
      wins: "Wins",
      losses: "Losses",
      skips: "Skips",
      trades: "Trades",
      winrate: "WinRate",
      avgR: "Avg R",
      stats: "Replay results",
      restart: "New session",
      repeat: "Repeat mistakes",
      weak: "Weak category",
      noWeak: "No critical weakness yet",
      errors: "Failed episodes",
      atr: "ATR",
      pips: "pips",
      cat_u: "uptrend",
      cat_d: "downtrend",
      cat_s: "sideways",
      preview: "Levels can be changed before replay.",
    },
    uz: {
      loading: "Epizodlar yuklanmoqda...",
      loadError: "Epizodlarni yuklab bo'lmadi. Sahifani yangilang.",
      episode: "Epizod",
      of: "dan",
      pair: "Juftlik",
      timeframe: "Taymfreym",
      direction: "1. Yo'nalishni tanlang",
      levels: "2. Grafikda Entry, SL va TP ni belgilang",
      buy: "Buy",
      sell: "Sell",
      skip: "O'tkazish",
      start: "3. Replayni boshlash",
      entry: "Entry",
      sl: "SL",
      tp: "TP",
      chooseDirection: "Avval Buy yoki Sell ni tanlang.",
      clickLevel: "Darajani tanlang va grafikni bosing.",
      missingLevels: "Uchala darajani belgilang: Entry, SL va TP.",
      invalidBuy: "Buy uchun: SL < Entry < TP.",
      invalidSell: "Sell uchun: TP < Entry < SL.",
      minStop: "Entry va SL oralig'i kamida 1 pip bo'lishi kerak.",
      win: "Foyda",
      loss: "Zarar",
      skipped: "O'tkazildi",
      notTriggered: "Entry ishga tushmadi",
      next: "Keyingi epizod",
      finish: "Statistika",
      wins: "G'alaba",
      losses: "Zarar",
      skips: "O'tkazildi",
      trades: "Savdo",
      winrate: "WinRate",
      avgR: "O'rtacha R",
      stats: "Replay natijalari",
      restart: "Yangi sessiya",
      repeat: "Xatolarni takrorlash",
      weak: "Zaif kategoriya",
      noWeak: "Hozircha jiddiy zaiflik yo'q",
      errors: "Xato epizodlar",
      atr: "ATR",
      pips: "pip",
      cat_u: "ko'tarilish trendi",
      cat_d: "pasayish trendi",
      cat_s: "flet",
      preview: "Replay boshlanguncha darajalarni o'zgartirish mumkin.",
    },
  };
  var T = I18N[lang];

  var style = document.createElement("style");
  style.textContent = [
    "#replay-widget{font-family:inherit;max-width:860px;margin:1.5rem 0}",
    "#replay-canvas{width:100%;height:340px;border-radius:9px;background:#0d1117;display:block;cursor:crosshair;touch-action:none}",
    ".rp-toolbar,.rp-controls,.rp-levels{display:flex;gap:.55rem;flex-wrap:wrap;align-items:center}",
    ".rp-toolbar{margin-bottom:.75rem;padding:.7rem;background:var(--md-code-bg-color);border-radius:8px}",
    ".rp-toolbar label{font-size:.78rem;color:var(--md-default-fg-color--light)}",
    ".rp-select{padding:.35rem .5rem;border:1px solid var(--md-default-fg-color--lighter);border-radius:5px;background:var(--md-default-bg-color);color:var(--md-default-fg-color)}",
    ".rp-step{margin:.8rem 0 .4rem;font-size:.83rem;font-weight:700}",
    ".rp-btn{padding:.48rem .9rem;border:1px solid transparent;border-radius:6px;cursor:pointer;font-weight:650}",
    ".rp-btn:hover{filter:brightness(1.08)}",
    ".rp-btn:disabled{opacity:.4;cursor:not-allowed}",
    ".rp-buy{background:#2dd4bf;color:#0d1117}",
    ".rp-sell{background:#f87171;color:#fff}",
    ".rp-skip{background:#6b7280;color:#fff}",
    ".rp-start,.rp-next{background:#3b82f6;color:#fff}",
    ".rp-btn.rp-active{outline:3px solid #facc15;outline-offset:1px}",
    ".rp-level{background:transparent;color:var(--md-default-fg-color);border-color:var(--md-default-fg-color--lighter)}",
    ".rp-level-value{font-family:monospace;font-size:.8rem;min-width:6.5rem}",
    ".rp-level-entry{color:#facc15}.rp-level-sl{color:#f87171}.rp-level-tp{color:#2dd4bf}",
    ".rp-hint,.rp-meta,.rp-progress{font-size:.8rem;color:var(--md-default-fg-color--light)}",
    ".rp-hint{min-height:1.3rem;margin:.5rem 0}",
    ".rp-error{color:#f87171}",
    ".rp-result{margin-top:.85rem;padding:.75rem 1rem;border-radius:7px;font-weight:650}",
    ".rp-result-win{background:rgba(45,212,191,.15);border:1px solid #2dd4bf;color:#2dd4bf}",
    ".rp-result-loss{background:rgba(248,113,113,.15);border:1px solid #f87171;color:#f87171}",
    ".rp-result-skip{background:rgba(107,114,128,.15);border:1px solid #6b7280;color:#9ca3af}",
    ".rp-meta{margin:.45rem 0}",
    ".rp-progress{margin-top:.65rem}",
    ".rp-stats{background:var(--md-code-bg-color);border-radius:10px;padding:1.2rem 1.4rem}",
    ".rp-stats h3{margin:0 0 .8rem}",
    ".rp-stats-grid{display:grid;grid-template-columns:repeat(3,minmax(90px,1fr));gap:.7rem}",
    ".rp-stat{text-align:center;padding:.45rem;border-radius:6px;background:var(--md-default-bg-color)}",
    ".rp-stat-val{font-size:1.35rem;font-weight:750;color:#2dd4bf}",
    ".rp-stat-lbl{font-size:.72rem;color:var(--md-default-fg-color--light)}",
    ".rp-weak{margin:.9rem 0;padding:.7rem;border-left:3px solid #facc15;background:rgba(250,204,21,.08)}",
    "@media(max-width:600px){#replay-canvas{height:300px}.rp-stats-grid{grid-template-columns:repeat(2,1fr)}}",
  ].join("");
  document.head.appendChild(style);

  var allEpisodes = [];
  var order = [];
  var idx = 0;
  var action = null;
  var placement = "entry";
  var levels = { entry: null, sl: null, tp: null };
  var running = false;
  var chartScale = null;
  var stats = newStats();
  var repeatQueue = null;

  CONTAINER.innerHTML = '<p id="rp-loading">' + T.loading + "</p>";
  var dataUrl = CONTAINER.getAttribute("data-src");
  if (!dataUrl) return showError();

  fetch(dataUrl)
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (data) {
      allEpisodes = (data.episodes || []).map(function (ep) {
        ep.pair = ep.pair || data.pair || "EURUSD";
        ep.tf = String(ep.tf || data.tf || "H1").toUpperCase();
        ep.id = String(ep.id);
        return ep;
      });
      if (!allEpisodes.length) throw new Error("empty");
      buildUI();
    })
    .catch(showError);

  function newStats() {
    return {
      trades: 0,
      wins: 0,
      losses: 0,
      skips: 0,
      totalR: 0,
      history: [],
    };
  }

  function showError() {
    CONTAINER.innerHTML = '<p class="rp-error">' + T.loadError + "</p>";
  }

  function uniqueValues(key) {
    var seen = {};
    return allEpisodes
      .map(function (ep) { return ep[key]; })
      .filter(function (value) {
        if (seen[value]) return false;
        seen[value] = true;
        return true;
      })
      .sort();
  }

  function options(values) {
    return values
      .map(function (value) {
        return '<option value="' + value + '">' + value + "</option>";
      })
      .join("");
  }

  function buildUI() {
    var pairs = uniqueValues("pair");
    var timeframes = uniqueValues("tf");
    CONTAINER.innerHTML = [
      '<div class="rp-toolbar">',
      '<label for="rp-pair">' + T.pair + "</label>",
      '<select class="rp-select" id="rp-pair">' + options(pairs) + "</select>",
      '<label for="rp-tf">' + T.timeframe + "</label>",
      '<select class="rp-select" id="rp-tf">' + options(timeframes) + "</select>",
      "</div>",
      '<div class="rp-meta" id="rp-meta"></div>',
      '<canvas id="replay-canvas" height="340" tabindex="0"></canvas>',
      '<div class="rp-step">' + T.direction + "</div>",
      '<div class="rp-controls">',
      '<button class="rp-btn rp-buy" id="rp-buy">' + T.buy + "</button>",
      '<button class="rp-btn rp-sell" id="rp-sell">' + T.sell + "</button>",
      '<button class="rp-btn rp-skip" id="rp-skip">' + T.skip + "</button>",
      "</div>",
      '<div class="rp-step">' + T.levels + "</div>",
      '<div class="rp-levels">',
      levelButton("entry", T.entry),
      levelButton("sl", T.sl),
      levelButton("tp", T.tp),
      "</div>",
      '<div class="rp-hint" id="rp-hint">' + T.chooseDirection + "</div>",
      '<button class="rp-btn rp-start" id="rp-start" disabled>' + T.start + "</button>",
      '<div id="rp-result" style="display:none"></div>',
      '<div class="rp-progress" id="rp-progress"></div>',
    ].join("");

    document.getElementById("rp-pair").addEventListener("change", resetFiltered);
    document.getElementById("rp-tf").addEventListener("change", resetFiltered);
    document.getElementById("rp-buy").addEventListener("click", function () {
      chooseDirection("buy");
    });
    document.getElementById("rp-sell").addEventListener("click", function () {
      chooseDirection("sell");
    });
    document.getElementById("rp-skip").addEventListener("click", skipEpisode);
    document.getElementById("rp-start").addEventListener("click", startReplay);
    ["entry", "sl", "tp"].forEach(function (name) {
      document.getElementById("rp-level-" + name).addEventListener(
        "click",
        function () { selectPlacement(name); }
      );
    });
    document.getElementById("replay-canvas").addEventListener(
      "click",
      placeLevel
    );
    resetFiltered();
  }

  function levelButton(name, label) {
    return (
      '<button class="rp-btn rp-level rp-level-' + name +
      '" id="rp-level-' + name + '">' + label + "</button>" +
      '<span class="rp-level-value rp-level-' + name +
      '" id="rp-value-' + name + '">--</span>'
    );
  }

  function resetFiltered() {
    if (running) return;
    repeatQueue = null;
    stats = newStats();
    idx = 0;
    var pair = document.getElementById("rp-pair").value;
    var tf = document.getElementById("rp-tf").value;
    order = shuffle(
      allEpisodes.filter(function (ep) {
        return ep.pair === pair && ep.tf === tf;
      })
    );
    showEpisode();
  }

  function shuffle(items) {
    var copy = items.slice();
    for (var i = copy.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = copy[i];
      copy[i] = copy[j];
      copy[j] = tmp;
    }
    return copy;
  }

  function currentEpisode() {
    return order[idx];
  }

  function showEpisode() {
    if (!order.length) return showError();
    running = false;
    action = null;
    placement = "entry";
    levels = { entry: null, sl: null, tp: null };

    var ep = currentEpisode();
    var result = document.getElementById("rp-result");
    result.style.display = "none";
    document.getElementById("rp-meta").textContent =
      T.episode + " " + (idx + 1) + " " + T.of + " " + order.length +
      " | " + ep.pair + " " + ep.tf +
      " | " + T.atr + ": " + ep.atr + " " + T.pips;
    document.getElementById("rp-hint").textContent = T.chooseDirection;
    document.getElementById("rp-hint").className = "rp-hint";
    document.getElementById("rp-start").disabled = true;
    setControlsEnabled(true);
    updateLevelUI();
    updateProgress();
    drawChart(ep, ep.ctx - 1, false, null);
  }

  function chooseDirection(direction) {
    if (running) return;
    action = direction;
    document.getElementById("rp-buy").classList.toggle(
      "rp-active",
      direction === "buy"
    );
    document.getElementById("rp-sell").classList.toggle(
      "rp-active",
      direction === "sell"
    );
    selectPlacement("entry");
    setHint(T.clickLevel, false);
  }

  function selectPlacement(name) {
    if (running) return;
    placement = name;
    ["entry", "sl", "tp"].forEach(function (level) {
      document.getElementById("rp-level-" + level).classList.toggle(
        "rp-active",
        level === name
      );
    });
  }

  function placeLevel(event) {
    if (running) return;
    if (!action) return setHint(T.chooseDirection, true);
    if (!chartScale) return;

    var rect = event.currentTarget.getBoundingClientRect();
    var localY = event.clientY - rect.top;
    var price = chartScale.price(localY, rect.height);
    levels[placement] = roundToPip(price, currentEpisode().pip);

    if (placement === "entry") selectPlacement("sl");
    else if (placement === "sl") selectPlacement("tp");
    updateLevelUI();
    validateLevels(false);
    drawChart(currentEpisode(), currentEpisode().ctx - 1, false, null);
  }

  function roundToPip(price, pip) {
    return Math.round(price / pip) * pip;
  }

  function digits(ep) {
    return ep.pip >= 0.01 ? 3 : 5;
  }

  function updateLevelUI() {
    var ep = currentEpisode();
    ["entry", "sl", "tp"].forEach(function (name) {
      document.getElementById("rp-value-" + name).textContent =
        levels[name] === null ? "--" : levels[name].toFixed(digits(ep));
    });
    document.getElementById("rp-buy").classList.toggle(
      "rp-active",
      action === "buy"
    );
    document.getElementById("rp-sell").classList.toggle(
      "rp-active",
      action === "sell"
    );
  }

  function validationMessage() {
    if (!action) return T.chooseDirection;
    if (
      levels.entry === null ||
      levels.sl === null ||
      levels.tp === null
    ) return T.missingLevels;
    if (Math.abs(levels.entry - levels.sl) < currentEpisode().pip) {
      return T.minStop;
    }
    if (
      action === "buy" &&
      !(levels.sl < levels.entry && levels.entry < levels.tp)
    ) return T.invalidBuy;
    if (
      action === "sell" &&
      !(levels.tp < levels.entry && levels.entry < levels.sl)
    ) return T.invalidSell;
    return "";
  }

  function validateLevels(showError) {
    var message = validationMessage();
    document.getElementById("rp-start").disabled = Boolean(message);
    if (message) {
      setHint(showError ? message : T.preview, showError);
      return false;
    }
    setHint(T.preview, false);
    return true;
  }

  function setHint(message, isError) {
    var hint = document.getElementById("rp-hint");
    hint.textContent = message;
    hint.className = "rp-hint" + (isError ? " rp-error" : "");
  }

  function skipEpisode() {
    if (running) return;
    stats.skips++;
    stats.history.push(historyItem("skip", 0));
    setControlsEnabled(false);
    showResult("skip", 0);
  }

  function startReplay() {
    if (!validateLevels(true)) return;
    running = true;
    setControlsEnabled(false);
    replayFuture();
  }

  function replayFuture() {
    var ep = currentEpisode();
    var current = ep.ctx;
    var entered = false;
    var result = null;
    var resultR = 0;
    var risk = Math.abs(levels.entry - levels.sl);

    function step() {
      if (current >= ep.k.length || result) {
        if (!entered) {
          stats.skips++;
          stats.history.push(historyItem("not_triggered", 0));
          drawChart(ep, ep.k.length - 1, true, "not_triggered");
          showResult("not_triggered", 0);
          return;
        }
        if (!result) {
          var lastClose = price(ep, ep.k[ep.k.length - 1][3]);
          resultR = action === "buy"
            ? (lastClose - levels.entry) / risk
            : (levels.entry - lastClose) / risk;
          result = resultR >= 0 ? "win" : "loss";
        }
        recordTrade(result, resultR);
        drawChart(ep, ep.k.length - 1, true, result);
        showResult(result, resultR);
        return;
      }

      var candle = ep.k[current];
      var high = price(ep, candle[1]);
      var low = price(ep, candle[2]);
      if (!entered && low <= levels.entry && high >= levels.entry) {
        entered = true;
      }
      if (entered) {
        if (action === "buy") {
          if (low <= levels.sl) {
            result = "loss";
            resultR = -1;
          } else if (high >= levels.tp) {
            result = "win";
            resultR = (levels.tp - levels.entry) / risk;
          }
        } else if (high >= levels.sl) {
          result = "loss";
          resultR = -1;
        } else if (low <= levels.tp) {
          result = "win";
          resultR = (levels.entry - levels.tp) / risk;
        }
      }

      drawChart(ep, current, true, result);
      current++;
      window.setTimeout(step, 80);
    }
    step();
  }

  function recordTrade(result, resultR) {
    stats.trades++;
    if (result === "win") stats.wins++;
    else stats.losses++;
    stats.totalR += resultR;
    stats.history.push(historyItem(result, resultR));
  }

  function historyItem(result, resultR) {
    var ep = currentEpisode();
    return {
      id: ep.id,
      pair: ep.pair,
      tf: ep.tf,
      cat: ep.cat,
      result: result,
      r: Number(resultR.toFixed(2)),
      action: action || "skip",
      entry: levels.entry,
      sl: levels.sl,
      tp: levels.tp,
    };
  }

  function showResult(type, resultR) {
    var element = document.getElementById("rp-result");
    var isLast = idx >= order.length - 1;
    var label = type === "win"
      ? T.win
      : type === "loss"
        ? T.loss
        : type === "not_triggered"
          ? T.notTriggered
          : T.skipped;
    var className = type === "win"
      ? "rp-result-win"
      : type === "loss"
        ? "rp-result-loss"
        : "rp-result-skip";
    var rText = type === "win" || type === "loss"
      ? " (" + (resultR > 0 ? "+" : "") + resultR.toFixed(2) + "R)"
      : "";
    element.className = "rp-result " + className;
    element.innerHTML =
      label + rText +
      ' <button class="rp-btn rp-next" id="rp-next">' +
      (isLast ? T.finish : T.next) + "</button>";
    element.style.display = "block";
    document.getElementById("rp-next").addEventListener("click", function () {
      if (isLast) showStats();
      else {
        idx++;
        showEpisode();
      }
    });
    updateProgress();
  }

  function updateProgress() {
    var progress = document.getElementById("rp-progress");
    if (!progress) return;
    progress.textContent =
      T.wins + ": " + stats.wins + " | " +
      T.losses + ": " + stats.losses + " | " +
      T.skips + ": " + stats.skips;
  }

  function categoryStats() {
    var result = {};
    stats.history.forEach(function (item) {
      if (item.result !== "win" && item.result !== "loss") return;
      if (!result[item.cat]) {
        result[item.cat] = { trades: 0, losses: 0, totalR: 0 };
      }
      result[item.cat].trades++;
      if (item.result === "loss") result[item.cat].losses++;
      result[item.cat].totalR += item.r;
    });
    Object.keys(result).forEach(function (cat) {
      result[cat].avgR = result[cat].totalR / result[cat].trades;
    });
    return result;
  }

  function weakestCategory(categories) {
    var keys = Object.keys(categories);
    if (!keys.length) return "";
    keys.sort(function (a, b) {
      return categories[a].avgR - categories[b].avgR;
    });
    return categories[keys[0]].avgR < 0 ? keys[0] : "";
  }

  function categoryLabel(cat) {
    return cat ? T["cat_" + cat] : T.noWeak;
  }

  function showStats() {
    var wr = stats.trades
      ? Math.round((stats.wins / stats.trades) * 100)
      : 0;
    var avgR = stats.trades
      ? (stats.totalR / stats.trades).toFixed(2)
      : "0.00";
    var categories = categoryStats();
    var weakCategory = weakestCategory(categories);
    var errors = stats.history.filter(function (item) {
      return item.result === "loss";
    });

    CONTAINER.innerHTML = [
      '<div class="rp-stats">',
      "<h3>" + T.stats + "</h3>",
      '<div class="rp-stats-grid">',
      stat(stats.trades, T.trades),
      stat(stats.wins, T.wins),
      stat(stats.losses, T.losses),
      stat(stats.skips, T.skips),
      stat(wr + "%", T.winrate),
      stat(avgR + "R", T.avgR),
      "</div>",
      '<div class="rp-weak"><strong>' + T.weak + ":</strong> " +
        categoryLabel(weakCategory) + "<br>" +
        T.errors + ": " + errors.length + "</div>",
      '<div class="rp-controls">',
      '<button class="rp-btn rp-next" id="rp-restart">' + T.restart + "</button>",
      errors.length
        ? '<button class="rp-btn rp-sell" id="rp-repeat">' +
          T.repeat + "</button>"
        : "",
      "</div>",
      "</div>",
    ].join("");

    saveStats(wr, avgR, categories, weakCategory, errors);
    document.getElementById("rp-restart").addEventListener("click", function () {
      stats = newStats();
      repeatQueue = null;
      idx = 0;
      buildUI();
    });
    if (errors.length) {
      document.getElementById("rp-repeat").addEventListener(
        "click",
        function () { repeatErrors(errors); }
      );
    }
  }

  function repeatErrors(errors) {
    var ids = {};
    errors.forEach(function (item) { ids[item.id] = true; });
    repeatQueue = allEpisodes.filter(function (ep) { return ids[ep.id]; });
    stats = newStats();
    idx = 0;
    buildUI();
    order = shuffle(repeatQueue);
    showEpisode();
  }

  function saveStats(wr, avgR, categories, weakCategory, errors) {
    try {
      localStorage.setItem("forex_replay_stats", JSON.stringify({
        version: 2,
        trades: stats.trades,
        wins: stats.wins,
        losses: stats.losses,
        skips: stats.skips,
        totalR: Number(stats.totalR.toFixed(2)),
        wr: wr,
        avgR: avgR,
        categories: categories,
        weakCategory: weakCategory,
        errors: errors.map(function (item) { return item.id; }),
        date: new Date().toISOString().slice(0, 10),
      }));
    } catch (error) {
      // localStorage can be disabled; Replay itself should still work.
    }
    try {
      var first15 = JSON.parse(localStorage.getItem("forex_first15_v1") || "{}");
      first15.replay = true;
      first15.updatedAt = new Date().toISOString();
      localStorage.setItem("forex_first15_v1", JSON.stringify(first15));
    } catch (error) {}
    if (window.fxTrack) window.fxTrack("replay_completed");
  }

  function stat(value, label) {
    return '<div class="rp-stat"><div class="rp-stat-val">' + value +
      '</div><div class="rp-stat-lbl">' + label + "</div></div>";
  }

  function setControlsEnabled(enabled) {
    [
      "rp-buy",
      "rp-sell",
      "rp-skip",
      "rp-level-entry",
      "rp-level-sl",
      "rp-level-tp",
    ].forEach(function (id) {
      var element = document.getElementById(id);
      if (element) element.disabled = !enabled;
    });
    var canvas = document.getElementById("replay-canvas");
    if (canvas) canvas.style.cursor = enabled ? "crosshair" : "default";
    ["rp-pair", "rp-tf"].forEach(function (id) {
      var select = document.getElementById(id);
      if (select) select.disabled = !enabled;
    });
  }

  var COLORS = {
    bull: "#2dd4bf",
    bear: "#f87171",
    entry: "#facc15",
    sl: "#f87171",
    tp: "#2dd4bf",
  };
  var PAD = { top: 20, right: 16, bottom: 22, left: 58 };

  function price(ep, pipValue) {
    return ep.base + pipValue * ep.pip;
  }

  function drawChart(ep, upTo, showFuture, outcome) {
    var canvas = document.getElementById("replay-canvas");
    if (!canvas) return;
    var dpr = window.devicePixelRatio || 1;
    var width = canvas.offsetWidth || 760;
    var height = canvas.offsetHeight || 340;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    var context = canvas.getContext("2d");
    context.scale(dpr, dpr);

    var candles = ep.k.slice(0, upTo + 1);
    var minPips = Infinity;
    var maxPips = -Infinity;
    candles.forEach(function (candle) {
      minPips = Math.min(minPips, candle[2]);
      maxPips = Math.max(maxPips, candle[1]);
    });
    if (!showFuture && levels.entry !== null) {
      ["entry", "sl", "tp"].forEach(function (name) {
        if (levels[name] === null) return;
        var value = (levels[name] - ep.base) / ep.pip;
        minPips = Math.min(minPips, value);
        maxPips = Math.max(maxPips, value);
      });
    }
    var range = maxPips - minPips || 10;
    minPips -= range * 0.12;
    maxPips += range * 0.12;

    function y(pipValue) {
      return PAD.top +
        (height - PAD.top - PAD.bottom) *
        (1 - (pipValue - minPips) / (maxPips - minPips));
    }
    chartScale = {
      price: function (pixelY, renderedHeight) {
        var scaledY = pixelY * (height / renderedHeight);
        var ratio = (scaledY - PAD.top) /
          (height - PAD.top - PAD.bottom);
        var pipValue = maxPips - ratio * (maxPips - minPips);
        return price(ep, pipValue);
      },
    };

    context.fillStyle = "#0d1117";
    context.fillRect(0, 0, width, height);
    drawGrid(context, ep, width, height, minPips, maxPips, y);

    var chartWidth = width - PAD.left - PAD.right;
    var barStep = chartWidth / Math.max(candles.length, ep.k.length);
    var barWidth = Math.max(2, barStep - 1);
    candles.forEach(function (candle, index) {
      var future = index >= ep.ctx;
      var bullish = candle[3] >= candle[0];
      context.globalAlpha = future ? 0.58 : 1;
      context.strokeStyle = bullish ? COLORS.bull : COLORS.bear;
      context.fillStyle = context.strokeStyle;
      var x = PAD.left + index * barStep + barStep / 2;
      context.beginPath();
      context.moveTo(x, y(candle[1]));
      context.lineTo(x, y(candle[2]));
      context.stroke();
      var bodyTop = y(Math.max(candle[0], candle[3]));
      var bodyHeight = Math.max(1, Math.abs(y(candle[0]) - y(candle[3])));
      context.fillRect(x - barWidth / 2, bodyTop, barWidth, bodyHeight);
    });
    context.globalAlpha = 1;

    drawLevels(context, ep, width, y);
    if (showFuture) {
      var divider = PAD.left + ep.ctx * barStep;
      context.strokeStyle = COLORS.entry;
      context.setLineDash([5, 4]);
      context.beginPath();
      context.moveTo(divider, PAD.top);
      context.lineTo(divider, height - PAD.bottom);
      context.stroke();
      context.setLineDash([]);
    }
    if (outcome === "win" || outcome === "loss") {
      context.fillStyle = outcome === "win" ? COLORS.bull : COLORS.bear;
      context.font = "bold 13px sans-serif";
      context.fillText(
        outcome === "win" ? "WIN" : "LOSS",
        width - 62,
        36
      );
    }
  }

  function drawGrid(context, ep, width, height, minPips, maxPips, y) {
    context.strokeStyle = "#21262d";
    context.lineWidth = 1;
    for (var index = 0; index <= 4; index++) {
      var pipValue = maxPips - ((maxPips - minPips) * index) / 4;
      var lineY = y(pipValue);
      context.beginPath();
      context.moveTo(PAD.left, lineY);
      context.lineTo(width - PAD.right, lineY);
      context.stroke();
      context.fillStyle = "#6b7280";
      context.font = "10px monospace";
      context.fillText(
        price(ep, pipValue).toFixed(digits(ep)),
        2,
        Math.min(height - 3, lineY + 4)
      );
    }
  }

  function drawLevels(context, ep, width, y) {
    ["entry", "sl", "tp"].forEach(function (name) {
      if (levels[name] === null) return;
      var pipValue = (levels[name] - ep.base) / ep.pip;
      context.strokeStyle = COLORS[name];
      context.fillStyle = COLORS[name];
      context.lineWidth = name === "entry" ? 1.5 : 1;
      context.setLineDash(name === "entry" ? [6, 3] : [2, 2]);
      context.beginPath();
      context.moveTo(PAD.left, y(pipValue));
      context.lineTo(width - PAD.right, y(pipValue));
      context.stroke();
      context.setLineDash([]);
      context.font = "10px monospace";
      context.fillText(
        name.toUpperCase(),
        width - PAD.right - 34,
        y(pipValue) - 3
      );
    });
  }
})();
