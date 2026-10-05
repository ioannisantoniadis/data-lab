"""Chapter 4: two leaks of very different size (T1 and pure noise; claims 28 and 9).

Panel A: 1-nearest-neighbor test accuracy on T1 as a growing share of the test rows are copies
of training rows, measured on the contaminated test set and on its fresh rows only; the
Bayes accuracy is the most any classifier can reach on fresh data (20 seeds, mean and range).
Panel B: change in test accuracy from fitting a preprocessing step on train + test instead of
on train only. Unsupervised steps (scaler, min-max, mean imputer; kNN and regularized logistic
regression; 200 seeds each) against a supervised step (feature selection on pure-noise labels,
selected on all data versus inside the folds; 20 seeds).

This figure makes visible that duplicated rows let a model score above what is possible on new
data, and that "never fit on the test data" guards against two leaks of very different size:
unsupervised steps barely move the estimate, supervised steps fabricate a signal.

Run: uv run python scripts/figures/fig_leakage.py   (about 10 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import (  # noqa: E402
    EVALUATION_COLOR,
    INK,
    INK_SECONDARY,
    MUTED,
    apply_theme,
    save_figure,
)

from data_lab.cleaning import (  # noqa: E402
    duplicate_experiment,
    supervised_selection_leak,
    unsupervised_fit_gap,
)
from data_lab.testbeds.t1_tabular import TabularGenerator  # noqa: E402

apply_theme()
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.5, 4.3),
                                 gridspec_kw={"width_ratios": [1, 1.15]})

shares = [0.0, 0.1, 0.2, 0.3, 0.5]
runs = np.array([duplicate_experiment(s) for s in shares])  # (shares, seeds, 2)
for k, (label, style, marker) in enumerate([("contaminated test set", "-", "o"),
                                            ("fresh rows only", (0, (5, 2)), "s")]):
    vals = runs[:, :, k]
    ax_a.fill_between(shares, vals.min(axis=1), vals.max(axis=1), color=EVALUATION_COLOR,
                      alpha=0.12, lw=0)
    ax_a.plot(shares, vals.mean(axis=1), color=EVALUATION_COLOR, ls=style, marker=marker,
              ms=5, lw=2)
    ax_a.annotate(label, xy=(shares[-1], vals.mean(axis=1)[-1]), xytext=(6, 0),
                  textcoords="offset points", va="center", fontsize=9.5, color=INK)
bayes = 1 - TabularGenerator(d=3, rho=0.3).bayes_risk()
ax_a.axhline(bayes, color=INK, lw=1, ls=(0, (4, 3)))
ax_a.annotate("Bayes accuracy", xy=(0.0, bayes), xytext=(2, 4), textcoords="offset points",
              fontsize=9, color=INK_SECONDARY)
ax_a.set_xlim(-0.02, 0.8)
ax_a.set_xlabel("share of test rows copied from training")
ax_a.set_ylabel("1-NN test accuracy")
ax_a.set_title("A. Duplicates inflate the test score")

labels, gaps = [], []
for model in ("knn", "logreg"):
    for prep, name in (("std", "standard scaler"), ("minmax", "min-max scaler"),
                       ("impute", "mean imputer")):
        labels.append(f"{name}, {'kNN' if model == 'knn' else 'logistic'}")
        gaps.append(unsupervised_fit_gap(prep, model))
sel = supervised_selection_leak()
labels.append("feature selection, kNN")
gaps.append(sel[:, 0] - sel[:, 1])
for i, g in enumerate(gaps):
    color = MUTED if i < len(gaps) - 1 else INK
    jitter = np.random.default_rng(i).uniform(-0.25, 0.25, g.size)
    ax_b.scatter(g, i + jitter, s=6, color=color, alpha=0.4)
    ax_b.plot([g.mean()] * 2, [i - 0.35, i + 0.35], color=INK, lw=1.8)
ax_b.axvline(0, color=INK_SECONDARY, lw=0.8)
ax_b.set_yticks(range(len(labels)), labels)
ax_b.invert_yaxis()
ax_b.set_xlabel("accuracy, fit on train + test minus fit on train")
ax_b.set_title("B. Unsupervised vs. supervised steps")
ax_b.grid(axis="y", visible=False)

save_figure(fig, "leakage")
