---
name: forex-check
description: Pre-commit health check for the forex-toolkit repo — runs the test suite, linter/formatter, type check, docs build, and the docs-duplication guard, then reports a concise pass/fail summary. Use before committing or when asked to "check the project", "run all checks", or "/forex-check".
---

# /forex-check — проверка проекта перед коммитом

Запусти по порядку и собери краткий отчёт (✅/❌ по каждому пункту). Используй
`.venv/bin/...` если виртуальное окружение есть, иначе системные команды.
Не останавливайся на первой ошибке — прогони всё и покажи сводку в конце.

1. **Тесты**
   ```bash
   .venv/bin/pytest -q
   ```
   Все 74+ должны проходить.

2. **Линт + формат** (если `ruff` установлен; иначе отметь «пропущено»)
   ```bash
   .venv/bin/ruff check .
   .venv/bin/ruff format --check .
   ```

3. **Типы** (если `mypy` установлен)
   ```bash
   .venv/bin/mypy forex_toolkit
   ```

4. **Документация собирается** (без `--strict` — в репо есть унаследованные
   битые якоря; падать на них не нужно)
   ```bash
   .venv/bin/mkdocs build 2>&1 | tail -5
   ```

5. **Нет дублей доков** (корень не должен дублировать `_mkdocs/`)
   ```bash
   .venv/bin/python tools/check_docs_sync.py
   ```

6. **Wheel-CLI не сломан** (быстрая проверка импорта точек входа)
   ```bash
   .venv/bin/python -c "import forex_toolkit.cli as c; print('cli ok')"
   ```

## Отчёт

Выведи таблицу: пункт → статус → короткая причина при падении. В конце —
один из двух вердиктов: «✅ Готово к коммиту» или «❌ Есть проблемы: …».
Если что-то упало, предложи конкретную следующую команду для починки.
