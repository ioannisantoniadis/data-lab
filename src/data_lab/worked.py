"""The decision guide's two worked examples (chapter 15), each checked against a known truth.

Tabular (T1): a positive, right-skewed cost y whose conditional *mean* is wanted (the total of
predictions must match the total cost). One feature is missing at random in the training data,
more often when another feature is large; deployment rows are complete. Pipelines cross three
treatments of the missing values (complete cases; mean imputation; regression imputation from
the other features) with three treatments of the target (least squares on y; least squares on
log y, back-transformed by exp; the same with Duan's smearing factor, the mean of exp(residual)).
The truth is T1's exact conditional mean exp(m(z) + sigma^2 / 2).

Audio (T5): two tone classes (400-600 Hz against 1,200-1,400 Hz, random phase, noise), recorded
at unit gain for training and at a random gain for deployment (log-uniform between 1/spread and
spread). A recording gain scales tone and noise together, so it multiplies the STFT magnitude
by the gain and adds the same constant, log(gain), to every bin of ``log_power_spectrum`` (the
log of the time-averaged STFT magnitude). Pipelines: the raw waveform; the log power
spectrum; the spectrum centered per recording (its mean over frequencies subtracted), which
removes the constant exactly; and the spectrum with gain augmentation (four copies of each
training recording at random gains, labels unchanged: a true invariance).
"""

from __future__ import annotations

import numpy as np

from data_lab.sampling import ols
from data_lab.testbeds.t1_tabular import TabularGenerator, mar_mask
from data_lab.testbeds.t5_signals import log_power_spectrum, tone_classes

# --- tabular --------------------------------------------------------------------------------

COST = TabularGenerator(d=3, rho=0.5, sigma0=0.8)
MISSING_TREATMENTS = ("complete", "mean", "regress")
TARGET_TREATMENTS = ("raw", "naive", "smear")


def _fill(z: np.ndarray, miss: np.ndarray, kind: str):
    """Training features after one treatment of column 1's missing values, and the rows kept."""
    z = z.copy()
    keep = np.ones(len(z), dtype=bool)
    if kind == "complete":
        keep = ~miss
    elif kind == "mean":
        z[miss, 1] = z[~miss, 1].mean()
    elif kind == "regress":
        coef = ols(z[~miss][:, [0, 2]], z[~miss, 1])
        z[miss, 1] = coef[0] + z[miss][:, [0, 2]] @ coef[1:]
    else:
        raise ValueError(kind)
    return z[keep], keep


def cost_example(seeds: int = 20, n: int = 2_000, n_test: int = 20_000,
                 base: float = 0.3, slope: float = 1.5):
    """Relative bias of the predicted total, sum(pred) / sum(truth) - 1, and the relative RMSE
    per row, sqrt(mean((pred / truth - 1)^2)), on complete deployment rows. Returns
    {(missing, target): {"bias": array(seeds), "rel_rmse": array(seeds)}} and the missing rate."""
    out = {(m, t): {"bias": np.empty(seeds), "rel_rmse": np.empty(seeds)}
           for m in MISSING_TREATMENTS for t in TARGET_TREATMENTS}
    rates = np.empty(seeds)
    for s in range(seeds):
        rng = np.random.default_rng(15_000 + s)
        z = COST.sample_z(n, rng)
        y = COST.sample_y(z, rng)
        miss = mar_mask(z[:, 0], base, slope, rng)
        rates[s] = miss.mean()
        zt = COST.sample_z(n_test, rng)
        truth = COST.conditional_mean(zt)
        for m in MISSING_TREATMENTS:
            zf, keep = _fill(z, miss, m)
            yk = y[keep]
            coef_raw = ols(zf, yk)
            coef_log = ols(zf, np.log(yk))
            resid = np.log(yk) - (coef_log[0] + zf @ coef_log[1:])
            log_pred = coef_log[0] + zt @ coef_log[1:]
            preds = {
                "raw": coef_raw[0] + zt @ coef_raw[1:],
                "naive": np.exp(log_pred),
                "smear": np.exp(log_pred) * np.mean(np.exp(resid)),
            }
            for t, pred in preds.items():
                out[(m, t)]["bias"][s] = pred.sum() / truth.sum() - 1
                out[(m, t)]["rel_rmse"][s] = np.sqrt(np.mean((pred / truth - 1) ** 2))
    return out, rates


# --- audio ----------------------------------------------------------------------------------

AUDIO_PIPELINES = ("raw", "spectrum", "centered", "augmented")


def center(spectra: np.ndarray) -> np.ndarray:
    """Subtract each recording's mean log power over frequencies: removes any gain exactly."""
    return spectra - spectra.mean(axis=1, keepdims=True)


def _gains(shape, spread: float, rng: np.random.Generator) -> np.ndarray:
    return np.exp(rng.uniform(-np.log(spread), np.log(spread), size=shape))


def tone_example(sizes=(10, 20, 40, 100), seeds: int = 30, spread: float = 100.0,
                 n_test: int = 400, copies: int = 4):
    """Test accuracy of logistic regression (scikit-learn, C = 1) for each pipeline and training
    size, trained at unit gain and tested at random gains; also "no_shift", the spectrum model
    tested at unit gain. Returns {pipeline: array (seeds, len(sizes))}."""
    from sklearn.linear_model import LogisticRegression

    keys = (*AUDIO_PIPELINES, "no_shift")
    out = {k: np.empty((seeds, len(sizes))) for k in keys}
    for s in range(seeds):
        for j, n in enumerate(sizes):
            rng = np.random.default_rng(15_500 + 100 * s + j)
            xtr, ytr = tone_classes(n, rng)
            xte, yte = tone_classes(n_test, rng)
            xg = xte * _gains(len(xte), spread, rng)[:, None]
            spec_tr, spec_te = log_power_spectrum(xtr), log_power_spectrum(xg)
            aug = np.concatenate([xtr] + [xtr * _gains(n, spread, rng)[:, None]
                                          for _ in range(copies)])

            def fit(a, b):
                return LogisticRegression(C=1.0, max_iter=5_000).fit(a, b)

            spec_model = fit(spec_tr, ytr)
            out["raw"][s, j] = fit(xtr, ytr).score(xg, yte)
            out["spectrum"][s, j] = spec_model.score(spec_te, yte)
            out["no_shift"][s, j] = spec_model.score(log_power_spectrum(xte), yte)
            out["centered"][s, j] = fit(center(spec_tr), ytr).score(center(spec_te), yte)
            out["augmented"][s, j] = fit(log_power_spectrum(aug),
                                         np.tile(ytr, copies + 1)).score(spec_te, yte)
    return out
