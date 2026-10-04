"""T1 ground truths, each checked against an independent reference (SciPy's lognorm, numerical
integration, or Monte Carlo over many draws)."""

import numpy as np
import pytest
from scipy import stats

from data_lab.testbeds.t1_tabular import (
    TabularGenerator,
    mar_mask,
    mar_probability,
    mcar_mask,
    mnar_mask,
)


@pytest.fixture
def gen():
    return TabularGenerator(d=3, rho=0.3, gamma=0.4)


def test_lognormal_truths_match_scipy_reference(gen):
    z = gen.sample_z(50, np.random.default_rng(0))
    m, s = gen.log_location(z), gen.noise_scale(z)
    ref = stats.lognorm(s=s, scale=np.exp(m))  # Y = exp(X), X ~ N(m, s)
    np.testing.assert_allclose(gen.conditional_mean(z), ref.mean(), rtol=1e-12)
    np.testing.assert_allclose(gen.conditional_median(z), ref.median(), rtol=1e-12)
    geo = [
        np.exp(stats.lognorm(s=si, scale=np.exp(mi)).expect(np.log))
        for mi, si in zip(m, s, strict=True)
    ]
    np.testing.assert_allclose(gen.conditional_geometric_mean(z), geo, rtol=1e-6)


def test_sampled_targets_have_the_stated_conditional_law(gen):
    """At one fixed z, many draws of y: mean and median within Monte Carlo error."""
    rng = np.random.default_rng(1)
    z = np.repeat(np.array([[0.4, -0.2, 1.0]]), 200_000, axis=0)
    y = gen.sample_y(z, rng)
    se = y.std() / np.sqrt(len(y))
    assert abs(y.mean() - gen.conditional_mean(z[:1])[0]) < 4 * se
    assert np.median(y) == pytest.approx(gen.conditional_median(z[:1])[0], rel=0.01)


def test_features_correlation_and_skew():
    rng = np.random.default_rng(2)
    g = TabularGenerator(d=3, rho=0.5)
    z = g.sample_z(100_000, rng)
    np.testing.assert_allclose(np.corrcoef(z.T)[0, 1], 0.5, atol=0.01)
    skewed = TabularGenerator(d=3, skewed=True).features(z)
    assert stats.skew(skewed[:, 0]) > 2 and np.all(skewed > 0)


def test_bayes_risk_matches_monte_carlo_of_the_bayes_classifier(gen):
    rng = np.random.default_rng(3)
    z = gen.sample_z(400_000, rng)
    y = gen.sample_labels(z, rng)
    err = np.mean((gen.posterior(z) > 0.5).astype(int) != y)
    se = np.sqrt(err * (1 - err) / len(y))
    assert abs(err - gen.bayes_risk()) < 4 * se
    assert abs(y.mean() - gen.prior()) < 4 * np.sqrt(0.25 / len(y))


def test_sample_with_prior_keeps_class_conditionals(gen):
    rng = np.random.default_rng(4)
    z, y = gen.sample_with_prior(20_000, 0.1, rng)
    assert y.sum() == 2_000
    # p(z | y = 1) is unchanged: compare with positives drawn the ordinary way.
    z_ref = gen.sample_z(200_000, rng)
    pos_ref = z_ref[gen.sample_labels(z_ref, rng) == 1]
    assert stats.ks_2samp(z[y == 1][:, 0], pos_ref[:, 0]).pvalue > 1e-3


def test_density_ratio_is_exact(gen):
    """E_q[w] = 1, E_q[w f] = E_p[f], and E_q[w^2] = exp(delta' Sigma^-1 delta)."""
    rng = np.random.default_rng(5)
    delta = np.array([0.5, 0.0, -0.3])
    zq = gen.sample_z(1_000_000, rng)
    w = gen.density_ratio(zq, delta)
    assert w.mean() == pytest.approx(1.0, abs=4 * w.std() / 1e3)
    zp = gen.sample_z(1_000_000, rng, shift=delta)
    f = lambda z: z[:, 0] ** 2 + z[:, 2]  # noqa: E731
    assert np.mean(w * f(zq)) == pytest.approx(np.mean(f(zp)), abs=0.01)
    assert np.mean(w**2) == pytest.approx(gen.density_ratio_second_moment(delta), rel=0.02)


def test_missingness_mechanisms_depend_on_what_they_should():
    rng = np.random.default_rng(6)
    g = TabularGenerator(d=3, rho=0.6)
    z = g.sample_z(400_000, rng)
    own, other = z[:, 0], z[:, 1]
    assert mcar_mask(len(z), 0.3, rng).mean() == pytest.approx(0.3, abs=0.005)
    mar = mar_mask(other, 0.3, 1.5, rng)
    # MAR: within a narrow band of the observed column, the rate does not depend on own value.
    band = np.abs(other) < 0.05
    lo, hi = band & (own < 0), band & (own >= 0)
    assert abs(mar[lo].mean() - mar[hi].mean()) < 0.03
    assert mar[band].mean() == pytest.approx(mar_probability(np.array([0.0]), 0.3, 1.5)[0],
                                             abs=0.02)
    # MNAR: within the same band, the rate does depend on the value that goes missing.
    mnar = mnar_mask(own, 0.3, 1.5, rng)
    assert mnar[hi].mean() - mnar[lo].mean() > 0.2
