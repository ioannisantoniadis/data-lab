"""Claim tests: the decision guide's worked examples (chapter 15; claims 44-46).

The tabular truth is T1's exact conditional mean; the audio truth is the accuracy of the same
model on unshifted recordings. See src/data_lab/worked.py for the set-ups.
"""

import numpy as np
import pytest

from data_lab.sampling import ols
from data_lab.testbeds.t1_tabular import mar_mask
from data_lab.testbeds.t5_signals import log_power_spectrum, tone_classes
from data_lab.worked import COST, _fill, center, cost_example, tone_example


@pytest.fixture(scope="module")
def cost():
    return cost_example()


def test_cost_example_needs_smearing_and_the_right_missing_value_treatment(cost):
    """Claim 44. For the mean of a log-normal cost (sigma = 0.8) with a feature missing at random
    in training (about a third of rows; 20 seeds):

    - the plain back-transform exp(prediction of log y) underestimates the total by about
      exp(-sigma^2 / 2) - 1 = -27% (within 6 points of it, every seed);
    - with complete cases and smearing, the bias is within 8% on every seed and averages
      within 2% (dropping rows on an observed feature leaves p(y | x) intact);
    - mean imputation biases the coefficients: with smearing the total is still more than 7%
      low on every seed;
    - least squares on y has a per-row relative error above 1, over 20 times that of complete
      cases with smearing (a linear fit to an exponential mean).
    """
    out, rates = cost
    assert 0.3 < rates.mean() < 0.45
    expected = np.exp(-COST.sigma0**2 / 2) - 1
    assert np.all(np.abs(out[("complete", "naive")]["bias"] - expected) < 0.06)
    smear = out[("complete", "smear")]["bias"]
    assert np.all(np.abs(smear) < 0.08) and abs(smear.mean()) < 0.02
    assert np.all(out[("mean", "smear")]["bias"] < -0.07)
    raw, good = out[("complete", "raw")]["rel_rmse"], out[("complete", "smear")]["rel_rmse"]
    assert raw.mean() > 1.0 and raw.mean() > 20 * good.mean()


def test_regression_imputation_inflates_the_smearing_factor(cost):
    """Claim 45. Deterministic regression imputation keeps the coefficients nearly unbiased (within
    0.03) but adds the imputation error to the residuals on imputed rows, so the smearing factor
    (their mean exp) is more than 2% too large and the total is biased upward on average, more
    than with complete cases, whose factor is within 1% of exp(sigma^2 / 2). Mean imputation
    distorts the coefficients themselves (20 seeds)."""
    out, _ = cost
    reg, cc = out[("regress", "smear")]["bias"], out[("complete", "smear")]["bias"]
    assert reg.mean() > 0.02
    assert reg.mean() > cc.mean()
    # The mechanism: coefficients and smearing factors, averaged over the same 20 seeds.
    coefs, factors = {}, {}
    for kind in ("complete", "mean", "regress"):
        cs, fs = [], []
        for s in range(20):
            rng = np.random.default_rng(15_000 + s)
            z = COST.sample_z(2_000, rng)
            y = COST.sample_y(z, rng)
            zf, keep = _fill(z, mar_mask(z[:, 0], 0.3, 1.5, rng), kind)
            c = ols(zf, np.log(y[keep]))
            cs.append(c)
            fs.append(np.mean(np.exp(np.log(y[keep]) - c[0] - zf @ c[1:])))
        coefs[kind], factors[kind] = np.mean(cs, axis=0), np.mean(fs)
    truth = np.r_[COST.a, COST.b]
    true_factor = np.exp(COST.sigma0**2 / 2)
    assert np.all(np.abs(coefs["regress"] - truth) < 0.03)
    assert np.all(np.abs(coefs["complete"] - truth) < 0.03)
    assert np.max(np.abs(coefs["mean"] - truth)) > 0.07  # mean imputation distorts them
    assert factors["regress"] > 1.02 * true_factor
    assert abs(factors["complete"] / true_factor - 1) < 0.01


def test_centering_the_log_spectrum_removes_any_gain_exactly():
    """A gain g multiplies tone and noise, hence the STFT magnitude, so it adds log g to every
    bin of log_power_spectrum (the log of the time-averaged magnitude). Centering per recording
    removes it to rounding error."""
    rng = np.random.default_rng(0)
    waves, _ = tone_classes(6, rng)
    for g in (0.01, 3.0, 100.0):
        a, b = log_power_spectrum(waves), log_power_spectrum(g * waves)
        assert np.allclose(b - a, np.log(g), atol=1e-6)
        assert np.allclose(center(a), center(b), atol=1e-6)


def test_tone_example_gain_shift_and_its_two_fixes():
    """Claim 46. Trained at unit gain and tested at gains up to +-40 dB (30 seeds), a logistic
    regression on the raw waveform is at chance (within 0.05 of 0.5: random phase); on the log
    spectrum it loses more than 0.08 accuracy to the gain at 10 examples; centering per
    recording makes the features exactly gain-free and restores the unshifted accuracy to within
    0.01, and gain augmentation restores it to within 0.02. At 100 examples the spectrum model
    is within 0.02 of the unshifted accuracy anyway."""
    out = tone_example(sizes=(10, 100))
    mean = {k: v.mean(axis=0) for k, v in out.items()}
    assert np.all(np.abs(mean["raw"] - 0.5) < 0.05)
    assert mean["no_shift"][0] - mean["spectrum"][0] > 0.08
    assert abs(mean["centered"][0] - mean["no_shift"][0]) < 0.01
    assert abs(mean["augmented"][0] - mean["no_shift"][0]) < 0.02
    assert mean["no_shift"][1] - mean["spectrum"][1] < 0.02
