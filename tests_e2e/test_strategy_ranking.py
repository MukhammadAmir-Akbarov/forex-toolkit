"""Устойчивость рейтинга стратегий — в настоящем браузере.

Третья страница подряд с одним и тем же устройством: сначала читатель выбирает,
потом видит вторую половину истории. Значит и проверять надо то же самое —
что будущее не протекает в разметку до выбора.

Числа в тест не зашиты: он читает тот же набор, что и страница.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forex_toolkit.strategy_ranking import summarize

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "_mkdocs" / "data" / "strategies.json"

LOCALES = ["", "en/", "uz/"]


def _document() -> dict:
    return json.loads(DATASET.read_text(encoding="utf-8"))


def _open(page, site_url, prefix):
    page.goto(f"{site_url}/{prefix}tools/strategy-ranking/")
    page.wait_for_selector(".sr-table, .calc-error", timeout=30_000)


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_widget_gets_its_data(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    assert page.locator(".calc-error").count() == 0, (
        f"[{prefix or 'ru'}] данные не загрузились: {page.text_content('.calc-error')}"
    )
    expected = summarize(_document())
    assert page.locator(".sr-table tbody tr").count() == expected.considered


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_the_future_is_hidden_until_you_pick(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    expected = summarize(_document())
    assert page.locator(".sr-pick").count() == expected.considered, (
        f"[{prefix or 'ru'}] в последней колонке должна быть кнопка выбора"
    )
    assert page.locator(".sr-good, .sr-bad").count() == 0, (
        f"[{prefix or 'ru'}] будущее покрашено до выбора"
    )
    assert page.text_content("#sr-verdict").strip() == ""


def test_picking_reveals_places_and_the_caveat(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")
    expected = summarize(_document())

    page.locator(".sr-pick").first.click()
    page.wait_for_selector("#sr-verdict p")

    assert page.locator(".sr-pick").count() == 0
    assert page.locator(".sr-good, .sr-bad").count() == expected.considered
    assert page.locator(".sr-lesson").count() == 1
    # Оговорка про размер выборки обязана быть на экране: без неё страница
    # утверждала бы, что порядок всегда переворачивается.
    assert page.locator(".sr-caution").count() == 1, "нет оговорки о выборке"

    verdict = page.text_content("#sr-verdict")
    assert expected.best_future.name in verdict
    assert str(expected.best_past_rank_future) in verdict


def test_browser_summary_matches_python(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    document = _document()
    got = page.evaluate("d => window.__fxStrategyRanking(d, 20)", document)
    expected = summarize(document, min_trades=20)

    assert expected is not None
    assert got["considered"] == expected.considered
    assert got["kept_place"] == expected.kept_place
    assert got["best_past"]["name"] == expected.best_past.name
    assert got["best_future"]["name"] == expected.best_future.name
    assert round(got["rank_correlation"], 6) == round(expected.rank_correlation, 6)
    assert got["order_held"] == expected.order_held


def test_page_text_agrees_with_the_dataset(pw_page, site_url):
    """Таблица в тексте написана руками — она не должна разъехаться с данными."""
    page = pw_page
    _open(page, site_url, "")

    text = page.text_content(".md-content").replace("−", "-").replace("–", "-")
    expected = summarize(_document())
    assert expected.best_future.name in text
    assert expected.best_past.name in text
    assert f"{expected.best_past.past_r:+.1f}R" in text


def test_you_can_pick_again(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    page.locator(".sr-pick").first.click()
    page.wait_for_selector("#sr-again")
    page.click("#sr-again")
    page.wait_for_selector(".sr-pick")
    assert page.locator(".sr-good, .sr-bad").count() == 0
