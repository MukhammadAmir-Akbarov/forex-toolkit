/* ==========================================================================
   hero.js — главная страница + глобальные UX-эффекты:
   1. Анимированные счётчики (.fx-stat__num[data-target])
   2. Scroll-reveal для .fx-feature-card и .fx-path__step
   3. Тикер активных торговых сессий (#fx-session-ticker)
   4. Floating CTA кнопка в шапке (только ≥ 960 px)
   ========================================================================== */
(function () {
  "use strict";

  /* ── 1. Анимированные счётчики ─────────────────────────────────────── */
  function animateCounters() {
    var els = document.querySelectorAll(".fx-stat__num[data-target]");
    if (!els.length) return;
    var DURATION = 1400;
    var easeOut = function (t) { return 1 - Math.pow(1 - t, 3); };
    els.forEach(function (el) {
      var target = parseInt(el.getAttribute("data-target"), 10);
      var suffix = el.getAttribute("data-suffix") || "";
      if (!target) return;
      var start = performance.now();
      (function step(now) {
        var t = Math.min((now - start) / DURATION, 1);
        el.textContent = Math.round(easeOut(t) * target) + suffix;
        if (t < 1) requestAnimationFrame(step);
      })(start);
    });
  }

  /* ── 2. Scroll-reveal ──────────────────────────────────────────────── */
  function initScrollReveal() {
    var targets = document.querySelectorAll(".fx-feature-card, .fx-path__step");
    if (!targets.length) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      targets.forEach(function (el) { el.classList.add("fx-revealed"); });
      return;
    }
    if (!window.IntersectionObserver) {
      targets.forEach(function (el) { el.classList.add("fx-revealed"); });
      return;
    }
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var delay = parseFloat(el.getAttribute("data-reveal-delay") || "0");
        setTimeout(function () { el.classList.add("fx-revealed"); }, delay * 1000);
        obs.unobserve(el);
      });
    }, { threshold: 0.12 });

    var cardIdx = 0, stepIdx = 0;
    targets.forEach(function (el) {
      el.classList.add("fx-reveal");
      var isStep = el.classList.contains("fx-path__step");
      var idx = isStep ? stepIdx++ : cardIdx++;
      el.setAttribute("data-reveal-delay", (idx * (isStep ? 0.12 : 0.09)).toFixed(2));
      obs.observe(el);
    });
  }

  /* ── 3. Тикер торговых сессий ──────────────────────────────────────── */
  function initTicker() {
    var el = document.getElementById("fx-session-ticker");
    if (!el) return;

    var SESSIONS = [
      { key: "sydney",  open: 22, close: 7  },
      { key: "tokyo",   open: 0,  close: 9  },
      { key: "london",  open: 8,  close: 17 },
      { key: "newyork", open: 13, close: 22 },
    ];
    var L = {
      ru: { sydney: "Сидней", tokyo: "Токио", london: "Лондон", newyork: "Нью-Йорк",
            weekend: "Выходные — рынок закрыт", pause: "Азиатская пауза" },
      en: { sydney: "Sydney", tokyo: "Tokyo", london: "London", newyork: "New York",
            weekend: "Weekend — market closed", pause: "Asian pause" },
      uz: { sydney: "Sidney", tokyo: "Tokio", london: "London", newyork: "Nyu-York",
            weekend: "Dam olish — bozor yopiq", pause: "Osiyo tanaffusi" },
    };
    var lang = (document.documentElement.lang || "ru").split("-")[0];
    var t = L[lang] || L.ru;

    function isOpen(open, close, h) {
      return open < close ? h >= open && h < close : h >= open || h < close;
    }

    function update() {
      var now = new Date();
      var h = now.getUTCHours() + now.getUTCMinutes() / 60;
      var day = now.getUTCDay();
      var weekend = day === 6 || (day === 0 && h < 22) || (day === 5 && h >= 22);

      if (weekend) {
        el.innerHTML =
          '<span class="fx-tick__dot fx-tick__dot--off"></span>' + t.weekend;
        return;
      }
      var open = SESSIONS.filter(function (s) { return isOpen(s.open, s.close, h); });
      if (!open.length) {
        el.innerHTML =
          '<span class="fx-tick__dot fx-tick__dot--off"></span>' + t.pause;
        return;
      }
      var hot = open.some(function (s) { return s.key === "london"; }) &&
                open.some(function (s) { return s.key === "newyork"; });
      var parts = open.map(function (s) {
        return '<span class="fx-tick__pill' + (hot ? " fx-tick__pill--hot" : "") + '">' +
               '<span class="fx-tick__dot fx-tick__dot--on' +
               (hot ? " fx-tick__dot--hot" : "") + '"></span>' +
               t[s.key] + "</span>";
      });
      el.innerHTML = parts.join('<span class="fx-tick__sep">·</span>');
    }

    update();
    setInterval(update, 60000);
  }

  /* ── 4. Floating CTA кнопка в навбаре (≥ 960 px) ──────────────────── */
  function initNavCta() {
    if (document.querySelector(".fx-nav-cta")) return;
    var header = document.querySelector(".md-header__inner");
    if (!header) return;

    var lang = (document.documentElement.lang || "ru").split("-")[0];
    var labels = { ru: "Начать →", en: "Start →", uz: "Boshlash →" };

    /* Вычисляем корень текущей локали из кнопки-логотипа Material.
       Это даёт абсолютный URL независимо от глубины вложенности страницы:
       /forex-toolkit/           (RU)
       /forex-toolkit/en/        (EN)
       /forex-toolkit/uz/        (UZ) */
    var logoBtn = document.querySelector(".md-header__button.md-logo");
    var localeRoot = logoBtn ? logoBtn.href : window.location.origin + "/";

    var a = document.createElement("a");
    a.href = localeRoot + "forex-guide/";
    a.className = "md-button md-button--primary fx-nav-cta";
    a.textContent = labels[lang] || labels.ru;
    header.appendChild(a);
  }

  /* ── Инициализация ─────────────────────────────────────────────────── */
  document.addEventListener("DOMContentLoaded", function () {
    animateCounters();
    initScrollReveal();
    initTicker();
    initNavCta();
  });
})();
