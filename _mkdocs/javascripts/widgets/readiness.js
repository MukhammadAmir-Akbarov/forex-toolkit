/*
 * «Готов ли я к реалу?» — вердикт по демо-статистике, общая логика для локалей.
 *
 * Зачем: тест готовности (risk-profile) проверяет психологию и подушку, но не
 * результаты. Здесь пользователь вводит свою демо-статистику и получает
 * честный ответ по чек-листу journal/demo-vs-real-comparison.md: что выполнено,
 * а что подтянуть. Ни одного «почти готов» — либо все пункты, либо рано.
 *
 * Profit Factor и матожидание считаются из winrate и среднего RR:
 *   PF = w·RR / (1 − w),  E = w·RR − (1 − w)  (в R на сделку).
 * Чистая функция — window.__fxReadiness; сверка в tests/test_readiness_widget.py.
 */
(function () {
  // Пороги — из чек-листа «переход на реал» и раздела 6 гайда.
  var LIMITS = { months: 3, trades: 50, winrate: 40, pf: 1.5, maxDD: 20, violations: 5 };

  // s: { months, trades, winrate (%), rr, maxDD (%), violations (% сделок), journal, canLose }
  function verdict(s) {
    var w = s.winrate / 100;
    var pf = w >= 1 ? Infinity : (w * s.rr) / (1 - w);
    var checks = [
      { id: "months", ok: s.months >= LIMITS.months },
      { id: "trades", ok: s.trades >= LIMITS.trades },
      { id: "winrate", ok: s.winrate >= LIMITS.winrate },
      { id: "pf", ok: pf >= LIMITS.pf },
      { id: "maxDD", ok: s.maxDD <= LIMITS.maxDD },
      { id: "violations", ok: s.violations < LIMITS.violations },
      { id: "journal", ok: !!s.journal },
      { id: "canLose", ok: !!s.canLose },
    ];
    return {
      ready: checks.every(function (c) { return c.ok; }),
      pf: pf,
      expectancy: w * s.rr - (1 - w),
      checks: checks,
    };
  }
  window.__fxReadiness = verdict;

  if (!document.getElementById("rd-result")) return;
  var F = window.FXW;
  var L = LIMITS;

  var T = F.pick({
    ru: {
      bad: "Заполни все числа: winrate 0–100 %, RR больше 0, просадка и нарушения 0–100 %.",
      ready: "🟢 Готов к маленькому реалу",
      readyNote: "Все пункты выполнены. Начни с $100–300 и риска 0.5% на сделку, а первые недели сравнивай реал с демо — психология на живых деньгах другая.",
      early: "🔴 Рано. Подтяни пункты ниже",
      earlyNote: "Демо — бесплатная учёба. Каждый невыполненный пункт на реале стоит денег.",
      metrics: function (pf, e) { return "Profit Factor: <strong>" + pf + "</strong> · матожидание: <strong>" + e + " R</strong> на сделку"; },
      items: {
        months: ["≥ " + L.months + " мес. на демо", "Торгуй на демо ещё — месяц удачи не отличить от системы."],
        trades: ["≥ " + L.trades + " сделок", "Мало сделок: статистика пока шум, а не результат."],
        winrate: ["Winrate ≥ " + L.winrate + "%", "Найди, где теряешь: вход раньше сигнала, слишком близкий стоп?"],
        pf: ["Profit Factor ≥ " + L.pf, "Прибыль едва перекрывает убытки — на реале спред и проскальзывание это съедят."],
        maxDD: ["Макс. просадка ≤ " + L.maxDD + "%", "Снизь риск на сделку: такая яма на реале ломает психику."],
        violations: ["Нарушения правил < " + L.violations + "% сделок", "Сначала дисциплина: правило, которое нарушают, — не правило."],
        journal: ["Журнал по каждой сделке", "Без журнала не видно, что чинить."],
        canLose: ["Сумму не жалко потерять полностью", "Не начинай реал на деньги, от которых зависит жизнь."],
      },
    },
    en: {
      bad: "Fill in every number: win rate 0–100%, RR above 0, drawdown and violations 0–100%.",
      ready: "🟢 Ready for a small live account",
      readyNote: "Every item is met. Start with $100–300 and 0.5% risk per trade, and compare live to demo for the first weeks — psychology with real money is different.",
      early: "🔴 Too early. Work on the items below",
      earlyNote: "Demo is free tuition. Every unmet item costs real money on a live account.",
      metrics: function (pf, e) { return "Profit Factor: <strong>" + pf + "</strong> · expectancy: <strong>" + e + " R</strong> per trade"; },
      items: {
        months: ["≥ " + L.months + " months on demo", "Keep trading demo — one lucky month looks just like a system."],
        trades: ["≥ " + L.trades + " trades", "Too few trades: the stats are still noise, not a result."],
        winrate: ["Win rate ≥ " + L.winrate + "%", "Find where you lose: entering before the signal, stop too tight?"],
        pf: ["Profit Factor ≥ " + L.pf, "Profits barely cover losses — live spread and slippage will eat that."],
        maxDD: ["Max drawdown ≤ " + L.maxDD + "%", "Cut risk per trade: a hole like that breaks you on a live account."],
        violations: ["Rule violations < " + L.violations + "% of trades", "Discipline first: a rule you break is not a rule."],
        journal: ["Journal for every trade", "Without a journal you can't see what to fix."],
        canLose: ["You can afford to lose the whole amount", "Don't go live with money your life depends on."],
      },
    },
    uz: {
      bad: "Barcha raqamlarni kiriting: winrate 0–100%, RR 0 dan katta, tushish va buzilishlar 0–100%.",
      ready: "🟢 Kichik real hisobga tayyor",
      readyNote: "Barcha bandlar bajarilgan. $100–300 va har savdoda 0.5% risk bilan boshlang, birinchi haftalarda realni demo bilan solishtiring — haqiqiy pulda psixologiya boshqacha.",
      early: "🔴 Hali erta. Quyidagi bandlarni yaxshilang",
      earlyNote: "Demo — bepul o'qish. Bajarilmagan har bir band realda pul turadi.",
      metrics: function (pf, e) { return "Profit Factor: <strong>" + pf + "</strong> · matematik kutilma: savdoga <strong>" + e + " R</strong>"; },
      items: {
        months: ["Demoda ≥ " + L.months + " oy", "Demoda davom eting — bir omadli oyni tizimdan ajratib bo'lmaydi."],
        trades: ["≥ " + L.trades + " savdo", "Savdolar kam: statistika hozircha natija emas, shovqin."],
        winrate: ["Winrate ≥ " + L.winrate + "%", "Qayerda yutqazayotganingizni toping: signaldan oldin kirish, juda yaqin stop?"],
        pf: ["Profit Factor ≥ " + L.pf, "Foyda zararni zo'rg'a qoplaydi — realda spred va slippage buni yeb qo'yadi."],
        maxDD: ["Maks. tushish ≤ " + L.maxDD + "%", "Savdo riskini kamaytiring: realda bunday chuqurlik psixikani buzadi."],
        violations: ["Qoida buzilishi < " + L.violations + "% savdolar", "Avval intizom: buziladigan qoida — qoida emas."],
        journal: ["Har bir savdo uchun jurnal", "Jurnalsiz nimani tuzatish kerakligi ko'rinmaydi."],
        canLose: ["Summani to'liq yo'qotishga tayyorman", "Hayotingiz bog'liq pul bilan realni boshlamang."],
      },
    },
  });

  function num(id) { return parseFloat(document.getElementById(id).value); }

  function calc() {
    var s = {
      months: num("rd-months"),
      trades: num("rd-trades"),
      winrate: num("rd-winrate"),
      rr: num("rd-rr"),
      maxDD: num("rd-dd"),
      violations: num("rd-viol"),
      journal: document.getElementById("rd-journal").checked,
      canLose: document.getElementById("rd-canlose").checked,
    };
    var out = document.getElementById("rd-result");
    var nums = [s.months, s.trades, s.winrate, s.rr, s.maxDD, s.violations];
    if (nums.some(isNaN) || nums.some(function (n) { return n < 0; }) ||
        s.winrate > 100 || s.rr <= 0 || s.maxDD > 100 || s.violations > 100) {
      out.innerHTML = '<div class="calc-warn">' + T.bad + "</div>";
      return;
    }
    var v = verdict(s);
    var list = v.checks.map(function (c) {
      var it = T.items[c.id];
      return "<li>" + (c.ok ? "✅ " + it[0] : "❌ <strong>" + it[0] + "</strong> — " + it[1]) + "</li>";
    }).join("");
    var pf = isFinite(v.pf) ? v.pf.toFixed(2) : "∞";
    out.innerHTML =
      '<div class="' + (v.ready ? "calc-ok" : "calc-error") + '"><h4>' +
      (v.ready ? T.ready : T.early) + "</h4><p>" + T.metrics(pf, v.expectancy.toFixed(2)) +
      "</p><ul>" + list + "</ul><p>" + (v.ready ? T.readyNote : T.earlyNote) + "</p></div>";
  }

  var btn = document.getElementById("rd-calc-btn");
  if (btn) btn.addEventListener("click", calc);
  calc();
})();
