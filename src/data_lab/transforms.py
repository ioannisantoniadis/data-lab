"""Transforms (Part II): affine scaling (chapter 5), shape-changing transforms (chapter 6),
encodings (chapter 7).

Affine scaling. StandardScaler, MinMaxScaler, MaxAbsScaler and RobustScaler (scikit-learn 1.9
docstrings, read 2026-10-04) each map every feature by x -> (x - a_j) / b_j with b_j > 0:
respectively (mean, standard deviation with ddof = 0), (min, max - min), (0, max |x|) and
(median, interquartile range). An increasing affine map leaves every standardized moment of a
feature unchanged, so skewness and kurtosis survive (tested).
"""

from __future__ import annotations

import numpy as np


def least_squares_condition(features: np.ndarray, intercept: bool = True) -> float:
    """Condition number of the least-squares Hessian D'D / n, with D the design matrix (plus a
    column of ones when ``intercept``). Gradient descent on squared error slows as it grows
    (optimization-lab, Foundations)."""
    design = np.column_stack([np.ones(len(features)), features]) if intercept else features
    return float(np.linalg.cond(design.T @ design / len(design)))


def contaminate(values: np.ndarray, share: float, location: float, rng: np.random.Generator):
    """Replace a ``share`` of the entries by values near ``location``: gross outliers.
    Returns the contaminated copy and the outlier mask."""
    out = values.copy()
    k = int(round(share * len(values)))
    idx = rng.choice(len(values), k, replace=False)
    out[idx] = rng.normal(location, 1.0, size=k)
    mask = np.zeros(len(values), dtype=bool)
    mask[idx] = True
    return out, mask


def box_cox_sample(lam: float, n: int, rng: np.random.Generator) -> np.ndarray:
    """Positive data whose Box-Cox transform with parameter ``lam`` is exactly normal:
    y = (lam w + 1)^(1/lam) with w normal (y = exp(w) when lam = 0). The mean and spread of w
    keep lam w + 1 at least six standard deviations above zero, so truncation is negligible."""
    if lam == 0:
        return np.exp(rng.normal(1.0, 0.25, n))
    w = rng.normal(0.5 / lam, 0.25 / abs(lam), n)
    return (lam * w + 1.0) ** (1.0 / lam)


def smearing_predict(log_predictions: np.ndarray, log_residuals: np.ndarray) -> np.ndarray:
    """Back-transform predictions of E[log y | x] to the original scale by averaging exp over
    the empirical residual distribution: exp(prediction) * mean(exp(residuals)).

    Derivation: if log y = m(x) + e with e independent of x, then
    E[y | x] = exp(m(x)) E[exp(e)]; replacing the unknown distribution of e by the empirical
    distribution of the training residuals gives this estimate. Duan (1983) proposes the
    smearing estimate for retransformation (abstract read; this formula is derived here)."""
    return np.exp(log_predictions) * np.mean(np.exp(log_residuals))


def target_encoding_experiment(seeds: int = 20, levels: int = 1_000, n: int = 4_000):
    """T1 classification plus one pure-noise categorical feature with ``levels`` values,
    target-encoded three ways: not used ("none"), fit and applied on the same training rows
    ("naive"), and cross-fitted (TargetEncoder.fit_transform with a seeded 5-fold splitter).

    Returns {method: array (seeds, 3)} with (train accuracy, test accuracy, coefficient of the
    encoded feature) of an unpenalized logistic regression. Used by tests/test_leakage.py and
    scripts/figures/fig_encoding.py.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import KFold
    from sklearn.preprocessing import TargetEncoder

    from data_lab.testbeds.t1_tabular import TabularGenerator

    gen = TabularGenerator(d=3, rho=0.3)
    out: dict[str, list] = {"none": [], "naive": [], "crossfit": []}
    for s in range(seeds):
        rng = np.random.default_rng(800 + s)
        z = gen.sample_z(n, rng)
        y = gen.sample_labels(z, rng)
        cat = rng.integers(0, levels, n)[:, None]
        tr, te = slice(0, n // 2), slice(n // 2, n)
        for method in out:
            if method == "none":
                x_tr, x_te = z[tr], z[te]
            else:
                # TargetEncoder shuffles its internal folds by default with no seed
                # (scikit-learn 1.9); a seeded splitter makes the cross-fit reproducible.
                enc = TargetEncoder(cv=KFold(5, shuffle=True, random_state=s))
                if method == "naive":
                    enc_tr = enc.fit(cat[tr], y[tr]).transform(cat[tr])
                else:
                    enc_tr = enc.fit_transform(cat[tr], y[tr])
                x_tr = np.hstack([z[tr], enc_tr])
                x_te = np.hstack([z[te], enc.transform(cat[te])])
            model = LogisticRegression(C=np.inf).fit(x_tr, y[tr])
            coef = model.coef_[0][-1] if method != "none" else 0.0
            out[method].append((model.score(x_tr, y[tr]), model.score(x_te, y[te]), coef))
    return {k: np.array(v) for k, v in out.items()}
