"""Make a blinded copy of a learning-repo book for auditing (PROTOCOL.md §2.1).

Usage: python assessment/blind_copy.py <repo dir> <destination dir>
"""

import re
import shutil
import sys
from pathlib import Path

PROCESS_FILES = ["SPEC.md", "DECISIONS.md", "ROADMAP.md", "CLAUDE.md", "CONVENTIONS.md",
                 "COVERAGE.md", "research-log.md", "review.md"]
PROCESS_DIRS = ["audits", "assessment"]
IGNORE = shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache",
                                "_site", "_book", ".quarto", ".DS_Store")


def files_read_by_tests(src: Path) -> set[str]:
    """Process files the repository's own tests open: kept, so the tests still run."""
    text = " ".join(p.read_text(errors="ignore") for p in (src / "tests").glob("**/*.py"))
    return {name for name in PROCESS_FILES if name in text}


def neutral_readme(src: Path) -> str:
    title = "Book"
    readme = src / "README.md"
    if readme.exists():
        for line in readme.read_text().splitlines():
            m = re.match(r"\*(.+?)\*", line.strip())
            if line.startswith("# "):
                title = line[2:].strip()
            elif m:
                title = f"{title}: {m.group(1)}"
                break
    blocks = re.findall(r"```[a-z]*\n.*?```", readme.read_text(), re.S) if readme.exists() else []
    commands = "\n\n".join(blocks) or "```bash\nuv sync\nuv run pytest\nquarto render docs\n```"
    return f"# {title}\n\nA Quarto book with code. Build commands, as documented:\n\n{commands}\n"


def main(src: str, dst: str) -> None:
    src_p, dst_p = Path(src).resolve(), Path(dst).resolve()
    if dst_p.exists():
        raise SystemExit(f"{dst_p} exists; remove it first")
    shutil.copytree(src_p, dst_p, ignore=IGNORE)
    keep = files_read_by_tests(src_p)
    for name in PROCESS_FILES:
        if name not in keep:
            (dst_p / name).unlink(missing_ok=True)
    for name in PROCESS_DIRS:
        shutil.rmtree(dst_p / name, ignore_errors=True)
    (dst_p / "README.md").write_text(neutral_readme(src_p))
    print(f"blinded copy of {src_p.name} at {dst_p}" + (f" (kept for tests: {sorted(keep)})"
                                                          if keep else ""))


if __name__ == "__main__":
    main(*sys.argv[1:3])
