"""Проверка ведения открытой позиции.

Здесь легко получить приятные и неверные числа, поэтому тесты в первую очередь
закрепляют консервативные правила, а не удобные случаи:

* если свеча задела и стоп, и цель — засчитывается стоп;
* срабатывания (безубыток, частичное, трейл) проверяются ПОСЛЕ стопа;
* R считается от первоначального риска, частичное закрытие базу не меняет.

Без этих правил тренажёр обещал бы пользу управления, которой нет.
"""

from __future__ import annotations

import pytest

from forex_toolkit.position_management import (
    Plan,
    compare,
    simulate,
    summarize,
)

ENTRY = 100.0
STOP = 90.0
TAKE = 120.0  # риск 10, цель +2R


def bar(high, low, close=None):
    return {"open": low, "high": high, "low": low, "close": close if close else low}


def run(bars, plan=None, **kw):
    candles = [bar(ENTRY, ENTRY, ENTRY)] + bars
    return simulate(
        candles,
        entry_index=0,
        entry=ENTRY,
        stop=STOP,
        take=TAKE,
        direction=kw.get("direction", "long"),
        plan=plan,
    )


def test_take_gives_the_planned_reward():
    got = run([bar(125, 99)])
    assert got.total_r == pytest.approx(2.0)
    assert got.reason == "take"


def test_stop_gives_minus_one():
    got = run([bar(105, 85)])
    assert got.total_r == pytest.approx(-1.0)
    assert got.reason == "stop"


def test_one_bar_touching_both_counts_as_a_loss():
    """Порядок хай и лоу внутри свечи неизвестен — считаем худший."""
    got = run([bar(125, 85)])
    assert got.total_r == pytest.approx(-1.0)
    assert got.reason == "stop"


def test_breakeven_turns_a_loss_into_zero():
    plan = Plan(breakeven_at=1.0)
    bars = [bar(112, 99), bar(101, 95, close=96)]

    managed = run(bars, plan)
    assert managed.moved_to_breakeven is True
    assert managed.total_r == pytest.approx(0.0)
    assert managed.reason == "breakeven"

    plain = run(bars)
    assert plain.reason == "timeout"
    assert plain.total_r == pytest.approx(-0.4)


def test_breakeven_does_not_trigger_below_its_level():
    plan = Plan(breakeven_at=1.5)
    got = run([bar(112, 99), bar(101, 85)], plan)
    assert got.moved_to_breakeven is False
    assert got.total_r == pytest.approx(-1.0)


def test_partial_books_at_the_trigger_and_the_rest_keeps_running():
    plan = Plan(partial_at=1.0, partial_fraction=0.5)
    got = run([bar(112, 99), bar(105, 85)], plan)

    assert got.partial_taken is True
    # 0.5 объёма зафиксировано на +1R, остаток словил стоп на -1R
    assert got.total_r == pytest.approx(0.0)
    assert got.reason == "partial+stop"


def test_partial_then_take_uses_the_remaining_size():
    plan = Plan(partial_at=1.0, partial_fraction=0.5)
    got = run([bar(112, 99), bar(125, 110)], plan)
    # 0.5 × 1R + 0.5 × 2R
    assert got.total_r == pytest.approx(1.5)
    assert got.reason == "take"


def test_closing_everything_at_the_trigger_ends_the_trade():
    plan = Plan(partial_at=1.0, partial_fraction=1.0)
    got = run([bar(112, 99), bar(125, 85)], plan)
    assert got.total_r == pytest.approx(1.0)
    assert got.reason == "partial"


def test_trailing_locks_in_part_of_the_move():
    plan = Plan(trail_r=1.0)
    got = run([bar(115, 99), bar(116, 104)], plan)
    # лучшая точка 1.5R, стоп подтянут на 0.5R и задет
    assert got.total_r == pytest.approx(0.5)
    assert got.reason == "trail"
    assert got.max_favourable_r == pytest.approx(1.5)


def test_trailing_keeps_the_level_reached_earlier():
    """Откат цены не отменяет уже подтянутый стоп.

    Оговорка честности: проверка `better` в коде (стоп не двигается назад) при
    нынешней формуле **недостижима** — `best` монотонно растёт, значит и
    подтянутый уровень тоже. Она оставлена как страховка на случай другой
    формулы, но тестом не покрывается: тест, который «покрывает» недостижимую
    ветку, проходил бы и на сломанном коде. Проверено — так и было.
    """
    plan = Plan(trail_r=1.0)
    got = run([bar(118, 99), bar(112, 108), bar(101, 95)], plan)
    # лучшая 1.8R → стоп 108; следующая свеча его и задевает
    assert got.total_r == pytest.approx(0.8)
    assert got.reason == "trail"


def test_timeout_exits_at_the_last_close():
    got = run([bar(105, 99, close=104)])
    assert got.reason == "timeout"
    assert got.total_r == pytest.approx(0.4)


def test_short_side_is_mirrored():
    candles = [bar(100, 100, 100), {"open": 100, "high": 101, "low": 79, "close": 80}]
    got = simulate(
        candles,
        entry_index=0,
        entry=100.0,
        stop=110.0,
        take=80.0,
        direction="short",
    )
    assert got.reason == "take"
    assert got.total_r == pytest.approx(2.0)


def test_no_room_to_trade_returns_none():
    assert run([]) is None
    assert (
        simulate(
            [bar(100, 100), bar(101, 99)],
            entry_index=0,
            entry=100.0,
            stop=100.0,
            take=120.0,
        )
        is None
    ), "нулевой риск — не сделка"


def test_comparison_says_whether_management_helped():
    plan = Plan(breakeven_at=1.0)
    bars = [bar(ENTRY, ENTRY, ENTRY), bar(112, 99), bar(101, 95, close=96)]
    got = compare(bars, entry_index=0, entry=ENTRY, stop=STOP, take=TAKE, plan=plan)
    assert got.helped is True
    assert got.difference == pytest.approx(0.4)


def test_verdict_counts_helped_hurt_and_same():
    plan = Plan(breakeven_at=1.0)
    helped = compare(
        [bar(ENTRY, ENTRY, ENTRY), bar(112, 99), bar(101, 95, close=96)],
        entry_index=0,
        entry=ENTRY,
        stop=STOP,
        take=TAKE,
        plan=plan,
    )
    same = compare(
        [bar(ENTRY, ENTRY, ENTRY), bar(125, 99)],
        entry_index=0,
        entry=ENTRY,
        stop=STOP,
        take=TAKE,
        plan=plan,
    )
    verdict = summarize([helped, same])
    assert verdict.trades == 2
    assert verdict.helped == 1
    assert verdict.same == 1
    assert verdict.hurt == 0


def test_nothing_to_summarize_returns_none():
    assert summarize([]) is None


def test_management_can_make_things_worse_and_that_is_reported():
    """Тренажёр обязан уметь показывать вред, иначе он реклама, а не тренажёр."""
    plan = Plan(breakeven_at=1.0)
    # Цена сходила на +1.2R, вернулась к входу, а потом дошла бы до цели.
    bars = [bar(ENTRY, ENTRY, ENTRY), bar(112, 99), bar(105, 99), bar(125, 104)]
    got = compare(bars, entry_index=0, entry=ENTRY, stop=STOP, take=TAKE, plan=plan)
    assert got.plain.total_r == pytest.approx(2.0)
    assert got.managed.total_r == pytest.approx(0.0)
    assert got.helped is False
    assert got.difference == pytest.approx(-2.0)
