"""Chapter 10: what each kind of shift lets you detect (T1; claim 39).

Panel A: rejection rate at level 0.05 of two tests that see only inputs (a classifier
two-sample test and Bonferroni-corrected per-feature Kolmogorov-Smirnov tests), 500 examples
per sample, as the mean of z_1 moves under p (200 seeds).
Panel B: rejection rates for no shift, prior shift and concept shift, for the two input tests
and for a labeled check (the deployed model's accuracy on 500 labeled new examples).

This figure makes visible that shift in the inputs is detectable from inputs, with power that
grows with its size, while concept shift leaves the inputs untouched and is visible only
through labels.

Also publishes the chapter's quoted numbers (namespace "ch10") to docs/_variables.yml.

Run: uv run python scripts/figures/fig_distribution_shift.py   (about 10 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _theme import (  # noqa: E402
    EVALUATION_COLOR,
    INK,
    INK_SECONDARY,
    MUTED,
    apply_theme,
    save_figure,
)
from publish import fmt, publish  # noqa: E402

from data_lab.shift import shift_detection_experiment  # noqa: E402

apply_theme()
shifts = (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4)  # the experiment's default grid
rates = shift_detection_experiment()  # default grid; the same run the test checks
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.5, 4.3),
                                 gridspec_kw={"width_ratios": [1.2, 1]})

xs = [0.0, *shifts]
for test, label, style, marker in ((0, "classifier two-sample test", "-", "o"),
                                   (1, "per-feature KS tests", (0, (4, 2)), "s")):
    ys = [rates["none"][test]] + [rates[f"covariate {s}"][test] for s in shifts]
    ax_a.plot(xs, ys, color=EVALUATION_COLOR, ls=style, marker=marker, ms=4, label=label)
ax_a.legend(loc="lower right")
ax_a.axhline(0.05, color=MUTED, lw=0.8)
ax_a.annotate("level 0.05", xy=(0.0, 0.05), xytext=(2, 4), textcoords="offset points",
              fontsize=9, color=INK_SECONDARY)
ax_a.set_xlabel("covariate shift: change in the mean of $z_1$ (standard deviations)")
ax_a.set_ylabel("rejection rate (500 vs. 500 examples)")
ax_a.set_ylim(0, 1.05)
ax_a.set_title("A. Covariate shift: detectable from inputs")

scen = ["none", "prior", "concept"]
width = 0.25
for k, (label, color) in enumerate((("classifier two-sample", EVALUATION_COLOR),
                                    ("KS tests", MUTED),
                                    ("labeled accuracy check", INK))):
    vals = [rates[s][k] for s in scen]
    if k == 2:
        vals = [rates["none"][2], np.nan, rates["concept"][2]]
    ax_b.bar(np.arange(3) + (k - 1) * width, vals, width=width * 0.9, color=color, label=label)
ax_b.axhline(0.05, color=MUTED, lw=0.8)
ax_b.set_xticks(range(3), ["no shift", "prior shift", "concept shift"])
ax_b.set_ylim(0, 1.05)
ax_b.set_ylabel("rejection rate")
ax_b.legend(loc="upper left", fontsize=8.5)
ax_b.set_title("B. Concept shift: only labels show it")
ax_b.grid(axis="x", visible=False)

save_figure(fig, "distribution_shift")

publish("ch10", {
    "none_c2st": fmt(rates["none"][0], 3), "none_ks": fmt(rates["none"][1], 3),
    "cov01_c2st": fmt(rates["covariate 0.1"][0], 2),
    "cov03_c2st": fmt(rates["covariate 0.3"][0], 2),
    "cov03_ks": fmt(rates["covariate 0.3"][1], 2),
    "cov04_c2st": fmt(rates["covariate 0.4"][0], 2),
    "prior_c2st": fmt(rates["prior"][0], 2), "prior_ks": fmt(rates["prior"][1], 2),
    "concept_c2st": fmt(rates["concept"][0], 3), "concept_ks": fmt(rates["concept"][1], 3),
    "concept_labeled": fmt(rates["concept"][2], 2), "none_labeled": fmt(rates["none"][2], 3),
})
