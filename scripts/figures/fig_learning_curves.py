"""Chapter 11: learning curves, the floor, and how far a pilot study can see (claims 19, 40, 41).

Panel A: exact expected risk of least squares on the linear-Gaussian task against training
size, for 3, 10 and 30 features (noise sigma = 1, so the Bayes floor is 1); 400 seeds.
Panel B: one 200-example pilot's estimated learning curve (n = 20 to 140), the POW3 fit with
the floor unknown and with the floor known, and the true curve, extrapolated to n = 5,000.
Panel C: for 30 pilots, the estimated training size needed to reach an error 5% above the
floor, with its 90% bootstrap interval, floor unknown and known, against the truth.

This figure makes visible that a learning curve's floor is set by the noise and its approach
by the dimension, and that a small pilot can bound the error far out but cannot pin down how
much data a target near the floor requires, mostly because it cannot see the floor.

Also publishes the chapter's quoted numbers (namespace "ch11") to docs/_variables.yml.

Run: uv run python scripts/figures/fig_learning_curves.py   (about 40 s)
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
    MUTED,
    SEQUENTIAL_BLUE,
    apply_theme,
    save_figure,
)
from publish import fmt, publish  # noqa: E402

from data_lab.curves import (  # noqa: E402
    PILOT_GRID,
    LinearGaussianTask,
    extrapolation_experiment,
    fit_pow3,
    learning_curve,
    pilot_curve,
    pow3,
    size_for_target,
)

warnings.filterwarnings("ignore")
apply_theme()
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.3))

# A
sizes = np.unique(np.logspace(np.log10(40), np.log10(5_000), 12).round()).astype(int)
ax = axes[0]
for d, color in ((3, SEQUENTIAL_BLUE[4]), (10, SEQUENTIAL_BLUE[7]), (30, SEQUENTIAL_BLUE[9])):
    mean, _ = learning_curve(LinearGaussianTask(d=d), sizes)
    ax.semilogx(sizes, mean, color=color, marker="o", ms=3)
    at = {3: 0, 10: 1, 30: 4}[d]
    ax.annotate(f"{d} features", xy=(sizes[at], mean[at]), xytext=(6, 2),
                textcoords="offset points", fontsize=9, color=INK)
ax.axhline(1.0, color=INK, lw=1, ls=(0, (4, 3)))
ax.annotate("Bayes floor $\\sigma_\\varepsilon^2$", xy=(sizes[-1], 1.0), xytext=(-4, -12),
            textcoords="offset points", ha="right", fontsize=9, color=INK_SECONDARY)
ax.set_ylim(0.9, 2.2)
ax.set_xlabel("training examples $n$")
ax.set_ylabel("expected test MSE")
ax.set_title("A. The floor and the approach")

# B
task = LinearGaussianTask(d=10)
rng = np.random.default_rng(100)
z, y = task.sample(200, rng)
points = pilot_curve(z, y, rng)
grid = np.logspace(np.log10(20), np.log10(5_000), 60)
true_mean, _ = learning_curve(task, grid.round().astype(int), seeds=300)
ax = axes[1]
ax.semilogx(grid, true_mean, color=INK, lw=2, label="true curve")
ax.semilogx(PILOT_GRID, points, "o", color=INK_SECONDARY, ms=5, label="pilot estimate")
for floor, style, label in ((None, (0, (5, 2)), "POW3, floor fitted"),
                            (1.0, (0, (1, 1.5)), "POW3, floor known")):
    p = fit_pow3(points, floor=floor)
    ax.semilogx(grid, pow3(grid, *p), color=SEQUENTIAL_BLUE[7], ls=style, label=label)
ax.axvspan(20, 140, color=MUTED, alpha=0.12, lw=0)
ax.annotate("pilot range", xy=(25, 2.1), fontsize=9, color=INK_SECONDARY)
ax.axhline(1.0, color=MUTED, lw=0.8)
ax.set_ylim(0.6, 2.3)
ax.set_xlabel("training examples $n$")
ax.set_ylabel("test MSE")
ax.legend(loc="upper right", fontsize=8.5)
ax.set_title("B. One pilot, extrapolated")

# C
truth_n = size_for_target(task, 1.05)
unknown = extrapolation_experiment(task)
known = extrapolation_experiment(task, known_floor=True)
ax = axes[2]
for offset, res, color, label in ((-0.15, unknown, MUTED,
                                   "floor fitted (top: not reachable)"),
                                  (0.15, known, SEQUENTIAL_BLUE[7], "floor known")):
    s = res["size"]
    k = np.arange(len(s))
    est = np.where(np.isfinite(s[:, 0]), s[:, 0], 2e4)
    hi = np.where(np.isfinite(s[:, 2]), s[:, 2], 2e4)
    ax.vlines(k + offset, np.maximum(s[:, 1], 10), hi, color=color, lw=1.2)
    ax.plot(k + offset, est, "o", ms=3.5, color=color, label=label)
ax.axhline(truth_n, color=INK, lw=1.2)
ax.annotate(f"truth: {truth_n}", xy=(0, truth_n), xytext=(0, 4), textcoords="offset points",
            fontsize=9, color=INK)
ax.set_yscale("log")
ax.set_ylim(10, 3e4)
ax.set_xlabel("pilot study (30 independent pilots)")
ax.set_ylabel("examples needed for error $1.05\\,\\sigma_\\varepsilon^2$")
ax.legend(loc="lower right", fontsize=8.5)
ax.set_title("C. How much data? Mostly the floor")

save_figure(fig, "learning_curves")

truth_2000 = learning_curve(task, [2_000], seeds=2_000)[0][0]
e_u, e_k = unknown["error"], known["error"]
cov_u = np.mean((e_u[:, 1] <= truth_2000) & (truth_2000 <= e_u[:, 2]))
cov_k = np.mean((e_k[:, 1] <= truth_2000) & (truth_2000 <= e_k[:, 2]))
s_u, s_k = unknown["size"], known["size"]
publish("ch11", {
    "truth_2000": fmt(truth_2000, 4),
    "cov_unknown": fmt(100 * cov_u, 0), "cov_known": fmt(100 * cov_k, 0),
    "width_unknown": fmt(np.median(e_u[:, 2] - e_u[:, 1]), 2),
    "width_known": fmt(np.median(e_k[:, 2] - e_k[:, 1]), 2),
    "n_star": fmt(truth_n),
    "inf_share_unknown": fmt(100 * np.mean(~np.isfinite(s_u[:, 0])), 0),
    "median_n_known": fmt(int(round(np.median(s_k[:, 0])))),
    "size_cov_known": fmt(100 * np.mean((s_k[:, 1] <= truth_n) & (truth_n <= s_k[:, 2])), 0),
    "size_ratio_known": fmt(np.median(s_k[:, 2] / s_k[:, 1]), 1),
    "exp_known": fmt(np.median(known["exponent"]), 2),
    "exp_unknown": fmt(np.median(unknown["exponent"]), 2),
})
