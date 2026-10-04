"""Claim tests: Part IV, model collapse (SPEC §8 claim 20; T2).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 3: claim 20 not yet implemented")
def test_refitting_on_own_samples_loses_tail():
    """Claim 20. Repeatedly refitting on samples from the previous fit loses the tail of T2's
    distribution (multi-seed). Prior art: Dohmatob et al. 2024 derive the rates on this model;
    this is the replace-not-accumulate regime (Gerstgrasser et al. 2024).
    """
