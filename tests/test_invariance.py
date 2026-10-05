"""Claim tests: Part II, which models care about which transforms (SPEC §8 claims 2-3; T1)."""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from data_lab.testbeds.t1_tabular import TabularGenerator

MONOTONE = {
    "affine": lambda a: 3.0 * a + 5.0,
    "log": np.log,
    "sqrt": np.sqrt,
    "cube": lambda a: a**3,
}


def _tree(x, y):
    return DecisionTreeClassifier(max_depth=5, random_state=0).fit(x, y)


def test_tree_thresholds_are_midpoints_within_each_node():
    """Library behavior the invariance argument rests on (scikit-learn 1.9, checked rather than
    recalled): every split threshold lies halfway between the two adjacent values of that
    feature among the training samples reaching the node (in float32, which trees use)."""
    gen = TabularGenerator(d=3, rho=0.3, skewed=True)
    rng = np.random.default_rng(2)
    z = gen.sample_z(800, rng)
    x, y = gen.features(z), gen.sample_labels(z, rng)
    tree = _tree(x, y)
    paths = tree.decision_path(x).toarray().astype(bool)
    xs = x.astype(np.float32).astype(np.float64)
    for node in np.flatnonzero(tree.tree_.feature >= 0):
        f, thr = tree.tree_.feature[node], tree.tree_.threshold[node]
        vals = xs[paths[:, node], f]
        below, above = vals[vals <= thr].max(), vals[vals > thr].min()
        assert np.isclose(thr, (below + above) / 2, rtol=1e-6)


def test_tree_predictions_invariant_to_monotone_feature_transform():
    """Claim 2 (refined in Phase 2). A decision tree's predictions on its training points are
    unchanged by any strictly increasing transform of the features (same tie-breaking: same
    random_state), because the transform keeps every ordering and so every candidate split.
    On new points, an increasing affine transform also keeps every prediction, but a nonlinear
    one can change the few that fall between the two training values a threshold separates:
    the threshold sits at their midpoint, and a nonlinear map does not keep midpoints. Measured
    over 10 seeds: at most 0.16% of 20,000 new points per seed (largest for the cube); tested
    against 0.3%."""
    gen = TabularGenerator(d=3, rho=0.3, skewed=True)
    for s in range(10):
        rng = np.random.default_rng(2_000 + s)
        z = gen.sample_z(800, rng)
        x, y = gen.features(z), gen.sample_labels(z, rng)
        x_new = gen.features(gen.sample_z(20_000, rng))
        base = _tree(x, y)
        for name, fn in MONOTONE.items():
            other = _tree(fn(x), y)
            np.testing.assert_array_equal(base.predict(x), other.predict(fn(x)))
            disagree = np.mean(base.predict(x_new) != other.predict(fn(x_new)))
            if name == "affine":
                assert disagree == 0.0
            else:
                assert disagree <= 3e-3


def test_knn_prediction_flips_under_feature_rescaling():
    """Claim 3. k-NN predictions change under per-feature rescaling. A constructed flip: the
    query (0, 0) has neighbor A = (1, 0), class 0, at distance 1 and B = (0, 10), class 1, at
    distance 10; dividing the second feature by 100 puts B at 0.1, and the 1-NN prediction
    flips. On T1, inflating one informative feature's scale by 100 lowers 15-NN accuracy far
    below that on standardized features (20 seeds)."""
    x = np.array([[1.0, 0.0], [0.0, 10.0]])
    y = np.array([0, 1])
    query = np.array([[0.0, 0.0]])
    assert KNeighborsClassifier(1).fit(x, y).predict(query)[0] == 0
    scale = np.array([1.0, 0.01])
    assert KNeighborsClassifier(1).fit(x * scale, y).predict(query * scale)[0] == 1

    gen = TabularGenerator(d=3, rho=0.3)
    raw_acc, std_acc = [], []
    for s in range(20):
        rng = np.random.default_rng(3_000 + s)
        z = gen.sample_z(2_000, rng)
        y = gen.sample_labels(z, rng)
        x = z * np.array([1.0, 1.0, 100.0])  # the third feature, weight 0.5, on a huge scale
        tr, te = slice(0, 1_000), slice(1_000, 2_000)
        raw_acc.append(KNeighborsClassifier(15).fit(x[tr], y[tr]).score(x[te], y[te]))
        sc = StandardScaler().fit(x[tr])
        model = KNeighborsClassifier(15).fit(sc.transform(x[tr]), y[tr])
        std_acc.append(model.score(sc.transform(x[te]), y[te]))
    assert np.mean(std_acc) - np.mean(raw_acc) > 0.05
    assert np.mean(std_acc) > 1 - gen.bayes_risk() - 0.05
