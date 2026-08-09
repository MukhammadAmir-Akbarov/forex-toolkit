"""Журнал на телефоне: ничего не должно вылезать за экран.

История дефекта. `.journal-breakdowns` — сетка с колонкой `1fr`. Такая колонка
не умеет сжиматься ниже минимальной ширины содержимого, а внутри лежит таблица
с `min-width: 680px`. Трек растягивался до 478px внутри контейнера в 300px.

Прокрутки при этом не появлялось — у `html` стоит `overflow-x: hidden`, — то
есть часть разбора журнала на телефоне была **обрезана и недоступна**. Именно
поэтому тест проверяет ширину элементов, а не `scrollWidth` страницы: страница
выглядела нормально, ломались её внутренности.

Появляется дефект только когда в журнале есть данные, поэтому демо-журнал
загружается обязательно.
"""

from __future__ import annotations

import pytest

PHONES = [(390, "iPhone 14"), (360, "Android"), (320, "старый маленький")]

# Что вылезает за экран, считаем по элементам виджета. Всё, что лежит внутри
# горизонтально прокручиваемого блока, законно: таблице шире экрана быть можно,
# если к ней можно прокрутить.
WIDER_THAN_SCREEN = """() => {
  const limit = document.documentElement.clientWidth;
  const wide = [];
  document.querySelectorAll('.journal-widget *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.right <= limit + 1) return;
    for (let p = el.parentElement; p; p = p.parentElement) {
      const o = getComputedStyle(p).overflowX;
      if (o === 'auto' || o === 'scroll') return;
    }
    wide.push({
      cls: String(el.className || '').slice(0, 40),
      width: Math.round(r.width),
      right: Math.round(r.right),
    });
  });
  return wide;
}"""


def _open_with_data(page, site_url, width):
    page.set_viewport_size({"width": width, "height": 844})
    page.goto(f"{site_url}/journal/web-journal/")
    page.wait_for_selector("#journal-demo")
    page.click("#journal-demo")
    page.wait_for_selector("#journal-tax-summary table")


@pytest.mark.parametrize("width,name", PHONES, ids=[p[1] for p in PHONES])
def test_nothing_sticks_out_of_the_screen(pw_page, site_url, width, name):
    page = pw_page
    _open_with_data(page, site_url, width)

    wide = page.evaluate(WIDER_THAN_SCREEN)
    assert not wide, (
        f"[{name}, {width}px] за экран вылезает {len(wide)} элементов, "
        f"первые: {wide[:3]}"
    )


def test_the_wide_table_is_reachable_by_scrolling(pw_page, site_url):
    """Поместиться можно и обрезав данные — это было бы хуже исходной болезни.

    Таблице шире экрана быть разрешено, но только внутри блока, к которому
    можно прокрутить.
    """
    page = pw_page
    _open_with_data(page, site_url, 390)

    reachable = page.evaluate("""() => {
      const boxes = [...document.querySelectorAll('.journal-table-scroll')];
      return boxes.map(b => ({
        scrolls: b.scrollWidth > b.clientWidth,
        overflowX: getComputedStyle(b).overflowX,
      }));
    }""")
    assert reachable, "на странице нет ни одной таблицы журнала"
    for box in reachable:
        assert box["overflowX"] in ("auto", "scroll"), box
    assert any(box["scrolls"] for box in reachable), (
        "ни одна таблица не прокручивается — похоже, данные обрезаны, а не "
        "убраны под прокрутку"
    )


def test_the_breakdown_grid_can_shrink(pw_page, site_url):
    """Прямая проверка причины: трек сетки не шире своего контейнера."""
    page = pw_page
    _open_with_data(page, site_url, 390)

    measured = page.evaluate("""() => {
      const grid = document.querySelector('.journal-breakdowns');
      if (!grid) return null;
      const item = grid.querySelector('.journal-breakdown');
      return {
        grid: Math.round(grid.getBoundingClientRect().width),
        item: item ? Math.round(item.getBoundingClientRect().width) : null,
      };
    }""")
    assert measured, "нет блока разбора — проверять нечего"
    assert measured["item"] <= measured["grid"], (
        f"элемент сетки шире контейнера: {measured['item']} > {measured['grid']} — "
        "колонка снова не умеет сжиматься (нужен minmax(0, 1fr) и min-width: 0)"
    )
