"""Прямые тесты финансового ядра пакета.

До сих пор `fx_math` проверялся только через обёртки в `tools/`
(`pip_calculator`, `position_calculator`, `multi_position_sizer`). Для
пользователя пакета — а пакет и есть публикуемый артефакт — это значит, что
опубликованный API не проверен напрямую ни разу.

Второе назначение файла: он единственный, по которому гоняется мутационное
тестирование (`mutmut`, см. [tool.mutmut] в pyproject.toml). Мутанты
запускают только эти тесты и `test_risk_budget.py`, поэтому здесь нужны
именно граничные случаи: подмена знака, `<` на `<=`, ноль и отрицательные.
"""

from __future__ import annotations

import math

import pytest

from forex_toolkit.fx_math import (
    LIVE_SENSITIVE_PAIRS,
    MIN_LOT,
    PIP_VALUE_USD_PER_LOT,
    STANDARD_LOT_UNITS,
    calc_lots,
    normalize_pair,
    pip_size,
    pip_value_in_account_currency,
    pip_value_in_quote,
)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("eur/usd", "EURUSD"),
        ("EUR-USD", "EURUSD"),
        ("eurusd", "EURUSD"),
        ("EURUSD", "EURUSD"),
        ("usd/jpy", "USDJPY"),
    ],
)
def test_normalize_pair(raw: str, expected: str) -> None:
    assert normalize_pair(raw) == expected


@pytest.mark.parametrize(
    "pair,expected",
    [
        ("EURUSD", 0.0001),
        ("GBPUSD", 0.0001),
        ("USDJPY", 0.01),
        ("EURJPY", 0.01),
        ("GBPJPY", 0.01),
        ("usd/jpy", 0.01),
    ],
)
def test_pip_size_knows_the_yen(pair: str, expected: float) -> None:
    """Стократная ошибка: у иены пункт 0.01, у остальных 0.0001.

    Именно на этом однажды «не сработала» стратегия на иеновых парах —
    фильтр считался в стократно завышенных единицах (см. SESSION-2026-08).
    """
    assert pip_size(pair) == expected


def test_pip_size_is_a_hundred_times_bigger_for_yen() -> None:
    assert pip_size("USDJPY") == pytest.approx(pip_size("EURUSD") * 100)


@pytest.mark.parametrize(
    "lots,pair,expected",
    [
        (1.0, "EURUSD", 10.0),
        (0.1, "EURUSD", 1.0),
        (0.01, "EURUSD", 0.1),
        (1.0, "USDJPY", 1000.0),  # в иенах, не в долларах
        (0.5, "GBPUSD", 5.0),
    ],
)
def test_pip_value_in_quote(lots: float, pair: str, expected: float) -> None:
    assert pip_value_in_quote(lots, pair) == pytest.approx(expected)


def test_pip_value_scales_with_lot_size() -> None:
    """Удвоил лот — удвоилась цена пункта. Без этого лот не значит ничего."""
    assert pip_value_in_quote(2.0, "EURUSD") == pytest.approx(
        2 * pip_value_in_quote(1.0, "EURUSD")
    )


def test_standard_lot_is_a_hundred_thousand_units() -> None:
    assert STANDARD_LOT_UNITS == 100_000
    assert pip_value_in_quote(1.0, "EURUSD") == STANDARD_LOT_UNITS * pip_size("EURUSD")


def test_account_in_quote_currency_needs_no_conversion() -> None:
    """Счёт в USD, торгуем EURUSD: цена пункта уже в долларах."""
    assert pip_value_in_account_currency(1.0, "EURUSD", "USD", 1.08) == pytest.approx(
        10.0
    )


def test_account_in_base_currency_is_divided_by_price() -> None:
    """Счёт в EUR, торгуем EURUSD: 10 USD за пункт делим на курс.

    Умножение вместо деления даёт 10.8 вместо 9.26 — ошибка в 17%, которую
    глазами в отчёте не видно.
    """
    value = pip_value_in_account_currency(1.0, "EURUSD", "EUR", 1.08)
    assert value == pytest.approx(10.0 / 1.08)
    assert value < 10.0


def test_yen_account_conversion_uses_yen_pip() -> None:
    """USDJPY со счётом в USD: 1000 иен за пункт делим на курс."""
    value = pip_value_in_account_currency(1.0, "USDJPY", "USD", 150.0)
    assert value == pytest.approx(1000.0 / 150.0)


def test_cross_conversion_refuses_to_guess() -> None:
    """Не хватает курса — ошибка, а не правдоподобное число."""
    with pytest.raises(ValueError, match="Кросс-конвертация"):
        pip_value_in_account_currency(1.0, "EURUSD", "UZS", 1.08)


