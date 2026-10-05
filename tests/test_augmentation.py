"""Claim tests: Part III, augmentation (SPEC §8 claims 13 and 38; T5)."""

import numpy as np
import pytest

from data_lab.augment import augmentation_experiment, mixup


@pytest.fixture(scope="module")
def results():
    return augmentation_experiment()


def test_invariant_augmentation_helps_noninvariant_hurts(results):
    """Claim 13. On T5's side task (20 seeds, logistic regression), augmenting with a transform
    the true function is invariant to (up-down flip) does not hurt at any training size and
    helps at small n (+0.02 or more at n = 10 and 20); augmenting with a transform it is not
    invariant to, keeping the label (left-right flip), hurts at every size (by 0.1 or more)."""
    none = np.nanmean(results["none"], axis=0)
    inv = np.nanmean(results["invariant"], axis=0)
    wrong = np.nanmean(results["wrong_label"], axis=0)
    assert np.all(inv >= none - 0.005)
    assert np.all(inv[:2] - none[:2] >= 0.02)
    assert np.all(none - wrong >= 0.1)


def test_label_changing_augmentation_helps_when_the_change_is_known(results):
    """Claim 38 (added in Phase 3 for chapter 9). The same left-right flip, with the label
    reversed as the flip truly reverses it, helps at every training size, more than the
    invariant flip at small n: a label-changing augmentation is valid when its effect on the
    label is known."""
    none = np.nanmean(results["none"], axis=0)
    inv = np.nanmean(results["invariant"], axis=0)
    changing = np.nanmean(results["label_changing"], axis=0)
    assert np.all(changing > none)
    assert np.all(changing[:3] > inv[:3])


def test_mixup_forms_the_same_convex_combination_of_inputs_and_labels():
    """mixup as defined by Zhang et al. (2017, §2): the mixed input and the mixed label are the
    same convex combination, with lam ~ Beta(alpha, alpha) (mean 1/2, variance
    1 / (4 (2 alpha + 1)))."""
    rng = np.random.default_rng(9)
    x = rng.standard_normal((20_000, 3))
    y = np.eye(2)[rng.integers(0, 2, 20_000)]
    xm, ym, lam, partner = mixup(x, y, 0.4, rng)
    np.testing.assert_allclose(xm, lam[:, None] * x + (1 - lam[:, None]) * x[partner])
    np.testing.assert_allclose(ym, lam[:, None] * y + (1 - lam[:, None]) * y[partner])
    assert lam.mean() == pytest.approx(0.5, abs=0.01)
    assert lam.var() == pytest.approx(1 / (4 * (2 * 0.4 + 1)), rel=0.05)
