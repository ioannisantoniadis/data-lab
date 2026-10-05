"""Chapter 7: what an encoding lets a model see, and how target encoding leaks (claims 8, 34).

Panel A: T1 classification plus one pure-noise categorical feature with 1,000 levels. Training
and test accuracy of an unpenalized logistic regression without the feature, with it target-
encoded on the same rows ("naive"), and with it cross-fitted (TargetEncoder.fit_transform);
lines join each seed's train and test score (20 seeds).
Panel B: y = sin(2x) + noise; the same linear regression on raw x, on 20 quantile bins
(one-hot), and on a cubic spline basis with 8 knots; the true curve in black.

This figure makes visible that a target encoding fit on the rows it encodes turns noise into a
training signal that collapses on new data, and that bins and splines let a linear model fit a
curve.

Run: uv run python scripts/figures/fig_encoding.py   (about 3 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import KBinsDiscretizer, SplineTransformer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import (  # noqa: E402
    GRIDLINE,
    INK,
    INK_SECONDARY,
    LEVER_COLOR,
    MUTED,
    apply_theme,
    save_figure,
)

from data_lab.transforms import target_encoding_experiment  # noqa: E402

apply_theme()
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.5, 4.3))

res = target_encoding_experiment()
methods = [("none", "without the\nnoise feature", MUTED),
           ("naive", "target-encoded,\nno cross-fitting", INK),
           ("crossfit", "target-encoded,\ncross-fitted", LEVER_COLOR["representation"])]
for j, (key, _label, color) in enumerate(methods):
    train, test = res[key][:, 0], res[key][:, 1]
    for a, b in zip(train, test, strict=True):
        ax_a.plot([j - 0.18, j + 0.18], [a, b], color=color, lw=0.7, alpha=0.5)
    ax_a.scatter(np.full(train.size, j - 0.18), train, s=10, color=color, marker="o")
    ax_a.scatter(np.full(test.size, j + 0.18), test, s=10, color=color, marker="s")
ax_a.set_xticks(range(3), [m[1] for m in methods])
ax_a.annotate("train", xy=(1 - 0.18, res["naive"][:, 0].max()), xytext=(-8, 6),
              textcoords="offset points", ha="right", fontsize=9, color=INK_SECONDARY)
ax_a.annotate("test", xy=(1 + 0.18, res["naive"][:, 1].min()), xytext=(8, -4),
              textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax_a.set_ylabel("accuracy (circles: train, squares: test)")
ax_a.set_title("A. A pure-noise category, target-encoded")
ax_a.grid(axis="x", visible=False)

rng = np.random.default_rng(34)
x = rng.uniform(-3, 3, (4_000, 1))
y = np.sin(2 * x[:, 0]) + 0.3 * rng.standard_normal(4_000)
grid = np.linspace(-3, 3, 400)[:, None]
ax_b.scatter(x[:600, 0], y[:600], s=4, color=GRIDLINE)
ax_b.plot(grid[:, 0], np.sin(2 * grid[:, 0]), color=INK, lw=2, label="truth")
fits = [
    ("raw $x$", LinearRegression(), MUTED, (0, (5, 2))),
    ("20 quantile bins", make_pipeline(KBinsDiscretizer(n_bins=20, strategy="quantile"),
                                       LinearRegression()), LEVER_COLOR["representation"],
     (0, (1, 1))),
    ("cubic spline, 8 knots", make_pipeline(SplineTransformer(n_knots=8), LinearRegression()),
     LEVER_COLOR["representation"], "-"),
]
for label, model, color, style in fits:
    model.fit(x[:2_000], y[:2_000])
    r2 = model.score(x[2_000:], y[2_000:])
    ax_b.plot(grid[:, 0], model.predict(grid), color=color, ls=style, lw=2,
              label=f"{label} (test $R^2$ {r2:.2f})")
ax_b.legend(loc="lower left", fontsize=8.5)
ax_b.set_ylim(-2.6, 2.0)
ax_b.set_xlabel("$x$")
ax_b.set_ylabel("$y$")
ax_b.set_title("B. One linear model, three representations")

save_figure(fig, "encoding")
