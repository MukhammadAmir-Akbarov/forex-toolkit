(function () {
  "use strict";

  var root = document.getElementById("first-15-widget");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var KEY = "forex_first15_v1";
  var T = F.pick({
    ru: {
      title: "Твой быстрый старт", progress: "Выполнено", done: "Готово", mark: "Я прочитал основу",
      next: "Следующий шаг", complete: "Маршрут завершён. Теперь переходи к полной дорожной карте.",
      steps: [
        ["1. Понять основу", "Узнай, что такое пипс, лот, риск и почему сначала нужна демо-практика.", "Открыть основу"],
        ["2. Рассчитать позицию", "Получи безопасный лот по депозиту, риску и стопу.", "Открыть калькулятор"],
        ["3. Пройти Replay", "Прими несколько решений на историческом графике без денег.", "Открыть Replay"],
        ["4. Сохранить первый план", "Пройди чек-лист и добавь план напрямую в журнал.", "Создать план"]
      ]
    },
    en: {
      title: "Your quick start", progress: "Completed", done: "Done", mark: "I read the basics",
      next: "Next step", complete: "Route complete. Continue with the full learning roadmap.",
      steps: [
        ["1. Understand the basics", "Learn what pips, lots and risk mean, and why demo practice comes first.", "Open the basics"],
        ["2. Size a position", "Get a safe lot size from balance, risk and stop distance.", "Open calculator"],
        ["3. Complete Replay", "Make several decisions on historical charts without money.", "Open Replay"],
        ["4. Save the first plan", "Complete the checklist and add a plan directly to the journal.", "Create plan"]
      ]
    },
    uz: {
      title: "Tezkor boshlash", progress: "Bajarildi", done: "Tayyor", mark: "Asosni o'qidim",
      next: "Keyingi qadam", complete: "Yo'nalish tugadi. Endi to'liq o'quv yo'l xaritasiga o'ting.",
      steps: [
        ["1. Asosni tushunish", "Pip, lot va risk nima ekanini hamda nega avval demo kerakligini biling.", "Asosni ochish"],
        ["2. Pozitsiyani hisoblash", "Balans, risk va stop bo'yicha xavfsiz lotni oling.", "Kalkulyatorni ochish"],
        ["3. Replay mashqi", "Pulsiz tarixiy grafikda bir nechta qaror qabul qiling.", "Replayni ochish"],
        ["4. Birinchi rejani saqlash", "Checklistdan o'ting va rejani to'g'ridan-to'g'ri jurnalga qo'shing.", "Reja yaratish"]
      ]
    }
  });
  var hrefs = ["../forex-guide/", "../tools/position-calculator/", "../tools/replay-trainer/", "../tools/trade-desk/"];

  function readJSON(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback)); } catch (e) { return fallback; }
  }

  function progress() {
    var stored = readJSON(KEY, {});
    var replay = readJSON("forex_replay_stats", {});
    var plans = readJSON("forex_trade_drafts_v1", []);
    return [Boolean(stored.basics), Boolean(stored.position), Boolean(replay.trades || stored.replay), Boolean((Array.isArray(plans) && plans.length) || stored.plan)];
  }

  function saveBasics() {
    var stored = readJSON(KEY, {});
    stored.basics = true;
    stored.updatedAt = new Date().toISOString();
    try { localStorage.setItem(KEY, JSON.stringify(stored)); } catch (e) {}
    render();
  }

  function render() {
    var completed = progress();
    var count = completed.filter(Boolean).length;
    var next = completed.indexOf(false);
    root.innerHTML = [
      '<div class="first-15-hero"><h2>' + T.title + '</h2><strong>' + T.progress + ': ' + count + ' / 4</strong><div class="first-15-bar"><span style="width:' + count * 25 + '%"></span></div></div>',
      '<div class="first-15-list">',
      T.steps.map(function (step, index) {
        var action = index === 0 && !completed[index]
          ? '<button type="button" id="first-15-basics">' + T.mark + '</button>'
          : '<a href="' + hrefs[index] + '">' + (completed[index] ? T.done : step[2]) + '</a>';
        return '<article class="first-15-step' + (completed[index] ? ' is-done' : '') + '"><span class="first-15-number">' + (completed[index] ? '✓' : index + 1) + '</span><div><h3>' + step[0] + '</h3><p>' + step[1] + '</p>' + action + '</div></article>';
      }).join(""),
      '</div>',
      '<div class="first-15-next"><strong>' + T.next + ':</strong> ' + (next < 0 ? T.complete : '<a href="' + hrefs[next] + '">' + T.steps[next][2] + '</a>') + '</div>'
    ].join("");
    var basics = document.getElementById("first-15-basics");
    if (basics) basics.addEventListener("click", saveBasics);
    if (count === 4 && window.fxTrack) window.fxTrack("first15_completed");
  }

  window.addEventListener("pageshow", render);
  document.addEventListener("visibilitychange", function () { if (!document.hidden) render(); });
  render();
})();
