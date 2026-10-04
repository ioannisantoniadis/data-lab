"""T4: a Markov text source with Zipf-like unigram frequencies and a known transition matrix.

Construction: the stationary (unigram) distribution is exactly pi_i proportional to i^-s over a
vocabulary of V tokens. The transition matrix is a mixture

    P = (1 - lam) 1 pi'  +  lam Q,

where Q is a Metropolis chain with a uniform proposal targeting pi: Q_ij = min(pi_i, pi_j) /
(V pi_i) for j != i, and the remaining mass on the diagonal. Q satisfies detailed balance with
respect to pi, so pi Q = pi, and therefore pi P = pi. ``lam`` sets how much each token depends
on the previous one (lam = 0: i.i.d. unigrams).

Ground truth, exactly:

- the entropy rate h = -sum_i pi_i sum_j P_ij log P_ij (nats per token) for a chain started
  from pi. A test checks it by brute-force enumeration: H(X_1..X_L) = H(pi) + (L - 1) h;
- hence the cross-entropy floor: for any model M of the transitions, the expected per-token
  cross-entropy -sum_i pi_i sum_j P_ij log M_ij is at least h (Gibbs' inequality);
- duplicate counts, because duplicates are injected by construction.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MarkovSource:
    vocab: int = 50
    zipf_s: float = 1.1
    lam: float = 0.7

    @property
    def stationary(self) -> np.ndarray:
        w = np.arange(1, self.vocab + 1, dtype=float) ** (-self.zipf_s)
        return w / w.sum()

    @property
    def metropolis(self) -> np.ndarray:
        pi = self.stationary
        q = np.minimum.outer(pi, pi) / (self.vocab * pi[:, None])
        np.fill_diagonal(q, 0.0)
        np.fill_diagonal(q, 1.0 - q.sum(axis=1))
        return q

    @property
    def transition(self) -> np.ndarray:
        pi = self.stationary
        return (1 - self.lam) * np.tile(pi, (self.vocab, 1)) + self.lam * self.metropolis

    @property
    def entropy_rate(self) -> float:
        p = self.transition
        return float(-np.sum(self.stationary[:, None] * p * np.log(p)))

    def cross_entropy(self, model: np.ndarray) -> float:
        """Expected per-token cross-entropy (nats) of a transition model M under the source."""
        p = self.transition
        return float(-np.sum(self.stationary[:, None] * p * np.log(model)))

    def sample(self, n_docs: int, length: int, rng: np.random.Generator) -> np.ndarray:
        """n_docs independent documents of ``length`` tokens, each started from pi."""
        cum = np.cumsum(self.transition, axis=1)
        docs = np.empty((n_docs, length), dtype=np.int64)
        docs[:, 0] = rng.choice(self.vocab, size=n_docs, p=self.stationary)
        for t in range(1, length):
            u = rng.random(n_docs)[:, None]
            docs[:, t] = np.minimum((u > cum[docs[:, t - 1]]).sum(axis=1), self.vocab - 1)
        return docs


def inject_duplicates(
    docs: np.ndarray, n_duplicated: int, copies: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Append ``copies`` extra exact copies of ``n_duplicated`` randomly chosen documents.

    Returns the shuffled corpus and, for each row, the index of its original document, so every
    duplicate is known exactly.
    """
    chosen = rng.choice(len(docs), size=n_duplicated, replace=False)
    origin = np.r_[np.arange(len(docs)), np.repeat(chosen, copies)]
    order = rng.permutation(origin.size)
    return docs[origin[order]], origin[order]


def bigram_counts(docs: np.ndarray, vocab: int) -> np.ndarray:
    counts = np.zeros((vocab, vocab))
    np.add.at(counts, (docs[:, :-1].ravel(), docs[:, 1:].ravel()), 1.0)
    return counts


def per_token_nll(docs: np.ndarray, model: np.ndarray) -> float:
    """Average negative log-likelihood (nats) of the transitions in ``docs`` under ``model``."""
    return float(-np.mean(np.log(model[docs[:, :-1], docs[:, 1:]])))
