"""T2: a Zipf feature stream with a memorizing learner (Hutter 2021, arXiv 2102.04074).

The setting (Hutter §2, read 2026-10-04): features i = 1, 2, ... are drawn i.i.d. with
probabilities p_i; each feature has one deterministic label; the learner memorizes the label of
every feature it has seen and errs on every feature it has not. Its expected error after n
uniform (i.i.d. from p) training draws is Hutter's eq. 2,

    E_n = sum_i p_i (1 - p_i)^n.

Notation: Hutter writes theta_i; this book writes p_i, because the feature distribution *is* the
target distribution p (docs/appendix-notation.qmd). Zipf data: p_i = i^-(alpha+1) / zeta(alpha+1)
on the infinite support i >= 1, so alpha > 0. Hutter shows E_n ~ c n^-alpha/(1+alpha).

Everything here is exact or exactly bracketed:

- ``tail_mass(n)`` = sum_{i>n} p_i = zeta(alpha+1, n+1) / zeta(alpha+1), with SciPy's Hurwitz
  zeta (two-argument ``scipy.special.zeta``, docstring read 2026-10-04: zeta(x, q) =
  sum_{k>=0} (k+q)^-x).
- ``expected_error(n)`` sums the first K terms directly and brackets the rest: for i > K,
  p_i (1 - n p_i) <= p_i (1 - p_i)^n <= p_i (Bernoulli's inequality), and both bracket sums are
  Hurwitz zetas. The result is a ``Bracket`` whose width is reported, never hidden.
- ``sample(m, rng)`` draws from ``numpy.random.Generator.zipf(alpha + 1)``, whose documented
  pmf is k^-a / zeta(a) (docstring read 2026-10-04): exact draws on the infinite support.

Selection on T2 (the SPEC §7 extension, derived in docs/appendix-testbeds.qmd):

- the *oracle* coverage selector labels features 1..n (most frequent first, never a repeat),
  so its error is ``tail_mass(n)``, between (n+1)^-alpha and n^-alpha over alpha zeta(alpha+1);
- a *pool* selector sees M unlabeled draws, ranks the distinct features by their count in the
  pool (ties broken at random, never by feature index, which would leak the oracle's
  ordering), and labels the top n. It never labels a feature absent from the pool, so its
  error is at least max(tail_mass(n), expected_error(M)).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.special import zeta

# Direct summation over the first K features, sized so that n * p_K <= _HEAD_TOLERANCE.
_HEAD_TOLERANCE = 1e-4
_K_MIN = 10_000
_K_MAX = 5_000_000


@dataclass(frozen=True)
class Bracket:
    """An exact quantity known to lie in [lower, upper]."""

    lower: float
    upper: float

    @property
    def mid(self) -> float:
        return 0.5 * (self.lower + self.upper)

    @property
    def width(self) -> float:
        return self.upper - self.lower


@dataclass(frozen=True)
class ZipfStream:
    """Hutter's toy model with Zipf-distributed features, p_i proportional to i^-(alpha+1)."""

    alpha: float

    def __post_init__(self) -> None:
        if not self.alpha > 0:
            raise ValueError("alpha must be positive (p_i ~ i^-(alpha+1) must be summable)")

    @property
    def s(self) -> float:
        """The Zipf exponent of p: p_i = i^-s / zeta(s), with s = alpha + 1."""
        return self.alpha + 1.0

    @property
    def normalizer(self) -> float:
        return float(zeta(self.s))

    @property
    def beta(self) -> float:
        """Hutter's learning-curve exponent for uniform sampling: alpha / (1 + alpha)."""
        return self.alpha / (1.0 + self.alpha)

    def p(self, i) -> np.ndarray:
        """Exact probabilities p_i for 1-based feature indices i."""
        i = np.asarray(i, dtype=float)
        return i ** (-self.s) / self.normalizer

    def tail_mass(self, n) -> np.ndarray:
        """sum_{i>n} p_i, exactly (Hurwitz zeta). The oracle coverage selector's error."""
        n = np.asarray(n, dtype=float)
        return zeta(self.s, n + 1.0) / self.normalizer

    def oracle_bounds(self, n) -> tuple[np.ndarray, np.ndarray]:
        """Integral bounds on tail_mass(n): ((n+1)^-a, n^-a) / (a zeta(a+1)), a = alpha."""
        n = np.asarray(n, dtype=float)
        c = 1.0 / (self.alpha * self.normalizer)
        return c * (n + 1.0) ** (-self.alpha), c * n ** (-self.alpha)

    def _head_size(self, n: float) -> int:
        k = (n / (_HEAD_TOLERANCE * self.normalizer)) ** (1.0 / self.s)
        return int(min(max(np.ceil(k), _K_MIN), _K_MAX))

    def expected_error(self, n: float) -> Bracket:
        """Hutter's E_n = sum_i p_i (1 - p_i)^n for uniform sampling, exactly bracketed."""
        if n < 0:
            raise ValueError("n must be non-negative")
        k = self._head_size(n)
        p = self.p(np.arange(1, k + 1))
        head = float(np.sum(p * np.exp(n * np.log1p(-p))))
        t1 = float(zeta(self.s, k + 1.0)) / self.normalizer
        t2 = float(zeta(2.0 * self.s, k + 1.0)) / self.normalizer**2
        return Bracket(lower=head + max(t1 - n * t2, 0.0), upper=head + t1)

    def expected_distinct(self, m: float) -> Bracket:
        """Expected number of distinct features in m draws: sum_i 1 - (1 - p_i)^m, bracketed.

        For i > K: m p_i - C(m, 2) p_i^2 <= 1 - (1 - p_i)^m <= m p_i (Bonferroni).
        """
        k = self._head_size(m)
        p = self.p(np.arange(1, k + 1))
        head = float(np.sum(-np.expm1(m * np.log1p(-p))))
        t1 = float(zeta(self.s, k + 1.0)) / self.normalizer
        t2 = float(zeta(2.0 * self.s, k + 1.0)) / self.normalizer**2
        return Bracket(lower=head + max(m * t1 - 0.5 * m * (m - 1) * t2, 0.0), upper=head + m * t1)

    def sample(self, m: int, rng: np.random.Generator) -> np.ndarray:
        """m i.i.d. feature indices from p (exact, infinite support)."""
        return rng.zipf(self.s, size=m)

    def memorizer_error(self, seen) -> float:
        """Error of the memorizing learner that has labels for the features in ``seen``:
        the p-mass of every feature it has not seen, 1 - sum over distinct seen of p_i."""
        distinct = np.unique(np.asarray(seen))
        return float(max(1.0 - np.sum(self.p(distinct)), 0.0))


def uniform_selector(stream: ZipfStream, n: int, rng: np.random.Generator) -> np.ndarray:
    """Label n i.i.d. draws from p: ordinary training data. Repeats waste labels."""
    return stream.sample(n, rng)


def oracle_selector(n: int) -> np.ndarray:
    """Label features 1..n: knows which features are covered *and* their frequency order."""
    return np.arange(1, n + 1)


def pool_selector(
    stream: ZipfStream, n: int, pool_size: int, rng: np.random.Generator
) -> np.ndarray:
    """See ``pool_size`` unlabeled draws; label the n distinct features most counted in the pool.

    No knowledge of p: frequency is estimated from pool counts, and ties are broken at random
    (breaking them by feature index would smuggle in the oracle's ordering). If the pool has
    fewer than n distinct features, all of them are labeled and the rest of the budget is
    unusable: the selector cannot label what it has not seen.
    """
    features, counts = np.unique(stream.sample(pool_size, rng), return_counts=True)
    order = np.lexsort((rng.random(features.size), -counts))
    return features[order[:n]]
