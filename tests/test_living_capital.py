"""Сколько нужно капитала, чтобы жить с трейдинга.

Это число существует ради одного эффекта — показать реальный порядок величины
человеку, которому продали «доход с телефона». Поэтому оно обязано быть
считаемым на бумаге и не приукрашивать: налог учтён, подушка отдельно, а
недостижимая цель называется недостижимой.
"""

from __future__ import annotations

import pytest

from forex_toolkit.living_capital import (
    DEFAULT_TAX_RATE,
    months_to_reach,
    plan_for,
)


def test_capital_accounts_for_tax_before_dividing_by_return():
    """Чтобы получить на руки, заработать надо больше на ставку налога."""
    plan = plan_for(monthly_need=500.0, monthly_return=0.015, buffer_months=0)

    # 500 / 0.88 = 568.18 нужно заработать до налога
    assert plan.gross_needed == pytest.approx(568.18, abs=0.01)
    # 568.18 / 0.015 = 37 878.79 капитала
    assert plan.required_capital == pytest.approx(37878.79, abs=0.5)


def test_buffer_is_held_on_top_of_the_trading_capital():
    """Убыточный месяц не должен съедать сам капитал."""
    plan = plan_for(monthly_need=500.0, monthly_return=0.015, buffer_months=6)

    assert plan.buffer == pytest.approx(3000.0)
    assert plan.total_needed == pytest.approx(plan.required_capital + 3000.0)


def test_lower_return_demands_dramatically_more_capital():
    """Главный вывод инструмента: доходность в знаменателе."""
    optimistic = plan_for(monthly_need=500.0, monthly_return=0.03, buffer_months=0)
    realistic = plan_for(monthly_need=500.0, monthly_return=0.01, buffer_months=0)

    assert realistic.required_capital == pytest.approx(
        optimistic.required_capital * 3, rel=0.01
    )


def test_zero_tax_is_allowed_for_other_jurisdictions():
    plan = plan_for(
        monthly_need=100.0, monthly_return=0.01, tax_rate=0.0, buffer_months=0
    )

    assert plan.gross_needed == pytest.approx(100.0)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"monthly_need": 0.0, "monthly_return": 0.01},
        {"monthly_need": -100.0, "monthly_return": 0.01},
        {"monthly_need": 100.0, "monthly_return": 0.0},
        {"monthly_need": 100.0, "monthly_return": 1.0},
        {"monthly_need": 100.0, "monthly_return": -0.01},
        {"monthly_need": 100.0, "monthly_return": 0.01, "tax_rate": 1.0},
        {"monthly_need": 100.0, "monthly_return": 0.01, "buffer_months": -1},
    ],
)
def test_nonsense_input_is_rejected_rather_than_guessed(kwargs):
    with pytest.raises(ValueError):
        plan_for(**kwargs)


def test_reaching_the_target_takes_no_time_if_you_already_have_it():
    assert (
        months_to_reach(1000.0, start=1000.0, monthly_add=0.0, monthly_return=0.01) == 0
    )


def test_saving_without_return_still_reaches_the_target():
    """Ноль доходности — не ошибка: так копят на депозит перед торговлей."""
    assert (
        months_to_reach(1000.0, start=0.0, monthly_add=100.0, monthly_return=0.0) == 10
    )


def test_unreachable_target_is_reported_as_unreachable():
    """Без пополнения и без доходности цель не приблизится никогда."""
    assert (
        months_to_reach(1000.0, start=10.0, monthly_add=0.0, monthly_return=0.0) is None
    )


def test_compounding_beats_plain_saving():
    with_return = months_to_reach(
        10000.0, start=0.0, monthly_add=200.0, monthly_return=0.015
    )
    without = months_to_reach(10000.0, start=0.0, monthly_add=200.0, monthly_return=0.0)

    assert with_return is not None and without is not None
    assert with_return < without


def test_plan_reports_the_time_to_reach_the_whole_sum():
    plan = plan_for(
        monthly_need=300.0,
        monthly_return=0.015,
        buffer_months=6,
        start=1000.0,
        monthly_add=300.0,
    )

    assert plan.months_to_reach is not None
    # Проверяем шагами вручную: результат должен совпасть с моделью.
    balance = 1000.0
    for _ in range(plan.months_to_reach):
        balance = balance * 1.015 + 300.0
    assert balance >= plan.total_needed


def test_default_tax_matches_the_documented_rate():
    assert DEFAULT_TAX_RATE == 0.12


def test_as_dict_is_json_friendly():
    plan = plan_for(monthly_need=500.0, monthly_return=0.015)
    data = plan.as_dict()

    assert isinstance(data["months_to_reach"], (int, type(None)))
    assert data["required_capital"] > data["monthly_need"]
