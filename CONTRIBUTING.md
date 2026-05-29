# Contributing to Forex Toolkit

Спасибо за желание помочь! / Thanks for wanting to help! / Yordamga tayyorligingiz uchun rahmat!

## Каналы / Channels

| Что | Где |
|---|---|
| 💬 Вопросы, обсуждения, идеи | [GitHub Discussions](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/discussions) |
| 🐛 Баги | [GitHub Issues](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/issues) |
| 🔒 Уязвимости безопасности | Смотри [SECURITY.md](SECURITY.md) |
| 🔧 Изменения в коде | Pull Request |

## Как сделать PR

1. **Форкни репозиторий** и склонируй локально
2. **Создай ветку**: `git checkout -b feature/my-improvement` (или `fix/bug-name`)
3. **Установи окружение**:
   ```bash
   python -m venv .venv
   .venv/bin/pip install -e ".[dev]"
   ```
4. **Запусти тесты**: `.venv/bin/pytest` — должны проходить все 74+
5. **Сделай изменения**. Стиль:
   - Python: PEP 8, типизация для новых функций
   - Markdown: одна пустая строка между секциями, заголовки в kebab-case для anchor
6. **Коммит** с понятным сообщением (см. ниже)
7. **Push + создай PR** в `main`. Заполни PR template, отметь связанный issue
8. **Дождись CI** — джобы `test`, `lint`, `coverage`, `package`, `docs` должны пройти

## Документация: где править

**`_mkdocs/` — единственный источник правды** для контента сайта (учебник,
гайды, шаблоны, журнал). Корневых копий больше нет.

- Правь страницы только в `_mkdocs/`. CI-страж `tools/check_docs_sync.py` не даст
  снова завести корневой `.md`, дублирующий путь из `_mkdocs/`.
- Переводы: клади `page.en.md` / `page.uz.md` рядом с `page.md` внутри `_mkdocs/`.
- PDF/DOCX-учебники собираются из `_mkdocs/` (`tools/build_pdf.py`,
  `tools/build_docx.py`) — отдельно дублировать главы не нужно.
- Перед коммитом прогони `/forex-check` (или вручную: `pytest`,
  `python tools/check_docs_sync.py`, `mkdocs build`).

## Стиль коммитов

Короткое сообщение в imperative mood. Префиксы:

| Префикс | Когда |
|---|---|
| `feat:` | новая функция |
| `fix:` | исправление бага |
| `docs:` | документация |
| `test:` | тесты |
| `refactor:` | рефакторинг без изменения поведения |
| `ci:` | CI/CD |
| `deps:` | обновление зависимостей |

Пример: `fix: position calculator now uses live rate for cross pairs`

## Что особенно приветствуется

- **Переводы** — добавляй файлы `.en.md` / `.uz.md` рядом с существующими `.md`
- **Новые стратегии** в `strategies/` с unit-тестами
- **Локальные ресурсы для Узбекистана** — брокеры, налоги, способы вывода
- **Уточнения по психологии и риск-менеджменту** — из реального опыта
- **Багфиксы в финансовых расчётах** — самое важное, проверяй math!

## Что НЕ принимаем

- ❌ «Грааль»-стратегии с обещанием 50% в месяц
- ❌ Реклама конкретных брокеров без сравнительного анализа
- ❌ Контент без дисклеймера про образовательность
- ❌ Лом ломов: API-ключи в коде, hardcoded пароли, скачивание из непроверяемых источников

## Code of Conduct

Все взаимодействия — на основе [Contributor Covenant 2.1](CODE_OF_CONDUCT.md). Будь добр и конструктивен. Грубость или дискриминация — бан.

## Лицензия

Отправляя PR, ты соглашаешься, что твой вклад выходит под лицензией [MIT](LICENSE).

---

## Контакты

- 💬 [Discussions](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/discussions) — публичные вопросы
- 📧 Через GitHub профиль — приватные вопросы

Спасибо за вклад в обучение трейдеров! 📈
