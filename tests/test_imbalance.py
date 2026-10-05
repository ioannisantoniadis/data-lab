"""Claim tests: Part III, imbalance, prior shift and SMOTE (SPEC §8 claims 10, 11, 36, 37; T1)."""

import numpy as np
import pytest

from data_lab.sampling import (
    em_experiment,
    imbalance_experiment,
    prior_shift_correct,
    smote,
    smote_gap_experiment,
)


@pytest.fixture(scope="module")
def imbalance():
    return imbalance_experiment()


def test_prior_shift_correction_restores_calibration(imbalance):
    """Claim 10. Training on balanced data, by undersampling or by class weights, shifts the
    predicted probabilities: on rare-event T1 (5% positives) their mean distance from the true
    posterior rises more than 50-fold; the prior-shift correction
    p(y | x) proportional to q(y | x) p(y) / q(y) restores it to within 2x of the plain model's
    (30 seeds)."""
    plain = imbalance["plain"].mean()
    for name in ("under", "weighted"):
        assert imbalance[name].mean() > 50 * plain
        assert imbalance[f"{name}_corrected"].mean() < 2 * plain


def test_resampling_and_reweighting_share_a_target_not_a_variance(imbalance):
    """Claim 36 (added in Phase 3 for chapter 8). Balanced undersampling (q) and balanced class
    weights (w) aim at the same tilted posterior, so their coefficients agree on average (both
    within 0.05 of the true 1.5), but undersampling discards data and its estimates vary more
    across seeds (standard deviation at least 1.2 times larger; 30 seeds)."""
    under, weighted = imbalance["under_coef"], imbalance["weighted_coef"]
    assert abs(under.mean() - 1.5) < 0.05 and abs(weighted.mean() - 1.5) < 0.05
    assert under.std(ddof=1) > 1.2 * weighted.std(ddof=1)


def test_prior_shift_correction_matches_bayes_rule():
    """Saerens et al. eq. 4 for two classes, checked against Bayes' rule on a worked case."""
    eta_train = np.array([0.5, 0.9, 0.1])  # posteriors under a training prior of 0.5
    corrected = prior_shift_correct(eta_train, 0.5, 0.2)
    odds = eta_train / (1 - eta_train) * (0.2 / 0.8) / (0.5 / 0.5)
    np.testing.assert_allclose(corrected, odds / (1 + odds))


def test_em_prior_estimation_recovers_test_prior():
    """Claim 11. EM prior estimation (Saerens et al. 2002, eq. 9) on unlabeled new data
    recovers a known new prior of 0.1 from a model trained at 0.5: the mean estimate over 20
    seeds is within 0.01, and every estimate within 0.04."""
    est = em_experiment()
    assert abs(est.mean() - 0.1) < 0.01
    assert np.all(np.abs(est - 0.1) < 0.04)


def test_smote_points_lie_on_segments_between_minority_neighbors():
    """SMOTE as specified by Chawla et al. (§4.2): every synthetic point lies on a segment
    between two minority examples."""
    rng = np.random.default_rng(37)
    x = rng.standard_normal((30, 2))
    syn = smote(x, 200, 5, rng)
    for p in syn:
        a = x[:, None, :] - p  # vectors from p to each pair's endpoints
        b = x[None, :, :] - p
        cross = a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]  # zero if p, x_i, x_j collinear
        between = (a * b).sum(axis=2) <= 1e-12  # and p lies between them
        assert np.any((np.abs(cross) < 1e-9) & between & ~np.eye(30, dtype=bool))


def test_smote_fills_the_gap_when_k_exceeds_cluster_size():
    """Claim 37 (added in Phase 3 for chapter 8). With 20 minority examples in two separated
    clusters, SMOTE with k up to 5 neighbors puts no more synthetic mass in the gap between them
    than the true minority distribution has (2.3%); with k = 15, larger than a cluster, it puts
    over six times as much there (50 seeds)."""
    ks, shares, true_share = smote_gap_experiment(ks=(1, 3, 5, 15))
    mean = shares.mean(axis=0)
    assert np.all(mean[:3] < true_share)
    assert mean[3] > 6 * true_share


def test_balanced_threshold_at_one_half_is_the_prior_threshold():
    """Derived in chapter 8: a model trained with balanced classes (training prior 1/2) that
    thresholds its output at 1/2 makes the same decisions as the plain posterior thresholded at
    the true prior P, because by Bayes' rule the balanced posterior exceeds 1/2 exactly when
    eta > P."""
    eta = np.linspace(0.001, 0.999, 9_991)
    for prior in (0.01, 0.05, 0.3):
        balanced = prior_shift_correct(eta, prior, 0.5)  # what a balanced model learns
        np.testing.assert_array_equal(balanced > 0.5, eta > prior)


def test_king_zeng_intercept_correction_equals_saerens_for_logit():
    """For a logistic model, King & Zeng's prior correction (subtract
    ln[((1 - tau) / tau) (ybar / (1 - ybar))] from the intercept; 2001, eq. 7) gives exactly
    the posterior of Saerens et al.'s eq. 4 with training prior ybar and target prior tau."""
    from scipy.special import expit

    score = np.linspace(-6, 6, 101)  # logit of the model trained on the sample
    for tau, ybar in ((0.05, 0.5), (0.01, 0.2), (0.3, 0.6)):
        king_zeng = expit(score - np.log((1 - tau) / tau * ybar / (1 - ybar)))
        saerens = prior_shift_correct(expit(score), ybar, tau)
        np.testing.assert_allclose(king_zeng, saerens, rtol=1e-12)
