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
            // Именно .md-select: у него position: relative и свой z-index,
            // то есть он и создаёт контекст наложения. Раньше здесь мерился
            // .md-select__list — статический элемент, на котором z-index не
            // действует вовсе, и тест зеленел при живом баге.
            zIndex: getComputedStyle(sel).zIndex,
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
    """Вкладки липкие: без большего z-index список окажется под ними.

    Проверяется `.md-select`, а не его внутренности. У `.md-select` есть
    `position: relative` и собственный z-index — он создаёт контекст наложения,
    и любое число внутри него уже ни на что не влияет.

    Первая версия этого теста мерила `.md-select__list` и была бесполезной:
    у того `position: static`, z-index не применяется, и тест проходил, пока
    первый пункт списка был реально закрыт вкладками.
    """
    state = open_switcher(pw_page, site_url, 1440)

    assert state["zIndex"] != "auto", (
        "у .md-select нет своего z-index — список уйдёт под липкие вкладки"
    )
    assert int(state["zIndex"]) > int(state["tabsZIndex"]), (
        f"переключатель z-index {state['zIndex']} против вкладок {state['tabsZIndex']}"
    )


# ── Пункт может быть на месте и всё равно не работать ──────────────────────
# Эти тесты дописаны после реального дефекта: на узбекской версии «Русский»
# был в разметке, но его закрывала липкая строка вкладок — вернуться на русский
# было нельзя. Прошлые проверки этого файла смотрели на ПОЛОЖЕНИЕ панели и
# ничего не заметили: пункт лежал внутри неё и по геометрии был «виден».
#
# Поэтому здесь проверяется не геометрия, а `document.elementFromPoint()` —
# он отвечает на единственный важный вопрос: что произойдёт при клике.

CLICKABILITY = """() => {
  return [...document.querySelectorAll('.md-select__link')].map(a => {
    const r = a.getBoundingClientRect();
    const el = document.elementFromPoint(
      Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2));
    const ok = el === a || a.contains(el);
    return {
      text: a.textContent.trim(),
      href: a.getAttribute('href'),
      clickable: ok,
      covered_by: ok ? null : (el ? el.tagName.toLowerCase() + '.' +
        String(el.className || '').split(' ')[0] : 'ничего'),
    };
  });
}"""

PSYCHOLOGY = {
    "ru": "/extras/psychology/",
    "en": "/en/extras/psychology/",
    "uz": "/uz/extras/psychology/",
}


@pytest.mark.parametrize("locale", list(PSYCHOLOGY), ids=list(PSYCHOLOGY))
def test_every_language_is_clickable(pw_page, site_url, locale):
    """Все три языка должны нажиматься — из любой локали.

    Самый дорогой случай: с узбекской версии нельзя вернуться на русский.
    Русский стоит в списке ПЕРВЫМ, а первый пункт и закрывала строка вкладок.
    """
    page = pw_page
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(f"{site_url}{PSYCHOLOGY[locale]}")
    page.wait_for_selector(".md-select")
    page.hover(".md-select")
    page.wait_for_timeout(400)

    links = page.evaluate(CLICKABILITY)
    assert len(links) == 3, f"[{locale}] языков в списке {len(links)}, а не три"

    blocked = [item for item in links if not item["clickable"]]
    assert not blocked, (
        f"[{locale}] пункт не нажимается: {blocked[0]['text']} — "
        f"сверху лежит {blocked[0]['covered_by']}"
    )


def test_switching_from_uzbek_back_to_russian_actually_works(pw_page, site_url):
    """Проверка целиком: клик по «Русский» с узбекской страницы уводит на неё же
    по-русски, а не на главную и не в никуда."""
    page = pw_page
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(f"{site_url}/uz/extras/psychology/")
    page.wait_for_selector(".md-select")
    page.hover(".md-select")
    page.wait_for_timeout(400)

    russian = page.locator('.md-select__link[hreflang="ru"]')
    assert russian.count() == 1, "в списке нет русского"

    with page.expect_navigation(wait_until="domcontentloaded"):
        russian.click()

    assert "/uz/" not in page.url, f"остались в узбекской версии: {page.url}"
    assert page.url.rstrip("/").endswith("extras/psychology"), (
        f"ушли не на ту страницу: {page.url}"
    )
    assert page.locator('html[lang="ru"]').count() == 1, "язык страницы не русский"
