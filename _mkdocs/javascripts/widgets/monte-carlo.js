(function () {
  "use strict";

  var root = document.getElementById("monte-carlo-widget");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var SETTINGS_KEY = "forex_tool_settings_v1";
  var T = F.pick({
    ru: {
      balance: "Начальный капитал, USD", rate: "USD -> UZS", simulations: "Симуляций",
      trades: "Сделок в серии", wr: "Win rate, %", rr: "Reward/Risk", risk: "Риск на сделку, %",
      seed: "Seed", run: "Запустить симуляцию", median: "Медианный финал", bad: "Финал в худших 5%",
      dd: "Медианная макс. просадка", dd95: "Просадка в худших 5%", loss: "Вероятность закончить в минусе",
      dd20: "Вероятность просадки 20%+", ruin: "Риск потерять 50% капитала", streak: "Убыточная серия в худших 5%",
      comparison: "Сравнение риска", riskLevel: "Риск", journalSource: "Параметры подставлены из твоего журнала.",
      smallSample: function (count) { return "Осторожно: в журнале только " + count + " сделок. Для устойчивой оценки нужно хотя бы 30."; },
      note: "Это модель независимых сделок с постоянными WR, R:R и риском. Она не предсказывает рынок."
    },
    en: {
      balance: "Starting capital, USD", rate: "USD -> UZS", simulations: "Simulations",
      trades: "Trades per run", wr: "Win rate, %", rr: "Reward/Risk", risk: "Risk per trade, %",
      seed: "Seed", run: "Run simulation", median: "Median final balance", bad: "Final balance in worst 5%",
      dd: "Median max drawdown", dd95: "Drawdown in worst 5%", loss: "Probability of finishing down",
      dd20: "Probability of 20%+ drawdown", ruin: "Risk of losing 50% of capital", streak: "Losing streak in worst 5%",
      comparison: "Risk comparison", riskLevel: "Risk", journalSource: "Parameters were filled from your journal.",
      smallSample: function (count) { return "Caution: your journal has only " + count + " trades. Use at least 30 for a stable estimate."; },
      note: "This model assumes independent trades and constant WR, R:R and risk. It does not predict the market."
    },
    uz: {
      balance: "Boshlang'ich kapital, USD", rate: "USD -> UZS", simulations: "Simulyatsiyalar",
      trades: "Seriyadagi savdolar", wr: "Win rate, %", rr: "Reward/Risk", risk: "Har savdoda risk, %",
      seed: "Seed", run: "Simulyatsiyani boshlash", median: "Median yakuniy balans", bad: "Eng yomon 5% dagi balans",
      dd: "Median maksimal pasayish", dd95: "Eng yomon 5% dagi pasayish", loss: "Minusda tugash ehtimoli",
      dd20: "20%+ pasayish ehtimoli", ruin: "Kapitalning 50% ini yo'qotish riski", streak: "Eng yomon 5% dagi zarar seriyasi",
      comparison: "Risk taqqoslash", riskLevel: "Risk", journalSource: "Parametrlar jurnalingizdan olindi.",
      smallSample: function (count) { return "Ehtiyot bo'ling: jurnalda faqat " + count + " savdo bor. Barqaror baho uchun kamida 30 ta kerak."; },
      note: "Model mustaqil savdolar va doimiy WR, R:R hamda riskni faraz qiladi. U bozorni bashorat qilmaydi."
    }
  });

  var settings = readSettings();
  var profile = settings.monteCarlo && settings.monteCarlo.source === "journal" ? settings.monteCarlo : null;
  var desk = settings.tradeDesk || {};

  root.innerHTML = [
    '<div id="mco-source" class="fx-tool-note" hidden></div>',
    '<div class="fx-tool-grid">',
    field(T.balance, "mco-balance", desk.balance || 1000, 'min="1"'),
    field(T.rate, "mco-rate", desk.usdUzs || 12500, 'min="1"'),
    field(T.simulations, "mco-sims", 1000, 'min="100" max="10000" step="100"'),
    field(T.trades, "mco-trades", profile ? profile.trades : 100, 'min="10" max="1000"'),
    field(T.wr, "mco-wr", profile ? Number(profile.winRate).toFixed(1) : 45, 'min="0" max="100" step="0.1"'),
    field(T.rr, "mco-rr", profile ? Number(profile.rewardRisk).toFixed(2) : 2, 'min="0.1" step="0.1"'),
    field(T.risk, "mco-risk", 1, 'min="0.1" max="20" step="0.1"'),
    field(T.seed, "mco-seed", 42, 'min="1" step="1"'),
    '</div>',
    '<div class="fx-tool-actions"><button id="mco-run" type="button">' + T.run + '</button></div>',
    '<div id="mco-result" class="fx-result" hidden></div>',
    '<canvas id="mco-chart" class="fx-chart" width="900" height="300" hidden></canvas>',
    '<section id="mco-risk-comparison" class="fx-result" hidden></section>',
    '<p class="fx-tool-note">' + T.note + '</p>'
  ].join("");

  if (profile) {
    var source = document.getElementById("mco-source");
    source.textContent = T.journalSource + (profile.sampleSize < 30 ? " " + T.smallSample(profile.sampleSize) : "");
    source.hidden = false;
  }

  function readSettings() {
    try {
      var value = JSON.parse(localStorage.getItem(SETTINGS_KEY) || "{}");
      return value && typeof value === "object" && !Array.isArray(value) ? value : {};
    } catch (e) {
      return {};
    }
  }

  function field(label, id, value, extra) {
    return '<label><span>' + label + '</span><input id="' + id + '" type="number" value="' + value + '" ' + (extra || "") + '></label>';
  }

  function rng(seed) {
    var state = Math.floor(seed) % 2147483647;
    if (state <= 0) state = 1;
    return function () {
      state = state * 48271 % 2147483647;
      return (state - 1) / 2147483646;
    };
  }

  function percentile(values, p) {
    var sorted = values.slice().sort(function (a, b) { return a - b; });
    var index = (sorted.length - 1) * p / 100;
    var lower = Math.floor(index);
    var fraction = index - lower;
    return lower + 1 < sorted.length ? sorted[lower] + (sorted[lower + 1] - sorted[lower]) * fraction : sorted[lower];
  }

  function val(id) { return Number(document.getElementById(id).value); }
  function pct(value) { return (value * 100).toFixed(1) + "%"; }

  function simulate(sims, trades, wr, rr, risk, seed) {
    var random = rng(seed);
    var finals = [], drawdowns = [], streaks = [], ruined = 0;
    for (var s = 0; s < sims; s++) {
      var equity = 1, peak = 1, maxDrawdown = 0, streak = 0, maxStreak = 0, hit = false;
      for (var i = 0; i < trades; i++) {
        if (random() < wr) {
          equity *= 1 + risk * rr;
          streak = 0;
        } else {
          equity *= 1 - risk;
          streak++;
          maxStreak = Math.max(maxStreak, streak);
        }
        peak = Math.max(peak, equity);
        maxDrawdown = Math.max(maxDrawdown, (peak - equity) / peak);
        if (equity <= 0.5) hit = true;
      }
      finals.push(equity);
      drawdowns.push(maxDrawdown);
      streaks.push(maxStreak);
      if (hit) ruined++;
    }
    return { finals: finals, drawdowns: drawdowns, streaks: streaks, ruined: ruined };
  }

  function draw(finals, balance) {
    var canvas = document.getElementById("mco-chart");
    var ctx = canvas.getContext("2d");
    var width = canvas.width, height = canvas.height;
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue("--md-default-bg-color") || "#fff";
    ctx.fillRect(0, 0, width, height);
    var sorted = finals.slice().sort(function (a, b) { return a - b; });
    var max = Math.max.apply(null, sorted), min = Math.min.apply(null, sorted);
    ctx.strokeStyle = "#3b82f6";
    ctx.lineWidth = 3;
    ctx.beginPath();
    sorted.forEach(function (value, index) {
      var x = 20 + index / Math.max(1, sorted.length - 1) * (width - 40);
      var y = height - 20 - (value - min) / (max - min || 1) * (height - 40);
      if (index === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.strokeStyle = "#ef4444";
    var breakEvenY = height - 20 - (1 - min) / (max - min || 1) * (height - 40);
    ctx.beginPath(); ctx.moveTo(20, breakEvenY); ctx.lineTo(width - 20, breakEvenY); ctx.stroke();
    canvas.hidden = false;
    canvas.setAttribute("aria-label", "Monte Carlo final balance distribution, starting balance " + balance);
  }

  function comparison(config) {
    var levels = [0.5, 1, 2];
    var panel = document.getElementById("mco-risk-comparison");
    panel.innerHTML = '<h3>' + T.comparison + '</h3><div class="fx-metrics">' + levels.map(function (level) {
      var result = simulate(config.sims, config.trades, config.wr, config.rr, level / 100, config.seed);
      var median = percentile(result.finals, 50) * config.balance;
      var badDrawdown = percentile(result.drawdowns, 95);
      return '<div><span>' + T.riskLevel + ' ' + level.toFixed(1) + '%</span><strong>' + F.money(median) + '</strong><small>' + T.dd95 + ': ' + pct(badDrawdown) + '<br>' + T.ruin + ': ' + pct(result.ruined / config.sims) + '</small></div>';
    }).join("") + '</div>';
    panel.hidden = false;
  }

  function saveCurrentSettings() {
    try {
      var current = readSettings();
      current.monteCarloLast = {
        balance: val("mco-balance"), usdUzs: val("mco-rate"), riskPct: val("mco-risk"),
        updatedAt: new Date().toISOString()
      };
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(current));
    } catch (e) {}
  }

  function run() {
    var config = {
      sims: Math.min(10000, Math.floor(val("mco-sims"))),
      trades: Math.min(1000, Math.floor(val("mco-trades"))),
      wr: val("mco-wr") / 100,
      rr: val("mco-rr"),
      risk: val("mco-risk") / 100,
      balance: val("mco-balance"),
      rate: val("mco-rate"),
      seed: val("mco-seed")
    };
    if (!(config.sims > 0 && config.trades > 0 && config.wr >= 0 && config.wr <= 1 && config.rr > 0 && config.risk > 0 && config.risk < 1 && config.balance > 0 && config.rate > 0)) return;
    var result = simulate(config.sims, config.trades, config.wr, config.rr, config.risk, config.seed);
    var metrics = [
      [T.median, F.money(percentile(result.finals, 50) * config.balance) + " / " + Math.round(percentile(result.finals, 50) * config.balance * config.rate).toLocaleString(F.numLocale) + " UZS"],
      [T.bad, F.money(percentile(result.finals, 5) * config.balance)],
      [T.dd, pct(percentile(result.drawdowns, 50))],
      [T.dd95, pct(percentile(result.drawdowns, 95))],
      [T.loss, pct(result.finals.filter(function (value) { return value < 1; }).length / config.sims)],
      [T.dd20, pct(result.drawdowns.filter(function (value) { return value >= 0.2; }).length / config.sims)],
      [T.ruin, pct(result.ruined / config.sims)],
      [T.streak, Math.round(percentile(result.streaks, 95))]
    ];
    var output = document.getElementById("mco-result");
    output.innerHTML = '<div class="fx-metrics">' + metrics.map(function (metric) {
      return '<div><span>' + metric[0] + '</span><strong>' + metric[1] + '</strong></div>';
    }).join("") + '</div>';
    output.hidden = false;
    draw(result.finals, config.balance);
    comparison(config);
    saveCurrentSettings();
    if (window.fxTrack) window.fxTrack("monte_carlo_completed", { once: false });
  }

  document.getElementById("mco-run").addEventListener("click", run);
  if (profile && new URLSearchParams(window.location.search).get("journal") === "1") run();
})();
