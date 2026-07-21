"""Discover test cases from a solution file's own `run_test(...)` calls.

Every solution in this repo follows the same convention: a `run_test(name,
<solving args...>, expected)` helper, called once per example under
`if __name__ == "__main__":`. This module reads that structure statically
(via `ast`, no code execution) so `tracer.checker` can run a solution's own
examples without the caller re-typing them on the command line.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any


@dataclass
class DiscoveredCase:
    label: str
    args: list[Any]
    expected: Any
    expected_is_partial: bool  # True when >1 leftover param, so `expected` is a dict and unverifiable


def _literal(node: ast.AST) -> tuple[bool, Any]:
    try:
        return True, ast.literal_eval(node)
    except (ValueError, SyntaxError):
        return False, None


def _find_harness_def(tree: ast.Module, harness_name: str) -> ast.FunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == harness_name:
            return node
    return None


def _find_solving_param_order(
    harness_def: ast.FunctionDef, method_name: str, param_names: list[str]
) -> list[str] | None:
    """Find the one `<obj>.<method_name>(...)` call inside the harness whose
    args are all references to the harness's own parameters, and return
    those parameter names in call order. None if zero or more-than-one such
    call is found (too ambiguous to trust)."""
    param_set = set(param_names)
    matches: list[list[str]] = []

    for node in ast.walk(harness_def):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == method_name):
            continue
        names: list[str] = []
        for a in node.args:
            if isinstance(a, ast.Name) and a.id in param_set:
                names.append(a.id)
            else:
                names = []
                break
        if names:
            matches.append(names)

    if len(matches) == 1:
        return matches[0]
    return None


def discover_test_cases(source: str, method_name: str, harness_name: str = "run_test") -> list[DiscoveredCase]:
    """Statically extract (label, args, expected) from `harness_name(...)` calls.

    Returns an empty list if the harness isn't found, if the solving call
    inside it can't be matched unambiguously, or if any call site uses
    non-literal arguments (e.g. passing a function object) — callers should
    fall back to asking for explicit arguments in that case.
    """
    tree = ast.parse(source)
    harness_def = _find_harness_def(tree, harness_name)
    if harness_def is None:
        return []

    param_names = [a.arg for a in harness_def.args.args]
    if not param_names:
        return []
    label_param = param_names[0]

    solving_params = _find_solving_param_order(harness_def, method_name, param_names)
    if not solving_params:
        return []

    expected_params = [p for p in param_names if p != label_param and p not in solving_params]

    cases: list[DiscoveredCase] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == harness_name):
            continue

        values: dict[str, Any] = {}
        ok = True

        for i, arg_node in enumerate(node.args):
            if i >= len(param_names):
                ok = False
                break
            parsed_ok, value = _literal(arg_node)
            if not parsed_ok:
                ok = False
                break
            values[param_names[i]] = value

        for kw in node.keywords:
            if kw.arg is None or kw.arg not in param_names:
                ok = False
                break
            parsed_ok, value = _literal(kw.value)
            if not parsed_ok:
                ok = False
                break
            values[kw.arg] = value

        if not ok or len(values) != len(param_names):
            continue

        label = str(values.get(label_param, f"case {len(cases) + 1}"))
        method_args = [values[p] for p in solving_params]

        if len(expected_params) == 1:
            expected: Any = values[expected_params[0]]
            partial = False
        elif expected_params:
            expected = {p: values[p] for p in expected_params}
            partial = True
        else:
            expected = None
            partial = True

        cases.append(DiscoveredCase(label=label, args=method_args, expected=expected, expected_is_partial=partial))

    return cases
