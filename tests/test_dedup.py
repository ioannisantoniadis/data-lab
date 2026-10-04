"""Claim tests: Part IV, deduplication (SPEC §8 claim 18; T4).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 3: claim 18 not yet implemented")
def test_deduplication_reduces_overlap_optimism():
    """Claim 18. Removing duplicates from T4 lowers the test cross-entropy optimism caused by
    train/test overlap.
    """
