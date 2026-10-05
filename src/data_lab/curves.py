"""Learning curves (chapter 11) on a linear-Gaussian task where every risk is exact.

Task: z ~ N(0, I_d), y = a + b . z + eps with eps ~ N(0, sigma^2). For any fitted line with
intercept a_hat and coefficients b_hat, the squared-error risk under p is exactly

    R = sigma^2 + (a_hat - a)^2 + |b_hat - b|^2,

because E[z] = 0 and Cov(z) = I. The Bayes risk (the floor) is sigma^2. A learning curve is the
expected risk of the fitted model as a function of the training size n (Viering and Loog 2021,
§2); here it is estimated by averaging the exact risk over many training sets, so the only
noise is over training sets, not over test points.

Least squares: b_hat - b is linear in eps for a fixed design, so on the same designs the excess
risk scales exactly as sigma^2 (tested).

Extrapolation: the parametric form POW3, E(n) = A n^-B + C (Viering and Loog, Table 1), is fit
by least squares to a learning curve estimated from a small pilot dataset (subsampling, with the
rest of the pilot as test data), and a bootstrap over the pilot gives an interval.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LinearGaussianTask:
    d: int = 10
    sigma: float = 1.0
    coef_seed: int = 0
    intercept: float = 1.0

    @property
    def b(self) -> np.ndarray:
        return 0.5 * np.random.default_rng(self.coef_seed).standard_normal(self.d)

    def sample(self, n: int, rng: np.random.Generator):
        z = rng.standard_normal((n, self.d))
        return z, self.intercept + z @ self.b + self.sigma * rng.standard_normal(n)

    def exact_risk(self, coef: np.ndarray) -> float:
        return float(self.sigma**2 + (coef[0] - self.intercept) ** 2
                     + np.sum((coef[1:] - self.b) ** 2))

    @property
    def bayes_risk(self) -> float:
        return self.sigma**2


def ols(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    design = np.column_stack([np.ones(len(z)), z])
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    return coef


def learning_curve(task: LinearGaussianTask, sizes, seeds: int = 400, base_seed: int = 1):
    """Expected exact risk of least squares at each training size (mean over seeds), and the
    standard error of that mean."""
    means, ses = [], []
    for n in sizes:
        rng = np.random.default_rng(base_seed)
        risks = [task.exact_risk(ols(*task.sample(n, rng))) for _ in range(seeds)]
        means.append(np.mean(risks))
        ses.append(np.std(risks, ddof=1) / np.sqrt(seeds))
    return np.array(means), np.array(ses)


def pow3(n, a, b, c):
    return a * np.asarray(n, dtype=float) ** (-b) + c


PILOT_GRID = np.array([20, 30, 45, 65, 95, 140])


def pilot_curve(z, y, rng, grid=PILOT_GRID, subsamples: int = 10, groups=None) -> np.ndarray:
    """Estimated learning curve from one pilot dataset: for each n, fit on n random rows and
    measure squared error on the remaining rows; average over subsamples.

    ``groups`` gives each row's original identity (for a bootstrap resample, which repeats
    rows): train and test rows are then split by identity, so no row's copy is on both sides.
    Without this, copies leak across the split (chapter 4) and the curve is optimistic.
    """
    groups = np.arange(len(y)) if groups is None else np.asarray(groups)
    ids = np.unique(groups)
    per_id = np.bincount(groups, minlength=ids.max() + 1)
    points = []
    for n in grid:
        vals = []
        for _ in range(subsamples):
            order = rng.permutation(ids)
            counts = np.cumsum(per_id[order])
            train_ids = order[: np.searchsorted(counts, n) + 1]
            in_train = np.isin(groups, train_ids)
            coef = ols(z[in_train], y[in_train])
            test = ~in_train
            design = np.column_stack([np.ones(test.sum()), z[test]])
            vals.append(np.mean((design @ coef - y[test]) ** 2))
        points.append(np.mean(vals))
    return np.array(points)


def fit_pow3(points, grid=PILOT_GRID, floor=None):
    """Least-squares fit of POW3; with ``floor`` given, C is fixed at it (a known noise level)."""
    from scipy.optimize import curve_fit

    if floor is None:
        params, _ = curve_fit(pow3, grid, points, p0=[10.0, 1.0, 1.0],
                              bounds=([0.0, 0.0, 0.0], [1e4, 3.0, 10.0]), maxfev=20_000)
        return params
    params, _ = curve_fit(lambda n, a, b: pow3(n, a, b, floor), grid, points, p0=[10.0, 1.0],
                          bounds=([0.0, 0.0], [1e4, 3.0]), maxfev=20_000)
    return np.array([params[0], params[1], floor])


def n_for_target(params, target: float) -> float:
    """Training size at which a POW3 curve reaches ``target`` (inf if never)."""
    a, b, c = params
    return float((a / (target - c)) ** (1.0 / b)) if target > c and b > 0 else float("inf")


def extrapolation_experiment(task: LinearGaussianTask, pilots: int = 30, pilot_size: int = 200,
                             boots: int = 40, at: int = 2_000, target_excess: float = 0.05,
                             known_floor: bool = False):
    """For independent pilot datasets: the POW3 extrapolation of the error at ``at`` with a
    90% bootstrap interval, the extrapolated training size needed to reach the error
    sigma^2 (1 + target_excess) with its interval, and the fitted exponent B. With
    ``known_floor``, C is fixed at the true noise level sigma^2. Returns a dict with arrays
    "error" and "size" (pilots x 3: estimate, low, high), "exponent" (pilots,), "target"."""
    import warnings

    target = task.bayes_risk * (1 + target_excess)
    floor = task.bayes_risk if known_floor else None
    err, size, expo = [], [], []
    for k in range(pilots):
        rng = np.random.default_rng(100 + k)
        z, y = task.sample(pilot_size, rng)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            params = fit_pow3(pilot_curve(z, y, rng), floor=floor)
            boot_err, boot_size = [], []
            for _ in range(boots):
                i = rng.integers(0, pilot_size, pilot_size)
                try:
                    p = fit_pow3(pilot_curve(z[i], y[i], rng, groups=i), floor=floor)
                except RuntimeError:
                    continue
                boot_err.append(pow3(at, *p))
                boot_size.append(n_for_target(p, target))
            lo, hi = np.percentile(boot_err, [5, 95])
            s_lo, s_hi = np.percentile(boot_size, [5, 95])
        err.append((pow3(at, *params), lo, hi))
        size.append((n_for_target(params, target), s_lo, s_hi))
        expo.append(params[1])
    return {"error": np.array(err), "size": np.array(size), "exponent": np.array(expo),
            "target": target}


def size_for_target(task: LinearGaussianTask, target: float, lo: int = 20, hi: int = 5_000,
                    seeds: int = 2_000) -> int:
    """Smallest training size whose expected risk is at most ``target`` (bisection on the
    exact learning curve, which is decreasing here)."""
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if learning_curve(task, [mid], seeds=seeds)[0][0] <= target:
            hi = mid
        else:
            lo = mid
    return hi
