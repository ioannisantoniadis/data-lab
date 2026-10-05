"""Claim tests: Part IV, learning curves (SPEC §8 claim 19; claims 40-41 added in Phase 3 for
chapter 11). Risks are exact on the linear-Gaussian task (src/data_lab/curves.py)."""

import numpy as np
import pytest

from data_lab.curves import (
    LinearGaussianTask,
    extrapolation_experiment,
    learning_curve,
    size_for_target,
)

TASK = LinearGaussianTask(d=10, sigma=1.0)


def test_learning_curve_falls_to_the_bayes_floor_scaled_by_noise_and_dimension():
    """Claim 40. The expected risk of least squares falls toward the Bayes risk sigma^2, never
    below it; the excess over the floor scales exactly as sigma^2 (same designs, same noise
    draws, noise scale doubled: excess times 4); and it grows with the dimension, following
    sigma^2 (d + 1) / (n - d - 2) to within 4 Monte Carlo standard errors for n >= 100 (400
    seeds)."""
    sizes = [100, 300, 1_000, 3_000]
    for d in (3, 10, 30):
        task = LinearGaussianTask(d=d, sigma=1.0)
        mean, se = learning_curve(task, sizes)
        assert np.all(mean > task.bayes_risk) and np.all(np.diff(mean) < 0)
        excess = mean - task.bayes_risk
        predicted = (d + 1) / (np.array(sizes) - d - 2)
        assert np.all(np.abs(excess - predicted) < 4 * se)
    low, _ = learning_curve(LinearGaussianTask(d=10, sigma=0.5), sizes)
    high, _ = learning_curve(LinearGaussianTask(d=10, sigma=1.0), sizes)
    np.testing.assert_allclose((high - 1.0) / (low - 0.25), 4.0, rtol=1e-9)


@pytest.fixture(scope="module")
def extrapolation():
    return {
        "unknown": extrapolation_experiment(TASK),
        "known": extrapolation_experiment(TASK, known_floor=True),
        "truth_2000": learning_curve(TASK, [2_000], seeds=2_000)[0][0],
        "n_star": size_for_target(TASK, 1.05),
    }


def test_learning_curve_extrapolation_within_interval(extrapolation):
    """Claim 19. A POW3 learning curve (A n^-B + C) fitted on a 200-example pilot (curve points
    from n = 20 to 140) extrapolates the error at n = 2,000 to within its 90% bootstrap
    interval in at least 80% of 30 pilots. The chapter reports how wide the interval is."""
    e, truth = extrapolation["unknown"]["error"], extrapolation["truth_2000"]
    coverage = np.mean((e[:, 1] <= truth) & (truth <= e[:, 2]))
    assert coverage >= 0.8


def test_extrapolated_data_requirement_is_biased_and_needs_the_floor(extrapolation):
    """Claim 41. Asking the same fit how many examples reach an error 5% above the noise floor
    (truth: about 230): with the floor unknown, the estimate is infinite (the fitted floor lies
    above the target) in at least a third of pilots; with the floor known, every estimate is
    finite and every 90% interval contains the truth, but the point estimate is biased low
    (median below 0.75 times the truth), because over the pilot range the curve falls faster
    than its asymptotic n^-1 (median fitted exponent above 1.4)."""
    n_star = extrapolation["n_star"]
    unknown, known = extrapolation["unknown"], extrapolation["known"]
    assert np.mean(~np.isfinite(unknown["size"][:, 0])) >= 1 / 3
    s = known["size"]
    assert np.all(np.isfinite(s[:, 0]))
    assert np.all((s[:, 1] <= n_star) & (n_star <= s[:, 2]))
    assert np.median(s[:, 0]) < 0.75 * n_star
    assert np.median(known["exponent"]) > 1.4


def test_ungrouped_bootstrap_understates_the_interval():
    """Without grouping copies of a resampled row, copies land in both the training and the
    held-out part of a pilot split, the pilot curve looks better than it is, and the bootstrap
    interval for the error at n = 2,000 is less than half as wide (median over 15 pilots)."""
    def width(grouped):
        r = extrapolation_experiment(TASK, pilots=15, grouped_bootstrap=grouped)
        return np.median(r["error"][:, 2] - r["error"][:, 1])

    assert width(False) < 0.5 * width(True)
