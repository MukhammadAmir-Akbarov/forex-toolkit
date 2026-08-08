"""Сверка «трёх самых дорогих привычек»: браузер == Python."""

from __future__ import annotations

import pytest

from forex_toolkit.habits import expensive_habits, months_in


def trade(day, pnl, rules="yes", emotion="calm", pair="EURUSD", setup="a"):
    return {
        "date": f"2026-03-{day:02d}",
        "pnl": pnl,
        "rules": rules,
        "emotion": emotion,
        "pair": pair,
        "setup": setup,
    }


CASES = {
    "нарушение плана дорого обходится": (
        [trade(i, 10.0) for i in range(1, 7)]
        + [trade(i, -30.0, rules="no") for i in range(10, 14)]
    ),
    "эмоция и пара вместе": (
        [trade(i, 12.0) for i in range(1, 8)]
        + [trade(i, -25.0, emotion="fomo", pair="GBPJPY") for i in range(10, 14)]
    ),
    "дисциплинированный месяц": [trade(i, 5.0) for i in range(1, 12)],
    "привычка по двум сделкам не считается": (
        [trade(i, 8.0) for i in range(1, 10)]
        + [trade(i, -500.0, rules="no") for i in range(20, 22)]
    ),
    "битые суммы": (
        [trade(i, 9.0) for i in range(1, 7)]
        + [trade(i, -20.0, rules="no") for i in range(10, 14)]
        + [trade(15, None, rules="no")]
    ),
}


@pytest.mark.parametrize("name", list(CASES), ids=list(CASES))
def test_browser_matches_python(pw_page, site_url, name):
    trades = CASES[name]
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.wait_for_function("() => typeof window.__fxHabits === 'function'")

    got = page.evaluate("rows => window.__fxHabits(rows, 3)", trades)
    expected = [habit.as_dict() for habit in expensive_habits(trades, limit=3)]

    assert len(got) == len(expected), f"{name}: разное число привычек"
    for browser, python in zip(got, expected):
        assert browser["key"] == python["key"], f"{name}: разные привычки"
        assert browser["trades"] == python["trades"]
        for field in ("total", "avg_with", "avg_without", "cost"):
            assert round(browser[field], 2) == python[field], (
                f"{name}: {field} разошлось — браузер {browser[field]}, "
                f"Python {python[field]}"
            )


def test_months_agree(pw_page, site_url):
    trades = [
        trade(1, 1.0),
        {"date": "2026-01-15", "pnl": 2.0},
        {"date": "не дата", "pnl": 3.0},
    ]
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.wait_for_function("() => typeof window.__fxMonths === 'function'")

    assert page.evaluate("rows => window.__fxMonths(rows)", trades) == months_in(trades)


def test_month_picker_switches_the_period(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/journal/web-journal/")
    page.click("#journal-demo")
    page.wait_for_selector("#journal-habits-month")

    options = page.locator("#journal-habits-month option")
    assert options.count() >= 1
    first = page.text_content("#journal-habits")

    if options.count() > 1:
        page.select_option(
            "#journal-habits-month", options.nth(1).get_attribute("value")
        )
        assert page.text_content("#journal-habits") != first


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_habits_block_is_translated(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}journal/web-journal/")
    page.click("#journal-demo")
    page.wait_for_selector("#journal-habits")

    text = page.text_content("#journal-habits")
    assert text.strip() and "undefined" not in text, f"[{prefix}] {text[:80]!r}"
