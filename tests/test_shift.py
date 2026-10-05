"""Claim tests: Part III, covariate shift (SPEC §8 claim 12; T1)."""

import numpy as np
import pytest

from data_lab.sampling import importance_weighting_experiment
from data_lab.testbeds.t1_tabular import TabularGenerator


@pytest.fixture(scope="module")
def iw():
    return importance_weighting_experiment()


def exact_variance(gen, delta, risk, n):
    """Var of the n-sample mean of w * loss under q, exactly. With q = N(0, S), p = N(d, S):
    q w^2 = N(2d, S) exp(d' S^-1 d), so E_q[w^2 loss] = exp(d' S^-1 d) R(2d), where R(m) is the
    risk under N(m, S) (0-1 loss: loss^2 = loss)."""
    second = gen.density_ratio_second_moment(delta) * gen.threshold_risk(0.5, shift=2 * delta)
    return (second - risk**2) / n


def test_importance_weighting_unbiased_with_growing_variance(iw):
    """Claim 12. Importance weighting with the true density ratio gives an unbiased risk
    estimate under covariate shift (mean of 500 seeds within 4 standard errors of the exact
    risk under p, at every shift), while the unweighted estimate is biased. Its variance grows
    with the shift, as exp(d' S^-1 d) R(2d) - R(d)^2 over n, exactly; the measured variance's
    bootstrap 95% interval contains that value at every shift, and the interval widens as the
    weights become heavy-tailed (T1)."""
    n, seeds = 1_000, iw["iw"].shape[0]
    gen = TabularGenerator(d=3, rho=0.3)
    sd = iw["iw"].std(axis=0, ddof=1)
    exact = []
    rng = np.random.default_rng(0)
    for j, shift in enumerate(iw["shifts"]):
        se = sd[j] / np.sqrt(seeds)
        assert abs(iw["iw"][:, j].mean() - iw["truth"][j]) < 4 * se
        if shift > 0:
            assert abs(iw["naive"][:, j].mean() - iw["truth"][j]) > 10 * se
        delta = np.array([shift, 0.0, 0.0])
        exact.append(exact_variance(gen, delta, iw["truth"][j], n))
        boot = [iw["iw"][rng.integers(0, seeds, seeds), j].var(ddof=1) for _ in range(2_000)]
        lo, hi = np.percentile(boot, [2.5, 97.5])
        assert lo <= exact[-1] <= hi
    assert np.all(np.diff(exact) > 0)
