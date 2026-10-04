"""Claim tests: Part IV, Hutter's model and coverage-driven selection (SPEC §8 claims 14-16; T2).

Stubs from Phase 0: each test is named after its claim and skipped until the phase that
implements it. Unskip only when the test checks the claim numerically against ground truth.
"""

import pytest


@pytest.mark.skip(reason="Phase 1: claim 14 not yet implemented")
def test_hutter_exact_sum_matches_monte_carlo():
    """Claim 14. Hutter's exact sum E_n = sum_i p_i (1 - p_i)^n matches Monte Carlo simulation of
    the memorizing learner (T2).
    """


@pytest.mark.skip(reason="Phase 1: claim 15 not yet implemented")
def test_learning_curve_slope_approaches_hutter_exponent():
    """Claim 15. The log-log slope of E_n approaches -alpha/(1+alpha) on T2 for several alpha."""


@pytest.mark.skip(reason="Phase 1: claim 16 not yet implemented")
def test_coverage_selection_beats_uniform_at_derived_rate():
    """Claim 16. Coverage-driven selection beats uniform sampling at equal budget on T2, at the
    rate derived in Phase 1 (SPEC §7).
    """
