(function () {
  "use strict";

  var ALLOWED = {
    calculator_completed: true,
    replay_completed: true,
    journal_demo_opened: true,
    journal_import_completed: true,
    exam_completed: true,
    dashboard_next_opened: true,
    feedback_yes: true,
    feedback_no: true,
    risk_exposure_completed: true,
    trade_plan_saved: true,
    monte_carlo_completed: true
  };
  var pending = [];

  function storageKey(name) {
    return "fx-event:" + name + ":" + window.location.pathname;
  }

  function send(name) {
    if (!window.goatcounter || typeof window.goatcounter.count !== "function") {
      if (pending.indexOf(name) < 0) pending.push(name);
      return false;
    }
    window.goatcounter.count({ path: name, title: name, event: true });
    return true;
  }

  window.fxTrack = function (name, options) {
    if (!ALLOWED[name]) return false;
    var once = !options || options.once !== false;
    try {
      if (once && sessionStorage.getItem(storageKey(name))) return false;
      if (once) sessionStorage.setItem(storageKey(name), "1");
    } catch (error) {}
    send(name);
    return true;
  };

  function flush() {
    if (!window.goatcounter || typeof window.goatcounter.count !== "function") return;
    pending.splice(0).forEach(send);
  }

  var calculatorButtons = {
    "mc-calc-btn": true,
    "cc-calc-btn": true,
    "pp-calc-btn": true,
    "pc-calc-btn": true,
    "wr-calc-btn": true,
    "tax-calc-btn": true,
    "co-calc-btn": true
  };

  document.addEventListener("click", function (event) {
    var button = event.target.closest("button");
    if (button && calculatorButtons[button.id]) window.fxTrack("calculator_completed");
    var dashboardLink = event.target.closest(".sd-card__link");
    if (dashboardLink) window.fxTrack("dashboard_next_opened");
  });

  var feedbackCopy = {
    ru: {
      title: "Была ли страница полезна?",
      yes: "Да, страница помогла",
      no: "Нет, страницу можно улучшить",
      thanks: "Спасибо за обратную связь!",
      improve: "Спасибо! Расскажи подробнее в Discussions."
    },
    en: {
      title: "Was this page helpful?",
      yes: "Yes, this page helped",
      no: "No, this page can be improved",
      thanks: "Thanks for your feedback!",
      improve: "Thanks! Tell us more in Discussions."
    },
    uz: {
      title: "Bu sahifa foydali bo'ldimi?",
      yes: "Ha, sahifa yordam berdi",
      no: "Yo'q, sahifani yaxshilash mumkin",
      thanks: "Fikr-mulohazangiz uchun rahmat!",
      improve: "Rahmat! Discussions bo'limida batafsil yozing."
    }
  };

  function initFeedback() {
    var form = document.querySelector("form.md-feedback");
    if (!form || form.dataset.fxReady === "1") return;
    form.dataset.fxReady = "1";
    form.hidden = false;
    var lang = (document.documentElement.lang || "ru").slice(0, 2);
    var copy = feedbackCopy[lang] || feedbackCopy.ru;
    var title = form.querySelector(".md-feedback__title");
    var buttons = form.querySelectorAll("button[data-md-value]");
    var notes = form.querySelectorAll(".md-feedback__note [data-md-value]");
    var list = form.querySelector(".md-feedback__list");
    var key = "fx-feedback:" + window.location.pathname;
    var saved = null;
    try { saved = localStorage.getItem(key); } catch (error) {}

    if (title) title.textContent = copy.title;
    buttons.forEach(function (button) {
      var yes = button.dataset.mdValue === "1";
      button.title = yes ? copy.yes : copy.no;
      button.setAttribute("aria-label", button.title);
    });
    notes.forEach(function (note) {
      var yes = note.dataset.mdValue === "1";
      if (yes) note.textContent = copy.thanks;
      else note.innerHTML = copy.improve.replace(
        "Discussions",
        '<a href="https://github.com/MukhammadAmir-Akbarov/forex-toolkit/discussions" target="_blank" rel="noopener">Discussions</a>'
      );
    });

    function show(value) {
      if (list) {
        list.hidden = true;
        list.style.display = "none";
      }
      notes.forEach(function (note) { note.hidden = note.dataset.mdValue !== value; });
    }
    if (saved === "0" || saved === "1") show(saved);

    form.addEventListener("submit", function (event) { event.preventDefault(); });
    buttons.forEach(function (button) {
      button.addEventListener("click", function (event) {
        event.preventDefault();
        if (saved === "0" || saved === "1") return;
        saved = button.dataset.mdValue;
        try { localStorage.setItem(key, saved); } catch (error) {}
        window.fxTrack(saved === "1" ? "feedback_yes" : "feedback_no");
        show(saved);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", initFeedback);
  if (typeof document$ !== "undefined") document$.subscribe(initFeedback);
  window.setInterval(flush, 1000);
})();
