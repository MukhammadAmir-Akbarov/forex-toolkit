"""Inject repository-backed counters into the three home pages."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = {
    "{{PROJECT_PAGES}}": "pages",
    "{{PROJECT_TOOLS}}": "tools",
    "{{PROJECT_STRATEGIES}}": "strategies",
    "{{PROJECT_TESTS}}": "tests",
}


def _literal_assignments(tree: ast.AST) -> dict[str, object]:
    values: dict[str, object] = {}
    for node in getattr(tree, "body", []):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                values[target.id] = value
    return values


def _parameter_count(decorator: ast.expr, values: dict[str, object]) -> int:
    if not isinstance(decorator, ast.Call) or len(decorator.args) < 2:
        return 1
    if not ast.unparse(decorator.func).endswith("parametrize"):
        return 1
    argument = decorator.args[1]
    try:
        cases = ast.literal_eval(argument)
    except (ValueError, TypeError):
        cases = values.get(argument.id, []) if isinstance(argument, ast.Name) else []
    return max(1, len(cases)) if isinstance(cases, (list, tuple)) else 1


def count_tests(folder: Path) -> int:
    count = 0
    for path in folder.glob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        values = _literal_assignments(tree)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or not node.name.startswith("test_"):
                continue
            cases = 1
            for decorator in node.decorator_list:
                cases *= _parameter_count(decorator, values)
            count += cases
    return count


def project_stats() -> dict[str, int]:
    docs = ROOT / "_mkdocs"
    pages = sum(
        1
        for path in docs.rglob("*.md")
        if not path.name.endswith((".en.md", ".uz.md")) and "includes" not in path.parts
    )
    tools = len(list((ROOT / "tools").glob("*.py")))
    strategies = sum(
        1
        for path in (ROOT / "strategies").glob("*.py")
        if "def detect(" in path.read_text(encoding="utf-8")
    ) + int((ROOT / "strategies" / "carry_trade.md").exists())
    tests = count_tests(ROOT / "tests") + count_tests(ROOT / "tests_e2e")
    return {"pages": pages, "tools": tools, "strategies": strategies, "tests": tests}


def on_page_markdown(markdown: str, *, page, config, files) -> str:  # noqa: ARG001
    if not any(token in markdown for token in TOKENS):
        return markdown
    stats = project_stats()
    for token, name in TOKENS.items():
        markdown = markdown.replace(token, str(stats[name]))
    return markdown
