"""Unicode-slugify для toc: кириллические заголовки → кириллические якоря.

Раньше в mkdocs.yml стоял `!!python/name:pymdownx.slugs.uslugify`, но из
pymdown-extensions 10+ функцию uslugify выпилили, а `!!python/name` умеет
ссылаться только на установленные модули (локальные файлы проекта не
импортируются на этапе разбора YAML). Поэтому функцию ставит этот хук —
hooks загружаются по пути относительно mkdocs.yml и работают без установки.

`slugify(case="lower")` из pymdownx побайтово совпадает со старым uslugify,
включая двойные дефисы от заголовков вида «3. Реквоты — что это…»
(проверено сравнением вывода на заголовках проекта + check_links).
"""

from pymdownx.slugs import slugify as _slugify_factory


def on_config(config):
    toc = config["mdx_configs"].setdefault("toc", {})
    toc["slugify"] = _slugify_factory(case="lower")
    return config
