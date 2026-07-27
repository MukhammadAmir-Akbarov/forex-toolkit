"""Rule-based coaching from a trading journal CSV."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Mapping

YES_VALUES = {"1", "true", "yes", "y", "да", "ha"}
NO_VALUES = {"0", "false", "no", "n", "нет", "yoq", "yo'q"}


@dataclass(frozen=True)
class CoachRule:
    """One evidence-based action for the trader."""

    code: str
    title: str
    evidence: str
    action: str


@dataclass(frozen=True)
class CoachReport:
    """Analysis result with exactly three prioritized rules."""

    trade_count: int
    rules: tuple[CoachRule, CoachRule, CoachRule]


def _number(value: object) -> float | None:
    try:
        return float(str(value).strip().replace(",", "."))
    except (TypeError, ValueError):
        return None


def _first(row: Mapping[str, object], *names: str) -> str:
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _datetime(row: Mapping[str, object]) -> datetime | None:
    date = _first(row, "date")
    time = _first(row, "time")
    combined = f"{date} {time}".strip()
    if not combined:
        combined = _first(row, "open_time", "datetime")

    normalized = combined.replace("T", " ").replace("/", "-")
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d.%m.%Y %H:%M:%S",
        "%d.%m.%Y %H:%M",
    ):
        try:
            return datetime.strptime(normalized, fmt)
        except ValueError:
            continue
    return None


def _pnl(row: Mapping[str, object]) -> float:
    return _number(_first(row, "result_usd", "profit", "pnl")) or 0.0


def _outcome(row: Mapping[str, object]) -> str:
    value = _first(row, "outcome", "result").lower()
    if value in {"win", "loss", "be"}:
        return value
    pnl = _pnl(row)
    return "win" if pnl > 0 else "loss" if pnl < 0 else "be"


def _performance(row: Mapping[str, object]) -> float:
    result_r = _number(_first(row, "result_r", "r_multiple"))
    if result_r is not None:
        return result_r
    risk = _number(_first(row, "risk_usd", "risk"))
    if risk and risk > 0:
        return _pnl(row) / risk
    return _pnl(row)


def _rule_followed(row: Mapping[str, object]) -> bool | None:
    value = _first(row, "followed_rules", "rules").lower()
    if value in YES_VALUES:
        return True
    if value in NO_VALUES:
        return False
    return None


def load_journal(path: Path | str) -> list[dict[str, str]]:
    """Load a journal and retain closed trades only."""

    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    with source.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    return [
        row
        for row in rows
        if _first(row, "outcome", "result").lower() != "open"
        and (
            _first(row, "outcome", "result").lower() in {"win", "loss", "be"}
            or _number(_first(row, "result_usd", "profit", "pnl")) is not None
        )
    ]


def analyze_trades(rows: Iterable[Mapping[str, object]]) -> CoachReport:
    """Return three prioritized, actionable coaching rules."""

    trades = list(rows)
    if not trades:
        raise ValueError("В журнале нет закрытых сделок")

    indexed = list(enumerate(trades))
    ordered = [
        row
        for _, row in sorted(
            indexed,
            key=lambda item: (_datetime(item[1]) or datetime.min, item[0]),
        )
    ]
    candidates: list[CoachRule] = []

    loss_streak = 0
    for row in reversed(ordered):
        if _outcome(row) != "loss":
            break
        loss_streak += 1
    if loss_streak >= 2:
        candidates.append(
            CoachRule(
                code="anti_tilt",
                title="Включи anti-tilt паузу",
                evidence=f"Последние {loss_streak} сделки закрыты в минус.",
                action=(
                    "Не открывай новую сделку минимум до следующей сессии. "
                    "Перед возвратом письменно разберись с каждой потерей."
                ),
            )
        )

    known_rules = [
        followed
        for row in trades
        if (followed := _rule_followed(row)) is not None
    ]
    discipline = (
        sum(known_rules) / len(known_rules) * 100 if known_rules else None
    )
    if discipline is not None and discipline < 95:
        candidates.append(
            CoachRule(
                code="discipline",
                title="Верни дисциплину выше 95%",
                evidence=(
                    f"Правила соблюдены в {discipline:.1f}% из "
                    f"{len(known_rules)} отмеченных сделок."
                ),
                action=(
                    "Следующие 10 сделок открывай только после письменного "
                    "чек-листа. При одном нарушении остановись до следующего дня."
                ),
            )
        )

    evening = [
        row for row in trades
        if (stamp := _datetime(row)) is not None and stamp.hour >= 18
    ]
    evening_score = sum(_performance(row) for row in evening)
    if len(evening) >= 3 and evening_score < 0:
        candidates.append(
            CoachRule(
                code="evening_limit",
                title="Ограничь вечернюю сессию",
                evidence=(
                    f"После 18:00: {len(evening)} сделок, "
                    f"суммарный результат {evening_score:+.2f}."
                ),
                action=(
                    "На 2 недели не торгуй после 18:00. Затем проверь результат "
                    "на новой выборке минимум из 10 дневных сделок."
                ),
            )
        )

    pair_scores: dict[str, list[float]] = defaultdict(list)
    for row in trades:
        pair = _first(row, "pair", "symbol").upper()
        if pair:
            pair_scores[pair].append(_performance(row))
    weak_pairs = [
        (pair, scores)
        for pair, scores in pair_scores.items()
        if len(scores) >= 5 and sum(scores) < 0
    ]
    if weak_pairs:
        pair, scores = min(
            weak_pairs,
            key=lambda item: sum(item[1]) / len(item[1]),
        )
        candidates.append(
            CoachRule(
                code="weak_pair",
                title=f"Убери {pair} на 2 недели",
                evidence=(
                    f"{pair}: {len(scores)} сделок, средний результат "
                    f"{sum(scores) / len(scores):+.2f} на сделку."
                ),
                action=(
                    "Исключи эту пару из торгового плана на 2 недели. "
                    "Возвращай только после отдельного разбора сетапов."
                ),
            )
        )

    if len(candidates) < 3:
        candidates.append(
            CoachRule(
                code="risk_freeze",
                title="Не увеличивай риск",
                evidence=f"Закрытых сделок в выборке: {len(trades)}.",
                action=(
                    "Сохраняй текущий риск на сделку до следующего анализа "
                    "после ещё 10 закрытых сделок."
                ),
            )
        )

    if len(candidates) < 3:
        best_pair = max(
            pair_scores.items(),
            key=lambda item: (len(item[1]), sum(item[1])),
            default=("", []),
        )[0]
        scope = f" и сосредоточься на {best_pair}" if best_pair else ""
        candidates.append(
            CoachRule(
                code="focus",
                title="Сократи число переменных",
                evidence=(
                    f"Инструментов в выборке: {len(pair_scores)}; "
                    f"закрытых сделок: {len(trades)}."
                ),
                action=(
                    "До следующего анализа торгуй один основной сетап"
                    f"{scope}; не добавляй новые инструменты."
                ),
            )
        )

    if len(candidates) < 3:
        candidates.append(
            CoachRule(
                code="review",
                title="Назначь контрольную точку",
                evidence="Найдено меньше трёх критических отклонений.",
                action=(
                    "После каждой сессии заполняй результат и соблюдение правил. "
                    "Повтори анализ через 10 сделок."
                ),
            )
        )

    rules = tuple(candidates[:3])
    return CoachReport(
        trade_count=len(trades),
        rules=(rules[0], rules[1], rules[2]),
    )
