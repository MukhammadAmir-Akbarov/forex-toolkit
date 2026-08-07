"""e2e: JS-математика виджетов-калькуляторов == каноничный Python из tools/.

Защищает от тихого расхождения: 7+ виджетов считают реальные деньги, а Python
покрыт тестами, JS — нет. Проверяем дефолтную (RU) локаль; JS-логика во всех
трёх локалях идентична (см. IMPROVEMENTS.md I2). Реализует I3.
"""

from __future__ import annotations

import re

import pytest

from compound_calculator import project_growth
from margin_calculator import margin_required
from position_calculator import calculate_position

# Канон стоимости пипса берём прямо из пакета (а не из tools/) — это эталон,
# который CLAUDE.md называет единственным источником финансовой математики.
from forex_toolkit.fx_math import pip_value_in_quote

# RU-локаль форматирует деньги как "$2 032,79" (nbsp-разряды, запятая-десятичная).
NBSP = " "


def money(text: str) -> float:
    """Распарсить '$2 032,79' (ru-RU) → 2032.79."""
    t = text.replace("$", "").replace(NBSP, "").replace(" ", "").replace(",", ".")
    return float(t)


def money_any(text: str) -> float:
    """Распарсить денежную строку в любой локали (ru-RU/en-US/uz-UZ).

    Последний разделитель ('.' или ',') считаем десятичным, остальные —
    разрядными. Покрывает '$1,234.56' (en), '$1 234,56' (ru/uz), '$36.00'.
    """
    t = text.replace("$", "").replace(NBSP, "").replace(" ", "")
    t = t.replace(" ", "").strip()
    dec = max(t.rfind(","), t.rfind("."))
    if dec == -1:
        return float(t)
    intpart = re.sub(r"[.,]", "", t[:dec])
    return float(intpart + "." + t[dec + 1 :])


def _fill(page, selector: str, value: str) -> None:
    page.fill(selector, str(value))


def _read(page, selector: str) -> str:
    page.wait_for_function(
        "sel => { const e = document.querySelector(sel);"
        " return e && e.textContent && e.textContent.trim() !== '—'; }",
        arg=selector,
    )
    return page.text_content(selector).strip()


# ───────────────────────── Margin ─────────────────────────

MARGIN_CASES = [
    # (deposit, lots, price, leverage, lot_type, contract_size)
    (1000, 0.01, 1.0800, 30, "standard", 100_000),
    (1000, 0.5, 1.0800, 30, "standard", 100_000),
    (500, 0.1, 1.2500, 100, "standard", 100_000),
    (1000, 1.0, 1.0800, 50, "mini", 10_000),
    (2000, 2.0, 0.9000, 200, "micro", 1_000),
]


