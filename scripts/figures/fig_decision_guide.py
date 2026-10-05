"""Chapter 15: the decision guide's two worked examples (claims 44-46).

Panel A (tabular, T1, 20 seeds): the predicted total cost relative to the true total, for each
treatment of the missing feature (complete cases, mean imputation, regression imputation) and
of the skewed target (least squares on log y back-transformed by exp, and with smearing). Dot =
mean over seeds, bar = range.
Panel B: the per-row relative error of the same pipelines and of least squares on y.
Panel C (audio, T5, 30 seeds): test accuracy against training size when deployment gains vary
by up to +-40 dB: raw waveform, log spectrum, centered log spectrum, gain-augmented log
spectrum, and the log spectrum without the gain shift.

This figure makes visible that each step of the decision procedure is checked against a truth:
the skewed target needs smearing to give the mean, the missing feature needs a treatment that
keeps p(y | x), and a gain shift is removed either by a representation that cannot see it or
by augmentation that teaches the invariance.

Also publishes the chapter's quoted numbers (namespace "ch15") to docs/_variables.yml.

Run: uv run python scripts/figures/fig_decision_guide.py   (about 15 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

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

from data_lab.worked import COST, cost_example, tone_example  # noqa: E402

apply_theme()
cost, rates = cost_example()
sizes = (10, 20, 40, 100)
tones = tone_example(sizes=sizes)

fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(13.5, 4.5),
                                       gridspec_kw={"width_ratios": [1.15, 1.0, 1.1]})
missing_label = {"complete": "complete cases", "mean": "mean imputation",
                 "regress": "regression imputation"}
target_style = {"naive": (MUTED, "o", r"exp(fit of $\log y$)"),
                "smear": (LEVER_COLOR["representation"], "D", "with smearing"),
                "raw": (INK_SECONDARY, "s", "least squares on $y$")}

# A: bias of the total
rows = [(m, t) for m in ("complete", "mean", "regress") for t in ("naive", "smear")]
for k, (m, t) in enumerate(rows):
    b = 100 * cost[(m, t)]["bias"]
    color, marker, _ = target_style[t]
    ax_a.plot([b.min(), b.max()], [k, k], color=color, lw=2)
    ax_a.plot(b.mean(), k, marker=marker, color=color, ms=7, mec="white", mew=1)
ax_a.axvline(0, color=INK, lw=0.8)
ax_a.axvline(100 * (np.exp(-COST.sigma0**2 / 2) - 1), color=MUTED, lw=0.8, ls=(0, (4, 3)))
ax_a.annotate(r"$e^{-\sigma_\varepsilon^2/2}-1$", xy=(100 * (np.exp(-COST.sigma0**2 / 2) - 1), 0.5),
              xytext=(4, 0), textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax_a.set_yticks(range(len(rows)),
                [f"{missing_label[m]}\n{target_style[t][2]}" for m, t in rows], fontsize=8.5)
ax_a.invert_yaxis()
ax_a.set_xlabel("predicted total minus true total (%)")
ax_a.set_title("A. Tabular: is the total right?")
ax_a.grid(axis="y", visible=False)

# B: per-row error
pipes = [(m, t) for m in ("complete", "mean", "regress") for t in ("raw", "naive", "smear")]
for k, (m, t) in enumerate(pipes):
    color, marker, _ = target_style[t]
    ax_b.plot(cost[(m, t)]["rel_rmse"].mean(), k, marker=marker, color=color, ms=7, ls="")
ax_b.set_xscale("log")
ax_b.set_yticks(range(len(pipes)),
                [f"{missing_label[m].split()[0]}, {target_style[t][2]}" for m, t in pipes],
                fontsize=8.5)
ax_b.invert_yaxis()
ax_b.set_xlabel("per-row relative error (RMS)")
ax_b.set_title("B. Tabular: is each prediction right?")
ax_b.grid(axis="y", visible=False)

# C: audio
styles = {
    "raw": (MUTED, ":", "o", "raw waveform"),
    "spectrum": (INK_SECONDARY, "-", "s", "log spectrum"),
    "centered": (LEVER_COLOR["representation"], "-", "D", "log spectrum, centered"),
    "augmented": (LEVER_COLOR["q"], (0, (4, 2)), "^", "log spectrum, gain-augmented"),
    "no_shift": (INK, (0, (1, 1.5)), None, "log spectrum, no gain shift"),
}
for key, (color, ls, marker, label) in styles.items():
    ax_c.plot(sizes, tones[key].mean(axis=0), color=color, ls=ls, marker=marker, ms=5,
              label=label)
ax_c.set_xscale("log")
ax_c.set_xticks(sizes, [str(s) for s in sizes])
ax_c.set_ylim(0.4, 1.02)
ax_c.set_xlabel("training recordings")
ax_c.set_ylabel("test accuracy (gains up to ±40 dB)")
ax_c.legend(loc="center right", fontsize=8.5)
ax_c.set_title("C. Audio: a gain shift, two fixes")

save_figure(fig, "decision_guide")


def pct(x):
    return fmt(100 * x, 0)


acc = {k: v.mean(axis=0) for k, v in tones.items()}
publish("ch15", {
    "missing_rate": pct(rates.mean()),
    "sigma": fmt(COST.sigma0, 1),
    "naive_bias": pct(cost[("complete", "naive")]["bias"].mean()),
    "naive_expected": pct(np.exp(-COST.sigma0**2 / 2) - 1),
    "smear_bias": fmt(100 * cost[("complete", "smear")]["bias"].mean(), 1),
    "smear_bias_min": pct(cost[("complete", "smear")]["bias"].min()),
    "smear_bias_max": pct(cost[("complete", "smear")]["bias"].max()),
    "mean_smear_bias": pct(cost[("mean", "smear")]["bias"].mean()),
    "regress_smear_bias": fmt(100 * cost[("regress", "smear")]["bias"].mean(), 1),
    "raw_rmse": fmt(cost[("complete", "raw")]["rel_rmse"].mean(), 1),
    "raw_bias": pct(cost[("complete", "raw")]["bias"].mean()),
    "smear_rmse": fmt(cost[("complete", "smear")]["rel_rmse"].mean(), 3),
    "acc_raw": fmt(acc["raw"][0], 2),
    "acc_spec_10": fmt(acc["spectrum"][0], 2),
    "acc_noshift_10": fmt(acc["no_shift"][0], 2),
    "acc_centered_10": fmt(acc["centered"][0], 2),
    "acc_aug_10": fmt(acc["augmented"][0], 2),
    "acc_spec_100": fmt(acc["spectrum"][-1], 3),
    "acc_noshift_100": fmt(acc["no_shift"][-1], 3),
})
