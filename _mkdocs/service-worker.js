const CACHE = "fx-toolkit-v1";
const CORE = [
  "./",
  "./en/",
  "./uz/",
  "./offline/",
  "./en/offline/",
  "./uz/offline/",
  "./forex-guide/",
  "./tools/position-calculator/",
  "./tools/risk-exposure-calculator/",
  "./tools/trade-desk/",
  "./tools/monte-carlo/",
  "./journal/web-journal/",
  "./en/forex-guide/",
  "./en/tools/position-calculator/",
  "./en/tools/risk-exposure-calculator/",
  "./en/tools/trade-desk/",
  "./en/tools/monte-carlo/",
  "./en/journal/web-journal/",
  "./uz/forex-guide/",
  "./uz/tools/position-calculator/",
  "./uz/tools/risk-exposure-calculator/",
  "./uz/tools/trade-desk/",
  "./uz/tools/monte-carlo/",
  "./uz/journal/web-journal/",
  "./stylesheets/extra.css",
  "./stylesheets/calculators.css",
  "./javascripts/widgets/_i18n.js",
  "./javascripts/widgets/position.js",
  "./javascripts/widgets/risk-exposure.js",
  "./javascripts/widgets/trade-desk.js",
  "./javascripts/widgets/monte-carlo.js"
];

self.addEventListener("install", function (event) {
  event.waitUntil(caches.open(CACHE).then(function (cache) { return cache.addAll(CORE); }));
  self.skipWaiting();
});

self.addEventListener("activate", function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (key) { return key !== CACHE; }).map(function (key) { return caches.delete(key); }));
  }));
  self.clients.claim();
});

function offlinePage(url) {
  var scope = new URL(self.registration.scope).pathname;
  var relative = url.pathname.slice(scope.length);
  if (relative.indexOf("en/") === 0) return "./en/offline/";
  if (relative.indexOf("uz/") === 0) return "./uz/offline/";
  return "./offline/";
}

self.addEventListener("fetch", function (event) {
  if (event.request.method !== "GET") return;
  var url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  if (event.request.mode === "navigate") {
    event.respondWith(fetch(event.request).then(function (response) {
      var copy = response.clone();
      caches.open(CACHE).then(function (cache) { cache.put(event.request, copy); });
      return response;
    }).catch(function () {
      return caches.match(event.request).then(function (cached) {
        return cached || caches.match(offlinePage(url));
      });
    }));
    return;
  }
  event.respondWith(caches.match(event.request).then(function (cached) {
    var update = fetch(event.request).then(function (response) {
      if (response.ok) caches.open(CACHE).then(function (cache) { cache.put(event.request, response.clone()); });
      return response;
    }).catch(function () { return cached; });
    return cached || update;
  }));
});
