/*
 * Тренажёр чтения DOM (стакана) и ленты — единственный способ научить order
 * flow, а не рассказать о нём.
 *
 * Симуляция честная по устройству сигнала: у раунда есть скрытый «нажим»
 * (latent drift), дисбаланс стакана тянется к нему, а направление тика
 * зависит от текущего дисбаланса. Значит, дисбаланс несёт СЛАБЫЙ, но реальный
 * сигнал — как на живом рынке: угадывается не направление, а вероятность.
 * Счёт за 10 раундов честно показывает: 5/10 — это монетка, а не навык.
 *
 * Раунд: 25 тиков наблюдения (400 мс) → пауза → прогноз на 5 тиков →
 * разбор. Всё синтетическое, реальные котировки не нужны.
 */
(function () {
  var root = document.getElementById("dom-trainer");
  if (!root || !window.FXW) return;

  var F = window.FXW;

  var T = F.pick({
    ru: {
      intro: "Смотри на стакан и ленту. Через 25 тиков лента остановится — угадай, куда уйдут следующие 5.",
      start: "▶ Начать раунд",
      up: "⬆ Рост",
      down: "⬇ Падение",
      decide: "Лента остановлена. Куда пойдут следующие 5 тиков?",
      watching: function (n, total) { return "Тик " + n + " из " + total + " — смотри дисбаланс и принты."; },
      revealing: "Раскрываем 5 тиков…",
      hit: "✅ Угадал",
      miss: "❌ Мимо",
      flat: "➖ Цена осталась на месте — очко никому",
      round: function (n, total) { return "Раунд " + n + " из " + total; },
      score: function (hits, done) { return "Счёт: " + hits + " из " + done; },
      bid: "Bid", ask: "Ask", size: "Объём", price: "Цена", tape: "Лента",
      imbalance: function (v) { return "Дисбаланс бидов: " + v + "%"; },
      verdictGreat: "7+ из 10 — ты читаешь дисбаланс лучше монетки. На живом рынке сигнал слабее: спред и шум съедают почти всё.",
      verdictOk: "5–6 из 10 — на уровне монетки. Это и есть главный урок: стакан даёт вероятность, а не ответ.",
      verdictBad: "4 и меньше — ты либо инвертируешь сигнал, либо угадываешь. Погоняй ещё, глядя на дисбаланс, а не на последний принт.",
      best: function (v) { return "🏆 Лучшая серия: " + v + " из 10"; },
      again: "↻ Новая серия",
      big: "КРУПНЫЙ",
    },
    en: {
      intro: "Watch the book and the tape. After 25 ticks the tape stops — guess where the next 5 will go.",
      start: "▶ Start round",
      up: "⬆ Up",
      down: "⬇ Down",
      decide: "Tape stopped. Where will the next 5 ticks go?",
      watching: function (n, total) { return "Tick " + n + " of " + total + " — watch the imbalance and the prints."; },
      revealing: "Revealing 5 ticks…",
      hit: "✅ Correct",
      miss: "❌ Wrong",
      flat: "➖ Price stayed put — no point for anyone",
      round: function (n, total) { return "Round " + n + " of " + total; },
      score: function (hits, done) { return "Score: " + hits + " of " + done; },
      bid: "Bid", ask: "Ask", size: "Size", price: "Price", tape: "Tape",
      imbalance: function (v) { return "Bid imbalance: " + v + "%"; },
      verdictGreat: "7+ out of 10 — you read imbalance better than a coin. On a live market the signal is weaker: spread and noise eat almost everything.",
      verdictOk: "5–6 out of 10 — coin-flip level. That's the main lesson: the book gives a probability, not an answer.",
      verdictBad: "4 or less — you're either inverting the signal or guessing. Run more rounds, watching the imbalance, not the last print.",
      best: function (v) { return "🏆 Best series: " + v + " of 10"; },
      again: "↻ New series",
      big: "LARGE",
    },
    uz: {
      intro: "Stakan va lentani kuzat. 25 tikdan keyin lenta to'xtaydi — keyingi 5 tik qayerga borishini top.",
      start: "▶ Raundni boshlash",
      up: "⬆ Yuqori",
      down: "⬇ Past",
      decide: "Lenta to'xtadi. Keyingi 5 tik qayerga boradi?",
      watching: function (n, total) { return total + " tikdan " + n + "-tik — disbalans va printlarni kuzat."; },
      revealing: "5 tik ochilmoqda…",
      hit: "✅ To'g'ri",
      miss: "❌ Xato",
      flat: "➖ Narx joyida qoldi — ochko hech kimga yo'q",
      round: function (n, total) { return total + " raunddan " + n + "-raund"; },
      score: function (hits, done) { return done + " tadan " + hits + " ball"; },
      bid: "Bid", ask: "Ask", size: "Hajm", price: "Narx", tape: "Lenta",
      imbalance: function (v) { return "Bid disbalansi: " + v + "%"; },
      verdictGreat: "10 tadan 7+ — disbalansni tangadan yaxshi o'qiysan. Jonli bozorda signal zaifroq: spred va shovqin deyarli hammasini yeydi.",
      verdictOk: "10 tadan 5–6 — tanga darajasi. Asosiy saboq shundaki, stakan javob emas, ehtimol beradi.",
      verdictBad: "4 va kam — signalni teskari o'qiyapsan yoki taxmin qilyapsan. Oxirgi printga emas, disbalansga qarab yana mashq qil.",
      best: function (v) { return "🏆 Eng yaxshi seriya: 10 tadan " + v; },
      again: "↻ Yangi seriya",
      big: "YIRIK",
    },
  });

  var TICK_MS = 400;
  var WATCH_TICKS = 25;
  var REVEAL_TICKS = 5;
  var ROUNDS = 10;
  var LEVELS = 5;
  var STORE_KEY = "ftk_dom_best";

  var style = document.createElement("style");
  style.textContent = [
    "#dom-trainer{max-width:860px;margin:1.2rem 0}",
    ".dom-grid{display:grid;grid-template-columns:1fr 1fr;gap:.8rem}",
    "@media(max-width:640px){.dom-grid{grid-template-columns:1fr}}",
    ".dom-panel{border:1px solid var(--md-default-fg-color--lighter);border-radius:9px;padding:.6rem .7rem;background:var(--md-code-bg-color)}",
    ".dom-title{font-size:.78rem;font-weight:700;color:var(--md-default-fg-color--light);margin-bottom:.35rem}",
    ".dom-book{width:100%;border-collapse:collapse;font-size:.78rem;font-variant-numeric:tabular-nums}",
    ".dom-book td{padding:.14rem .3rem;position:relative}",
    ".dom-ask-row td{background:rgba(248,113,113,.10)}",
    ".dom-bid-row td{background:rgba(45,212,191,.10)}",
    ".dom-spread td{text-align:center;font-size:.7rem;color:var(--md-default-fg-color--light);padding:.2rem}",
    ".dom-bar{position:absolute;top:2px;bottom:2px;right:0;background:currentColor;opacity:.18;pointer-events:none}",
    ".dom-size{text-align:right;position:relative}",
    ".dom-tape{list-style:none;margin:0;padding:0;max-height:220px;overflow:hidden;font-size:.76rem;font-variant-numeric:tabular-nums}",
    ".dom-tape li{display:flex;justify-content:space-between;padding:.1rem .3rem;border-radius:3px}",
    ".dom-tape .dom-buy{color:#2dd4bf}",
    ".dom-tape .dom-sell{color:#f87171}",
    ".dom-tape .dom-big{font-weight:800;border:1px solid currentColor}",
    ".dom-status{min-height:1.3rem;font-size:.84rem;margin:.55rem 0;font-weight:600}",
    ".dom-controls{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center}",
    ".dom-btn{padding:.5rem 1.1rem;border-radius:6px;border:1px solid transparent;cursor:pointer;font-weight:700;font-size:.92rem}",
    ".dom-btn:disabled{opacity:.4;cursor:not-allowed}",
    ".dom-start{background:#3b82f6;color:#fff}",
    ".dom-up{background:#2dd4bf;color:#0d1117}",
    ".dom-down{background:#f87171;color:#fff}",
    ".dom-meta{display:flex;justify-content:space-between;font-size:.78rem;color:var(--md-default-fg-color--light);margin-top:.5rem;flex-wrap:wrap;gap:.3rem}",
    ".dom-verdict{margin-top:.7rem;padding:.7rem .9rem;border-left:3px solid #8b5cf6;background:rgba(139,92,246,.08);font-size:.88rem}",
    ".dom-result-hit{color:#2dd4bf}.dom-result-miss{color:#f87171}.dom-result-flat{color:#9ca3af}",
  ].join("");
  document.head.appendChild(style);

  var state = null; // {drift, mid, ticks[], tape[], round, hits, phase}
  var timer = null;
  var best = 0;
  try { best = Number(localStorage.getItem(STORE_KEY)) || 0; } catch (e) {}

  function rnd(min, max) { return min + Math.random() * (max - min); }

  function newRound(round, hits) {
    return {
      drift: Math.random() < 0.5 ? -1 : 1,
      mid: 100,
      imbalance: 0.5, // доля бида в суммарном объёме
      tick: 0,
      tape: [],
      round: round,
      hits: hits,
      phase: "watch", // watch → decide → reveal → done
      prediction: null,
      result: null,
    };
  }

  function bookSizes() {
    // Дисбаланс тянется к скрытому нажиму — сигнал слабый, но настоящий.
    var target = 0.5 + 0.3 * state.drift;
    state.imbalance = Math.min(0.9, Math.max(0.1,
      0.7 * state.imbalance + 0.3 * target + rnd(-0.07, 0.07)));
    var totalBid = 1000 * state.imbalance;
    var totalAsk = 1000 * (1 - state.imbalance);
    var bids = [], asks = [];
    for (var i = 0; i < LEVELS; i++) {
      bids.push(Math.round(totalBid / LEVELS * rnd(0.5, 1.5)));
      asks.push(Math.round(totalAsk / LEVELS * rnd(0.5, 1.5)));
    }
    return { bids: bids, asks: asks };
  }

  function stepTick() {
    var book = bookSizes();
    // Направление тика зависит от дисбаланса: 0.35 + 0.3·I ∈ [0.38, 0.62].
    var up = Math.random() < 0.35 + 0.3 * state.imbalance;
    state.mid += up ? 1 : -1;
    var size = Math.round(rnd(5, 120));
    if (Math.random() < 0.06) size = Math.round(rnd(250, 500)); // крупный принт
    state.tape.unshift({ up: up, size: size, price: state.mid });
    if (state.tape.length > 14) state.tape.pop();
    state.tick++;
    render(book);
  }

  function stopTimer() {
    if (timer !== null) {
      clearInterval(timer);
      timer = null;
    }
  }

  function startRound(round, hits) {
    stopTimer();
    state = newRound(round, hits);
    timer = setInterval(function () {
      if (state.phase === "watch") {
        stepTick();
        if (state.tick >= WATCH_TICKS) {
          state.phase = "decide";
          stopTimer();
          render(bookSizes.current || null);
        }
      } else if (state.phase === "reveal") {
        stepTick();
        if (state.tick >= WATCH_TICKS + REVEAL_TICKS) {
          stopTimer();
          finishRound();
        }
      }
    }, TICK_MS);
  }

  function finishRound() {
    var last = state.tape.slice(0, REVEAL_TICKS);
    var move = last.length ? last[0].price - last[last.length - 1].price : 0;
    var hit = (move > 0 && state.prediction === "up") ||
              (move < 0 && state.prediction === "down");
    state.result = move === 0 ? "flat" : hit ? "hit" : "miss";
    if (state.result === "hit") state.hits++;
    state.phase = "done";
    if (state.round >= ROUNDS) {
      if (state.hits > best) {
        best = state.hits;
        try { localStorage.setItem(STORE_KEY, String(best)); } catch (e) {}
      }
    }
    render(null);
  }

  function esc(s) { return F.escape(s); }

  function render(book) {
    if (!book) book = bookSizes();
    var asks = book.asks.slice().reverse();
    var maxSize = Math.max.apply(null, book.bids.concat(book.asks));

    var bookRows =
      asks.map(function (size, i) {
        var price = state.mid + (LEVELS - i);
        return '<tr class="dom-ask-row"><td class="dom-size">' + size +
          '<span class="dom-bar" style="width:' + Math.round(size / maxSize * 60) + 'px"></span></td><td>' +
          price.toFixed(1) + "</td></tr>";
      }).join("") +
      '<tr class="dom-spread"><td colspan="2">— ' + state.mid.toFixed(1) + " —</td></tr>" +
      book.bids.map(function (size, i) {
        var price = state.mid - (i + 1);
        return '<tr class="dom-bid-row"><td class="dom-size">' + size +
          '<span class="dom-bar" style="width:' + Math.round(size / maxSize * 60) + 'px"></span></td><td>' +
          price.toFixed(1) + "</td></tr>";
      }).join("");

    var tapeRows = state.tape.map(function (print) {
      return '<li class="' + (print.size >= 250 ? "dom-big " : "") +
        (print.up ? "dom-buy" : "dom-sell") + '"><span>' + print.price.toFixed(1) +
        "</span><span>" + print.size + (print.size >= 250 ? " · " + esc(T.big) : "") + "</span></li>";
    }).join("");

    var status = "";
    if (state.phase === "watch") status = T.watching(state.tick, WATCH_TICKS);
    else if (state.phase === "decide") status = T.decide;
    else if (state.phase === "reveal") status = T.revealing;
    else if (state.phase === "done") {
      var label = state.result === "hit" ? T.hit : state.result === "miss" ? T.miss : T.flat;
      var cls = state.result === "hit" ? "dom-result-hit" : state.result === "miss" ? "dom-result-miss" : "dom-result-flat";
      status = '<span class="' + cls + '">' + esc(label) + "</span>";
    }

    var verdict = "";
    if (state.phase === "done" && state.round >= ROUNDS) {
      var text = state.hits >= 7 ? T.verdictGreat : state.hits >= 5 ? T.verdictOk : T.verdictBad;
      verdict = '<div class="dom-verdict">' + esc(text) + "</div>";
    }

    root.innerHTML =
      '<div class="dom-grid">' +
      '<div class="dom-panel"><div class="dom-title">' + esc(T.bid) + " / " + esc(T.ask) +
      " · " + esc(T.imbalance(Math.round(state.imbalance * 100))) + "</div>" +
      '<table class="dom-book"><tbody>' + bookRows + "</tbody></table></div>" +
      '<div class="dom-panel"><div class="dom-title">' + esc(T.tape) + " · " + esc(T.price) + " / " + esc(T.size) + "</div>" +
      '<ul class="dom-tape">' + tapeRows + "</ul></div>" +
      "</div>" +
      '<div class="dom-status" id="dom-status">' + status + "</div>" +
      '<div class="dom-controls">' +
      '<button class="dom-btn dom-up" id="dom-up" ' + (state.phase === "decide" ? "" : "disabled") + ">" + esc(T.up) + "</button>" +
      '<button class="dom-btn dom-down" id="dom-down" ' + (state.phase === "decide" ? "" : "disabled") + ">" + esc(T.down) + "</button>" +
      (state.phase === "done"
        ? '<button class="dom-btn dom-start" id="dom-next">' +
          esc(state.round >= ROUNDS ? T.again : T.start) + "</button>"
        : "") +
      "</div>" +
      '<div class="dom-meta"><span>' + esc(T.round(state.round, ROUNDS)) + "</span><span>" +
      esc(T.score(state.hits, state.phase === "done" ? state.round : state.round - 1)) +
      (best ? " · " + esc(T.best(best)) : "") + "</span></div>" +
      verdict;

    document.getElementById("dom-up").addEventListener("click", function () { predict("up"); });
    document.getElementById("dom-down").addEventListener("click", function () { predict("down"); });
    var next = document.getElementById("dom-next");
    if (next) {
      next.addEventListener("click", function () {
        if (state.round >= ROUNDS) startRound(1, 0);
        else startRound(state.round + 1, state.hits);
      });
    }
  }

  function predict(direction) {
    if (state.phase !== "decide") return;
    state.prediction = direction;
    state.phase = "reveal";
    render(null);
    timer = setInterval(function () {
      stepTick();
      if (state.tick >= WATCH_TICKS + REVEAL_TICKS) {
        stopTimer();
        finishRound();
      }
    }, TICK_MS);
  }

  // Стартовый экран.
  root.innerHTML =
    "<p>" + esc(T.intro) + "</p>" +
    '<div class="dom-controls"><button class="dom-btn dom-start" id="dom-first">' +
    esc(T.start) + "</button>" +
    (best ? '<span class="dom-meta">' + esc(T.best(best)) + "</span>" : "") +
    "</div>";
  document.getElementById("dom-first").addEventListener("click", function () {
    startRound(1, 0);
  });
})();
