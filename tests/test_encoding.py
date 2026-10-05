"""Claim tests: Part II, encodings and features (claims 32-35, added in Phase 2 for chapter 7).
Library behavior is exercised against the documented formulas (SPEC §12.5)."""

import numpy as np
import pytest
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import KBinsDiscretizer, OneHotEncoder, OrdinalEncoder, SplineTransformer


def test_ordinal_codes_impose_an_order_one_hot_does_not():
    """Claim 32. A category whose effect on y is not monotone in its (arbitrary) code: a linear
    model on the ordinal code explains little of it, the same model on a one-hot encoding
    recovers every level's effect (test R^2 near the noise ceiling)."""
    rng = np.random.default_rng(32)
    effects = np.array([0.0, 3.0, -2.0, 1.0, -3.0, 2.0])
    cat = rng.integers(0, 6, 4_000)[:, None]
    y = effects[cat[:, 0]] + 0.5 * rng.standard_normal(4_000)
    tr, te = slice(0, 2_000), slice(2_000, 4_000)
    scores = {}
    for name, enc in (("ordinal", OrdinalEncoder()), ("onehot", OneHotEncoder())):
        model = make_pipeline(enc, LinearRegression()).fit(cat[tr], y[tr])
        scores[name] = model.score(cat[te], y[te])
    ceiling = effects.var() / (effects.var() + 0.25)
    assert scores["onehot"] == pytest.approx(ceiling, abs=0.02)
    assert scores["ordinal"] < 0.2


def test_feature_hashing_collides_at_the_expected_rate():
    """Claim 33. Hashing k distinct categories into m columns leaves about
    m (1 - (1 - 1/m)^k) columns in use, the expected number of occupied buckets for a uniform
    hash, so distinct categories share columns (collide) once k is not small against m."""
    k = 2_000
    names = [[f"category_{i}"] for i in range(k)]
    for m in (256, 1_024, 8_192):
        hashed = FeatureHasher(n_features=m, input_type="string", alternate_sign=False)
        used = np.unique(hashed.transform(names).nonzero()[1]).size
        expected = m * (1 - (1 - 1 / m) ** k)
        assert abs(used - expected) < 4 * np.sqrt(expected)
    assert used < k  # even at m = 8,192, some of the 2,000 categories collide


def test_splines_and_bins_let_a_linear_model_fit_a_curve():
    """Claim 34. On y = sin(2 x) + noise, a linear model on raw x explains little; the same
    model on a cubic spline basis (SplineTransformer, 8 knots) or on quantile bins
    (KBinsDiscretizer, 20 bins, one-hot) reaches near the noise ceiling, the splines closer;
    and quantile bins hold nearly equal counts."""
    rng = np.random.default_rng(34)
    x = rng.uniform(-3, 3, (4_000, 1))
    y = np.sin(2 * x[:, 0]) + 0.3 * rng.standard_normal(4_000)
    tr, te = slice(0, 2_000), slice(2_000, 4_000)
    ceiling = 1 - 0.09 / y.var()
    raw = LinearRegression().fit(x[tr], y[tr]).score(x[te], y[te])
    spline = make_pipeline(SplineTransformer(n_knots=8), LinearRegression())
    bins = make_pipeline(KBinsDiscretizer(n_bins=20, strategy="quantile"), LinearRegression())
    s_score = spline.fit(x[tr], y[tr]).score(x[te], y[te])
    b_score = bins.fit(x[tr], y[tr]).score(x[te], y[te])
    assert raw < 0.2
    assert s_score > ceiling - 0.03 and b_score > ceiling - 0.08 and s_score > b_score
    codes = KBinsDiscretizer(n_bins=20, strategy="quantile", encode="ordinal").fit_transform(x)
    counts = np.bincount(codes[:, 0].astype(int))
    assert counts.max() - counts.min() <= 2


def test_tfidf_matches_the_documented_formula():
    """Claim 35. TfidfVectorizer's default output equals the formula in its documentation:
    tf(t, d) * (ln((1 + n) / (1 + df(t))) + 1), each document's vector scaled to unit length."""
    docs = ["the cat sat", "the dog sat", "the cat ate the fish", "a dog"]
    vec = TfidfVectorizer()
    out = vec.fit_transform(docs).toarray()
    vocab = vec.get_feature_names_out()
    tokens = [d.split() for d in docs]
    tf = np.array([[toks.count(t) for t in vocab] for toks in tokens], dtype=float)
    df = (tf > 0).sum(axis=0)
    n = len(docs)
    raw = tf * (np.log((1 + n) / (1 + df)) + 1)
    expected = raw / np.linalg.norm(raw, axis=1, keepdims=True)
    np.testing.assert_allclose(out, expected, rtol=1e-12)
