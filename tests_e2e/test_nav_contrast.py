"""Контраст верхних вкладок — обе темы, WCAG AA.

Зачем отдельный тест. Полоса вкладок в светлой теме — это НЕ белый лист, её
красит Material в ``--md-primary-fg-color`` (индиго #3f51b5). Активный пункт
когда-то красился в ``--fx-accent``, а он в светлой теме тоже индиго —
получилось 1.09:1, надпись физически была на странице, но её нельзя было
прочитать. Обычный тест «текст на месте» такое пропускает: элемент есть,
текст есть, ``is_visible()`` истинно.

Поэтому проверяем не наличие, а измеримое: реальный контраст. Считаем как
браузер — накладываем цвет текста (с учётом ``opacity``) на фактический фон,
а фон собираем композицией ``background-color`` по цепочке предков, потому что
плашка активного пункта полупрозрачная и сама по себе ничего не значит.
"""

from __future__ import annotations

import pytest

# Порог AA для обычного текста. Вкладки набраны 13.2px — это НЕ «крупный текст»
# по WCAG (нужно ≥18.66px полужирного или ≥24px), послабление 3:1 не подходит.
AA_NORMAL = 4.5

_MEASURE = """
(sel) => {
  const parse = (c) => {
    const m = c.match(/[\\d.]+/g).map(Number);
    return m.length === 3 ? [...m, 1] : m;
  };
  const over = (fg, bg) => {
    const a = fg[3];
    return [0, 1, 2].map((i) => fg[i] * a + bg[i] * (1 - a)).concat([1]);
  };
  const el = document.querySelector(sel);
  if (!el) return null;

  // Фон: снизу вверх до первого непрозрачного слоя, затем накладываем обратно.
  const stack = [];
  for (let n = el; n; n = n.parentElement) {
    const bg = parse(getComputedStyle(n).backgroundColor);
    if (bg[3] > 0) stack.push(bg);
    if (bg[3] === 1) break;
  }
  let bg = stack.pop() || [255, 255, 255, 1];
  while (stack.length) bg = over(stack.pop(), bg);

  const cs = getComputedStyle(el);
  const raw = parse(cs.color);
  const op = parseFloat(cs.opacity);
  const text = over([raw[0], raw[1], raw[2], raw[3] * op], bg);

  const lum = (c) => {
    const s = [0, 1, 2].map((i) => {
      const v = c[i] / 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2];
  };
  const l1 = lum(text);
  const l2 = lum(bg);
  const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  return {
    text: text.slice(0, 3).map(Math.round),
    bg: bg.slice(0, 3).map(Math.round),
    fontPx: parseFloat(cs.fontSize),
    ratio: Math.round(ratio * 100) / 100,
  };
}
"""

ACTIVE = ".md-tabs__item--active .md-tabs__link"
IDLE = ".md-tabs__item:not(.md-tabs__item--active) .md-tabs__link"


def _open_wide(page, site_url, scheme):
    """Строка вкладок существует только от 1220px — ниже её заменяет ☰."""
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(f"{site_url}/docs/technical-analysis/")
    page.evaluate(
        """(s) => {
             document.body.setAttribute('data-md-color-scheme', s);
             document.documentElement.setAttribute('data-md-color-scheme', s);
           }""",
        scheme,
    )
    page.wait_for_selector(".md-tabs__item--active")


@pytest.mark.parametrize("scheme", ["default", "slate"])
@pytest.mark.parametrize("what,sel", [("активная", ACTIVE), ("обычная", IDLE)])
def test_tab_text_is_readable(pw_page, site_url, scheme, what, sel):
    page = pw_page
    _open_wide(page, site_url, scheme)

    got = page.evaluate(_MEASURE, sel)
    assert got is not None, f"[{scheme}] не найдена {what} вкладка"
    assert got["ratio"] >= AA_NORMAL, (
        f"[{scheme}] {what} вкладка: контраст {got['ratio']}:1 при норме "
        f"{AA_NORMAL}:1 — текст {got['text']} на фоне {got['bg']}, "
        f"кегль {got['fontPx']}px"
    )


@pytest.mark.parametrize("scheme", ["default", "slate"])
def test_active_tab_is_distinguishable(pw_page, site_url, scheme):
    """Читаемости мало: активный раздел должен ещё и отличаться от остальных.

    Иначе «починка контраста» вида «покрасить всё одинаково белым» прошла бы
    предыдущий тест и отняла у шапки единственный указатель «вы здесь».
    """
    page = pw_page
    _open_wide(page, site_url, scheme)

    active = page.evaluate(_MEASURE, ACTIVE)
    idle = page.evaluate(_MEASURE, IDLE)
    assert active["text"] != idle["text"] or active["bg"] != idle["bg"], (
        f"[{scheme}] активная вкладка неотличима от обычной: "
        f"текст {active['text']}, фон {active['bg']}"
    )
