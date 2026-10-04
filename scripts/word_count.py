"""Count the book's prose words and enforce the size cap (SPEC §1, §13).

Prose is what a reader reads as running text in ``docs/**/*.qmd``. The script removes:

- YAML front matter;
- fenced code blocks (lines between ``` fences);
- display math ($$ … $$) and inline math ($ … $);
- HTML comments;
- Quarto shortcodes ({{< … >}}) and attribute blocks ({#fig-x}, {.callout-tip …});
- callout fences (:::);
- link and image targets, keeping the link text and figure captions.

Generated includes (``docs/includes/**/*.md``: data cards, the decision-guide table) are not
``.qmd`` files and are not counted. They are tables, not prose.

A word is a run of letters or digits (with internal apostrophes or hyphens). Usage:

    uv run python scripts/word_count.py            # report; exit 1 if over the cap
    uv run python scripts/word_count.py --quiet    # total only

The report also prints the raw whitespace-separated count (``wc -w``), because SPEC §1's
sibling sizes were measured that way; which count the cap applies to is an open owner question
(ROADMAP.md). The cap is enforced on prose, as SPEC §1 words it.

Exit status 1 when the total exceeds CAP. Chapters outside the per-chapter range are reported
as warnings only: stubs are short by design, and SPEC §5 allows merging and splitting.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CAP = 35_000
TARGET = (22_000, 30_000)
CHAPTER_RANGE = (1_200, 2_200)

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SKIP_DIRS = {"_site", "_book", ".quarto", "_freeze"}

_FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
_FENCE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.S | re.M)
_DISPLAY_MATH = re.compile(r"\$\$.*?\$\$", re.S)
_INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\s)[^$\n]+?(?<!\s)\$")
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_SHORTCODE = re.compile(r"\{\{<.*?>\}\}", re.S)
_ATTRS = re.compile(r"\{[#.][^}]*\}")
_CALLOUT = re.compile(r"^:::.*$", re.M)
_LINK_TARGET = re.compile(r"\]\([^)]*\)")
_WORD = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")


def prose(text: str) -> str:
    """Strip everything that is not prose, in an order that keeps fences from leaking."""
    for pattern, repl in [
        (_FRONT_MATTER, ""),
        (_FENCE, ""),
        (_COMMENT, ""),
        (_SHORTCODE, ""),
        (_DISPLAY_MATH, ""),
        (_INLINE_MATH, ""),
        (_ATTRS, ""),
        (_CALLOUT, ""),
        (_LINK_TARGET, "]"),
    ]:
        text = pattern.sub(repl, text)
    return text


def count_words(text: str) -> int:
    return len(_WORD.findall(prose(text)))


def qmd_files(docs: Path = DOCS) -> list[Path]:
    return sorted(
        p for p in docs.rglob("*.qmd") if not SKIP_DIRS.intersection(p.relative_to(docs).parts)
    )


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    counts = {p.relative_to(ROOT): count_words(p.read_text()) for p in qmd_files()}
    total = sum(counts.values())
    if not quiet:
        lo, hi = CHAPTER_RANGE
        for path, n in counts.items():
            flag = ""
            if path.parts[1] == "chapters" and not lo <= n <= hi:
                flag = f"  (outside {lo:,}-{hi:,}; warning only)"
            print(f"{n:>7,}  {path}{flag}")
        print(f"{total:>7,}  TOTAL prose (target {TARGET[0]:,}-{TARGET[1]:,}; cap {CAP:,})")
        raw = sum(len(p.read_text().split()) for p in qmd_files())
        print(f"{raw:>7,}  raw wc -w, for comparison with SPEC §1's sibling sizes")
    else:
        print(total)
    if total > CAP:
        print(f"FAIL: {total:,} words exceeds the cap of {CAP:,}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
