"""Claim tests: Part II, which models care about which transforms (SPEC §8 claims 2-3).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 2: claim 2 not yet implemented")
def test_tree_predictions_invariant_to_monotone_feature_transform():
    """Claim 2. A decision tree's predictions are unchanged by any strictly monotone transform of
    a feature (given the same tie-breaking).
    """


@pytest.mark.skip(reason="Phase 2: claim 3 not yet implemented")
def test_knn_prediction_flips_under_feature_rescaling():
    """Claim 3. k-NN predictions change under per-feature rescaling; a constructed case where
    scaling flips the prediction.
    """
