(function () {
  "use strict";
  if (!("serviceWorker" in navigator)) return;
  var script = document.currentScript;
  if (!script) return;
  var workerUrl = new URL("../service-worker.js", script.src);
  var lang = (document.documentElement.lang || "ru").slice(0, 2);
  var copy = {
    ru: { text: "Доступна новая offline-версия сайта.", button: "Обновить" },
    en: { text: "A new offline version is available.", button: "Update" },
    uz: { text: "Saytning yangi offline versiyasi tayyor.", button: "Yangilash" }
  }[lang] || { text: "Доступна новая offline-версия сайта.", button: "Обновить" };
  var refreshing = false;
  var refreshRequested = false;

  function showUpdate(worker) {
    if (!worker || document.getElementById("fx-update-banner")) return;
    var banner = document.createElement("div");
    banner.id = "fx-update-banner";
    banner.className = "fx-update-banner";
    banner.setAttribute("role", "status");
    banner.innerHTML = '<span>' + copy.text + '</span><button type="button">' + copy.button + '</button>';
    banner.querySelector("button").addEventListener("click", function () {
      refreshRequested = true;
      worker.postMessage({ type: "SKIP_WAITING" });
    });
    document.body.appendChild(banner);
  }

  navigator.serviceWorker.addEventListener("controllerchange", function () {
    if (!refreshRequested || refreshing) return;
    refreshing = true;
    window.location.reload();
  });

  window.addEventListener("load", function () {
    navigator.serviceWorker.register(workerUrl.href, { scope: new URL("./", workerUrl).pathname }).then(function (registration) {
      if (registration.waiting) showUpdate(registration.waiting);
      registration.addEventListener("updatefound", function () {
        var worker = registration.installing;
        if (!worker) return;
        worker.addEventListener("statechange", function () {
          if (worker.state === "installed" && navigator.serviceWorker.controller) showUpdate(worker);
        });
      });
    }).catch(function () {
      // Offline support is progressive enhancement; the site remains usable.
    });
  });
})();
