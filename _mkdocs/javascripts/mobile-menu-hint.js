/**
 * Пульсирующая точка на гамбургере при первом посещении на мобильном.
 * Убирается как только пользователь тапнет в любом месте или откроет ящик.
 */
(function () {
  if (typeof localStorage === "undefined") return;
  // Показываем только на устройствах с касанием и < 1220px
  if (window.matchMedia("(hover: hover)").matches) return;
  var KEY = "fx_menu_seen_v1";
  if (localStorage.getItem(KEY)) return;
  var btn = document.querySelector('label[for="__drawer"]');
  if (!btn) return;
  btn.style.position = "relative";
  btn.classList.add("fx-menu-hint");
  function remove() {
    btn.classList.remove("fx-menu-hint");
    localStorage.setItem(KEY, "1");
  }
  document.addEventListener("click", remove, { once: true });
  document.addEventListener("touchstart", remove, { once: true, passive: true });
})();
