#!/usr/bin/env python3
"""Страж дублей документации.

``_mkdocs/`` — единственный источник правды для контента сайта. Скрипт падает,
если в репозитории появился ``.md`` вне ``_mkdocs/``, дублирующий путь внутри
``_mkdocs/`` (раньше из-за таких копий контент незаметно расходился — например,
корневой ``index.md`` отстал от ``_mkdocs/index.md`` на десятки строк).

Запуск:
    python tools/check_docs_sync.py

Коды возврата: 0 — дублей нет; 1 — найдены дубли (печатается список).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "_mkdocs"

# Верхнеуровневые мета-файлы проекта — это не контент сайта, их не трогаем.
ALLOWED_ROOT_MD = {
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "DISCLAIMER.md",
    "HOW-TO-USE.md",
    "LAUNCH.md",
    "MAINTAINER-30D.md",
    "CLAUDE.md",
    "CHANGELOG.md",
    "LICENSE-CONTENT.md",
    "TODO.md",
}


def tracked_md() -> list[Path]:
    # core.quotepath=false → не-ASCII имена (кириллица) выводятся в UTF-8,
    # а не в octal-escape, иначе их пути не сматчатся с _mkdocs/.
    out = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", "*.md"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    return [Path(p) for p in out]


def main() -> int:
    dupes: list[Path] = []
    for rel in tracked_md():
        if rel.parts and rel.parts[0] == "_mkdocs":
            continue  # сам источник правды
        if str(rel) in ALLOWED_ROOT_MD:
            continue  # мета-файлы проекта
        if (MKDOCS / rel).exists():
            dupes.append(rel)

    if dupes:
        print("❌ Найдены дубли контента (копия уже есть в _mkdocs/):")
        for d in sorted(dupes):
            print(f"   {d}  ↔  _mkdocs/{d}")
        print()
        print("_mkdocs/ — единственный источник правды. Удали корневую копию")
        print("или перенеси изменения в _mkdocs/ (см. CONTRIBUTING.md / CLAUDE.md).")
        return 1

    print("✅ Дублей документации нет — _mkdocs/ единственный источник правды.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
