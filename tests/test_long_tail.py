"""Claim tests: Part IV, Hutter's model and coverage-driven selection (SPEC §8 claims 14-16; T2).

Exact quantities come from ``ZipfStream`` (exact sums with a reported bracket, Hurwitz zetas);
Monte Carlo quantities are means over independent seeds, compared within a stated number of
standard errors. The derivation behind claim 16 is in docs/appendix-testbeds.qmd.
"""

import numpy as np
import pytest
from scipy.special import gamma

from data_lab.testbeds.t2_zipf import (
    ZipfStream,
    oracle_selector,
    pool_selector,
    uniform_selector,
)

ALPHAS = (0.5, 1.0, 2.0)


def _mc_mean(fn, seeds: int, base_seed: int):
    errors = np.array([fn(np.random.default_rng(base_seed + s)) for s in range(seeds)])
    return errors.mean(), errors.std(ddof=1) / np.sqrt(seeds)


def _slope(n1, e1, n2, e2):
    return np.log(e2 / e1) / np.log(n2 / n1)


# --- the exact machinery ----------------------------------------------------------------------


@pytest.mark.parametrize("alpha", ALPHAS)
def test_expected_error_bracket_is_tight(alpha):
    stream = ZipfStream(alpha)
    for n in (0, 10, 1_000, 1_000_000):
        b = stream.expected_error(n)
        assert 0 <= b.lower <= b.upper <= 1
        assert b.width <= 1e-5 * max(b.mid, 1e-12) + 1e-12
    assert stream.expected_error(0).mid == pytest.approx(1.0, abs=1e-9)


def test_tail_mass_matches_direct_partial_sums():
    stream = ZipfStream(2.0)  # fast-decaying tail: a direct sum to 10^6 is accurate to 1e-13
    i = np.arange(1, 1_000_001)
    p = stream.p(i)
    assert p.sum() == pytest.approx(1.0, abs=1e-11)
    for n in (0, 1, 5, 100):
        assert stream.tail_mass(n) == pytest.approx(p[n:].sum(), abs=1e-12)


# --- claim 14 ---------------------------------------------------------------------------------


@pytest.mark.parametrize("alpha", ALPHAS)
def test_hutter_exact_sum_matches_monte_carlo(alpha):
    """Claim 14. Hutter's exact sum E_n = sum_i p_i (1 - p_i)^n matches Monte Carlo simulation
    of the memorizing learner (T2): 400 seeds per (alpha, n), within 4 standard errors."""
    stream = ZipfStream(alpha)
    for n in (10, 100, 1_000):
        exact = stream.expected_error(n).mid
        mean, se = _mc_mean(
            lambda rng, n=n: stream.memorizer_error(uniform_selector(stream, n, rng)),
            seeds=400,
            base_seed=14_000 + n,
        )
        assert abs(mean - exact) < 4 * se, (alpha, n, mean, exact, se)


# --- claim 15 ---------------------------------------------------------------------------------


@pytest.mark.parametrize("alpha", ALPHAS)
def test_learning_curve_slope_approaches_hutter_exponent(alpha):
    """Claim 15. The log-log slope of E_n approaches -alpha/(1+alpha) on T2: the local slope
    over a decade gets closer to -beta as n grows, and is within 0.002 of it by 10^5..10^6."""
    stream = ZipfStream(alpha)
    ns = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
    errors = [stream.expected_error(n).mid for n in ns]
    gaps = [
        abs(_slope(ns[k], errors[k], ns[k + 1], errors[k + 1]) + stream.beta)
        for k in range(len(ns) - 1)
    ]
    assert gaps[-1] < 0.002
    assert gaps[-1] < gaps[0]


@pytest.mark.parametrize("alpha", ALPHAS)
def test_learning_curve_coefficient_for_normalized_zipf(alpha):
    """E_n n^beta -> A^(1/s) Gamma(beta) / s with A = 1/zeta(s), s = alpha + 1.

    Hutter's coefficient c_alpha = alpha^(1/(1+alpha)) Gamma(alpha/(1+alpha)) / (1+alpha) is
    derived for theta_i = alpha i^-(alpha+1); the same derivation (his eq. 4) with
    theta_i = A i^-s replaces alpha by A. This checks that generalization against the exact sum.
    """
    stream = ZipfStream(alpha)
    c = (1.0 / stream.normalizer) ** (1.0 / stream.s) * gamma(stream.beta) / stream.s
    n = 1_000_000
    assert stream.expected_error(n).mid * n**stream.beta == pytest.approx(c, rel=1e-3)


