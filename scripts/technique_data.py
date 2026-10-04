"""Single source of truth for the data cards and the decision-guide table (SPEC §2.2, §10).

Each technique is one record. Running this file writes:

- ``docs/includes/cards/<slug>.md``: the data card (a ``callout-tip``), included in the
  chapter right after the technique's definition box;
- ``docs/includes/decision-guide.md``: the table chapter 15 shows, one row per card.

Edit a card here, never in the generated files, then run
``uv run python scripts/technique_data.py``.

The format mirrors ``rl-for-llms/scripts/method_data.py`` (a list of ``dict(...)`` records plus
``FIELDS`` and ``HEADERS``), so the records can later be merged with ``objectives-book``'s
method records (DECISIONS D6).

Fields
------
slug            file-safe id; the card is written to docs/includes/cards/<slug>.md
name            display name
chapter         chapter file stem where the card appears
levers          which of the four levers it pulls: subset of LEVERS. More than one is
                allowed, and the card must then say why (SPEC §2.2, falsifiability).
                Or exactly ["evaluation"] for a technique that acts only on evaluation
status          "draft" = transcribed from SPEC and not yet checked against sources and tests;
                "verified" = every field sourced (research-log.md) and its test passes
sources         bibliography keys (docs/references.bib) the card's claims rest on
changes ... checked_by   the eight card fields of SPEC §2.2, in order
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LEVERS = ("representation", "q", "w", "labels")
# Techniques that act only on evaluation (splits, leakage control, shift detection,
# learning-curve estimation) pull no lever; their cards say so (SPEC §2.2, DECISIONS D7).
EVALUATION = "evaluation"
LEVER_LABEL = {
    "representation": "Representation",
    "q": "Sampling distribution $q$",
    "w": "Weights $w$",
    "labels": "Labels",
    EVALUATION: "Evaluation only",
}

# The card fields, in the order SPEC §2.2 fixes.
FIELDS = [
    "changes",
    "assumption",
    "effect",
    "models",
    "fit_on",
    "failure_modes",
    "alternatives",
    "checked_by",
]
HEADERS = {
    "changes": "Changes",
    "assumption": "Assumption",
    "effect": "What it does to the learned function",
    "models": "Which models care",
    "fit_on": "Fit on",
    "failure_modes": "Failure modes",
    "alternatives": "Alternatives",
    "checked_by": "Checked by",
}

T = [
    # The worked example of SPEC §2.2, transcribed verbatim. Status stays "draft" until
    # chapter 6 is researched (Duan 1983 read; the test passes).
    dict(
        slug="log-target",
        name="Log-transforming a skewed target",
        chapter="06-changing-the-shape",
        levers=["representation"],
        status="draft",
        sources=["duan1983smearing"],
        changes="Representation (of $y$)",
        assumption=r"$y > 0$, with multiplicative noise or right skew",
        effect=r"With MSE, the model learns $\mathbb{E}[\log y \mid x]$: on the original scale, a geometric-mean-like prediction, not the mean",
        models="Linear and GLM-type models, neural nets; trees much less",
        fit_on="None (a fixed function); the smearing correction is fit on training residuals",
        failure_modes="Retransformation bias; zeros and negatives; heavy-tailed residuals after transform",
        alternatives="Box-Cox / Yeo-Johnson; a log-link GLM; a loss matched to the noise",
        checked_by="tests/test_transforms.py::test_log_target_mse_predicts_geometric_mean",
    ),
]

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "docs" / "includes" / "cards"
GUIDE = ROOT / "docs" / "includes" / "decision-guide.md"
CHECKED_BY = re.compile(r"^tests/test_[a-z0-9_]+\.py::test_[a-z0-9_]+$")


def validate(records: list[dict]) -> list[str]:
    """Return a list of problems; empty means the records are well formed."""
    problems = []
    slugs = set()
    required = {"slug", "name", "chapter", "levers", "status", "sources", *FIELDS}
    for r in records:
        tag = r.get("slug", "<no slug>")
        missing = required - set(r)
        if missing:
            problems.append(f"{tag}: missing fields {sorted(missing)}")
            continue
        if r["slug"] in slugs:
            problems.append(f"{tag}: duplicate slug")
        slugs.add(r["slug"])
        levers = r["levers"]
        if levers != [EVALUATION] and (not levers or any(lv not in LEVERS for lv in levers)):
            problems.append(
                f"{tag}: levers must be a non-empty subset of {LEVERS}, or ['{EVALUATION}']"
            )
        if r["status"] not in ("draft", "verified"):
            problems.append(f"{tag}: status must be 'draft' or 'verified'")
        if not CHECKED_BY.match(r["checked_by"]):
            problems.append(f"{tag}: checked_by must look like tests/test_x.py::test_y")
        if not (ROOT / "docs" / "chapters" / f"{r['chapter']}.qmd").exists():
            problems.append(f"{tag}: chapter file {r['chapter']}.qmd does not exist")
    return problems


def cell(text: str) -> str:
    """Escape a table cell. A bare | inside math breaks Markdown tables (playbook pitfall)."""
    return str(text).replace("|", r"\|")


def card(r: dict) -> str:
    draft = " (draft: not yet verified)" if r["status"] == "draft" else ""
    lines = [f'::: {{.callout-tip title="Data card: {r["name"]}{draft}"}}', "| | |", "|---|---|"]
    for f in FIELDS:
        value = f"`{r[f]}`" if f == "checked_by" else r[f]
        lines.append(f"| **{HEADERS[f]}** | {cell(value)} |")
    lines.append(":::")
    return "\n".join(lines) + "\n"


def guide_table(records: list[dict]) -> str:
    cols = ["assumption", "fit_on", "failure_modes"]
    head = "| Technique | Lever | " + " | ".join(HEADERS[c] for c in cols) + " |"
    sep = "|" + "---|" * (len(cols) + 2)
    rows = []
    for r in records:
        # The guide is included from a chapter file, so links are relative to docs/chapters/.
        name = f"[{r['name']}]({r['chapter']}.qmd)"
        lever = ", ".join(LEVER_LABEL[lv] for lv in r["levers"])
        if r["status"] == "draft":
            name += " (draft)"
        rows.append(f"| {name} | {lever} | " + " | ".join(cell(r[c]) for c in cols) + " |")
    return "\n".join([head, sep, *rows]) + "\n"


def main() -> int:
    problems = validate(T)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    CARDS.mkdir(parents=True, exist_ok=True)
    for r in T:
        (CARDS / f"{r['slug']}.md").write_text(card(r))
    GUIDE.write_text(guide_table(T))
    print(f"wrote {len(T)} card(s) and the decision guide")
    return 0


if __name__ == "__main__":
    sys.exit(main())
