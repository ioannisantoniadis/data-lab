"""Claim tests: Part II, affine scaling (SPEC §8 claims 1 and 21).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 2: claim 1 not yet implemented")
def test_affine_scalers_preserve_skewness_and_kurtosis():
    """Claim 1. Standard, min-max, max-abs and robust scaling leave sample skewness and kurtosis
    unchanged (affine invariance).
    """


@pytest.mark.skip(reason="Phase 2: claim 21 not yet implemented")
def test_feature_scaling_changes_least_squares_conditioning():
    """Claim 21. Per-feature rescaling changes the condition number of the least-squares
    Hessian (proportional to X^T X), and standardization reduces it on a constructed T1 case.
    """
