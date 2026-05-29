/* ==========================================================================
   Forex Toolkit — трекер прогресса обучения
   Кнопка «Отметить как пройдено» на каждой странице урока.
   Состояние хранится в localStorage браузера (ничего не уходит на сервер).
   Показывает галочки в меню и счётчик «Пройдено N из M».
   ========================================================================== */

(function () {
  "use strict";

  var KEY = "fx-progress-v1";

  var LABELS = {
    ru: {
      mark: "Отметить как пройдено",
      done: "Пройдено",
      count: function (n, m) { return "Пройдено " + n + " из " + m; }
    },
    en: {
      mark: "Mark as read",
      done: "Completed",
      count: function (n, m) { return n + " of " + m + " read"; }
    },
    uz: {
      mark: "O'qildi deb belgilash",
      done: "O'qildi",
      count: function (n, m) { return m + " dan " + n + " tasi o'qildi"; }
    }
  };

  function t() {
    var code = (document.documentElement.lang || "ru").slice(0, 2);
    return LABELS[code] || LABELS.ru;
  }

  /* --- хранилище --- */
  function load() {
    try {
      return new Set(JSON.parse(localStorage.getItem(KEY) || "[]"));
    } catch (e) {
      return new Set();
    }
  }
  function save(set) {
    try {
      localStorage.setItem(KEY, JSON.stringify(Array.from(set)));
    } catch (e) { /* приватный режим — молча игнорируем */ }
  }

  function pathOf(href) {
    try { return new URL(href, location.href).pathname; }
    catch (e) { return null; }
  }

  /* --- все внутренние ссылки навигации (для счётчика и галочек) --- */
  function navAnchors() {
    return Array.prototype.slice
      .call(document.querySelectorAll(".md-nav--primary .md-nav__link[href]"))
      .filter(function (a) {
        var p = pathOf(a.getAttribute("href"));
        return p && a.host === location.host;
      });
  }

  function checkIcon() {
    return (
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">' +
      '<polyline points="20 6 9 17 4 12"></polyline></svg>'
    );
  }

  /* --- отрисовка галочек в меню и пересчёт счётчика --- */
  function refresh(done, els) {
    var anchors = navAnchors();
    var totalPaths = {};
    anchors.forEach(function (a) {
      var p = pathOf(a.getAttribute("href"));
      totalPaths[p] = true;
      a.classList.toggle("fx-done", done.has(p));
    });
    var total = Object.keys(totalPaths).length;
    var current = location.pathname;
    var n = 0;
    Object.keys(totalPaths).forEach(function (p) { if (done.has(p)) n++; });

    if (els) {
      var isDone = done.has(current);
      els.btn.classList.toggle("fx-progress__btn--done", isDone);
      els.btn.setAttribute("aria-pressed", isDone ? "true" : "false");
      els.label.textContent = isDone ? t().done : t().mark;
      els.icon.style.display = isDone ? "inline-flex" : "none";
      if (total > 0) {
        els.count.textContent = t().count(n, total);
        els.fill.style.width = Math.round((n / total) * 100) + "%";
      }
    }
  }

  function build() {
    var article = document.querySelector(".md-content article");
    if (!article) return;
    if (article.querySelector(".fx-hero")) return;       // главная — пропускаем
    if (article.querySelector(".fx-progress")) return;   // уже добавлено
    var h1 = article.querySelector("h1");
    if (!h1) return;

    var done = load();

    var wrap = document.createElement("div");
    wrap.className = "fx-progress";
    wrap.innerHTML =
      '<button class="fx-progress__btn" type="button">' +
        '<span class="fx-progress__icon">' + checkIcon() + "</span>" +
        '<span class="fx-progress__label"></span>' +
      "</button>" +
      '<div class="fx-progress__stat">' +
        '<div class="fx-progress__bar"><span class="fx-progress__fill"></span></div>' +
        '<span class="fx-progress__count"></span>' +
      "</div>";

    var els = {
      btn: wrap.querySelector(".fx-progress__btn"),
      icon: wrap.querySelector(".fx-progress__icon"),
      label: wrap.querySelector(".fx-progress__label"),
      count: wrap.querySelector(".fx-progress__count"),
      fill: wrap.querySelector(".fx-progress__fill")
    };

    els.btn.addEventListener("click", function () {
      var set = load();
      var p = location.pathname;
      if (set.has(p)) { set.delete(p); } else { set.add(p); }
      save(set);
      refresh(set, els);
    });

    // Вставляем под бейджем времени чтения, если он есть, иначе под H1.
    var anchor = article.querySelector(".fx-readtime") || h1;
    anchor.insertAdjacentElement("afterend", wrap);

    refresh(done, els);
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(build);
  } else if (document.readyState !== "loading") {
    build();
  } else {
    document.addEventListener("DOMContentLoaded", build);
  }
})();
