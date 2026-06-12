/*
 * Калькулятор маржи — общая логика для всех локалей.
 * Формула идентична tools/margin_calculator.py:
 *   margin = (lots * contract_size * price) / leverage
 * Пороги: warn > 20% депозита, danger > 50% депозита.
 * Строки локализованы через таблицу T; математика и id-шники — единые.
 */
(function () {
  if (!document.getElementById("mc-widget")) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      lot: " лот",
      errDeposit: "Депозит должен быть больше 0.",
      errLots: "Лотов должно быть больше 0.",
      errPrice: "Цена должна быть больше 0.",
      errLeverage: "Плечо должно быть больше 0.",
      dangerHigh: function (p) {
        return "⛔ Маржа " + p + " депозита — очень мало свободной маржи. Один сильный ход против тебя — и будет Margin Call.";
      },
      warnHigh: function (p) {
        return "⚠️ Маржа " + p + " депозита — высокая нагрузка на счёт. Мало пространства для просадки.";
      },
      negFree: function (m) {
        return "⛔ Свободная маржа отрицательная (" + m + ") — брокер не даст открыть такую позицию.";
      },
      ok: function (p) {
        return "✅ Нагрузка на счёт в норме (" + p + "). Есть пространство для просадки.";
      },
    },
    en: {
      lot: " lot",
      errDeposit: "Balance must be greater than 0.",
      errLots: "Lot size must be greater than 0.",
      errPrice: "Price must be greater than 0.",
      errLeverage: "Leverage must be greater than 0.",
      dangerHigh: function (p) {
        return "⛔ Margin usage is " + p + " of your balance — very little free margin left. One adverse move and you face a Margin Call.";
      },
      warnHigh: function (p) {
        return "⚠️ Margin usage is " + p + " — high load on your account. Little room for drawdown.";
      },
      negFree: function (m) {
        return "⛔ Free margin is negative (" + m + ") — the broker will not allow opening this position.";
      },
      ok: function (p) {
        return "✅ Margin load is healthy (" + p + "). Plenty of room for drawdown.";
      },
    },
    uz: {
      lot: " lot",
      errDeposit: "Balans 0 dan katta bo'lishi kerak.",
      errLots: "Lotlar 0 dan katta bo'lishi kerak.",
      errPrice: "Narx 0 dan katta bo'lishi kerak.",
      errLeverage: "Richak 0 dan katta bo'lishi kerak.",
      dangerHigh: function (p) {
        return "⛔ Marja foydalanishi " + p + " — erkin marja juda kam qoldi. Bitta kuchli harakat va Margin Call bo'lishi mumkin.";
      },
      warnHigh: function (p) {
        return "⚠️ Marja foydalanishi " + p + " — hisob yuqori yuklanganiga ehtiyot bo'ling. Pasayish uchun kam joy qoldi.";
      },
      negFree: function (m) {
        return "⛔ Erkin marja manfiy (" + m + ") — broker bu pozitsiyani ochishga ruxsat bermaydi.";
      },
      ok: function (p) {
        return "✅ Marja yuklamasi normal (" + p + "). Pasayish uchun yetarli joy bor.";
      },
    },
  });

  var CONTRACT_SIZES = { standard: 100000, mini: 10000, micro: 1000 };

  function calcMargin(lots, price, leverage, contractSize) {
    // margin_required из tools/margin_calculator.py
    return (lots * contractSize * price) / leverage;
  }

  function recalc() {
    var deposit = parseFloat(document.getElementById("mc-deposit").value);
    var lots = parseFloat(document.getElementById("mc-lots").value);
    var price = parseFloat(document.getElementById("mc-price").value);
    var leverage = parseInt(document.getElementById("mc-leverage").value, 10);
    var lotType = document.getElementById("mc-type").value;
    var contractSize = CONTRACT_SIZES[lotType];

    var result = document.getElementById("mc-result");
    var warnings = document.getElementById("mc-warnings");
    warnings.innerHTML = "";

    var errors = [];
    if (!(deposit > 0)) errors.push(T.errDeposit);
    if (!(lots > 0)) errors.push(T.errLots);
    if (!(price > 0)) errors.push(T.errPrice);
    if (!(leverage > 0)) errors.push(T.errLeverage);
    if (errors.length) {
      result.style.display = "block";
      result.className = "danger";
      document.getElementById("mc-headline").textContent = "—";
      warnings.innerHTML = errors
        .map(function (e) {
          return '<div class="mc-warn mc-danger">⛔ ' + e + "</div>";
        })
        .join("");
      return;
    }

    var margin = calcMargin(lots, price, leverage, contractSize);
    var freeMargin = deposit - margin;
    var usagePct = (margin / deposit) * 100;

    document.getElementById("mc-out-deposit").textContent = F.money(deposit);
    document.getElementById("mc-out-lots").textContent = lots.toFixed(2) + T.lot;
    document.getElementById("mc-out-price").textContent = price.toFixed(5);
    document.getElementById("mc-out-leverage").textContent = "1:" + leverage;
    document.getElementById("mc-out-contract").textContent = F.int(contractSize);
    document.getElementById("mc-out-margin").textContent = F.money(margin);
    document.getElementById("mc-out-free").textContent = F.money(freeMargin);
    document.getElementById("mc-out-pct").textContent = F.pct(usagePct);
    document.getElementById("mc-headline").textContent = F.money(margin);
    result.style.display = "block";

    var cls = "";
    if (usagePct > 50) {
      cls = "danger";
      warnings.innerHTML += '<div class="mc-warn mc-danger">' + T.dangerHigh(F.pct(usagePct)) + "</div>";
    } else if (usagePct > 20) {
      cls = "warn";
      warnings.innerHTML += '<div class="mc-warn">' + T.warnHigh(F.pct(usagePct)) + "</div>";
    }
    if (freeMargin < 0) {
      cls = "danger";
      warnings.innerHTML += '<div class="mc-warn mc-danger">' + T.negFree(F.money(freeMargin)) + "</div>";
    }
    if (cls === "") {
      warnings.innerHTML += '<div class="mc-warn" style="background:rgba(34,197,94,0.08);border-left-color:#22c55e;">' + T.ok(F.pct(usagePct)) + "</div>";
    }
    result.className = cls;
  }

  ["mc-deposit", "mc-lots", "mc-price", "mc-leverage", "mc-pair", "mc-type"].forEach(function (id) {
    var el = document.getElementById(id);
    el.addEventListener("input", recalc);
    el.addEventListener("change", recalc);
  });
  document.getElementById("mc-calc-btn").addEventListener("click", recalc);

  recalc();
})();
