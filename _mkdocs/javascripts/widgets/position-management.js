/*
 * Что делать, пока сделка открыта: безубыток, частичное закрытие, трейл.
 *
 * Путь ученика был закрыт с обеих сторон и пуст посередине: «Перед сделкой»
 * считает риск, журнал разбирает результат, а решения принимаются между ними.
 * Журнал за перенос стопа ставит нарушение и выдаёт задачу — тренировать
 * причину было нечем.
 *
 * Тренажёр не учит «всегда переноси в безубыток». Он даёт выбрать план и сразу
 * показывает два числа: что вышло на этой сделке и что тот же план дал на всех
 * 80 эпизодах архива в обе стороны. Часто выясняется, что план навредил.
 *
 * Расчёт — зеркало forex_toolkit/position_management.py, включая
 * консервативные правила: внутри свечи первым проверяется стоп, срабатывания
 * считаются после него, R измеряется от первоначального риска.
 */
(function () {
  var root = document.getElementById("position-management");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var CTX = 30; // свечей контекста, дальше идёт ведение

  var T = F.pick({
    ru: {
      loading: "Загружаю архивные сделки…",
      loadError: "Не удалось загрузить эпизоды. Обнови страницу.",
      setup: function (pair, tf, dir) {
        return "Сделка уже открыта: " + pair + " " + tf + ", " +
          (dir === "long" ? "покупка" : "продажа") +
          ". Стоп — одна ATR, цель — 2R. Дальше 15 свечей.";
      },
      task: "Что делаешь с открытой позицией?",
      plans: {
        hold: "Ничего — держу до стопа или цели",
        be: "Перенесу стоп в безубыток на +1R",
        partial: "Закрою половину на +1R",
        trail: "Буду тянуть стоп в 1R за ценой",
      },
      thisTrade: "На этой сделке",
      yours: function (value) { return "Твой план дал " + value + "."; },
      plain: function (value) { return "Просто держать дало бы " + value + "."; },
      betterHere: "Здесь управление помогло.",
      worseHere: "Здесь управление навредило.",
      sameHere: "Здесь разницы не было.",
      overall: "А теперь то же самое на всех сделках архива",
      overallLine: function (n, plain, managed) {
        return n + " сделок: держать — " + plain + ", твой план — " + managed + ".";
      },
      counts: function (helped, hurt, same) {
        return "Помог в " + helped + " случаях, навредил в " + hurt +
          ", не изменил ничего в " + same + ".";
      },
      lessonGood: "На этом архиве план в сумме помог. Это не значит, что он поможет всегда.",
      lessonBad: "На этом архиве план в сумме навредил — чаще всего он режет прибыль раньше, чем спасает от убытка.",
      lessonFlat: "На этом архиве план почти ничего не изменил.",
      note: "Правило подсчёта: если свеча задела и стоп, и цель, засчитывается стоп — порядок движения внутри свечи неизвестен.",
      next: "Другая сделка →",
    },
    en: {
      loading: "Loading archive trades…",
      loadError: "Could not load the episodes. Refresh the page.",
      setup: function (pair, tf, dir) {
        return "The trade is already open: " + pair + " " + tf + ", " +
          (dir === "long" ? "long" : "short") +
          ". Stop is one ATR, target is 2R. Fifteen candles to go.";
      },
      task: "What do you do with the open position?",
      plans: {
        hold: "Nothing — hold to stop or target",
        be: "Move the stop to breakeven at +1R",
        partial: "Close half at +1R",
        trail: "Trail the stop 1R behind price",
      },
      thisTrade: "On this trade",
      yours: function (value) { return "Your plan gave " + value + "."; },
      plain: function (value) { return "Just holding would have given " + value + "."; },
      betterHere: "Here the management helped.",
      worseHere: "Here the management hurt.",
      sameHere: "Here it made no difference.",
      overall: "Now the same thing across every trade in the archive",
      overallLine: function (n, plain, managed) {
        return n + " trades: holding — " + plain + ", your plan — " + managed + ".";
      },
      counts: function (helped, hurt, same) {
        return "Helped in " + helped + " cases, hurt in " + hurt +
          ", changed nothing in " + same + ".";
      },
      lessonGood: "On this archive the plan helped in total. That does not mean it always will.",
      lessonBad: "On this archive the plan hurt in total — it usually cuts profit sooner than it saves from a loss.",
      lessonFlat: "On this archive the plan changed almost nothing.",
      note: "Counting rule: if a candle touched both the stop and the target, the stop counts — the order inside a candle is unknown.",
      next: "Another trade →",
    },
    uz: {
      loading: "Arxiv savdolari yuklanmoqda…",
      loadError: "Epizodlarni yuklab bo'lmadi. Sahifani yangilang.",
      setup: function (pair, tf, dir) {
        return "Savdo allaqachon ochiq: " + pair + " " + tf + ", " +
          (dir === "long" ? "sotib olish" : "sotish") +
          ". Stop — bitta ATR, maqsad — 2R. Oldinda 15 ta sham.";
      },
      task: "Ochiq pozitsiya bilan nima qilasiz?",
      plans: {
        hold: "Hech narsa — stop yoki maqsadgacha ushlayman",
        be: "+1R da stopni zararsizlikka ko'chiraman",
        partial: "+1R da yarmini yopaman",
        trail: "Stopni narxdan 1R orqada tortaman",
      },
      thisTrade: "Bu savdoda",
      yours: function (value) { return "Sizning rejangiz " + value + " berdi."; },
      plain: function (value) { return "Shunchaki ushlash " + value + " bergan bo'lardi."; },
      betterHere: "Bu yerda boshqaruv yordam berdi.",
      worseHere: "Bu yerda boshqaruv zarar keltirdi.",
      sameHere: "Bu yerda farq bo'lmadi.",
      overall: "Endi xuddi shuni arxivdagi barcha savdolarda",
      overallLine: function (n, plain, managed) {
        return n + " savdo: ushlash — " + plain + ", sizning reja — " + managed + ".";
      },
      counts: function (helped, hurt, same) {
        return helped + " holatda yordam berdi, " + hurt + " holatda zarar qildi, " +
          same + " holatda hech narsani o'zgartirmadi.";
      },
      lessonGood: "Bu arxivda reja jami yordam berdi. Bu doim yordam beradi degani emas.",
      lessonBad: "Bu arxivda reja jami zarar qildi — u ko'pincha zarardan qutqarishdan ko'ra foydani erta kesadi.",
      lessonFlat: "Bu arxivda reja deyarli hech narsani o'zgartirmadi.",
      note: "Hisoblash qoidasi: sham stopga ham, maqsadga ham tekkan bo'lsa, stop hisoblanadi — sham ichidagi harakat tartibi noma'lum.",
      next: "Boshqa savdo →",
    },
  });

  // ── Расчёт: зеркало forex_toolkit/position_management.py ─────────────────

  function rOf(price, entry, risk, direction) {
    if (risk <= 0) return 0;
    return direction === "long" ? (price - entry) / risk : (entry - price) / risk;
  }

  function simulate(candles, options) {
    var entryIndex = options.entryIndex;
    var entry = options.entry, stop0 = options.stop, take = options.take;
    var direction = options.direction || "long";
    var plan = options.plan || {};
    var risk = Math.abs(entry - stop0);
    if (risk <= 0 || entryIndex + 1 >= candles.length) return null;

    var stop = stop0, remaining = 1, booked = 0;
    var partialTaken = false, movedToBreakeven = false, trailed = false;
    var best = 0, reason = "timeout", bars = 0;

    for (var i = entryIndex + 1; i < candles.length; i++) {
      var candle = candles[i];
      bars = i - entryIndex;
      var high = Number(candle.high), low = Number(candle.low);
      var adverse = direction === "long" ? low : high;
      var favourable = direction === "long" ? high : low;

      var hitStop = direction === "long" ? adverse <= stop : adverse >= stop;
      if (hitStop) {
        booked += remaining * rOf(stop, entry, risk, direction);
        remaining = 0;
        reason = stopReason(partialTaken, movedToBreakeven, trailed);
        break;
      }

      var hitTake = direction === "long" ? favourable >= take : favourable <= take;
      if (hitTake) {
        booked += remaining * rOf(take, entry, risk, direction);
        remaining = 0;
        reason = "take";
        break;
      }

      var reached = rOf(favourable, entry, risk, direction);
      if (reached > best) best = reached;

      if (plan.partial_at != null && !partialTaken && reached >= plan.partial_at) {
        var part = Math.max(0, Math.min(1, plan.partial_fraction == null ? 0.5 : plan.partial_fraction));
        booked += remaining * part * plan.partial_at;
        remaining *= 1 - part;
        partialTaken = true;
      }

      if (plan.breakeven_at != null && !movedToBreakeven && reached >= plan.breakeven_at) {
        stop = entry;
        movedToBreakeven = true;
      }

      if (plan.trail_r != null && best > plan.trail_r) {
        var level = direction === "long"
          ? entry + (best - plan.trail_r) * risk
          : entry - (best - plan.trail_r) * risk;
        var better = direction === "long" ? level > stop : level < stop;
        if (better) { stop = level; trailed = true; }
      }

      if (remaining <= 0) { reason = "partial"; break; }
    }

    if (remaining > 0 && reason === "timeout") {
      booked += remaining * rOf(Number(candles[candles.length - 1].close), entry, risk, direction);
    }

    return {
      total_r: booked,
      reason: reason,
      bars: bars,
      partial_taken: partialTaken,
      moved_to_breakeven: movedToBreakeven,
      max_favourable_r: best,
    };
  }

  function stopReason(partial, breakeven, trailed) {
    var tail = trailed ? "trail" : breakeven ? "breakeven" : "stop";
    return partial ? "partial+" + tail : tail;
  }

  function compare(candles, options) {
    var plainOptions = {};
    Object.keys(options).forEach(function (k) { plainOptions[k] = options[k]; });
    plainOptions.plan = {};
    var plain = simulate(candles, plainOptions);
    var managed = simulate(candles, options);
    if (!plain || !managed) return null;
    return {
      plain: plain,
      managed: managed,
      difference: managed.total_r - plain.total_r,
      helped: managed.total_r - plain.total_r > 0,
    };
  }

  function summarize(list) {
    if (!list.length) return null;
    var plain = 0, managed = 0, helped = 0, hurt = 0, same = 0;
    list.forEach(function (c) {
      plain += c.plain.total_r;
      managed += c.managed.total_r;
      if (c.difference > 1e-9) helped++;
      else if (c.difference < -1e-9) hurt++;
      else same++;
    });
    return {
      trades: list.length,
      plain_total: plain,
      managed_total: managed,
      difference: managed - plain,
      helped: helped,
      hurt: hurt,
      same: same,
    };
  }

  window.__fxManagePosition = simulate;
  window.__fxComparePosition = compare;
  window.__fxManageVerdict = summarize;

  // ── Страница ────────────────────────────────────────────────────────────

  var PLANS = {
    hold: {},
    be: { breakeven_at: 1 },
    partial: { partial_at: 1, partial_fraction: 0.5 },
    trail: { trail_r: 1 },
  };

  var episodes = [], current = 0, answered = null;

  root.innerHTML = '<p id="pm-loading">' + F.escape(T.loading) + "</p>";

  fetch(root.getAttribute("data-src"))
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (document_) {
      episodes = (document_.episodes || []).map(decode);
      if (!episodes.length) throw new Error("empty");
      current = Math.floor(Math.random() * episodes.length);
      render();
    })
    .catch(function () {
      root.innerHTML =
        '<p class="calc-result calc-error">' + F.escape(T.loadError) + "</p>";
    });

  function decode(episode) {
    var base = episode.base, pip = episode.pip;
    var candles = episode.k.map(function (c) {
      return {
        open: base + c[0] * pip,
        high: base + c[1] * pip,
        low: base + c[2] * pip,
        close: base + c[3] * pip,
      };
    });
    return {
      pair: episode.pair,
      tf: episode.tf,
      candles: candles,
      risk: episode.atr * pip,
      entryIndex: CTX - 1,
    };
  }

  function tradeOf(episode, direction) {
    var entry = episode.candles[episode.entryIndex].close;
    var risk = episode.risk;
    return {
      entryIndex: episode.entryIndex,
      entry: entry,
      stop: direction === "long" ? entry - risk : entry + risk,
      take: direction === "long" ? entry + 2 * risk : entry - 2 * risk,
      direction: direction,
    };
  }

  function r(value) {
    return (value >= 0 ? "+" : "") + value.toFixed(2) + "R";
  }

  function render() {
    var episode = episodes[current];
    var direction = current % 2 === 0 ? "long" : "short";
    var buttons = Object.keys(PLANS)
      .map(function (key) {
        return '<button type="button" class="pm-plan" data-key="' + key + '">' +
          F.escape(T.plans[key]) + "</button>";
      })
      .join("");

    root.innerHTML =
      "<p>" + F.escape(T.setup(episode.pair, episode.tf, direction)) + "</p>" +
      (answered === null
        ? "<p><strong>" + F.escape(T.task) + "</strong></p>" +
          '<div class="pm-plans">' + buttons + "</div>"
        : "") +
      '<div id="pm-verdict" role="status" aria-live="polite"></div>';

    root.querySelectorAll(".pm-plan").forEach(function (button) {
      button.addEventListener("click", function () {
        answered = button.getAttribute("data-key");
        render();
        reveal(episode, direction, answered);
      });
    });
  }

  function reveal(episode, direction, key) {
    var plan = PLANS[key];
    var trade = tradeOf(episode, direction);
    var here = compare(episode.candles, {
      entryIndex: trade.entryIndex,
      entry: trade.entry,
      stop: trade.stop,
      take: trade.take,
      direction: direction,
      plan: plan,
    });

    // Тот же план на всех эпизодах и в обе стороны — иначе вывод зависел бы
    // от того, какая сделка попалась, и от перекоса в одну сторону.
    var all = [];
    episodes.forEach(function (item) {
      ["long", "short"].forEach(function (side) {
        var t = tradeOf(item, side);
        var got = compare(item.candles, {
          entryIndex: t.entryIndex,
          entry: t.entry,
          stop: t.stop,
          take: t.take,
          direction: side,
          plan: plan,
        });
        if (got) all.push(got);
      });
    });
    var verdict = summarize(all);

    var hereLine = here
      ? (here.difference > 1e-9 ? T.betterHere
        : here.difference < -1e-9 ? T.worseHere : T.sameHere)
      : T.sameHere;

    var lesson = !verdict || Math.abs(verdict.difference) < 1
      ? T.lessonFlat
      : verdict.difference > 0 ? T.lessonGood : T.lessonBad;

    var lines = ["<h4>" + F.escape(T.thisTrade) + "</h4>"];
    if (here) {
      lines.push("<p>" + F.escape(T.yours(r(here.managed.total_r))) + " " +
        F.escape(T.plain(r(here.plain.total_r))) + "</p>");
      lines.push("<p><strong>" + F.escape(hereLine) + "</strong></p>");
    }
    if (verdict) {
      lines.push("<h4>" + F.escape(T.overall) + "</h4>");
      lines.push('<p class="pm-overall">' + F.escape(
        T.overallLine(verdict.trades, r(verdict.plain_total), r(verdict.managed_total))
      ) + "</p>");
      lines.push("<p>" + F.escape(T.counts(verdict.helped, verdict.hurt, verdict.same)) + "</p>");
    }
    lines.push('<p class="pm-lesson">' + F.escape(lesson) + "</p>");
    lines.push('<p class="pm-note">' + F.escape(T.note) + "</p>");
    lines.push('<button type="button" class="calc-button" id="pm-next">' +
      F.escape(T.next) + "</button>");

    var box = document.getElementById("pm-verdict");
    box.innerHTML = lines.join("");
    document.getElementById("pm-next").addEventListener("click", function () {
      current = (current + 1) % episodes.length;
      answered = null;
      render();
    });
    if (window.fxTrack) window.fxTrack("position_management_answered", { once: false });
  }
})();
