(function () {
  "use strict";
  if (!("serviceWorker" in navigator)) return;
  var script = document.currentScript;
  if (!script) return;
  var workerUrl = new URL("../service-worker.js", script.src);
  window.addEventListener("load", function () {
    navigator.serviceWorker.register(workerUrl.href, { scope: new URL("./", workerUrl).pathname }).catch(function () {
      // Offline support is progressive enhancement; the site remains usable.
    });
  });
})();
