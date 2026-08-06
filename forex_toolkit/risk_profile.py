"""Подсчёт теста готовности к торговле — общий для CLI и веб-виджета.

Сами вопросы живут в двух местах намеренно: в ``tools/risk_profile.py`` для
CLI и в JSON-блоке каждой локализованной страницы для сайта (тексты нужно
переводить). А вот модель подсчёта — баллы, границы полос, определение слабых
категорий — обязана быть одна, иначе один и тот же ответ даст разный вердикт
в терминале и в браузере. Поэтому она здесь, а сверку JS == Python держит
``tests_e2e``.
"""

from __future__ import annotations

import math
from typing import Iterable, Mapping, Sequence

# Границы полос в процентах от максимума, от лучшей к худшей.
BANDS: tuple[tuple[float, str], ...] = (
    (80.0, "excellent"),
    (60.0, "good"),
    (40.0, "borderline"),
    (20.0, "high_risk"),
)
CRITICAL = "critical"

# Категория считается слабой, если набрано меньше половины её максимума.
WEAK_RATIO = 0.5


def band_for(percent: float) -> str:
    """Полоса вердикта по проценту от максимума."""
    if not math.isfinite(percent):
        raise ValueError("percent must be finite")
    for threshold, name in BANDS:
        if percent >= threshold:
            return name
    return CRITICAL


def _option_points(question: Mapping) -> list[float]:
    options = question.get("options") or []
    if not options:
        raise ValueError("question without options")
    return [float(option["points"]) for option in options]


def max_score(questions: Sequence[Mapping]) -> float:
    """Сумма лучших вариантов — знаменатель процента."""
    return sum(max(_option_points(question)) for question in questions)


def score_profile(
    questions: Sequence[Mapping],
    answers: Iterable[int],
) -> dict:
    """Итог теста: баллы, процент, полоса и слабые категории.

    ``answers`` — индексы выбранных вариантов, по одному на вопрос.
    """
    chosen = list(answers)
    if len(chosen) != len(questions):
        raise ValueError("answers must cover every question")

    total = 0.0
    per_category: dict[str, float] = {}
    category_max: dict[str, float] = {}
    for question, answer in zip(questions, chosen):
        points = _option_points(question)
        if not isinstance(answer, int) or not 0 <= answer < len(points):
            raise ValueError(f"answer out of range: {answer!r}")
        category = str(question.get("category") or "")
        total += points[answer]
        per_category[category] = per_category.get(category, 0.0) + points[answer]
        category_max[category] = category_max.get(category, 0.0) + max(points)

    top = max_score(questions)
    if top <= 0:
        raise ValueError("max score must be positive")
    percent = total / top * 100

    weak = sorted(
        category
        for category, limit in category_max.items()
        if limit > 0 and per_category[category] / limit < WEAK_RATIO
    )
    return {
        "total": total,
        "max_score": top,
        "percent": percent,
        "band": band_for(percent),
        "categories": {
            category: {
                "score": per_category[category],
                "max": category_max[category],
                "weak": category in weak,
            }
            for category in sorted(category_max)
        },
        "weak_categories": weak,
    }
