/*
 * Напоминания о повторении карточек — PWA без сервера.
 *
 * Честная механика статичного сайта: настоящий push требует сервера, а его
 * нет и не будет. Поэтому напоминание живёт в двух честных формах:
 *   1. Баннер на любой странице, если сегодня карточки ещё не повторяли —
 *      срабатывает при открытии сайта, прячется кнопкой «Позже» до завтра.
 *   2. Системное уведомление (Notification API), если браузер дал разрешение —
 *      тоже при открытии сайта, не чаще раза в день.
 *
 * Источник истины о повторении — тот же ключ, что пишет тренажёр карточек:
 * ftk-flash-lastday (YYYY-MM-DD). Включение — кнопкой на странице карточек,
 * чтобы согласие было явным и в контексте, а не модалкой на главной.
 */
(function () {
  "use strict";

  var LANG = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (["ru", "en", "uz"].indexOf(LANG) < 0) return; // uz-cyrl — копия uz, баннер не дублируем

  var KEY_ENABLED = "ftk-remind-enabled";
  var KEY_SNOOZE = "ftk-remind-snooze";
  var KEY_NOTIFIED = "ftk-remind-notified";
  var KEY_LASTDAY = "ftk-flash-lastday";
  var KEY_STREAK = "ftk-flash-streak";

  var T = {
    ru: {
      enable: "🔔 Напоминать о повторении",
      enabled: "🔔 Напоминания включены — отключить",
      denied: "Браузер запретил уведомления — останется только баннер на сайте.",
      due: "Карточки сегодня ещё не повторяли.",
      dueStreak: function (n) { return "Серия " + n + " дн. подряд — не прерывай её."; },
      review: "Повторить сейчас",
      later: "Позже",
      notifTitle: "Карточки дня ждут",
      notifBody: "5 минут повторения — и серия не прервётся.",
    },
    en: {
      enable: "🔔 Remind me to review",
      enabled: "🔔 Reminders on — turn off",
      denied: "The browser blocked notifications — the on-site banner remains.",
      due: "You have not reviewed the flashcards today.",
      dueStreak: function (n) { return "A " + n + "-day streak — don't break it."; },
      review: "Review now",
      later: "Later",
      notifTitle: "Cards of the day are waiting",
      notifBody: "5 minutes of review — and the streak survives.",
    },
    uz: {
      enable: "🔔 Takrorlashni eslat",
      enabled: "🔔 Eslatmalar yoqilgan — o'chirish",
      denied: "Brauzer bildirishnomalarni taqiqladi — faqat saytdagi banner qoladi.",
      due: "Bugun kartochkalar hali takrorlanmadi.",
      dueStreak: function (n) { return n + " kunlik seriya — uzma."; },
      review: "Hozir takrorlash",
      later: "Keyin",
      notifTitle: "Kunning kartochkalari kutmoqda",
      notifBody: "5 daqiqa takrorlash — va seriya uzulmaydi.",
    },
  }[LANG];

  function today() {
    return new Date().toISOString().slice(0, 10);
  }

  function store(key, value) {
    try {
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, value);
    } catch (e) {}
  }

  function read(key) {
    try {
      return localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  function flashcardsUrl() {
    var parts = location.pathname.split("/").filter(Boolean);
    var base = parts[0] === "forex-toolkit" ? "/forex-toolkit/" : "/";
    return base + (LANG === "ru" ? "" : LANG + "/") + "tools/flashcards/";
  }

  /* --- Кнопка включения на странице карточек --------------------------- */

  function renderToggle(widget) {
    var on = read(KEY_ENABLED) === "1";
    var button = document.createElement("button");
    button.type = "button";
    button.id = "ftk-remind-toggle";
    button.textContent = on ? T.enabled : T.enable;
    button.style.cssText =
      "margin:.4rem 0;padding:.45rem 1rem;border-radius:6px;cursor:pointer;" +
      "border:1px solid var(--md-default-fg-color--lighter);font-weight:600;" +
      (on ? "background:#2dd4bf;color:#0d1117;" : "background:transparent;color:inherit;");
    button.addEventListener("click", function () {
      if (read(KEY_ENABLED) === "1") {
        store(KEY_ENABLED, null);
      } else {
        store(KEY_ENABLED, "1");
        if ("Notification" in window && Notification.permission === "default") {
          Notification.requestPermission().then(function (permission) {
            if (permission === "denied") alert(T.denied);
          });
        }
      }
      button.replaceWith();
      renderToggle(widget);
    });
    widget.prepend(button);
  }

  /* --- Баннер и уведомление --------------------------------------------- */

  function reviewedToday() {
    return read(KEY_LASTDAY) === today();
  }

  function maybeNotify() {
    if (!("Notification" in window)) return;
    if (Notification.permission !== "granted") return;
    if (read(KEY_NOTIFIED) === today()) return;
    store(KEY_NOTIFIED, today());
    new Notification(T.notifTitle, { body: T.notifBody });
  }

  function maybeBanner() {
    if (read(KEY_ENABLED) !== "1") return;
    if (reviewedToday()) return;
    if (read(KEY_SNOOZE) === today()) return;
    if (document.getElementById("ftk-remind-banner")) return;

    var streak = parseInt(read(KEY_STREAK) || "0", 10);
    var banner = document.createElement("div");
    banner.id = "ftk-remind-banner";
    banner.style.cssText =
      "margin:.8rem 0;padding:.7rem .9rem;border-radius:8px;font-size:.88rem;" +
      "border:1px solid #8b5cf6;background:rgba(139,92,246,.10);" +
      "display:flex;gap:.7rem;align-items:center;flex-wrap:wrap;";

    var text = document.createElement("span");
    text.textContent = "🎴 " + T.due + (streak > 1 ? " " + T.dueStreak(streak) : "");

    var go = document.createElement("a");
    go.href = flashcardsUrl();
    go.textContent = T.review;
    go.style.cssText = "font-weight:700;";

    var later = document.createElement("button");
    later.type = "button";
    later.id = "ftk-remind-later";
    later.textContent = T.later;
    later.style.cssText =
      "padding:.25rem .8rem;border-radius:5px;cursor:pointer;" +
      "border:1px solid var(--md-default-fg-color--lighter);background:transparent;color:inherit;";
    later.addEventListener("click", function () {
      store(KEY_SNOOZE, today());
      banner.remove();
    });

    banner.appendChild(text);
    banner.appendChild(go);
    banner.appendChild(later);

    var article = document.querySelector(".md-content__inner");
    if (article && article.firstChild) article.insertBefore(banner, article.firstChild);
  }

  /* --- Запуск ------------------------------------------------------------ */

  var widget = document.getElementById("ftk-widget");
  if (widget) renderToggle(widget);

  // Небольшая задержка: баннер не должен мигать поверх первого экрана.
  setTimeout(function () {
    maybeBanner();
    if (read(KEY_ENABLED) === "1" && !reviewedToday()) maybeNotify();
  }, 1500);
})();
