"""Claim inventory and seeded sample for the cross-repository assessment (PROTOCOL.md §2.2).

Usage: python assessment/inventory.py <book repo dir> <output .md> [n=30]

Splits the book's .qmd files and generated includes into blocks (paragraphs, list items,
captions, table rows, display equations), classifies each block into one stratum, and draws a
seeded stratified sample. Published-number shortcodes ({{< var ns.key >}}) are replaced by
their values from docs/_variables.yml when it exists.
"""

import json
import random
import re
import sys
import zlib
from pathlib import Path

QUOTA = {"figure": 4, "citation": 8, "equation": 6, "code": 4, "number": 8}
ORDER = ["figure", "citation", "equation", "code", "number"]
LIBS = r"(sklearn|scikit|numpy|np\.|scipy|pandas|torch|quarto|statsmodels|Vectorizer|Scaler|" \
       r"Transformer|Encoder|Regression|Classifier|default)"


def load_vars(root: Path) -> dict:
    p = root / "docs" / "_variables.yml"
    return json.loads(p.read_text()) if p.exists() else {}


def substitute(text: str, variables: dict) -> str:
    def repl(m):
        ns, key = m.group(1).split(".", 1)
        return str(variables.get(ns, {}).get(key, m.group(0)))
    return re.sub(r"\{\{<\s*var\s+([\w.]+)\s*>\}\}", repl, text)


def blocks(text: str):
    """Yield (line number, block text). Display math is one block; table rows and list items
    are their own blocks; paragraphs are runs of non-blank lines."""
    lines = text.splitlines()
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):  # a code block or executable cell: code, not prose
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            continue
        if not s or s.startswith(("#", ":::", "{{< include", "|---", "| |")):
            i += 1
            continue
        if s.startswith("$$"):
            j = i + 1
            while j < n and not lines[j].strip().startswith("$$"):
                j += 1
            yield i + 1, "\n".join(lines[i:j + 1])
            i = j + 1
            continue
        if s.startswith("|") or s.startswith("!["):
            yield i + 1, s
            i += 1
            continue
        start = i
        buf = [line]
        i += 1
        is_item = bool(re.match(r"^\s*([-*]|\d+\.)\s", line))
        while i < n:
            nxt = lines[i]
            ns = nxt.strip()
            if not ns or ns.startswith(("$$", "|", "![", ":::", "#", "```")):
                break
            if re.match(r"^\s*([-*]|\d+\.)\s", nxt) and (is_item or not nxt.startswith(" ")):
                break
            buf.append(nxt)
            i += 1
        yield start + 1, "\n".join(buf)


def is_assertion(s: str) -> bool:
    """Skip blocks that only point to a figure or section, ask a question, or are headings
    of a list ("The failures:")."""
    plain = re.sub(r"\[[^\]]*\]\([^)]*\)|@(fig|sec|tbl)-[\w-]+", "", s).strip(" -*:.")
    if s.rstrip().endswith("?") or s.rstrip().endswith(":"):
        return False
    return len(plain.split()) >= 6


def stratum(b: str) -> str | None:
    s = b.strip()
    if not s.startswith(("![", "$$", "|")) and not is_assertion(s):
        return None
    if s.startswith("!["):
        return "figure"
    if re.search(r"(?<![\w.])@[a-z][a-z0-9]+", s):
        return "citation"
    math = re.findall(r"\$\$.*?\$\$|\$[^$]+\$", s, re.S)
    if s.startswith("$$") or any(re.search(r"=|\\le|\\ge|\\propto|\\approx", m) for m in math):
        return "equation"
    if re.search(r"`[^`]*" + LIBS + r"[^`]*`", s) or re.search(r"`\w+\([^`]*\)`", s):
        return "code"
    plain = re.sub(r"\$[^$]+\$|\[[^\]]*\]\([^)]*\)|`[^`]*`|\{[^}]*\}", "", s)
    if re.search(r"\d", plain):
        return "number"
    return None


def inventory(root: Path):
    variables = load_vars(root)
    files = sorted((root / "docs").glob("**/*.qmd")) + sorted((root / "docs" / "includes").glob(
        "**/*.md"))
    items = []
    for f in files:
        if "_site" in f.parts:
            continue
        text = substitute(f.read_text(), variables)
        for line, b in blocks(text):
            st = stratum(b)
            if st:
                items.append({"file": str(f.relative_to(root)), "line": line, "stratum": st,
                              "text": b})
    return items


def sample(items, n: int, seed: int):
    rng = random.Random(seed)
    by = {s: [it for it in items if it["stratum"] == s] for s in ORDER}
    quota = {s: round(QUOTA[s] * n / 30) for s in ORDER}
    picked = []
    for s in ORDER:
        k = min(quota[s], len(by[s]))
        picked += rng.sample(by[s], k)
        by[s] = [it for it in by[s] if it not in picked]
    while len(picked) < n and any(by.values()):
        s = max(by, key=lambda k: len(by[k]))
        it = rng.choice(by[s])
        picked.append(it)
        by[s].remove(it)
    return picked


def main(repo: str, out: str, n: str = "30") -> None:
    root = Path(repo).resolve()
    items = inventory(root)
    seed = 2026 + zlib.crc32(root.name.encode())
    chosen = sample(items, int(n), seed)
    counts = {s: sum(it["stratum"] == s for it in items) for s in ORDER}
    lines = [f"# Claim sample: {root.name} (protocol v2)", "",
             f"Inventory: {len(items)} checkable blocks {counts}. Seed {seed}. "
             f"Sample: {len(chosen)} items.", ""]
    for k, it in enumerate(chosen, 1):
        lines += [f"## Item {k} ({it['stratum']}): {it['file']}:{it['line']}", "",
                  "```text", it["text"], "```", ""]
    Path(out).write_text("\n".join(lines))
    print(f"{root.name}: {len(items)} blocks {counts}; wrote {len(chosen)} items to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
