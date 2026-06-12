/*
 * Калькулятор стоимости пункта (pip value) — общая логика для всех локалей.
 * Стоимость пункта в валюте котировки = pipSize * 100000 * lots, далее
 * конвертация в USD по курсу (live из api.frankfurter.app либо статичная таблица).
 * Деньги форматируются с 4 знаками после запятой (F.money(v, 4)).
 *
 * Примечание: в исходной UZ-копии fmt$ ошибочно использовал локаль 'ru-RU';
 * здесь формат берётся из текущей локали страницы через F.money.
 */
(function () {
  if (!document.getElementById("pp-calc-btn")) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      errLots: "Размер позиции должен быть больше 0.",
      srcTable: "таблица",
      srcTableInv: "таблица (обратно)",
      usdQuote: "— (USD — quote)",
      loading: "Загрузка курса…",
      fetchFail: "⚠️ Не удалось получить курс. Попробуй позже.",
      pipSuffix: " / пипс",
    },
    en: {
      errLots: "Position size must be greater than 0.",
      srcTable: "static",
      srcTableInv: "static (inv)",
      usdQuote: "— (USD is quote)",
      loading: "Loading rate…",
      fetchFail: "⚠️ Could not fetch rate.",
      pipSuffix: " / pip",
    },
    uz: {
      errLots: "Pozitsiya hajmi 0 dan katta bo'lishi kerak.",
      srcTable: "jadval",
      srcTableInv: "jadval (teskari)",
      usdQuote: "— (USD — quote)",
      loading: "Kurs yuklanmoqda…",
      fetchFail: "⚠️ Kursni olib bo'lmadi. Keyinroq urinib ko'ring.",
      pipSuffix: " / pip",
    },
  });

  var STATIC_RATES = {
    "USD-JPY": 150, "USD-CHF": 0.88, "USD-CAD": 1.37,
    "EUR-USD": 1.08, "GBP-USD": 1.27, "AUD-USD": 0.66,
    "NZD-USD": 0.6, "EUR-GBP": 0.85,
  };

  async function fetchRate(base, quote) {
    try {
      var r = await fetch("https://api.frankfurter.app/latest?from=" + base + "&to=" + quote);
      if (!r.ok) return null;
      var d = await r.json();
      return d.rates && d.rates[quote] ? d.rates[quote] : null;
    } catch (e) {
      return null;
    }
  }

  async function getRate(base, quote, live) {
    if (live) {
      var r = await fetchRate(base, quote);
      if (r) return { value: r, source: "ECB live" };
    }
    var key = base + "-" + quote;
    if (STATIC_RATES[key]) return { value: STATIC_RATES[key], source: T.srcTable };
    var rev = quote + "-" + base;
    if (STATIC_RATES[rev]) return { value: 1 / STATIC_RATES[rev], source: T.srcTableInv };
    return null;
  }

  async function calculate() {
    var pair = document.getElementById("pp-pair").value;
    var lots = parseFloat(document.getElementById("pp-lots").value);
    var live = document.getElementById("pp-live").checked;
    var result = document.getElementById("pp-result");
    var warnings = document.getElementById("pp-warnings");
    warnings.innerHTML = "";

    if (!(lots > 0)) {
      result.style.display = "block";
      result.className = "pc-result danger";
      document.getElementById("pp-headline").textContent = "—";
      warnings.innerHTML = '<div class="pc-warn pc-danger">⛔ ' + T.errLots + "</div>";
      return;
    }

    var base = pair.slice(0, 3);
    var quote = pair.slice(3, 6);
    var pipSize = quote === "JPY" ? 0.01 : 0.0001;
    var pipValueQuote = pipSize * 100000 * lots;

    var pipValueUSD;
    var rateUsed = "—";

    if (quote === "USD") {
      pipValueUSD = pipValueQuote;
      rateUsed = T.usdQuote;
    } else if (base === "USD") {
      document.getElementById("pp-headline").textContent = T.loading;
      result.style.display = "block";
      var r1 = await getRate(base, quote, live);
      if (!r1) {
        warnings.innerHTML = '<div class="pc-warn">' + T.fetchFail + "</div>";
        return;
      }
      pipValueUSD = pipValueQuote / r1.value;
      rateUsed = "1 USD = " + r1.value.toFixed(4) + " " + quote + " (" + r1.source + ")";
    } else {
      document.getElementById("pp-headline").textContent = T.loading;
      result.style.display = "block";
      var r = await getRate(quote, "USD", live);
      if (r) {
        pipValueUSD = pipValueQuote * r.value;
        rateUsed = "1 " + quote + " = " + r.value.toFixed(4) + " USD (" + r.source + ")";
      } else {
        r = await getRate("USD", quote, live);
        if (!r) {
          warnings.innerHTML = '<div class="pc-warn">' + T.fetchFail + "</div>";
          return;
        }
        pipValueUSD = pipValueQuote / r.value;
        rateUsed = "1 USD = " + r.value.toFixed(4) + " " + quote + " (" + r.source + ")";
      }
    }

    document.getElementById("pp-out-pair").textContent = pair;
    document.getElementById("pp-out-lots").textContent = lots.toFixed(2);
    document.getElementById("pp-out-pipsize").textContent = pipSize.toString();
    document.getElementById("pp-out-rate").textContent = rateUsed;
    document.getElementById("pp-out-pip").textContent = F.money(pipValueUSD, 4);
    document.getElementById("pp-out-10").textContent = F.money(pipValueUSD * 10, 4);
    document.getElementById("pp-headline").textContent = F.money(pipValueUSD, 4) + T.pipSuffix;
    result.style.display = "block";
    result.className = "pc-result";
  }

  ["pp-pair", "pp-lots", "pp-live"].forEach(function (id) {
    var el = document.getElementById(id);
    el.addEventListener("input", calculate);
    el.addEventListener("change", calculate);
  });
  document.getElementById("pp-calc-btn").addEventListener("click", calculate);
  calculate();
})();
