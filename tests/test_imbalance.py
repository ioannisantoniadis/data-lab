"""Claim tests: Part III, imbalance and prior shift (SPEC §8 claims 10-11).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 3: claim 10 not yet implemented")
def test_prior_shift_correction_restores_calibration():
    """Claim 10. Training on resampled balanced data shifts predicted probabilities; the
    correction p(y | x) proportional to q(y | x) p(y) / q(y) restores calibration (T1). SPEC
    v0.1 wrote the priors as pi_y; restated in the book's p/q notation.
    """


@pytest.mark.skip(reason="Phase 3: claim 11 not yet implemented")
def test_em_prior_estimation_recovers_test_prior():
    """Claim 11. EM prior estimation (Saerens et al. 2002) recovers a known test prior on T1."""
