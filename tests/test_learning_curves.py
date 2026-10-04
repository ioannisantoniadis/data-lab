"""Claim tests: Part IV, learning curves (SPEC §8 claim 19; T1).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 3: claim 19 not yet implemented")
def test_learning_curve_extrapolation_within_interval():
    """Claim 19. A learning curve fitted on small n extrapolates to within its stated interval at
    larger n on T1, or the chapter reports that it does not.
    """
