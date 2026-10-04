"""Claim tests: Part II, leakage (SPEC §8 claims 8-9).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 2: claim 8 not yet implemented")
def test_target_encoding_without_cross_fitting_leaks():
    """Claim 8. Target encoding without cross-fitting gives a pure-noise high-cardinality feature
    a large training score and no test advantage; cross-fitting removes the gap.
    """


@pytest.mark.skip(reason="Phase 2: claim 9 not yet implemented")
def test_fitting_preprocessing_on_test_is_optimistic():
    """Claim 9. Fitting a scaler or imputer on train + test changes test metrics vs. train-only
    fitting, in the direction of optimism, on a constructed case.
    """
