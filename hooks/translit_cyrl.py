"""MkDocs-хук: статическое кириллическое зеркало узбекской локали (/uz-cyrl/).

Зачем: весь UZ-контент написан латиницей, а клиентский переключатель
(`javascripts/translit.js`) рисует кириллицу только в браузере — Google её НЕ
индексирует. Этот хук на `on_post_build` клонирует уже собранное дерево
``site/uz/`` в ``site/uz-cyrl/``, транслитерируя ТОЛЬКО видимый текст (как
translit.js — по текстовым узлам HTML, минуя code/pre/script/style/kbd/samp и
``.fx-no-translit``). Теги, атрибуты, id, href/src, тела <script>/<style> и
JSON-LD остаются байт-в-байт — поэтому виджеты, ссылки и якоря не ломаются.

Правила транслитерации портированы 1:1 из ``_mkdocs/javascripts/translit.js``
(см. tests/test_translit_cyrl.py — таблица паритета не даёт порту разойтись с JS).

Преобразование лотин→кирилл лоссовое (c,s→с; v,w→в; h→ҳ, x→х) — поэтому мы
КЛОНИРУЕМ страницы, оставляя латиницу оригиналом, и никогда не делаем обратное.
"""
from __future__ import annotations

import gzip
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

# --------------------------------------------------------------------------
# 1. Транслитерация лотин → кирилл (порт toCyrillic из translit.js)
# --------------------------------------------------------------------------

# Все варианты апострофа (ASCII, модификаторы ʻ ʼ, типографские ' ', `, ´, ′) → '
_APOS_RE = re.compile("[ʻʼ‘’`´′']")
# o'/g' (после нормализации апострофа) → ў/ғ, ДО разбора одиночных букв
_OG_RE = re.compile(r"([OoGg])'")

_MAP2 = {
    "sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я", "ye": "е", "ts": "ц",
}
_MAP1 = {
    "a": "а", "b": "б", "c": "с", "d": "д", "f": "ф", "g": "г",
    "h": "ҳ", "i": "и", "j": "ж", "k": "к", "l": "л", "m": "м",
    "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с",
    "t": "т", "u": "у", "v": "в", "w": "в", "x": "х", "y": "й", "z": "з",
}
# Класс «кириллическая буква» для правила e→э/е — идентичен translit.js.
_CYR_RE = re.compile("[А-Яа-яЎўҒғҚқҲҳ]")

_OG_MAP = {"o": "ў", "O": "Ў", "g": "ғ", "G": "Ғ"}


def _apply_case(src: str, out: str) -> str:
    """Переносит регистр исходного латинского токена на кириллический вывод."""
    if src == src.lower():
        return out
    if src == src.upper() and len(src) > 1:
        return out.upper()
    return out[0].upper() + out[1:]


def to_cyrillic(text: str) -> str:
    """Лотин-узбекский → кирилл-узбекский. Порт translit.js:toCyrillic."""
    if not text:
        return text
    s = _APOS_RE.sub("'", text)
    s = _OG_RE.sub(lambda m: _OG_MAP[m.group(1)], s)

    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if not (("a" <= ch <= "z") or ("A" <= ch <= "Z")):
            # tutuq belgisi (одиночный апостроф) → ъ; прочее как есть.
            out.append("ъ" if ch == "'" else ch)
            i += 1
            continue

        two = s[i:i + 2]
        two_lower = two.lower()
        if len(two) == 2 and two_lower in _MAP2:
            out.append(_apply_case(two, _MAP2[two_lower]))
            i += 2
            continue

        lower = ch.lower()
        if lower == "e":
            # e в начале слова → э, внутри → е. Смотрим на ПОСЛЕДНИЙ символ
            # ВЫВОДА (как в translit.js), а не входа.
            prev = out[-1][-1] if out else ""
            at_word_start = prev == "" or not _CYR_RE.match(prev)
            cyr = "э" if at_word_start else "е"
        else:
            cyr = _MAP1.get(lower)

        out.append(_apply_case(ch, cyr) if cyr else ch)
        i += 1
    return "".join(out)


# --------------------------------------------------------------------------
# 2. Транслитерация видимого текста HTML (как text-node walker в translit.js)
# --------------------------------------------------------------------------

