"""Chapter 5: which models care about affine scaling, and what outliers do to it (T1).

Panel A: 15-nearest-neighbor test accuracy on T1 as one informative feature is put on a larger
scale, on raw and on standardized features (20 seeds, mean and range; claim 3).
Panel B: the inliers of a standard normal sample with 1% gross outliers at 100, after
StandardScaler and after RobustScaler (claim 29).
Panel C: condition number of the least-squares Hessian as one feature's scale grows, raw and
standardized (claim 21); gradient descent slows as it grows (optimization-lab).

This figure makes visible that affine scaling changes nothing about the data's shape but
everything for distance-based models and for the conditioning of a fit, and that one scaler
is built to ignore outliers that wreck the others.

Run: uv run python scripts/figures/fig_affine_scaling.py   (about 3 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import RobustScaler, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import INK, INK_SECONDARY, LEVER_COLOR, MUTED, apply_theme, save_figure  # noqa: E402

from data_lab.testbeds.t1_tabular import TabularGenerator  # noqa: E402
from data_lab.transforms import contaminate, least_squares_condition  # noqa: E402

apply_theme()
gen = TabularGenerator(d=3, rho=0.3)
fig, axes = plt.subplots(1, 3, figsize=(13, 4.0))

# A
scales = [1, 3, 10, 30, 100, 300]
acc = {"raw": [], "standardized": []}
for k in scales:
    raw, std = [], []
    for s in range(20):
        rng = np.random.default_rng(3_000 + s)
        z = gen.sample_z(2_000, rng)
        y = gen.sample_labels(z, rng)
        x = z * np.array([1.0, 1.0, float(k)])
        tr, te = slice(0, 1_000), slice(1_000, 2_000)
        raw.append(KNeighborsClassifier(15).fit(x[tr], y[tr]).score(x[te], y[te]))
        sc = StandardScaler().fit(x[tr])
        std.append(KNeighborsClassifier(15).fit(sc.transform(x[tr]), y[tr])
                   .score(sc.transform(x[te]), y[te]))
    acc["raw"].append(raw)
    acc["standardized"].append(std)
ax = axes[0]
for name, color, style in (("raw", MUTED, (0, (5, 2))),
                           ("standardized", LEVER_COLOR["representation"], "-")):
    vals = np.array(acc[name])
    ax.fill_between(scales, vals.min(1), vals.max(1), color=color, alpha=0.15, lw=0)
    ax.semilogx(scales, vals.mean(1), color=color, ls=style, marker="o", ms=4)
    ax.annotate(name, xy=(scales[-1], vals.mean(1)[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", fontsize=9.5, color=INK)
bayes = 1 - gen.bayes_risk()
ax.axhline(bayes, color=INK, lw=0.9, ls=(0, (4, 3)))
ax.annotate("Bayes accuracy", xy=(1, bayes), xytext=(2, 4), textcoords="offset points",
            fontsize=9, color=INK_SECONDARY)
ax.set_xlim(0.8, 1_500)
ax.set_xlabel("scale of feature 3 (relative)")
ax.set_ylabel("15-NN test accuracy")
ax.set_title("A. Distances depend on units")

# B
rng = np.random.default_rng(29)
clean = rng.standard_normal(20_000)
dirty, outlier = contaminate(clean, 0.01, 100.0, rng)
ax = axes[1]
bins = np.linspace(-3, 3, 61)
for scaler, color, label in ((StandardScaler, MUTED, "StandardScaler"),
                             (RobustScaler, LEVER_COLOR["representation"], "RobustScaler")):
    out = scaler().fit_transform(dirty[:, None])[:, 0][~outlier]
    ax.hist(out, bins=bins, color=color, alpha=0.6, label=f"{label}: spread {out.std():.2f}")
ax.set_xlabel("transformed value (inliers only)")
ax.set_ylabel("count")
ax.set_title("B. 1% outliers at 100")
ax.legend(loc="upper left", fontsize=8.5)

# C
ratios = np.logspace(0, 4, 9)
z = gen.sample_z(5_000, np.random.default_rng(21))
raw_c = [least_squares_condition(z * np.array([1.0, 1.0, r])) for r in ratios]
std_c = [least_squares_condition(StandardScaler().fit_transform(z * np.array([1.0, 1.0, r])))
         for r in ratios]
ax = axes[2]
ax.loglog(ratios, raw_c, color=MUTED, ls=(0, (5, 2)), marker="o", ms=4)
ax.loglog(ratios, std_c, color=LEVER_COLOR["representation"], marker="o", ms=4)
ax.annotate("raw", xy=(ratios[-1], raw_c[-1]), xytext=(-24, 0), textcoords="offset points",
            va="center", fontsize=9.5, color=INK)
ax.annotate("standardized", xy=(ratios[-1], std_c[-1]), xytext=(-70, 10),
            textcoords="offset points", fontsize=9.5, color=INK)
ax.set_xlabel("scale of feature 3 (relative)")
ax.set_ylabel("condition number, least-squares Hessian")
ax.set_title("C. Conditioning of least squares")

save_figure(fig, "affine_scaling")
