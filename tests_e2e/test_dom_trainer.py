"""Тренажёр DOM/ленты — order flow учится практикой, а не статьёй.

Симуляция синтетическая и недетерминированная (скрытый нажим случаен),
поэтому проверяем поведение, а не числа:

* раунд сам проигрывает 25 тиков наблюдения и останавливается для прогноза;
* до конца наблюдения кнопки прогноза заблокированы;
* после прогноза доигрываются 5 тиков и показывается честный разбор;
* десять раундов заканчиваются вердиктом серии (5/10 — монетка, а не навык).

Время гоняется через playwright clock — прогон мгновенный.
"""

from __future__ import annotations

TICK_MS = 400
WATCH = 25
REVEAL = 5


def _open(page, site_url, path="/tools/dom-trainer/"):
    page.clock.install()
    page.goto(f"{site_url}{path}")
    page.wait_for_selector("#dom-first")


def _play_round(page, first: bool):
    """Один раунд: наблюдение → прогноз ⬆ → доигровка → разбор."""
    page.click("#dom-first" if first else "#dom-next")
    page.clock.run_for(WATCH * TICK_MS + TICK_MS)
    assert page.locator("#dom-up").is_enabled(), (
        "после 25 тиков наблюдения кнопка прогноза не разблокировалась"
    )
    page.click("#dom-up")
    page.clock.run_for(REVEAL * TICK_MS + TICK_MS)
    status = page.locator("#dom-status").inner_text()
    assert any(mark in status for mark in ("✅", "❌", "➖")), (
        f"после доигровки нет честного разбора, статус: {status!r}"
    )


def test_round_stops_for_prediction_after_watch_phase(site_url, pw_page):
    page = pw_page
    _open(page, site_url)

    page.click("#dom-first")
    assert page.locator("#dom-up").is_disabled(), (
        "кнопки прогноза должны быть заблокированы, пока идёт наблюдение"
    )
    page.clock.run_for(WATCH * TICK_MS + TICK_MS)
    assert page.locator("#dom-up").is_enabled()
    assert page.locator("#dom-down").is_enabled()


def test_prediction_reveals_ticks_and_shows_breakdown(site_url, pw_page):
    page = pw_page
    _open(page, site_url)

    _play_round(page, first=True)

    assert page.locator("#dom-next").is_visible(), (
        "после разбора не появилась кнопка следующего раунда"
    )


def test_full_series_ends_with_a_verdict(site_url, pw_page):
    page = pw_page
    _open(page, site_url)

    _play_round(page, first=True)
    for _ in range(9):
        _play_round(page, first=False)

    assert page.locator(".dom-verdict").is_visible(), (
        "после десяти раундов нет вердикта серии"
    )
    # После серии кнопка предлагает начать заново, а не «раунд 11».
    assert page.locator("#dom-next").is_visible()


def test_widget_renders_in_english_and_uzbek(site_url, pw_page):
    page = pw_page

    page.clock.install()
    page.goto(f"{site_url}/en/tools/dom-trainer/")
    page.wait_for_selector("#dom-first")
    page.click("#dom-first")
    page.clock.run_for(WATCH * TICK_MS + TICK_MS)
    assert "stopped" in page.locator("#dom-status").inner_text().lower()

    page.clock.install()
    page.goto(f"{site_url}/uz/tools/dom-trainer/")
    page.wait_for_selector("#dom-first")
    page.click("#dom-first")
    page.clock.run_for(WATCH * TICK_MS + TICK_MS)
    assert "to'xtadi" in page.locator("#dom-status").inner_text()
