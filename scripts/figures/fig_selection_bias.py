"""Chapter 1: what selection does to a regression and to a mean (T1, claim 22).

Panel A: one sample of (z_1, log y) from T1; examples kept by a selection that under-samples
large targets (on y) are colored, dropped ones are gray; the true conditional mean of log y and
the line fitted to the kept examples.
Panels B and C: over 200 seeds, the fitted slope on z_1 and the sample mean of log y, for
random selection (q = p), selection on x, and selection on y.

This figure makes visible that selection on x leaves the regression of y on x intact while
biasing summaries of the inputs and targets, and selection on y biases the regression itself.

Run: uv run python scripts/figures/fig_selection_bias.py   (about 2 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import (  # noqa: E402
    GRIDLINE,
    INK,
    INK_SECONDARY,
    LEVER_COLOR,
    apply_theme,
    save_figure,
)

from data_lab.sampling import keep_on_x, keep_on_y, ols  # noqa: E402
from data_lab.testbeds.t1_tabular import TabularGenerator  # noqa: E402

apply_theme()
gen = TabularGenerator(d=3, rho=0.3, sigma0=0.6)
SEEDS = 200

# Panel A data: one sample, selection on y.
rng = np.random.default_rng(1)
z = gen.sample_z(1_500, rng)
log_y = np.log(gen.sample_y(z, rng))
kept = keep_on_y(log_y, 2.0, rng)

# Panels B and C: repeated samples (same protocol as tests/test_selection.py).
results = {"random": ([], []), "on x": ([], []), "on y": ([], [])}
for s in range(SEEDS):
    rng = np.random.default_rng(22_000 + s)
    zz = gen.sample_z(4_000, rng)
    ly = np.log(gen.sample_y(zz, rng))
    masks = {
        "random": rng.random(len(zz)) < 0.5,
        "on x": keep_on_x(zz, 2.0, rng),
        "on y": keep_on_y(ly, 2.0, rng),
    }
    for name, m in masks.items():
        results[name][0].append(ols(zz[m], ly[m])[1])
        results[name][1].append(ly[m].mean())

fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.0), gridspec_kw={"width_ratios": [1.3, 1, 1]})
ax = axes[0]
ax.scatter(z[~kept, 0], log_y[~kept], s=6, color=GRIDLINE, label="dropped")
ax.scatter(z[kept, 0], log_y[kept], s=6, color=LEVER_COLOR["q"], alpha=0.6, label="kept")
grid = np.linspace(-3, 3, 50)
# E[log y | z_1] marginalizes z_2, z_3 given z_1 under equicorrelation rho:
# E[z_j | z_1] = rho z_1, so the line is a + (b_1 + rho (b_2 + b_3)) z_1.
total = gen.b[0] + gen.rho * (gen.b[1] + gen.b[2])
ax.plot(grid, gen.a + total * grid, color=INK, lw=2, label="truth under $p$")
coef = ols(z[kept, :1], log_y[kept])
ax.plot(grid, coef[0] + coef[1] * grid, color=LEVER_COLOR["q"], lw=2, ls="--",
        label="fit to kept")
ax.set_xlabel("$z_1$")
ax.set_ylabel(r"$\log y$")
ax.set_title("A. Selection on $y$, one sample")
ax.legend(loc="upper left", markerscale=2)

names = ["random", "on x", "on y"]
styles = {"random": (INK_SECONDARY, "o"), "on x": (LEVER_COLOR["q"], "s"),
          "on y": (LEVER_COLOR["q"], "^")}
for k, (ax, truth, title, xlabel) in enumerate([
    (axes[1], gen.b[0], "B. Fitted coefficient", "coefficient on $z_1$"),
    (axes[2], gen.a, r"C. Sample mean of $\log y$", r"mean of $\log y$"),
]):
    for j, name in enumerate(names):
        vals = np.array(results[name][k])
        jitter = np.random.default_rng(j).uniform(-0.15, 0.15, vals.size)
        color, marker = styles[name]
        ax.scatter(vals, j + jitter, s=8, color=color, marker=marker, alpha=0.5)
        ax.plot([np.mean(vals)] * 2, [j - 0.3, j + 0.3], color=INK, lw=1.5)
    ax.axvline(truth, color=INK, lw=1, ls=(0, (4, 3)))
    ax.set_yticks(range(3), [f"selection {n}" if n != "random" else "random ($q = p$)"
                             for n in names])
    ax.set_ylim(-0.6, 2.6)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.grid(axis="y", visible=False)
axes[1].annotate("truth", xy=(gen.b[0], 2.55), xytext=(4, 0), textcoords="offset points",
                 fontsize=9, color=INK_SECONDARY, va="top")
axes[2].annotate("truth", xy=(gen.a, 2.55), xytext=(4, 0), textcoords="offset points",
                 fontsize=9, color=INK_SECONDARY, va="top")
axes[2].set_yticklabels([])

save_figure(fig, "selection_bias")
