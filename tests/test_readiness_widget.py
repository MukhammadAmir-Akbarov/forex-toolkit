"""Вердикт «Готов ли я к реалу?»: страницы, якоря и логика критериев.

Логика выполняется в песочнице Node (``tests/widget_sandbox.mjs``), как в
``test_drawdown_widget.py``. Пороги обязаны совпадать с чек-листом
``journal/demo-vs-real-comparison.md``: 3 месяца, PF ≥ 1.5, winrate ≥ 40%,
нарушения < 5%.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WIDGET = ROOT / "_mkdocs" / "javascripts" / "widgets" / "readiness.js"
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"
PAGES = [
    ROOT / "_mkdocs" / "tools" / f"demo-readiness{s}.md" for s in ("", ".en", ".uz")
]
INPUTS = ["rd-months", "rd-trades", "rd-winrate", "rd-rr", "rd-dd", "rd-viol"]

READY = {
    "months": 3,
    "trades": 50,
    "winrate": 40,
    "rr": 2.25,  # PF = 0.4·2.25/0.6 = 1.5 ровно на границе
    "maxDD": 20,
    "violations": 4.9,
    "journal": True,
    "canLose": True,
}


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_page_declares_widget_and_inputs(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    assert text.startswith("---\nwidgets: [readiness]\n---")
    for el in [*INPUTS, "rd-journal", "rd-canlose", "rd-result"]:
        assert f'id="{el}"' in text, f"{page.name}: нет #{el}"


def _verdict(stats: dict) -> dict:
    done = subprocess.run(
        ["node", str(SANDBOX), str(WIDGET), "__fxReadiness", "-", "ru"],
        input=json.dumps([stats]),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


NO_NODE = shutil.which("node") is None


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_all_thresholds_met_is_ready() -> None:
    v = _verdict(READY)
    assert v["ready"] is True
    assert v["pf"] == pytest.approx(1.5)
    assert v["expectancy"] == pytest.approx(0.4 * 2.25 - 0.6)


@pytest.mark.skipif(NO_NODE, reason="нет node")
@pytest.mark.parametrize(
    ("overrides", "failed"),
    [
        ({"months": 2}, "months"),
        ({"trades": 49}, "trades"),
        ({"winrate": 39, "rr": 3}, "winrate"),  # PF 1.92 — валится только winrate
        ({"rr": 2.2}, "pf"),
        ({"maxDD": 21}, "maxDD"),
        ({"violations": 5}, "violations"),
        ({"journal": False}, "journal"),
        ({"canLose": False}, "canLose"),
    ],
)
def test_one_unmet_item_means_too_early(overrides, failed) -> None:
    v = _verdict({**READY, **overrides})
    assert v["ready"] is False
    assert [c["id"] for c in v["checks"] if not c["ok"]] == [failed]
