/* ==========================================================================
   a11y.js — мелкие правки доступности поверх темы Material.

   1. Поиск Material — это role="dialog" без доступного имени (axe-правило
      aria-dialog-name, Lighthouse a11y падает). Material имени не задаёт —
      добавляем aria-label по локали страницы.
   ========================================================================== */
(function () {
  "use strict";

  var SEARCH_LABEL = {
    ru: "Поиск по сайту",
    en: "Search the site",
    uz: "Saytdan qidirish",
  };

  function labelSearchDialog() {
    var search = document.querySelector(".md-search");
    if (!search) return;
    if (search.getAttribute("aria-label")) return;
    var lang = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
    search.setAttribute("aria-label", SEARCH_LABEL[lang] || SEARCH_LABEL.ru);
  }

  // Material совместим с document$ (мгновенная навигация); поддержим и его.
  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(labelSearchDialog);
  } else if (document.readyState !== "loading") {
    labelSearchDialog();
  } else {
    document.addEventListener("DOMContentLoaded", labelSearchDialog);
  }
})();
