"""Claim tests: Part II, missing-data mechanisms (SPEC §8 claim 7).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 2: claim 7 not yet implemented")
def test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased():
    """Claim 7. Under MCAR, mean imputation leaves the mean unbiased but shrinks the variance;
    under MAR, complete-case estimates of the mean are biased (T1, multi-seed).
    """
