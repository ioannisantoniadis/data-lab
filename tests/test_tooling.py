"""Tests of the repository's own machinery: the word count, the portability checks, the
data-card records, the figure theme and the book's structure. These run from Phase 0 on.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "figures"))

import check_portability  # noqa: E402
import technique_data  # noqa: E402
import word_count  # noqa: E402

# --- word count -------------------------------------------------------------------------------


def test_word_count_counts_prose_only():
    text = """---
title: "x"
---
# A title {#sec-a}

One two three $x^2 + y$ four.

$$
a + b = c
$$

```python
not counted at all
```

::: {.callout-tip title="T"}
Five [six](other.qmd#sec-b) seven.
:::

<!-- a comment -->
{{< include ../includes/cards/x.md >}}
![Eight nine.](../images/x.png){#fig-x}
"""
    # A title (2) + One two three four (4) + Five six seven (3) + Eight nine (2)
    assert word_count.count_words(text) == 11


def test_word_count_is_under_the_cap():
    total = sum(word_count.count_words(p.read_text()) for p in word_count.qmd_files())
    assert 0 < total <= word_count.CAP


# --- portability ------------------------------------------------------------------------------


def test_portability_flags_each_rule():
    text = "\n".join(
        [
            "Plain prose.",
            "<div>raw html</div>",
            "As shown in Chapter 3, it works.",
            "```python",
            "x = " + "1" * 90,
            "```",
        ]
    )
    problems = [p for _, p in check_portability.check_text(text)]
    assert any("raw HTML" in p for p in problems)
    assert any("chapter/section number" in p for p in problems)
    assert any("code line" in p for p in problems)
    assert len(problems) == 3


def test_book_passes_portability_checks():
    problems = {
        str(p.relative_to(ROOT)): check_portability.check_text(p.read_text())
        for p in word_count.qmd_files()
    }
    assert not {k: v for k, v in problems.items() if v}


# --- data cards -------------------------------------------------------------------------------


def test_technique_records_are_valid():
    assert technique_data.validate(technique_data.T) == []


def test_validate_rejects_bad_records():
    bad = dict(technique_data.T[0], slug="bad", levers=["vibes"], checked_by="somewhere")
    problems = technique_data.validate([bad])
    assert any("levers" in p for p in problems)
    assert any("checked_by" in p for p in problems)
    mixed = dict(technique_data.T[0], slug="mixed", levers=["evaluation", "q"])
    assert any("levers" in p for p in technique_data.validate([mixed]))
    evaluation_only = dict(technique_data.T[0], slug="split", levers=["evaluation"])
    assert technique_data.validate([evaluation_only]) == []


def _test_functions(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    return {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}


def test_every_checked_by_names_an_existing_test():
    for r in technique_data.T:
        file, name = r["checked_by"].split("::")
        assert (ROOT / file).exists(), r["checked_by"]
        assert name in _test_functions(ROOT / file), r["checked_by"]


def test_generated_cards_are_current():
    """The committed includes match what the records generate (no hand edits)."""
    for r in technique_data.T:
        assert (technique_data.CARDS / f"{r['slug']}.md").read_text() == technique_data.card(r)
    assert technique_data.GUIDE.read_text() == technique_data.guide_table(technique_data.T)


# --- figure theme -----------------------------------------------------------------------------


def test_save_figure_writes_png_at_200_dpi(tmp_path):
    import _theme
    import matplotlib.pyplot as plt

    _theme.apply_theme()
    fig, ax = plt.subplots(figsize=(2, 1))
    ax.plot([0, 1], [0, 1], color=_theme.LEVER_COLOR["q"])
    path = _theme.save_figure(fig, "probe", images_dir=tmp_path)
    assert path.exists() and path.suffix == ".png"
    from matplotlib.image import imread

    height, width = imread(path).shape[:2]
    # 2 x 1 inches at 200 dpi, before tight-bbox trimming: well above 72-dpi size.
    assert width > 2 * 150 and height > 1 * 150


def test_lever_palette_is_the_validated_one():
    import _theme

    assert _theme.LEVERS == technique_data.LEVERS
    # Validated with the dataviz validator on 2026-10-04 (see _theme.py docstring).
    assert list(_theme.LEVER_COLOR.values()) == ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]


# --- book structure ---------------------------------------------------------------------------


def _quarto_paths() -> list[str]:
    text = (ROOT / "docs" / "_quarto.yml").read_text()
    return re.findall(r"^\s*-\s+([\w/.-]+\.qmd)\s*$", text, re.M)


def test_every_page_in_quarto_yml_exists_and_vice_versa():
    listed = set(_quarto_paths())
    assert listed, "no pages found in _quarto.yml"
    for page in listed:
        assert (ROOT / "docs" / page).exists(), page
    on_disk = {str(p.relative_to(ROOT / "docs")) for p in word_count.qmd_files()}
    assert on_disk == listed


@pytest.mark.parametrize("chapter", sorted((ROOT / "docs" / "chapters").glob("*.qmd")))
def test_chapter_has_section_id_and_connections(chapter):
    text = chapter.read_text()
    heading = r"# .+ \{#sec-[a-z0-9-]+( \.unnumbered)?\}\n"
    assert re.match(heading, text), "first line must be: # Title {#sec-id}"
    assert "\n## Connections\n" in text


def test_coverage_lists_every_chapter_item():
    coverage = (ROOT / "COVERAGE.md").read_text()
    rows = re.findall(r"^\| \[[ x]\] \|", coverage, re.M)
    # SPEC §6: 9 + 18 + 10 + 18 + 2 items.
    assert len(rows) == 57
