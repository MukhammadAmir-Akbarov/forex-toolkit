"""Напоминания о повторении карточек — баннер и кнопка включения.

Проверяем честную механику статичного сайта (push-сервера нет):

* кнопка на странице карточек включает напоминания (ключ в localStorage);
* если сегодня карточки не повторяли — баннер приходит на любую страницу;
* «Позже» прячет баннер до завтра;
* повторил сегодня — баннера нет.
"""

from __future__ import annotations


def _enable_reminders(page, site_url):
    page.goto(f"{site_url}/tools/flashcards/")
    page.wait_for_selector("#ftk-remind-toggle")
    page.click("#ftk-remind-toggle")
    assert page.evaluate("localStorage.getItem('ftk-remind-enabled')") == "1", (
        "кнопка не включила напоминания"
    )


def test_toggle_on_flashcards_page_enables_reminders(site_url, pw_page):
    page = pw_page
    page.goto(f"{site_url}/tools/flashcards/")
    page.wait_for_selector("#ftk-remind-toggle")

    page.click("#ftk-remind-toggle")

    assert page.evaluate("localStorage.getItem('ftk-remind-enabled')") == "1"
    assert "🔔" in page.locator("#ftk-remind-toggle").inner_text()


def test_banner_appears_when_review_is_due(site_url, pw_page):
    page = pw_page
    _enable_reminders(page, site_url)

    page.goto(f"{site_url}/tools/seasonality/")

    banner = page.locator("#ftk-remind-banner")
    banner.wait_for()
    assert "🎴" in banner.inner_text()
    assert banner.locator("a").get_attribute("href").endswith("/tools/flashcards/")


def test_later_button_snoozes_the_banner_until_tomorrow(site_url, pw_page):
    page = pw_page
    _enable_reminders(page, site_url)
    page.goto(f"{site_url}/tools/seasonality/")
    page.locator("#ftk-remind-banner").wait_for()

    page.click("#ftk-remind-later")

    assert page.locator("#ftk-remind-banner").count() == 0
    page.goto(f"{site_url}/tools/market-analytics/")
    page.wait_for_timeout(2000)  # баннер даёт себя ждать 1.5 с
    assert page.locator("#ftk-remind-banner").count() == 0, (
        "после «Позже» баннер всплыл на другой странице в тот же день"
    )


def test_no_banner_when_cards_reviewed_today(site_url, pw_page):
    page = pw_page
    _enable_reminders(page, site_url)
    page.evaluate(
        "localStorage.setItem('ftk-flash-lastday',"
        " new Date().toISOString().slice(0, 10))"
    )

    page.goto(f"{site_url}/tools/seasonality/")
    page.wait_for_timeout(2000)

    assert page.locator("#ftk-remind-banner").count() == 0, (
        "карточки повторены сегодня, а баннер всё равно всплыл"
    )


def test_banner_speaks_english_and_uzbek(site_url, pw_page):
    page = pw_page
    _enable_reminders(page, site_url)

    page.goto(f"{site_url}/en/tools/seasonality/")
    assert "not reviewed" in page.locator("#ftk-remind-banner").inner_text()

    page.goto(f"{site_url}/uz/tools/seasonality/")
    assert "takrorlanmadi" in page.locator("#ftk-remind-banner").inner_text()
