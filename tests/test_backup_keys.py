"""Гард: каждый ключ прогресса из виджетов попадает в бэкап кабинета.

Прогресс живёт в localStorage; если новый виджет заводит свой ключ и его
забыли добавить в KEYS у dashboard.js, «Экспорт JSON» молча его теряет.
"""

import re
from pathlib import Path

JS = Path(__file__).resolve().parent.parent / "_mkdocs" / "javascripts"

# Служебные ключи UI/напоминаний — не прогресс пользователя.
NOT_PROGRESS = {"fx_menu_seen_v1"}


def _storage_keys() -> set[str]:
    keys: set[str] = set()
    for path in JS.rglob("*.js"):
        src = path.read_text(encoding="utf-8")
        keys.update(re.findall(r"localStorage\.setItem\(\s*[\"']([^\"']+)[\"']", src))
        if "localStorage.setItem(" in src:
            const = r"\b(?:KEY|STORE_KEY|STORAGE_KEY)\s*=\s*[\"']([^\"']+)[\"']"
            keys.update(re.findall(const, src))
    return {k for k in keys if not k.startswith("ftk-remind") and k not in NOT_PROGRESS}


def test_all_progress_keys_are_backed_up() -> None:
    dash = (JS / "widgets" / "dashboard.js").read_text(encoding="utf-8")
    block = re.search(r"var KEYS = \[(.*?)\];", dash, re.S)
    assert block
    backed = set(re.findall(r"\"([^\"]+)\"", block.group(1)))
    missing = _storage_keys() - backed
    assert not missing, f"добавь в KEYS dashboard.js: {sorted(missing)}"
