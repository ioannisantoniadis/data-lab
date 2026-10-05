"""Claim tests: Part IV, model collapse (SPEC §8 claim 20; T2)."""

import numpy as np
import pytest

from data_lab.selection import collapse_experiment, downstream_error
from data_lab.testbeds.t2_zipf import ZipfStream


@pytest.fixture(scope="module")
def runs():
    return collapse_experiment()


def test_refitting_on_own_samples_loses_tail(runs):
    """Claim 20. Repeatedly refitting a generator on samples from its previous fit (the replace
    regime) loses the tail of T2's distribution: the p-mass outside its support grows in every
    generation on average, and after 10 generations exceeds twice the generation-0 loss. The
    generation-0 loss equals Hutter's expected error at the generator's sample size, within 4
    standard errors (20 seeds, t0 = 10,000). Accumulating real and synthetic data keeps the
    loss at its generation-0 value (Gerstgrasser et al. 2024's contrast)."""
    rep, acc = runs["replace"], runs["accumulate"]
    mean = rep.mean(axis=0)
    assert np.all(np.diff(mean) > 0)
    assert mean[-1] > 2 * mean[0]
    exact = ZipfStream(1.0).expected_error(10_000).mid
    se = rep[:, 0].std(ddof=1) / np.sqrt(rep.shape[0])
    assert abs(mean[0] - exact) < 4 * se
    np.testing.assert_allclose(acc, acc[:, :1] * np.ones_like(acc))


def test_training_on_generated_data_plateaus_at_the_lost_mass():
    """With a generator fit once to t0 real draws, a learner trained on t generated draws has
    error at least the lost mass and approaching it as t grows (a plateau, as Dohmatob et al.
    2024 derive for this model), while the error on t real draws keeps falling below it."""
    stream = ZipfStream(1.0)
    rng = np.random.default_rng(0)
    feats, counts = np.unique(stream.sample(10_000, rng), return_counts=True)
    probs = counts / counts.sum()
    lost = 1.0 - stream.p(feats).sum()
    synthetic = [downstream_error(stream, feats, probs, t) for t in (1e4, 1e6, 1e8)]
    real = [stream.expected_error(t).mid for t in (1e4, 1e6, 1e8)]
    assert all(e >= lost for e in synthetic)
    assert synthetic[-1] - lost < 1e-6
    assert real[-1] < lost / 10