def test_pair_case_and_separators_do_not_change_the_answer() -> None:
    assert pip_value_in_account_currency(1.0, "eur/usd", "usd", 1.08) == pytest.approx(
        pip_value_in_account_currency(1.0, "EURUSD", "USD", 1.08)
    )


@pytest.mark.parametrize(
    "risk,stop,pip_value,expected",
    [
        (10.0, 25.0, 10.0, 0.04),
        (5.0, 25.0, 10.0, 0.02),
        (100.0, 50.0, 10.0, 0.2),
        (10.0, 30.0, 10.0, 0.03),
    ],
)
def test_calc_lots(risk: float, stop: float, pip_value: float, expected: float) -> None:
    assert calc_lots(risk, stop, pip_value) == pytest.approx(expected)


def test_calc_lots_rounds_down_so_real_risk_never_exceeds_plan() -> None:
    """Округление вверх увеличило бы риск сверх запланированного.

    7 / (25 * 10) = 0.028 лота. Вверх — 0.03, то есть риск 7.5 вместо 7.
    """
    lots = calc_lots(7.0, 25.0, 10.0)
    assert lots == pytest.approx(0.02)
    assert lots * 25.0 * 10.0 <= 7.0


def test_calc_lots_keeps_the_broker_step() -> None:
    """Результат всегда кратен 0.01 — иначе брокер откажет в ордере."""
    for risk in (3.0, 7.0, 11.0, 13.5, 99.9):
        lots = calc_lots(risk, 23.0, 9.3)
        assert math.isclose(round(lots / MIN_LOT), lots / MIN_LOT, abs_tol=1e-9)


@pytest.mark.parametrize("stop", [0.0, -1.0, -25.0])
def test_calc_lots_rejects_non_positive_stop(stop: float) -> None:
    """Стоп ноль — не «бесконечный лот», а отказ считать."""
    assert calc_lots(100.0, stop, 10.0) == 0.0


@pytest.mark.parametrize("pip_value", [0.0, -10.0])
def test_calc_lots_rejects_non_positive_pip_value(pip_value: float) -> None:
    assert calc_lots(100.0, 25.0, pip_value) == 0.0


def test_calc_lots_is_zero_when_risk_is_below_one_step() -> None:
    """Депозит слишком мал для этого стопа — честный ноль, а не 0.01."""
    assert calc_lots(1.0, 100.0, 10.0) == 0.0


def test_calc_lots_grows_with_risk_and_shrinks_with_stop() -> None:
    """Монотонность: больше риск — больше лот, дальше стоп — меньше лот."""
    assert calc_lots(20.0, 25.0, 10.0) > calc_lots(10.0, 25.0, 10.0)
    assert calc_lots(10.0, 50.0, 10.0) < calc_lots(10.0, 25.0, 10.0)


def test_small_but_valid_stop_is_not_treated_as_invalid() -> None:
    """Стоп меньше пункта — редкий, но законный ввод (скальпинг на индексах).

    Мутант менял `stop_pips <= 0` на `<= 1`: такой стоп молча давал бы 0 лотов
    вместо расчёта, и пользователь не понял бы, почему калькулятор молчит.
    """
    assert calc_lots(10.0, 0.5, 10.0) == pytest.approx(2.0)


def test_small_pip_value_is_not_treated_as_invalid() -> None:
    """0.1 USD за пункт — это микро-лот EURUSD, самый частый случай новичка.

    Мутант `pip_value <= 1` отключал бы расчёт ровно для той аудитории,
    ради которой проект написан.
    """
    assert calc_lots(5.0, 25.0, 0.1) == pytest.approx(2.0)


def test_floor_step_is_exactly_one_hundredth() -> None:
    """Округление вниз идёт по сотым, а не по «примерно сотым».

    3.97 / (10 × 1) = 0.397 лота → 0.39. Мутант со множителем 101 давал 0.40:
    риск выше запланированного на 2.5% при внешне правдоподобном числе.
    """
    assert calc_lots(3.97, 10.0, 1.0) == pytest.approx(0.39)


def test_live_sensitive_pairs_are_the_ones_that_depend_on_the_rate() -> None:
    """Список «нужен живой курс» должен совпадать с тем, где USD не котируемый."""
    for pair in PIP_VALUE_USD_PER_LOT:
        depends_on_rate = not pair.endswith("USD")
        assert (pair in LIVE_SENSITIVE_PAIRS) is depends_on_rate, pair
