"""Publish measured numbers for the prose to quote (DECISIONS D9).

An experiment script computes its numbers and calls ``publish("ch8", {"key": value, ...})``.
The values are formatted once, here or by the caller, and written into ``docs/_variables.yml``
under the namespace; chapters quote them with Quarto's shortcode ``{{< var ch8.key >}}``.
A missing key is a Quarto WARNING, which fails the docs build, so prose cannot quote a number
no script produced. Re-running the script refreshes every quoted number at once.

``docs/_variables.yml`` is written as JSON (valid YAML), sorted, so it needs no YAML library and
diffs cleanly. Never edit it by hand.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIABLES = ROOT / "docs" / "_variables.yml"


def fmt(value, digits: int = 3) -> str:
    """Format a number for prose: thousands separators for integers, fixed decimals otherwise."""
    whole = isinstance(value, float) and value.is_integer() and abs(value) >= 1000
    if isinstance(value, int) or whole:
        return f"{int(value):,}"
    return f"{value:.{digits}f}"


def publish(namespace: str, values: dict[str, str], path: Path = VARIABLES) -> None:
    """Replace ``namespace`` in the variables file with ``values`` (strings, already formatted)."""
    if not all(isinstance(v, str) for v in values.values()):
        raise TypeError("format values as strings before publishing (see fmt)")
    data = json.loads(path.read_text()) if path.exists() else {}
    data[namespace] = dict(sorted(values.items()))
    path.write_text(json.dumps(dict(sorted(data.items())), indent=2, ensure_ascii=False) + "\n")
    print(f"published {len(values)} number(s) under '{namespace}' to {path.name}")
