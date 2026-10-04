"""Claim tests: Part III, augmentation (SPEC §8 claim 13).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 3: claim 13 not yet implemented")
def test_invariant_augmentation_helps_noninvariant_hurts():
    """Claim 13. Augmenting with a transform the true function is invariant to does not hurt test
    error (and helps at small n); a non-invariant transform hurts (T5 or T1).
    """
