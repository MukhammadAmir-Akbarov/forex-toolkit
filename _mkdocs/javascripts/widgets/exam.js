/*
 * Итоговый экзамен + именной PNG-сертификат — самодостаточный виджет.
 * НЕ зависит от _i18n.js (детект локали локально), чтобы страница работала
 * независимо от рефакторинга движка. Вопросы берёт из JSON-блока на странице
 * (#exam-questions) — они переведены в каждой локали; строки интерфейса и
 * подписи сертификата — в таблице по локали ниже.
 *
 * Проходной балл 80%. На успехе пишет в localStorage forex_exam_passed (для
 * интеграции с трекером прогресса) и forex_exam_best (лучший процент).
 */
(function () {
  if (!document.getElementById("exam-widget")) return;

  var lang = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (lang !== "en" && lang !== "uz") lang = "ru";
  var dateLocale = { ru: "ru-RU", en: "en-US", uz: "uz-UZ" }[lang];

  var PASS = 80; // %

  var S = ({
    ru: {
      counter: function (i, n) { return "Вопрос " + i + " из " + n; },
      score: function (s) { return "Очки: " + s; },
      best: function (p) { return "🏆 Лучший результат: " + p + "%"; },
      noBest: "Пройди экзамен, чтобы проверить себя.",
      passTitle: function (p) { return "🎉 Сдано — " + p + "%!"; },
      failTitle: function (p) { return "Пока не сдано — " + p + "%"; },
      passBody: "Отличная база! Скачай сертификат ниже. Но помни: настоящий экзамен — рынок. Переходи на реал маленьким объёмом.",
      failBody: "Нужно ≥ 80%. Перечитай слабые темы и попробуй снова — это нормально.",
      needName: "✍️ Введи имя в поле выше и пройди заново, чтобы получить именной сертификат.",
      retake: "↻ Пройти заново",
      certTitle: "СЕРТИФИКАТ О ПРОХОЖДЕНИИ",
      certAwarded: "выдан",
      certCourse: "Курс «Forex для новичков: основы»",
      certResult: "Результат",
      certDate: "Дата",
      certNote: "Образовательное достижение — не финансовый совет",
    },
    en: {
      counter: function (i, n) { return "Question " + i + " of " + n; },
      score: function (s) { return "Score: " + s; },
      best: function (p) { return "🏆 Best result: " + p + "%"; },
      noBest: "Take the exam to test yourself.",
      passTitle: function (p) { return "🎉 Passed — " + p + "%!"; },
      failTitle: function (p) { return "Not passed yet — " + p + "%"; },
      passBody: "Great foundation! Download your certificate below. But remember: the real exam is the market. Go live with a small size.",
      failBody: "You need ≥ 80%. Review the weak topics and try again — that's normal.",
      needName: "✍️ Enter your name in the field above and retake to get a personalized certificate.",
      retake: "↻ Retake",
      certTitle: "CERTIFICATE OF COMPLETION",
      certAwarded: "awarded to",
      certCourse: 'Course "Forex for Beginners: Fundamentals"',
      certResult: "Score",
      certDate: "Date",
      certNote: "An educational achievement — not financial advice",
    },
    uz: {
      counter: function (i, n) { return i + " / " + n + " savol"; },
      score: function (s) { return "Ball: " + s; },
      best: function (p) { return "🏆 Eng yaxshi natija: " + p + "%"; },
      noBest: "O'zingizni sinab ko'rish uchun imtihon topshiring.",
      passTitle: function (p) { return "🎉 Topshirildi — " + p + "%!"; },
      failTitle: function (p) { return "Hali topshirilmadi — " + p + "%"; },
      passBody: "Ajoyib poydevor! Quyida sertifikatni yuklab oling. Lekin esda tuting: asl imtihon — bozor. Kichik hajm bilan realga o'ting.",
      failBody: "≥ 80% kerak. Zaif mavzularni qayta o'qing va yana urinib ko'ring — bu normal.",
      needName: "✍️ Nomli sertifikat olish uchun yuqoridagi maydonga ismingizni kiriting va qaytadan topshiring.",
      retake: "↻ Qayta topshirish",
      certTitle: "TUGATGANLIK SERTIFIKATI",
      certAwarded: "egasi",
      certCourse: "«Yangi boshlovchilar uchun Forex: asoslar» kursi",
      certResult: "Natija",
      certDate: "Sana",
      certNote: "O'quv yutug'i — moliyaviy maslahat emas",
    },
  })[lang];

  var QUESTIONS = [];
  try {
    QUESTIONS = JSON.parse(document.getElementById("exam-questions").textContent);
  } catch (e) {
    QUESTIONS = [];
  }
  var total = QUESTIONS.length;

  var idx = 0;
  var score = 0;
  var answered = false;
  var passedName = "";

  var el = function (id) { return document.getElementById(id); };

  function showBest() {
    var b = null;
    try { b = localStorage.getItem("forex_exam_best"); } catch (e) {}
    el("exam-best").textContent = b ? S.best(parseInt(b, 10)) : S.noBest;
  }

  function start() {
    idx = 0;
    score = 0;
    el("exam-start").style.display = "none";
    el("exam-result").style.display = "none";
    el("exam-cert-wrap").style.display = "none";
    el("exam-play").style.display = "block";
    render();
  }

  function render() {
    answered = false;
    var q = QUESTIONS[idx];
    el("exam-counter").textContent = S.counter(idx + 1, total);
    el("exam-score").textContent = S.score(score);
    el("exam-bar").style.width = (idx / total) * 100 + "%";
    el("exam-question").textContent = q.q;
    el("exam-explain").style.display = "none";
    el("exam-next").style.display = "none";

    var opts = el("exam-options");
    opts.innerHTML = "";
    q.options.forEach(function (text, i) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "exam-option";
      btn.textContent = text;
      btn.addEventListener("click", function () { choose(i, btn); });
      opts.appendChild(btn);
    });
  }

  function choose(i, btn) {
    if (answered) return;
    answered = true;
    var q = QUESTIONS[idx];
    var buttons = el("exam-options").querySelectorAll(".exam-option");
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].disabled = true;
      if (j === q.answer) buttons[j].classList.add("exam-correct");
    }
    if (i === q.answer) {
      score++;
    } else {
      btn.classList.add("exam-wrong");
    }
    el("exam-score").textContent = S.score(score);
    var ex = el("exam-explain");
    ex.textContent = q.explain;
    ex.style.display = "block";
    el("exam-next").style.display = "inline-block";
  }

  function next() {
    idx++;
    if (idx < total) {
      render();
    } else {
      finish();
    }
  }

  function finish() {
    el("exam-play").style.display = "none";
    var pct = Math.round((score / total) * 100);
    var passed = pct >= PASS;

    try {
      var prev = parseInt(localStorage.getItem("forex_exam_best") || "0", 10);
      if (pct > prev) localStorage.setItem("forex_exam_best", String(pct));
      if (passed) localStorage.setItem("forex_exam_passed", "1");
    } catch (e) {}

    var name = (el("exam-name").value || "").trim();
    var html =
      '<div class="calc-result ' + (passed ? "calc-ok" : "calc-warn") + '">' +
      "<h3>" + (passed ? S.passTitle(pct) : S.failTitle(pct)) + "</h3>" +
      "<p>" + (passed ? S.passBody : S.failBody) + "</p>" +
      (passed && !name ? "<p><strong>" + S.needName + "</strong></p>" : "") +
      '<button class="calc-button" id="exam-retake">' + S.retake + "</button>" +
      "</div>";
    var res = el("exam-result");
    res.innerHTML = html;
    res.style.display = "block";
    el("exam-retake").addEventListener("click", start);

    if (passed && name) {
      passedName = name;
      drawCertificate(name, pct);
      el("exam-cert-wrap").style.display = "block";
    }
  }

  function drawCertificate(name, pct) {
    var c = el("exam-cert");
    var ctx = c.getContext("2d");
    var W = c.width, H = c.height;

    // Фон
    ctx.fillStyle = "#0d1117";
    ctx.fillRect(0, 0, W, H);
    // Рамка
    ctx.strokeStyle = "#2dd4bf";
    ctx.lineWidth = 6;
    ctx.strokeRect(24, 24, W - 48, H - 48);
    ctx.strokeStyle = "rgba(45,212,191,0.35)";
    ctx.lineWidth = 2;
    ctx.strokeRect(40, 40, W - 80, H - 80);

    ctx.textAlign = "center";
    var cx = W / 2;

    ctx.fillStyle = "#5eead4";
    ctx.font = "bold 40px Georgia, 'Times New Roman', serif";
    ctx.fillText(S.certTitle, cx, 150);

    ctx.fillStyle = "rgba(230,237,243,0.7)";
    ctx.font = "22px Georgia, serif";
    ctx.fillText(S.certAwarded, cx, 250);

    // Имя
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 54px Georgia, serif";
    ctx.fillText(name, cx, 320);
    ctx.strokeStyle = "rgba(45,212,191,0.5)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx - 280, 345);
    ctx.lineTo(cx + 280, 345);
    ctx.stroke();

    ctx.fillStyle = "rgba(230,237,243,0.85)";
    ctx.font = "24px Georgia, serif";
    ctx.fillText(S.certCourse, cx, 420);

    ctx.fillStyle = "#5eead4";
    ctx.font = "bold 30px Georgia, serif";
    ctx.fillText(S.certResult + ": " + pct + "%", cx, 490);

    var dateStr = new Date().toLocaleDateString(dateLocale, {
      year: "numeric", month: "long", day: "numeric",
    });
    ctx.fillStyle = "rgba(230,237,243,0.6)";
    ctx.font = "20px Georgia, serif";
    ctx.fillText(S.certDate + ": " + dateStr, cx, 560);

    ctx.fillStyle = "rgba(94,234,212,0.8)";
    ctx.font = "bold 22px Georgia, serif";
    ctx.fillText("forex-toolkit", cx, 620);

    ctx.fillStyle = "rgba(230,237,243,0.4)";
    ctx.font = "italic 16px Georgia, serif";
    ctx.fillText(S.certNote, cx, 655);
  }

  function download() {
    var c = el("exam-cert");
    var link = document.createElement("a");
    var safe = (passedName || "certificate").replace(/[^\p{L}\p{N}_-]+/gu, "_");
    link.download = "forex-certificate-" + safe + ".png";
    link.href = c.toDataURL("image/png");
    link.click();
  }

  el("exam-start-btn").addEventListener("click", start);
  el("exam-next").addEventListener("click", next);
  el("exam-download-btn").addEventListener("click", download);
  showBest();
})();
