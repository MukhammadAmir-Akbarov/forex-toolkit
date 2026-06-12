/*
 * Калькулятор сложного процента — общая логика для всех локалей.
 * Математика идентична tools/compound_calculator.py (project_growth):
 *   balance = balance * (1 + r) + monthlyDeposit, помесячно.
 * Строки локализованы через таблицу T; id-шники и математика — единые.
 *
 * Примечание: в исходных RU/UZ копиях «не реалистично» было обёрнуто в
 * markdown `**...**`, который внутри innerHTML не рендерится. Здесь во всех
 * локалях используется <strong> (как уже было в EN).
 */
(function () {
  if (!document.getElementById("cc-calc-btn")) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      errInitial: "Стартовый капитал должен быть больше 0.",
      errRoi: "Доходность — число.",
      errMonths: "Срок должен быть больше 0 месяцев.",
      months: function (m, y) {
        return m + " мес. (" + y + " лет)";
      },
      row: function (m) {
        return m + " мес";
      },
      scam: function (roi, annual) {
        return "⛔ " + roi + " в месяц = " + annual + " в год. Это <strong>не реалистично</strong>. Если кто-то это обещает — это скам.";
      },
      optimistic: function (roi) {
        return "⚠️ " + roi + "/мес — очень оптимистично. Лучшие хедж-фонды делают 20-30% в год = ~2%/мес. Проверь обещания.";
      },
      negative: function (months, loss) {
        return "📉 Отрицательная доходность — сценарий просадки. Через " + months + " мес. потеряешь " + loss + " от стартового.";
      },
      realistic: function (roi) {
        return "ℹ️ " + roi + "/мес — реалистичный диапазон для опытных трейдеров. Большинство довольны 1-3%.";
      },
    },
    en: {
      errInitial: "Starting capital must be > 0.",
      errRoi: "Return must be a number.",
      errMonths: "Period must be > 0 months.",
      months: function (m, y) {
        return m + " months (" + y + " years)";
      },
      row: function (m) {
        return "Month " + m;
      },
      scam: function (roi, annual) {
        return "⛔ " + roi + " per month = " + annual + " per year. This is <strong>not realistic</strong>. If someone promises this, it's a scam.";
      },
      optimistic: function (roi) {
        return "⚠️ " + roi + "/month is very optimistic. The best hedge funds do 20-30%/year ≈ 2%/month. Verify any promises.";
      },
      negative: function (months, loss) {
        return "📉 Negative return — drawdown scenario. After " + months + " months you'd lose " + loss + " from the starting capital.";
      },
      realistic: function (roi) {
        return "ℹ️ " + roi + "/month is a realistic range for experienced traders. Most are content with 1-3%.";
      },
    },
    uz: {
      errInitial: "Boshlang'ich kapital 0 dan katta bo'lishi kerak.",
      errRoi: "Daromadlilik — son bo'lishi kerak.",
      errMonths: "Muddat 0 dan katta bo'lishi kerak.",
      months: function (m, y) {
        return m + " oy (" + y + " yil)";
      },
      row: function (m) {
        return m + " oy";
      },
      scam: function (roi, annual) {
        return "⛔ Oyiga " + roi + " = yiliga " + annual + ". Bu <strong>real emas</strong>. Agar kimdir buni va'da qilsa — bu firibgarlik.";
      },
      optimistic: function (roi) {
        return "⚠️ " + roi + "/oy — juda optimistik. Eng yaxshi xedj-fondlar yiliga 20-30% = ~2%/oy qiladi. Va'dalarni tekshiring.";
      },
      negative: function (months, loss) {
        return "📉 Salbiy daromadlilik — drawdown stsenariyi. " + months + " oydan so'ng boshlang'ichdan " + loss + " yo'qotasiz.";
      },
      realistic: function (roi) {
        return "ℹ️ " + roi + "/oy — tajribali treyderlar uchun realistik diapazon. Ko'pchilik 1-3% dan mamnun.";
      },
    },
  });

  function calc() {
    var initial = parseFloat(document.getElementById("cc-initial").value);
    var roiPct = parseFloat(document.getElementById("cc-roi").value);
    var months = parseInt(document.getElementById("cc-months").value, 10);
    var monthlyDeposit = parseFloat(document.getElementById("cc-deposit").value) || 0;
    var result = document.getElementById("cc-result");
    var warnings = document.getElementById("cc-warnings");
    warnings.innerHTML = "";

    var errors = [];
    if (!(initial > 0)) errors.push(T.errInitial);
    if (isNaN(roiPct)) errors.push(T.errRoi);
    if (!(months > 0)) errors.push(T.errMonths);
    if (errors.length) {
      result.style.display = "block";
      result.className = "pc-result danger";
      document.getElementById("cc-headline").textContent = "—";
      warnings.innerHTML = errors
        .map(function (e) {
          return '<div class="pc-warn pc-danger">⛔ ' + e + "</div>";
        })
        .join("");
      return;
    }

    var r = roiPct / 100;
    var balance = initial;
    var totalDeposited = initial;
    var series = [{ month: 0, balance: balance, gain: 0, profit: 0 }];

    for (var m = 1; m <= months; m++) {
      var gain = balance * r;
      balance = balance * (1 + r) + monthlyDeposit;
      if (m > 1) totalDeposited += monthlyDeposit;
      series.push({ month: m, balance: balance, gain: gain, profit: balance - totalDeposited });
    }

    var finalBalance = series[series.length - 1].balance;
    var profit = finalBalance - totalDeposited;
    var annualEquivalent = (Math.pow(1 + r, 12) - 1) * 100;
    var totalRoi = ((finalBalance - initial) / initial) * 100;

    document.getElementById("cc-out-initial").textContent = F.money(initial);
    document.getElementById("cc-out-roi").textContent = F.pct(roiPct);
    document.getElementById("cc-out-months").textContent = T.months(months, (months / 12).toFixed(1));
    document.getElementById("cc-out-deposited").textContent = F.money(totalDeposited);
    document.getElementById("cc-out-profit").textContent = F.money(profit);
    document.getElementById("cc-out-final").textContent = F.money(finalBalance);
    document.getElementById("cc-out-annual").textContent = F.pct(annualEquivalent);
    document.getElementById("cc-out-roi-total").textContent = F.pct(totalRoi);
    document.getElementById("cc-headline").textContent = F.money(finalBalance);
    result.style.display = "block";
    result.className = "pc-result";

    var checkpoints = [1, 3, 6, 12, 24, 60, 120].filter(function (m) {
      return m <= months;
    });
    if (checkpoints.indexOf(months) === -1) checkpoints.push(months);
    document.getElementById("cc-tbody").innerHTML = checkpoints
      .map(function (m) {
        var s = series[m];
        return "<tr><td>" + T.row(m) + "</td><td>" + F.money(s.balance) + "</td><td>" + F.money(s.gain) + "</td><td>" + F.money(s.profit) + "</td></tr>";
      })
      .join("");

    if (roiPct > 10) {
      warnings.innerHTML += '<div class="pc-warn pc-danger">' + T.scam(F.pct(roiPct), F.pct(annualEquivalent)) + "</div>";
    } else if (roiPct > 5) {
      warnings.innerHTML += '<div class="pc-warn">' + T.optimistic(F.pct(roiPct)) + "</div>";
    } else if (roiPct < 0) {
      warnings.innerHTML += '<div class="pc-warn">' + T.negative(months, F.money(initial - finalBalance)) + "</div>";
    }
    if (roiPct >= 1 && roiPct <= 5) {
      warnings.innerHTML += '<div class="pc-warn pc-info">' + T.realistic(F.pct(roiPct)) + "</div>";
    }
  }

  ["cc-initial", "cc-roi", "cc-months", "cc-deposit"].forEach(function (id) {
    document.getElementById(id).addEventListener("input", calc);
  });
  document.getElementById("cc-calc-btn").addEventListener("click", calc);
  calc();
})();
