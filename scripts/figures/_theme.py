"""Shared matplotlib styling for every figure script in this directory.

Every ``fig_*.py`` script calls ``apply_theme()`` and ends with ``save_figure(fig, "<slug>")``,
which writes ``docs/images/<slug>.png`` at 200 dpi. Quarto does not execute Python at render
time; the PNGs are pre-generated and committed (SPEC §9, §16).

Palette: the same fixed categorical order, sequential ramp, ink and surface tokens as
``rl-for-llms/scripts/figures/_theme.py`` (read 2026-10-04), so the sibling books read as one
system.

Book-specific addition: ``LEVER_COLOR``. Color is semantic. It encodes which of the four data
levers a technique pulls (SPEC §2.1): representation, sampling distribution q, weights w, or
labels. The four lever colors were run through the dataviz palette validator on 2026-10-04
(``validate_palette.js "#2a78d6,#eb6834,#1baf7a,#4a3aa7" --mode light --surface "#fcfcfb"
--pairs all``). Lightness, chroma, CVD separation (worst all-pairs ΔE 9.2, deutan) and the
normal-vision floor (worst ΔE 16.3) all PASS. Contrast against the surface is a WARN for aqua
(2.74:1). Every multi-series figure therefore carries a legend *and* direct labels or distinct
line styles, so that identity is never carried by color alone. Magenta was rejected for the
labels lever: it fails the normal-vision floor against orange (ΔE 12.9).

Elsewhere (no lever involved), assign ``CATEGORICAL`` in its fixed order; never let matplotlib
cycle colors. Exact ground-truth curves are drawn in ``INK``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Fixed categorical order, copied from rl-for-llms: index into it, never auto-cycle.
CATEGORICAL = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

SEQUENTIAL_BLUE = [
    "#eaf2fc", "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef",
    "#6da7ec", "#5598e7", "#3987e5", "#1f6dc9", "#0d366b",
]

INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRIDLINE = "#e1e0d9"
SURFACE = "#fcfcfb"

# The four levers (SPEC §2.1) -> fixed color, used in every figure and in the Map.
LEVER_COLOR = {
    "representation": CATEGORICAL[0],  # blue
    "q": CATEGORICAL[1],  # orange: the sampling distribution
    "w": CATEGORICAL[2],  # aqua: per-example weights
    "labels": CATEGORICAL[6],  # violet
}
LEVERS = tuple(LEVER_COLOR)

# Evaluation-only techniques pull no lever (DECISIONS D7): drawn in a neutral, never a hue.
EVALUATION_COLOR = INK_SECONDARY

# Exact computations (the truth a method is measured against).
REFERENCE_COLOR = INK

FIGURE_DPI = 200
REPO_ROOT = Path(__file__).resolve().parents[2]
IMAGES = REPO_ROOT / "docs" / "images"


def apply_theme() -> None:
    """Call once at the top of every fig_*.py, before creating any figure."""
    plt.rcParams.update(
        {
            "figure.dpi": FIGURE_DPI,
            "savefig.dpi": FIGURE_DPI,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "axes.edgecolor": GRIDLINE,
            "axes.labelcolor": INK_SECONDARY,
            "axes.titlecolor": INK,
            "axes.grid": True,
            "grid.color": GRIDLINE,
            "grid.linewidth": 0.8,
            "text.color": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "font.family": "sans-serif",
            "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans", "sans-serif"],
            "font.size": 11,
            "axes.titlesize": 12.5,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.prop_cycle": plt.cycler(color=[INK_SECONDARY]),  # force explicit colors
            "legend.frameon": False,
            "legend.fontsize": 9.5,
            "lines.linewidth": 2.0,
            "mathtext.fontset": "cm",
        }
    )


def save_figure(fig, slug: str, images_dir: Path | None = None) -> Path:
    """Save ``docs/images/<slug>.png`` at FIGURE_DPI with the shared padding convention.

    The single place figures are written (objectives-book SPEC §21.1, rule 6), so adding vector
    output later is a change here only. ``images_dir`` exists for tests.
    """
    out_dir = IMAGES if images_dir is None else Path(images_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{slug}.png"
    if fig.get_layout_engine() is None:
        fig.tight_layout()
    fig.savefig(path, dpi=FIGURE_DPI, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    try:
        shown = path.relative_to(REPO_ROOT)
    except ValueError:
        shown = path
    print(f"wrote {shown}")
    return path
