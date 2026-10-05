"""How the training sample is drawn: selection mechanisms and sampling designs (Part I), and
later resampling, reweighting and prior-shift correction (Part III).

Selection (chapter 1). An example drawn from the target distribution p is kept with
probability s(x, y). The kept examples follow q(x, y) proportional to s(x, y) p(x, y), so

    q(y | x) = s(x, y) p(y | x) / sum_y' s(x, y') p(y' | x).

If s depends on x only, the s(x) factors cancel and q(y | x) = p(y | x): selection on x
changes only the input distribution. If s depends on y, q(y | x) differs from p(y | x). In both
cases p is proportional to q / s, so when s is known, weighting each kept example by 1 / s
restores expectations under p.
"""

from __future__ import annotations

import numpy as np
from scipy.special import expit


def keep_on_x(z: np.ndarray, strength: float, rng: np.random.Generator) -> np.ndarray:
    """Keep each example with probability sigmoid(strength * z_1): depends on inputs only."""
    return rng.random(len(z)) < expit(strength * z[:, 0])


def keep_on_y_probability(log_y: np.ndarray, strength: float) -> np.ndarray:
    """s(y) = sigmoid(-strength * (log y - median)): large targets are under-sampled."""
    return expit(-strength * (log_y - np.median(log_y)))


def keep_on_y(log_y: np.ndarray, strength: float, rng: np.random.Generator) -> np.ndarray:
    """Keep each example with probability keep_on_y_probability: as when high values are less
    often recorded."""
    return rng.random(len(log_y)) < keep_on_y_probability(log_y, strength)


def ols(features: np.ndarray, target: np.ndarray, weights: np.ndarray | None = None):
    """(Weighted) least-squares coefficients [intercept, slopes...]."""
    design = np.column_stack([np.ones(len(features)), features])
    if weights is not None:
        root = np.sqrt(weights)
        design, target = design * root[:, None], target * root
    coef, *_ = np.linalg.lstsq(design, target, rcond=None)
    return coef


def stratified_sample(
    strata: np.ndarray, n: int, rng: np.random.Generator
) -> np.ndarray:
    """Indices of a proportionally allocated stratified sample: in each stratum h, a simple
    random sample of round(n * N_h / N) units (Çetinkaya-Rundel & Hardin 2024, §2.1.5)."""
    labels, sizes = np.unique(strata, return_counts=True)
    alloc = np.round(n * sizes / sizes.sum()).astype(int)
    picks = [
        rng.choice(np.flatnonzero(strata == h), size=k, replace=False)
        for h, k in zip(labels, alloc, strict=True)
    ]
    return np.concatenate(picks)


# --- class imbalance and prior shift (chapter 8) ----------------------------------------------


def prior_shift_correct(prob1: np.ndarray, train_prior1: float, target_prior1: float):
    """Saerens et al. 2002, eq. 4, for two classes: reweight the trained model's posterior by the
    ratio of new to old priors and renormalize. Valid when p(x | y) is the same in training and
    target data and only the class priors differ."""
    a = prob1 * target_prior1 / train_prior1
    b = (1.0 - prob1) * (1.0 - target_prior1) / (1.0 - train_prior1)
    return a / (a + b)


def em_prior(prob1_new: np.ndarray, train_prior1: float, tol: float = 1e-10,
             max_iter: int = 10_000) -> float:
    """Saerens et al. 2002, eq. 9: estimate the class-1 prior of unlabeled new data by EM,
    starting from the training prior. Each step corrects the posteriors to the current prior
    estimate and sets the next estimate to their mean."""
    prior = train_prior1
    for _ in range(max_iter):
        new = float(np.mean(prior_shift_correct(prob1_new, train_prior1, prior)))
        if abs(new - prior) < tol:
            return new
        prior = new
    return prior


