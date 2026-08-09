from datetime import date

import pytest

from forex_toolkit.risk_budget import ClosedTrade, RiskLimits, risk_budget_summary


def test_risk_budget_combines_open_and_new_risk() -> None:
    summary = risk_budget_summary(
        planned_percent=0.5,
        open_percent=1.25,
        new_percent=1.0,
        trades=[],
        limits=RiskLimits(max_open_percent=2),
        today=date(2026, 8, 6),
    )

    assert summary["after_percent"] == pytest.approx(2.25)
    assert summary["remaining_open_percent"] == 0
    assert summary["reasons"] == ["open"]
    assert summary["requires_confirmation"] is True


def test_risk_budget_tracks_day_week_and_latest_loss_streak() -> None:
    trades = [
        ClosedTrade(date(2026, 8, 3), -1),
        ClosedTrade(date(2026, 8, 5), -1.25),
        ClosedTrade(date(2026, 8, 6), -1),
    ]
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0.5,
        new_percent=0.5,
        trades=trades,
        limits=RiskLimits(daily_loss_r=1, weekly_loss_r=3, pause_after_losses=3),
        today=date(2026, 8, 6),
    )

    assert summary["daily_r"] == pytest.approx(-1)
    assert summary["weekly_r"] == pytest.approx(-3.25)
    assert summary["loss_streak"] == 3
    assert summary["reasons"] == ["daily", "weekly", "streak"]


def test_risk_limits_reject_invalid_values() -> None:
    with pytest.raises(ValueError):
        RiskLimits(max_open_percent=0)


# ── Границы, которые нашло мутационное тестирование ────────────────────────
#
# Тесты выше проходили и на подменённом коде: `>` на `>=`, «безубыток считается
# убытком», `break` на `return`. Ниже — ровно те случаи, на которых подмена
# видна. Каждый тест убивает конкретного выжившего мутанта, поэтому удалять их
# бессмысленно: mutmut найдёт дыру снова (см. tools/mutation.md).


def test_risk_exactly_at_the_limit_is_allowed() -> None:
    """2.0% при лимите 2.0% — это ещё можно, а не уже нельзя.

    Разница между `>` и `>=` здесь — целое подтверждение на экране: с `>=`
    пользователь получал бы предупреждение на каждой сделке по лимиту.
    """
    summary = risk_budget_summary(
        planned_percent=0.5,
        open_percent=1.0,
        new_percent=1.0,
        trades=[],
        limits=RiskLimits(max_open_percent=2),
        today=date(2026, 8, 6),
    )

    assert summary["after_percent"] == pytest.approx(2.0)
    assert summary["remaining_open_percent"] == pytest.approx(0.0)
    assert summary["reasons"] == []
    assert summary["requires_confirmation"] is False


def test_daily_limit_fires_exactly_on_the_boundary() -> None:
    """−2R при лимите 2R — уже стоп, а не «ещё чуть-чуть»."""
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0,
        new_percent=0.5,
        trades=[ClosedTrade(date(2026, 8, 6), -2.0)],
        limits=RiskLimits(daily_loss_r=2, weekly_loss_r=5),
        today=date(2026, 8, 6),
    )

    assert summary["reasons"] == ["daily"]
    assert summary["remaining_daily_r"] == pytest.approx(0.0)


def test_weekly_limit_fires_exactly_on_the_boundary() -> None:
    """−5R за неделю при лимите 5R — уже стоп. То же, что для дня, но неделя
    считается по другому окну, и её границу надо пинать отдельно."""
    trades = [
        ClosedTrade(date(2026, 8, 3), -2.5),
        ClosedTrade(date(2026, 8, 4), -2.5),
    ]
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0,
        new_percent=0.5,
        trades=trades,
        limits=RiskLimits(daily_loss_r=10, weekly_loss_r=5),
        today=date(2026, 8, 6),
    )

    assert summary["weekly_r"] == pytest.approx(-5.0)
    assert summary["reasons"] == ["weekly"]
    assert summary["remaining_weekly_r"] == pytest.approx(0.0)


def test_remaining_weekly_budget_can_be_a_fraction() -> None:
    """Полтинник недельного запаса — это 0.5R, а не «ещё целый R»."""
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0,
        new_percent=0.5,
        trades=[ClosedTrade(date(2026, 8, 4), -4.5)],
        limits=RiskLimits(daily_loss_r=10, weekly_loss_r=5),
        today=date(2026, 8, 6),
    )

    assert summary["remaining_weekly_r"] == pytest.approx(0.5)
    assert summary["reasons"] == []


