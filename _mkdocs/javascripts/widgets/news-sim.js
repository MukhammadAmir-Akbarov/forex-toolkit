/*
 * Симулятор новостей: «выходит NFP, у тебя открыта позиция» → выбор действия →
 * разбор по протоколу (practice/news-trading-protocol.md) и типичная реакция
 * рынка с историческим примером.
 *
 * Сценарии — JSON-блок #ns-scenarios на странице (переведён в каждой локали,
 * как банк экзамена); строки интерфейса — здесь. Варианты перемешиваются на
 * каждую попытку, чтобы ход запоминали по смыслу, а не по позиции кнопки.
 *
 * Оценка: лучший ход по протоколу — 2 балла, допустимый — 1, опасный — 0.
 * Опасные ходы уходят в карточки из ошибок (FXMistakes), лучший процент —
 * в ftk_news_best.
 */
(function () {
  var root = document.getElementById("ns-widget");
  var POINTS = { best: 2, ok: 1, bad: 0 };
  var STORE_KEY = "ftk_news_best";

  // answers: вердикты выбранных ходов ("best" | "ok" | "bad").
  function score(answers) {
    var points = answers.reduce(function (s, v) { return s + (POINTS[v] || 0); }, 0);
    var max = answers.length * 2;
    var pct = max ? Math.round((points / max) * 100) : 0;
    return { points: points, max: max, pct: pct, tier: pct >= 80 ? "ready" : pct >= 50 ? "almost" : "early" };
  }
  window.__fxNewsScore = score;

  if (!root || !window.FXW) return;
  var F = window.FXW;
  var bank;
  try { bank = JSON.parse(document.getElementById("ns-scenarios").textContent); } catch (e) { return; }
  if (!Array.isArray(bank) || !bank.length) return;
  // Вердикт идёт в имя CSS-класса: в разметку попадает только литерал из кода,
  // а не текст страницы (CodeQL js/xss-through-dom считает весь банк из
  // JSON.parse заражённым, и переприсваивание поля его не «очищает»).
  function kind(v) { return v === "best" ? "best" : v === "ok" ? "ok" : "bad"; }

  var T = F.pick({
    ru: {
      start: "▶ Начать симуляцию",
      counter: function (i, n) { return "Сценарий " + i + " из " + n; },
      verdict: { best: "✅ Лучший ход по протоколу", ok: "🟡 Допустимо, но с риском", bad: "❌ Опасный ход" },
      bestWas: "Лучший ход",
      reaction: "📈 Как обычно реагирует рынок",
      history: "📜 Из истории",
      next: "Дальше →",
      result: "Итог",
      score: function (p, m, pct) { return "Результат: " + p + " из " + m + " баллов (" + pct + "%)"; },
      tier: {
        ready: "Протокол в голове: на новостях ты защищаешь счёт, а не играешь в рулетку.",
        almost: "Почти. Перечитай протокол там, где ошибся, и пройди ещё раз.",
        early: "Пока рано торговать на новостях: только демо и наблюдение за релизами."
      },
      best: function (p) { return "🏆 Лучший результат: " + p + "%"; },
      protocol: "Протокол торговли на новостях →",
      mistakes: function (n) { return "🔁 Опасные ходы добавлены во флеш-карточки: " + n + "."; },
      mistakesLink: "Повторить →",
      again: "↻ Пройти ещё раз"
    },
    en: {
      start: "▶ Start the simulation",
      counter: function (i, n) { return "Scenario " + i + " of " + n; },
      verdict: { best: "✅ Best move by the protocol", ok: "🟡 Acceptable, but risky", bad: "❌ Dangerous move" },
      bestWas: "Best move",
      reaction: "📈 How the market usually reacts",
      history: "📜 From history",
      next: "Next →",
      result: "Result",
      score: function (p, m, pct) { return "Score: " + p + " of " + m + " points (" + pct + "%)"; },
      tier: {
        ready: "You know the protocol: around news you protect the account instead of playing roulette.",
        almost: "Almost. Re-read the protocol where you slipped and run it again.",
        early: "Too early to trade the news: demo only, and watch the releases."
      },
      best: function (p) { return "🏆 Best result: " + p + "%"; },
      protocol: "News trading protocol →",
      mistakes: function (n) { return "🔁 Dangerous moves added to your flashcards: " + n + "."; },
      mistakesLink: "Review them →",
      again: "↻ Run it again"
    },
    uz: {
      start: "▶ Simulyatsiyani boshlash",
      counter: function (i, n) { return n + " tadan " + i + "-ssenariy"; },
      verdict: { best: "✅ Protokol bo'yicha eng yaxshi harakat", ok: "🟡 Mumkin, lekin xavfli", bad: "❌ Xavfli harakat" },
      bestWas: "Eng yaxshi harakat",
      reaction: "📈 Bozor odatda qanday reaksiya qiladi",
      history: "📜 Tarixdan",
      next: "Keyingi →",
      result: "Natija",
      score: function (p, m, pct) { return "Natija: " + m + " balldan " + p + " (" + pct + "%)"; },
      tier: {
        ready: "Protokol yodingizda: yangiliklarda siz ruletka o'ynamaysiz, hisobni himoya qilasiz.",
        almost: "Deyarli. Xato qilgan joylaringizda protokolni qayta o'qing va yana o'ting.",
        early: "Yangiliklarda savdo qilishga hali erta: faqat demo va relizlarni kuzatish."
      },
      best: function (p) { return "🏆 Eng yaxshi natija: " + p + "%"; },
      protocol: "Yangiliklarda savdo protokoli →",
      mistakes: function (n) { return "🔁 Xavfli harakatlar flesh-kartochkalarga qo'shildi: " + n + " ta."; },
      mistakesLink: "Takrorlash →",
      again: "↻ Yana o'tish"
    }
  });

  var style = document.createElement("style");
  style.textContent = [
    "#ns-widget{margin:1.2rem 0;padding:1rem 1.1rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:12px;background:var(--md-code-bg-color)}",
    ".ns-meta{font-size:.8rem;color:var(--md-default-fg-color--light);margin-bottom:.4rem}",
    ".ns-event{font-weight:800;font-size:1.05rem;margin:.2rem 0 .5rem}",
    ".ns-situation{margin:.3rem 0 .8rem}",
    ".ns-options{display:grid;gap:.55rem}",
    ".ns-opt{padding:.7rem .9rem;border-radius:8px;cursor:pointer;text-align:left;font:inherit;line-height:1.4;color:inherit;border:1px solid var(--md-default-fg-color--lighter);background:var(--md-default-bg-color)}",
    ".ns-opt:not(:disabled):hover{border-color:#3b82f6}",
    ".ns-opt:disabled{cursor:default}",
    ".ns-opt.ns-best{border-color:#22c55e;background:rgba(34,197,94,.12)}",
    ".ns-opt.ns-ok{border-color:#f59e0b;background:rgba(245,158,11,.10)}",
    ".ns-opt.ns-bad{border-color:#f87171;background:rgba(248,113,113,.10)}",
    ".ns-opt.ns-picked{box-shadow:0 0 0 2px var(--md-default-fg-color)}",
    ".ns-box{margin-top:.8rem;padding:.7rem .9rem;border-left:3px solid #3b82f6;background:rgba(59,130,246,.07);border-radius:0 8px 8px 0}",
    ".ns-box p{margin:.35rem 0}.ns-box h4{margin:.1rem 0 .3rem}",
    ".ns-v-best{border-left-color:#22c55e}.ns-v-ok{border-left-color:#f59e0b}.ns-v-bad{border-left-color:#f87171}",
    ".ns-btn{margin-top:.9rem;padding:.55rem 1.2rem;border-radius:6px;border:none;cursor:pointer;font-weight:700;font-size:.95rem;background:#3b82f6;color:#fff}"
  ].join("");
  document.head.appendChild(style);

  function shuffled(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function readBest() {
    try { return Number(localStorage.getItem(STORE_KEY)) || 0; } catch (e) { return 0; }
  }

  var idx = 0;
  var options = [];
  var answers = [];
  var missed = [];

  function startScreen() {
    var best = readBest();
    root.innerHTML =
      (best ? '<p class="ns-meta">' + F.escape(T.best(best)) + "</p>" : "") +
      '<button type="button" class="ns-btn" id="ns-start">' + F.escape(T.start) + "</button>";
    document.getElementById("ns-start").addEventListener("click", start);
  }

  function start() {
    idx = 0;
    answers = [];
    missed = [];
    ask();
  }

  function head(sc) {
    return '<div class="ns-meta">' + F.escape(T.counter(idx + 1, bank.length)) + "</div>" +
      '<div class="ns-event">' + F.escape(sc.event) + "</div>" +
      '<p class="ns-situation">' + F.escape(sc.situation) + "</p>";
  }

  function ask() {
    var sc = bank[idx];
    options = shuffled(sc.options);
    root.innerHTML = head(sc) + '<div class="ns-options">' + options.map(function (o, i) {
      return '<button type="button" class="ns-opt" data-i="' + i + '">' + F.escape(o.text) + "</button>";
    }).join("") + "</div>";
    Array.prototype.forEach.call(root.querySelectorAll(".ns-opt"), function (btn) {
      btn.addEventListener("click", function () { answer(Number(btn.getAttribute("data-i"))); });
    });
  }

  function answer(i) {
    var sc = bank[idx];
    var picked = options[i];
    var best = options.filter(function (o) { return o.verdict === "best"; })[0];
    answers.push(kind(picked.verdict));
    if (kind(picked.verdict) === "bad" && best) {
      missed.push({ q: sc.event + " — " + sc.situation, a: best.text, explain: best.why, src: "news" });
    }
    root.innerHTML = head(sc) + '<div class="ns-options">' + options.map(function (o, j) {
      return '<button type="button" class="ns-opt ns-' + kind(o.verdict) + (j === i ? " ns-picked" : "") + '" disabled>' +
        F.escape(o.text) + "</button>";
    }).join("") + "</div>" +
      '<div class="ns-box ns-v-' + kind(picked.verdict) + '" aria-live="polite"><p><strong>' + F.escape(T.verdict[kind(picked.verdict)]) +
      ".</strong> " + F.escape(picked.why) + "</p>" +
      (picked !== best && best
        ? "<p><strong>" + F.escape(T.bestWas) + ":</strong> " + F.escape(best.text) + " — " + F.escape(best.why) + "</p>"
        : "") + "</div>" +
      '<div class="ns-box"><h4>' + F.escape(T.reaction) + "</h4><p>" + F.escape(sc.reaction) + "</p>" +
      "<p><strong>" + F.escape(T.history) + ":</strong> " + F.escape(sc.history) + "</p></div>" +
      '<button type="button" class="ns-btn" id="ns-next">' + F.escape(idx + 1 < bank.length ? T.next : T.result) + "</button>";
    document.getElementById("ns-next").addEventListener("click", function () {
      idx++;
      if (idx < bank.length) ask(); else finish();
    });
  }

  function finish() {
    var s = score(answers);
    var best = Math.max(readBest(), s.pct);
    try { localStorage.setItem(STORE_KEY, String(best)); } catch (e) {}
    var saved = missed.length && window.FXMistakes ? window.FXMistakes.add(missed) : 0;
    if (window.fxActivity) window.fxActivity();
    if (window.fxTrack) window.fxTrack("news_sim_completed");
    var protocol = new URL("practice/news-trading-protocol/", F.siteUrl()).href;
    root.innerHTML =
      '<div class="ns-event">' + F.escape(T.score(s.points, s.max, s.pct)) + "</div>" +
      '<div class="ns-box ns-v-' + (s.tier === "ready" ? "best" : s.tier === "almost" ? "ok" : "bad") + '"><p>' +
      F.escape(T.tier[s.tier]) + "</p></div>" +
      '<p class="ns-meta">' + F.escape(T.best(best)) + "</p>" +
      (saved ? "<p>" + F.escape(T.mistakes(saved)) + ' <a href="' + F.escape(window.FXMistakes.deckUrl()) + '">' +
        F.escape(T.mistakesLink) + "</a></p>" : "") +
      '<p><a href="' + F.escape(protocol) + '">' + F.escape(T.protocol) + "</a></p>" +
      '<button type="button" class="ns-btn" id="ns-again">' + F.escape(T.again) + "</button>";
    document.getElementById("ns-again").addEventListener("click", start);
  }

  startScreen();
})();
