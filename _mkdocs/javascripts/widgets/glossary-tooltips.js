/*
 * Тултипы глоссария в тексте глав.
 *
 * Глоссарий живёт отдельной страницей (extras/glossary.md), и читатель главы
 * узнавал о термине, только если сам догадывался туда сходить. Теперь на
 * страницах разделов docs/, practice/, growth/ и uz/ термины подчёркиваются
 * точками, а по наведению или фокусе с клавиатуры всплывает короткое
 * определение на языке страницы.
 *
 * Данные — data/glossary-terms.json (tools/build_glossary_terms.py из
 * extras/glossary*.md). В исходниках файл на локаль (glossary-terms.ru.json
 * и т.д.), но mkdocs-static-i18n при сборке раскладывает их по локальным
 * корням — /en/data/, /uz/data/, — поэтому виджет просит один и тот же
 * относительный путь и получает определения на языке страницы.
 *
 * Скрипт глобальный (extra_javascript), но сам решает по URL, нужен ли он
 * на странице: просыпается только в главах. Аббревиатуры вроде RSI/SL
 * подсвечивает другой механизм (abbr + хук hooks/glossary_tooltips.py),
 * поэтому их <abbr> здесь пропускаем — двойные тултипы никому не нужны.
 *
 * Пределы: только первое вхождение каждого термина и не больше MAX_TOTAL
 * подсветок на страницу — иначе вместо учебника получается ёлочная гирлянда.
 */
(function () {
  "use strict";

  var LANG = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (["ru", "en", "uz"].indexOf(LANG) < 0) return;

  // Разделы-главы. Служебные страницы (index, extras, tools…) не трогаем.
  var SECTIONS = ["docs", "practice", "growth", "uz"];

  var MAX_TOTAL = 15; // не больше стольких подсветок на всю страницу

  // Узлы, где матчить нельзя: ссылки, код, заголовки, квизы, чужие тултипы.
  var SKIP =
    "a, abbr, code, pre, kbd, samp, script, style, noscript," +
    " h1, h2, h3, form, .chapter-quiz, .fx-term";

  /* Путь вида /forex-toolkit/en/practice/lot-discipline/ → раздел practice.
     Префикс локали снимаем, только если он совпадает с языком страницы:
     «uz/» в русской локали — это раздел «Узбекистан», а не префикс. */
  var root = "/";
  var parts = location.pathname.split("/").filter(Boolean);
  if (parts[0] === "forex-toolkit") {
    root = "/forex-toolkit/";
    parts.shift();
  }
  var localePrefix = "";
  if (LANG === "en" && parts[0] === "en") {
    localePrefix = "en/";
    parts.shift();
  } else if (LANG === "uz" && parts[0] === "uz") {
    localePrefix = "uz/";
    parts.shift();
  } else if (LANG === "uz" && parts[0] === "uz-cyrl") {
    // Кириллическое зеркало uz: своих данных у него нет, а определения
    // на латыни к кириллическому тексту не подошли бы — пропускаем.
    return;
  }
  if (SECTIONS.indexOf(parts[0]) < 0) return;

  var article = document.querySelector(".md-content__inner");
  if (!article) return;

  function escapeRegExp(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  /* Собирает карту «термин → определение» и один регэксп на все термины.
     \b в JS не знает кириллицу (\w — только ASCII), поэтому границы слов
     делаем вручную: не-буква/не-цифра до и после. Длинные термины идут
     первыми, чтобы «Stop Loss» не съедался «Stop». */
  function compile(terms) {
    var defs = {};
    terms.forEach(function (item) {
      defs[item.term.toLowerCase()] = item.short;
    });
    var alternation = terms
      .slice()
      .sort(function (a, b) {
        return b.term.length - a.term.length;
      })
      .map(function (item) {
        return escapeRegExp(item.term);
      })
      .join("|");
    var re = new RegExp(
      "(^|[^\\p{L}\\p{N}_])(" + alternation + ")(?![\\p{L}\\p{N}_])",
      "giu"
    );
    return { defs: defs, re: re };
  }

  // Текстовые узлы статьи, кроме SKIP-поддеревьев. Сначала собираем в массив:
  // TreeWalker живой, а мы собираемся переписывать узлы прямо во время обхода.
  function collectTextNodes(rootNode) {
    var walker = document.createTreeWalker(rootNode, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !node.nodeValue.trim()) {
          return NodeFilter.FILTER_REJECT;
        }
        if (node.parentElement && node.parentElement.closest(SKIP)) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    var nodes = [];
    var node;
    while ((node = walker.nextNode())) nodes.push(node);
    return nodes;
  }

  function highlight(terms) {
    var compiled = compile(terms);
    var defs = compiled.defs;
    var re = compiled.re;
    var total = 0;
    var used = {};

    collectTextNodes(article).some(function (node) {
      if (total >= MAX_TOTAL) return true;
      var text = node.nodeValue;
      re.lastIndex = 0;
      var match;
      var cursor = 0;
      var fragment = null;

      while ((match = re.exec(text))) {
        if (total >= MAX_TOTAL) break;
        var start = match.index + match[1].length;
        var word = match[2];
        var key = word.toLowerCase();
        if (used[key]) continue;

        if (!fragment) fragment = document.createDocumentFragment();
        fragment.appendChild(
          document.createTextNode(text.slice(cursor, start))
        );

        var span = document.createElement("span");
        span.className = "fx-term";
        span.tabIndex = 0; // фокус с клавиатуры — тултип показывается и по :focus
        span.textContent = word;
        span.setAttribute("data-definition", defs[key]);
        span.setAttribute("aria-label", word + " — " + defs[key]);
        fragment.appendChild(span);

        cursor = start + word.length;
        used[key] = true;
        total += 1;
      }

      if (fragment) {
        fragment.appendChild(document.createTextNode(text.slice(cursor)));
        node.parentNode.replaceChild(fragment, node);
      }
      return false;
    });
  }

  fetch(root + localePrefix + "data/glossary-terms.json")
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(highlight)
    .catch(function () {
      /* Подсветка — дополнение, а не контент: без JSON (офлайн, старый кэш)
         страница просто остаётся обычным текстом. */
    });
})();
