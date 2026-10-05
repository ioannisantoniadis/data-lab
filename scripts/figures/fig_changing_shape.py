"""Chapter 6: affine versus nonlinear transforms of one skewed feature, and what MSE averages
(T1; SPEC §9; claims 1, 4 and 31).

Top row: one log-normal feature (5,000 draws) raw, standardized, log-transformed, and quantile-
transformed to a normal; skewness in each title.
Bottom left: for a log-normal target along z_1 (other features at 0, sigma_eps = 0.8), the true
conditional mean, the true median (= geometric mean), and two predictions from least squares on
log y: back-transformed with exp, and smeared.
Bottom right: smeared prediction divided by the true conditional mean, by z_1, with constant
noise and with noise growing with z_1 (median and 10-90% band over 10 seeds).

This figure makes visible that an affine scaler leaves a skewed feature's shape untouched while
a nonlinear transform changes it, that least squares on log y aims at the median, not the mean,
and that the smearing correction works only when the noise does not depend on the inputs.

Run: uv run python scripts/figures/fig_changing_shape.py   (about 3 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.preprocessing import QuantileTransformer, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import INK, INK_SECONDARY, LEVER_COLOR, MUTED, apply_theme, save_figure  # noqa: E402

from data_lab.sampling import ols  # noqa: E402
from data_lab.testbeds.t1_tabular import TabularGenerator  # noqa: E402
from data_lab.transforms import smearing_predict  # noqa: E402

apply_theme()
fig = plt.figure(figsize=(13, 7.2), layout="constrained")
grid = fig.add_gridspec(2, 4, height_ratios=[1, 1.35])

# Top row
rng = np.random.default_rng(1)
x = np.exp(rng.standard_normal(5_000))
versions = [
    ("raw", x, MUTED),
    ("standardized (affine)", StandardScaler().fit_transform(x[:, None])[:, 0], MUTED),
    ("log", np.log(x), LEVER_COLOR["representation"]),
    ("quantile to normal", QuantileTransformer(output_distribution="normal", random_state=0)
     .fit_transform(x[:, None])[:, 0], LEVER_COLOR["representation"]),
]
for k, (name, v, color) in enumerate(versions):
    ax = fig.add_subplot(grid[0, k])
    ax.hist(v, bins=60, color=color)
    ax.set_title(f"{name}\nskewness {stats.skew(v):.2f}", fontsize=10.5)
    ax.set_yticks([])
    ax.grid(False)

# Bottom left: what MSE averages
gen = TabularGenerator(d=3, rho=0.3, sigma0=0.8)
rng = np.random.default_rng(4_000)
z = gen.sample_z(20_000, rng)
log_y = np.log(gen.sample_y(z, rng))
coef = ols(z, log_y)
resid = log_y - (coef[0] + z @ coef[1:])
line = np.linspace(-2, 2, 81)
zl = np.column_stack([line, np.zeros_like(line), np.zeros_like(line)])
pred = coef[0] + zl @ coef[1:]
ax = fig.add_subplot(grid[1, :2])
series = [
    (gen.conditional_mean(zl), INK, "-", r"true mean $\mathbb{E}[y\mid x]$"),
    (gen.conditional_median(zl), INK, (0, (4, 3)), "true median = geometric mean"),
    (np.exp(pred), LEVER_COLOR["representation"], (0, (1, 1.5)), "exp(least squares on log y)"),
    (smearing_predict(pred, resid), LEVER_COLOR["representation"], "-", "smeared"),
]
for vals, color, style, label in series:
    ax.plot(line, vals, color=color, ls=style, lw=2, label=label)
ax.legend(loc="upper left")
ax.annotate("smeared = mean", xy=(line[-1], series[0][0][-1]), xytext=(6, 0),
            textcoords="offset points", va="center", fontsize=9.5, color=INK)
ax.annotate("exp(fit) = median", xy=(line[-1], series[1][0][-1]), xytext=(6, 0),
            textcoords="offset points", va="center", fontsize=9.5, color=INK)
ax.set_xlim(-2, 3.0)
ax.set_xlabel("$z_1$ (other features at 0)")
ax.set_ylabel("$y$ (original scale)")
ax.set_title("What least squares on log y aims at")

# Bottom right: smearing under constant vs. growing noise
ax = fig.add_subplot(grid[1, 2:])
edges = np.linspace(-2, 2, 9)
mids = (edges[:-1] + edges[1:]) / 2
for gamma, color, style, label in ((0.0, LEVER_COLOR["representation"], "-", "constant noise"),
                                   (0.5, MUTED, (0, (5, 2)), "noise growing with $z_1$")):
    g = TabularGenerator(d=3, rho=0.3, sigma0=0.8, gamma=gamma)
    curves = []
    for s in range(10):
        r = np.random.default_rng(4_100 + s)
        zz = g.sample_z(20_000, r)
        ly = np.log(g.sample_y(zz, r))
        c = ols(zz, ly)
        res = ly - (c[0] + zz @ c[1:])
        zn = g.sample_z(20_000, r)
        ratio = smearing_predict(c[0] + zn @ c[1:], res) / g.conditional_mean(zn)
        idx = np.digitize(zn[:, 0], edges) - 1
        curves.append([ratio[idx == b].mean() for b in range(len(mids))])
    curves = np.array(curves)
    lo, med, hi = np.percentile(curves, [10, 50, 90], axis=0)
    ax.fill_between(mids, lo, hi, color=color, alpha=0.15, lw=0)
    ax.semilogy(mids, med, color=color, ls=style, marker="o", ms=4)
    ax.annotate(label, xy=(mids[-1], med[-1]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=9.5, color=INK)
ax.axhline(1, color=INK_SECONDARY, lw=0.8)
ax.set_xlim(-2, 3.6)
ax.set_xlabel("$z_1$")
ax.set_ylabel("smeared prediction / true mean")
ax.set_title("Smearing needs noise that does not depend on $x$")

save_figure(fig, "changing_shape")
