"""Chapter 8: resampling, reweighting, threshold and prior correction; importance weighting;
SMOTE (T1; SPEC §9 "resampling vs reweighting vs threshold calibration comparison").

Panel A: on rare-event T1 (5% positives), predicted probability against the true posterior
eta, for a plain logistic regression, one trained on a balanced undersample, one with balanced
class weights, and the undersampled model after the prior-shift correction (one seed, binned).
Panel B: coefficient on z_1 across 30 seeds for undersampling (q) and class weights (w).
Panel C: importance-weighted and unweighted estimates of the risk under a shifted p from 1,000
examples of q, against the exact risk, as the shift grows (500 seeds; median and 5-95% band).
Panel D: share of SMOTE's synthetic points in the gap between two minority clusters of 20
examples, by neighbor count k, against the true share (50 seeds).

This figure makes visible that resampling and reweighting aim at the same tilted posterior,
which the prior-shift correction undoes, that the two differ in variance, that importance
weighting removes bias at a cost in variance that explodes with the shift, and that SMOTE's
interpolation fills gaps once k exceeds a cluster's size.

Also publishes the chapter's quoted numbers (namespace "ch8") to docs/_variables.yml.

Run: uv run python scripts/figures/fig_sampling_weighting.py   (about 10 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression

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

from data_lab.sampling import (  # noqa: E402
    balanced_undersample,
    em_experiment,
    imbalance_experiment,
    importance_weighting_experiment,
    prior_shift_correct,
    rare_event_generator,
    smote_gap_experiment,
)

apply_theme()
fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.4))

# A: calibration
gen = rare_event_generator(0.05)
prior = gen.prior()
rng = np.random.default_rng(1_000)
z = gen.sample_z(20_000, rng)
y = gen.sample_labels(z, rng)
z_new = gen.sample_z(20_000, rng)
eta = gen.posterior(z_new)
idx = balanced_undersample(y, rng)
p_plain = LogisticRegression(C=np.inf).fit(z, y).predict_proba(z_new)[:, 1]
p_under = LogisticRegression(C=np.inf).fit(z[idx], y[idx]).predict_proba(z_new)[:, 1]
p_weighted = (LogisticRegression(C=np.inf, class_weight="balanced").fit(z, y)
              .predict_proba(z_new)[:, 1])
p_corrected = prior_shift_correct(p_under, 0.5, prior)
ax = axes[0, 0]
edges = np.quantile(eta, np.linspace(0, 1, 16))
mids = 0.5 * (edges[:-1] + edges[1:])
bins = np.clip(np.digitize(eta, edges) - 1, 0, len(mids) - 1)
series = [
    (p_plain, INK, "-", "o", "plain (trained on $p$)"),
    (p_under, LEVER_COLOR["q"], "-", "s", "balanced undersample ($q$)"),
    (p_weighted, LEVER_COLOR["w"], (0, (4, 2)), "D", "balanced class weights ($w$)"),
    (p_corrected, LEVER_COLOR["q"], (0, (1, 1.5)), "^", "undersample, prior-corrected"),
]
for pred, color, style, marker, label in series:
    ax.plot([eta[bins == b].mean() for b in range(len(mids))],
            [pred[bins == b].mean() for b in range(len(mids))],
            color=color, ls=style, marker=marker, ms=4, label=label)
ax.set_xscale("log")
diag = np.logspace(np.log10(mids[0]) - 0.2, 0, 50)
ax.plot(diag, diag, color=MUTED, lw=0.8)
ax.annotate("perfect calibration", xy=(0.3, 0.3), xytext=(-6, 6), textcoords="offset points",
            ha="right", fontsize=8.5, color=INK_SECONDARY)
ax.set_xlim(mids[0] / 2, 1)
ax.set_ylim(0, 1)
ax.set_xlabel(r"true posterior $\eta(x)$ (log scale)")
ax.set_ylabel("predicted probability")
ax.set_title("A. Balancing inflates probabilities")
ax.legend(loc="upper left", fontsize=8.5)

# B: same target, different variance
imb = imbalance_experiment()
ax = axes[0, 1]
for j, (key, color, _label) in enumerate((("under_coef", LEVER_COLOR["q"], "undersample ($q$)"),
                                         ("weighted_coef", LEVER_COLOR["w"],
                                          "class weights ($w$)"))):
    vals = imb[key]
    ax.scatter(np.full(vals.size, j) + np.linspace(-0.2, 0.2, vals.size), vals, s=14,
               color=color)
    ax.plot([j - 0.3, j + 0.3], [vals.mean()] * 2, color=INK, lw=1.5)
    ax.annotate(f"sd {vals.std(ddof=1):.3f}", xy=(j, vals.max()), xytext=(0, 6),
                textcoords="offset points", ha="center", fontsize=9, color=INK_SECONDARY)
ax.axhline(gen.u[0], color=INK, lw=0.9, ls=(0, (4, 3)))
ax.set_xticks([0, 1], ["undersample ($q$)", "class weights ($w$)"])
ax.set_xlim(-0.5, 1.5)
ax.set_ylabel("coefficient on $z_1$ (truth 1.5)")
ax.set_title("B. Same target, different variance")
ax.grid(axis="x", visible=False)

# C: importance weighting
iw = importance_weighting_experiment()
ax = axes[1, 0]
shifts = iw["shifts"]
lo, med, hi = np.percentile(iw["iw"], [5, 50, 95], axis=0)
ax.fill_between(shifts, lo, hi, color=LEVER_COLOR["w"], alpha=0.2, lw=0)
ax.plot(shifts, iw["iw"].mean(axis=0), color=LEVER_COLOR["w"], marker="o", ms=4)
ax.plot(shifts, iw["naive"].mean(axis=0), color=MUTED, ls=(0, (5, 2)), marker="s", ms=4)
ax.plot(shifts, iw["truth"], color=INK, lw=1.2)
ax.annotate("unweighted", xy=(shifts[-1], iw["naive"].mean()), xytext=(6, 0),
            textcoords="offset points", va="center", fontsize=9.5, color=INK)
ax.annotate("weighted (mean, 5-95%)", xy=(shifts[-1], hi[-1]), xytext=(6, 0),
            textcoords="offset points", va="center", fontsize=9.5, color=INK)
ax.annotate("exact risk under $p$", xy=(shifts[-1], iw["truth"][-1]), xytext=(6, -8),
            textcoords="offset points", va="center", fontsize=9.5, color=INK)
ax.set_xlim(-0.05, 2.9)
ax.set_xlabel(r"shift $\delta$ of $z_1$'s mean under $p$")
ax.set_ylabel("estimated 0-1 risk under $p$")
ax.set_title("C. Importance weighting: unbiased, noisy")

# D: SMOTE
ks, shares, true_share = smote_gap_experiment()
ax = axes[1, 1]
ax.plot(ks, shares.mean(axis=0), color=LEVER_COLOR["q"], marker="o", ms=4)
ax.fill_between(ks, *np.percentile(shares, [10, 90], axis=0), color=LEVER_COLOR["q"],
                alpha=0.15, lw=0)
ax.axhline(true_share, color=INK, lw=0.9, ls=(0, (4, 3)))
ax.annotate("true minority share of the gap", xy=(ks[0], true_share), xytext=(0, 5),
            textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax.axvline(10, color=MUTED, lw=0.8)
ax.annotate("about one cluster\n(20 examples / 2)", xy=(10, 0.25), xytext=(4, 0),
            textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax.set_xlabel("SMOTE neighbors $k$")
ax.set_ylabel("share of synthetic points in the gap")
ax.set_title("D. SMOTE fills gaps once $k$ exceeds a cluster")

save_figure(fig, "sampling_weighting")

em = em_experiment()
# Effective sample size at the largest shift: n such that a plain mean of 0-1 losses with the
# same risk would have the importance-weighted estimate's exact variance (see tests/test_shift).
d_last = np.array([iw["shifts"][-1], 0.0, 0.0])
from data_lab.testbeds.t1_tabular import TabularGenerator  # noqa: E402

g1 = TabularGenerator(d=3, rho=0.3)
r_last = iw["truth"][-1]
var_exact = (g1.density_ratio_second_moment(d_last) * g1.threshold_risk(0.5, shift=2 * d_last)
             - r_last**2) / 1_000
n_eff = r_last * (1 - r_last) / var_exact
boot_rng = np.random.default_rng(0)
boot = [iw["iw"][boot_rng.integers(0, 500, 500), -1].var(ddof=1) for _ in range(2_000)]
boot_lo, boot_hi = np.percentile(boot, [2.5, 97.5])
publish("ch8", {
    "prior": fmt(prior, 3),
    "plain_err": fmt(imb["plain"].mean(), 4),
    "under_err": fmt(imb["under"].mean(), 3),
    "weighted_err": fmt(imb["weighted"].mean(), 3),
    "under_corr_err": fmt(imb["under_corrected"].mean(), 4),
    "weighted_corr_err": fmt(imb["weighted_corrected"].mean(), 4),
    "under_coef_mean": fmt(imb["under_coef"].mean(), 3),
    "weighted_coef_mean": fmt(imb["weighted_coef"].mean(), 3),
    "under_coef_sd": fmt(imb["under_coef"].std(ddof=1), 3),
    "weighted_coef_sd": fmt(imb["weighted_coef"].std(ddof=1), 3),
    "em_mean": fmt(em.mean(), 4),
    "em_min": fmt(em.min(), 3),
    "em_max": fmt(em.max(), 3),
    "iw_sd_first": fmt(iw["iw"][:, 0].std(ddof=1), 3),
    "iw_sd_last": fmt(iw["iw"][:, -1].std(ddof=1), 3),
    "iw_truth_last": fmt(iw["truth"][-1], 3),
    "iw_mean_last": fmt(iw["iw"][:, -1].mean(), 3),
    "naive_mean": fmt(iw["naive"].mean(), 3),
    "w2_last": fmt(iw["second_moment"][-1], 0),
    "w2_mid": fmt(iw["second_moment"][2], 2),
    "n_eff_last": fmt(int(round(n_eff, -1))),
    "boot_ratio_last": fmt(boot_hi / boot_lo, 1),
    "smote_true_gap": fmt(100 * true_share, 1),
    "smote_gap_k5": fmt(100 * shares.mean(axis=0)[list(ks).index(5)], 1),
    "smote_gap_k15": fmt(100 * shares.mean(axis=0)[list(ks).index(15)], 1),
    "smote_gap_k19": fmt(100 * shares.mean(axis=0)[list(ks).index(19)], 1),
})
