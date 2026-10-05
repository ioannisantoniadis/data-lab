"""Part IV: choosing data (chapter 14). The coverage-driven selectors of chapter 13 live in
testbeds/t2_zipf.py; this module holds the chapter 14 experiments:

- pruning by teacher margin on T3 (Sorscher et al. 2022's setting);
- deduplication on T4 with a trigram model that can memorize documents;
- pool-based active learning by uncertainty sampling on T1 (Settles 2009, §3.1);
- model collapse on T2, replacing vs accumulating data (Dohmatob et al. 2024;
  Gerstgrasser et al. 2024).
"""

from __future__ import annotations

import numpy as np

# --- chapter 14 experiments, shared by tests, figures and published numbers --------------------


def pruning_experiment(ratios=(1.0, 2.0, 4.0, 8.0, 16.0), keep_fraction: float = 0.5,
                       dim: int = 100, seeds: int = 20):
    """Sorscher et al.'s setting on T3: from P = ratio * dim teacher-labeled examples, keep the
    hardest or easiest half by teacher margin (probe angle 0), or a random half, and train the
    max-margin student. Returns {"hard" | "easy" | "random": array (seeds, len(ratios))} of
    exact test errors."""
    from data_lab.testbeds.t3_teacher_student import make_problem, max_margin, prune

    out = {k: np.zeros((seeds, len(ratios))) for k in ("hard", "easy", "random")}
    for s in range(seeds):
        for j, ratio in enumerate(ratios):
            rng = np.random.default_rng(17_000 + s)
            prob = make_problem(dim, rng)
            x, y = prob.sample(int(ratio * dim), rng)
            probe = prob.probe(0.0, rng)
            for keep in ("hard", "easy"):
                xs, ys = prune(x, y, probe, keep_fraction, keep)
                out[keep][s, j] = prob.test_error(max_margin(xs, ys).weights)
            idx = rng.permutation(len(y))[: int(round(keep_fraction * len(y)))]
            out["random"][s, j] = prob.test_error(max_margin(x[idx], y[idx]).weights)
    return out


def trigram_model(docs: np.ndarray, vocab: int, smoothing: float = 0.01) -> np.ndarray:
    counts = np.zeros((vocab, vocab, vocab))
    np.add.at(counts, (docs[:, :-2].ravel(), docs[:, 1:-1].ravel(), docs[:, 2:].ravel()), 1.0)
    counts += smoothing
    return counts / counts.sum(axis=2, keepdims=True)


def trigram_nll(docs: np.ndarray, model: np.ndarray) -> float:
    return float(-np.mean(np.log(model[docs[:, :-2], docs[:, 1:-1], docs[:, 2:]])))


def dedup_experiment(seeds: int = 20, n_docs: int = 400, length: int = 50,
                     n_duplicated: int = 50, copies: int = 5):
    """T4 with injected duplicates (n_duplicated documents copied ``copies`` extra times), an
    80/20 document split, and a trigram model that can memorize. Returns a dict of arrays over
    seeds: "contaminated" (test NLL on the split with duplicates), "dedup" (test NLL after
    removing duplicates before splitting), "fresh" (NLL of each model on new documents from the
    source; "fresh_dedup" for the deduplicated model) and "overlap" (share of contaminated test
    documents also in training), plus the entropy rate."""
    from data_lab.testbeds.t4_markov_text import MarkovSource, inject_duplicates

    src = MarkovSource(vocab=20, zipf_s=1.1, lam=0.7)
    out: dict[str, list] = {k: [] for k in ("contaminated", "dedup", "fresh", "fresh_dedup",
                                             "overlap")}
    for s in range(seeds):
        rng = np.random.default_rng(18_000 + s)
        docs = src.sample(n_docs, length, rng)
        corpus, origin = inject_duplicates(docs, n_duplicated, copies, rng)
        perm = rng.permutation(len(corpus))
        cut = int(0.8 * len(perm))
        train, test = perm[:cut], perm[cut:]
        model = trigram_model(corpus[train], src.vocab)
        _, first = np.unique(origin, return_index=True)
        unique = corpus[first]
        perm2 = rng.permutation(len(unique))
        cut2 = int(0.8 * len(perm2))
        model2 = trigram_model(unique[perm2[:cut2]], src.vocab)
        fresh = src.sample(n_docs, length, rng)
        out["contaminated"].append(trigram_nll(corpus[test], model))
        out["dedup"].append(trigram_nll(unique[perm2[cut2:]], model2))
        out["fresh"].append(trigram_nll(fresh, model))
        out["fresh_dedup"].append(trigram_nll(fresh, model2))
        out["overlap"].append(np.mean(np.isin(origin[test], origin[train])))
    res = {k: np.array(v) for k, v in out.items()}
    res["entropy_rate"] = src.entropy_rate
    return res


