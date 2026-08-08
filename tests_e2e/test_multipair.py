"""Перенос настройки между парами — в настоящем браузере.

Как и на странице про переобучение, порядок здесь принципиален: сначала
читатель отвечает сам, и только потом видит таблицу. Если таблица показана
сразу, вопрос превращается в риторический и урок пропадает.

Числа не зашиты в тест: он читает тот же набор, что и страница, и сверяет с
`forex_toolkit.multipair`. Пересчитают набор — тест продолжит проверять то же
самое утверждение, а не устаревшие цифры.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forex_toolkit.multipair import summarize

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "_mkdocs" / "data" / "multipair.json"

LOCALES = ["", "en/", "uz/"]


def _document() -> dict:
    return json.loads(DATASET.read_text(encoding="utf-8"))


def _open(page, site_url, prefix):
    page.goto(f"{site_url}/{prefix}tools/multipair/")
    page.wait_for_selector(".mp-guesses, .calc-error", timeout=30_000)


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_widget_gets_its_data(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    assert page.locator(".calc-error").count() == 0, (
        f"[{prefix or 'ru'}] данные не загрузились: {page.text_content('.calc-error')}"
    )
    pairs = summarize(_document()).pairs
    # Вариантов ответа на один больше, чем пар: ноль тоже допустимый ответ.
    assert page.locator(".mp-guess").count() == pairs + 1


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_the_table_is_hidden_until_you_answer(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    assert page.locator(".mp-table").count() == 0, (
        f"[{prefix or 'ru'}] таблица показана до ответа — вопрос обесценен"
    )
    assert page.text_content("#mp-verdict").strip() == ""


def test_answering_reveals_every_pair(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")
    summary = summarize(_document())

    page.locator(".mp-guess").first.click()
    page.wait_for_selector(".mp-table")

    assert page.locator(".mp-table tbody tr").count() == summary.pairs
    assert page.locator(".mp-home").count() == 1, "опорная пара не выделена"
    assert page.locator(".mp-lesson").count() == 1
    verdict = page.text_content("#mp-verdict")
    assert str(summary.profitable) in verdict


def test_browser_summary_matches_python(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    document = _document()
    got = page.evaluate("d => window.__fxMultiPair(d)", document)
    expected = summarize(document)

    assert expected is not None
    assert got["pairs"] == expected.pairs
    assert got["profitable"] == expected.profitable
    assert got["own_params_differ"] == expected.own_params_differ
    assert got["best"]["pair"] == expected.best.pair
    assert got["worst"]["pair"] == expected.worst.pair
    assert round(got["median_r"], 3) == round(expected.median_r, 3)
    assert round(got["spread"], 3) == round(expected.spread, 3)


def test_the_home_pair_is_named_honestly(pw_page, site_url):
    """Опорная пара обязана быть подписана: без этого таблица выглядит как
    честное сравнение восьми равных пар, а она таковой не является."""
    page = pw_page
    _open(page, site_url, "")
    summary = summarize(_document())

    page.locator(".mp-guess").first.click()
    page.wait_for_selector(".mp-table")

    home_row = page.locator(".mp-home")
    assert summary.home_pair in home_row.text_content()
    assert home_row.locator("small").count() == 1, "нет подписи «опорная»"


def test_you_can_answer_again(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    page.locator(".mp-guess").first.click()
    page.wait_for_selector("#mp-again")
    page.click("#mp-again")
    page.wait_for_selector(".mp-guesses")
    assert page.locator(".mp-table").count() == 0
