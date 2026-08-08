"""Быстрая сверка расчётов виджетов с Python — без браузера.

Зачем: та же сверка через Playwright поднимает браузер ради одного числа, и
135 браузерных сценариев идут три с половиной минуты. Сами расчёты браузер не
требуют: они не трогают DOM и уже выставлены наружу как ``window.__fx*``.
Здесь виджет выполняется в песочнице Node (``tests/widget_sandbox.mjs``) и
отвечает за миллисекунды.

Браузерные сверки при этом остаются: они проверяют другое — что виджет вообще
подключился к странице, отрисовал результат и перевёл интерфейс. Разделение
такое: **здесь арифметика, там страница.**

Если Node не установлен, тесты пропускаются: у пакета нет и не должно быть
зависимости от него.
"""

from __future__ import annotations

import errno
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"
WIDGETS = ROOT / "_mkdocs" / "javascripts" / "widgets"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None, reason="нет node — быстрые сверки пропускаем"
)


def call(widget: str, function: str, *args, locale: str = "ru"):
    """Зовёт функцию виджета в песочнице Node и возвращает её результат.

    Аргументы уходят через stdin, а не через командную строку: сверка на полном
    архиве свечей занимает 278 КБ, а в Linux один аргумент командной строки
    ограничен 128 КБ. На macOS такого предела нет — поэтому первая версия
    проходила локально и падала в CI на всех ubuntu-джобах сразу.
    """
    completed = subprocess.run(
        ["node", str(SANDBOX), str(WIDGETS / f"{widget}.js"), function, "-", locale],
        input=json.dumps(list(args)),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert "error" not in payload, f"{widget}.{function}: {payload['error']}"
    return payload["result"]


# ─────────────────────────── Годовой итог для декларации ───────────────────

TAX_CASES = {
    "прибыльный год": [
        {"date": "2025-02-03", "pnl": 300.0},
        {"date": "2025-07-19", "pnl": -120.0},
        {"date": "2025-12-30", "pnl": 45.5},
    ],
    "убыточный год": [
        {"date": "2025-01-05", "pnl": -200.0},
        {"date": "2025-03-11", "pnl": 50.0},
    ],
    "битые записи": [
        {"date": "2025-04-04", "pnl": 80.0},
        {"date": "2025-04-05", "pnl": None},
        {"date": "не дата", "pnl": 999.0},
    ],
    "пустой журнал": [],
}


@pytest.mark.parametrize("name", list(TAX_CASES), ids=list(TAX_CASES))
def test_tax_summary_matches_python(name: str) -> None:
    from forex_toolkit.tax_summary import summarize_all

    trades = TAX_CASES[name]
    got = call("journal", "__fxTaxSummary", trades)
    expected = [year.as_dict() for year in summarize_all(trades)]

    assert len(got) == len(expected), f"{name}: разное число лет"
    for browser, python in zip(got, expected):
        assert browser["year"] == python["year"]
        assert browser["trades"] == python["trades"]
        for field in ("profit", "loss", "net", "taxable", "tax"):
            assert round(browser[field], 2) == python[field], f"{name}: {field}"


# ─────────────────────────── Дорогие привычки ──────────────────────────────


def trade(day, pnl, rules="yes", emotion="calm", pair="EURUSD", setup="a"):
    return {
        "date": f"2026-03-{day:02d}",
        "pnl": pnl,
        "rules": rules,
        "emotion": emotion,
        "pair": pair,
        "setup": setup,
    }


HABIT_CASES = {
    "нарушение плана": (
        [trade(i, 10.0) for i in range(1, 7)]
        + [trade(i, -30.0, rules="no") for i in range(10, 14)]
    ),
    "эмоция и пара": (
        [trade(i, 12.0) for i in range(1, 8)]
        + [trade(i, -25.0, emotion="fomo", pair="GBPJPY") for i in range(10, 14)]
    ),
    "чистый месяц": [trade(i, 5.0) for i in range(1, 12)],
    "две сделки — не привычка": (
        [trade(i, 8.0) for i in range(1, 10)]
        + [trade(i, -500.0, rules="no") for i in range(20, 22)]
    ),
}


@pytest.mark.parametrize("name", list(HABIT_CASES), ids=list(HABIT_CASES))
def test_habits_match_python(name: str) -> None:
    from forex_toolkit.habits import expensive_habits

    trades = HABIT_CASES[name]
    got = call("journal", "__fxHabits", trades, 3)
    expected = [habit.as_dict() for habit in expensive_habits(trades, limit=3)]

    assert len(got) == len(expected), f"{name}: разное число привычек"
    for browser, python in zip(got, expected):
        assert browser["key"] == python["key"]
        assert browser["trades"] == python["trades"]
        for field in ("total", "avg_with", "avg_without", "cost"):
            assert round(browser[field], 2) == python[field], f"{name}: {field}"


# ─────────────────────────── Капитал для жизни ─────────────────────────────

LIVING_CASES = [
    (500.0, 0.015, 6, 1000.0, 200.0),
    (300.0, 0.01, 3, 0.0, 100.0),
    (1000.0, 0.03, 12, 5000.0, 500.0),
    (200.0, 0.005, 0, 0.0, 0.0),
]


@pytest.mark.parametrize(
    "case", LIVING_CASES, ids=[f"${c[0]:.0f}" for c in LIVING_CASES]
)
def test_living_capital_matches_python(case) -> None:
    from forex_toolkit.living_capital import plan_for

    need, monthly_return, buffer_months, start, add = case
    got = call(
        "living-capital",
        "__fxLivingCapital",
        need,
        monthly_return,
        buffer_months,
        start,
        add,
    )
    expected = plan_for(
        monthly_need=need,
        monthly_return=monthly_return,
        buffer_months=buffer_months,
        start=start,
        monthly_add=add,
    ).as_dict()

    for field in ("gross_needed", "required_capital", "buffer", "total_needed"):
        assert round(got[field], 2) == expected[field], field
    assert got["months_to_reach"] == expected["months_to_reach"]


# ─────────────────────────── Месяцы журнала ────────────────────────────────


def test_months_match_python() -> None:
    from forex_toolkit.habits import months_in

    trades = [
        {"date": "2026-03-01"},
        {"date": "2026-01-15"},
        {"date": "не дата"},
        {"date": "2025-12-31"},
    ]
    assert call("journal", "__fxMonths", trades) == months_in(trades)


# ─────────────────────────── Сама песочница ────────────────────────────────


def test_sandbox_reports_a_missing_function_instead_of_passing() -> None:
    """Опечатка в имени должна валить тест, а не тихо возвращать пустоту."""
    completed = subprocess.run(
        ["node", str(SANDBOX), str(WIDGETS / "journal.js"), "__fxНетТакой", "[]", "ru"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    payload = json.loads(completed.stdout)
    assert "error" in payload and "не объявлена" in payload["error"]


def test_a_command_line_too_long_never_passes_quietly() -> None:
    """Длинный аргумент обязан отвергаться — но отказывают разные слои.

    Сверка на полном архиве занимает 278 КБ. В Linux один аргумент командной
    строки ограничен 128 КБ: там процесс даже не запускается, `execve` отдаёт
    E2BIG. В macOS предела нет, и молчаливый проход как раз и был причиной
    того, что сверка зеленела локально и валила все ubuntu-джобы сразу —
    поэтому песочница отказывает сама.

    Годится любой из двух отказов. Не годится третий исход: тихо посчитать.
    """
    oversized = json.dumps([[{"date": "2025-01-01", "pnl": 1.0}] * 4000])
    command = [
        "node",
        str(SANDBOX),
        str(WIDGETS / "journal.js"),
        "__fxTaxSummary",
        oversized,
        "ru",
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=30)
    except OSError as error:  # Linux: до Node дело не доходит
        assert error.errno == errno.E2BIG, error
        return

    payload = json.loads(completed.stdout)  # macOS: отказывает песочница
    assert "stdin" in payload.get("error", ""), payload


def test_sandbox_takes_a_payload_larger_than_the_command_line_limit() -> None:
    """А через stdin тот же объём обязан проходить — иначе сверять нечем."""
    trades = [{"date": "2025-01-01", "pnl": 1.0}] * 4000
    assert len(json.dumps([trades]).encode()) > 131_072, "набор перестал быть большим"
    assert call("journal", "__fxTaxSummary", trades)[0]["trades"] == 4000


def test_sandbox_runs_every_widget_that_exposes_logic() -> None:
    """Если виджет перестанет выполняться вне браузера, узнаем сразу."""
    for widget, function in (
        ("journal", "__fxTaxSummary"),
        ("journal", "__fxHabits"),
        ("living-capital", "__fxLivingCapital"),
        ("trade-desk", "__fxRiskBudget"),
    ):
        completed = subprocess.run(
            ["node", str(SANDBOX), str(WIDGETS / f"{widget}.js"), function, "[]", "ru"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        payload = json.loads(completed.stdout)
        assert "виджет не выполнился" not in payload.get("error", ""), (
            f"{widget}: {payload.get('error')}"
        )


# ─────────────────────── Свечные паттерны и их исход ────────────────────────
# Проверяем не только совпадение, но и то, что тренажёр не приукрашивает:
# доля отработавших должна оставаться около половины.


def _archive_series():
    from forex_toolkit.pattern_outcomes import decode_episode

    episodes = json.loads(
        (ROOT / "_mkdocs" / "data" / "replay-episodes.json").read_text(encoding="utf-8")
    )["episodes"]
    return [decode_episode(episode) for episode in episodes]


def test_pattern_stats_match_python_on_the_real_archive():
    from forex_toolkit.pattern_outcomes import collect_stats

    series = _archive_series()
    got = call("pattern-trainer", "__fxPatternStats", series, 5)
    expected = {key: stat.as_dict() for key, stat in collect_stats(series).items()}

    assert set(got) == set(expected), "разный набор паттернов"
    for key, python in expected.items():
        browser = got[key]
        assert browser["found"] == python["found"], f"{key}: разное число находок"
        assert browser["worked"] == python["worked"], (
            f"{key}: разное число отработавших"
        )
        assert browser["flat"] == python["flat"], f"{key}: разное число ничьих"
        assert round(browser["rate"], 4) == python["rate"], f"{key}: разная доля"


def test_browser_finds_the_same_patterns_in_a_single_series():
    from forex_toolkit.pattern_outcomes import find_patterns

    candles = _archive_series()[0]
    got = call("pattern-trainer", "__fxFindPatterns", candles)
    expected = [{"index": m.index, "key": m.key} for m in find_patterns(candles)]

    assert got == expected


@pytest.mark.parametrize("index", [10, 20, 30])
def test_outcome_matches_python(index: int) -> None:
    from forex_toolkit.pattern_outcomes import outcome_after

    candles = _archive_series()[0]
    got = call("pattern-trainer", "__fxPatternOutcome", candles, index, 5)

    assert got == outcome_after(candles, index, horizon=5)


# ──────────────────── Переобучение: браузер == пакет ───────────────────────


def _overfit_rows() -> list[dict]:
    path = ROOT / "_mkdocs" / "data" / "overfitting.json"
    return json.loads(path.read_text(encoding="utf-8"))["rows"]


def test_overfitting_summary_matches_python() -> None:
    """Вывод страницы — это число. Оно обязано совпасть с пакетом до знака."""
    from forex_toolkit.overfitting import summarize

    rows = _overfit_rows()
    got = call("overfitting", "__fxOverfitSummary", rows, 20)
    expected = summarize(rows, min_trades=20)

    assert expected is not None
    assert got["considered"] == expected.considered
    assert got["rank_out"] == expected.rank_out
    assert round(got["median_out"], 3) == round(expected.median_out, 3)
    assert round(got["mean_out"], 3) == round(expected.mean_out, 3)
    assert round(got["correlation"], 6) == round(expected.correlation, 6)
    assert round(got["degradation"], 3) == round(expected.degradation, 3)
    assert got["beat_median"] == expected.beat_median
    assert got["best_in"]["params"] == expected.best_in.params
    assert got["best_out"]["params"] == expected.best_out.params


def test_overfitting_thin_samples_are_dropped_in_the_browser_too() -> None:
    """Фильтр по числу сделок обязан работать в обоих зеркалах одинаково."""
    from forex_toolkit.overfitting import summarize

    rows = [
        {
            "params": {"rr": 1},
            "in": {"total_r": 99.0, "trades": 2},
            "out": {"total_r": 99.0, "trades": 2},
        },
        {
            "params": {"rr": 2},
            "in": {"total_r": 10.0, "trades": 50},
            "out": {"total_r": 3.0, "trades": 50},
        },
    ]
    got = call("overfitting", "__fxOverfitSummary", rows, 20)
    expected = summarize(rows, min_trades=20)
    assert got["considered"] == expected.considered == 1
    assert got["best_in"]["params"] == expected.best_in.params == {"rr": 2}


def test_overfitting_correlation_matches_python() -> None:
    from forex_toolkit.overfitting import correlation

    for xs, ys in (
        ([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]),
        ([1.0, 2.0, 3.0], [6.0, 4.0, 2.0]),
        ([1.0, 1.0, 1.0], [3.0, 7.0, 11.0]),
        ([3.0, -1.0, 4.0, 1.5], [2.0, 2.5, -3.0, 0.0]),
    ):
        got = call("overfitting", "__fxOverfitCorrelation", xs, ys)
        assert round(got, 9) == round(correlation(xs, ys), 9), (xs, ys)
