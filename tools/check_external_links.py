#!/usr/bin/env python3
"""Проверка внешних ссылок учебника: живы ли регуляторы, брокеры и источники.

Зачем отдельный инструмент. ``check_links.py`` сознательно пропускает
``http(s)`` — он про якоря внутри собранного сайта. Но проект ведёт читателя на
реестры FCA/CySEC/ASIC/NFA/FINMA, на 12 брокеров и на источники котировок, и
мёртвая ссылка на регулятора бьёт по доверию сильнее битого якоря: человек
приходит проверить брокера и упирается в 404.

Почему это **не** гейт на каждый PR: внешний мир падает без нашего участия.
Красный CI из-за чужого таймаута приучает игнорировать красный CI. Поэтому
инструмент запускается по расписанию раз в неделю и по умолчанию возвращает 0.
``--fail`` есть для ручного прогона, когда результат нужен кодом возврата.

Использование:
    python tools/check_external_links.py                 # отчёт, всегда rc=0
    python tools/check_external_links.py --fail          # rc=1 при мёртвых
    python tools/check_external_links.py --only uz       # только раздел uz/
    python tools/check_external_links.py --timeout 15
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "_mkdocs"

# Ссылки вида [текст](https://…) и голые <https://…>.
LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)|<(https?://[^>\s]+)>")

# Куда ходить бессмысленно: шаблоны, примеры и заведомо приватные адреса.
SKIP_HOSTS = {
    "localhost",
    "127.0.0.1",
    "example.com",
    "example.org",
    "your-broker.com",
}

# Часть сайтов отдаёт 403 на любой запрос без «человеческого» заголовка —
# это не мёртвая ссылка, а защита от ботов, и ловить её как поломку нельзя.
USER_AGENT = (
    "Mozilla/5.0 (compatible; forex-toolkit-linkcheck/1.0; "
    "+https://github.com/MukhammadAmir-Akbarov/forex-toolkit)"
)

# 403/405 = «нас не пустили», а не «страницы нет». Считаем ссылку живой, но
# помечаем отдельно, чтобы человек мог глянуть глазами.
BLOCKED_CODES = {401, 403, 405, 406, 429}


def collect_links(root: Path, only: str | None = None) -> dict[str, list[str]]:
    """Собрать {url: [страницы, где встречается]} из markdown-исходников."""
    found: dict[str, list[str]] = defaultdict(list)
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        if only and not rel.startswith(only):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            url = match.group(1) or match.group(2)
            url = url.rstrip(".,;")
            host = (urlsplit(url).hostname or "").lower()
            if host in SKIP_HOSTS or host.endswith(".local"):
                continue
            if rel not in found[url]:
                found[url].append(rel)
    return dict(found)


def _describe(exc: BaseException) -> str:
    """Причина, а не имя класса.

    ``URLError`` одинаково выглядит и при отсутствующем домене, и при
    просроченном сертификате, и при блокировке по стране. Без разворачивания
    причины отчёт заставляет проверять всё руками — то есть не экономит ничего.
    """
    cause = getattr(exc, "reason", None)
    if isinstance(cause, BaseException):
        inner = getattr(cause, "strerror", None) or str(cause)
        return f"{type(cause).__name__}: {inner}".strip(": ")
    if cause:
        return str(cause)
    return f"{type(exc).__name__}: {exc}".strip(": ")


def probe(url: str, timeout: float) -> tuple[str, int | None, str]:
    """Вернуть (url, http_код или None, короткое описание)."""
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return url, response.status, "ok"
    except urllib.error.HTTPError as exc:
        # HEAD поддерживают не все — пробуем GET прежде чем звать ссылку мёртвой.
        if exc.code in {400, 404, 405, 501}:
            try:
                get = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(get, timeout=timeout) as response:
                    return url, response.status, "ok (GET)"
            except urllib.error.HTTPError as get_exc:
                return url, get_exc.code, get_exc.reason or "HTTP error"
            except Exception as get_exc:  # noqa: BLE001 — сеть отдаёт что угодно
                return url, None, _describe(get_exc)
        return url, exc.code, exc.reason or "HTTP error"
    except Exception as exc:  # noqa: BLE001 — таймауты, DNS, TLS, редиректы
        return url, None, _describe(exc)


def classify(code: int | None, note: str = "") -> str:
    """Отделить «сайта нет» от «до сайта не дошли отсюда».

    Таймаут к soliq.uz из другой страны — про сеть, а не про ссылку, и звать
    такое поломкой нельзя. А вот несуществующий домен (``gaierror``) — это
    ровно мёртвая ссылка: DNS отвечает всем одинаково.
    """
    if code is None:
        return "dead" if "gaierror" in note else "unreachable"
    if code in BLOCKED_CODES:
        return "blocked"
    if 200 <= code < 400:
        return "ok"
    return "dead"


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка внешних ссылок учебника")
    parser.add_argument("--only", help="проверять только раздел, например uz/")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--fail",
        action="store_true",
        help="вернуть 1, если есть мёртвые ссылки (по умолчанию всегда 0)",
    )
    args = parser.parse_args()

    links = collect_links(DOCS, args.only)
    if not links:
        print("Внешних ссылок не найдено — проверять нечего.")
        return 0

    print(f"🌍 Проверяю {len(links)} внешних ссылок …\n")
    results: dict[str, tuple[int | None, str]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(probe, url, args.timeout) for url in links]
        for future in concurrent.futures.as_completed(futures):
            url, code, note = future.result()
            results[url] = (code, note)

    buckets: dict[str, list[str]] = defaultdict(list)
    for url, (code, note) in results.items():
        buckets[classify(code, note)].append(url)

    for kind, icon, title in (
        ("dead", "❌", "Мёртвые"),
        ("unreachable", "⚠️ ", "Не ответили отсюда (сеть, не обязательно ссылка)"),
        ("blocked", "🔒", "Закрылись от бота (проверить глазами)"),
    ):
        urls = sorted(buckets.get(kind, []))
        if not urls:
            continue
        print(f"{icon} {title}: {len(urls)}")
        for url in urls:
            code, note = results[url]
            where = ", ".join(links[url][:3])
            more = f" (+{len(links[url]) - 3})" if len(links[url]) > 3 else ""
            print(f"   {code or '—'} {note}  {url}\n      ← {where}{more}")
        print()

    ok = len(buckets.get("ok", []))
    print(f"✅ Живых: {ok} из {len(links)}")

    dead = buckets.get("dead", [])
    if dead and args.fail:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