# --- claim 16 and the selection derivation ----------------------------------------------------


@pytest.mark.parametrize("alpha", ALPHAS)
def test_coverage_selection_beats_uniform_at_derived_rate(alpha):
    """Claim 16. The oracle coverage selector (labels features 1..n) has error
    sum_{i>n} p_i, inside the integral bounds ((n+1)^-alpha, n^-alpha) / (alpha zeta(alpha+1)),
    so its exponent is alpha, steeper than uniform's alpha/(1+alpha). It beats uniform
    sampling at every equal budget, and is still a power law."""
    stream = ZipfStream(alpha)
    ns = np.array([10, 100, 1_000, 10_000, 100_000])
    oracle = stream.tail_mass(ns)
    lo, hi = stream.oracle_bounds(ns)
    assert np.all(lo <= oracle) and np.all(oracle <= hi)
    uniform = np.array([stream.expected_error(n).mid for n in ns])
    assert np.all(oracle < uniform)
    assert abs(_slope(ns[-2], oracle[-2], ns[-1], oracle[-1]) + alpha) < 0.01
    # The oracle's error is exactly the memorizer's error on what it labels.
    for n in (10, 1_000):
        assert stream.memorizer_error(oracle_selector(n)) == pytest.approx(
            stream.tail_mass(n), abs=1e-12
        )


def test_pool_selector_is_bounded_by_unseen_pool_mass():
    """A selector that labels only features present in a pool of M unlabeled draws cannot beat
    max(oracle error at n, E_M): per draw of the pool, its error is at least the mass absent
    from the pool, and at least the mass beyond the n features it can label."""
    stream = ZipfStream(1.0)
    for n, pool in [(100, 1_000), (100, 10_000), (1_000, 100_000)]:
        bound = max(float(stream.tail_mass(n)), stream.expected_error(pool).mid)
        mean, se = _mc_mean(
            lambda rng, n=n, pool=pool: stream.memorizer_error(
                pool_selector(stream, n, pool, rng)
            ),
            seeds=200,
            base_seed=16_000 + pool,
        )
        assert mean > bound - 4 * se, (n, pool, mean, bound)


def test_linear_pool_keeps_the_uniform_exponent():
    """With a pool proportional to the budget (M = 10 n), the selector's error tracks E_{10n}:
    a constant-factor gain over uniform sampling, with uniform's exponent (-1/2 at alpha = 1)."""
    stream = ZipfStream(1.0)
    means = {}
    for n in (100, 1_000):
        means[n], _ = _mc_mean(
            lambda rng, n=n: stream.memorizer_error(pool_selector(stream, n, 10 * n, rng)),
            seeds=100,
            base_seed=16_100 + n,
        )
    assert abs(_slope(100, means[100], 1_000, means[1_000]) + stream.beta) < 0.05


def test_superlinear_pool_approaches_the_oracle_exponent():
    """With a pool growing as n^(1+alpha) (= n^2 at alpha = 1), the selector, which knows
    nothing about p, recovers the oracle's exponent (-1 at alpha = 1) to within 0.05."""
    stream = ZipfStream(1.0)
    means = {}
    for n in (100, 1_000):
        means[n], _ = _mc_mean(
            lambda rng, n=n: stream.memorizer_error(pool_selector(stream, n, n * n, rng)),
            seeds=20,
            base_seed=16_200 + n,
        )
    assert abs(_slope(100, means[100], 1_000, means[1_000]) + stream.alpha) < 0.05
    assert means[1_000] < 2 * float(stream.tail_mass(1_000))


def test_pool_selector_ties_are_not_broken_by_index():
    """With every pool count equal, the labeled subset must not favor small (frequent) indices,
    which would leak the oracle's ordering into a selector that is supposed not to know p."""

    class Flat(ZipfStream):
        def sample(self, m, rng):  # each of 1000 features exactly once
            return rng.permutation(np.arange(1, 1_001))[:m]

    picks = [pool_selector(Flat(1.0), 100, 1_000, np.random.default_rng(s)) for s in range(50)]
    mean_index = np.mean(np.concatenate(picks))
    assert 400 < mean_index < 600  # uniform over 1..1000 has mean 500.5
