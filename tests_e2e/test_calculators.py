"""e2e: JS-математика виджетов-калькуляторов == каноничный Python из tools/.

Защищает от тихого расхождения: 7+ виджетов считают реальные деньги, а Python
покрыт тестами, JS — нет. Проверяем дефолтную (RU) локаль; JS-логика во всех
трёх локалях идентична (см. IMPROVEMENTS.md I2). Реализует I3.
"""

from __future__ import annotations

from compound_calculator import project_growth
from margin_calculator import margin_required

# RU-локаль форматирует деньги как "$2 032,79" (nbsp-разряды, запятая-десятичная).
NBSP = " "


def money(text: str) -> float:
    """Распарсить '$2 032,79' (ru-RU) → 2032.79."""
    t = text.replace("$", "").replace(NBSP, "").replace(" ", "").replace(",", ".")
    return float(t)


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
