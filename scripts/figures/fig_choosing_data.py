"""Chapter 14: choosing data (claims 17, 18, 20 and 43).

Panel A: on T3 (dimension 100), exact test error after keeping the hardest half, the easiest
half or a random half of P = ratio * 100 examples, against the ratio (20 seeds; Sorscher et
al.'s easy/hard crossover).
Panel B: on T4 with duplicated documents, a trigram model's measured test cross-entropy minus
its cross-entropy on fresh documents, with a contaminated split and after deduplication (20
seeds).
Panel C: on T1, disagreement with the Bayes rule after 100 labels, uncertainty sampling divided
by random labeling, as label noise grows (60 seeds).
Panel D: on T2 (alpha = 1, 10,000 draws per generation), the p-mass outside a generator's
support over generations, replacing vs accumulating data (20 seeds).

This figure makes visible that every way of choosing data rests on a condition: pruning
toward hard examples needs abundant data, an evaluation needs deduplication, uncertainty
sampling needs clean labels, and training on generated data needs the real data kept.

Also publishes the chapter's quoted numbers (namespace "ch14") to docs/_variables.yml.

Run: uv run python scripts/figures/fig_choosing_data.py   (about 60 s)
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
    LEVER_COLOR,
    MUTED,
    apply_theme,
    save_figure,
)
from publish import fmt, publish  # noqa: E402

from data_lab.selection import (  # noqa: E402
    active_learning_experiment,
    collapse_experiment,
    dedup_experiment,
    pruning_experiment,
)
from data_lab.testbeds.t1_tabular import TabularGenerator  # noqa: E402
from data_lab.testbeds.t2_zipf import ZipfStream  # noqa: E402

apply_theme()
fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.4))

# A: pruning crossover
ratios = (1.0, 2.0, 4.0, 8.0, 16.0)
prune = pruning_experiment(ratios)
ax = axes[0, 0]
for key, color, style, marker, label in (
        ("random", MUTED, "-", "o", "random half"),
        ("easy", LEVER_COLOR["q"], (0, (4, 2)), "s", "easiest half (largest margin)"),
        ("hard", LEVER_COLOR["q"], "-", "D", "hardest half (smallest margin)")):
    ax.loglog(ratios, prune[key].mean(axis=0), color=color, ls=style, marker=marker, ms=5,
              label=label)
ax.legend(loc="lower left", fontsize=8.5)
ax.set_xlabel("initial examples per dimension $P/N$")
ax.set_ylabel("test error (exact)")
ax.set_title("A. Keep hard only when data is abundant")

# B: dedup
dd = dedup_experiment()
ax = axes[0, 1]
opt = dd["contaminated"] - dd["fresh"]
opt_dd = dd["dedup"] - dd["fresh_dedup"]
for j, (vals, color) in enumerate(((opt, EVALUATION_COLOR), (opt_dd, MUTED))):
    ax.scatter(np.full(vals.size, j) + np.linspace(-0.15, 0.15, vals.size), vals, s=14,
               color=color)
    ax.plot([j - 0.25, j + 0.25], [vals.mean()] * 2, color=INK, lw=1.5)
ax.axhline(0, color=INK_SECONDARY, lw=0.8)
ax.set_xticks([0, 1], ["duplicates across\nthe split", "deduplicated\nbefore splitting"])
ax.set_ylabel("measured minus fresh cross-entropy (nats)")
ax.set_title("B. Duplicates flatter the test set")
ax.grid(axis="x", visible=False)

# C: active learning vs noise
scales = (4.0, 2.0, 1.0, 0.5)
ratio_100, bayes_risk = [], []
for scale in scales:
    r = active_learning_experiment(scale, seeds=60)
    ratio_100.append(r["uncertainty"][:, -1].mean() / r["random"][:, -1].mean())
    gen = TabularGenerator(d=3, rho=0.3, u=np.array([1.5, -1.0, 0.5]) * scale)
    bayes_risk.append(gen.bayes_risk())
ax = axes[1, 0]
ax.plot(bayes_risk, ratio_100, color=LEVER_COLOR["q"], marker="o", ms=5)
ax.axhline(1.0, color=INK_SECONDARY, lw=0.8)
ax.annotate("no gain", xy=(bayes_risk[0], 1.0), xytext=(2, 4), textcoords="offset points",
            fontsize=9, color=INK_SECONDARY)
ax.set_xlabel("Bayes risk (label noise)")
ax.set_ylabel("uncertainty / random disagreement\n(100 labels)")
ax.set_ylim(0.4, 1.2)
ax.set_title("C. Uncertainty sampling needs clean labels")

# D: collapse
col = collapse_experiment()
ax = axes[1, 1]
gens = np.arange(col["replace"].shape[1])
for key, color, style, label in (("replace", LEVER_COLOR["q"], "-", "replace (synthetic only)"),
                                  ("accumulate", INK_SECONDARY, (0, (4, 2)),
                                   "accumulate (real data kept)")):
    vals = col[key]
    ax.fill_between(gens, *np.percentile(vals, [10, 90], axis=0), color=color, alpha=0.15, lw=0)
    ax.plot(gens, vals.mean(axis=0), color=color, ls=style, marker="o", ms=4, label=label)
exact = ZipfStream(1.0).expected_error(10_000).mid
ax.axhline(exact, color=INK, lw=0.8, ls=(0, (1, 2)))
ax.annotate("Hutter's $E_{t_0}$ (exact)", xy=(gens[-1], exact), xytext=(-4, -12),
            textcoords="offset points", ha="right", fontsize=9, color=INK_SECONDARY)
ax.legend(loc="upper left", fontsize=8.5)
ax.set_xlabel("generation")
ax.set_ylabel("mass outside the generator's support")
ax.set_title("D. Model collapse loses the tail")

save_figure(fig, "choosing_data")

h = prune["hard"] < prune["easy"]
publish("ch14", {
    "easy_scarce": fmt(prune["easy"][:, 0].mean(), 3),
    "hard_scarce": fmt(prune["hard"][:, 0].mean(), 3),
    "random_scarce": fmt(prune["random"][:, 0].mean(), 3),
    "easy_rich": fmt(prune["easy"][:, -1].mean(), 4),
    "hard_rich": fmt(prune["hard"][:, -1].mean(), 4),
    "random_rich": fmt(prune["random"][:, -1].mean(), 4),
    "hard_wins_scarce": fmt(int(h[:, 0].sum())), "hard_wins_rich": fmt(int(h[:, -1].sum())),
    "hard_wins_mid": fmt(int(h[:, 2].sum())),
    "dedup_overlap": fmt(100 * dd["overlap"].mean(), 0),
    "opt_contam": fmt(-opt.mean(), 2), "opt_contam_min": fmt(-opt.max(), 2),
    "opt_contam_max": fmt(-opt.min(), 2),
    "opt_dedup_abs_max": fmt(np.abs(opt_dd).max(), 2),
    "al_ratio_clean": fmt(ratio_100[0], 2), "al_ratio_noisy": fmt(ratio_100[2], 2),
    "al_ratio_very_noisy": fmt(ratio_100[3], 2),
    "bayes_clean": fmt(bayes_risk[0], 2), "bayes_noisy": fmt(bayes_risk[2], 2),
    "collapse_g0": fmt(col["replace"][:, 0].mean(), 4),
    "collapse_g9": fmt(col["replace"][:, -1].mean(), 4),
    "hutter_e_t0": fmt(exact, 4),
})
