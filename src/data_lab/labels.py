"""Labels (chapter 2): class-conditional label noise and confident learning.

Noise model (binary): a class-conditional process flips each label independently of x, with
rho_0 = P(noisy = 1 | true = 0) and rho_1 = P(noisy = 0 | true = 1); Northcutt et al. 2021
(arXiv 1911.00068, §2, "Assumptions") use this class-conditional assumption for m classes.

By total probability, the noisy posterior is an affine function of the clean one,

    P(noisy = 1 | x) = rho_0 + (1 - rho_0 - rho_1) eta(x),   eta(x) = P(true = 1 | x),

so a model fit to noisy labels learns this, not eta. Thresholding it at 1/2 is the same as
thresholding eta at (1/2 - rho_0) / (1 - rho_0 - rho_1): the decision boundary moves unless
rho_0 = rho_1 (requires rho_0 + rho_1 < 1).

Confident learning, CL method 2 of Northcutt et al. (§3.1, eqs. 1-2; §3.2): with out-of-sample
predicted probabilities, the per-class threshold t_j is the average predicted probability of
class j over examples labeled j; an example labeled i is counted in confident-joint bin (i, j)
if its probability of class j is at least t_j (the largest such class if several qualify); the
off-diagonal bins are the estimated label errors.
"""

from __future__ import annotations

import numpy as np


def flip_labels(y: np.ndarray, rho0: float, rho1: float, rng: np.random.Generator):
    """Class-conditional noise for binary labels. Returns the noisy labels."""
    u = rng.random(len(y))
    flip = np.where(y == 1, u < rho1, u < rho0)
    return np.where(flip, 1 - y, y)


def noisy_posterior(eta, rho0: float, rho1: float):
    return rho0 + (1.0 - rho0 - rho1) * np.asarray(eta)


def clean_threshold(rho0: float, rho1: float) -> float:
    """The threshold on the clean posterior eta that thresholding the noisy one at 1/2 implies."""
    if not rho0 + rho1 < 1:
        raise ValueError("rho_0 + rho_1 must be below 1")
    return (0.5 - rho0) / (1.0 - rho0 - rho1)


def confident_joint_issues(labels: np.ndarray, probs: np.ndarray) -> np.ndarray:
    """CL method 2: True for examples in an off-diagonal bin of the confident joint.

    ``probs`` are out-of-sample predicted probabilities, shape (n, m); ``labels`` in 0..m-1.
    """
    n, m = probs.shape
    thresholds = np.array([probs[labels == j, j].mean() for j in range(m)])
    above = probs >= thresholds
    masked = np.where(above, probs, -np.inf)
    best = masked.argmax(axis=1)
    counted = above.any(axis=1)
    return counted & (best != labels)