def active_learning_experiment(scale: float, seeds: int = 20, budget: int = 100,
                               start: int = 10, pool: int = 3_000, checkpoints=(20, 40, 100)):
    """Pool-based learning on T1 with logistic regression (C = 1): label ``start`` random
    examples, then add one at a time either at random or by uncertainty sampling (the pool
    example whose predicted probability is nearest 1/2; Settles 2009, §3.1). ``scale``
    multiplies the true coefficients: large = nearly separable, 1 = noisy labels. Returns
    {"random" | "uncertainty": array (seeds, len(checkpoints))} of the share of inputs on which
    the learned rule disagrees with the Bayes rule (estimated on 100,000 fresh inputs)."""
    from sklearn.linear_model import LogisticRegression

    from data_lab.testbeds.t1_tabular import TabularGenerator

    gen = TabularGenerator(d=3, rho=0.3, u=np.array([1.5, -1.0, 0.5]) * scale)
    probe = gen.sample_z(100_000, np.random.default_rng(1))
    bayes = gen.posterior(probe) > 0.5
    out = {k: np.zeros((seeds, len(checkpoints))) for k in ("random", "uncertainty")}
    for strategy in out:
        for s in range(seeds):
            rng = np.random.default_rng(43_000 + s)
            x = gen.sample_z(pool, rng)
            y = gen.sample_labels(x, rng)
            labeled = list(rng.choice(pool, start, replace=False))
            while len(labeled) <= budget:
                if len(set(y[labeled])) < 2:
                    labeled.append(int(rng.integers(pool)))
                    continue
                model = LogisticRegression(C=1.0).fit(x[labeled], y[labeled])
                if len(labeled) in checkpoints:
                    j = checkpoints.index(len(labeled))
                    out[strategy][s, j] = np.mean(model.predict(probe) != bayes)
                rest = np.setdiff1d(np.arange(pool), labeled)
                if strategy == "random":
                    labeled.append(int(rng.choice(rest)))
                else:
                    p = model.predict_proba(x[rest])[:, 1]
                    labeled.append(int(rest[np.argmin(np.abs(p - 0.5))]))
    return out


def collapse_experiment(alpha: float = 1.0, t0: int = 10_000, generations: int = 10,
                        seeds: int = 20):
    """Model collapse on T2 (replace vs accumulate). Generation 0 is t0 draws from p; each
    generator is the empirical distribution of its training data, and the next generation is t0
    draws from it. "replace": each generator trains on the previous generation only;
    "accumulate": on all data so far, real data included. Returns {"replace" | "accumulate":
    array (seeds, generations)} of the p-mass outside each generator's support (the error floor
    of any memorizer trained on its output)."""
    from data_lab.testbeds.t2_zipf import ZipfStream

    stream = ZipfStream(alpha)
    out = {k: np.zeros((seeds, generations)) for k in ("replace", "accumulate")}
    for mode in out:
        for s in range(seeds):
            rng = np.random.default_rng(20_000 + s)
            pool = [stream.sample(t0, rng)]
            for g in range(generations):
                train = np.concatenate(pool) if mode == "accumulate" else pool[-1]
                feats, counts = np.unique(train, return_counts=True)
                out[mode][s, g] = 1.0 - stream.p(feats).sum()
                pool.append(rng.choice(feats, size=t0, p=counts / counts.sum()))
    return out


def downstream_error(stream, feats: np.ndarray, probs: np.ndarray, t: float) -> float:
    """Exact expected error, under p, of a memorizer trained on t draws from a generator with
    support ``feats`` and probabilities ``probs``: mass outside the support plus, inside it,
    p_i (1 - q_i)^t."""
    p_in = stream.p(feats)
    return float((1.0 - p_in.sum()) + np.sum(p_in * np.exp(t * np.log1p(-probs))))
