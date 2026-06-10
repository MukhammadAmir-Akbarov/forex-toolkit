/* ==========================================================================
   Forex Toolkit — переключатель письма для узбекской локали: лотин ⇄ кирилл.

   Зачем: весь UZ-контент написан латиницей (o'zbek lotin). Но значительная
   часть аудитории — особенно старшего возраста и из регионов — читает и ищет
   кириллицей. Этот скрипт на лету транслитерирует видимый текст страницы
   лотин→кирилл (и обратно — простым восстановлением оригинала) и запоминает
   выбор в localStorage. Никаких дополнительных файлов контента: один источник
   (латиница), второе письмо генерируется в браузере.

   Важно: это вспомогательная авто-транслитерация, а не выверенная орфография.
   Имена собственные/аббревиатуры (ESMA, MT5) могут выглядеть непривычно —
   это нормально для машинного перевода письма.

   Работает только на страницах локали uz. Совместим с document$ (Material).
   ========================================================================== */

(function () {
  "use strict";

  /* Активируем только на узбекской локали. i18n строит uz-страницы под /uz/
     и проставляет <html lang="uz">. Проверяем оба признака. */
  function isUzLocale() {
    var lang = (document.documentElement.lang || "").slice(0, 2).toLowerCase();
    if (lang === "uz") return true;
    return /\/uz\//.test(location.pathname) || /\.uz\//.test(location.pathname);
  }

  var STORAGE_KEY = "fx-uz-script"; // "latn" | "cyrl"

  /* ----------------------------------------------------------------------
     Таблицы транслитерации лотин → кирилл.
     Многобуквенные сочетания обрабатываются раньше одиночных букв.
     o' / g' с любым видом апострофа сначала схлопываются в ў / ғ
     отдельным проходом, чтобы не конфликтовать с «yo», «ya» и т.п.
     ---------------------------------------------------------------------- */
  var MAP2 = {
    "sh": "ш", "ch": "ч",
    "yo": "ё", "yu": "ю", "ya": "я", "ye": "е", "ts": "ц"
  };
  var MAP1 = {
    "a": "а", "b": "б", "c": "с", "d": "д", "f": "ф", "g": "г",
    "h": "ҳ", "i": "и", "j": "ж", "k": "к", "l": "л", "m": "м",
    "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с",
    "t": "т", "u": "у", "v": "в", "w": "в", "x": "х", "y": "й", "z": "з"
  };

  /* Все варианты апострофа (ASCII, модификаторы, типографские) → один ' */
  var APOS = /[ʻʼ‘’`´′']/g;

  function isLatinLetter(ch) {
    return /[A-Za-z]/.test(ch);
  }

  /* Применяем регистр исходного латинского токена к кириллическому выводу. */
  function applyCase(src, out) {
    if (src === src.toLowerCase()) return out; // нет заглавных
    var allUpper = src === src.toUpperCase();
    if (allUpper && src.length > 1) return out.toUpperCase();
    return out.charAt(0).toUpperCase() + out.slice(1);
  }

  function toCyrillic(text) {
    if (!text) return text;

    // 1) Схлопываем o'/g' (любой апостроф) в ў/ғ с учётом регистра.
    var s = text.replace(APOS, "'");
    s = s.replace(/([OoGg])'/g, function (_m, l) {
      if (l === "o") return "ў";
      if (l === "O") return "Ў";
      if (l === "g") return "ғ";
      return "Ғ";
    });

    // 2) Токенайзер с приоритетом двухбуквенных сочетаний.
    var out = "";
    var i = 0;
    var n = s.length;
    while (i < n) {
      var ch = s[i];

      if (!isLatinLetter(ch)) {
        // tutuq belgisi (одиночный апостроф) → ъ; прочие символы как есть.
        out += ch === "'" ? "ъ" : ch;
        i += 1;
        continue;
      }

      var two = s.substr(i, 2);
      var twoLower = two.toLowerCase();
      if (two.length === 2 && MAP2[twoLower]) {
        out += applyCase(two, MAP2[twoLower]);
        i += 2;
        continue;
      }

      var lower = ch.toLowerCase();
      var cyr;
      if (lower === "e") {
        // e в начале слова → э, внутри слова → е.
        var prev = out.length ? out[out.length - 1] : "";
        var atWordStart = prev === "" || !/[А-Яа-яЎўҒғҚқҲҳ]/.test(prev);
        cyr = atWordStart ? "э" : "е";
      } else {
        cyr = MAP1[lower];
      }

      if (cyr) {
        out += applyCase(ch, cyr);
      } else {
        out += ch; // незнакомая латинская буква — оставляем
      }
      i += 1;
    }
    return out;
  }

  /* ----------------------------------------------------------------------
     Обход DOM: собираем текстовые узлы статьи, кроме кода и служебных блоков.
     ---------------------------------------------------------------------- */
  var SKIP_TAGS = { CODE: 1, PRE: 1, SCRIPT: 1, STYLE: 1, KBD: 1, SAMP: 1 };
  var SKIP_CLASS = "fx-no-translit";

  // Список преобразованных узлов: { node, latn } — для восстановления латиницы.
  var converted = [];

  function collectTextNodes(root) {
    var nodes = [];
    var walker = document.createTreeWalker(
      root, NodeFilter.SHOW_TEXT,
      {
        acceptNode: function (node) {
          if (!node.nodeValue || !node.nodeValue.trim()) {
            return NodeFilter.FILTER_REJECT;
          }
          var el = node.parentNode;
          while (el && el !== root) {
            if (el.nodeType === 1) {
              if (SKIP_TAGS[el.tagName]) return NodeFilter.FILTER_REJECT;
              if (el.classList && el.classList.contains(SKIP_CLASS)) {
                return NodeFilter.FILTER_REJECT;
              }
            }
            el = el.parentNode;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );
    var n;
    while ((n = walker.nextNode())) nodes.push(n);
    return nodes;
  }

  function applyCyrillic() {
    var article = document.querySelector(".md-content");
    if (!article) return;
    if (converted.length) return; // уже применено
    var nodes = collectTextNodes(article);
    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      var latn = node.nodeValue;
      var cyr = toCyrillic(latn);
      if (cyr !== latn) {
        converted.push({ node: node, latn: latn });
        node.nodeValue = cyr;
      }
    }
  }

  function restoreLatin() {
    for (var i = 0; i < converted.length; i++) {
      converted[i].node.nodeValue = converted[i].latn;
    }
    converted = [];
  }

  function currentMode() {
    try {
      return localStorage.getItem(STORAGE_KEY) === "cyrl" ? "cyrl" : "latn";
    } catch (e) {
      return "latn";
    }
  }

  function setMode(mode) {
    try { localStorage.setItem(STORAGE_KEY, mode); } catch (e) { /* ignore */ }
    if (mode === "cyrl") applyCyrillic();
    else restoreLatin();
    updateToggleUI(mode);
  }

  /* ----------------------------------------------------------------------
     Плавающий переключатель [ Lotin | Кирил ].
     ---------------------------------------------------------------------- */
  var toggleEl = null;

  function buildToggle() {
    if (toggleEl && document.body.contains(toggleEl)) return;
    toggleEl = document.createElement("div");
    toggleEl.className = "fx-script-toggle fx-no-translit";
    toggleEl.setAttribute("role", "group");
    toggleEl.setAttribute("aria-label", "Yozuv: lotin yoki kirill");
    toggleEl.innerHTML =
      '<button type="button" data-mode="latn">Lotin</button>' +
      '<button type="button" data-mode="cyrl">Кирил</button>';
    toggleEl.addEventListener("click", function (ev) {
      var btn = ev.target.closest("button[data-mode]");
      if (!btn) return;
      setMode(btn.getAttribute("data-mode"));
    });
    document.body.appendChild(toggleEl);
  }

  function updateToggleUI(mode) {
    if (!toggleEl) return;
    var btns = toggleEl.querySelectorAll("button[data-mode]");
    for (var i = 0; i < btns.length; i++) {
      var active = btns[i].getAttribute("data-mode") === mode;
      btns[i].classList.toggle("fx-active", active);
      btns[i].setAttribute("aria-pressed", active ? "true" : "false");
    }
  }

  /* ----------------------------------------------------------------------
     Запуск (с поддержкой мгновенной навигации Material через document$).
     ---------------------------------------------------------------------- */
  function onPageReady() {
    // Сбрасываем состояние от предыдущей страницы (узлы уже заменены).
    converted = [];
    if (!isUzLocale()) {
      if (toggleEl) { toggleEl.remove(); toggleEl = null; }
      return;
    }
    buildToggle();
    var mode = currentMode();
    if (mode === "cyrl") applyCyrillic();
    updateToggleUI(mode);
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(onPageReady);
  } else if (document.readyState !== "loading") {
    onPageReady();
  } else {
    document.addEventListener("DOMContentLoaded", onPageReady);
  }
})();
