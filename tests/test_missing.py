"""Claim tests: Part II, missing-data mechanisms (SPEC §8 claim 7; T1)."""

import numpy as np

from data_lab.cleaning import missingness_experiment as run

RATE = 0.4


def _bias_in_se(est: np.ndarray, truth: float) -> float:
    return abs(est.mean() - truth) / (est.std(ddof=1) / np.sqrt(len(est)))


def test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased():
    """Claim 7. Under MCAR, mean imputation leaves the mean unbiased but shrinks the variance
    (to about 1 - r with r the missing share: 0.6 here); under MAR, complete-case estimates of
    the mean are biased, and regression imputation on the column that drives the missingness
    removes that bias; under MNAR every treatment here stays biased. 200 seeds, T1."""
    mcar, mar, mnar = run("MCAR"), run("MAR"), run("MNAR")
    assert _bias_in_se(mcar["mean"][:, 0], 0.0) < 4
    assert _bias_in_se(mcar["cc"][:, 0], 0.0) < 4
    assert abs(mcar["mean"][:, 1].mean() - (1 - RATE)) < 0.02
    assert abs(mcar["cc"][:, 1].mean() - 1.0) < 0.02
    assert _bias_in_se(mar["cc"][:, 0], 0.0) > 20
    assert _bias_in_se(mar["mean"][:, 0], 0.0) > 20
    assert _bias_in_se(mar["reg"][:, 0], 0.0) < 4
    for key in ("cc", "mean", "reg"):
        assert _bias_in_se(mnar[key][:, 0], 0.0) > 20
