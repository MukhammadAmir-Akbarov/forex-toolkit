"""Property-based тесты финансового ядра (L2, hypothesis).

Мутационное тестирование (tools/mutation.md) показало, где тесты слепы:
риск ровно по лимиту, округление лота, размер пункта иены. Примерные тесты
проверяют точки, которые автор вспомнил; свойства ниже проверяют инварианты,
которые обязаны держаться на ЛЮБЫХ входных данных:

- реальный риск никогда не больше планового (округление лота только вниз);
- лот неотрицателен и кратен шагу 0.01;
- лот монотонно убывает по размеру стопа;
- размер пункта: JPY-пары — 0.01, остальные — 0.0001;
- в риск-бюджете лимит срабатывает строго выше границы, а не «ровно на ней».
"""

from __future__ import annotations

import math
from datetime import date, timedelta

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from forex_toolkit.fx_math import (
    calc_lots,
    normalize_pair,
    pip_size,
    pip_value_in_account_currency,
    pip_value_in_quote,
)
from forex_toolkit.risk_budget import (
    ClosedTrade,
    RiskLimits,
    consecutive_losses,
    risk_budget_summary,
)

# --- стратегии генерации -------------------------------------------------

risk_money = st.floats(min_value=0.0, max_value=1e7, allow_nan=False)
stop_pips = st.floats(min_value=0.1, max_value=1e4, allow_nan=False)
pip_value = st.floats(min_value=0.01, max_value=1e3, allow_nan=False)
lots_pos = st.floats(min_value=0.01, max_value=1e3, allow_nan=False)
price_pos = st.floats(min_value=0.1, max_value=1e4, allow_nan=False)
percents = st.floats(min_value=0.0, max_value=50.0, allow_nan=False)

ccy = st.sampled_from(["EUR", "USD", "GBP", "JPY", "AUD", "CHF", "CAD", "NZD"])


@st.composite
def fx_pair(draw):
    """Пара из двух РАЗНЫХ валют."""
    base = draw(ccy)
    quote = draw(ccy.filter(lambda c: c != base))
    return base + quote


# --- fx_math: размер и стоимость пункта -----------------------------------


@given(pair=fx_pair())
def test_pip_size_depends_only_on_jpy(pair):
    """JPY-пара → 0.01, любая другая → 0.0001. Регрессия на ошибку с иеной."""
    expected = 0.01 if "JPY" in pair else 0.0001
    assert pip_size(pair) == expected
    # normalize_pair не должен влиять на результат
    assert pip_size(pair.lower()) == expected
    assert pip_size(pair[:3] + "/" + pair[3:]) == expected


@given(lots=lots_pos, pair=fx_pair())
def test_pip_value_in_quote_positive_and_linear(lots, pair):
    """Стоимость пункта положительна и линейна по лотам."""
    value = pip_value_in_quote(lots, pair)
    assert value > 0
    doubled = pip_value_in_quote(lots * 2, pair)
    assert math.isclose(doubled, value * 2, rel_tol=1e-9)


@given(lots=lots_pos, pair=fx_pair(), price=price_pos)
def test_pip_value_account_currency_matches_quote_and_base(lots, pair, price):
    """Счёт в котируемой валюте = стоимость в quote; в базовой — деление на цену."""
    base, quote = pair[:3], pair[3:]
    in_quote = pip_value_in_quote(lots, pair)
    assert pip_value_in_account_currency(lots, pair, quote, price) == in_quote
    assert math.isclose(
        pip_value_in_account_currency(lots, pair, base, price),
        in_quote / price,
        rel_tol=1e-9,
    )


# --- fx_math: расчёт лота --------------------------------------------------


@given(risk=risk_money, stop=stop_pips, pv=pip_value)
def test_calc_lots_never_exceeds_planned_risk(risk, stop, pv):
    """Реальный риск посчитанного лота не превышает плановый."""
    lots = calc_lots(risk, stop, pv)
    assert lots >= 0
    assert lots * stop * pv <= risk + 1e-6


@given(risk=risk_money, stop=stop_pips, pv=pip_value)
def test_calc_lots_is_multiple_of_min_step(risk, stop, pv):
    """Лот округлён до шага 0.01 (и только вниз — см. предыдущий тест)."""
    lots = calc_lots(risk, stop, pv)
    assert math.isclose(lots * 100, round(lots * 100), abs_tol=1e-9)


