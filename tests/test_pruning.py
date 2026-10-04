"""Claim tests: Part IV, data pruning (SPEC §8 claim 17; T3).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 3: claim 17 not yet implemented")
def test_pruning_crossover_hard_when_abundant_easy_when_scarce():
    """Claim 17. On T3, keeping hard examples beats keeping easy ones when initial data is
    abundant, and the reverse when scarce (multi-seed; the text quotes how many seeds show it).
    """
