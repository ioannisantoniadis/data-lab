"""Signature figure (SPEC §9): the long tail on Hutter's model (T2).

Panel A: exact expected error E_n of the memorizing learner under uniform sampling, for three
Zipf exponents alpha, with Monte Carlo means (200 seeds) on top and the asymptote
c n^-alpha/(1+alpha) as a guide.

Panel B (alpha = 1): error against labels used. Uniform sampling labeling every draw (exact);
the same uniform stream labeling only features not seen before (exact curve (E[D_m], E_m));
the oracle coverage selector that labels features 1..n (exact, the lower bound for any n
labels); and a selector that knows nothing about p: it sees an unlabeled pool of M draws and
labels the n distinct features counted most often (budget n). Pools of M = 10 n and 100 n,
and M = n^2 = n^(1+alpha); median and 10-90% band over seeds, plotted at the labels actually
used: a pool with fewer distinct features than the budget labels them all and no more.

This figure makes visible that uniform sampling's error falls as a power law set by the tail
(slope -alpha/(1+alpha)); that per label, not paying for repeats is what steepens it to
-alpha, with frequency ordering adding only a constant factor; and that the steeper slope is
never an escape from a power law, and costs about n^(1+alpha) draws; and that a pool too small
to fill the budget is the deduplicated stream again, while a pool of n^(1+alpha) draws moves
toward the oracle.

Also publishes the chapter's quoted numbers (namespace "ch13") to docs/_variables.yml.

Run: uv run python scripts/figures/fig_long_tail_signature.py   (about 30 s on a laptop CPU)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _theme import (  # noqa: E402
    INK,
    INK_SECONDARY,
    LEVER_COLOR,
    MUTED,
    SEQUENTIAL_BLUE,
    apply_theme,
    save_figure,
)
from publish import fmt, publish  # noqa: E402

from data_lab.testbeds.t2_zipf import (  # noqa: E402
    ZipfStream,
    at_labels,
    pool_selector,
    uniform_selector,
)

apply_theme()
SEED = 2026


def asymptote(stream: ZipfStream, n):
    """c n^-beta with c = A^(1/s) Gamma(beta)/s, A = 1/zeta(s) (checked in tests)."""
    c = (1.0 / stream.normalizer) ** (1.0 / stream.s) * gamma(stream.beta) / stream.s
    return c * np.asarray(n, dtype=float) ** (-stream.beta)


fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.5, 4.6))

# --- Panel A ------------------------------------------------------------------------------------
n_grid = np.unique(np.logspace(0, 6, 61).round())
mc_ns = [10, 100, 1_000, 10_000]
shades = {0.5: SEQUENTIAL_BLUE[4], 1.0: SEQUENTIAL_BLUE[7], 2.0: SEQUENTIAL_BLUE[9]}
for alpha, color in shades.items():
    stream = ZipfStream(alpha)
    exact = np.array([stream.expected_error(n).mid for n in n_grid])
    ax_a.loglog(n_grid, exact, color=color, lw=2.0)
    tail = n_grid[n_grid >= 100]
    ax_a.loglog(tail, asymptote(stream, tail), color=INK_SECONDARY, lw=0.9, ls=(0, (4, 3)))
    rng = np.random.default_rng(SEED)
    for n in mc_ns:
        errs = [stream.memorizer_error(uniform_selector(stream, n, rng)) for _ in range(200)]
        ax_a.plot(n, np.mean(errs), "o", ms=6, mfc="white", mec=color, mew=1.6)
    ax_a.annotate(
        rf"$\alpha={alpha:g}$: slope $-{stream.beta:.2f}$",
        xy=(n_grid[-1], exact[-1]),
        xytext=(4, 0),
        textcoords="offset points",
        va="center",
        fontsize=9.5,
        color=INK,
    )
ax_a.plot([], [], color=SEQUENTIAL_BLUE[7], label="exact $E_n$ (Hutter's sum)")
ax_a.plot([], [], "o", mfc="white", mec=SEQUENTIAL_BLUE[7], label="Monte Carlo, 200 seeds")
ax_a.plot([], [], color=INK_SECONDARY, lw=0.9, ls=(0, (4, 3)), label=r"$c\,n^{-\alpha/(1+\alpha)}$")
ax_a.legend(loc="lower left")
ax_a.set_xlim(1, 4e7)
ax_a.set_ylim(1.5e-5, 1.5)
ax_a.set_xlabel("training examples $n$ (uniform sampling from $p$)")
ax_a.set_ylabel("expected test error")
ax_a.set_title("A. The tail sets a power law")

# --- Panel B ------------------------------------------------------------------------------------
stream = ZipfStream(1.0)
ns = np.unique(np.logspace(np.log10(30), np.log10(2_000), 7).round()).astype(int)
uniform = np.array([stream.expected_error(n).mid for n in ns])
oracle = stream.tail_mass(ns)
_, dedup = at_labels(stream, ns)
ax_b.loglog(ns, uniform, color=INK_SECONDARY, lw=2.0)
ax_b.loglog(ns, dedup, color=INK_SECONDARY, lw=2.0, ls=(0, (2, 1.5)))
ax_b.loglog(ns, oracle, color=INK, lw=2.0, ls=(0, (6, 2)))

pools = [
    ("pool $M = 10\\,n$", lambda n: 10 * n, 60, (0, (1, 1.5))),
    ("pool $M = 100\\,n$", lambda n: 100 * n, 40, (0, (5, 2))),
    ("pool $M = n^2$", lambda n: n * n, 12, "-"),
]
for label, size, seeds, style in pools:
    rng = np.random.default_rng(SEED + seeds)
    picks = [[pool_selector(stream, n, size(n), rng) for n in ns] for _ in range(seeds)]
    runs = np.array([[stream.memorizer_error(x) for x in row] for row in picks])
    # A pool with fewer distinct cases than the budget labels all of them and no more, so each
    # point is plotted at the labels actually used (mean over seeds), not at the budget n.
    used = np.array([[len(x) for x in row] for row in picks]).mean(axis=0)
    lo, med, hi = np.percentile(runs, [10, 50, 90], axis=0)
    ax_b.fill_between(used, lo, hi, color=LEVER_COLOR["q"], alpha=0.15, lw=0)
    ax_b.loglog(used, med, color=LEVER_COLOR["q"], lw=2.0, ls=style, marker="o", ms=4,
                label=label)
ax_b.legend(loc="lower left", fontsize=9, title="selector ranking an unlabeled pool",
            title_fontsize=8.5)

labels = {
    "uniform, every draw labeled": uniform[-1],
    "uniform, new cases only": dedup[-1],
    "oracle: features $1..n$": oracle[-1],
}
# Spread end labels at least a factor GAP apart in y (log axis), keeping their order.
GAP = 1.55
placed = sorted(labels.items(), key=lambda kv: kv[1])
ys = [placed[0][1]]
for _, y in placed[1:]:
    ys.append(max(y, ys[-1] * GAP))
for (text, y), y_text in zip(placed, ys, strict=True):
    ax_b.annotate(text, xy=(ns[-1], y), xytext=(ns[-1] * 1.12, y_text), va="center",
                  fontsize=9.5, color=INK,
                  arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.6}
                  if y_text != y else None)
x0, x1 = ns[0], ns[-1]
ax_b.loglog([x0, x1], [2.2 * uniform[0], 2.2 * uniform[0] * (x1 / x0) ** -0.5],
            color=MUTED, lw=0.8)
ax_b.annotate("slope $-1/2$", xy=(x0 * 1.3, 2.2 * uniform[0] * 1.3**-0.5), xytext=(0, 6),
              textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax_b.loglog([x0, x1], [0.45 * oracle[0], 0.45 * oracle[0] * (x1 / x0) ** -1.0],
            color=MUTED, lw=0.8)
ax_b.annotate("slope $-1$", xy=(x0 * 1.2, 0.45 * oracle[0] / 1.2), xytext=(0, -14),
              textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax_b.set_xlim(10, ns[-1] * 9)
ax_b.set_xlabel("labels used $n$")
ax_b.set_ylabel(r"expected test error ($\alpha = 1$)")
ax_b.set_title("B. Skipping repeats steepens it, at a price")

save_figure(fig, "long_tail_signature")


# Numbers quoted in chapter 13 (computed here from the same objects as the tests).
s1 = ZipfStream(1.0)


def local_slope(f, n1, n2):
    return np.log(f(n2) / f(n1)) / np.log(n2 / n1)


uni = local_slope(lambda n: s1.expected_error(n).mid, 1e5, 1e6)
ora = local_slope(lambda n: float(s1.tail_mass(n)), 1e4, 1e5)
distinct_100 = s1.expected_distinct(100).mid


def pool_mean(n, size_fn, seeds, base):
    return np.mean([s1.memorizer_error(pool_selector(s1, n, size_fn(n),
                                                     np.random.default_rng(base + k)))
                    for k in range(seeds)])


lin = np.log(pool_mean(1_000, lambda n: 10 * n, 100, 16_100 + 1_000)
             / pool_mean(100, lambda n: 10 * n, 100, 16_100 + 100)) / np.log(10)
quad_1000 = pool_mean(1_000, lambda n: n * n, 20, 16_200 + 1_000)
quad = np.log(quad_1000 / pool_mean(100, lambda n: n * n, 20, 16_200 + 100)) / np.log(10)
ded_m, ded_err = at_labels(s1, [1_000, 10_000])
ded_slope = np.log(ded_err[1] / ded_err[0]) / np.log(10)
const = {a: ZipfStream(a).beta * gamma(ZipfStream(a).beta) ** (1 + a) for a in (0.5, 1.0, 2.0)}
publish("ch13", {
    "dedup_slope": fmt(ded_slope, 3),
    "dedup_over_oracle": fmt(ded_err[0] / float(s1.tail_mass(1_000)), 2),
    "dedup_draws_1000": fmt(round(ded_m[0], -3), 0),
    "dedup_const_half": fmt(const[0.5], 2),
    "dedup_const_two": fmt(const[2.0], 2),
    "uniform_slope": fmt(uni, 3),
    "oracle_slope": fmt(ora, 3),
    "repeat_share_100": fmt(100 * (1 - distinct_100 / 100), 0),
    "linear_pool_slope": fmt(lin, 2),
    "quad_pool_slope": fmt(quad, 2),
    "quad_over_oracle": fmt(quad_1000 / float(s1.tail_mass(1_000)), 2),
    "linear_pool_used_1000": fmt(np.mean([len(pool_selector(s1, 1_000, 10_000,
                                                             np.random.default_rng(16_300 + k)))
                                          for k in range(20)]), 0),
    "uniform_err_1000": fmt(s1.expected_error(1_000).mid, 4),
    "oracle_err_1000": fmt(float(s1.tail_mass(1_000)), 5),
})