@given(
    risk=st.floats(min_value=1.0, max_value=1e7, allow_nan=False),
    pv=pip_value,
    stop1=stop_pips,
    stop2=stop_pips,
)
def test_calc_lots_monotonic_in_stop(risk, pv, stop1, stop2):
    """Чем шире стоп, тем меньше (или столько же) лот."""
    assume(abs(stop1 - stop2) > 1e-9)
    lo, hi = min(stop1, stop2), max(stop1, stop2)
    assert calc_lots(risk, lo, pv) >= calc_lots(risk, hi, pv)


@given(
    risk=risk_money, pv=pip_value, bad_stop=st.floats(max_value=0.0, allow_nan=False)
)
def test_calc_lots_zero_on_invalid_stop(risk, pv, bad_stop):
    """Невалидный стоп → 0 лотов, а не отрицательная позиция."""
    assert calc_lots(risk, bad_stop, pv) == 0.0


@given(pair=fx_pair())
def test_normalize_pair_idempotent(pair):
    """Повторная нормализация ничего не меняет."""
    once = normalize_pair(pair)
    assert normalize_pair(once) == once
    assert normalize_pair(pair.lower()) == once


# --- risk_budget ------------------------------------------------------------


@given(open_pct=percents, new_pct=percents)
def test_open_limit_trips_strictly_above_the_edge(open_pct, new_pct):
    """Лимит открытого риска срабатывает ВЫШЕ границы, ровно на границе — нет.

    Это был выживший мутант («риск ровно по лимиту»): подмена `>` на `>=`
    делала лимит жёстче на один шаг и не ловилась примерными тестами.
    """
    limits = RiskLimits(max_open_percent=2.0)
    edge = 2.0 - open_pct
    assume(edge >= 0)
    on_edge = risk_budget_summary(
        planned_percent=0.0,
        open_percent=open_pct,
        new_percent=edge,
        trades=[],
        limits=limits,
    )
    assert "open" not in on_edge["reasons"]

    over = risk_budget_summary(
        planned_percent=0.0,
        open_percent=open_pct,
        new_percent=edge + 0.01,
        trades=[],
        limits=limits,
    )
    assert "open" in over["reasons"]
    assert over["requires_confirmation"] is True


@given(open_pct=percents, new_pct=percents)
def test_remaining_open_never_negative(open_pct, new_pct):
    """Остаток лимита не уходит в минус, сколько бы ни было открыто."""
    summary = risk_budget_summary(
        planned_percent=0.0,
        open_percent=open_pct,
        new_percent=new_pct,
        trades=[],
        limits=RiskLimits(max_open_percent=2.0),
    )
    assert summary["remaining_open_percent"] >= 0.0
    assert summary["after_percent"] == open_pct + new_pct
    assert summary["requires_confirmation"] == bool(summary["reasons"])


def _trade(days_ago: int, result_r: float, today: date) -> ClosedTrade:
    return ClosedTrade(closed_on=today - timedelta(days=days_ago), result_r=result_r)


@given(
    wins=st.lists(
        st.floats(min_value=0.01, max_value=10, allow_nan=False, allow_infinity=False),
        max_size=8,
    ),
    losses=st.lists(
        st.floats(
            min_value=-1e6, max_value=-0.01, allow_nan=False, allow_infinity=False
        ),
        max_size=8,
    ),
)
@settings(max_examples=60)
def test_consecutive_losses_resets_on_win(wins, losses):
    """Серия убытков обнуляется первой же прибыльной сделкой."""
    today = date(2026, 11, 1)
    # Убытки — в прошлом (2..n+1 дней назад), победа — СЕГОДНЯ (свежая сделка).
    # Серия считается от самой свежей сделки назад, поэтому свежая победа её рвёт.
    trades = [_trade(i + 2, r, today) for i, r in enumerate(losses)]
    if wins:
        trades.append(_trade(1, wins[0], today))
        assert consecutive_losses(trades) == 0
    else:
        assert consecutive_losses(trades) == len(losses)


@given(
    daily_loss=st.floats(min_value=0.0, max_value=10, allow_nan=False),
)
def test_daily_limit_boundary(daily_loss):
    """Дневной лимит: срабатывает ровно на -limit и ниже, не выше."""
    today = date(2026, 11, 1)
    limits = RiskLimits(daily_loss_r=2.0)
    trades = [_trade(0, -daily_loss, today)]
    summary = risk_budget_summary(
        planned_percent=0.0,
        open_percent=0.0,
        new_percent=0.0,
        trades=trades,
        limits=limits,
        today=today,
    )
    assert ("daily" in summary["reasons"]) == (daily_loss >= 2.0)
    assert summary["remaining_daily_r"] >= 0.0
