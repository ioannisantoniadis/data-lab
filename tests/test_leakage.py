"""Claim tests: Part II, leakage (SPEC §8 claims 8, 9 and 28)."""

import numpy as np

from data_lab.cleaning import (
    duplicate_experiment,
    supervised_selection_leak,
    unsupervised_fit_gap,
)
from data_lab.testbeds.t1_tabular import TabularGenerator
from data_lab.transforms import target_encoding_experiment


def test_target_encoding_without_cross_fitting_leaks():
    """Claim 8. Target encoding without cross-fitting gives a pure-noise high-cardinality
    feature a large training score and no test advantage: training accuracy rises well above
    the model without it, test accuracy falls below it, and the model puts a large weight on
    noise. Cross-fitting (TargetEncoder.fit_transform) removes the gap: train and test accuracy
    match the model without the feature (20 seeds, T1 plus a 1,000-level noise category)."""
    res = target_encoding_experiment()
    none, naive, cross = (res[k].mean(axis=0) for k in ("none", "naive", "crossfit"))
    assert naive[0] - none[0] > 0.05  # training score inflated
    assert naive[1] < none[1] - 0.05  # and worse on new data
    assert abs(naive[2]) > 2
    assert abs(cross[0] - none[0]) < 0.01 and abs(cross[1] - none[1]) < 0.01
    assert abs(cross[2]) < 0.5


def test_fitting_preprocessing_on_test_is_optimistic():
    """Claim 9 (restated in Phase 2; SPEC v0.1 said any scaler or imputer fit on train + test
    is optimistic, which the evidence does not support). Unsupervised steps (a scaler or an
    imputer) fit on train + test change i.i.d. test accuracy by under one point and not
    consistently upward (200 seeds, kNN and regularized logistic regression). A supervised step
    fit on all data (feature selection on pure-noise labels) reports accuracy far above chance
    (above 0.7 against a true 0.5), while the same step inside the cross-validation folds
    reports chance."""
    for model in ("knn", "logreg"):
        for prep in ("std", "minmax", "impute"):
            assert abs(unsupervised_fit_gap(prep, model).mean()) < 0.01
    leaky, clean = supervised_selection_leak().T
    assert np.mean(leaky) > 0.7
    assert abs(np.mean(clean) - 0.5) < 0.05


def test_train_test_duplicates_inflate_the_test_score():
    """Claim 28 (added in Phase 2 for chapter 4). When 30% of the test rows duplicate training
    rows, a 1-nearest-neighbor classifier's test accuracy rises above the Bayes accuracy, which
    no classifier can exceed on fresh data; removing the overlapping rows removes the excess
    (20 seeds, T1)."""
    rows = duplicate_experiment(0.3)
    bayes_accuracy = 1 - TabularGenerator(d=3, rho=0.3).bayes_risk()
    assert rows[:, 0].mean() > bayes_accuracy
    assert rows[:, 1].mean() < bayes_accuracy
