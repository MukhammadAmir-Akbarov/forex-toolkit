"""Подсчёт теста готовности: полосы, слабые категории и связь с CLI."""

from __future__ import annotations

import pytest
from risk_profile import QUESTIONS, category_analysis, interpret_score

from forex_toolkit.risk_profile import (
    band_for,
    max_score,
    score_profile,
)

# Вопросы CLI в том виде, в каком их получает общий счётчик и веб-страница.
CLI_QUESTIONS = [
    {
        "category": q.category,
        "options": [{"label": label, "points": points} for label, points in q.options],
    }
    for q in QUESTIONS
]


@pytest.mark.parametrize(
    ("percent", "expected"),
    [
        (100.0, "excellent"),
        (80.0, "excellent"),
        (79.9, "good"),
        (60.0, "good"),
        (40.0, "borderline"),
        (20.0, "high_risk"),
        (19.9, "critical"),
        (-168.3, "critical"),
    ],
)
def test_band_boundaries_are_inclusive_from_below(
    percent: float, expected: str
) -> None:
    assert band_for(percent) == expected


def test_best_answers_score_full_marks() -> None:
    best = [
        max(range(len(q["options"])), key=lambda i: q["options"][i]["points"])
        for q in CLI_QUESTIONS
    ]
    result = score_profile(CLI_QUESTIONS, best)
    assert result["total"] == max_score(CLI_QUESTIONS) == 300
    assert result["percent"] == pytest.approx(100.0)
    assert result["band"] == "excellent"
    assert result["weak_categories"] == []


def test_worst_answers_are_critical_and_flag_every_category() -> None:
    worst = [
        min(range(len(q["options"])), key=lambda i: q["options"][i]["points"])
        for q in CLI_QUESTIONS
    ]
    result = score_profile(CLI_QUESTIONS, worst)
    assert result["total"] == -505
    assert result["band"] == "critical"
    assert len(result["weak_categories"]) == 9


def test_scoring_matches_the_cli_verdict() -> None:
    """Одни и те же ответы должны давать один вердикт в пакете и в CLI."""
    answers = [i % len(q["options"]) for i, q in enumerate(CLI_QUESTIONS)]
    result = score_profile(CLI_QUESTIONS, answers)

    cli_total = sum(
        q["options"][a]["points"] for q, a in zip(CLI_QUESTIONS, answers, strict=True)
    )
    assert result["total"] == cli_total

    # interpret_score выбирает текст по той же полосе.
    text = interpret_score(int(cli_total), 300)
    marker = {
        "excellent": "ОТЛИЧНЫЙ",
        "good": "ХОРОШИЙ",
        "borderline": "ПОГРАНИЧНЫЙ",
        "high_risk": "ВЫСОКИЙ РИСК",
        "critical": "КРИТИЧЕСКИЙ",
    }[result["band"]]
    assert marker in text

    cli_scores: dict[str, int] = {}
    for q, a in zip(CLI_QUESTIONS, answers, strict=True):
        cli_scores[q["category"]] = (
            cli_scores.get(q["category"], 0) + q["options"][a]["points"]
        )
    analysis = category_analysis(cli_scores)
    for weak in result["weak_categories"]:
        assert weak in analysis or "СЛАБЫЕ ЗОНЫ" in analysis


def test_answers_must_cover_every_question() -> None:
    with pytest.raises(ValueError):
        score_profile(CLI_QUESTIONS, [0, 1])


def test_answer_outside_the_option_list_is_rejected() -> None:
    with pytest.raises(ValueError):
        score_profile(CLI_QUESTIONS, [99] + [0] * (len(CLI_QUESTIONS) - 1))
