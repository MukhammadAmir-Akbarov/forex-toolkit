/*
 * Калькулятор полной стоимости торговли — общая логика для всех локалей.
 * Издержки за сделку: спред + комиссия (круг) + своп; безубыток в пунктах;
 * экстраполяция на месяц/год и % от депозита («цена овертрейдинга»).
 *
 *   spreadCost = spread * pipValue * lots
 *   commission = commPerLotSide * lots * 2
 *   swapCost   = -swapPerLotNight * lots * nights   (отриц. своп = ты платишь)
 *   total      = spreadCost + commission + swapCost
 *   breakeven  = total / (pipValue * lots)
 * pipValue — статичная стоимость пункта на 1 лот (как в position.js).
 */
(function () {
  if (!document.getElementById("co-widget")) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      pips: " пунктов",
      perTrade: " / сделка",
      errDeposit: "Депозит должен быть больше 0.",
      errLots: "Лотов должно быть больше 0.",
      errTrades: "Сделок в месяц должно быть больше 0.",
      swapEarn: function (m) {
        return "ℹ️ Своп положительный — за перенос тебе доплачивают (" + m + " за сделку). Это снижает издержки.";
      },
      beHigh: function (p) {
        return "⚠️ Безубыток " + p + " — издержки на сделку высокие. На коротких тейках они съедают значимую часть прибыли.";
      },
      overDanger: function (p) {
        return "⛔ За год издержки = " + p + " депозита. Это очень много — типичный овертрейдинг. Торгуй реже и крупнее по тейку.";
      },
      overWarn: function (p) {
        return "⚠️ За год издержки = " + p + " депозита. Заметная доля — присмотрись к частоте сделок и спредам.";
      },
      ok: function (p) {
        return "✅ За год издержки = " + p + " депозита — в разумных пределах. Держи частоту под контролем.";
      },
    },
    en: {
      pips: " pips",
      perTrade: " / trade",
      errDeposit: "Balance must be greater than 0.",
      errLots: "Lot size must be greater than 0.",
      errTrades: "Trades per month must be greater than 0.",
      swapEarn: function (m) {
        return "ℹ️ Positive swap — you get paid to hold overnight (" + m + " per trade). This lowers your costs.";
      },
      beHigh: function (p) {
        return "⚠️ Break-even is " + p + " — cost per trade is high. On short take-profits it eats a big chunk of your edge.";
      },
      overDanger: function (p) {
        return "⛔ Yearly costs = " + p + " of your balance. That's very high — classic overtrading. Trade less often, with bigger take-profits.";
      },
      overWarn: function (p) {
        return "⚠️ Yearly costs = " + p + " of your balance. A noticeable share — review your trade frequency and spreads.";
      },
      ok: function (p) {
        return "✅ Yearly costs = " + p + " of your balance — within reason. Keep your frequency in check.";
      },
    },
    uz: {
      pips: " punkt",
      perTrade: " / savdo",
      errDeposit: "Balans 0 dan katta bo'lishi kerak.",
      errLots: "Lotlar 0 dan katta bo'lishi kerak.",
      errTrades: "Oyiga savdolar soni 0 dan katta bo'lishi kerak.",
      swapEarn: function (m) {
        return "ℹ️ Svop musbat — tunga olib o'tganingiz uchun sizga to'lashadi (savdoga " + m + "). Bu xarajatni kamaytiradi.";
      },
      beHigh: function (p) {
        return "⚠️ Zarar ko'rmaslik nuqtasi " + p + " — savdo xarajati yuqori. Qisqa teyklarda u foydaning katta qismini yeydi.";
      },
      overDanger: function (p) {
        return "⛔ Yillik xarajat = depozitning " + p + " qismi. Bu juda ko'p — klassik overtrading. Kamroq va kattaroq teyk bilan savdo qiling.";
      },
      overWarn: function (p) {
        return "⚠️ Yillik xarajat = depozitning " + p + " qismi. Sezilarli ulush — savdo chastotasi va spredlarni ko'rib chiqing.";
      },
      ok: function (p) {
        return "✅ Yillik xarajat = depozitning " + p + " qismi — me'yorida. Chastotani nazoratda tuting.";
      },
    },
  });

  // Стоимость пункта в USD на 1 стандартный лот (как в position.js).
  var PIP_VALUE_PER_LOT = {
    EURUSD: 10.0, GBPUSD: 10.0, AUDUSD: 10.0, NZDUSD: 10.0,
    USDJPY: 6.7, USDCHF: 11.3, USDCAD: 7.3,
    EURJPY: 6.7, GBPJPY: 6.7, EURGBP: 12.7,
  };

  function recalc() {
    var deposit = parseFloat(document.getElementById("co-deposit").value);
    var pair = document.getElementById("co-pair").value;
    var lots = parseFloat(document.getElementById("co-lots").value);
    var spread = parseFloat(document.getElementById("co-spread").value);
    var commission = parseFloat(document.getElementById("co-commission").value);
    var trades = parseInt(document.getElementById("co-trades").value, 10);
    var nights = parseInt(document.getElementById("co-nights").value, 10) || 0;
    var swap = parseFloat(document.getElementById("co-swap").value);

    var result = document.getElementById("co-result");
    var warnings = document.getElementById("co-warnings");
    warnings.innerHTML = "";

    var errors = [];
    if (!(deposit > 0)) errors.push(T.errDeposit);
    if (!(lots > 0)) errors.push(T.errLots);
    if (!(trades > 0)) errors.push(T.errTrades);
    if (!(spread >= 0)) spread = 0;
    if (!(commission >= 0)) commission = 0;
    if (isNaN(swap)) swap = 0;
    if (errors.length) {
      result.style.display = "block";
      result.className = "danger";
      document.getElementById("co-headline").textContent = "—";
      warnings.innerHTML = errors
        .map(function (e) {
          return '<div class="pc-warn pc-danger">⛔ ' + e + "</div>";
        })
        .join("");
      return;
    }

    var pipValue = PIP_VALUE_PER_LOT[pair] * lots;
    var spreadCost = spread * pipValue;
    var commissionCost = commission * lots * 2;
    var swapCost = -swap * lots * nights;
    var total = spreadCost + commissionCost + swapCost;
    var breakEven = pipValue > 0 ? total / pipValue : 0;
    var monthly = total * trades;
    var monthlyPct = (monthly / deposit) * 100;
    var yearly = monthly * 12;
    var yearlyPct = (yearly / deposit) * 100;

    document.getElementById("co-out-spread").textContent = F.money(spreadCost);
    document.getElementById("co-out-commission").textContent = F.money(commissionCost);
    document.getElementById("co-out-swap").textContent = F.money(swapCost);
    document.getElementById("co-out-total").textContent = F.money(total);
    document.getElementById("co-out-breakeven").textContent = breakEven.toFixed(1) + T.pips;
    document.getElementById("co-out-monthly").textContent = F.money(monthly);
    document.getElementById("co-out-monthly-pct").textContent = F.pct(monthlyPct);
    document.getElementById("co-out-yearly").textContent = F.money(yearly) + " (" + F.pct(yearlyPct) + ")";
    document.getElementById("co-headline").textContent = F.money(total) + T.perTrade;
    result.style.display = "block";

    var cls = "";
    if (yearlyPct > 30) {
      cls = "danger";
      warnings.innerHTML += '<div class="pc-warn pc-danger">' + T.overDanger(F.pct(yearlyPct)) + "</div>";
    } else if (yearlyPct > 15) {
      cls = "warn";
      warnings.innerHTML += '<div class="pc-warn">' + T.overWarn(F.pct(yearlyPct)) + "</div>";
    } else {
      warnings.innerHTML += '<div class="pc-warn pc-info">' + T.ok(F.pct(yearlyPct)) + "</div>";
    }
    if (breakEven > 5) {
      cls = cls === "danger" ? cls : "warn";
      warnings.innerHTML += '<div class="pc-warn">' + T.beHigh(breakEven.toFixed(1) + T.pips) + "</div>";
    }
    if (swapCost < 0) {
      warnings.innerHTML += '<div class="pc-warn pc-info">' + T.swapEarn(F.money(-swapCost)) + "</div>";
    }
    result.className = cls;
  }

  ["co-deposit", "co-pair", "co-lots", "co-spread", "co-commission", "co-trades", "co-nights", "co-swap"].forEach(function (id) {
    var el = document.getElementById(id);
    el.addEventListener("input", recalc);
    el.addEventListener("change", recalc);
  });
  document.getElementById("co-calc-btn").addEventListener("click", recalc);

  recalc();
})();
