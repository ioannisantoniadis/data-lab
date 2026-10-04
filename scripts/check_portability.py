"""Check the portability rules this book inherits from objectives-book SPEC §21.1 (DECISIONS D6).

Checks every ``docs/**/*.qmd``:

1. no raw HTML tags or ``<style>`` outside fenced code (rule 1);
2. fenced code lines are at most 80 characters (rule 5);
3. no emoji or pictographic symbols in book text (rule 7);
4. no hand-typed "Chapter N" / "Section N" in prose; link by title instead (SPEC §11).

Exit status 1 if any check fails. Usage: ``uv run python scripts/check_portability.py``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from word_count import DOCS, ROOT, qmd_files  # noqa: E402

MAX_CODE_WIDTH = 80
_FENCE_OPEN = re.compile(r"^(```|~~~)")
_HTML = re.compile(r"</?(?:div|span|style|script|br|p|img|table|iframe|font|center)\b", re.I)
_EMOJI = re.compile("[\U0001f300-\U0001faff☀-➿⭐⬆⤴⤵]")
_CHAPTER_NUMBER = re.compile(r"\b(?:Chapter|Section|Ch\.)\s+\d+", re.I)


def check_text(text: str) -> list[tuple[int, str]]:
    """Return (line number, problem) pairs for one file's text."""
    problems = []
    in_code = False
    for i, line in enumerate(text.splitlines(), start=1):
        if _FENCE_OPEN.match(line.strip()):
            in_code = not in_code
            continue
        if in_code:
            if len(line) > MAX_CODE_WIDTH:
                problems.append((i, f"code line is {len(line)} > {MAX_CODE_WIDTH} characters"))
            continue
        if _HTML.search(line):
            problems.append((i, "raw HTML in book text"))
        if _EMOJI.search(line):
            problems.append((i, "emoji or pictographic symbol"))
        if _CHAPTER_NUMBER.search(line):
            problems.append((i, "hand-typed chapter/section number; link by title"))
    return problems


def main() -> int:
    failed = 0
    for path in qmd_files(DOCS):
        for line_no, problem in check_text(path.read_text()):
            print(f"{path.relative_to(ROOT)}:{line_no}: {problem}")
            failed += 1
    if failed:
        print(f"FAIL: {failed} portability problem(s)", file=sys.stderr)
        return 1
    print("portability checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
