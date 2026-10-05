"""Claim tests: Part III, detecting distribution shift (claim 39, added in Phase 3 for
chapter 10; T1)."""

import numpy as np
import pytest
from scipy import stats

from data_lab.shift import classifier_two_sample_test, shift_detection_experiment
from data_lab.testbeds.t1_tabular import TabularGenerator


def test_classifier_two_sample_test_is_calibrated_under_no_shift():
    """With no shift, the classifier two-sample test's p-values are uniform: about 5% fall
    below 0.05 (400 seeds)."""
    gen = TabularGenerator(d=3, rho=0.3)
    p = []
    for s in range(400):
        rng = np.random.default_rng(50_000 + s)
        p.append(classifier_two_sample_test(gen.sample_z(500, rng), gen.sample_z(500, rng), rng))
    p = np.array(p)
    assert abs((p < 0.05).mean() - 0.05) < 0.03
    assert stats.kstest(p, "uniform").pvalue > 0.01


@pytest.fixture(scope="module")
def rates():
    return shift_detection_experiment()


def test_input_tests_detect_covariate_and_prior_shift_not_concept_shift(rates):
    """Claim 39. Tests that see only inputs (a classifier two-sample test; Bonferroni-corrected
    per-feature Kolmogorov-Smirnov tests; 500 examples per sample, level 0.05, 200 seeds) detect
    covariate shift with power rising in its size (above 0.85 at a shift of 0.3 standard
    deviations) and detect prior shift (above 0.5), but reject concept shift no more often than
    no shift (at most 0.1): its inputs are unchanged. A labeled check, the deployed model's
    accuracy on 500 labeled new examples, detects the concept shift (above 0.7) while staying
    near the level under no shift."""
    for test in (0, 1):
        powers = [rates[f"covariate {s}"][test] for s in (0.1, 0.2, 0.3)]
        assert powers[0] < powers[1] < powers[2] and powers[2] > 0.85
        assert rates["prior"][test] > 0.5
        assert rates["none"][test] <= 0.1 and rates["concept"][test] <= 0.1
    assert rates["concept"][2] > 0.7
    assert rates["none"][2] <= 0.1
