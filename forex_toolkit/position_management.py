"""Что делать, пока сделка открыта: безубыток, частичное закрытие, трейл.

Путь ученика в проекте закрыт с обеих сторон: «Перед сделкой» считает риск,
журнал разбирает результат. Середины не было — а именно там принимаются решения,
за которые журнал потом ставит нарушение. Перенос стопа он засчитывает как
ошибку и выдаёт задачу, но тренировать причину было нечем.

Модуль отвечает на вопрос **измеримо**, а не лозунгом: даёт прогнать одну и ту
же сделку с управлением и без него на тех же самых свечах и сравнить исход.

Правила, без которых числа были бы завышены
-------------------------------------------

1. **Внутри одной свечи порядок хай и лоу неизвестен.** Поэтому сначала всегда
   проверяется неблагоприятная сторона (для покупки — лоу, для продажи — хай).
   Это занижает пользу управления, а не завышает: если свеча задела и стоп, и
   цель, засчитывается стоп.
2. **Срабатывания проверяются после неблагоприятной стороны.** Иначе свеча,
   которая одновременно дотянулась до безубытка и до стопа, выглядела бы
   выигрышной.
3. **R считается от первоначального риска** (вход минус стоп). Частичное
   закрытие уменьшает объём, но не пересчитывает базу.

Без numpy и pandas: формулы зеркалятся в браузере один в один.
"""

from __future__ import annotations

from dataclasses import dataclass, field

LONG = "long"
SHORT = "short"


@dataclass(frozen=True)
class Plan:
    """Что делать с открытой позицией. `None` — не делать ничего."""

    breakeven_at: float | None = None
    """Перенести стоп в безубыток, когда прибыль достигнет стольких R."""
    partial_at: float | None = None
    """Закрыть часть на стольких R."""
    partial_fraction: float = 0.5
    trail_r: float | None = None
    """Тянуть стоп, держа эту дистанцию в R от лучшей достигнутой цены."""

    def is_plain(self) -> bool:
        """Ничего не делаем — держим до цели или стопа."""
        return (
            self.breakeven_at is None
            and self.partial_at is None
            and self.trail_r is None
        )


@dataclass(frozen=True)
class Outcome:
    total_r: float
    """Итог в R с учётом частичного закрытия."""
    reason: str
    """`take`, `stop`, `breakeven`, `trail`, `partial+stop`, `timeout`."""
    bars: int
    partial_taken: bool
    moved_to_breakeven: bool
    max_favourable_r: float
    """Сколько R сделка показывала в лучшей точке — цена упущенного."""

    def as_dict(self) -> dict:
        return {
            "total_r": round(self.total_r, 4),
            "reason": self.reason,
            "bars": self.bars,
            "partial_taken": self.partial_taken,
            "moved_to_breakeven": self.moved_to_breakeven,
            "max_favourable_r": round(self.max_favourable_r, 4),
        }


@dataclass
class _State:
    stop: float
    remaining: float = 1.0
    booked: float = 0.0
    partial_taken: bool = False
    moved_to_breakeven: bool = False
    trailed: bool = False
    best: float = 0.0
    notes: list[str] = field(default_factory=list)


def _r_of(price: float, entry: float, risk: float, direction: str) -> float:
    """Сколько R даёт цена. Риск всегда положительный."""
    if risk <= 0:
        return 0.0
    return (price - entry) / risk if direction == LONG else (entry - price) / risk