def test_remaining_budget_can_be_a_fraction() -> None:
    """Остаток 0.5R должен показываться как 0.5, а не округляться вверх.

    Мутант заменял `max(0.0, …)` на `max(1.0, …)`: пользователю с почти
    исчерпанным лимитом рисовался бы целый R запаса, которого нет.
    """
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0,
        new_percent=0.5,
        trades=[ClosedTrade(date(2026, 8, 6), -1.5)],
        limits=RiskLimits(daily_loss_r=2, weekly_loss_r=5),
        today=date(2026, 8, 6),
    )

    assert summary["remaining_daily_r"] == pytest.approx(0.5)
    assert summary["remaining_weekly_r"] == pytest.approx(3.5)
    assert summary["reasons"] == []


def test_breakeven_trade_interrupts_the_loss_streak() -> None:
    """Безубыток — не убыток: серия обнуляется.

    Иначе пауза после трёх убытков наступала бы после трёх сделок в ноль,
    то есть после ничего.
    """
    trades = [
        ClosedTrade(date(2026, 8, 3), -1),
        ClosedTrade(date(2026, 8, 4), -1),
        ClosedTrade(date(2026, 8, 5), 0.0),
        ClosedTrade(date(2026, 8, 6), -1),
    ]
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0,
        new_percent=0.5,
        trades=trades,
        limits=RiskLimits(pause_after_losses=3),
        today=date(2026, 8, 6),
    )

    assert summary["loss_streak"] == 1
    assert "streak" not in summary["reasons"]


def test_small_win_interrupts_the_loss_streak() -> None:
    """+0.5R — уже прибыль. Мутант считал прибылью только +1R и больше."""
    trades = [
        ClosedTrade(date(2026, 8, 3), -1),
        ClosedTrade(date(2026, 8, 4), -1),
        ClosedTrade(date(2026, 8, 5), 0.5),
        ClosedTrade(date(2026, 8, 6), -1),
    ]
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0,
        new_percent=0.5,
        trades=trades,
        limits=RiskLimits(pause_after_losses=3),
        today=date(2026, 8, 6),
    )

    assert summary["loss_streak"] == 1


def test_loss_streak_counts_only_the_run_after_the_last_win() -> None:
    """Прерывание должно оставлять посчитанное, а не терять его.

    Мутант менял `break` на `return`: цикл выходил без значения, и вся
    серия превращалась в None. Тест ловит это только если победа стоит
    ПЕРЕД серией убытков — то есть выход из цикла реально случается.
    """
    trades = [
        ClosedTrade(date(2026, 8, 1), -1),
        ClosedTrade(date(2026, 8, 2), 2.0),
        ClosedTrade(date(2026, 8, 4), -1),
        ClosedTrade(date(2026, 8, 5), -1),
    ]
    summary = risk_budget_summary(
        planned_percent=0,
        open_percent=0,
        new_percent=0.5,
        trades=trades,
        limits=RiskLimits(pause_after_losses=3),
        today=date(2026, 8, 6),
    )

    assert summary["loss_streak"] == 2


def test_negative_percentage_is_rejected() -> None:
    """Отрицательный риск — ошибка ввода, а не «риск наоборот».

    Мутант менял `or` на `and`: бесконечность проходила бы проверку, потому
    что она не отрицательная.
    """
    with pytest.raises(
        ValueError, match=r"^risk percentages must be non-negative finite numbers$"
    ):
        risk_budget_summary(
            planned_percent=-0.5,
            open_percent=0,
            new_percent=0.5,
            trades=[],
            today=date(2026, 8, 6),
        )


def test_infinite_percentage_is_rejected() -> None:
    with pytest.raises(
        ValueError, match=r"^risk percentages must be non-negative finite numbers$"
    ):
        risk_budget_summary(
            planned_percent=0.5,
            open_percent=float("inf"),
            new_percent=0.5,
            trades=[],
            today=date(2026, 8, 6),
        )


def test_summary_keys_match_the_browser_contract() -> None:
    """Имена ключей — часть контракта с trade-desk.js и сохранёнными планами.

    Переименование здесь тихо ломает уже сохранённые в браузере планы:
    `risk_guard.reasons` внутри них ссылается на эти же метки.
    """
    summary = risk_budget_summary(
        planned_percent=0.5,
        open_percent=0.5,
        new_percent=0.5,
        trades=[],
        today=date(2026, 8, 6),
    )

    assert set(summary) == {
        "planned_percent",
        "open_percent",
        "new_percent",
        "after_percent",
        "remaining_open_percent",
        "daily_r",
        "weekly_r",
        "remaining_daily_r",
        "remaining_weekly_r",
        "loss_streak",
        "requires_confirmation",
        "reasons",
    }
