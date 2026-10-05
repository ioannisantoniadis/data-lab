"""Chapter 12: a data-scaling curve with a known floor, and what fitted forms do with it (T4;
claim 42).

Panel A: exact expected cross-entropy of an add-k bigram model on T4 against training tokens
(10 seeds), the source's exact entropy rate (the irreducible loss), and two forms fitted on
D <= 10^4 tokens and extrapolated: a pure power law (Kaplan et al. 2020, eq. 1.2) and a power
law plus an irreducible term (Hoffmann et al. 2022, eq. 2, data term only).
Panel B: the local log-log slope of the excess loss over the entropy rate.

This figure makes visible that a scaling curve is a power law only within a regime, that a
form without an irreducible term extrapolates below what any model can reach, and that an
exponent fitted early need not hold later.

Also publishes the chapter's quoted numbers (namespace "ch12") to docs/_variables.yml.

Run: uv run python scripts/figures/fig_scaling_laws.py   (about 3 s)
"""

import sys
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _theme import (  # noqa: E402
    INK,
    INK_SECONDARY,
    LEVER_COLOR,
    MUTED,
    apply_theme,
    save_figure,
)
from publish import fmt, publish  # noqa: E402

from data_lab.scaling import (  # noqa: E402
    SOURCE,
    data_scaling_curve,
    fit_forms,
    power_law,
    power_law_with_floor,
)

warnings.filterwarnings("ignore")
apply_theme()
sizes = np.unique(np.logspace(2, 6, 17).astype(int))
losses = data_scaling_curve(sizes)
h = SOURCE.entropy_rate
window = sizes <= 1e4
pure, floor = fit_forms(sizes[window], losses[window])
grid = np.logspace(2, 6, 200)

fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.5, 4.3),
                                 gridspec_kw={"width_ratios": [1.3, 1]})
ax_a.semilogx(sizes, losses, "o", color=INK, ms=5, label="bigram model (exact, 10 seeds)")
ax_a.semilogx(grid, power_law(grid, *pure), color=LEVER_COLOR["representation"],
              ls=(0, (5, 2)), label=r"fit $A D^{-\alpha}$ (no floor)")
ax_a.semilogx(grid, power_law_with_floor(grid, *floor), color=LEVER_COLOR["representation"],
              ls=(0, (1, 1.5)), label=r"fit $E + A D^{-\alpha}$")
ax_a.axhline(h, color=INK, lw=1)
ax_a.annotate("entropy rate (irreducible)", xy=(1e6, h), xytext=(-4, -12),
              textcoords="offset points", ha="right", fontsize=9, color=INK_SECONDARY)
ax_a.axvspan(100, 1e4, color=MUTED, alpha=0.12, lw=0)
ax_a.annotate("fitted on", xy=(130, 2.92), fontsize=9, color=INK_SECONDARY)
ax_a.set_ylim(2.15, 2.95)
ax_a.set_xlabel("training tokens $D$")
ax_a.set_ylabel("cross-entropy (nats per token)")
ax_a.legend(loc="upper right", fontsize=8.5)
ax_a.set_title("A. Extrapolating a scaling curve")

excess = losses - h
slopes = np.diff(np.log(excess)) / np.diff(np.log(sizes))
mids = np.sqrt(sizes[1:] * sizes[:-1])
ax_b.semilogx(mids, slopes, color=INK, marker="o", ms=4)
ax_b.axhline(-1, color=MUTED, lw=0.8, ls=(0, (4, 3)))
ax_b.annotate("slope $-1$ (variance-limited)", xy=(1e2, -1), xytext=(2, -12),
              textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax_b.set_ylim(-1.5, 0.1)
ax_b.set_xlabel("training tokens $D$")
ax_b.set_ylabel("local slope of excess loss (log-log)")
ax_b.set_title("B. One curve, several exponents")

save_figure(fig, "scaling_laws")

publish("ch12", {
    "entropy_rate": fmt(h, 3),
    "loss_1e6": fmt(losses[-1], 3),
    "pure_alpha": fmt(pure[1], 3),
    "pure_pred_1e6": fmt(power_law(1e6, *pure), 3),
    "floor_E": fmt(floor[0], 3),
    "floor_alpha": fmt(floor[2], 2),
    "floor_pred_1e6": fmt(power_law_with_floor(1e6, *floor), 3),
    "late_slope": fmt(float(np.mean(slopes[-4:])), 2),
    "early_slope_min": fmt(float(np.min(slopes[mids <= 10**3.5])), 2),
    "early_slope_max": fmt(float(np.max(slopes[mids <= 10**3.5])), 2),
})
