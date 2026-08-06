/*
 * Тест готовности к реальной торговле — веб-версия tools/risk_profile.py.
 *
 * Зачем виджет: roadmap требует пройти этот тест на первой неделе, но до
 * сих пор он жил только в CLI — то есть за установкой Python. Аудитория
 * сидит с телефона и до терминала не доходит, а это единственный инструмент,
 * который может сказать «не торгуй на заёмные, пока нет подушки».
 *
 * Вопросы берём из JSON-блока страницы (#risk-profile-questions) — они
 * переведены в каждой локали. Баллы, границы полос и порог слабой категории
 * обязаны совпадать с forex_toolkit/risk_profile.py; сверку держит e2e,
 * а совпадение баллов между локалями — tests/test_risk_profile_pages.py.
 */
(function () {
  "use strict";

  var root = document.getElementById("risk-profile-widget");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var KEY = "forex_risk_profile_v1";
  // Те же пороги, что BANDS в forex_toolkit/risk_profile.py.
  var BANDS = [[80, "excellent"], [60, "good"], [40, "borderline"], [20, "high_risk"]];
  var WEAK_RATIO = 0.5;

  var T = F.pick({
    ru: {
      start: "Начать тест", intro: "30 вопросов, около 10 минут. Отвечай честно — результат видишь только ты, он остаётся в браузере и никуда не отправляется.",
      of: function (i, n) { return "Вопрос " + i + " из " + n; },
      back: "Назад", retake: "Пройти заново", result: "Твой результат",
      score: "Баллы", weakTitle: "Слабые зоны — с них и начинай",
      strong: "Во всех категориях результат выше половины.",
      savedAt: function (d) { return "Пройден: " + d; },
      previous: "Прошлый результат", again: "Пройди тест снова через 6 месяцев и сравни.",
      categories: {
        finance: "Финансы", time: "Время и обучение", psychology: "Психология",
        character: "Характер", experience: "Опыт", health: "Здоровье",
        relationships: "Отношения", motivation: "Мотивация", warnings: "Предупреждения"
      },
      bands: {
        excellent: { title: "Отличный профиль", text: "Подушка есть, психология устойчивая, ожидания реалистичные. Можно начинать обучение и демо — но объём на реале держи минимальным." },
        good: { title: "Хороший профиль", text: "В целом подходишь, но слабые места ниже стоит закрыть до реальных денег. Начинай осторожно и с минимальным риском." },
        borderline: { title: "Пограничный профиль", text: "Риски серьёзные. Сначала укрепи финансовую подушку и психологию — это минимум полгода подготовки. Реальные деньги пока подождут." },
        high_risk: { title: "Высокий риск", text: "Сейчас торговля рискует стоить не только денег, но и сна и отношений. Рекомендую пока не начинать: накопи подушку на 6 месяцев, получи стабильный доход, вернись к тесту через год." },
        critical: { title: "Критический риск", text: "Настоятельно не начинай сейчас. С таким профилем вероятность катастрофического убытка очень высока. Сначала подушка и стабильный доход; если есть склонность к азарту или зависимости — обратись к специалисту. Долгосрочное инвестирование безопаснее." }
      }
    },
    en: {
      start: "Start the test", intro: "30 questions, about 10 minutes. Answer honestly — only you see the result, it stays in your browser and is never sent anywhere.",
      of: function (i, n) { return "Question " + i + " of " + n; },
      back: "Back", retake: "Take it again", result: "Your result",
      score: "Points", weakTitle: "Weak areas — start here",
      strong: "Every category scored above half.",
      savedAt: function (d) { return "Taken: " + d; },
      previous: "Previous result", again: "Take the test again in 6 months and compare.",
      categories: {
        finance: "Finance", time: "Time and learning", psychology: "Psychology",
        character: "Character", experience: "Experience", health: "Health",
        relationships: "Relationships", motivation: "Motivation", warnings: "Red flags"
      },
      bands: {
        excellent: { title: "Excellent profile", text: "You have a cushion, steady psychology and realistic expectations. Start learning and demo trading — but keep live size minimal." },
        good: { title: "Good profile", text: "You broadly fit, but close the weak spots below before real money. Start carefully with minimal risk." },
        borderline: { title: "Borderline profile", text: "The risks are serious. Build the financial cushion and work on psychology first — at least six months of preparation. Real money can wait." },
        high_risk: { title: "High risk", text: "Trading now risks costing you more than money — sleep and relationships too. I recommend not starting yet: build a six-month cushion, get stable income, come back in a year." },
        critical: { title: "Critical risk", text: "Strongly do not start now. With this profile the chance of a catastrophic loss is very high. Build the cushion and stable income first; if there is a tendency to gambling or addiction, talk to a specialist. Long-term investing is safer." }
      }
    },
    uz: {
      start: "Testni boshlash", intro: "30 ta savol, taxminan 10 daqiqa. Rostini javob bering — natijani faqat siz ko'rasiz, u brauzeringizda qoladi va hech qayerga yuborilmaydi.",
      of: function (i, n) { return i + " / " + n + "-savol"; },
      back: "Orqaga", retake: "Qayta topshirish", result: "Sizning natijangiz",
      score: "Ball", weakTitle: "Zaif tomonlar — shulardan boshlang",
      strong: "Barcha toifalarda natija yarmidan yuqori.",
      savedAt: function (d) { return "Topshirilgan: " + d; },
      previous: "Oldingi natija", again: "6 oydan keyin testni qayta topshiring va solishtiring.",
      categories: {
        finance: "Moliya", time: "Vaqt va o'rganish", psychology: "Psixologiya",
        character: "Xarakter", experience: "Tajriba", health: "Salomatlik",
        relationships: "Munosabatlar", motivation: "Motivatsiya", warnings: "Ogohlantirishlar"
      },
      bands: {
        excellent: { title: "A'lo profil", text: "Moliyaviy yostiq bor, psixologiya barqaror, kutganlaringiz real. O'rganish va demoni boshlashingiz mumkin — lekin real hisobda hajmni eng kichik qilib saqlang." },
        good: { title: "Yaxshi profil", text: "Umuman mos kelasiz, lekin quyidagi zaif joylarni real puldan oldin yoping. Ehtiyotkorlik bilan va minimal risk bilan boshlang." },
        borderline: { title: "Chegaradagi profil", text: "Risklar jiddiy. Avval moliyaviy yostiqni mustahkamlang va psixologiya ustida ishlang — bu kamida olti oylik tayyorgarlik. Real pul kutib tursin." },
        high_risk: { title: "Yuqori risk", text: "Hozir savdo qilish nafaqat pul, balki uyqu va munosabatlarga ham tushishi mumkin. Hozircha boshlamaslikni tavsiya qilaman: 6 oylik yostiq to'plang, barqaror daromad qiling va bir yildan keyin testga qayting." },
        critical: { title: "Kritik risk", text: "Hozir boshlamang. Bunday profilda halokatli zarar ehtimoli juda yuqori. Avval yostiq va barqaror daromad; qimor yoki qaramlikka moyillik bo'lsa — mutaxassisga murojaat qiling. Uzoq muddatli investitsiya xavfsizroq." }
      }
    }
  });

  var questions = [];
  try {
    var raw = document.getElementById("risk-profile-questions");
    questions = JSON.parse(raw.textContent);
  } catch (error) {
    return;
  }
  if (!questions.length) return;

  var answers = [];
  var step = -1;

  function bandFor(percent) {
    for (var i = 0; i < BANDS.length; i++) {
      if (percent >= BANDS[i][0]) return BANDS[i][1];
    }
    return "critical";
  }

  function summarise() {
    var total = 0;
    var byCategory = {};
    var maxByCategory = {};
    var top = 0;
    questions.forEach(function (question, index) {
      var points = question.options.map(function (option) { return Number(option.points); });
      var best = Math.max.apply(null, points);
      var category = question.category || "";
      top += best;
      maxByCategory[category] = (maxByCategory[category] || 0) + best;
      var picked = points[answers[index]];
      total += picked;
      byCategory[category] = (byCategory[category] || 0) + picked;
    });
    var percent = top > 0 ? total / top * 100 : 0;
    var weak = Object.keys(maxByCategory).filter(function (category) {
      return maxByCategory[category] > 0 &&
        byCategory[category] / maxByCategory[category] < WEAK_RATIO;
    }).sort();
    return {
      total: total, max_score: top, percent: percent,
      band: bandFor(percent), weak_categories: weak,
      categories: byCategory, category_max: maxByCategory
    };
  }

  function save(summary) {
    try {
      localStorage.setItem(KEY, JSON.stringify({
        percent: Math.round(summary.percent * 10) / 10,
        band: summary.band,
        weak: summary.weak_categories,
        takenAt: new Date().toISOString()
      }));
    } catch (error) {}
  }

  function previous() {
    try {
      var value = JSON.parse(localStorage.getItem(KEY) || "null");
      return value && typeof value.percent === "number" ? value : null;
    } catch (error) { return null; }
  }

  function renderIntro() {
    var last = previous();
    var earlier = "";
    if (last) {
      var when = new Date(last.takenAt);
      earlier = '<p class="risk-profile__previous"><strong>' + F.escape(T.previous) + ':</strong> ' +
        last.percent.toFixed(1) + '% — ' + F.escape(T.bands[last.band].title) +
        (isNaN(when.getTime()) ? "" : ' · ' + F.escape(T.savedAt(when.toLocaleDateString(F.numLocale)))) +
        '</p>';
    }
    root.innerHTML = '<div class="risk-profile"><p>' + F.escape(T.intro) + '</p>' + earlier +
      '<div class="fx-tool-actions"><button type="button" id="rp-start">' +
      F.escape(T.start) + '</button></div></div>';
    document.getElementById("rp-start").addEventListener("click", function () {
      answers = [];
      step = 0;
      renderStep();
    });
  }

  function renderStep() {
    var question = questions[step];
    var options = question.options.map(function (option, index) {
      return '<label class="risk-profile__option"><input type="radio" name="rp-answer" value="' +
        index + '"' + (answers[step] === index ? " checked" : "") + '> <span>' +
        F.escape(option.label) + '</span></label>';
    }).join("");
    root.innerHTML = '<div class="risk-profile">' +
      '<div class="risk-profile__progress" aria-live="polite">' + F.escape(T.of(step + 1, questions.length)) + '</div>' +
      '<progress max="' + questions.length + '" value="' + step + '"></progress>' +
      '<fieldset class="risk-profile__question"><legend>' + F.escape(question.q) + '</legend>' +
      options + '</fieldset>' +
      (step > 0 ? '<div class="fx-tool-actions"><button type="button" class="fx-secondary" id="rp-back">' +
        F.escape(T.back) + '</button></div>' : "") +
      '</div>';

    var first = root.querySelector('input[name="rp-answer"]');
    if (first) first.focus();
    root.querySelectorAll('input[name="rp-answer"]').forEach(function (input) {
      input.addEventListener("change", function () {
        answers[step] = Number(input.value);
        step++;
        if (step >= questions.length) renderResult();
        else renderStep();
      });
    });
    var back = document.getElementById("rp-back");
    if (back) back.addEventListener("click", function () { step--; renderStep(); });
  }

  function renderResult() {
    var summary = summarise();
    save(summary);
    window.__fxRiskProfile = summary;
    var band = T.bands[summary.band];
    var weak = summary.weak_categories.length
      ? '<h4>' + F.escape(T.weakTitle) + '</h4><ul class="risk-profile__weak">' +
        summary.weak_categories.map(function (category) {
          return '<li>' + F.escape(T.categories[category] || category) + ': ' +
            summary.categories[category] + ' / ' + summary.category_max[category] + '</li>';
        }).join("") + '</ul>'
      : '<p>' + F.escape(T.strong) + '</p>';

    // Мы заменяем всё содержимое виджета: без переноса фокуса пользователь
    // экранного диктора не узнает, что тест кончился и появился вердикт.
    root.innerHTML = '<div class="risk-profile risk-profile--result is-' + summary.band +
      '" role="status">' +
      '<h3 id="rp-result-title" tabindex="-1">' + F.escape(T.result) + '</h3>' +
      '<div class="risk-profile__score"><strong>' + summary.percent.toFixed(1) + '%</strong>' +
      '<span>' + F.escape(T.score) + ': ' + summary.total + ' / ' + summary.max_score + '</span></div>' +
      '<h4 class="risk-profile__verdict">' + F.escape(band.title) + '</h4>' +
      '<p>' + F.escape(band.text) + '</p>' + weak +
      '<p class="risk-profile__again">' + F.escape(T.again) + '</p>' +
      '<div class="fx-tool-actions"><button type="button" class="fx-secondary" id="rp-retake">' +
      F.escape(T.retake) + '</button></div></div>';
    document.getElementById("rp-retake").addEventListener("click", renderIntro);
    document.getElementById("rp-result-title").focus();
    if (window.fxTrack) window.fxTrack("risk_profile_completed");
  }

  renderIntro();
})();
