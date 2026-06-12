/*
 * Виджет торговых сессий + живые часы — общий для всех локалей.
 * Сессии заданы в UTC; статус «открыта/закрыта» считается по реальному UTC-времени,
 * а часы показываются в выбранном пользователем поясе через Intl (DST учитывается
 * автоматически). Денег не считает — e2e не требуется; локаль из <html lang>.
 */
(function () {
  if (!document.getElementById("ts-widget")) return;
  var F = window.FXW;

  var T = F.pick({
    ru: {
      sydney: "🇦🇺 Сидней",
      tokyo: "🇯🇵 Токио",
      london: "🇬🇧 Лондон",
      newyork: "🇺🇸 Нью-Йорк",
      open: "🟢 открыта",
      closed: "⚪ закрыта",
      overlap: "🔥 Лондон + Нью-Йорк открыты одновременно — лучшее окно для мажоров (узкие спреды, максимум объёма).",
      weekend: "💤 Сейчас выходные — рынок forex закрыт. Откроется в понедельник (азиатская сессия).",
    },
    en: {
      sydney: "🇦🇺 Sydney",
      tokyo: "🇯🇵 Tokyo",
      london: "🇬🇧 London",
      newyork: "🇺🇸 New York",
      open: "🟢 open",
      closed: "⚪ closed",
      overlap: "🔥 London + New York are open at the same time — the best window for majors (tight spreads, peak volume).",
      weekend: "💤 It's the weekend — the forex market is closed. It reopens Monday (Asian session).",
    },
    uz: {
      sydney: "🇦🇺 Sidney",
      tokyo: "🇯🇵 Tokio",
      london: "🇬🇧 London",
      newyork: "🇺🇸 Nyu-York",
      open: "🟢 ochiq",
      closed: "⚪ yopiq",
      overlap: "🔥 London + Nyu-York bir vaqtda ochiq — majorlar uchun eng yaxshi oyna (tor spredlar, maksimal hajm).",
      weekend: "💤 Hozir dam olish kunlari — forex bozori yopiq. Dushanba (Osiyo sessiyasi) ochiladi.",
    },
  });

  // UTC-окна сессий (ориентир, ±1 ч из-за DST Лондона/Нью-Йорка).
  var SESSIONS = [
    { name: T.sydney, open: 22, close: 7 },
    { name: T.tokyo, open: 0, close: 9 },
    { name: T.london, open: 8, close: 17 },
    { name: T.newyork, open: 13, close: 22 },
  ];

  function isOpen(open, close, h) {
    return open < close ? h >= open && h < close : h >= open || h < close;
  }

  function tick() {
    var tz = document.getElementById("ts-tz").value;
    var now = new Date();
    var utcH = now.getUTCHours() + now.getUTCMinutes() / 60;
    var day = now.getUTCDay(); // 0=вс, 6=сб

    // Часы в выбранном поясе.
    try {
      document.getElementById("ts-clock").textContent = new Intl.DateTimeFormat(F.numLocale, {
        timeZone: tz,
        weekday: "short",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
      }).format(now);
    } catch (e) {
      document.getElementById("ts-clock").textContent = now.toUTCString();
    }

    // Выходные: forex закрыт с пт 22:00 UTC до вс 22:00 UTC.
    var weekend =
      day === 6 || (day === 0 && utcH < 22) || (day === 5 && utcH >= 22);

    var grid = document.getElementById("ts-sessions");
    grid.innerHTML = SESSIONS.map(function (s) {
      var open = !weekend && isOpen(s.open, s.close, utcH);
      return (
        '<div class="pc-result-row"><span>' +
        s.name +
        "</span><span>" +
        (open ? T.open : T.closed) +
        "</span></div>"
      );
    }).join("");

    var warnings = document.getElementById("ts-warnings");
    if (weekend) {
      warnings.innerHTML = '<div class="pc-warn pc-info">' + T.weekend + "</div>";
    } else if (isOpen(8, 17, utcH) && isOpen(13, 22, utcH)) {
      warnings.innerHTML = '<div class="pc-warn" style="background:rgba(34,197,94,0.1);border-left-color:#22c55e;">' + T.overlap + "</div>";
    } else {
      warnings.innerHTML = "";
    }
  }

  document.getElementById("ts-tz").addEventListener("change", tick);
  tick();
  setInterval(tick, 1000);
})();
