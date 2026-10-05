"""Scaling laws (chapter 12): a data-scaling curve whose irreducible loss is known exactly.

On the Markov text source T4, a bigram model with add-k smoothing is trained on D tokens. Its
expected per-token cross-entropy under the source is exact (MarkovSource.cross_entropy), and
its floor is the source's entropy rate. This makes visible what the published functional
forms assume:

- Kaplan et al. 2020, eq. 1.2: L(D) = (D_c / D)^alpha_D, a pure power law (no floor);
- Hoffmann et al. 2022, eq. 2: L(N, D) = E + A / N^alpha + B / D^beta, whose first term
  "should correspond to the entropy of natural text".

Fitting either form to small-D losses and extrapolating can be checked against the truth.
"""

from __future__ import annotations

import numpy as np

from data_lab.testbeds.t4_markov_text import MarkovSource, bigram_counts

SOURCE = MarkovSource(vocab=50, zipf_s=1.1, lam=0.7)


def bigram_loss(tokens: int, seed: int, smoothing: float = 0.1,
                source: MarkovSource = SOURCE) -> float:
    """Exact expected cross-entropy (nats per token) of an add-k bigram model trained on about
    ``tokens`` tokens (documents of up to 100 tokens)."""
    rng = np.random.default_rng(seed)
    n_docs = int(np.ceil(tokens / 100))
    docs = source.sample(n_docs, max(2, tokens // n_docs), rng)
    counts = bigram_counts(docs, source.vocab) + smoothing
    return source.cross_entropy(counts / counts.sum(axis=1, keepdims=True))


def data_scaling_curve(sizes, seeds: int = 10, source: MarkovSource = SOURCE) -> np.ndarray:
    return np.array([np.mean([bigram_loss(int(d), s, source=source) for s in range(seeds)])
                     for d in sizes])


def power_law(d, a, alpha):
    return a * np.asarray(d, dtype=float) ** (-alpha)


def power_law_with_floor(d, e, a, alpha):
    return e + a * np.asarray(d, dtype=float) ** (-alpha)


def fit_forms(sizes, losses):
    """Least-squares fits of the two forms; returns (pure params, floor params)."""
    from scipy.optimize import curve_fit

    pure, _ = curve_fit(power_law, sizes, losses, p0=[10.0, 0.1], maxfev=50_000)
    floor, _ = curve_fit(power_law_with_floor, sizes, losses,
                         p0=[losses.min(), 10.0, 0.5], maxfev=50_000)
    return pure, floor
