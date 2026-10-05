"""Claim tests: Part II, affine scaling (SPEC §8 claims 1, 21 and 29; T1). The scikit-learn
transformers are exercised, not re-implemented (SPEC §12.5)."""

import numpy as np
import pytest
from scipy import stats
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, RobustScaler, StandardScaler

from data_lab.testbeds.t1_tabular import TabularGenerator
from data_lab.transforms import contaminate, least_squares_condition

SCALERS = [StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler]


@pytest.mark.parametrize("scaler", SCALERS)
def test_affine_scalers_preserve_skewness_and_kurtosis(scaler):
    """Claim 1. Standard, min-max, max-abs and robust scaling leave sample skewness and kurtosis
    unchanged (affine invariance), on T1's log-normal (skewed) features."""
    gen = TabularGenerator(d=3, rho=0.3, skewed=True)
    x = gen.features(gen.sample_z(5_000, np.random.default_rng(1)))
    out = scaler().fit_transform(x)
    np.testing.assert_allclose(stats.skew(out), stats.skew(x), rtol=1e-9)
    np.testing.assert_allclose(stats.kurtosis(out), stats.kurtosis(x), rtol=1e-9)
    # and it really is affine per feature: a straight line through (x, out) for each column
    for j in range(x.shape[1]):
        slope, intercept = np.polyfit(x[:, j], out[:, j], 1)
        np.testing.assert_allclose(out[:, j], slope * x[:, j] + intercept, atol=1e-9)
        assert slope > 0


def test_feature_scaling_changes_least_squares_conditioning():
    """Claim 21. Per-feature rescaling changes the condition number of the least-squares
    Hessian (proportional to D'D), and standardization reduces it on a constructed T1 case:
    features on scales 1, 100 and 0.01, one offset by 50."""
    gen = TabularGenerator(d=3, rho=0.3)
    z = gen.sample_z(5_000, np.random.default_rng(21))
    raw = z * np.array([1.0, 100.0, 0.01]) + np.array([50.0, 0.0, 0.0])
    assert least_squares_condition(raw) > 1e7
    standardized = StandardScaler().fit_transform(raw)
    assert least_squares_condition(standardized) < 3
    # Standardizing removes the scales entirely: the result equals standardizing z itself.
    assert least_squares_condition(standardized) == pytest.approx(
        least_squares_condition(StandardScaler().fit_transform(z)), rel=1e-9
    )


def test_robust_scaler_keeps_inlier_spread_under_outliers():
    """Claim 29 (added in Phase 2 for chapter 5). With 1% gross outliers at 100 standard
    deviations, StandardScaler compresses the inliers to a spread of about 0.1, while
    RobustScaler (median and interquartile range) keeps them near 1 / IQR(N(0, 1)) = 0.741;
    without outliers both give inlier spreads within 0.03 of their clean values."""
    rng = np.random.default_rng(29)
    clean = rng.standard_normal(20_000)
    dirty, outlier = contaminate(clean, 0.01, 100.0, rng)
    iqr_normal = stats.norm.ppf(0.75) - stats.norm.ppf(0.25)
    spread = {}
    for scaler in (StandardScaler, RobustScaler):
        for name, data in (("clean", clean), ("dirty", dirty)):
            out = scaler().fit_transform(data[:, None])[:, 0]
            spread[scaler.__name__, name] = out[~outlier].std()
    assert spread["StandardScaler", "clean"] == pytest.approx(1.0, abs=0.03)
    assert spread["StandardScaler", "dirty"] < 0.15
    assert spread["RobustScaler", "clean"] == pytest.approx(1 / iqr_normal, abs=0.03)
    assert spread["RobustScaler", "dirty"] == pytest.approx(1 / iqr_normal, abs=0.03)