_SKIP_TAGS = {"code", "pre", "script", "style", "kbd", "samp"}
_VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class _TextSpanFinder(HTMLParser):
    """Находит байтовые диапазоны видимых текстовых узлов вне skip-тегов.

    convert_charrefs=False: сущности (&amp; …) приходят отдельными событиями и
    в handle_data НЕ попадают, поэтому каждый кусок data соответствует исходной
    подстроке 1:1 (можно резать оригинал по offset + len).
    """

    def __init__(self, src: str) -> None:
        super().__init__(convert_charrefs=False)
        self._line_starts = [0]
        for idx, c in enumerate(src):
            if c == "\n":
                self._line_starts.append(idx + 1)
        self.spans: list[tuple[int, int]] = []
        self._stack: list[tuple[str, bool, bool]] = []
        self._skip = 0
        self._fxskip = 0

    def _offset(self) -> int:
        line, col = self.getpos()
        return self._line_starts[line - 1] + col

    def handle_starttag(self, tag, attrs):  # noqa: ANN001
        if tag in _VOID_TAGS:
            return
        is_skip = tag in _SKIP_TAGS
        is_fx = any(
            k == "class" and v and "fx-no-translit" in v.split() for k, v in attrs
        )
        self._stack.append((tag, is_skip, is_fx))
        if is_skip:
            self._skip += 1
        if is_fx:
            self._fxskip += 1

    def handle_startendtag(self, tag, attrs):  # noqa: ANN001
        return  # самозакрывающийся — без вложенности

    def handle_endtag(self, tag):  # noqa: ANN001
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                _, is_skip, is_fx = self._stack.pop(i)
                if is_skip:
                    self._skip -= 1
                if is_fx:
                    self._fxskip -= 1
                return

    def handle_data(self, data):  # noqa: ANN001
        if self._skip == 0 and self._fxskip == 0 and data.strip():
            start = self._offset()
            self.spans.append((start, start + len(data)))


def transliterate_html(src: str) -> str:
    """Возвращает HTML, где кириллизован только видимый текст вне skip-тегов."""
    finder = _TextSpanFinder(src)
    finder.feed(src)
    finder.close()
    if not finder.spans:
        return src
    parts: list[str] = []
    pos = 0
    for start, end in finder.spans:
        if start < pos:  # страховка от перекрытия — пропускаем
            continue
        parts.append(src[pos:start])
        parts.append(to_cyrillic(src[start:end]))
        pos = end
    parts.append(src[pos:])
    return "".join(parts)


# --------------------------------------------------------------------------
# 3. Правка <head> клонированной страницы (lang / canonical / og:url / hreflang / JSON-LD)
# --------------------------------------------------------------------------

def _rewrite_head(html: str) -> str:
    # <html lang="uz"> → uz-Cyrl
    html = re.sub(r'(<html[^>]*\blang=")uz(")', r"\1uz-Cyrl\2", html, count=1)

    # canonical и og:url: /uz/ → /uz-cyrl/
    html = re.sub(
        r'(<link rel="canonical" href=")([^"]*)(")',
        lambda m: m.group(1) + m.group(2).replace("/uz/", "/uz-cyrl/", 1) + m.group(3),
        html, count=1,
    )
    html = re.sub(
        r'(<meta property="og:url" content=")([^"]*)(")',
        lambda m: m.group(1) + m.group(2).replace("/uz/", "/uz-cyrl/", 1) + m.group(3),
        html, count=1,
    )

    # Добавляем hreflang="uz-Cyrl" (рядом с уже существующими ru/en/uz).
    if 'hreflang="uz-Cyrl"' not in html:
        m = re.search(r'<link rel="alternate" href="([^"]*)" hreflang="uz">', html)
        if m:
            cyrl_href = m.group(1).replace("/uz/", "/uz-cyrl/", 1)
            link = f'<link rel="alternate" href="{cyrl_href}" hreflang="uz-Cyrl">'
            html = html.replace("</head>", link + "\n</head>", 1)

    # JSON-LD inLanguage (компактный JSON из structured_data.py).
    html = html.replace('"inLanguage":"uz"', '"inLanguage":"uz-Cyrl"')
    return html


# --------------------------------------------------------------------------
# 4. sitemap: добавляем /uz-cyrl/ записи зеркалом /uz/
# --------------------------------------------------------------------------

def _extend_sitemap(site: Path) -> None:
    sm = site / "sitemap.xml"
    if not sm.exists():
        return
    text = sm.read_text(encoding="utf-8")
    additions = []
    for block in re.findall(r"<url>.*?</url>", text, re.S):
        loc = re.search(r"<loc>([^<]*)</loc>", block)
        if loc and "/uz/" in loc.group(1):
            additions.append(block.replace("/uz/", "/uz-cyrl/"))
    if not additions:
        return
    new_text = text.replace("</urlset>", "".join(additions) + "</urlset>", 1)
    try:
        ET.fromstring(new_text)
    except ET.ParseError:
        return  # не пишем поломанный XML
    sm.write_text(new_text, encoding="utf-8")
    gz = site / "sitemap.xml.gz"
    if gz.exists():
        gz.write_bytes(gzip.compress(new_text.encode("utf-8")))


# --------------------------------------------------------------------------
# 5. Событие MkDocs
# --------------------------------------------------------------------------

def on_post_build(config, **kwargs) -> None:  # noqa: ANN001
    site = Path(config["site_dir"])
    src = site / "uz"
    if not src.exists():
        return
    count = 0
    for page in sorted(src.rglob("*.html")):
        dest = site / "uz-cyrl" / page.relative_to(src)
        try:
            html = page.read_text(encoding="utf-8")
            cloned = _rewrite_head(transliterate_html(html))
        except Exception as exc:  # noqa: BLE001 — одна битая страница не валит билд
            print(f"  ⚠️  translit_cyrl: пропущена {page.name}: {exc}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(cloned, encoding="utf-8")
        count += 1
    _extend_sitemap(site)
    print(f"  ✓ translit_cyrl: сгенерировано {count} кириллических страниц → site/uz-cyrl/")
