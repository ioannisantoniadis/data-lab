"""Claim tests: Part IV, scaling laws (claim 42, added in Phase 3 for chapter 12; T4)."""

import numpy as np
import pytest

from data_lab.scaling import (
    SOURCE,
    data_scaling_curve,
    fit_forms,
    power_law,
    power_law_with_floor,
)


@pytest.fixture(scope="module")
def curve():
    sizes = np.unique(np.logspace(2, 6, 17).astype(int))
    return sizes, data_scaling_curve(sizes)


def test_data_scaling_has_a_floor_and_regimes(curve):
    """Claim 42. On T4, a smoothed bigram model's exact cross-entropy stays above the source's
    entropy rate and approaches it (10 seeds); its excess over the floor is not one power law:
    the local log-log slope is shallow early (above -0.6 below 10^3.5 tokens) and close to -1
    late (within 0.15 over the last decade, the variance-limited regime of a fixed-size model).
    Fitted on D <= 10^4 tokens and extrapolated to 10^6, a pure power law (Kaplan et al.'s
    form, no floor) predicts a loss below the entropy rate, which no model can reach; adding an
    irreducible term (Hoffmann et al.'s form) keeps the prediction above the floor but
    overestimates the loss, because the early exponent is not the late one."""
    sizes, losses = curve
    h = SOURCE.entropy_rate
    excess = losses - h
    assert np.all(excess > 0) and excess[-1] < 0.002
    slopes = np.diff(np.log(excess)) / np.diff(np.log(sizes))
    early = sizes[1:] <= 10**3.5
    assert np.all(slopes[early] > -0.6)
    assert np.all(np.abs(slopes[-4:] + 1) < 0.15)
    window = sizes <= 1e4
    pure, floor = fit_forms(sizes[window], losses[window])
    assert power_law(1e6, *pure) < h
    assert power_law_with_floor(1e6, *floor) > losses[-1]
    assert abs(floor[2] - 1) > 0.5
