/*
 * Калькулятор Win Rate × R:R — общая логика для всех локалей.
 * Математика идентична во всех копиях (toFixed, без локального форматирования):
 *   EV = (wr*rr - (1-wr)) * risk;  requiredRR = (1-wr)/wr.
 * Каждая локаль хранит свой render(d) — дословный HTML-шаблон результата.
 */
(function () {
  if (!document.getElementById("wr-result")) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      fillAll: "Заполни все поля",
      status: function (ev) {
        if (ev > 0.5) return { t: "✅ Сильная стратегия — стабильный плюс", c: "calc-ok" };
        if (ev > 0.1) return { t: "🟡 Стратегия в плюсе, но плюс слабый", c: "calc-warn" };
        if (ev > -0.1) return { t: "🟠 Стратегия на грани — близко к нулю", c: "calc-warn" };
        return { t: "🔴 Стратегия УБЫТОЧНА по математике", c: "calc-error" };
      },
      render: function (d) {
        return (
          '<table class="calc-table">' +
          "<tr><td><strong>Прибыльных сделок</strong></td><td>" + d.wins + " (" + d.wrPct + "%)</td></tr>" +
          "<tr><td><strong>Убыточных сделок</strong></td><td>" + d.losses + " (" + d.lossPct + "%)</td></tr>" +
          "<tr><td><strong>Прибыль с побед</strong></td><td>+" + d.winPnL + "% депозита</td></tr>" +
          "<tr><td><strong>Убыток с поражений</strong></td><td>-" + d.lossPnL + "% депозита</td></tr>" +
          "<tr><td><strong>Итог за " + d.trades + " сделок</strong></td><td><strong>" + d.netSign + d.netPnL + "% депозита</strong></td></tr>" +
          "<tr><td><strong>EV (на 1 сделку)</strong></td><td>" + d.evSign + d.ev + "% депозита</td></tr>" +
          "<tr><td><strong>Минимальный RR для безубытка</strong></td><td>" + d.requiredRR + "</td></tr>" +
          "</table>" +
          "<p><strong>Расшифровка:</strong></p><ul>" +
          "<li>EV (Expected Value) = математическое ожидание одной сделки</li>" +
          "<li>Если EV > 0 — стратегия в долгосроке прибыльна</li>" +
          "<li>Если EV < 0 — даже миллион сделок не спасут</li>" +
          "<li>При твоём WR <strong>" + d.wrPct + "%</strong> минимальный RR для нуля = <strong>" + d.requiredRR + "</strong>. Ты используешь RR=<strong>" + d.rr + "</strong>, что " + (d.above ? "✅ ВЫШЕ" : "❌ НИЖЕ") + " требуемого.</li>" +
          "</ul>"
        );
      },
    },
    en: {
      fillAll: "Fill in all fields",
      status: function (ev) {
        if (ev > 0.5) return { t: "✅ Strong strategy — consistently profitable", c: "calc-ok" };
        if (ev > 0.1) return { t: "🟡 Strategy is profitable, but marginally", c: "calc-warn" };
        if (ev > -0.1) return { t: "🟠 Strategy on the edge — close to breakeven", c: "calc-warn" };
        return { t: "🔴 Strategy is UNPROFITABLE by mathematics", c: "calc-error" };
      },
      render: function (d) {
        return (
          '<table class="calc-table">' +
          "<tr><td><strong>Winning trades</strong></td><td>" + d.wins + " (" + d.wrPct + "%)</td></tr>" +
          "<tr><td><strong>Losing trades</strong></td><td>" + d.losses + " (" + d.lossPct + "%)</td></tr>" +
          "<tr><td><strong>Profit from wins</strong></td><td>+" + d.winPnL + "% of deposit</td></tr>" +
          "<tr><td><strong>Loss from losses</strong></td><td>-" + d.lossPnL + "% of deposit</td></tr>" +
          "<tr><td><strong>Net result over " + d.trades + " trades</strong></td><td><strong>" + d.netSign + d.netPnL + "% of deposit</strong></td></tr>" +
          "<tr><td><strong>EV (per 1 trade)</strong></td><td>" + d.evSign + d.ev + "% of deposit</td></tr>" +
          "<tr><td><strong>Minimum RR for breakeven</strong></td><td>" + d.requiredRR + "</td></tr>" +
          "</table>" +
          "<p><strong>Explanation:</strong></p><ul>" +
          "<li>EV (Expected Value) = mathematical expectation of one trade</li>" +
          "<li>If EV > 0 — the strategy is profitable in the long run</li>" +
          "<li>If EV < 0 — even a million trades won't save you</li>" +
          "<li>At your WR of <strong>" + d.wrPct + "%</strong> the minimum RR for breakeven = <strong>" + d.requiredRR + "</strong>. You are using RR=<strong>" + d.rr + "</strong>, which is " + (d.above ? "✅ ABOVE" : "❌ BELOW") + " the required value.</li>" +
          "</ul>"
        );
      },
    },
    uz: {
      fillAll: "Barcha maydonlarni to'ldiring",
      status: function (ev) {
        if (ev > 0.5) return { t: "✅ Kuchli strategiya — barqaror plyus", c: "calc-ok" };
        if (ev > 0.1) return { t: "🟡 Strategiya plyusda, lekin plyus kuchsiz", c: "calc-warn" };
        if (ev > -0.1) return { t: "🟠 Strategiya chegarada — nolga yaqin", c: "calc-warn" };
        return { t: "🔴 Strategiya matematika bo'yicha ZARARLI", c: "calc-error" };
      },
      render: function (d) {
        return (
          '<table class="calc-table">' +
          "<tr><td><strong>Foydali savdolar</strong></td><td>" + d.wins + " (" + d.wrPct + "%)</td></tr>" +
          "<tr><td><strong>Zararli savdolar</strong></td><td>" + d.losses + " (" + d.lossPct + "%)</td></tr>" +
          "<tr><td><strong>G'alabalardan foyda</strong></td><td>+" + d.winPnL + "% depozit</td></tr>" +
          "<tr><td><strong>Mag'lubiyatlardan zarar</strong></td><td>-" + d.lossPnL + "% depozit</td></tr>" +
          "<tr><td><strong>" + d.trades + " savdo uchun jami</strong></td><td><strong>" + d.netSign + d.netPnL + "% depozit</strong></td></tr>" +
          "<tr><td><strong>EV (1 savdoga)</strong></td><td>" + d.evSign + d.ev + "% depozit</td></tr>" +
          "<tr><td><strong>Zarar ko'rmaslik uchun minimal RR</strong></td><td>" + d.requiredRR + "</td></tr>" +
          "</table>" +
          "<p><strong>Izoh:</strong></p><ul>" +
          "<li>EV (Expected Value) = bir savdoning matematik kutilmasi</li>" +
          "<li>Agar EV > 0 — strategiya uzoq muddatda foydali</li>" +
          "<li>Agar EV < 0 — million savdo ham yordam bermaydi</li>" +
          "<li>Sizning WR <strong>" + d.wrPct + "%</strong> bo'lganda nol uchun minimal RR = <strong>" + d.requiredRR + "</strong>. Siz RR=<strong>" + d.rr + "</strong> ishlatyapsiz, bu talab qilinganidan " + (d.above ? "✅ YUQORI" : "❌ PAST") + ".</li>" +
          "</ul>"
        );
      },
    },
  });

  function calc() {
    var wr = parseFloat(document.getElementById("wr-input").value) / 100;
    var rr = parseFloat(document.getElementById("rr-input").value);
    var trades = parseInt(document.getElementById("trades-input").value, 10);
    var risk = parseFloat(document.getElementById("risk-input").value);

    if (!wr || !rr || !trades || !risk) {
      document.getElementById("wr-result").innerHTML = '<div class="calc-warn">' + T.fillAll + "</div>";
      return;
    }

    var wins = Math.round(trades * wr);
    var losses = trades - wins;
    var winPnL = wins * rr * risk;
    var lossPnL = losses * risk;
    var netPnL = winPnL - lossPnL;
    var ev = (wr * rr - (1 - wr)) * risk;
    var requiredRR = (1 - wr) / wr;
    var st = T.status(ev);

    var d = {
      wins: wins,
      losses: losses,
      wrPct: (wr * 100).toFixed(0),
      lossPct: ((1 - wr) * 100).toFixed(0),
      winPnL: winPnL.toFixed(2),
      lossPnL: lossPnL.toFixed(2),
      netSign: netPnL >= 0 ? "+" : "",
      netPnL: netPnL.toFixed(2),
      evSign: ev >= 0 ? "+" : "",
      ev: ev.toFixed(3),
      requiredRR: requiredRR.toFixed(2),
      rr: rr.toFixed(1),
      trades: trades,
      above: rr > requiredRR,
    };

    document.getElementById("wr-result").innerHTML =
      '<div class="' + st.c + '"><h4>' + st.t + "</h4>" + T.render(d) + "</div>";
  }

  var btn = document.getElementById("wr-calc-btn");
  if (btn) btn.addEventListener("click", calc);
  calc();
})();
