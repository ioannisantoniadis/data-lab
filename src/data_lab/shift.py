"""Distribution shift (chapter 10): the taxonomy, and detecting shift from inputs alone.

Taxonomy (Moreno-Torres et al. 2012, Pattern Recognition 45, Definitions 1-4, read in the
reprint in Moreno-Torres's 2013 thesis): covariate shift, P(y | x) unchanged and P(x) changed
(X -> Y problems); prior probability shift, P(x | y) unchanged and P(y) changed (Y -> X
problems); concept shift, the conditional changes while the other marginal does not.

Classifier two-sample test (Lopez-Paz and Oquab 2016, arXiv 1610.06545): label the reference
sample 0 and the new sample 1, fit a classifier on half of each, and test whether its scores
on the held-out halves separate the two. Here the test is a one-sided Mann-Whitney U test on
the held-out scores (scipy.stats.mannwhitneyu), which is valid under the null because the
held-out scores of the two samples are then exchangeable.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def classifier_two_sample_test(reference: np.ndarray, new: np.ndarray,
                               rng: np.random.Generator) -> float:
    """p-value of a classifier two-sample test (logistic regression with squared features, so
    that changes in spread as well as location can be seen)."""
    from sklearn.linear_model import LogisticRegression

    def features(x):
        return np.hstack([x, x**2])

    a, b = rng.permutation(len(reference)), rng.permutation(len(new))
    ha, hb = len(a) // 2, len(b) // 2
    x_fit = np.vstack([reference[a[:ha]], new[b[:hb]]])
    y_fit = np.r_[np.zeros(ha), np.ones(hb)]
    model = LogisticRegression(C=1.0, max_iter=1_000).fit(features(x_fit), y_fit)
    s_ref = model.decision_function(features(reference[a[ha:]]))
    s_new = model.decision_function(features(new[b[hb:]]))
    return float(stats.mannwhitneyu(s_new, s_ref, alternative="greater").pvalue)


def ks_test_min(reference: np.ndarray, new: np.ndarray) -> float:
    """Bonferroni-corrected p-value of per-feature two-sample Kolmogorov-Smirnov tests."""
    p = [stats.ks_2samp(reference[:, j], new[:, j]).pvalue for j in range(reference.shape[1])]
    return float(min(1.0, min(p) * reference.shape[1]))


def accuracy_drop_test(correct_ref: np.ndarray, correct_new: np.ndarray) -> float:
    """One-sided two-proportion z-test that accuracy on new labeled data is lower."""
    n1, n2 = len(correct_ref), len(correct_new)
    p1, p2 = correct_ref.mean(), correct_new.mean()
    pooled = (correct_ref.sum() + correct_new.sum()) / (n1 + n2)
    se = np.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    return float(stats.norm.sf((p1 - p2) / se)) if se > 0 else 1.0


def shift_detection_experiment(n: int = 500, seeds: int = 200, alpha: float = 0.05,
                               shifts=(0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4)):
    """Rejection rates at level alpha on T1 for: no shift; covariate shift (mean of z_1 moved
    by 0.1, 0.2, 0.3); prior shift (class-1 share 0.5 -> 0.3, class-conditionals unchanged);
    concept shift (same inputs, labels from a different rule, u = (0.5, -1, 1.5) instead of
    (1.5, -1, 0.5)).

    Returns {scenario: (c2st rate, ks rate, labeled-accuracy-drop rate)}. The labeled test
    compares a model trained on reference data on n labeled reference and n labeled new
    examples; it is reported for "none" and "concept".
    """
    from sklearn.linear_model import LogisticRegression

    from data_lab.testbeds.t1_tabular import TabularGenerator

    gen = TabularGenerator(d=3, rho=0.3)
    other_rule = TabularGenerator(d=3, rho=0.3, u=np.array([0.5, -1.0, 1.5]))
    scenarios = ["none", *[f"covariate {s}" for s in shifts], "prior", "concept"]
    hits = {s: [0, 0, 0] for s in scenarios}
    for k in range(seeds):
        rng = np.random.default_rng(10_000 + k)
        ref = gen.sample_z(n, rng)
        y_ref = gen.sample_labels(ref, rng)
        model = LogisticRegression(C=np.inf).fit(ref, y_ref)
        z_hold = gen.sample_z(n, rng)
        correct_ref = model.predict(z_hold) == gen.sample_labels(z_hold, rng)
        for s in scenarios:
            if s.startswith("covariate"):
                new = gen.sample_z(n, rng, shift=[float(s.split()[1]), 0.0, 0.0])
            elif s == "prior":
                new, _ = gen.sample_with_prior(n, 0.3, rng)
            else:  # "none" and "concept" draw inputs from the same p(x)
                new = gen.sample_z(n, rng)
            hits[s][0] += classifier_two_sample_test(ref, new, rng) < alpha
            hits[s][1] += ks_test_min(ref, new) < alpha
            if s in ("none", "concept"):
                labeler = other_rule if s == "concept" else gen
                correct_new = model.predict(new) == labeler.sample_labels(new, rng)
                hits[s][2] += accuracy_drop_test(correct_ref, correct_new) < alpha
    return {s: tuple(h / seeds for h in v) for s, v in hits.items()}
