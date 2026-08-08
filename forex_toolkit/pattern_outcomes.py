"""Свечные паттерны и то, чем они кончались в архиве.

Зачем именно так. Собственная страница проекта говорит: «**никогда не торговать
только по паттерну**», а экзамен — что стабильно угадывать направление не
получается ни у кого. Тренажёр вида «назови фигуру» учил бы обратному тому,
откуда он растёт: распознал молот — значит знаешь, куда пойдёт цена.

Поэтому здесь два действия, а не одно. Первое — найти фигуру (это навык
чтения графика, он полезен). Второе — **сразу показать, чем такие фигуры
кончались на реальных котировках**: какая доля отработала в обещанную сторону.
Обычно это около половины, и именно это число делает урок честным.

Правила распознавания не переписываются: берутся из ``forex_toolkit.candles``,
который работает и с pandas, и с обычными словарями. Третьей копии правил в
проекте быть не должно.

Что этот расчёт НЕ утверждает: что паттерн причина движения. Он измеряет
совпадение на конкретной выборке архива, и выборка маленькая — рядом всегда
стоит число находок.
"""

from __future__ import annotations

from dataclasses import dataclass

from .candles import (
    is_bearish_engulfing,
    is_bullish_engulfing,
    is_doji,
    is_hammer,
    is_shooting_star,
)

# Сколько свечей после фигуры смотрим, чтобы назвать исход.
DEFAULT_HORIZON = 5

# Меньше этого числа находок — статистику не показываем: доля по трём случаям
# ничего не значит и вводит в заблуждение сильнее, чем её отсутствие.
MIN_MATCHES = 5

# ключ -> (сколько свечей нужно, куда «обещает», человекочитаемое имя)
PATTERNS: dict[str, tuple[int, str]] = {
    "hammer": (1, "up"),
    "shooting_star": (1, "down"),
    "doji": (1, "none"),
    "bullish_engulfing": (2, "up"),
    "bearish_engulfing": (2, "down"),
}


@dataclass(frozen=True)
class Match:
    """Найденная фигура: индекс последней её свечи и ключ паттерна."""

    index: int
    key: str


@dataclass(frozen=True)
class PatternStats:
    key: str
    found: int
    worked: int
    """Сколько раз цена ушла в сторону, которую фигуре приписывают."""
    flat: int

    @property
    def rate(self) -> float:
        """Доля отработавших среди тех, где движение вообще было."""
        moved = self.found - self.flat
        return self.worked / moved if moved else 0.0

    def as_dict(self) -> dict[str, float | int | str]:
        return {
            "key": self.key,
            "found": self.found,
            "worked": self.worked,
            "flat": self.flat,
            "rate": round(self.rate, 4),
        }


def _at(candles: list[dict], index: int) -> dict:
    return candles[index]


def find_patterns(candles: list[dict]) -> list[Match]:
    """Все фигуры в ряду свечей; индекс указывает на последнюю свечу фигуры."""
    found: list[Match] = []
    for index in range(len(candles)):
        candle = _at(candles, index)
        if is_hammer(candle):
            found.append(Match(index, "hammer"))
        if is_shooting_star(candle):
            found.append(Match(index, "shooting_star"))
        if is_doji(candle):
            found.append(Match(index, "doji"))
        if index >= 1:
            previous = _at(candles, index - 1)
            if is_bullish_engulfing(previous, candle):
                found.append(Match(index, "bullish_engulfing"))
            if is_bearish_engulfing(previous, candle):
                found.append(Match(index, "bearish_engulfing"))
    return found


def outcome_after(
    candles: list[dict], index: int, *, horizon: int = DEFAULT_HORIZON
) -> str:
    """Куда ушла цена через ``horizon`` свечей: ``up``, ``down`` или ``flat``.

    ``flat`` — когда закрытие совпало с точностью до нуля; в статистике такие
    случаи выносятся отдельно, а не записываются в чей-то актив.
    Возвращает пустую строку, если будущих свечей не хватает.
    """
    target = index + horizon
    if target >= len(candles):
        return ""
    start = float(_at(candles, index)["close"])
    finish = float(_at(candles, target)["close"])
    if finish > start:
        return "up"
    if finish < start:
        return "down"
    return "flat"


def collect_stats(
    series: list[list[dict]], *, horizon: int = DEFAULT_HORIZON
) -> dict[str, PatternStats]:
    """Статистика по нескольким рядам свечей — например, по эпизодам Replay."""
    counters: dict[str, list[int]] = {key: [0, 0, 0] for key in PATTERNS}
    for candles in series:
        for match in find_patterns(candles):
            result = outcome_after(candles, match.index, horizon=horizon)
            if not result:
                continue
            promised = PATTERNS[match.key][1]
            counters[match.key][0] += 1
            if result == "flat":
                counters[match.key][2] += 1
            elif promised != "none" and result == promised:
                counters[match.key][1] += 1
    return {
        key: PatternStats(key=key, found=found, worked=worked, flat=flat)
        for key, (found, worked, flat) in counters.items()
    }


def decode_episode(episode: dict) -> list[dict]:
    """Свечи эпизода Replay из компактного вида в обычные словари.

    Эпизоды хранят целые пункты от опорной цены: ``base + k * pip``.
    """
    base = float(episode["base"])
    pip = float(episode["pip"])
    return [
        {
            "open": base + candle[0] * pip,
            "high": base + candle[1] * pip,
            "low": base + candle[2] * pip,
            "close": base + candle[3] * pip,
        }
        for candle in episode["k"]
    ]
