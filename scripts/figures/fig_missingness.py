"""Chapter 4: missingness mechanisms against imputation bias (T1, claim 7; SPEC §9).

For column z_1 of T1 (true mean 0, variance 1; 40% missing; z_2 always observed, correlation
0.6), the estimated mean and variance after complete-case analysis, mean imputation and
regression imputation on z_2, under MCAR, MAR (on z_2) and MNAR (on z_1 itself); 200 seeds,
dots are seeds and bars are means.

This figure makes visible that which treatment is biased depends on the mechanism, not on the
treatment alone: mean imputation keeps the MCAR mean but shrinks the variance, regression
imputation repairs the MAR mean, and nothing here repairs MNAR.

Run: uv run python scripts/figures/fig_missingness.py   (about 2 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import INK, INK_SECONDARY, LEVER_COLOR, apply_theme, save_figure  # noqa: E402

from data_lab.cleaning import missingness_experiment  # noqa: E402

apply_theme()
mechanisms = ["MCAR", "MAR", "MNAR"]
treatments = [
    ("cc", "complete case", LEVER_COLOR["q"], "s"),
    ("mean", "mean imputation", LEVER_COLOR["representation"], "o"),
    ("reg", "regression imputation", LEVER_COLOR["representation"], "D"),
]
results = {m: missingness_experiment(m) for m in mechanisms}

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2), sharey=True)
for col, (ax, truth, title, xlabel) in enumerate([
    (axes[0], 0.0, "A. Estimated mean", "estimated mean of $z_1$"),
    (axes[1], 1.0, "B. Estimated variance", "estimated variance of $z_1$"),
]):
    for i, mech in enumerate(mechanisms):
        for j, (key, _, color, marker) in enumerate(treatments):
            y0 = i * 4 + j
            vals = results[mech][key][:, col]
            jitter = np.random.default_rng(i * 10 + j).uniform(-0.25, 0.25, vals.size)
            ax.scatter(vals, y0 + jitter, s=5, color=color, marker=marker, alpha=0.35)
            ax.plot([vals.mean()] * 2, [y0 - 0.38, y0 + 0.38], color=INK, lw=1.5)
    ax.axvline(truth, color=INK, lw=1, ls=(0, (4, 3)))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.grid(axis="y", visible=False)
ticks, labels = [], []
for i, mech in enumerate(mechanisms):
    for j, (_, label, _, _) in enumerate(treatments):
        ticks.append(i * 4 + j)
        labels.append(f"{mech}: {label}")
axes[0].set_yticks(ticks, labels)
axes[0].invert_yaxis()
axes[0].annotate("truth", xy=(0.0, -0.9), xytext=(4, 0), textcoords="offset points",
                 fontsize=9, color=INK_SECONDARY)
axes[1].annotate("truth", xy=(1.0, -0.9), xytext=(4, 0), textcoords="offset points",
                 fontsize=9, color=INK_SECONDARY)

save_figure(fig, "missingness")
