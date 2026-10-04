"""T4 ground truths: stationarity, the entropy rate by brute-force enumeration, the
cross-entropy floor, and exact duplicate bookkeeping."""

import itertools

import numpy as np
import pytest

from data_lab.testbeds.t4_markov_text import (
    MarkovSource,
    bigram_counts,
    inject_duplicates,
    per_token_nll,
)


def test_transition_is_stochastic_and_pi_is_stationary():
    src = MarkovSource(vocab=30, zipf_s=1.2, lam=0.8)
    p, pi, q = src.transition, src.stationary, src.metropolis
    np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-14)
    assert np.all(p > 0)
    np.testing.assert_allclose(pi @ p, pi, atol=1e-15)
    np.testing.assert_allclose(pi[:, None] * q, (pi[:, None] * q).T, atol=1e-16)  # detailed balance
    w = np.arange(1, 31, dtype=float) ** -1.2
    np.testing.assert_allclose(pi, w / w.sum())


def test_entropy_rate_by_brute_force_enumeration():
    """H(X_1..X_L) = H(pi) + (L - 1) h, by summing over all V^L sequences (V = 4, L = 5)."""
    src = MarkovSource(vocab=4, zipf_s=1.0, lam=0.6)
    p, pi = src.transition, src.stationary
    length = 5
    joint_entropy = 0.0
    for seq in itertools.product(range(4), repeat=length):
        prob = pi[seq[0]] * np.prod([p[a, b] for a, b in itertools.pairwise(seq)])
        joint_entropy -= prob * np.log(prob)
    h_pi = -np.sum(pi * np.log(pi))
    assert joint_entropy == pytest.approx(h_pi + (length - 1) * src.entropy_rate, rel=1e-12)


def test_no_model_beats_the_entropy_rate():
    src = MarkovSource(vocab=20, lam=0.7)
    rng = np.random.default_rng(0)
    assert src.cross_entropy(src.transition) == pytest.approx(src.entropy_rate, rel=1e-12)
    for _ in range(20):
        m = rng.dirichlet(np.ones(20), size=20)
        assert src.cross_entropy(m) > src.entropy_rate
    unigram = np.tile(src.stationary, (20, 1))
    assert src.cross_entropy(unigram) > src.entropy_rate  # lam > 0: context helps


def test_sampled_text_has_the_source_statistics():
    src = MarkovSource(vocab=20, lam=0.7)
    docs = src.sample(2_000, 200, np.random.default_rng(1))
    freq = np.bincount(docs.ravel(), minlength=20) / docs.size
    np.testing.assert_allclose(freq, src.stationary, atol=0.003)
    counts = bigram_counts(docs, 20)
    np.testing.assert_allclose(counts / counts.sum(axis=1, keepdims=True), src.transition,
                               atol=0.02)
    assert per_token_nll(docs, src.transition) == pytest.approx(src.entropy_rate, rel=0.005)


def test_duplicate_injection_is_exact():
    src = MarkovSource(vocab=10)
    rng = np.random.default_rng(2)
    docs = src.sample(500, 30, rng)
    corpus, origin = inject_duplicates(docs, n_duplicated=20, copies=3, rng=rng)
    assert len(corpus) == 500 + 60
    np.testing.assert_array_equal(corpus, docs[origin])
    counts = np.bincount(origin, minlength=500)
    assert (counts == 4).sum() == 20 and (counts == 1).sum() == 480
