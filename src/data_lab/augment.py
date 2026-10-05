"""Augmentation (chapter 9): augmentation as an assumption about p, tested on T5's synthetic
side label, which is exactly invariant under an up-down flip and exactly reversed by a
left-right flip.

Augmenting a training set with transformed copies changes the training distribution q: it adds
the transformed inputs, with labels set by an assumption about how the transform acts on the
target. The assumption is either right (the augmented pairs are draws from p) or wrong (they
are mislabeled examples).

mixup (Zhang et al. 2017, arXiv 1710.09412, §2): x = lam x_i + (1 - lam) x_j and
y = lam y_i + (1 - lam) y_j with lam ~ Beta(alpha, alpha), a "vicinal" distribution around the
training pairs.
"""

from __future__ import annotations

import numpy as np

MODES = ("none", "invariant", "wrong_label", "label_changing")


def augment(images: np.ndarray, labels: np.ndarray, mode: str):
    """Return the augmented training set for one of MODES:

    - "none": the data as is;
    - "invariant": add up-down flips with the same labels (a true invariance);
    - "wrong_label": add left-right flips with the same labels (assumes an invariance that is
      false: the flip reverses the label);
    - "label_changing": add left-right flips with reversed labels (the true effect of the flip).
    """
    from data_lab.testbeds.t5_signals import flip_left_right, flip_up_down

    if mode == "none":
        return images, labels
    if mode == "invariant":
        return np.concatenate([images, flip_up_down(images)]), np.r_[labels, labels]
    if mode == "wrong_label":
        return np.concatenate([images, flip_left_right(images)]), np.r_[labels, labels]
    if mode == "label_changing":
        return np.concatenate([images, flip_left_right(images)]), np.r_[labels, 1 - labels]
    raise ValueError(mode)


def augmentation_experiment(sizes=(10, 20, 50, 100, 400), seeds: int = 20):
    """Test accuracy of a logistic regression (scikit-learn defaults, C = 1) on T5's side task
    for each training size and augmentation mode. Returns {mode: array (seeds, len(sizes))};
    a seed whose training set has one class only is recorded as NaN."""
    from sklearn.linear_model import LogisticRegression

    from data_lab.testbeds.t5_signals import side_task

    x, y = side_task()
    out = {m: np.full((seeds, len(sizes)), np.nan) for m in MODES}
    for s in range(seeds):
        order = np.random.default_rng(13_000 + s).permutation(len(y))
        for j, n in enumerate(sizes):
            train, test = order[:n], order[n:]
            for mode in MODES:
                xa, ya = augment(x[train], y[train], mode)
                if len(np.unique(ya)) < 2:
                    continue
                model = LogisticRegression(C=1.0, max_iter=2_000)
                model.fit(xa.reshape(len(xa), -1), ya)
                out[mode][s, j] = model.score(x[test].reshape(len(test), -1), y[test])
    return out


def mixup(x: np.ndarray, y: np.ndarray, alpha: float, rng: np.random.Generator):
    """One mixup batch: each example mixed with a random partner, with lam ~ Beta(alpha, alpha).
    ``y`` should be one-hot or a probability; returns (x_mixed, y_mixed, lam, partner)."""
    lam = rng.beta(alpha, alpha, size=len(x))
    partner = rng.permutation(len(x))
    shape = (-1,) + (1,) * (x.ndim - 1)
    x_mix = lam.reshape(shape) * x + (1 - lam.reshape(shape)) * x[partner]
    y_mix = lam[:, None] * y + (1 - lam[:, None]) * y[partner]
    return x_mix, y_mix, lam, partner
