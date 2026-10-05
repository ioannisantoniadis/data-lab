"""Claim tests: Part I, the data-generating process (claims 22-23, added in Phase 2 for
chapter 1; T1)."""

import numpy as np

from data_lab.sampling import (
    keep_on_x,
    keep_on_y,
    keep_on_y_probability,
    ols,
    stratified_sample,
)
from data_lab.testbeds.t1_tabular import TabularGenerator

SEEDS = 200


def _slopes_and_means(mechanism):
    gen = TabularGenerator(d=3, rho=0.3, sigma0=0.6)
    slopes, means = [], []
    for s in range(SEEDS):
        rng = np.random.default_rng(22_000 + s)
        z = gen.sample_z(4_000, rng)
        log_y = np.log(gen.sample_y(z, rng))
        keep = {
            "random": rng.random(len(z)) < 0.5,
            "on_x": keep_on_x(z, 2.0, rng),
            "on_y": keep_on_y(log_y, 2.0, rng),
        }[mechanism]
        slopes.append(ols(z[keep], log_y[keep])[1])
        means.append(log_y[keep].mean())
    return gen, np.array(slopes), np.array(means)


def test_selection_on_x_keeps_the_conditional_selection_on_y_biases_it():
    """Claim 22. Selection that depends only on x leaves p(y | x) unchanged: a well-specified
    regression on the kept sample recovers the true coefficient (mean over 200 seeds within 4
    standard errors), while the sample mean of the target is biased. Selection that depends on
    y biases the coefficient."""
    gen = TabularGenerator(d=3, rho=0.3, sigma0=0.6)
    true_slope = gen.b[0]
    population_mean = gen.a  # E[log y] = a + b . E[z] = a
    for mech in ("random", "on_x"):
        _, slopes, means = _slopes_and_means(mech)
        se = slopes.std(ddof=1) / np.sqrt(SEEDS)
        assert abs(slopes.mean() - true_slope) < 4 * se, mech
    _, _, means_x = _slopes_and_means("on_x")
    assert abs(means_x.mean() - population_mean) > 10 * means_x.std(ddof=1) / np.sqrt(SEEDS)
    _, slopes_y, _ = _slopes_and_means("on_y")
    se_y = slopes_y.std(ddof=1) / np.sqrt(SEEDS)
    assert abs(slopes_y.mean() - true_slope) > 10 * se_y


def test_stratified_sampling_lowers_the_variance_of_the_mean():
    """Claim 23. A proportionally allocated stratified sample estimates the population mean
    with lower variance than a simple random sample of the same size when stratum means differ,
    close to the ratio sum_h W_h S_h^2 / S^2 (finite-population corrections ignored)."""
    rng = np.random.default_rng(23)
    gen = TabularGenerator(d=3, rho=0.3, sigma0=0.6)
    z = gen.sample_z(20_000, rng)
    target = np.log(gen.sample_y(z, rng))
    strata = np.digitize(z[:, 0], np.quantile(z[:, 0], [0.25, 0.5, 0.75]))
    n, reps = 200, 3_000
    srs = [target[rng.choice(len(target), n, replace=False)].mean() for _ in range(reps)]
    strat = [target[stratified_sample(strata, n, rng)].mean() for _ in range(reps)]
    ratio = np.var(strat) / np.var(srs)
    weights = np.bincount(strata) / len(strata)
    within = np.array([target[strata == h].var() for h in range(4)])
    predicted = (weights * within).sum() / target.var()
    assert ratio < 1
    assert abs(ratio - predicted) < 0.1


def test_known_selection_probabilities_undo_selection_on_y():
    """Claim 22, second part (added after the Phase 2 audit). When the selection probability
    s(x, y) is known, weighting each kept example by 1 / s restores the regression under p,
    even for selection on y, but slowly: the largest weights grow with n. At n = 4,000 the
    weighted coefficient removes most of the bias (within 0.03 of the truth, against 0.13
    unweighted; 200 seeds); at n = 256,000 it is unbiased within 4 standard errors (20 seeds)."""
    gen = TabularGenerator(d=3, rho=0.3, sigma0=0.6)

    def weighted_slopes(n, seeds):
        slopes = []
        for s in range(seeds):
            rng = np.random.default_rng(22_500 + s)
            z = gen.sample_z(n, rng)
            log_y = np.log(gen.sample_y(z, rng))
            prob = keep_on_y_probability(log_y, 2.0)
            keep = rng.random(n) < prob
            slopes.append(ols(z[keep], log_y[keep], weights=1.0 / prob[keep])[1])
        return np.array(slopes)

    small = weighted_slopes(4_000, SEEDS)
    assert abs(small.mean() - gen.b[0]) < 0.03
    large = weighted_slopes(256_000, 20)
    assert abs(large.mean() - gen.b[0]) < 4 * large.std(ddof=1) / np.sqrt(20)
