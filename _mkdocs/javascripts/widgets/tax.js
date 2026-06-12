/*
 * Калькулятор налога (НДФЛ 12% для резидентов УЗ) — общая логика для локалей.
 * Математика идентична uz/tax-calculator.py:calculate_tax:
 *   net = profit - loss;  tax = net * 0.12 (только если net > 0);  after = net - tax.
 * Строки и суффикс национальной валюты локализованы через таблицу T.
 */
(function () {
  if (!document.getElementById("tax-widget")) return;
  var F = window.FXW;
  var NDFL_RATE = 0.12;

  var T = F.pick({
    ru: {
      uzs: " сум",
      errProfit: "Прибыль не может быть отрицательной.",
      errLoss: "Убыток укажи как положительное число.",
      errRate: "Укажи курс USD → UZS.",
      subheadLoss: "налога нет — убыток за год",
      subheadTax: "налог к уплате (НДФЛ 12%)",
      noteLoss: function (net) {
        return "✅ За год убыток (" + net + ") — НДФЛ платить не нужно. Сохрани отчёт брокера минимум 3 года на случай вопросов.";
      },
      noteDeclare: function (y) {
        return "📌 Задекларируй чистую прибыль до <strong>1 апреля " + y + "</strong> года в личном кабинете my.soliq.uz.";
      },
      noteAnnual: "💡 Декларируется итог за год (прибыли − убытки), а не каждая сделка отдельно.",
      noteVerify: "⚠️ Ставку и порядок уточни на soliq.uz — это образовательная оценка, не налоговая консультация.",
    },
    en: {
      uzs: " UZS",
      errProfit: "Profit cannot be negative.",
      errLoss: "Enter the loss as a positive number.",
      errRate: "Please enter the USD → UZS rate.",
      subheadLoss: "no tax — net loss for the year",
      subheadTax: "tax due (NDFL 12%)",
      noteLoss: function (net) {
        return "✅ Net loss for the year (" + net + ") — no NDFL is due. Keep your broker statement for at least 3 years in case of an audit.";
      },
      noteDeclare: function (y) {
        return "📌 Declare your net profit by <strong>April 1, " + y + "</strong> in your my.soliq.uz personal account.";
      },
      noteAnnual: "💡 You declare the annual net result (profits − losses), not each trade individually.",
      noteVerify: "⚠️ Verify the rate and procedure at soliq.uz — this is an educational estimate, not tax advice.",
    },
    uz: {
      uzs: " so'm",
      errProfit: "Foyda manfiy bo'lishi mumkin emas.",
      errLoss: "Zararni musbat son sifatida kiriting.",
      errRate: "USD → UZS kursini kiriting.",
      subheadLoss: "soliq yo'q — yil davomida zarar",
      subheadTax: "to'lanadigan soliq (JShDS 12%)",
      noteLoss: function (net) {
        return "✅ Yil davomida zarar (" + net + ") — JShDS to'lash shart emas. Broker hisobotini kamida 3 yil saqlang.";
      },
      noteDeclare: function (y) {
        return "📌 Sof foydani <strong>" + y + "-yil 1-aprelgacha</strong> my.soliq.uz shaxsiy kabinetida deklaratsiya qiling.";
      },
      noteAnnual: "💡 Har bir bitim emas, balki yillik natija (foydalar − zararlar) deklaratsiya qilinadi.",
      noteVerify: "⚠️ Stavka va tartibni soliq.uz da tekshiring — bu o'quv bahosi, soliq maslahati emas.",
    },
  });

  function fmtUZS(v) {
    return F.int(Math.round(v)) + T.uzs;
  }

  function calcTax(profit, loss, rate) {
    var net = profit - loss;
    if (net <= 0) {
      return { net: net, netUzs: net * rate, tax: 0, taxUzs: 0, after: net, afterUzs: net * rate, isLoss: true };
    }
    var tax = net * NDFL_RATE;
    return { net: net, netUzs: net * rate, tax: tax, taxUzs: tax * rate, after: net - tax, afterUzs: (net - tax) * rate, isLoss: false };
  }

  function recalc() {
    var profit = parseFloat(document.getElementById("tax-profit").value);
    var loss = parseFloat(document.getElementById("tax-loss").value);
    var rate = parseFloat(document.getElementById("tax-rate").value);

    var result = document.getElementById("tax-result");
    var warnings = document.getElementById("tax-warnings");
    warnings.innerHTML = "";

    var errors = [];
    if (!(profit >= 0)) errors.push(T.errProfit);
    if (!(loss >= 0)) errors.push(T.errLoss);
    if (!(rate > 0)) errors.push(T.errRate);
    if (errors.length) {
      result.style.display = "block";
      result.className = "";
      document.getElementById("tax-headline").textContent = "—";
      warnings.innerHTML = errors
        .map(function (e) {
          return '<div class="tax-note tax-danger">⛔ ' + e + "</div>";
        })
        .join("");
      return;
    }

    var r = calcTax(profit, loss, rate);

    document.getElementById("tax-out-net").textContent = F.money(r.net);
    document.getElementById("tax-out-net-uzs").textContent = fmtUZS(r.netUzs);
    document.getElementById("tax-out-tax").textContent = F.money(r.tax);
    document.getElementById("tax-out-tax-uzs").textContent = fmtUZS(r.taxUzs);
    document.getElementById("tax-out-after").textContent = F.money(r.after);
    document.getElementById("tax-out-after-uzs").textContent = fmtUZS(r.afterUzs);
    document.getElementById("tax-headline").textContent = F.money(r.tax);
    result.style.display = "block";
    result.className = r.isLoss ? "ok" : "";

    var nextYear = new Date().getFullYear() + 1;
    if (r.isLoss) {
      document.getElementById("tax-subhead").textContent = T.subheadLoss;
      warnings.innerHTML += '<div class="tax-note tax-ok">' + T.noteLoss(F.money(r.net)) + "</div>";
    } else {
      document.getElementById("tax-subhead").textContent = T.subheadTax;
      warnings.innerHTML += '<div class="tax-note">' + T.noteDeclare(nextYear) + "</div>";
      warnings.innerHTML += '<div class="tax-note">' + T.noteAnnual + "</div>";
    }
    warnings.innerHTML += '<div class="tax-note">' + T.noteVerify + "</div>";
  }

  ["tax-profit", "tax-loss", "tax-rate"].forEach(function (id) {
    var el = document.getElementById(id);
    el.addEventListener("input", recalc);
    el.addEventListener("change", recalc);
  });
  document.getElementById("tax-calc-btn").addEventListener("click", recalc);

  recalc();
})();
