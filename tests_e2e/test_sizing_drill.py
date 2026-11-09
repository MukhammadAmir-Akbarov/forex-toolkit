"""Дрель сайзинга: лот за 20 секунд — в настоящем браузере.

Задачи случайны, поэтому проверяем поведение, а не числа:

* задача открывается с четырьмя вариантами и живым таймером;
* ответ подсвечивает верный вариант и показывает разбор формулы;
* таймаут засчитывается как промах, серия не встаёт;
* десять задач заканчиваются вердиктом серии;
* страница работает на всех трёх локалях.

Время гоняется через playwright clock — прогон мгновенный.
"""

from __future__ import annotations

SECONDS = 20


def _open(page, site_url, path="/tools/sizing-drill/"):
    page.clock.install()
    page.goto(f"{site_url}{path}")
    page.wait_for_selector("#sd-start")


def _start(page):
    page.click("#sd-start")
    page.wait_for_selector(".sd-opt[data-v]")


def test_question_has_four_options_and_a_live_timer(site_url, pw_page):
    page = pw_page
    _open(page, site_url)
    _start(page)

    assert page.locator(".sd-opt[data-v]").count() == 4
    assert "20" in page.locator("#sd-clock").inner_text()
    page.clock.run_for(3000)
    assert "17" in page.locator("#sd-clock").inner_text(), (
        "таймер не тикает — задача без давления времени"
    )


def test_answer_highlights_the_right_option_and_shows_formula(site_url, pw_page):
    page = pw_page
    _open(page, site_url)
    _start(page)

    page.locator(".sd-opt[data-v]").first.click()

    assert page.locator(".sd-opt.sd-hit").count() == 1, (
        "правильный вариант не подсвечен после ответа"
    )
    assert "÷" in page.locator(".sd-explain").inner_text(), "разбор формулы не показан"
    assert page.locator("#sd-next").is_visible()


def test_timeout_counts_as_a_miss_and_the_series_moves_on(site_url, pw_page):
    page = pw_page
    _open(page, site_url)
    _start(page)

    page.clock.run_for((SECONDS + 1) * 1000)

    assert "⏱" in page.locator(".sd-status").inner_text(), (
        "таймаут не засчитан промахом"
    )
    assert page.locator("#sd-next").is_visible(), "серия встала после таймаута"


def test_full_series_ends_with_a_verdict(site_url, pw_page):
    page = pw_page
    _open(page, site_url)
    _start(page)

    for _ in range(10):
        page.locator(".sd-opt[data-v]").first.click()
        page.click("#sd-next")

    assert page.locator(".sd-verdict").is_visible(), (
        "после десяти задач нет вердикта серии"
    )
    assert page.locator("#sd-again").is_visible()


def test_page_renders_in_english_and_uzbek(site_url, pw_page):
    page = pw_page

    _open(page, site_url, "/en/tools/sizing-drill/")
    page.click("#sd-start")
    page.wait_for_selector(".sd-opt[data-v]")
    assert "Problem 1 of 10" in page.locator(".sd-meta").first.inner_text()

    _open(page, site_url, "/uz/tools/sizing-drill/")
    page.click("#sd-start")
    page.wait_for_selector(".sd-opt[data-v]")
    assert "masaladan 1" in page.locator(".sd-meta").first.inner_text()
