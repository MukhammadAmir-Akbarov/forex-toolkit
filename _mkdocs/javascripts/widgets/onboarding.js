/*
 * Мастер «С чего начать?» на главной: 3 вопроса → маршрут на 3 дня.
 *
 * Зачем: 30+ инструментов пугают новичка, а «Путь трейдера» на главной
 * одинаков для всех. Опыт, деньги и цель меняют порядок: новичку — основа и
 * «Первые 15 минут», опытному — диагностика roadmap (вычёркивает известное),
 * тому, кто собирается на реал, — проверка брокера и вердикт по демо.
 * Заёмные деньги — всегда первым шагом тест готовности.
 *
 * Ответы — localStorage forex_onboarding_v1 (в бэкапе кабинета). Пока ответов
 * нет, мастер показывается как баннер; потом — сразу готовый маршрут.
 * Чистая функция маршрута — window.__fxOnboardingRoute
 * (tests/test_onboarding_widget.py). Ссылки относительные: виджет живёт
 * только на главной своей локали.
 */
(function () {
  var KEY = "forex_onboarding_v1";

  // Шаг → адрес относительно главной локали.
  var URLS = {
    first15: "first-15/",
    guide: "forex-guide/",
    diag: "roadmap/#roadmap-diag",
    riskProfile: "tools/risk-profile/",
    position: "tools/position-calculator/",
    drawdown: "tools/drawdown-recovery/",
    replay: "tools/replay-trainer/",
    flash: "tools/flashcards/",
    journal: "journal/",
    readiness: "tools/demo-readiness/",
    broker: "tools/broker-check/",
    overfitting: "tools/overfitting/",
    exam: "tools/exam/",
  };

  // a: { exp: none|charts|demo|live, money: none|small|big|borrowed,
  //      goal: understand|demo|live|algo } → { days: [[step…]×3], warn }
  function route(a) {
    var novice = a.exp === "none" || a.exp === "charts";
    var day1 = a.exp === "none" ? ["first15", "guide"] : ["diag"];
    var day2 = ["position", novice ? "drawdown" : "journal"];
    var day3 = novice ? ["replay", "flash"] : ["readiness"];
    if (a.goal === "live" || a.exp === "live") day3.push("broker");
    if (a.goal === "live" && day3.indexOf("readiness") === -1) day3.push("readiness");
    if (a.goal === "algo") day3.push("overfitting");
    if (a.goal === "understand") day3.push("exam");
    if (a.money === "borrowed") day1.unshift("riskProfile");
    else day2.push("riskProfile");
    return {
      days: [day1, day2, day3],
      // Без своих денег или на заёмные — реал не обсуждается, только демо.
      warn: a.money === "borrowed" ? "borrowed" : (a.goal === "live" && novice ? "early" : null),
    };
  }
  window.__fxOnboardingRoute = route;

  var root = document.getElementById("fx-onboarding");
  if (!root || !window.FXW) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      title: "🧭 С чего начать? 3 вопроса — и маршрут на 3 дня",
      q: [
        ["exp", "Твой опыт", { none: "Нулевой", charts: "Смотрел графики, читал", demo: "Торгую на демо", live: "Торговал на реальные" }],
        ["money", "Деньги на трейдинг", { none: "Пока нет — только учусь", small: "До $500", big: "$500 и больше", borrowed: "Заёмные / в кредит" }],
        ["goal", "Цель", { understand: "Понять, как это работает", demo: "Научиться торговать на демо", live: "Выйти на реальный счёт", algo: "Автоматизировать стратегию" }],
      ],
      go: "Собрать маршрут", redo: "Ответить заново", pickAll: "Ответь на все три вопроса.",
      day: "День", routeTitle: "🗺️ Твой маршрут",
      warn: {
        borrowed: "⚠️ Заёмные деньги — главный способ потерять больше, чем было. Начни с теста готовности и торгуй только на демо.",
        early: "⚠️ Реал без опыта — рано. Маршрут ведёт через демо; вердикт «Готов ли я к реалу?» скажет, когда пора.",
      },
      steps: {
        first15: "Первые 15 минут — рабочий цикл", guide: "Учебник: основы forex", diag: "Диагностика: вычеркни, что уже знаешь",
        riskProfile: "Тест готовности (подушка, психология)", position: "Калькулятор позиции", drawdown: "Почему просадка опасна",
        replay: "Replay: решения на истории без денег", flash: "Карточки: закрепи термины", journal: "Журнал сделок",
        readiness: "Готов ли я к реалу? — вердикт по демо", broker: "Проверка брокера", overfitting: "Почему бэктест врёт",
        exam: "Итоговый экзамен",
      },
    },
    en: {
      title: "🧭 Where to start? 3 questions — a 3-day route",
      q: [
        ["exp", "Your experience", { none: "None", charts: "Watched charts, read a bit", demo: "Trading on demo", live: "Traded real money" }],
        ["money", "Money for trading", { none: "None yet — just learning", small: "Up to $500", big: "$500 or more", borrowed: "Borrowed / on credit" }],
        ["goal", "Goal", { understand: "Understand how it works", demo: "Learn to trade on demo", live: "Move to a live account", algo: "Automate a strategy" }],
      ],
      go: "Build my route", redo: "Answer again", pickAll: "Answer all three questions.",
      day: "Day", routeTitle: "🗺️ Your route",
      warn: {
        borrowed: "⚠️ Borrowed money is the surest way to lose more than you had. Start with the readiness test and trade demo only.",
        early: "⚠️ Going live without experience is too early. The route goes through demo; the “Am I ready for live?” verdict will tell you when.",
      },
      steps: {
        first15: "First 15 minutes — the working cycle", guide: "Handbook: forex basics", diag: "Diagnostic: cross off what you know",
        riskProfile: "Readiness test (cushion, psychology)", position: "Position calculator", drawdown: "Why drawdown is dangerous",
        replay: "Replay: decisions on history, no money", flash: "Flashcards: lock in the terms", journal: "Trading journal",
        readiness: "Am I ready for live? — demo verdict", broker: "Broker check", overfitting: "Why backtests lie",
        exam: "Final exam",
      },
    },
    uz: {
      title: "🧭 Nimadan boshlash? 3 savol — 3 kunlik yo'nalish",
      q: [
        ["exp", "Tajribangiz", { none: "Yo'q", charts: "Grafiklarni ko'rganman, o'qiganman", demo: "Demoda savdo qilaman", live: "Haqiqiy pulda savdo qilganman" }],
        ["money", "Savdo uchun pul", { none: "Hozircha yo'q — o'rganyapman", small: "$500 gacha", big: "$500 va undan ko'p", borrowed: "Qarz / kreditga" }],
        ["goal", "Maqsad", { understand: "Qanday ishlashini tushunish", demo: "Demoda savdoni o'rganish", live: "Real hisobga o'tish", algo: "Strategiyani avtomatlashtirish" }],
      ],
      go: "Yo'nalish tuzish", redo: "Qaytadan javob berish", pickAll: "Uchala savolga javob bering.",
      day: "Kun", routeTitle: "🗺️ Sizning yo'nalishingiz",
      warn: {
        borrowed: "⚠️ Qarz pul — borimizdan ko'p yo'qotishning eng ishonchli yo'li. Tayyorlik testidan boshlang va faqat demoda savdo qiling.",
        early: "⚠️ Tajribasiz realga chiqish — erta. Yo'nalish demo orqali o'tadi; «Realga tayyormanmi?» xulosasi qachon vaqt kelganini aytadi.",
      },
      steps: {
        first15: "Birinchi 15 daqiqa — ish sikli", guide: "Darslik: forex asoslari", diag: "Diagnostika: bilganingizni o'chiring",
        riskProfile: "Tayyorlik testi (zaxira, psixologiya)", position: "Pozitsiya kalkulyatori", drawdown: "Nega tushish xavfli",
        replay: "Replay: tarixda pulsiz qarorlar", flash: "Kartochkalar: atamalarni mustahkamlang", journal: "Savdo jurnali",
        readiness: "Realga tayyormanmi? — demo xulosasi", broker: "Brokerni tekshirish", overfitting: "Nega bektest aldaydi",
        exam: "Yakuniy imtihon",
      },
    },
  });

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { return null; }
  }

  function renderForm() {
    root.innerHTML =
      '<div class="calc-widget"><h3>' + T.title + "</h3>" +
      T.q.map(function (q) {
        return '<fieldset class="fx-onb__q"><legend><strong>' + q[1] + "</strong></legend>" +
          Object.keys(q[2]).map(function (v) {
            return '<label><input type="radio" name="onb-' + q[0] + '" value="' + v + '"> ' + q[2][v] + "</label>";
          }).join("") + "</fieldset>";
      }).join("") +
      '<button class="calc-button" id="onb-go">' + T.go + '</button><div id="onb-msg"></div></div>';
    document.getElementById("onb-go").addEventListener("click", function () {
      var a = {};
      T.q.forEach(function (q) {
        var el = root.querySelector('input[name="onb-' + q[0] + '"]:checked');
        if (el) a[q[0]] = el.value;
      });
      if (!a.exp || !a.money || !a.goal) {
        document.getElementById("onb-msg").innerHTML = '<div class="calc-warn">' + T.pickAll + "</div>";
        return;
      }
      try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {}
      renderRoute(a);
    });
  }

  function renderRoute(a) {
    var r = route(a);
    root.innerHTML =
      '<div class="calc-widget"><h3>' + T.routeTitle + "</h3>" +
      (r.warn ? '<div class="calc-warn">' + T.warn[r.warn] + "</div>" : "") +
      "<ol>" + r.days.map(function (steps, i) {
        return "<li><strong>" + T.day + " " + (i + 1) + ":</strong> " + steps.map(function (s) {
          return '<a href="' + URLS[s] + '">' + T.steps[s] + "</a>";
        }).join(" → ") + "</li>";
      }).join("") + "</ol>" +
      '<button class="calc-button" id="onb-redo">' + T.redo + "</button></div>";
    document.getElementById("onb-redo").addEventListener("click", function () {
      try { localStorage.removeItem(KEY); } catch (e) {}
      renderForm();
    });
  }

  var saved = load();
  if (saved && saved.exp && saved.money && saved.goal) renderRoute(saved);
  else renderForm();
})();
