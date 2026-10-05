"""Cleaning (chapter 4): simple treatments of missing values, and duplicate bookkeeping.

Definitions (van Buuren 2018, *Flexible Imputation of Missing Data*, §1.2, after Rubin 1976):
data are MCAR if the probability of being missing is the same for all cases, MAR if it is the
same only within groups defined by the observed data, and MNAR otherwise.

The three treatments here are deliberately simple, so their bias can be derived:

- complete-case analysis: drop rows with the value missing (a change to q);
- mean imputation: replace a missing value by the observed mean (a change to the
  representation that shrinks the variance by the share imputed, under MCAR);
- regression imputation: replace a missing value by its least-squares prediction from an
  always-observed column, which removes the bias of the mean under MAR when that column
  carries the dependence (van Buuren §1.3.4: regression weights unbiased, variability
  understated).
"""

from __future__ import annotations

import numpy as np


def complete_case(values: np.ndarray, missing: np.ndarray) -> np.ndarray:
    return values[~missing]


def mean_impute(values: np.ndarray, missing: np.ndarray) -> np.ndarray:
    return np.where(missing, values[~missing].mean(), values)


def regression_impute(values: np.ndarray, missing: np.ndarray, predictor: np.ndarray):
    """Impute from a straight-line fit of ``values`` on an always-observed ``predictor``."""
    slope, intercept = np.polyfit(predictor[~missing], values[~missing], 1)
    return np.where(missing, intercept + slope * predictor, values)


def overlap_mask(train: np.ndarray, test: np.ndarray) -> np.ndarray:
    """True for test rows that appear exactly in the training rows."""
    seen = {row.tobytes() for row in np.ascontiguousarray(train)}
    return np.array([row.tobytes() in seen for row in np.ascontiguousarray(test)])


def missingness_experiment(
    mechanism: str, seeds: int = 200, n: int = 2_000, rate: float = 0.4, rho: float = 0.6
) -> dict[str, np.ndarray]:
    """Estimate the mean and variance of T1's z_1 (truth 0 and 1) under a missingness
    mechanism ("MCAR", "MAR" on z_2, "MNAR" on z_1 itself), for each treatment.

    Returns {"cc" | "mean" | "reg": array of shape (seeds, 2)} with columns (mean, variance).
    Used by tests/test_missing.py and scripts/figures/fig_missingness.py.
    """
    from data_lab.testbeds.t1_tabular import TabularGenerator, mar_mask, mcar_mask, mnar_mask

    gen = TabularGenerator(d=3, rho=rho)
    out: dict[str, list] = {k: [] for k in ("cc", "mean", "reg")}
    for s in range(seeds):
        rng = np.random.default_rng(7_000 + s)
        z = gen.sample_z(n, rng)
        x1, x2 = z[:, 0], z[:, 1]
        if mechanism == "MCAR":
            miss = mcar_mask(n, rate, rng)
        elif mechanism == "MAR":
            miss = mar_mask(x2, rate, 2.0, rng)
        elif mechanism == "MNAR":
            miss = mnar_mask(x1, rate, 2.0, rng)
        else:
            raise ValueError(mechanism)
        for key, vals in (
            ("cc", complete_case(x1, miss)),
            ("mean", mean_impute(x1, miss)),
            ("reg", regression_impute(x1, miss, x2)),
        ):
            out[key].append((vals.mean(), vals.var()))
    return {k: np.array(v) for k, v in out.items()}


def duplicate_experiment(share: float, seeds: int = 20, n_test: int = 1_000):
    """1-nearest-neighbor accuracy on T1 when a ``share`` of the test rows are copies of
    training rows: returns (accuracy on the contaminated test set, accuracy on its fresh
    rows) per seed. Used by tests/test_leakage.py and scripts/figures/fig_leakage.py."""
    from sklearn.neighbors import KNeighborsClassifier

    from data_lab.testbeds.t1_tabular import TabularGenerator

    gen = TabularGenerator(d=3, rho=0.3)
    rows = []
    for s in range(seeds):
        rng = np.random.default_rng(28_000 + s)
        z = gen.sample_z(2_000 + n_test, rng)
        y = gen.sample_labels(z, rng)
        ztr, ytr = z[:2_000], y[:2_000]
        k = int(round(share * n_test))
        copied = rng.choice(2_000, k, replace=False)
        zte = np.vstack([z[2_000 : 2_000 + n_test - k], ztr[copied]])
        yte = np.r_[y[2_000 : 2_000 + n_test - k], ytr[copied]]
        model = KNeighborsClassifier(1).fit(ztr, ytr)
        fresh = ~overlap_mask(ztr, zte)
        rows.append((model.score(zte, yte), model.score(zte[fresh], yte[fresh])))
    return np.array(rows)


def unsupervised_fit_gap(prep: str, model_name: str, seeds: int = 200) -> np.ndarray:
    """Test accuracy with a preprocessing step fit on train + test minus with it fit on train
    only, per seed, on i.i.d. T1 data with unequal feature scales. ``prep``: "std", "minmax"
    or "impute" (30% MCAR in one column); ``model_name``: "knn" (15 neighbors) or "logreg"
    (C = 0.01)."""
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.preprocessing import MinMaxScaler, StandardScaler

    from data_lab.testbeds.t1_tabular import TabularGenerator, mcar_mask

    gen = TabularGenerator(d=3, rho=0.3)
    scales = np.array([1.0, 10.0, 0.1])
    make_prep = {"std": StandardScaler, "minmax": MinMaxScaler, "impute": SimpleImputer}[prep]
    gaps = []
    for s in range(seeds):
        rng = np.random.default_rng(9_000 + s)
        z = gen.sample_z(400, rng)
        y = gen.sample_labels(z, rng)
        x = z * scales
        if prep == "impute":
            x[mcar_mask(400, 0.3, rng), 0] = np.nan
        train, test = slice(0, 200), slice(200, 400)
        scores = []
        for fit_on in (x[train], x):
            p = make_prep().fit(fit_on)
            model = KNeighborsClassifier(15) if model_name == "knn" else LogisticRegression(C=0.01)
            model.fit(p.transform(x[train]), y[train])
            scores.append(model.score(p.transform(x[test]), y[test]))
        gaps.append(scores[1] - scores[0])
    return np.array(gaps)


def supervised_selection_leak(seeds: int = 20) -> np.ndarray:
    """Pure-noise labels, 100 examples, 2,000 noise features, 20 selected by an F-test. Returns
    per seed (CV accuracy with selection fit on all data, CV accuracy with selection inside the
    folds). The true accuracy of any model is 0.5."""
    from sklearn.feature_selection import SelectKBest, f_classif
    from sklearn.model_selection import cross_val_score
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline

    rows = []
    for s in range(seeds):
        rng = np.random.default_rng(9_500 + s)
        x = rng.standard_normal((100, 2_000))
        y = rng.integers(0, 2, 100)
        selected = SelectKBest(f_classif, k=20).fit(x, y).transform(x)
        leaky = cross_val_score(KNeighborsClassifier(5), selected, y, cv=5).mean()
        pipe = make_pipeline(SelectKBest(f_classif, k=20), KNeighborsClassifier(5))
        rows.append((leaky, cross_val_score(pipe, x, y, cv=5).mean()))
    return np.array(rows)
