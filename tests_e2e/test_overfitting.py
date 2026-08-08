"""Демонстрация переобучения в настоящем браузере.

Упражнение держится на одном условии: до выбора читатель НЕ должен видеть
вторую половину истории. Если будущее протекает в разметку, страница
превращается в обычную таблицу и урок пропадает — поэтому это первое, что
здесь проверяется, и проверяется по DOM, а не по картинке.

Второе — путь к данным. У русской страницы он `../../data/`, у en и uz
`../../../data/`, потому что они на уровень глубже. Ошибка в нём выглядит не
падением, а вежливым «не удалось загрузить».
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forex_toolkit.overfitting import summarize

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "_mkdocs" / "data" / "overfitting.json"

LOCALES = ["", "en/", "uz/"]


def _rows() -> list[dict]:
    return json.loads(DATASET.read_text(encoding="utf-8"))["rows"]


def _open(page, site_url, prefix):
    page.goto(f"{site_url}/{prefix}tools/overfitting/")
    page.wait_for_selector(".of-table, .calc-error", timeout=30_000)


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_widget_gets_its_data(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    assert page.locator(".calc-error").count() == 0, (
        f"[{prefix or 'ru'}] данные не загрузились: {page.text_content('.calc-error')}"
    )
    assert page.locator(".of-table tbody tr").count() == 54


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_the_future_is_hidden_until_you_choose(pw_page, site_url, prefix):
    """Ради этого всё и сделано: сначала выбор вслепую, потом расплата."""
    page = pw_page
    _open(page, site_url, prefix)

    # Проверяем структурой, а не поиском чисел по тексту. Первая версия этого
    # теста искала любое значение будущего в разметке и падала на «-7.7R»:
    # у одной комбинации это результат на прошлом, у другой — на будущем.
    # Совпадение чисел неизбежно, и такой тест кричал бы «утечка» без утечки.
    rows = page.locator(".of-table tbody tr")
    assert rows.count() == 54
    assert page.locator(".of-table tbody tr td:last-child .of-pick").count() == 54, (
        f"[{prefix or 'ru'}] в последней колонке должна быть кнопка выбора"
    )
    # Классы исхода появляются только после раскрытия.
    assert page.locator(".of-good, .of-bad").count() == 0, (
        f"[{prefix or 'ru'}] будущее покрашено до выбора"
    )
    assert page.text_content("#of-verdict").strip() == "", "разбор показан заранее"
    # И сам набор не должен лежать в разметке — иначе его прочитают глазами.
    assert "out_total_r" not in page.inner_html("#overfitting")


def test_choosing_reveals_the_future_and_the_verdict(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    page.locator(".of-pick").first.click()
    page.wait_for_selector("#of-verdict h4")

    verdict = page.text_content("#of-verdict")
    assert "R" in verdict, verdict
    assert page.locator(".of-lesson").count() == 1, "нет вывода урока"
    assert page.locator(".of-pick").count() == 0, "кнопки выбора остались"
    assert page.locator(".of-table .of-bad, .of-table .of-good").count() == 54


def test_browser_summary_matches_python(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    rows = _rows()
    got = page.evaluate("r => window.__fxOverfitSummary(r, 20)", rows)
    expected = summarize(rows, min_trades=20)

    assert expected is not None
    assert got["considered"] == expected.considered
    assert got["rank_out"] == expected.rank_out
    assert round(got["correlation"], 6) == round(expected.correlation, 6)
    assert round(got["median_out"], 3) == round(expected.median_out, 3)
    assert got["best_in"]["params"] == expected.best_in.params


def test_page_numbers_agree_with_the_dataset(pw_page, site_url):
    """Текст страницы утверждает конкретные числа — они не должны разъехаться.

    Таблица в тексте написана руками. Если набор пересчитают, а текст забудут,
    сайт будет утверждать одно, а виджет показывать другое.
    """
    page = pw_page
    _open(page, site_url, "")

    text = page.text_content(".md-content")
    expected = summarize(_rows())
    assert f"{expected.best_in.in_total_r:+.1f}R".replace("+", "+") in text.replace(
        "−", "-"
    ).replace("–", "-"), "в тексте нет результата лучшей комбинации на прошлом"
    assert str(expected.rank_out) in text, "в тексте нет места на будущем"
    assert str(expected.considered) in text, "в тексте нет числа комбинаций"


def test_you_can_pick_again(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    page.locator(".of-pick").first.click()
    page.wait_for_selector("#of-again")
    page.click("#of-again")
    page.wait_for_selector(".of-pick")
    assert page.locator(".of-pick").count() == 54
