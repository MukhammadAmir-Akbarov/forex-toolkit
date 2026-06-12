/*
 * Калькулятор размера позиции — общая логика для всех локалей.
 * compute() идентичен tools/position_calculator.py:
 *   lots = (balance * risk% / 100) / (stopPips * pipValue), округление вниз до 0.01.
 * pip value: статичная таблица либо live-курс (api.frankfurter.app / ECB).
 * Строки локализованы через таблицу T; математика и id-шники — единые.
 */
(function () {
  if (!document.getElementById("pc-calc-btn")) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      errBalance: "Депозит должен быть больше 0.",
      errRisk: "Риск должен быть в диапазоне 0 < x ≤ 10%.",
      errStop: "Стоп-лосс должен быть больше 0 пипсов.",
      srcTable: "таблица",
      srcConstant: "константа",
      loading: "Загрузка курса…",
      liveFail: "⚠️ Не удалось получить актуальный курс — использую табличное значение.",
      pips: " пипсов",
      pipUnit: "/пипс",
      lot: " лот",
      riskHigh: function (p) {
        return "⛔ Риск " + p + " депозита — это очень много. По статистике, такие риски приводят к обнулению счёта в течение месяца.";
      },
      riskMed: function (p) {
        return "⚠️ Риск " + p + " депозита — выше рекомендованного для новичка (≤ 2%). Подумай о меньшем риске или большем стопе.";
      },
      rounding: function (actual, planned) {
        return "⚠️ После округления реальный риск " + actual + " больше планового " + planned + " — уменьши лот вручную в терминале до 0.01.";
      },
      minLot: "ℹ️ Расчёт даёт меньше 0.01 лота — установлен минимум брокера. Для соблюдения риска уменьши стоп-лосс или увеличь депозит.",
    },
    en: {
      errBalance: "Balance must be greater than 0.",
      errRisk: "Risk must be in 0 < x ≤ 10%.",
      errStop: "Stop-loss must be greater than 0 pips.",
      srcTable: "static table",
      srcConstant: "constant",
      loading: "Loading rate…",
      liveFail: "⚠️ Could not fetch live rate — using static table value.",
      pips: " pips",
      pipUnit: "/pip",
      lot: " lot",
      riskHigh: function (p) {
        return "⛔ Risk of " + p + " is very high. Statistically this leads to account blowups within a month.";
      },
      riskMed: function (p) {
        return "⚠️ Risk of " + p + " is above the beginner-recommended ≤ 2%. Consider smaller risk or wider stop.";
      },
      rounding: function (actual, planned) {
        return "⚠️ Rounding pushed actual risk " + actual + " above planned " + planned + " — manually lower lot to 0.01.";
      },
      minLot: "ℹ️ Calculation gives less than 0.01 lot — broker minimum applied. Tighten your stop or grow your account to stay within the planned risk.",
    },
    uz: {
      errBalance: "Balans 0 dan katta bo'lishi kerak.",
      errRisk: "Xavf 0 < x ≤ 10% oraliqda bo'lishi kerak.",
      errStop: "Stop-loss 0 dan katta pips bo'lishi kerak.",
      srcTable: "jadval",
      srcConstant: "doimiy",
      loading: "Kurs yuklanmoqda…",
      liveFail: "⚠️ Jonli kursni olib bo'lmadi — jadval qiymatidan foydalanildi.",
      pips: " pips",
      pipUnit: "/pip",
      lot: " lot",
      riskHigh: function (p) {
        return "⛔ " + p + " xavf — juda yuqori. Statistikaga ko'ra, bunday xavflar bir oy ichida hisobni nolga keltiradi.";
      },
      riskMed: function (p) {
        return "⚠️ " + p + " xavf yangi boshlovchi uchun tavsiya etilgan ≤ 2% dan yuqori. Kichikroq xavf yoki kengroq stop haqida o'ylab ko'ring.";
      },
      rounding: function (actual, planned) {
        return "⚠️ Yumalashdan keyin real xavf " + actual + " rejalashtirilgan " + planned + " dan ortdi — terminalda lotni 0.01 ga qo'lda kamaytiring.";
      },
      minLot: "ℹ️ Hisob 0.01 lotdan kam beradi — broker minimumi qo'llanildi. Stopni qisqartiring yoki depozit oshiring.",
    },
  });

  var PIP_VALUES_STATIC = {
    EURUSD: 10.0, GBPUSD: 10.0, AUDUSD: 10.0, NZDUSD: 10.0,
    USDJPY: 6.7, USDCHF: 11.3, USDCAD: 7.3,
    EURJPY: 6.7, GBPJPY: 6.7, EURGBP: 12.7,
  };
  var LIVE_SENSITIVE = new Set(["USDJPY", "USDCHF", "USDCAD", "EURJPY", "GBPJPY", "EURGBP"]);

  async function fetchRate(pair) {
    var base = pair.slice(0, 3);
    var quote = pair.slice(3, 6);
    try {
      var r = await fetch("https://api.frankfurter.app/latest?from=" + base + "&to=" + quote);
      if (!r.ok) return null;
      var d = await r.json();
      return d.rates && d.rates[quote] ? d.rates[quote] : null;
    } catch (e) {
      return null;
    }
  }

  async function livePipValue(pair) {
    var base = pair.slice(0, 3);
    var quote = pair.slice(3, 6);
    var pipSize = quote === "JPY" ? 0.01 : 0.0001;
    var lot = 100000;

    if (quote === "USD") {
      return { value: pipSize * lot, source: T.srcConstant };
    }
    if (base === "USD") {
      var rate = await fetchRate(pair);
      if (!rate) return null;
      return { value: (pipSize * lot) / rate, source: "ECB: 1 USD = " + rate.toFixed(4) + " " + quote };
    }
    var pipValueQuote = pipSize * lot;
    var quoteToUsd = await fetchRate(quote + "USD");
    if (!quoteToUsd) {
      var usdToQuote = await fetchRate("USD" + quote);
      if (!usdToQuote) return null;
      return { value: pipValueQuote / usdToQuote, source: "ECB: USD/" + quote + " = " + usdToQuote.toFixed(4) };
    }
    return { value: pipValueQuote * quoteToUsd, source: "ECB: " + quote + "/USD = " + quoteToUsd.toFixed(4) };
  }

  function compute(balance, riskPct, stopPips, pipValue) {
    var riskAmount = (balance * riskPct) / 100;
    var lots = riskAmount / (stopPips * pipValue);
    var lotsRounded = Math.floor(lots * 100 + 1e-9) / 100;
    if (lotsRounded < 0.01) lotsRounded = 0.01;
    var actualRisk = lotsRounded * stopPips * pipValue;
    var actualRiskPct = (actualRisk / balance) * 100;
    return { riskAmount: riskAmount, lots: lots, lotsRounded: lotsRounded, actualRisk: actualRisk, actualRiskPct: actualRiskPct };
  }

  var fmtPct = function (v) { return v.toFixed(2) + "%"; };
  var fmtLots = function (v) { return v.toFixed(4); };
  var fmtLotsR = function (v) { return v.toFixed(2); };

  async function recalc() {
    var balance = parseFloat(document.getElementById("pc-balance").value);
    var riskPct = parseFloat(document.getElementById("pc-risk").value);
    var stopPips = parseFloat(document.getElementById("pc-stop").value);
    var pair = document.getElementById("pc-pair").value;
    var live = document.getElementById("pc-live").checked;

    var result = document.getElementById("pc-result");
    var warnings = document.getElementById("pc-warnings");
    warnings.innerHTML = "";

    var errors = [];
    if (!(balance > 0)) errors.push(T.errBalance);
    if (!(riskPct > 0 && riskPct <= 10)) errors.push(T.errRisk);
    if (!(stopPips > 0)) errors.push(T.errStop);
    if (errors.length) {
      result.style.display = "block";
      result.className = "danger";
      document.getElementById("pc-headline").textContent = "—";
      warnings.innerHTML = errors
        .map(function (e) {
          return '<div class="pc-warn pc-danger">⛔ ' + e + "</div>";
        })
        .join("");
      return;
    }

    var pipValue = PIP_VALUES_STATIC[pair];
    var pipSource = T.srcTable;
    if (live && LIVE_SENSITIVE.has(pair)) {
      document.getElementById("pc-headline").textContent = T.loading;
      result.style.display = "block";
      var live_pv = await livePipValue(pair);
      if (live_pv && live_pv.value > 0) {
        pipValue = live_pv.value;
        pipSource = live_pv.source;
      } else {
        warnings.innerHTML += '<div class="pc-warn">' + T.liveFail + "</div>";
      }
    }

    var r = compute(balance, riskPct, stopPips, pipValue);

    document.getElementById("pc-out-balance").textContent = F.money(balance);
    document.getElementById("pc-out-risk-plan").textContent = fmtPct(riskPct) + " = " + F.money(r.riskAmount);
    document.getElementById("pc-out-stop").textContent = stopPips + T.pips;
    document.getElementById("pc-out-pair").textContent = pair;
    document.getElementById("pc-out-pip").textContent = F.money(pipValue) + T.pipUnit + " (" + pipSource + ")";
    document.getElementById("pc-out-lots-exact").textContent = fmtLots(r.lots);
    document.getElementById("pc-out-lots-rounded").textContent = fmtLotsR(r.lotsRounded);
    document.getElementById("pc-out-actual").textContent = F.money(r.actualRisk) + " (" + fmtPct(r.actualRiskPct) + ")";
    document.getElementById("pc-headline").textContent = fmtLotsR(r.lotsRounded) + T.lot;
    result.style.display = "block";

    var cls = "ok";
    if (r.actualRiskPct > 5) {
      cls = "danger";
      warnings.innerHTML += '<div class="pc-warn pc-danger">' + T.riskHigh(fmtPct(r.actualRiskPct)) + "</div>";
    } else if (r.actualRiskPct > 2) {
      cls = "warn";
      warnings.innerHTML += '<div class="pc-warn">' + T.riskMed(fmtPct(r.actualRiskPct)) + "</div>";
    }
    if (r.actualRisk > r.riskAmount * 1.05) {
      cls = cls === "ok" ? "warn" : cls;
      warnings.innerHTML += '<div class="pc-warn">' + T.rounding(F.money(r.actualRisk), F.money(r.riskAmount)) + "</div>";
    }
    if (r.lotsRounded === 0.01 && r.lots < 0.005) {
      warnings.innerHTML += '<div class="pc-warn pc-info">' + T.minLot + "</div>";
    }
    result.className = cls === "ok" ? "" : cls;
  }

  ["pc-balance", "pc-risk", "pc-stop", "pc-pair", "pc-live"].forEach(function (id) {
    var el = document.getElementById(id);
    el.addEventListener("input", recalc);
    el.addEventListener("change", recalc);
  });
  document.getElementById("pc-calc-btn").addEventListener("click", recalc);

  recalc();
})();
