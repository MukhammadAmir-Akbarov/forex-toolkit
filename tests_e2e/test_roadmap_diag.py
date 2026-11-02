"""Адаптивная дорожная карта: диагностика вычёркивает известные уровни.

Проверяем контракт, а не содержание вопросов:
* на всех локалях виджет поднимается и вопросов столько, сколько заявлено;
* 20 правильных ответов → все уровни 0–4 вычеркнуты, отметки переживают
  перезагрузку (localStorage);
* уровень с <3 правильных из 4 не вычеркивается — «знаю» и «угадывал» —
  разные состояния;
* сброс возвращает карту в чистый вид.

Правильность ответа тест узнаёт из того же JSON-блока, что читает страница:
вопросы поменяют — тест останется честным.
"""

from __future__ import annotations

import pytest

LOCALES = ["", "en/", "uz/"]


def _open(page, site_url, prefix):
    page.goto(f"{site_url}/{prefix}roadmap/")
    page.wait_for_selector("#rd-start")


def _bank(page):
    return page.evaluate(
        "() => JSON.parse(document.getElementById('diag-questions').textContent)"
    )


def _answer_all(page, bank, fail_level=None):
    """Пройти диагностику; на fail_level специально отвечать неверно.

    Порядок вопросов и вариантов перемешан — вопрос опознаём по тексту,
    а не по номеру в банке.
    """
    page.click("#rd-start")
    by_text = {q["q"]: q for q in bank}
    for _ in bank:
        page.wait_for_selector(".rd-opt")
        shown = page.locator(".rd-q").inner_text()
        q = by_text[shown]
        options = page.locator(".rd-opt")
        target = None
        for i in range(options.count()):
            text = options.nth(i).inner_text()
            correct = text == q["options"][q["answer"]]
            if fail_level is not None and q["level"] == fail_level:
                correct = not correct
            if correct:
                target = i
                break
        assert target is not None, f"не нашёл нужный вариант для «{shown[:40]}…»"
        options.nth(target).click()
    page.wait_for_selector(".rd-levels")


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_diag_widget_loads_on_every_locale(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)
    bank = _bank(page)
    assert len(bank) == 20, f"[{prefix or 'ru'}] в банке не 20 вопросов"
    levels = sorted({q["level"] for q in bank})
    assert levels == [0, 1, 2, 3, 4]
    # Карта должна нести data-level на всех пяти проверяемых уровнях.
    for level in levels:
        assert page.locator(f'.fx-rm__item[data-level="{level}"]').count() == 1


def test_perfect_run_crosses_out_all_levels_and_persists(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")
    _answer_all(page, _bank(page))

    assert page.locator(".rd-row--pass").count() == 5
    assert page.locator(".fx-rm__item--known").count() == 5

    page.reload()
    page.wait_for_selector("#rd-start")
    assert page.locator(".fx-rm__item--known").count() == 5, (
        "отметки не пережили перезагрузку — localStorage не записался"
    )


def test_level_below_the_bar_is_not_crossed_out(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")
    _answer_all(page, _bank(page), fail_level=2)

    assert page.locator(".rd-row--pass").count() == 4
    assert page.locator(".rd-row--fail").count() == 1
    assert page.locator('.fx-rm__item[data-level="2"].fx-rm__item--known').count() == 0


def test_reset_clears_the_marks(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")
    _answer_all(page, _bank(page))
    assert page.locator(".fx-rm__item--known").count() == 5

    page.reload()
    page.wait_for_selector("#rd-start")
    page.click("#rd-reset")
    assert page.locator(".fx-rm__item--known").count() == 0
