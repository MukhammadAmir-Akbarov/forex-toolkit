# CLAUDE.md — правила работы с этим репозиторием

Образовательный forex-проект для новичков. Три части в одном репо:

1. **Python-пакет `forex-toolkit`** (`forex_toolkit/`) — калькуляторы, индикаторы,
   бэктестер, ~8 CLI-команд. Публикуемый артефакт.
2. **Многоязычный учебник на MkDocs** (`_mkdocs/`, локали RU/EN/UZ) → GitHub Pages.
3. **Advanced-слой** (`advanced/`) — брокерские API (MT5/Binance), Telegram-бот,
   Streamlit, walk-forward, журнал сделок.

> ⚠️ Образовательный материал, **не финансовый совет**. Багфиксы в финансовых
> расчётах — самое важное: всегда проверяй математику и прогоняй тесты.

## Команды

```bash
# окружение
python -m venv .venv && .venv/bin/pip install -e ".[dev]"

# тесты (должны проходить все 74+)
.venv/bin/pytest -q

# линт/формат/типы (dev-инструменты)
.venv/bin/ruff check . && .venv/bin/ruff format --check .
.venv/bin/mypy forex_toolkit

# документация (локальный предпросмотр / сборка)
.venv/bin/mkdocs serve
.venv/bin/mkdocs build            # сайт собирается из _mkdocs/, кладётся в site/

# проверка перед коммитом (всё сразу)
.venv/bin/python tools/check_docs_sync.py              # дубли доков
.venv/bin/python tools/check_translation_coverage.py  # наличие переводов
.venv/bin/python tools/check_translation_drift.py      # свежесть переводов (дрейф)
# или просто: /forex-check
```

> После правки RU-страницы и обновления её переводов отметь их свежими:
> `python tools/sync_translation_manifest.py --file <путь от _mkdocs/>`.
> Манифест `tools/i18n-manifest.json` — единственный источник правды о том, под
> какой sha256 RU сделан каждый перевод (детали — [IMPROVEMENTS.md](IMPROVEMENTS.md) I1).

## Источник правды для документации

- **`_mkdocs/` — единственный источник правды** для контента сайта.
  `mkdocs.yml` указывает `docs_dir: _mkdocs`, деплой идёт только из него.
- Корневых дублей `.md` (`docs/`, `extras/`, `growth/`, `journal/`...) больше нет —
  они удалены, чтобы контент не расходился. Сборщики PDF/DOCX
  (`tools/build_pdf.py`, `tools/build_docx.py`) читают `_mkdocs/forex-guide*.md`.
- `tools/check_docs_sync.py` в CI падает, если в корне снова появится `.md`,
  дублирующий путь из `_mkdocs/`. Не создавай такие файлы.
- Переводы: рядом с `page.md` кладём `page.en.md` и `page.uz.md`
  (суффиксный режим `mkdocs-static-i18n`). RU — дефолтная локаль.

## Ловушки этого репо (читать перед правками)

- **CLI работает из установленного wheel** через `runpy`: `forex_toolkit/cli.py`
  сначала ищет скрипты в `forex_toolkit/_tools/` (force-include в wheel), потом
  в репозитории (`tools/`, `bot/`). Если добавляешь новую команду — добавь скрипт
  и в `[tool.hatch.build.targets.wheel.force-include]` в `pyproject.toml`.
- **Финансовая математика — только в `forex_toolkit/fx_math.py`.** Не переписывай
  формулы pip-value / calc_lots в инструментах: импортируй из `fx_math`
  (с фолбэком на `sys.path`, чтобы скрипт работал и без установки пакета).
- **Тесты импортируют инструменты по голым именам** (`from pip_calculator import ...`):
  это работает потому, что `tests/conftest.py` добавляет `tools/`, `bot/`,
  `strategies/`, `advanced/`, `journal/` в `sys.path`. Не переименовывай публичные
  функции инструментов без обновления тестов.
- `mkdocs build --strict` проходит и **включён в CI** (джоб `docs`). Кириллические
  якоря работают благодаря `toc.slugify: pymdownx.slugs.uslugify` в `mkdocs.yml` —
  без него оглавления (`#что-такое-forex …`) не совпадают с заголовками. Заголовки
  с разделителем в slug дают двойной дефис (` — ` → `--`); для одинарного дефиса в
  якоре используй `:` в заголовке. Ссылки на исходники (`.py/.csv/.png`) из страниц
  сайта веди на GitHub (`blob/main/…`), а не относительным путём — их нет в `site/`.

## Что НЕ коммитим

`.venv/`, `site/`, `dist/`, сгенерированные PDF/DOCX, `data/*.csv`,
личные данные журнала (`journal/personal-*`, `journal/my-trades.csv`),
`материал/`, секреты (`.env`). Всё уже в `.gitignore`.

## Стиль

- Python: PEP 8, типизация для новых функций, докстринги по-русски — как в проекте.
- Коммиты: imperative mood с префиксом (`feat:`, `fix:`, `docs:`, `test:`,
  `refactor:`, `ci:`, `deps:`). См. `CONTRIBUTING.md`.
- Тестируется на numpy/pandas (см. `pyproject.toml`); локально проверено на
  numpy 2.x / pandas 3.x / Python 3.12+.
