"""Строка отчёта rebuild_showcase_data не должна ронять прогон.

У витрин разные meta: сканеры пишут from/to, «Неделя на рынке» — week,
мультипарный прогон — только home_pair, у банка эпизодов meta нет вообще.
_describe обязан пережить любой из этих наборов: однажды он упал на min() от
пустого списка уже после успешной пересборки — и весь weekly workflow
покраснел на чисто косметическом шаге.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "rebuild_showcase_data",
    Path(__file__).resolve().parent.parent / "tools" / "rebuild_showcase_data.py",
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

_describe = module._describe


def test_describe_scanner_meta_with_from_to():
    document = {
        "meta": {
            "pair": "EURUSD",
            "timeframe": "1h",
            "from": "2024-01-01",
            "to": "2026-01-01",
            "generated_at": "2026-11-03",
        }
    }

    line = _describe(document)

    assert "EURUSD" in line and "2024-01-01 → 2026-01-01" in line


def test_describe_weekly_review_meta_with_week_range():
    document = {
        "meta": {
            "week": {"from": "2026-05-11", "to": "2026-05-17"},
            "generated_at": "2026-11-03",
        }
    }

    line = _describe(document)

    assert "2026-05-11 → 2026-05-17" in line


def test_describe_multipair_meta_without_period():
    document = {"meta": {"home_pair": "EURUSD", "timeframe": "1h"}}

    line = _describe(document)

    assert "EURUSD" in line and "без периода" in line


def test_describe_episode_bank_without_meta():
    document = {
        "episodes": [{"t": ["2025-01-05"]}, {"t": ["2024-06-10"]}],
        "generated_at": "2026-11-03",
    }

    line = _describe(document)

    assert "эпизодов: 2" in line and "2024-06-10" in line


def test_describe_empty_document_does_not_crash():
    line = _describe({})

    assert "без периода" in line