def balanced_undersample(y: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Indices keeping every minority example and an equal number of majority examples."""
    pos, neg = np.flatnonzero(y == 1), np.flatnonzero(y == 0)
    small, large = (pos, neg) if len(pos) < len(neg) else (neg, pos)
    return np.concatenate([small, rng.choice(large, len(small), replace=False)])


def smote(minority: np.ndarray, n_new: int, k: int, rng: np.random.Generator) -> np.ndarray:
    """SMOTE (Chawla et al. 2002, §4.2): each synthetic example is a random point on the segment
    between a minority example and one of its k nearest minority neighbors (gap ~ U(0, 1)).
    Base examples are taken in turn, so each is used about n_new / len(minority) times."""
    d2 = ((minority[:, None, :] - minority[None, :, :]) ** 2).sum(axis=2)
    np.fill_diagonal(d2, np.inf)
    neighbors = np.argsort(d2, axis=1)[:, :k]
    base = np.arange(n_new) % len(minority)
    pick = neighbors[base, rng.integers(0, k, n_new)]
    gap = rng.random(n_new)[:, None]
    return minority[base] + gap * (minority[pick] - minority[base])


def two_cluster_minority(n: int, rng: np.random.Generator, prior1: float = 0.1,
                         sep: float = 2.0):
    """A non-convex minority class: class 1 is an equal mixture of two unit-variance blobs at
    (-sep, 0) and (sep, 0), class 0 one blob at (0, 0). Returns (x, y, eta) with the exact
    posterior eta(x) = P(y = 1 | x) computed from the known densities."""
    y = (rng.random(n) < prior1).astype(int)
    centers = np.where(rng.random(n) < 0.5, -sep, sep)
    x = rng.standard_normal((n, 2))
    x[:, 0] += np.where(y == 1, centers, 0.0)
    return x, y, two_cluster_posterior(x, prior1, sep)


def two_cluster_posterior(x: np.ndarray, prior1: float = 0.1, sep: float = 2.0) -> np.ndarray:
    def dens(cx):
        return np.exp(-0.5 * ((x[:, 0] - cx) ** 2 + x[:, 1] ** 2))

    f1 = 0.5 * dens(-sep) + 0.5 * dens(sep)
    f0 = dens(0.0)
    return prior1 * f1 / (prior1 * f1 + (1 - prior1) * f0)


def minority_sample(n_minority: int, sep: float, rng: np.random.Generator) -> np.ndarray:
    """n_minority draws from the minority mixture of two_cluster_minority."""
    x = rng.standard_normal((n_minority, 2))
    x[:, 0] += np.where(rng.random(n_minority) < 0.5, -sep, sep)
    return x


# --- chapter 8 experiments, shared by tests, figures and published numbers ---------------------


def rare_event_generator(prior1: float = 0.05):
    """T1 with the intercept u0 set so that P(y = 1) = prior1 under p."""
    from scipy.optimize import brentq

    from data_lab.testbeds.t1_tabular import TabularGenerator

    u0 = brentq(lambda c: TabularGenerator(d=3, rho=0.3, u0=c).prior() - prior1, -20, 20)
    return TabularGenerator(d=3, rho=0.3, u0=u0)


def imbalance_experiment(seeds: int = 30, n: int = 20_000, prior1: float = 0.05):
    """Plain, balanced-undersampled and class-weighted logistic regressions on rare-event T1.

    Returns {name: array (seeds,)} of mean |predicted - true posterior| on fresh data for
    "plain", "under", "weighted", "under_corrected", "weighted_corrected" (Saerens eq. 4 from a
    training prior of 1/2 back to the true prior), and {"under_coef", "weighted_coef"}: the
    coefficient on z_1 (true value u_1 = 1.5).
    """
    from sklearn.linear_model import LogisticRegression

    gen = rare_event_generator(prior1)
    prior = gen.prior()
    out: dict[str, list] = {k: [] for k in (
        "plain", "under", "weighted", "under_corrected", "weighted_corrected",
        "under_coef", "weighted_coef")}
    for s in range(seeds):
        rng = np.random.default_rng(1_000 + s)
        z = gen.sample_z(n, rng)
        y = gen.sample_labels(z, rng)
        z_new = gen.sample_z(n, rng)
        eta = gen.posterior(z_new)
        plain = LogisticRegression(C=np.inf).fit(z, y)
        idx = balanced_undersample(y, rng)
        under = LogisticRegression(C=np.inf).fit(z[idx], y[idx])
        weighted = LogisticRegression(C=np.inf, class_weight="balanced").fit(z, y)
        p_under = under.predict_proba(z_new)[:, 1]
        p_weighted = weighted.predict_proba(z_new)[:, 1]
        out["plain"].append(np.mean(np.abs(plain.predict_proba(z_new)[:, 1] - eta)))
        out["under"].append(np.mean(np.abs(p_under - eta)))
        out["weighted"].append(np.mean(np.abs(p_weighted - eta)))
        out["under_corrected"].append(
            np.mean(np.abs(prior_shift_correct(p_under, 0.5, prior) - eta)))
        out["weighted_corrected"].append(
            np.mean(np.abs(prior_shift_correct(p_weighted, 0.5, prior) - eta)))
        out["under_coef"].append(under.coef_[0][0])
        out["weighted_coef"].append(weighted.coef_[0][0])
    return {k: np.array(v) for k, v in out.items()}


def em_experiment(seeds: int = 20, train_prior: float = 0.5, new_prior: float = 0.1):
    """Train on T1 data with class-1 prior train_prior; estimate the prior of unlabeled new
    data drawn with new_prior by EM (Saerens eq. 9). Returns the estimates per seed."""
    from sklearn.linear_model import LogisticRegression

    from data_lab.testbeds.t1_tabular import TabularGenerator

    gen = TabularGenerator(d=3, rho=0.3)
    est = []
    for s in range(seeds):
        rng = np.random.default_rng(2_000 + s)
        z, y = gen.sample_with_prior(4_000, train_prior, rng)
        model = LogisticRegression(C=np.inf).fit(z, y)
        z_new, _ = gen.sample_with_prior(5_000, new_prior, rng)
        est.append(em_prior(model.predict_proba(z_new)[:, 1], train_prior))
    return np.array(est)


def smote_gap_experiment(ks=(1, 3, 5, 9, 12, 15, 19), n_minority: int = 20, sep: float = 4.0,
                         seeds: int = 50):
    """Share of SMOTE's synthetic points in the gap |x_1| < 2 between the two minority
    clusters, by neighbor count k, over seeds. Returns (ks, shares (seeds, len(ks)), true
    minority share of the gap)."""
    from scipy import stats

    true_share = 2 * 0.5 * (stats.norm.cdf(2, -sep, 1) - stats.norm.cdf(-2, -sep, 1))
    shares = np.zeros((seeds, len(ks)))
    for s in range(seeds):
        for j, k in enumerate(ks):
            rng = np.random.default_rng(3_000 + s)
            x = minority_sample(n_minority, sep, rng)
            synthetic = smote(x, 2_000, k, rng)
            shares[s, j] = np.mean(np.abs(synthetic[:, 0]) < 2)
    return np.array(ks), shares, float(true_share)


def importance_weighting_experiment(shifts=(0.0, 0.5, 1.0, 1.5, 2.0), n: int = 1_000,
                                    seeds: int = 500):
    """Estimate the 0-1 risk under p = N(delta e_1, Sigma) of T1's Bayes rule from samples of
    q = N(0, Sigma), with the exact density ratio as weights. Returns a dict of arrays over
    shifts: truth, iw (seeds x shifts), naive (seeds x shifts), second_moment E_q[w^2]."""
    from data_lab.testbeds.t1_tabular import TabularGenerator

    gen = TabularGenerator(d=3, rho=0.3)
    deltas = [np.array([s, 0.0, 0.0]) for s in shifts]
    truth = np.array([gen.threshold_risk(0.5, shift=d) for d in deltas])
    iw = np.zeros((seeds, len(shifts)))
    naive = np.zeros((seeds, len(shifts)))
    for k in range(seeds):
        rng = np.random.default_rng(12_000 + k)
        z = gen.sample_z(n, rng)
        y = gen.sample_labels(z, rng)
        loss = ((gen.score(z) > 0).astype(int) != y).astype(float)
        for j, d in enumerate(deltas):
            iw[k, j] = np.mean(gen.density_ratio(z, d) * loss)
            naive[k, j] = loss.mean()
    moments = np.array([gen.density_ratio_second_moment(d) for d in deltas])
    return {"shifts": np.array(shifts), "truth": truth, "iw": iw, "naive": naive,
            "second_moment": moments}
