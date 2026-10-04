"""Claim tests: Part III, covariate shift (SPEC §8 claim 12).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 3: claim 12 not yet implemented")
def test_importance_weighting_unbiased_with_growing_variance():
    """Claim 12. Importance weighting with the true density ratio gives an unbiased risk estimate
    under covariate shift, with variance that grows as the shift grows (T1).
    """
