// Выполняет браузерный виджет вне браузера и зовёт одну из его чистых функций.
//
// Зачем: логика виджетов проверялась только через Playwright — 135 сценариев
// идут три с половиной минуты, и каждый поднимает браузер ради одного числа.
// Сами расчёты браузер не нужен: они не трогают DOM и уже выставлены наружу
// как window.__fx*. Здесь виджет выполняется в песочнице Node с заглушкой DOM,
// достаточной, чтобы он дошёл до конца и объявил свои функции.
//
// Что этим НЕ проверяется: отрисовка, обработчики, доступность, локализация
// интерфейса. Это остаётся за браузерными тестами — они про другое.
//
// Запуск:
//   node tests/widget_sandbox.mjs <файл-виджета> <имя функции> '<JSON-массив аргументов>'

import { readFileSync } from "node:fs";
import vm from "node:vm";

function stubElement() {
  const node = {
    innerHTML: "",
    textContent: "",
    value: "",
    hidden: false,
    className: "",
    style: {},
    classList: { add() {}, remove() {}, contains: () => false, toggle() {} },
    addEventListener() {},
    removeEventListener() {},
    appendChild() {},
    removeChild() {},
    setAttribute() {},
    getAttribute: () => null,
    removeAttribute() {},
    querySelectorAll: () => [],
    querySelector: () => null,
    closest: () => null,
    focus() {},
    click() {},
    getBoundingClientRect: () => ({ width: 0, height: 0, top: 0, left: 0 }),
    getContext: () => null,
  };
  node.parentNode = { insertBefore() {}, appendChild() {}, removeChild() {} };
  return node;
}

function buildSandbox(locale) {
  const document = {
    documentElement: { lang: locale },
    body: stubElement(),
    getElementById: () => stubElement(),
    querySelector: () => stubElement(),
    querySelectorAll: () => [],
    createElement: () => stubElement(),
    addEventListener() {},
  };

  const sandbox = {
    document,
    console,
    URLSearchParams,
    setTimeout,
    clearTimeout,
    requestAnimationFrame: (fn) => fn(),
    navigator: { storage: null, language: locale },
    localStorage: {
      store: {},
      getItem(key) {
        return Object.prototype.hasOwnProperty.call(this.store, key)
          ? this.store[key]
          : null;
      },
      setItem(key, value) {
        this.store[key] = String(value);
      },
      removeItem(key) {
        delete this.store[key];
      },
    },
    addEventListener() {},
    location: { search: "", href: "", pathname: "/" },
    // Виджеты, которые подгружают данные, обязаны дойти до конца и объявить
    // свои функции. Данные в песочнице не нужны: расчёт вызывается напрямую.
    fetch: () => Promise.reject(new Error("сеть в песочнице недоступна")),
  };
  sandbox.window = sandbox;

  // Общий хелпер виджетов. Форматирование здесь упрощённое — тесты сравнивают
  // числа, а не строки; за строки отвечают браузерные тесты.
  sandbox.FXW = {
    pick: (table) => table[locale] || table.ru,
    money: (value, frac) => "$" + Number(value).toFixed(frac == null ? 2 : frac),
    int: (value) => String(Math.round(Number(value))),
    pct: (value) => value + "%",
    escape: (value) => String(value == null ? "" : value),
  };
  return sandbox;
}

const [file, functionName, argsJson, locale = "ru"] = process.argv.slice(2);
const sandbox = buildSandbox(locale);
const context = vm.createContext(sandbox);

try {
  vm.runInContext(readFileSync(file, "utf8"), context);
} catch (error) {
  console.log(JSON.stringify({ error: "виджет не выполнился: " + error.message }));
  process.exit(0);
}

const fn = sandbox[functionName];
if (typeof fn !== "function") {
  const exposed = Object.keys(sandbox).filter((key) => key.startsWith("__fx"));
  console.log(
    JSON.stringify({
      error: `${functionName} не объявлена; виджет выставил: ${exposed.join(", ") || "ничего"}`,
    })
  );
  process.exit(0);
}

try {
  console.log(JSON.stringify({ result: fn(...JSON.parse(argsJson || "[]")) }));
} catch (error) {
  console.log(JSON.stringify({ error: "вызов упал: " + error.message }));
}
