/* ==========================================================================
   Forex Toolkit — улучшения чтения
   1) Прогресс-бар чтения вверху страницы.
   2) Бейдж «время чтения» под заголовком (RU / EN / UZ).
   Работает с мгновенной навигацией Material (navigation.instant) через document$.
   ========================================================================== */

(function () {
  "use strict";

  /* ----------------------------------------------------------------------
     1. Прогресс-бар чтения (создаётся один раз, body не пересоздаётся).
     ---------------------------------------------------------------------- */
  var bar = document.createElement("div");
  bar.className = "fx-reading-progress";
  bar.setAttribute("aria-hidden", "true");
  document.body.appendChild(bar);

  function updateProgress() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - doc.clientHeight;
    var pct = max > 0 ? (doc.scrollTop / max) * 100 : 0;
    bar.style.width = pct.toFixed(2) + "%";
  }

  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress, { passive: true });

  /* ----------------------------------------------------------------------
     2. Бейдж времени чтения.
     ---------------------------------------------------------------------- */
  var WORDS_PER_MIN = 180; // средняя скорость осознанного чтения

  var LABELS = {
    ru: function (m) { return m + " мин чтения"; },
    en: function (m) { return m + " min read"; },
    uz: function (m) { return m + " daqiqa o'qish"; }
  };

  function currentLang() {
    var code = (document.documentElement.lang || "ru").slice(0, 2);
    return LABELS[code] ? code : "ru";
  }

  function clockIcon() {
    return (
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path></svg>'
    );
  }

  function addReadingTime() {
    var article = document.querySelector(".md-content article");
    if (!article) return;
    if (article.querySelector(".fx-readtime")) return; // уже добавлено
    if (article.querySelector(".fx-hero")) return;      // главная — пропускаем

    var h1 = article.querySelector("h1");
    if (!h1) return;

    var words = (article.innerText || "").trim().split(/\s+/).filter(Boolean).length;
    if (words < 60) return; // короткие служебные страницы

    var minutes = Math.max(1, Math.round(words / WORDS_PER_MIN));
    var badge = document.createElement("div");
    badge.className = "fx-readtime";
    badge.innerHTML = clockIcon() + "<span>" + LABELS[currentLang()](minutes) + "</span>";
    h1.insertAdjacentElement("afterend", badge);
  }

  function onPageReady() {
    addReadingTime();
    updateProgress();
  }

  /* ----------------------------------------------------------------------
     3. Запуск — с поддержкой мгновенной навигации Material.
     ---------------------------------------------------------------------- */
  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(onPageReady);
  } else if (document.readyState !== "loading") {
    onPageReady();
  } else {
    document.addEventListener("DOMContentLoaded", onPageReady);
  }
})();
