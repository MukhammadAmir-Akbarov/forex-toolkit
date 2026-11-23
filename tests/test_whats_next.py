"""«Что дальше» в конце главы: маршрут по главам с квизами и выбор шага.

Маршрут живёт в chapter-quiz.js (ROUTE), а кабинет держит ту же карту в
CHAPTER_PATHS (dashboard.js). Тест держит их в синхроне с навигацией сайта
и с ключами квизов на самих страницах; выбор шага (``window.__fxNextStep``)
выполняется в Node-песочнице.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WIDGETS = ROOT / "_mkdocs" / "javascripts" / "widgets"
QUIZ = WIDGETS / "chapter-quiz.js"
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"
NOW = "2026-11-23T12:00:00+00:00"


def _route() -> list[tuple[str, str]]:
    src = QUIZ.read_text(encoding="utf-8")
    block = re.search(r"var ROUTE = \[(.*?)\];", src, re.S)
    assert block
    return re.findall(r'\["([\w-]+)", "([\w/-]+)"\]', block.group(1))


ROUTE = _route()
KEYS = [k for k, _ in ROUTE]


def test_route_matches_dashboard_map() -> None:
    dash = (WIDGETS / "dashboard.js").read_text(encoding="utf-8")
    block = re.search(r"var CHAPTER_PATHS = \{(.*?)\};", dash, re.S)
    assert block
    paths = dict(re.findall(r'"([\w-]+)": "([\w/-]+)"', block.group(1)))
    assert dict(ROUTE) == paths
    assert len(ROUTE) == 21


def test_route_follows_site_navigation_order() -> None:
    nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    nav = nav[nav.index("\nnav:") :]
    order = [m + "/" for m in re.findall(r":\s*([\w/-]+)\.md\s*$", nav, re.M)]
    wanted = {p for _, p in ROUTE}
    assert [p for p in order if p in wanted] == [p for _, p in ROUTE]


@pytest.mark.parametrize(("key", "path"), ROUTE)
def test_every_route_page_carries_its_quiz(key: str, path: str) -> None:
    for suffix in ("", ".en", ".uz"):
        page = ROOT / "_mkdocs" / f"{path.rstrip('/')}{suffix}.md"
        assert f'data-quiz-key="{key}"' in page.read_text(encoding="utf-8"), page


def _step(results: dict, current: str, now: str = NOW) -> dict:
    now_ms = int(datetime.fromisoformat(now).timestamp() * 1000)
    done = subprocess.run(
        ["node", str(SANDBOX), str(QUIZ), "__fxNextStep", "-", "ru"],
        input=json.dumps([results, current, now_ms]),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


def _passed(*keys: str, when: str = "2026-11-20T10:00:00Z") -> dict:
    return {k: {"passed": True, "updatedAt": when} for k in keys}


NO_NODE = shutil.which("node") is None


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_nothing_to_suggest_until_the_chapter_quiz_is_passed() -> None:
    failed = {"scaling-in": {"passed": False, "updatedAt": NOW}}
    assert _step(failed, "scaling-in")["kind"] == "quiz"
    assert _step({}, "scaling-in")["kind"] == "quiz"


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_next_skips_chapters_already_passed() -> None:
    results = _passed("technical-analysis", "strategy-details", "real-analysis")
    step = _step(results, "technical-analysis")
    assert step == {
        "kind": "next",
        "key": "order-types-mechanics",
        "refresh": None,
        "passed": 3,
    }


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_end_of_route_wraps_to_skipped_chapters() -> None:
    results = _passed(*[k for k in KEYS if k != "gold-trading"])
    assert _step(results, "swap-free")["key"] == "gold-trading"


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_all_passed_is_done_and_old_quiz_asks_for_refresh() -> None:
    results = _passed(*KEYS)
    results["lot-discipline"]["updatedAt"] = "2026-10-01T10:00:00Z"  # 53 дня назад
    step = _step(results, "law-faq")
    assert step["kind"] == "done" and step["key"] is None
    assert step["refresh"] == "lot-discipline" and step["passed"] == 21


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_current_chapter_is_never_its_own_refresh() -> None:
    results = _passed("cycle-theory", when="2026-09-01T10:00:00Z")
    assert _step(results, "cycle-theory")["refresh"] is None
