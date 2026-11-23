/* Карточки из ошибок: промахи экзамена и квизов глав → «вопрос → ответ».
   Пишут exam.js и chapter-quiz.js, читает tools/flashcards*.md (тег mistakes).
   Прогресс — ftk-flash-m-<id>: индексы базовой колоды не сдвигаются. */
(function () {
  "use strict";
  var KEY = "forex_mistake_cards_v1";
  var MAX = 60;
  var STATE = "ftk-flash-m-";

  // id по тексту вопроса: повторный промах не плодит дубли.
  function cardId(q) {
    var h = 5381;
    for (var i = 0; i < q.length; i++) h = ((h * 33) ^ q.charCodeAt(i)) >>> 0;
    return h.toString(36);
  }

  function valid(c) { return !!(c && c.q && c.a); }

  // Свежий промах (и повторный) — в начало колоды.
  function merge(cards, items) {
    items.filter(valid).forEach(function (c) {
      var id = cardId(c.q);
      cards = [{ id: id, q: c.q, a: c.a, explain: c.explain || "", src: c.src || "" }]
        .concat(cards.filter(function (x) { return x.id !== id; }));
    });
    return cards.slice(0, MAX);
  }

  function list() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  }

  // Снова ошибся — прогресс карточки обнуляется; вытесненные лимитом уносят свой.
  function add(items) {
    items = (items || []).filter(valid);
    var before = list();
    var after = merge(before, items);
    var kept = {};
    after.forEach(function (c) { kept[c.id] = 1; });
    try {
      localStorage.setItem(KEY, JSON.stringify(after));
      items.forEach(function (c) { localStorage.removeItem(STATE + cardId(c.q)); });
      before.forEach(function (c) { if (!kept[c.id]) localStorage.removeItem(STATE + c.id); });
    } catch (e) {}
    return items.length;
  }

  function deckUrl() {
    try { return new URL("tools/flashcards/", window.FXW ? window.FXW.siteUrl() : location.href).href; }
    catch (e) { return "#"; }
  }

  window.FXMistakes = { key: KEY, list: list, add: add, deckUrl: deckUrl };
  window.__fxMistakeMerge = merge;
  window.__fxMistakeId = cardId;
})();