def simulate(
    candles: list[dict],
    *,
    entry_index: int,
    entry: float,
    stop: float,
    take: float,
    direction: str = LONG,
    plan: Plan | None = None,
) -> Outcome | None:
    """Проводит сделку по свечам после входа. `None`, если данных нет."""
    plan = plan or Plan()
    risk = abs(entry - stop)
    if risk <= 0 or entry_index + 1 >= len(candles):
        return None

    state = _State(stop=stop)
    reason = "timeout"
    bars = 0

    for index in range(entry_index + 1, len(candles)):
        candle = candles[index]
        bars = index - entry_index
        high = float(candle["high"])
        low = float(candle["low"])

        adverse = low if direction == LONG else high
        favourable = high if direction == LONG else low

        # 1. Неблагоприятная сторона — всегда первой (см. правило 1).
        hit_stop = adverse <= state.stop if direction == LONG else adverse >= state.stop
        if hit_stop:
            state.booked += state.remaining * _r_of(state.stop, entry, risk, direction)
            state.remaining = 0.0
            reason = _stop_reason(state)
            break

        # 2. Цель.
        hit_take = favourable >= take if direction == LONG else favourable <= take
        if hit_take:
            state.booked += state.remaining * _r_of(take, entry, risk, direction)
            state.remaining = 0.0
            reason = "take"
            break

        # 3. Что успела показать свеча — по этому и срабатывают правила.
        reached = _r_of(favourable, entry, risk, direction)
        state.best = max(state.best, reached)

        if plan.partial_at is not None and not state.partial_taken:
            if reached >= plan.partial_at:
                part = max(0.0, min(1.0, plan.partial_fraction))
                state.booked += state.remaining * part * plan.partial_at
                state.remaining *= 1.0 - part
                state.partial_taken = True

        if plan.breakeven_at is not None and not state.moved_to_breakeven:
            if reached >= plan.breakeven_at:
                state.stop = entry
                state.moved_to_breakeven = True

        if plan.trail_r is not None and state.best > plan.trail_r:
            trailed = (
                entry + (state.best - plan.trail_r) * risk
                if direction == LONG
                else entry - (state.best - plan.trail_r) * risk
            )
            better = trailed > state.stop if direction == LONG else trailed < state.stop
            if better:
                state.stop = trailed
                state.trailed = True

        if state.remaining <= 0:
            reason = "partial"
            break

    if state.remaining > 0 and reason == "timeout":
        last = float(candles[-1]["close"])
        state.booked += state.remaining * _r_of(last, entry, risk, direction)

    return Outcome(
        total_r=state.booked,
        reason=reason,
        bars=bars,
        partial_taken=state.partial_taken,
        moved_to_breakeven=state.moved_to_breakeven,
        max_favourable_r=state.best,
    )


def _stop_reason(state: _State) -> str:
    """Как именно закончилась сделка — по тому, кто последним двигал стоп."""
    if state.trailed:
        tail = "trail"
    elif state.moved_to_breakeven:
        tail = "breakeven"
    else:
        tail = "stop"
    return f"partial+{tail}" if state.partial_taken else tail


@dataclass(frozen=True)
class Comparison:
    """Одна и та же сделка с управлением и без — на тех же свечах."""

    plain: Outcome
    managed: Outcome

    @property
    def difference(self) -> float:
        return self.managed.total_r - self.plain.total_r

    @property
    def helped(self) -> bool:
        return self.difference > 0

    def as_dict(self) -> dict:
        return {
            "plain": self.plain.as_dict(),
            "managed": self.managed.as_dict(),
            "difference": round(self.difference, 4),
            "helped": self.helped,
        }


def compare(
    candles: list[dict],
    *,
    entry_index: int,
    entry: float,
    stop: float,
    take: float,
    direction: str = LONG,
    plan: Plan,
) -> Comparison | None:
    """Сравнивает «держать до конца» с управлением. `None`, если данных нет."""
    plain = simulate(
        candles,
        entry_index=entry_index,
        entry=entry,
        stop=stop,
        take=take,
        direction=direction,
        plan=Plan(),
    )
    managed = simulate(
        candles,
        entry_index=entry_index,
        entry=entry,
        stop=stop,
        take=take,
        direction=direction,
        plan=plan,
    )
    if plain is None or managed is None:
        return None
    return Comparison(plain=plain, managed=managed)


@dataclass(frozen=True)
class Verdict:
    """Итог по многим сделкам: помогло управление или нет."""

    trades: int
    plain_total: float
    managed_total: float
    helped: int
    hurt: int
    same: int

    @property
    def difference(self) -> float:
        return self.managed_total - self.plain_total

    def as_dict(self) -> dict:
        return {
            "trades": self.trades,
            "plain_total": round(self.plain_total, 3),
            "managed_total": round(self.managed_total, 3),
            "difference": round(self.difference, 3),
            "helped": self.helped,
            "hurt": self.hurt,
            "same": self.same,
        }


def summarize(comparisons: list[Comparison]) -> Verdict | None:
    """Свод по списку сравнений. `None`, если сравнивать нечего."""
    if not comparisons:
        return None
    return Verdict(
        trades=len(comparisons),
        plain_total=sum(c.plain.total_r for c in comparisons),
        managed_total=sum(c.managed.total_r for c in comparisons),
        helped=sum(1 for c in comparisons if c.difference > 1e-9),
        hurt=sum(1 for c in comparisons if c.difference < -1e-9),
        same=sum(1 for c in comparisons if abs(c.difference) <= 1e-9),
    )
