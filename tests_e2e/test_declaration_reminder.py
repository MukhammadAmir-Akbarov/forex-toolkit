"""Напоминание о налоговой декларации в кабинете.

Декларация подаётся до 1 апреля за прошедший год, а узнаёт человек об этом из
статьи, прочитанной полгода назад. Напоминание должно появляться само — но
только когда оно уместно, иначе это шум девять месяцев в году.

Дату подменяем: иначе тест проходил бы только зимой и молча «зеленел» летом.
"""

from __future__ import annotations

import json

import pytest

JOURNAL_KEY = "forex_journal_data_v2"


def seed(page, rows):
    page.evaluate(
        "([key, rows]) => localStorage.setItem(key, JSON.stringify({rows: rows}))",
        [JOURNAL_KEY, rows],
    )


def freeze(page, iso):
    """Замораживает часы страницы до загрузки виджета."""
    page.add_init_script(
        """
        (() => {
          const fixed = new Date(%s).getTime();
          const Real = Date;
          class Frozen extends Real {
            constructor(...args) { super(...(args.length ? args : [fixed])); }
            static now() { return fixed; }
          }
          window.Date = Frozen;
        })();
        """
        % json.dumps(iso)
    )


@pytest.mark.parametrize(
    ("today", "visible", "why"),
    [
        ("2026-01-15T10:00:00Z", True, "январь — срок близко"),
        ("2026-03-31T10:00:00Z", True, "последний день перед сроком"),
        ("2026-04-02T10:00:00Z", False, "срок прошёл"),
        ("2026-08-10T10:00:00Z", False, "середина года — это был бы шум"),
    ],
)
def test_reminder_appears_only_in_the_months_before_the_deadline(
    pw_page, site_url, today, visible, why
):
    page = pw_page
    page.goto(f"{site_url}/extras/dashboard/")
    seed(page, [{"date": "2025-03-01", "pnl": 100}, {"date": "2025-11-20", "pnl": -40}])
    freeze(page, today)
    page.reload()
    page.wait_for_selector("#student-dashboard .sd-grid")

    found = page.locator("#sd-declaration").count()
    assert bool(found) is visible, f"{why}: ожидали visible={visible}"


def test_reminder_stays_silent_without_trades_from_last_year(pw_page, site_url):
    """Декларировать нечего — напоминать не о чем."""
    page = pw_page
    page.goto(f"{site_url}/extras/dashboard/")
    seed(page, [{"date": "2026-01-05", "pnl": 50}])
    freeze(page, "2026-02-01T10:00:00Z")
    page.reload()
    page.wait_for_selector("#student-dashboard .sd-grid")

    assert page.locator("#sd-declaration").count() == 0


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_reminder_is_translated_and_names_the_year(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}extras/dashboard/")
    seed(page, [{"date": "2025-05-05", "pnl": 10}, {"date": "2025-06-06", "pnl": 20}])
    freeze(page, "2026-02-10T10:00:00Z")
    page.reload()
    page.wait_for_selector("#sd-declaration")

    text = page.text_content("#sd-declaration")
    assert "undefined" not in text, f"[{prefix}] {text[:80]!r}"
    assert "2025" in text and "2026" in text, f"[{prefix}] нет годов: {text[:120]!r}"
    assert "2" in text, f"[{prefix}] нет числа сделок"
    assert page.locator("#sd-declaration a").count() == 1


@pytest.mark.parametrize(
    ("today", "rows", "expected"),
    [
        ("2026-01-15", [{"date": "2025-01-01"}], True),
        ("2026-03-31", [{"date": "2025-01-01"}], True),
        ("2026-04-01", [{"date": "2025-01-01"}], False),
        ("2026-12-31", [{"date": "2025-01-01"}], False),
        ("2026-02-01", [], False),
        ("2026-02-01", [{"date": "2026-01-05"}], False),
        ("2026-02-01", [{"date": None}], False),
    ],
)
def test_decision_logic_directly(pw_page, site_url, today, rows, expected):
    """Сама логика — без отрисовки, чтобы граница по месяцам была явной."""
    page = pw_page
    page.goto(f"{site_url}/extras/dashboard/")
    page.wait_for_function("() => typeof window.__fxDeclarationDue === 'function'")

    got = page.evaluate("a => window.__fxDeclarationDue(a[0], a[1])", [today, rows])

    assert got["due"] is expected, f"{today} с {rows}: получили {got}"
