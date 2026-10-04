"""Claim tests: Part II, shape-changing transforms (SPEC §8 claims 4-6).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 2: claim 4 not yet implemented")
def test_log_target_mse_predicts_geometric_mean():
    """Claim 4. With MSE on log y, back-transformed predictions estimate exp(E[log y | x]); under
    log-normal noise this underestimates E[y | x] by the factor exp(sigma_eps^2 / 2), and the
    smearing estimate corrects it (T1). Factor to be checked against Duan 1983 before use.
    """


@pytest.mark.skip(reason="Phase 2: claim 5 not yet implemented")
def test_box_cox_mle_recovers_known_lambda():
    """Claim 5. Box-Cox lambda by maximum likelihood recovers a known lambda on T1 data."""


@pytest.mark.skip(reason="Phase 2: claim 6 not yet implemented")
def test_quantile_transform_changes_distances_preserves_ranks():
    """Claim 6. A quantile transform to uniform changes pairwise Euclidean distances while
    preserving ranks within each feature.
    """
