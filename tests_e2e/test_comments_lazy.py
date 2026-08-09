"""Комментарии giscus не должны стоить ничего тем, кто до них не долистал.

giscus подключается на 365 страницах из 366. Его клиент тянет за собой iframe
с giscus.app и данными GitHub, то есть эагерная загрузка — это внешний запрос
на каждой странице учебника. Ровно тот вес, ради снятия которого калькуляторы
разнесли по своим страницам (38 KB gzip → 17.9 KB глобально).

Поэтому скрипт создаётся из IntersectionObserver, когда блок комментариев
попадает в область видимости. Тест проверяет обе половины утверждения: до
прокрутки запроса нет, после прокрутки — есть. Внешние запросы в этих тестах
заблокированы фикстурой, но факт попытки виден в page.on("request").
"""

from __future__ import annotations

import pytest

# Длинная страница: блок комментариев заведомо ниже первого экрана, иначе
# observer сработает сразу и тест перестанет что-либо проверять.
LONG_PAGE = "/docs/technical-analysis/"


@pytest.fixture
def giscus_requests(pw_page):
    """Собирать все обращения к giscus.app по ходу теста."""
    seen: list[str] = []
    pw_page.on(
        "request",
        lambda request: (
            seen.append(request.url) if "giscus.app" in request.url else None
        ),
    )
    return seen


def test_comments_block_is_rendered(pw_page, site_url) -> None:
    """Сам блок на странице есть — иначе следующий тест ничего не докажет."""
    pw_page.goto(f"{site_url}{LONG_PAGE}", wait_until="domcontentloaded")
    assert pw_page.locator("#__giscus-mount").count() == 1
    assert pw_page.locator("#__comments").count() == 1


def test_giscus_is_not_loaded_before_scrolling(
    pw_page, site_url, giscus_requests
) -> None:
    # `load`, а не `networkidle`: внешние запросы в этих тестах обрываются
    # фикстурой, и «тишина в сети» наступает в непредсказуемый момент.
    pw_page.goto(f"{site_url}{LONG_PAGE}", wait_until="load")
    pw_page.wait_for_timeout(700)

    assert giscus_requests == [], (
        f"giscus загрузился без прокрутки — вес на каждой странице: {giscus_requests}"
    )


def test_giscus_loads_after_scrolling_to_comments(
    pw_page, site_url, giscus_requests
) -> None:
    pw_page.goto(f"{site_url}{LONG_PAGE}", wait_until="load")
    pw_page.locator("#__comments").scroll_into_view_if_needed()

    pw_page.wait_for_function(
        "() => document.querySelector('#__giscus-mount script') !== null",
        timeout=10000,
    )
    assert any("giscus.app" in url for url in giscus_requests), (
        "после прокрутки к комментариям giscus так и не запросили"
    )


def test_locale_pages_ask_giscus_for_a_language_it_knows(pw_page, site_url) -> None:
    """У giscus нет узбекского: UZ-страница должна просить английский.

    Молчаливый русский на узбекской странице читатель не заказывал, а
    несуществующий код языка giscus просто проигнорирует.
    """
    expected = {"/": "ru", "/en/": "en", "/uz/": "en"}
    for path, lang in expected.items():
        pw_page.goto(f"{site_url}{path}", wait_until="domcontentloaded")
        mount = pw_page.locator("#__giscus-mount")
        assert mount.get_attribute("data-giscus-lang") == lang, path
