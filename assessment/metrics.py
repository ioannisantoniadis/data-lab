"""Metrics for the cross-repository assessment (PROTOCOL.md §4).

Usage: python assessment/metrics.py <verdicts.json>

verdicts.json: {"<repo>": {"A": [verdict, ...], "B": [verdict, ...],
                           "planted_items": [item numbers], "found": {"A": k, "B": k},
                           "planted": n}}
with one verdict per sampled item, in item order: correct, imprecise, wrong, unsupported,
unverifiable or n/a. Planted items are excluded from the defect rate.
"""

import json
import math
import sys

DEFECT = {"wrong", "unsupported"}
EXCLUDE = {"unverifiable", "n/a"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def kappa(a: list[bool], b: list[bool]) -> float:
    n = len(a)
    if n == 0:
        return math.nan
    po = sum(x == y for x, y in zip(a, b, strict=True)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return math.nan if pe == 1 else (po - pe) / (1 - pe)


def rate(verdicts, skip, defects=DEFECT):
    kept = [v for i, v in enumerate(verdicts, 1) if i not in skip and v not in EXCLUDE]
    k = sum(v in defects for v in kept)
    return k, len(kept)


def main(path: str) -> None:
    data = json.load(open(path))
    for repo, d in data.items():
        skip = set(d.get("planted_items", []))
        print(f"## {repo}")
        for who in ("A", "B"):
            k, n = rate(d[who], skip)
            ki, _ = rate(d[who], skip, DEFECT | {"imprecise"})
            lo, hi = wilson(k, n)
            print(f"  auditor {who}: defects {k}/{n} = {k / n:.0%} [{lo:.0%}, {hi:.0%}];"
                  f" with imprecise {ki}/{n}; planted found {d['found'][who]}/{d['planted']}")
        pooled = ["wrong" if (a in DEFECT or b in DEFECT) else
                  ("n/a" if a in EXCLUDE and b in EXCLUDE else "correct")
                  for a, b in zip(d["A"], d["B"], strict=True)]
        k, n = rate(pooled, skip)
        lo, hi = wilson(k, n)
        print(f"  pooled: {k}/{n} = {k / n:.0%} [{lo:.0%}, {hi:.0%}]")
        shared = [(a in DEFECT, b in DEFECT) for i, (a, b) in enumerate(zip(d["A"], d["B"],
                  strict=True), 1) if i not in skip and a not in EXCLUDE and b not in EXCLUDE]
        print(f"  kappa (defect vs not, {len(shared)} shared items): "
              f"{kappa([x for x, _ in shared], [y for _, y in shared]):.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
