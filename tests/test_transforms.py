"""Claim tests: Part II, shape-changing transforms (SPEC §8 claims 4-6 and 30; T1)."""

import numpy as np
import pytest
from scipy import stats
from scipy.spatial.distance import pdist
from sklearn.preprocessing import PowerTransformer, QuantileTransformer

from data_lab.sampling import ols
from data_lab.testbeds.t1_tabular import TabularGenerator
from data_lab.transforms import box_cox_sample, smearing_predict


def _log_target_run(gen, seed):
    rng = np.random.default_rng(seed)
    z = gen.sample_z(20_000, rng)
    log_y = np.log(gen.sample_y(z, rng))
    coef = ols(z, log_y)
    residuals = log_y - (coef[0] + z @ coef[1:])
    z_new = gen.sample_z(20_000, rng)
    pred = coef[0] + z_new @ coef[1:]
    return z_new, np.exp(pred), smearing_predict(pred, residuals)


def test_log_target_mse_predicts_geometric_mean():
    """Claim 4. With MSE on log y, back-transformed predictions estimate exp(E[log y | x]) (the
    conditional geometric mean and, for log-normal noise, the median); for log-normal noise this
    underestimates E[y | x] by the factor exp(-sigma_eps^2 / 2); the smearing estimate removes
    the gap when the noise does not depend on x (T1, sigma_eps = 0.8, 10 seeds)."""
    gen = TabularGenerator(d=3, rho=0.3, sigma0=0.8)
    factor = np.exp(-0.8**2 / 2)
    for s in range(10):
        z_new, naive, smeared = _log_target_run(gen, 4_000 + s)
        assert np.mean(naive / gen.conditional_geometric_mean(z_new)) == pytest.approx(1, abs=0.01)
        assert np.mean(naive / gen.conditional_mean(z_new)) == pytest.approx(factor, abs=0.01)
        assert np.mean(smeared / gen.conditional_mean(z_new)) == pytest.approx(1, abs=0.025)


def test_smearing_fails_under_heteroscedastic_noise():
    """Claim 31 (added in Phase 2 for chapter 6). When the log-scale noise grows with z_1
    (gamma = 0.5), a single smearing factor overstates E[y | x] where the noise is small,
    relative to where it is large, by a factor above 2 in every one of 10 seeds; and the factor
    itself, an average of exponentiated heavy-tailed residuals, varies across seeds (coefficient
    of variation above 0.3, against below 0.01 with constant noise)."""
    for gamma, cv_bound in ((0.0, None), (0.5, 0.3)):
        gen = TabularGenerator(d=3, rho=0.3, sigma0=0.8, gamma=gamma)
        region_ratio, factor = [], []
        for s in range(10):
            z_new, naive, smeared = _log_target_run(gen, 4_100 + s)
            ratio = smeared / gen.conditional_mean(z_new)
            region_ratio.append(ratio[z_new[:, 0] < -0.5].mean() / ratio[z_new[:, 0] > 0.5].mean())
            factor.append(np.mean(smeared / naive))
        cv = np.std(factor) / np.mean(factor)
        if cv_bound is None:
            assert cv < 0.01 and max(abs(np.array(region_ratio) - 1)) < 0.05
        else:
            assert cv > cv_bound and min(region_ratio) > 2


@pytest.mark.parametrize("lam", [-1.0, -0.5, 0.0, 0.5, 1.5])
def test_box_cox_mle_recovers_known_lambda(lam):
    """Claim 5. Box-Cox lambda by maximum likelihood (scipy.stats.boxcox, which maximizes the
    profile log-likelihood of scipy.stats.boxcox_llf) recovers a known lambda: mean over 50
    seeds within 0.05, on data constructed so that the true transform is exactly normal; and
    PowerTransformer(method="box-cox") finds the same lambda."""
    estimates = []
    for s in range(50):
        y = box_cox_sample(lam, 2_000, np.random.default_rng(500 + s))
        _, lam_hat = stats.boxcox(y)
        estimates.append(lam_hat)
    assert np.mean(estimates) == pytest.approx(lam, abs=0.05)
    y = box_cox_sample(lam, 2_000, np.random.default_rng(500))
    pt = PowerTransformer(method="box-cox").fit(y[:, None])
    assert pt.lambdas_[0] == pytest.approx(stats.boxcox(y)[1], abs=1e-4)


def test_quantile_transform_changes_distances_preserves_ranks():
    """Claim 6. A quantile transform to uniform preserves the ranks within each feature
    (Spearman correlation 1) but is not distance-preserving: pairwise Euclidean distances
    after the transform correlate only weakly with those before (below 0.7 on log-normal data,
    against 1 for any common rescaling)."""
    rng = np.random.default_rng(6)
    x = np.exp(rng.standard_normal((2_000, 2)))
    q = QuantileTransformer(random_state=0).fit_transform(x)
    for j in range(2):
        assert stats.spearmanr(x[:, j], q[:, j]).statistic == pytest.approx(1.0)
    d_before, d_after = pdist(x[:300]), pdist(q[:300])
    assert np.corrcoef(d_before, d_after)[0, 1] < 0.7
    assert np.corrcoef(d_before, pdist(3 * x[:300]))[0, 1] == pytest.approx(1.0)


def test_quantile_transform_clips_values_beyond_the_training_range():
    """Claim 30 (added in Phase 2 for chapter 6). QuantileTransformer maps new values beyond
    the fitted range to the bounds of the output distribution (scikit-learn 1.9 docstring), so
    every value above the training maximum gets the same output: it cannot extrapolate."""
    rng = np.random.default_rng(7)
    x = np.exp(rng.standard_normal((1_000, 1)))
    qt = QuantileTransformer(n_quantiles=1_000).fit(x)
    beyond = np.array([[x.max() * 2], [x.max() * 100]])
    out = qt.transform(beyond)[:, 0]
    assert out[0] == out[1] == pytest.approx(1.0)


def test_yeo_johnson_extends_box_cox_to_zero_and_negative_values():
    """Yeo-Johnson (scipy.stats.yeojohnson, formula in its docstring): for x >= 0 it equals the
    Box-Cox transform of x + 1, and it is defined, increasing and finite for negative x, where
    Box-Cox is undefined."""
    rng = np.random.default_rng(8)
    x = np.abs(rng.standard_normal(500)) * 3
    for lam in (-0.5, 0.0, 0.7, 2.0):
        np.testing.assert_allclose(stats.yeojohnson(x, lam), stats.boxcox(x + 1, lam),
                                   rtol=1e-12)
    xs = np.sort(rng.standard_normal(500) * 3)
    out = stats.yeojohnson(xs, 0.5)
    assert np.all(np.isfinite(out)) and np.all(np.diff(out) > 0)
    with pytest.raises(ValueError):
        stats.boxcox(xs)
