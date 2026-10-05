"""Chapter 2: what class-conditional label noise does, and when label errors can be found (T1).

Panel A: the posterior a model learns from noisy labels, P(noisy = 1 | x), against the clean
posterior eta(x), for no noise, symmetric noise (0.2, 0.2) and asymmetric noise (0.1, 0.3);
exact lines; ticks mark where each crosses 1/2.
Panel B: confident learning (CL method 2, Northcutt et al. 2021) on 4,000 examples with 20%
symmetric flips: precision and recall of the flagged examples against the clean classes'
Bayes risk (classes made more or less separable by scaling the true coefficients); mean and
standard deviation over 10 seeds.

This figure makes visible that symmetric noise flattens the learned probabilities without
moving the decision boundary, asymmetric noise moves it, and label errors can be found
reliably only when the clean classes barely overlap.

Run: uv run python scripts/figures/fig_label_noise.py   (about 3 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import INK, INK_SECONDARY, LEVER_COLOR, MUTED, apply_theme, save_figure  # noqa: E402

from data_lab.labels import (  # noqa: E402
    clean_threshold,
    confident_joint_issues,
    flip_labels,
    noisy_posterior,
)
from data_lab.testbeds.t1_tabular import TabularGenerator  # noqa: E402

apply_theme()
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11, 4.3))

eta = np.linspace(0, 1, 201)
settings = [((0.0, 0.0), INK, "-", "no noise"),
            ((0.2, 0.2), LEVER_COLOR["labels"], (0, (5, 2)), r"$\rho_0=\rho_1=0.2$"),
            ((0.1, 0.3), LEVER_COLOR["labels"], "-", r"$\rho_0=0.1,\ \rho_1=0.3$")]
for (r0, r1), color, style, label in settings:
    ax_a.plot(eta, noisy_posterior(eta, r0, r1), color=color, ls=style, lw=2, label=label)
    tau = clean_threshold(r0, r1)
    ax_a.plot([tau], [0.5], marker="o", ms=7, mfc="white", mec=color, mew=1.8)
ax_a.axhline(0.5, color=MUTED, lw=0.8)
ax_a.annotate("boundary moves to\n" + r"$\eta = 0.67$", xy=(clean_threshold(0.1, 0.3), 0.5),
              xytext=(0.72, 0.22), fontsize=9.5, color=INK_SECONDARY,
              arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})
ax_a.set_xlabel(r"clean posterior $\eta(x) = P(y = 1 \mid x)$")
ax_a.set_ylabel("posterior learned from noisy labels")
ax_a.set_title("A. Noise changes what is learned")
ax_a.legend(loc="upper left")
ax_a.set_xlim(0, 1)
ax_a.set_ylim(0, 1)

scales = [0.5, 1.0, 2.0, 4.0, 8.0]
risks, prec, rec = [], [], []
for k in scales:
    gen = TabularGenerator(d=3, rho=0.3, u=np.array([1.5, -1.0, 0.5]) * k)
    risks.append(gen.bayes_risk())
    p_s, r_s = [], []
    for s in range(10):
        rng = np.random.default_rng(25_000 + s)
        z = gen.sample_z(4_000, rng)
        y = gen.sample_labels(z, rng)
        noisy = flip_labels(y, 0.2, 0.2, rng)
        probs = cross_val_predict(LogisticRegression(C=np.inf), z, noisy, cv=4,
                                  method="predict_proba")
        flagged = confident_joint_issues(noisy, probs)
        err = noisy != y
        p_s.append(err[flagged].mean())
        r_s.append(flagged[err].mean())
    prec.append((np.mean(p_s), np.std(p_s)))
    rec.append((np.mean(r_s), np.std(r_s)))
risks = np.array(risks)
series = [(prec, "-", "o", "precision"), (rec, (0, (5, 2)), "s", "recall")]
for vals, style, marker, label in series:
    m, s = np.array(vals).T
    ax_b.errorbar(risks, m, yerr=s, color=LEVER_COLOR["labels"], ls=style, marker=marker,
                  ms=5, lw=2, capsize=3)
    ax_b.annotate(label, xy=(risks[0], m[0]), xytext=(6, 0), textcoords="offset points",
                  va="center", fontsize=9.5, color=INK)
ax_b.axhline(0.2, color=MUTED, lw=0.8)
ax_b.annotate("precision of random flagging (noise rate 0.2)", xy=(0.02, 0.2), xytext=(0, 4),
              textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax_b.set_xlabel("Bayes risk of the clean classes (overlap)")
ax_b.set_ylabel("share of flagged / of flipped examples")
ax_b.set_title("B. Finding flipped labels needs separable classes")
ax_b.set_xlim(0, 0.42)
ax_b.set_ylim(0, 1.05)

save_figure(fig, "label_noise")
