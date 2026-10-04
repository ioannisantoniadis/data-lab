"""Signature figure (SPEC §9): the long tail on Hutter's model (T2).

Panel A: exact expected error E_n of the memorizing learner under uniform sampling, for three
Zipf exponents alpha, with Monte Carlo means (200 seeds) on top and the asymptote
c n^-alpha/(1+alpha) as a guide.

Panel B (alpha = 1): at equal labeled budget n, uniform sampling (exact), the oracle coverage
selector that labels features 1..n (exact), and a selector that knows nothing about p: it sees
an unlabeled pool of M draws and labels the n distinct features counted most often. Pools of
M = 10 n and 100 n, and M = n^2 = n^(1+alpha); median and 10-90% band over seeds.

This figure makes visible that uniform sampling's error falls as a power law set by the tail
(slope -alpha/(1+alpha)), and that selecting for coverage steepens that power law (to -alpha)
but does not escape it, and only an oracle or an unlabeled pool growing like n^(1+alpha) buys
the steeper slope: a pool proportional to n only shifts the uniform line down.

Run: uv run python scripts/figures/fig_long_tail_signature.py   (about 30 s on a laptop CPU)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import (  # noqa: E402
    INK,
    INK_SECONDARY,
    LEVER_COLOR,
    MUTED,
    SEQUENTIAL_BLUE,
    apply_theme,
    save_figure,
)

from data_lab.testbeds.t2_zipf import ZipfStream, pool_selector, uniform_selector  # noqa: E402

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
ax_a.set_xlim(1, 3e8)
ax_a.set_ylim(1.5e-5, 1.5)
ax_a.set_xlabel("training examples $n$ (uniform sampling from $p$)")
ax_a.set_ylabel("expected test error")
ax_a.set_title("A. The tail sets a power law")

# --- Panel B ------------------------------------------------------------------------------------
stream = ZipfStream(1.0)
ns = np.unique(np.logspace(np.log10(30), np.log10(2_000), 7).round()).astype(int)
uniform = np.array([stream.expected_error(n).mid for n in ns])
oracle = stream.tail_mass(ns)
ax_b.loglog(ns, uniform, color=INK_SECONDARY, lw=2.0)
ax_b.loglog(ns, oracle, color=INK, lw=2.0, ls=(0, (6, 2)))

pools = [
    ("pool $M = 10\\,n$", lambda n: 10 * n, 60, (0, (1, 1.5))),
    ("pool $M = 100\\,n$", lambda n: 100 * n, 40, (0, (5, 2))),
    ("pool $M = n^2$", lambda n: n * n, 12, "-"),
]
pool_end = {}
for label, size, seeds, style in pools:
    rng = np.random.default_rng(SEED + seeds)
    runs = np.array(
        [
            [stream.memorizer_error(pool_selector(stream, n, size(n), rng)) for n in ns]
            for _ in range(seeds)
        ]
    )
    lo, med, hi = np.percentile(runs, [10, 50, 90], axis=0)
    ax_b.fill_between(ns, lo, hi, color=LEVER_COLOR["q"], alpha=0.15, lw=0)
    ax_b.loglog(ns, med, color=LEVER_COLOR["q"], lw=2.0, ls=style, marker="o", ms=4)
    pool_end[label] = med[-1]

labels = {
    "uniform: $q = p$": uniform[-1],
    "oracle: features $1..n$": oracle[-1],
    **pool_end,
}
for text, y in labels.items():
    ax_b.annotate(text, xy=(ns[-1], y), xytext=(6, 0), textcoords="offset points",
                  va="center", fontsize=9.5, color=INK)
x0, x1 = ns[0], ns[-1]
ax_b.loglog([x0, x1], [2.2 * uniform[0], 2.2 * uniform[0] * (x1 / x0) ** -0.5],
            color=MUTED, lw=0.8)
ax_b.annotate("slope $-1/2$", xy=(x0 * 1.3, 2.2 * uniform[0] * 1.3**-0.5), xytext=(0, 6),
              textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax_b.loglog([x0, x1], [0.45 * oracle[0], 0.45 * oracle[0] * (x1 / x0) ** -1.0],
            color=MUTED, lw=0.8)
ax_b.annotate("slope $-1$", xy=(x0 * 1.2, 0.45 * oracle[0] / 1.2), xytext=(0, -14),
              textcoords="offset points", fontsize=9, color=INK_SECONDARY)
ax_b.set_xlim(ns[0] * 0.8, ns[-1] * 9)
ax_b.set_xlabel("labeled examples $n$")
ax_b.set_ylabel(r"expected test error ($\alpha = 1$)")
ax_b.set_title("B. Coverage steepens it, at a price")

save_figure(fig, "long_tail_signature")
