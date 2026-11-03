/*
 * Сезонность пар: средний ход каждого календарного месяца (8 × 12).
 *
 * Данные — _mkdocs/data/seasonality.json (tools/build_seasonality.py):
 * месячные лог-доходности по дневным свечам → среднее/медиана/доля плюсовых
 * лет/число лет в каждой ячейке.
 *
 * Честность важнее красоты: на форексе сезонность слабая, а наблюдений на
 * месяц — считаные годы. Поэтому тонкие ячейки (n ниже порога из meta)
 * рисуются приглушённо и с пометкой: это контекст, а не сигнал входа.
 */
(function () {
  "use strict";

  var root = document.getElementById("seasonality");
  if (!root || !window.FXW) return;

  var F = window.FXW;

  var T = F.pick({
    ru: {
      loading: "Считаю сезонность…",
      loadError: "Не удалось загрузить данные. Обнови страницу.",
      title: "Средний ход месяца, % (дневные свечи)",
      months: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
      down: "вниз",
      up: "вверх",
      noData: "—",
      thin: "мало лет",
      cell: function (pair, month, avg, median, pos, n) {
        return pair + ", " + month + ": в среднем " + avg + "% (медиана " + median +
          "%), рос " + pos + "% лет из " + n + ".";
      },
      thinNote: function (threshold) {
        return "Приглушённые ячейки — меньше " + threshold +
          " лет наблюдений: это шум выборки, а не закономерность.";
      },
      range: function (from, to, stamp) {
        return "Дневные свечи восьми пар, " + from + " → " + to + ". Пересчёт: " + stamp + ".";
      },
    },
    en: {
      loading: "Computing seasonality…",
      loadError: "Could not load the data. Refresh the page.",
      title: "Average month move, % (daily candles)",
      months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      down: "down",
      up: "up",
      noData: "—",
      thin: "few years",
      cell: function (pair, month, avg, median, pos, n) {
        return pair + ", " + month + ": " + avg + "% on average (median " + median +
          "%), up in " + pos + "% of " + n + " years.";
      },
      thinNote: function (threshold) {
        return "Dimmed cells have fewer than " + threshold +
          " years of observations: that is sample noise, not a pattern.";
      },
      range: function (from, to, stamp) {
        return "Daily candles of eight pairs, " + from + " → " + to + ". Recomputed: " + stamp + ".";
      },
    },
    uz: {
      loading: "Mavsumiylik hisoblanmoqda…",
      loadError: "Ma'lumotni yuklab bo'lmadi. Sahifani yangilang.",
      title: "Oyning o'rtacha xodi, % (kunlik shamchalar)",
      months: ["Yan", "Fev", "Mar", "Apr", "May", "Iyn", "Iyl", "Avg", "Sen", "Okt", "Noy", "Dek"],
      down: "pastga",
      up: "yuqoriga",
      noData: "—",
      thin: "kam yil",
      cell: function (pair, month, avg, median, pos, n) {
        return pair + ", " + month + ": o'rtacha " + avg + "% (mediana " + median +
          "%), " + n + " yildan " + pos + "% ida o'sgan.";
      },
      thinNote: function (threshold) {
        return "Ochiq rangli kataklarda " + threshold +
          " yildan kam kuzatuv bor: bu qonuniyat emas, tanlov shovqini.";
      },
      range: function (from, to, stamp) {
        return "Sakkiz juftlikning kunlik shamchalari, " + from + " → " + to + ". Hisoblangan: " + stamp + ".";
      },
    },
  });

  var style = document.createElement("style");
  style.textContent = [
    ".fx-season{overflow-x:auto;margin:1rem 0}",
    ".fx-season table{border-collapse:collapse;font-size:.78rem;font-variant-numeric:tabular-nums}",
    ".fx-season th{padding:.3rem .45rem;font-weight:600;color:var(--md-default-fg-color--light)}",
    ".fx-season td{padding:.3rem .45rem;text-align:center;min-width:3rem;border-radius:3px;cursor:default}",
    ".fx-season td.fx-season-pair{text-align:left;font-weight:700;cursor:default}",
    ".fx-season td.fx-season-thin{opacity:.45}",
    ".fx-season-legend{display:flex;gap:.5rem;align-items:center;font-size:.72rem;color:var(--md-default-fg-color--light);margin:.4rem 0}",
    ".fx-season-chip{width:.9rem;height:.9rem;border-radius:2px;display:inline-block}",
    ".fx-season-note{font-size:.78rem;color:var(--md-default-fg-color--light)}",
    ".fx-season-detail{margin-top:.6rem;padding:.6rem .8rem;border-left:3px solid #8b5cf6;background:rgba(139,92,246,.08);font-size:.88rem;min-height:1.4rem}",
  ].join("");
  document.head.appendChild(style);

  function cellColor(avg) {
    // Расходящаяся шкала: минус — красный, плюс — бирюзовый, 2% — насыщенность.
    var strength = Math.min(Math.abs(avg) / 2, 1);
    var alpha = (0.12 + 0.55 * strength).toFixed(2);
    return avg >= 0
      ? "rgba(45,212,191," + alpha + ")"
      : "rgba(248,113,113," + alpha + ")";
  }

  function render(document_) {
    var threshold = (document_.meta && document_.meta.thin_sample_below) || 10;
    var detail = null;

    var header = '<tr><th></th>' + T.months.map(function (name) {
      return "<th>" + F.escape(name) + "</th>";
    }).join("") + "</tr>";

    var rows = document_.pairs.map(function (pair) {
      var cells = document_.stats[pair].map(function (cell, index) {
        if (cell.n === 0 || cell.avg === null) {
          return '<td class="fx-season-thin">' + F.escape(T.noData) + "</td>";
        }
        var thin = cell.n < threshold ? " fx-season-thin" : "";
        return '<td class="fx-season-cell' + thin + '" data-pair="' + pair +
          '" data-month="' + index + '" style="background:' + cellColor(cell.avg) + '"' +
          ' title="' + F.escape(cell.n + " · " + (cell.n < threshold ? T.thin : "")) + '">' +
          (cell.avg > 0 ? "+" : "") + cell.avg + "</td>";
      }).join("");
      return '<tr><td class="fx-season-pair">' + pair + "</td>" + cells + "</tr>";
    }).join("");

    root.innerHTML =
      '<div class="fx-season">' +
      '<div class="fx-season-note"><strong>' + F.escape(T.title) + "</strong></div>" +
      "<table><thead>" + header + "</thead><tbody>" + rows + "</tbody></table>" +
      '<div class="fx-season-legend">' +
      '<span class="fx-season-chip" style="background:rgba(248,113,113,.6)"></span><span>' + F.escape(T.down) + "</span>" +
      '<span class="fx-season-chip" style="background:rgba(45,212,191,.6)"></span><span>' + F.escape(T.up) + "</span>" +
      "<span>· " + F.escape(T.thinNote(threshold)) + "</span>" +
      "</div>" +
      '<div class="fx-season-detail" id="fx-season-detail">' +
      F.escape(T.range(document_.meta.range.from.slice(0, 10), document_.meta.range.to.slice(0, 10), document_.meta.generated_at)) +
      "</div></div>";

    detail = root.querySelector("#fx-season-detail");
    root.querySelectorAll(".fx-season-cell").forEach(function (cell) {
      cell.addEventListener("click", function () {
        var pair = cell.getAttribute("data-pair");
        var month = Number(cell.getAttribute("data-month"));
        var stats = document_.stats[pair][month];
        detail.textContent = T.cell(
          pair, T.months[month], (stats.avg > 0 ? "+" : "") + stats.avg,
          (stats.median > 0 ? "+" : "") + stats.median,
          Math.round(stats.pos * 100), stats.n
        );
      });
    });
  }

  root.textContent = T.loading;
  fetch(root.getAttribute("data-src"))
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(render)
    .catch(function () {
      root.textContent = T.loadError;
    });
})();
