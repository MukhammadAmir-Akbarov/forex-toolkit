/*
 * TL;DR-блок «Простыми словами за 30 секунд» в начале каждой страницы.
 *
 * Тексты лежат в data/tldr.json одним файлом (ключ — путь страницы без
 * расширения и локали), а не размазаны по 258 файлам: так перевод не может
 * «отстать» от оригинала — все три локали живут в одной строке. Блок
 * вставляется JS сразу после H1 и рисуется штатными стилями admonition,
 * поэтому выглядит как родная часть страницы.
 *
 * Страницы index / offline / privacy намеренно без блока: на главной свой
 * герой, служебным страницам пересказ не нужен.
 */
(function () {
  var LANG = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (["ru", "en", "uz"].indexOf(LANG) < 0) return; // uz-cyrl — кириллическая копия uz, блок не дублируем

  var TITLE = {
    ru: "Простыми словами за 30 секунд",
    en: "In plain words, in 30 seconds",
    uz: "Oddiy so'zlar bilan, 30 soniyada",
  }[LANG];

  /* Путь вида /forex-toolkit/en/tools/pip-calculator/ → ключ tools/pip-calculator
     и корень сайта /forex-toolkit/. Локально корень — просто /. */
  var parts = location.pathname.split("/").filter(Boolean);
  var root = "/";
  if (parts[0] === "forex-toolkit") {
    root = "/forex-toolkit/";
    parts.shift();
  }
  if (["en", "uz", "uz-cyrl"].indexOf(parts[0]) >= 0) parts.shift();
  var key = parts.join("/") || "index";

  fetch(root + "data/tldr.json")
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (all) {
      var entry = all[key];
      if (!entry || !entry[LANG]) return;
      var article = document.querySelector(".md-content__inner");
      if (!article) return;
      var block = document.createElement("div");
      block.className = "admonition tip fx-tldr";
      block.innerHTML =
        '<p class="admonition-title">' + TITLE + "</p><p>" + entry[LANG] + "</p>";
      var h1 = article.querySelector("h1");
      if (h1 && h1.nextSibling) article.insertBefore(block, h1.nextSibling);
      else if (h1) article.appendChild(block);
      else article.insertBefore(block, article.firstChild);
    })
    .catch(function () {
      /* Блок — приятное дополнение, а не критичный контент: без JSON
         (старое кэширование, офлайн) страница просто остаётся как была. */
    });
})();
