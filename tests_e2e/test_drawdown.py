"""Калькулятор восстановления после просадки — в настоящем браузере.

Проверяем поведение и математику, а не вёрстку:

* страница открывается и виджет считает сразу (дефолт 20% → +25.0%);
* ввод 50 → требуемая прибыль +100.0%;
* ввод 10 → ≈ +11.1%;
* при просадке ≥ 30% показывается анти-отыгрышное предупреждение;
* страница работает на всех трёх локалях.
"""

from __future__ import annotations

import re


def _result(page) -> str:
    page.wait_for_function(
        "() => document.getElementById('dd-result').textContent.trim() !== ''"
    )
    return page.text_content("#dd-result")


def _enter(page, value: str) -> str:
    page.fill("#dd-input", value)
    page.click("#dd-calc-btn")
    return _result(page)


def _gain_of(text: str) -> float:
    """Вытащить из результата требуемую прибыль: '+100.0%' / '+11.1%'."""
    match = re.search(r"\+(\d+(?:[.,]\d+)?)%", text)
    assert match, f"в результате нет требуемой прибыли: {text!r}"
    return float(match.group(1).replace(",", "."))


def test_default_input_renders_result(site_url, pw_page):
    page = pw_page
    page.goto(f"{site_url}/tools/drawdown-recovery/")
    # Дефолт 20% → 20/(100-20)*100 = 25%.
    assert _gain_of(_result(page)) == 25.0


def test_half_drawdown_needs_double_gain(site_url, pw_page):
    page = pw_page
    page.goto(f"{site_url}/tools/drawdown-recovery/")
    assert _gain_of(_enter(page, "50")) == 100.0


def test_ten_percent_drawdown_needs_eleven(site_url, pw_page):
    page = pw_page
    page.goto(f"{site_url}/tools/drawdown-recovery/")
    assert _gain_of(_enter(page, "10")) == 11.1


def test_deep_drawdown_shows_anti_revenge_warning(site_url, pw_page):
    page = pw_page
    page.goto(f"{site_url}/tools/drawdown-recovery/")
    text = _enter(page, "40")
    assert "calc-error" in page.inner_html("#dd-result"), (
        "при просадке ≥ 30% нет красного статуса"
    )
    assert "⚠️" in text, "при просадке ≥ 30% нет предупреждения об анти-отыгрыше"

    text = _enter(page, "10")
    assert "⚠️" not in text, "предупреждение не должно показываться на мелкой просадке"


def test_page_renders_in_english_and_uzbek(site_url, pw_page):
    page = pw_page

    page.goto(f"{site_url}/en/tools/drawdown-recovery/")
    assert _gain_of(_enter(page, "50")) == 100.0
    assert "Gain needed" in _result(page)

    page.goto(f"{site_url}/uz/tools/drawdown-recovery/")
    assert _gain_of(_enter(page, "50")) == 100.0
    assert "kerak foyda" in _result(page)
