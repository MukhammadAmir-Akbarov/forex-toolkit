#!/usr/bin/env python3
"""Кросс-локальный чекер внутренних ссылок и якорей по СОБРАННОМУ сайту.

Зачем: `mkdocs build --strict` проверяет, что целевая *страница* существует, но
НЕ проверяет фрагменты `#anchor` — а мы уже ловили вручную битые русские якоря
в EN-страницах (заголовки перевели, а `#якорь` остался старым). Этот инструмент
парсит готовый `site/` и для каждой внутренней ссылки с `#fragment` проверяет,
что на целевой странице реально есть элемент с таким `id`.

Работает по реальному HTML, который сгенерировал MkDocs, поэтому не зависит от
тонкостей slugify (uslugify, кириллица, двойные дефисы) — берём настоящие `id`.

Использование:
    python tools/check_links.py            # требует собранный site/
    python tools/check_links.py --build    # собрать site/ перед проверкой
    python tools/check_links.py --site DIR  # нестандартный каталог сайта

Код возврата 1, если найдены битые якоря (для CI).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urljoin

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"


class _Collector(HTMLParser):
    """Собирает из HTML-страницы: все id/name (якоря) и все href ссылок."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        # <a name="..."> — устаревший якорь, но MkDocs/расширения могут давать.
        if tag == "a" and d.get("name"):
            self.ids.add(d["name"])
        if tag == "a" and d.get("href"):
            self.hrefs.append(d["href"])


def _parse(path: Path) -> _Collector:
    c = _Collector()
    c.feed(path.read_text(encoding="utf-8", errors="replace"))
    return c


def _is_external(href: str) -> bool:
    h = href.strip().lower()
    return (
        h.startswith("http://")
        or h.startswith("https://")
        or h.startswith("mailto:")
        or h.startswith("tel:")
        or h.startswith("data:")
        or h.startswith("//")
    )


def check_site(site: Path) -> tuple[int, int, list[str]]:
    """Возвращает (проверено_якорей, страниц, список_проблем)."""
    pages = sorted(site.rglob("*.html"))
    # Кэш якорей по файлу, чтобы не парсить целевые страницы повторно.
    cache: dict[Path, set[str]] = {}

    def ids_of(p: Path) -> set[str]:
        if p not in cache:
            cache[p] = _parse(p).ids if p.exists() else set()
        return cache[p]

    problems: list[str] = []
    checked = 0

    for page in pages:
        col = cache.get(page)
        if col is None:
            parsed = _parse(page)
            cache[page] = parsed.ids
            hrefs = parsed.hrefs
        else:
            # уже распарсили ids как цель; href нужно достать заново
            hrefs = _parse(page).hrefs

        rel_page = page.relative_to(site)
        for href in hrefs:
            # Внешние и ссылки без #фрагмента нас не интересуют: существование
            # самой страницы уже проверяет mkdocs build --strict.
            if not href or _is_external(href) or "#" not in href:
                continue
            base, frag = urldefrag(href)
            if not frag:
                continue
            frag = unquote(frag)

            # Куда указывает ссылка.
            if base == "" or base is None:
                target = page  # якорь на этой же странице
            else:
                # Разрешаем относительный URL от URL текущей страницы.
                page_url = "/" + rel_page.as_posix()
                joined = urljoin(page_url, base)
                joined = unquote(joined).lstrip("/")
                tpath = site / joined
                if tpath.is_dir():
                    tpath = tpath / "index.html"
                elif tpath.suffix != ".html":
                    # ссылка на не-HTML (png/py/csv) — якоря не наша забота
                    continue
                target = tpath

            if not target.exists():
                # битую страницу ловит build --strict; здесь не дублируем
                continue

            checked += 1
            if frag not in ids_of(target):
                problems.append(
                    f"  ❌ {rel_page}  →  {href}\n"
                    f"     якорь #{frag} отсутствует на целевой странице"
                )

    return checked, len(pages), problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Чекер внутренних якорей по site/")
    ap.add_argument("--site", type=Path, default=SITE)
    ap.add_argument(
        "--build", action="store_true", help="собрать site/ перед проверкой"
    )
    args = ap.parse_args()

    if args.build:
        print("🔨 mkdocs build --strict …")
        r = subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--strict", "--quiet"],
            cwd=REPO,
        )
        if r.returncode != 0:
            print("❌ build упал — чинить сборку прежде чем проверять ссылки.")
            return r.returncode

    if not args.site.exists():
        print(
            f"❌ Каталог сайта не найден: {args.site}\n"
            f"   Собери его: python tools/check_links.py --build"
        )
        return 1

    checked, pages, problems = check_site(args.site)
    print(f"🔗 Проверено якорей: {checked} на {pages} страницах")
    if problems:
        print(f"\n⚠️  Битых якорей: {len(problems)}\n")
        print("\n".join(problems))
        print(
            "\nПочини ссылку или заголовок-цель. Якоря берутся из реального HTML "
            "(slugify MkDocs), так что проверяй точное написание #фрагмента."
        )
        return 1
    print("✅ Все внутренние якоря ведут на существующие заголовки.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