def test_margin_calculator(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/margin-calculator/")
    for deposit, lots, price, lev, lot_type, contract in MARGIN_CASES:
        _fill(page, "#mc-deposit", deposit)
        _fill(page, "#mc-lots", lots)
        _fill(page, "#mc-price", price)
        page.select_option("#mc-leverage", str(lev))
        page.select_option("#mc-type", lot_type)
        page.click("#mc-calc-btn")

        expected = margin_required(lots, price, lev, contract)
        got = money(_read(page, "#mc-out-margin"))
        assert abs(got - expected) < 0.01, (
            f"margin {lots=} {price=} {lev=} {lot_type=}: JS={got} Python={expected}"
        )


# ──────────────────────── Compound ────────────────────────

COMPOUND_CASES = [
    # (initial, monthly_roi_pct, months, monthly_deposit)
    (1000, 3, 24, 0),
    (500, 2, 12, 0),
    (1000, 1, 60, 50),
    (2000, 5, 36, 0),
]


def test_compound_calculator(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/compound-calculator/")
    for initial, roi, months, dep in COMPOUND_CASES:
        _fill(page, "#cc-initial", initial)
        _fill(page, "#cc-roi", roi)
        _fill(page, "#cc-months", months)
        _fill(page, "#cc-deposit", dep)
        page.click("#cc-calc-btn")

        expected = project_growth(initial, roi, months, dep)[-1]
        got = money(_read(page, "#cc-out-final"))
        assert abs(got - expected) < 0.01, (
            f"compound {initial=} {roi=} {months=} {dep=}: JS={got} Python={expected}"
        )


# ───────────────── Cross-locale (общий JS виджетов, I2) ─────────────────
# Виджеты переведены на общий JS из _mkdocs/javascripts/widgets/*.js, где локаль
# берётся из <html lang>. Проверяем, что вынесенный скрипт активируется на EN/UZ
# страницах (другой путь, другой lang) и считает ту же математику, что Python.


# ──────────────────────── Position ────────────────────────

POSITION_CASES = [
    # (balance, risk%, stop_pips, pair) — EURUSD: статичный pip $10, live не влияет
    (1000, 1, 20, "EURUSD"),
    (500, 2, 50, "EURUSD"),
    (2000, 0.5, 30, "EURUSD"),
    (1000, 3, 15, "EURUSD"),
]


def test_position_calculator(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/position-calculator/")
    # Выключаем live-курс — детерминизм без сети (EURUSD статичен в любом случае).
    if page.is_checked("#pc-live"):
        page.uncheck("#pc-live")
    for balance, risk, stop, pair in POSITION_CASES:
        _fill(page, "#pc-balance", balance)
        _fill(page, "#pc-risk", risk)
        _fill(page, "#pc-stop", stop)
        page.select_option("#pc-pair", pair)
        page.click("#pc-calc-btn")

        expected = calculate_position(balance, risk, stop, pair).lots_rounded
        got = float(_read(page, "#pc-out-lots-rounded"))
        assert abs(got - expected) < 1e-9, (
            f"position {balance=} {risk=} {stop=} {pair=}: JS={got} Python={expected}"
        )

        # I21: риск в сумах = actualRisk (lots·stop·pipvalue) × курс 12600 (дефолт).
        # Все POSITION_CASES — USD-quote (EURUSD), поэтому pipvalue = 10.
        uzs_num = int(re.sub(r"\D", "", _read(page, "#pc-out-uzs")))
        assert uzs_num == round(got * stop * 10 * 12600), (
            f"UZS {balance=} {stop=}: got={uzs_num}"
        )


# ──────────────────────── Pip value ────────────────────────
# Эталон — forex_toolkit.fx_math.pip_value_in_quote. Для пар с котировкой USD
# (EUR/USD, GBP/USD, …) стоимость пипса в USD равна значению в котируемой валюте,
# поэтому конвертация по live-курсу не нужна и тест не ходит в сеть. JPY/кросс-
# пары требуют курс — их сюда не берём (их покрывает математика fx_math отдельно).

PIP_CASES = [
    # (lots, pair) — только USD-quote, где pipValueUSD == pip_value_in_quote
    (1.0, "EURUSD"),
    (0.1, "EURUSD"),
    (0.5, "GBPUSD"),
    (2.0, "AUDUSD"),
    (0.25, "NZDUSD"),
]


def test_pip_calculator(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/pip-calculator/")
    # Выключаем live-курс — детерминизм без сети (USD-quote пары статичны и так).
    if page.is_checked("#pp-live"):
        page.uncheck("#pp-live")
    for lots, pair in PIP_CASES:
        page.select_option("#pp-pair", pair)
        _fill(page, "#pp-lots", lots)
        page.click("#pp-calc-btn")

        expected = pip_value_in_quote(lots, pair)
        got = money(_read(page, "#pp-out-pip"))
        assert abs(got - expected) < 1e-4, (
            f"pip {lots=} {pair=}: JS={got} fx_math={expected}"
        )

        uzs = int(re.sub(r"\D", "", _read(page, "#pp-out-uzs")))
        uzs_10 = int(re.sub(r"\D", "", _read(page, "#pp-out-uzs-10")))
        assert uzs == round(expected * 12_600)
        assert uzs_10 == round(expected * 10 * 12_600)

    _fill(page, "#pp-lots", 0.1)
    page.select_option("#pp-pair", "EURUSD")
    _fill(page, "#pp-uzs", 13_000)
    page.click("#pp-calc-btn")
    assert int(re.sub(r"\D", "", _read(page, "#pp-out-uzs"))) == 13_000

    _fill(page, "#pp-uzs", 0)
    page.click("#pp-calc-btn")
    assert not page.locator("#pp-out-uzs-row").is_visible()
    assert not page.locator("#pp-out-uzs-10-row").is_visible()


@pytest.mark.parametrize("prefix", ["en/", "uz/"])
def test_pip_calculator_uzs_locales(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}tools/pip-calculator/")
    if page.is_checked("#pp-live"):
        page.uncheck("#pp-live")
    page.select_option("#pp-pair", "EURUSD")
    _fill(page, "#pp-lots", 0.1)
    _fill(page, "#pp-uzs", 12_600)
    page.click("#pp-calc-btn")

    assert money_any(_read(page, "#pp-out-pip")) == pytest.approx(1.0)
    assert int(re.sub(r"\D", "", _read(page, "#pp-out-uzs"))) == 12_600
    assert "so'm" in _read(page, "#pp-out-uzs")


@pytest.mark.parametrize("prefix", ["en", "uz"])
def test_margin_calculator_locales(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}/tools/margin-calculator/")
    deposit, lots, price, lev = 1000, 0.1, 1.0800, 30
    lot_type, contract = "standard", 100_000
    _fill(page, "#mc-deposit", deposit)
    _fill(page, "#mc-lots", lots)
    _fill(page, "#mc-price", price)
    page.select_option("#mc-leverage", str(lev))
    page.select_option("#mc-type", lot_type)
    page.click("#mc-calc-btn")

    expected = margin_required(lots, price, lev, contract)
    got = money_any(_read(page, "#mc-out-margin"))
    assert abs(got - expected) < 0.01, f"[{prefix}] margin: JS={got} Python={expected}"


# ──────────────────────── Tax (НДФЛ 12%) ────────────────────────
# Каноничная формула — uz/tax-calculator.py:calculate_tax (имя файла с дефисом,
# не импортируется через conftest), поэтому ожидание считаем инлайн:
#   net = profit - loss;  tax = max(0, net) * 0.12.

TAX_CASES = [
    # (profit, loss, expected_tax)
    (5000, 1000, 480.0),
    (3000, 3000, 0.0),
    (10000, 2500, 900.0),
    (1000, 5000, 0.0),
]


def test_tax_calculator(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/uz/tax-calculator/")
    for profit, loss, expected in TAX_CASES:
        _fill(page, "#tax-profit", profit)
        _fill(page, "#tax-loss", loss)
        page.click("#tax-calc-btn")
        # tax==0 → headline показывает "$0.00", _read это примет.
        got = money(_read(page, "#tax-out-tax"))
        assert abs(got - expected) < 0.01, (
            f"tax {profit=} {loss=}: JS={got} expected={expected}"
        )


# ──────────────────────── Win Rate × R:R ────────────────────────
# Чистая математика (без Python-инструмента): минимальный RR безубытка = (1-wr)/wr.
# Проверяем, что значение появляется в таблице результата на всех локалях.


# ──────────────────── Cost of trading (I17) ────────────────────
# Самодостаточный виджет (Python-канона нет). Ожидание считаем инлайн:
#   pipValue = PIP_VALUE_PER_LOT[pair] * lots
#   total    = spread*pipValue + commission*lots*2 + (-swap)*lots*nights.

PIP_VALUE_PER_LOT = {"EURUSD": 10.0, "USDJPY": 6.7}

COST_CASES = [
    # (lots, spread, commission, nights, swap, pair) — nights=0 → своп не влияет
    (0.10, 1.0, 0.0, 0, -2, "EURUSD"),
    (0.50, 1.2, 3.5, 0, -2, "EURUSD"),
    (0.10, 2.0, 0.0, 0, 0, "USDJPY"),
    (0.20, 1.0, 3.5, 1, -3, "EURUSD"),
]


def test_cost_calculator(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/cost-calculator/")
    for lots, spread, commission, nights, swap, pair in COST_CASES:
        _fill(page, "#co-lots", lots)
        _fill(page, "#co-spread", spread)
        _fill(page, "#co-commission", commission)
        _fill(page, "#co-nights", nights)
        _fill(page, "#co-swap", swap)
        page.select_option("#co-pair", pair)
        page.click("#co-calc-btn")

        pip_value = PIP_VALUE_PER_LOT[pair] * lots
        expected = spread * pip_value + commission * lots * 2 + (-swap) * lots * nights
        got = money(_read(page, "#co-out-total"))
        assert abs(got - expected) < 0.01, (
            f"cost {lots=} {spread=} {commission=} {nights=} {swap=} {pair=}: "
            f"JS={got} expected={expected}"
        )


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_winrate_calculator(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}tools/winrate-rr-calculator/")
    page.fill("#wr-input", "40")
    page.fill("#rr-input", "2")
    page.fill("#trades-input", "100")
    page.fill("#risk-input", "1")
    page.click("#wr-calc-btn")
    # requiredRR = (1-0.4)/0.4 = 1.50 — должно появиться в таблице.
    page.wait_for_function(
        "() => document.getElementById('wr-result').textContent.includes('1.50')"
    )
    text = page.text_content("#wr-result")
    assert "1.50" in text
    # Сверяем саму математику EV и нетто, а не только requiredRR:
    #   EV  = (wr*rr - (1-wr))*risk = (0.4*2 - 0.6)*1 = +0.200 за сделку;
    #   net = wins*rr*risk - losses*risk = 40*2 - 60 = +20.00% депозита.
    assert "+0.200" in text, f"EV не совпал: {text!r}"
    assert "+20.00" in text, f"нетто-результат не совпал: {text!r}"


# ──────────────────── Итоговый экзамен + сертификат (I10) ────────────────────
# Проходим экзамен на 100% (кликаем правильный вариант по индексу answer из JSON),
# проверяем: проходной балл сработал, сертификат отрисован, прогресс записан.


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_exam_certificate(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}tools/exam/")
    bank = page.evaluate(
        "() => JSON.parse(document.getElementById('exam-questions').textContent)"
    )
    assert len(bank) == 30, f"[{prefix}] банк вопросов не 30"
    draw = 20  # столько виджет достаёт из банка за попытку
    # Порядок вопросов и вариантов случаен, поэтому идём по тому, что реально
    # показано на экране, а не по индексам банка.
    correct_for = {q["q"]: q["options"][q["answer"]] for q in bank}

    page.fill("#exam-name", "Test User")
    page.wait_for_selector("#exam-start-btn", state="visible")
    # Material/reading.js обновляют геометрию длинной страницы во время
    # автопрокрутки, из-за чего координатный click может попасть в следующий h2.
    # DOM-click вызывает тот же штатный обработчик без зависимости от viewport.
    page.locator("#exam-start-btn").evaluate("button => button.click()")

    seen = []
    for n in range(draw):
        page.wait_for_function(
            "() => document.getElementById('exam-question').textContent.trim()"
            " && document.querySelectorAll('#exam-options .exam-option').length > 0"
        )
        shown = page.text_content("#exam-question").strip()
        assert shown in correct_for, f"[{prefix}] вопрос вне банка: {shown!r}"
        seen.append(shown)
        clicked = page.evaluate(
            "c => { const b = [...document.querySelectorAll("
            "'#exam-options .exam-option')].find(x => x.textContent.trim() === c);"
            " if (!b) return false; b.click();"
            " document.getElementById('exam-next').click(); return true; }",
            correct_for[shown],
        )
        assert clicked, f"[{prefix}] не нашёл вариант: {correct_for[shown]!r}"

    assert len(set(seen)) == draw, f"[{prefix}] вопрос повторился внутри попытки"

    # Результат: 100% → проходной балл, сертификат виден, прогресс записан.
    page.wait_for_selector("#exam-cert-wrap", state="visible")
    passed = page.evaluate("() => localStorage.getItem('forex_exam_passed')")
    best = page.evaluate("() => localStorage.getItem('forex_exam_best')")
    assert passed == "1", f"[{prefix}] экзамен не отметился пройденным"
    assert best == "100", f"[{prefix}] best={best}, ожидали 100"
    # canvas сертификата непустой (есть data-URL).
    durl = page.evaluate(
        "() => document.getElementById('exam-cert').toDataURL('image/png').length"
    )
    assert durl > 1000, "сертификат не отрисован"
