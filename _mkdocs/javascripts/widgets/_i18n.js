/*
 * Общий i18n-хелпер для браузерных виджетов-калькуляторов.
 *
 * Зачем: раньше JS каждого калькулятора был скопирован по три раза (RU/EN/UZ),
 * различаясь только строками и локалью форматирования чисел. Любой фикс
 * математики приходилось вносить в три места — источник дрейфа. Теперь логика
 * лежит в одном файле на виджет, а строки — в таблице по локали.
 *
 * Локаль берём из <html lang>, который mkdocs-static-i18n проставляет на каждой
 * странице (ru | en | uz). Подключается ПЕРВЫМ среди widgets/*.js (см. порядок
 * в extra_javascript внутри mkdocs.yml), чтобы window.FXW был готов к моменту
 * запуска конкретного виджета.
 */
window.FXW = (function () {
  var lang = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
  if (lang !== "en" && lang !== "uz") lang = "ru";
  var numLocale = { ru: "ru-RU", en: "en-US", uz: "uz-UZ" }[lang];

  return {
    // Текущая локаль страницы: "ru" | "en" | "uz".
    lang: lang,
    // Локаль для Number.prototype.toLocaleString.
    numLocale: numLocale,

    // Выбирает блок строк под текущую локаль; RU — фолбэк.
    pick: function (tables) {
      return tables[lang] || tables.ru;
    },

    // "$1,234.56" в локализованном формате разрядов.
    money: function (v) {
      return (
        "$" +
        Number(v).toLocaleString(numLocale, {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        })
      );
    },

    // Целое число с локализованными разделителями разрядов: 100000 -> "100 000".
    int: function (v) {
      return Number(v).toLocaleString(numLocale);
    },

    // "12.34%"
    pct: function (v, digits) {
      return Number(v).toFixed(digits == null ? 2 : digits) + "%";
    },
  };
})();
