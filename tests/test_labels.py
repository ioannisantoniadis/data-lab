"""Claim tests: Part I, labels (claims 24-25, added in Phase 2 for chapter 2; T1)."""

import numpy as np
import pytest
from scipy.special import logit
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict

from data_lab.labels import (
    clean_threshold,
    confident_joint_issues,
    flip_labels,
    noisy_posterior,
)
from data_lab.testbeds.t1_tabular import TabularGenerator

GEN = TabularGenerator(d=3, rho=0.3)


def test_class_conditional_noise_moves_the_learned_boundary():
    """Claim 24. Under class-conditional noise (rho_0, rho_1), the noisy-label posterior is
    rho_0 + (1 - rho_0 - rho_1) eta(x): checked in bins of eta on 400,000 draws. A flexible
    model fit to noisy labels (isotonic regression on the score) therefore crosses 1/2 where
    eta = (1/2 - rho_0) / (1 - rho_0 - rho_1): the same boundary as the clean Bayes classifier
    when rho_0 = rho_1, a shifted one otherwise, whose clean risk exceeds the Bayes risk."""
    rng = np.random.default_rng(24)
    z = GEN.sample_z(400_000, rng)
    eta = GEN.posterior(z)
    y = GEN.sample_labels(z, rng)
    for rho0, rho1 in [(0.2, 0.2), (0.1, 0.3)]:
        noisy = flip_labels(y, rho0, rho1, rng)
        bins = np.digitize(eta, np.linspace(0.05, 0.95, 19))
        for b in np.unique(bins):
            sel = bins == b
            if sel.sum() < 2_000:
                continue
            expected = noisy_posterior(eta[sel], rho0, rho1).mean()
            se = np.sqrt(expected * (1 - expected) / sel.sum())
            assert abs(noisy[sel].mean() - expected) < 4.5 * se
        iso = IsotonicRegression(out_of_bounds="clip").fit(GEN.score(z), noisy)
        grid = np.linspace(-4, 4, 4_001)
        crossing = grid[np.argmax(iso.predict(grid) >= 0.5)]
        tau = clean_threshold(rho0, rho1)
        assert abs(crossing - logit(tau)) < 0.25
    assert clean_threshold(0.2, 0.2) == pytest.approx(0.5)
    assert GEN.threshold_risk(clean_threshold(0.1, 0.3)) > GEN.bayes_risk() + 0.02
    assert GEN.threshold_risk(0.5) == pytest.approx(GEN.bayes_risk(), abs=1e-8)


def _cl_precision(scale: float, seeds: int = 10) -> float:
    gen = TabularGenerator(d=3, rho=0.3, u=np.array([1.5, -1.0, 0.5]) * scale)
    precisions = []
    for s in range(seeds):
        rng = np.random.default_rng(25_000 + s)
        z = gen.sample_z(4_000, rng)
        y = gen.sample_labels(z, rng)
        noisy = flip_labels(y, 0.2, 0.2, rng)
        probs = cross_val_predict(
            LogisticRegression(C=np.inf), z, noisy, cv=4, method="predict_proba"
        )
        flagged = confident_joint_issues(noisy, probs)
        precisions.append(np.mean((noisy != y)[flagged]))
    return float(np.mean(precisions))


def test_confident_learning_precision_depends_on_separability():
    """Claim 25. Confident learning (CL method 2, out-of-sample probabilities from 4-fold cross
    validation) flags injected label flips with precision far above the 20% noise rate when the
    classes are separable, and barely above it when they overlap: mean precision over 10 seeds
    rises with separability and exceeds 0.9 at a Bayes risk near 0.08."""
    scales = [0.5, 1.0, 2.0, 4.0]
    precision = [_cl_precision(s) for s in scales]
    assert all(a < b for a, b in zip(precision, precision[1:], strict=False))
    assert precision[0] < 0.45 and precision[-1] > 0.9


def test_confident_joint_flags_exactly_the_off_diagonal_examples():
    """A hand-checkable case of the definition (Northcutt et al. 2021, eqs. 1-2)."""
    labels = np.array([0, 0, 0, 1, 1, 1])
    probs = np.array([[0.9, 0.1], [0.8, 0.2], [0.2, 0.8], [0.3, 0.7], [0.1, 0.9], [0.85, 0.15]])
    # t_0 = mean(0.9, 0.8, 0.2) = 0.633; t_1 = mean(0.7, 0.9, 0.15) = 0.583
    flagged = confident_joint_issues(labels, probs)
    np.testing.assert_array_equal(flagged, [False, False, True, False, False, True])
