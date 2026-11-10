/*
 * Калькулятор восстановления после просадки — общая логика для всех локалей.
 *
 * Зачем: убыток и прибыль в процентах несимметричны — после −50% нужно +100%,
 * а не +50%. Это самая недооценённая математика новичка и главный аргумент
 * против «отыгрывания»: чем глубже яма, тем недостижимее восстановление.
 *
 * Формула: gain = d / (100 − d) * 100, где d — просадка в процентах (0–95).
 * Чистая функция выставлена как window.__fxDrawdownRecovery — быстрая сверка
 * с эталоном идёт в tests/test_drawdown_widget.py через tests/widget_sandbox.mjs.
 */
(function () {
  var WARN_FROM = 30; // с этой просадки показываем предупреждение об анти-отыгрыше

  // Чистая математика: сколько % прибыли нужно, чтобы вернуться к исходному
  // депозиту после просадки d%. d=50 → 100, d=10 → 11.111…, d=20 → 25.
  function requiredGain(d) {
    return (d / (100 - d)) * 100;
  }
  window.__fxDrawdownRecovery = requiredGain;

  if (!document.getElementById("dd-result")) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      fillAll: "Укажи просадку от 0 до 95 %",
      status: function (d) {
        if (d >= WARN_FROM)
          return { t: "🔴 Глубокая яма — быстрого восстановления не будет", c: "calc-error" };
        if (d >= 10)
          return { t: "🟠 Заметная просадка — прибыль должна быть больше убытка", c: "calc-warn" };
        return { t: "🟢 Небольшая просадка — восстановление реально", c: "calc-ok" };
      },
      render: function (d) {
        return (
          '<table class="calc-table">' +
          "<tr><td><strong>Текущая просадка</strong></td><td>-" + d.drawdown + "% от пика депозита</td></tr>" +
          "<tr><td><strong>Осталось от депозита</strong></td><td>" + d.left + "%</td></tr>" +
          "<tr><td><strong>Нужно заработать до возврата в ноль</strong></td><td><strong>+" + d.gain + "%</strong></td></tr>" +
          "<tr><td><strong>Это больше самой просадки в</strong></td><td>" + d.ratio + " раз</td></tr>" +
          "</table>" +
          (d.warn
            ? '<p><strong>⚠️ Чем глубже яма, тем недостижимее восстановление.</strong> При −50% нужно +100% — это подвиг, а не план. Не отыгрывайся: остановись, снизь риск и вернись к правилам риск-менеджмента.</p>'
            : "")
        );
      },
    },
    en: {
      fillAll: "Enter a drawdown between 0 and 95%",
      status: function (d) {
        if (d >= WARN_FROM)
          return { t: "🔴 Deep hole — recovery won't be quick", c: "calc-error" };
        if (d >= 10)
          return { t: "🟠 Notable drawdown — the required gain exceeds the loss", c: "calc-warn" };
        return { t: "🟢 Small drawdown — recovery is realistic", c: "calc-ok" };
      },
      render: function (d) {
        return (
          '<table class="calc-table">' +
          "<tr><td><strong>Current drawdown</strong></td><td>-" + d.drawdown + "% from account peak</td></tr>" +
          "<tr><td><strong>Account remaining</strong></td><td>" + d.left + "%</td></tr>" +
          "<tr><td><strong>Gain needed to get back to breakeven</strong></td><td><strong>+" + d.gain + "%</strong></td></tr>" +
          "<tr><td><strong>That is larger than the drawdown itself by</strong></td><td>" + d.ratio + " times</td></tr>" +
          "</table>" +
          (d.warn
            ? '<p><strong>⚠️ The deeper the hole, the more unreachable recovery becomes.</strong> At −50% you need +100% — a feat, not a plan. Don\'t chase losses: stop, cut your risk, and return to your risk-management rules.</p>'
            : "")
        );
      },
    },
    uz: {
      fillAll: "0% dan 95% gacha tushishni kiriting",
      status: function (d) {
        if (d >= WARN_FROM)
          return { t: "🔴 Chuqur chuqurlik — tiklanish tez bo'lmaydi", c: "calc-error" };
        if (d >= 10)
          return { t: "🟠 Sezilarli tushish — kerakli foyda zarardan katta", c: "calc-warn" };
        return { t: "🟢 Kichik tushish — tiklanish real", c: "calc-ok" };
      },
      render: function (d) {
        return (
          '<table class="calc-table">' +
          "<tr><td><strong>Joriy tushish</strong></td><td>-" + d.drawdown + "% depozit cho'qqisidan</td></tr>" +
          "<tr><td><strong>Depozitdan qoldi</strong></td><td>" + d.left + "%</td></tr>" +
          "<tr><td><strong>Nolga qaytish uchun kerak foyda</strong></td><td><strong>+" + d.gain + "%</strong></td></tr>" +
          "<tr><td><strong>Bu tushishning o'zidan katta</strong></td><td>" + d.ratio + " baravar</td></tr>" +
          "</table>" +
          (d.warn
            ? '<p><strong>⚠️ Chuqurlik qancha chuqur bo\'lsa, tiklanish shuncha erishib bo\'lmas bo\'ladi.</strong> −50% da +100% kerak — bu jasorat, reja emas. Zararni qoplashga shoshilmang: to\'xtang, riskni kamaytiring va risk-menejment qoidalariga qayting.</p>'
            : "")
        );
      },
    },
  });

  function calc() {
    var d = parseFloat(document.getElementById("dd-input").value);

    if (isNaN(d) || d < 0 || d > 95) {
      document.getElementById("dd-result").innerHTML =
        '<div class="calc-warn">' + T.fillAll + "</div>";
      return;
    }

    var gain = requiredGain(d);
    var st = T.status(d);

    var data = {
      drawdown: d.toFixed(1),
      left: (100 - d).toFixed(1),
      gain: gain.toFixed(1),
      // при d=0 отношение не имеет смысла — показываем прочерк
      ratio: d > 0 ? (gain / d).toFixed(2) : "—",
      warn: d >= WARN_FROM,
    };

    document.getElementById("dd-result").innerHTML =
      '<div class="' + st.c + '"><h4>' + st.t + "</h4>" + T.render(data) + "</div>";
  }

  var btn = document.getElementById("dd-calc-btn");
  if (btn) btn.addEventListener("click", calc);
  calc();
})();
