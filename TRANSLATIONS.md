# 🌍 Переводы / Translations / Tarjimalar

Проект многоязычный (RU → EN → UZ) через `mkdocs-static-i18n`. Сейчас переведена
малая часть страниц — это **отличная задача для первого вклада**: не нужен Python,
не нужны тесты, один markdown-файл мёржится сразу.

## Как перевести страницу (3 шага)

1. Возьми RU-файл в `_mkdocs/`, например `_mkdocs/practice/lot-discipline.md`.
2. Создай рядом перевод с суффиксом локали:
   - английский → `_mkdocs/practice/lot-discipline.en.md`
   - узбекский (лотин) → `_mkdocs/practice/lot-discipline.uz.md`
3. Переведи **только текст**: заголовки, абзацы, ячейки таблиц, подписи. НЕ трогай
   ссылки, пути к картинкам, тикеры (EUR/USD), числа, блоки кода и Mermaid.

Сохрани структуру 1-в-1 (те же заголовки и `!!! admonition`). Пример готового
перевода — `_mkdocs/practice/README.uz.md` и `_mkdocs/practice/README.en.md`.

Проверка: `mkdocs serve` и переключи язык вверху страницы.

> 💡 Можно попросить ассистента: используется агент `add-translation`
> (`.claude/agents/add-translation.md`) — он создаёт `.en.md`/`.uz.md` по правилам.

## Приоритет

**Сначала UZ** (недообслуженная домашняя аудитория), затем EN. В первую очередь —
раздел `practice/` (самые ценные «не слей депозит» главы) и калькуляторы `tools/`.

## Что уже переведено полностью (RU/EN/UZ)

- `index.md`, `roadmap.md`, `extras/market-data-sources.md`

## Что нужно перевести (приоритетные разделы)

### 🥇 practice/ — приоритет №1 (UZ, затем EN)
- [x] `practice/README.md` → **UZ ✓, EN ✓** (образец)
- [ ] `practice/lot-discipline.md`
- [ ] `practice/gold-trading.md`
- [ ] `practice/breakeven-protocol.md`
- [ ] `practice/scaling-in.md`
- [ ] `practice/cycle-theory.md`
- [ ] `practice/market-structure.md`

### 🛠️ tools/ — калькуляторы (высокая отдача)
- [ ] `tools/winrate-rr-calculator.md`
- [ ] `tools/pip-calculator.md` (есть EN, нужен UZ)
- [ ] `tools/compound-calculator.md` (есть EN, нужен UZ)
- [ ] `tools/flashcards.md`, `tools/risk-of-ruin.md` (новые виджеты)

### 🧠 extras/, 📝 journal/, 🌱 growth/ — по мере сил
Полный актуальный список незакрытых языков всегда можно получить командой:

```bash
python - <<'PY'
from pathlib import Path
src = Path("_mkdocs")
for p in sorted(src.rglob("*.md")):
    if p.name.endswith((".en.md", ".uz.md")):
        continue
    stem = str(p.with_suffix(""))
    miss = [s for s in (".en.md", ".uz.md") if not Path(stem + s).exists()]
    if miss:
        print(p.relative_to(src), "→ нет:", ", ".join(miss))
PY
```

## Узбекский: соглашения

- Латиница (O'zbek lotin), как в существующих `*.uz.md`.
- Финансовые термины оставляй узнаваемыми: «lot», «spread», «stop-loss» можно
  не переводить, если так понятнее новичку.
