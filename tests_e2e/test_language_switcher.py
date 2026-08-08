"""Положение выпадающего списка языков.

Material центрирует список по кнопке (``left: 24px`` плюс ``translateX(-50%)``),
из-за чего на широком экране он свисает на 41px влево — на соседние вкладки, и
непонятно, чей он. Прижимаем левый край к кнопке, но только там, где вкладки
существуют: ниже 1220px кнопка стоит близко к правому краю, и прижатая влево
панель вылезает за экран. Это не догадка — замерено: 414px при окне 390px.

Тест проверяет обе стороны правки, потому что первая версия чинила широкий
экран и ломала телефон.
"""

from __future__ import annotations

import pytest

PAGE = "/docs/strategy-details/"

# Ширина, с которой Material показывает вкладки и включается наше выравнивание.
TABS_BREAKPOINT = 1220


def open_switcher(page, site_url, width, height=900):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(f"{site_url}{PAGE}")
    page.wait_for_selector(".md-select")
    page.hover(".md-select")
    page.wait_for_timeout(300)
    return page.evaluate(
        """() => {
          const sel = document.querySelector('.md-select');
          const btn = sel.querySelector('.md-header__button');
          const inner = sel.querySelector('.md-select__inner');
          const box = e => {
            const r = e.getBoundingClientRect();
            return {x: r.x, y: r.y, right: r.right, bottom: r.bottom};
          };
          const b = box(btn), p = box(inner);
          return {
            offset: p.x - b.x,
            gap: p.y - b.bottom,
            overflowsRight: p.right > window.innerWidth,
            overflowsLeft: p.x < 0,
            zIndex: getComputedStyle(sel.querySelector('.md-select__list')).zIndex,
            tabsZIndex: getComputedStyle(document.querySelector('.md-tabs')).zIndex,
            border: getComputedStyle(inner).borderTopWidth,
          };
        }"""
    )


@pytest.mark.parametrize("width", [390, 768, 1024, 1280, 1440, 1920])
def test_dropdown_never_leaves_the_screen(pw_page, site_url, width):
    """Главная проверка: панель видна целиком на любой ширине."""
    state = open_switcher(pw_page, site_url, width)

    assert not state["overflowsRight"], f"{width}px: панель уехала за правый край"
    assert not state["overflowsLeft"], f"{width}px: панель уехала за левый край"


@pytest.mark.parametrize("width", [1280, 1440, 1920])
def test_dropdown_sits_under_its_button_on_wide_screens(pw_page, site_url, width):
    """Иначе панель висит над чужими вкладками и непонятно, чья она."""
    state = open_switcher(pw_page, site_url, width)

    assert abs(state["offset"]) <= 8, (
        f"{width}px: левый край панели в {state['offset']}px от кнопки — "
        "она снова свисает вбок"
    )


@pytest.mark.parametrize("width", [390, 768])
def test_narrow_screens_keep_the_default_placement(pw_page, site_url, width):
    """На узких оставляем поведение Material — прижатая влево панель там не влезает."""
    state = open_switcher(pw_page, site_url, width)

    assert state["offset"] < -8, (
        f"{width}px: выравнивание для широких экранов применилось к узкому"
    )


def test_dropdown_is_separated_from_the_header(pw_page, site_url):
    """Без отступа и рамки панель сливается со строкой вкладок в одну поверхность."""
    state = open_switcher(pw_page, site_url, 1440)

    assert state["gap"] >= 4, f"зазор {state['gap']}px — панель прилипла к шапке"
    assert state["border"] != "0px", "у панели нет рамки"


def test_dropdown_stays_above_the_sticky_tabs(pw_page, site_url):
    """Вкладки липкие: без большего z-index список окажется под ними."""
    state = open_switcher(pw_page, site_url, 1440)

    assert int(state["zIndex"]) > int(state["tabsZIndex"]), (
        f"список z-index {state['zIndex']} против вкладок {state['tabsZIndex']}"
    )
