// Линтер для браузерных виджетов.
//
// Зачем: в _mkdocs/javascripts лежит ~6300 строк, которые CI не проверял вообще
// — линтовался только Python. Уязвимость с innerHTML (PR #52) и опечатка в
// имени глобальной переменной — ровно те классы ошибок, которые здесь ловятся
// статически, до браузера.
//
// Правила намеренно узкие: ищем ошибки, а не спорим о стиле. Форматирование в
// этих файлах разное по историческим причинам, и переписывать его ради линтера
// смысла нет.

const BROWSER_GLOBALS = {
  window: "readonly",
  document: "readonly",
  navigator: "readonly",
  localStorage: "readonly",
  sessionStorage: "readonly",
  location: "readonly",
  console: "readonly",
  fetch: "readonly",
  caches: "readonly",
  URL: "readonly",
  URLSearchParams: "readonly",
  Blob: "readonly",
  FileReader: "readonly",
  Image: "readonly",
  Intl: "readonly",
  setTimeout: "readonly",
  clearTimeout: "readonly",
  setInterval: "readonly",
  clearInterval: "readonly",
  requestAnimationFrame: "readonly",
  matchMedia: "readonly",
  getComputedStyle: "readonly",
  alert: "readonly",
  confirm: "readonly",
  CustomEvent: "readonly",
  Event: "readonly",
  DOMParser: "readonly",
  TextDecoder: "readonly",
  self: "readonly",
  performance: "readonly",
  IntersectionObserver: "readonly",
  NodeFilter: "readonly",
  CSS: "readonly",
  // Material for MkDocs отдаёт наблюдаемую смену страницы при instant loading —
  // без неё скрипты не переинициализируются после перехода без перезагрузки.
  document$: "readonly",
  // Виджеты общаются между собой через window, но часть кода зовёт эти имена
  // напрямую — перечисляем, чтобы no-undef ловил настоящие опечатки.
  FXW: "readonly",
  fxTrack: "readonly",
};

export default [
  {
    files: ["_mkdocs/javascripts/**/*.js"],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "script",
      globals: BROWSER_GLOBALS,
    },
    rules: {
      // Настоящие ошибки.
      "no-undef": "error",
      // caughtErrors: "none" — в проекте принято `catch (e) {}` вокруг
      // localStorage: приватный режим кидает исключение, и виджет должен
      // просто продолжить работу. Это приём, а не забытая переменная.
      "no-unused-vars": ["error", { args: "none", caughtErrors: "none" }],
      "no-redeclare": "error",
      "no-unreachable": "error",
      "no-dupe-keys": "error",
      "no-dupe-args": "error",
      "no-duplicate-case": "error",
      "no-self-assign": "error",
      "no-self-compare": "error",
      "no-constant-condition": "error",
      "no-fallthrough": "error",
      "no-cond-assign": "error",
      "use-isnan": "error",
      "valid-typeof": "error",
      // Ловушки, на которых этот проект уже обжигался.
      eqeqeq: ["error", "smart"],
      "no-implied-eval": "error",
      "no-new-func": "error",
      "no-script-url": "error",
    },
  },
  {
    // Service worker живёт в своём окружении.
    files: ["_mkdocs/service-worker.js"],
    languageOptions: {
      globals: { ...BROWSER_GLOBALS, clients: "readonly", skipWaiting: "readonly" },
    },
  },
];
