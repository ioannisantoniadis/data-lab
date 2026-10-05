"""Claim tests: Part I, data types (claims 26-27, added in Phase 2 for chapter 3; T5)."""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score
from sklearn.neighbors import KNeighborsRegressor

from data_lab.testbeds.t5_signals import ar1_series, log_power_spectrum, tone_classes

FS = 8_000.0


def test_aliasing_is_exact_above_half_the_sampling_rate():
    """At 8 kHz, the samples of a 5 kHz sine are exactly those of a 3 kHz sine, sign-flipped:
    sin(2 pi 5 n / 8) = sin(2 pi n - 2 pi 3 n / 8) = -sin(2 pi 3 n / 8)."""
    n = np.arange(64)
    np.testing.assert_allclose(np.sin(2 * np.pi * 5_000 * n / FS),
                               -np.sin(2 * np.pi * 3_000 * n / FS), atol=1e-12)


def test_spectrogram_representation_makes_tone_classes_linearly_separable():
    """Claim 27. With random phases, a linear classifier on the raw waveform is at chance on
    two classes of noisy tones, while the same classifier on the log power spectrum (from the
    spectrogram) is near perfect: 5 seeds, 400 training and 400 test signals each."""
    raw, spec = [], []
    for s in range(5):
        rng = np.random.default_rng(27_000 + s)
        xtr, ytr = tone_classes(400, rng)
        xte, yte = tone_classes(400, rng)
        model = LogisticRegression(C=1.0, max_iter=5_000)
        raw.append(model.fit(xtr, ytr).score(xte, yte))
        spec.append(model.fit(log_power_spectrum(xtr), ytr).score(log_power_spectrum(xte), yte))
    assert abs(np.mean(raw) - 0.5) < 0.05
    assert min(spec) > 0.97


def test_shuffled_cross_validation_leaks_time():
    """Claim 26. On an autocorrelated series, shuffled 5-fold cross-validation of a model that
    can interpolate in time reports an error far below its error on the following period;
    time-ordered splits do not. Over 10 seeds: shuffled is below a tenth of the future error in
    every seed; the time-ordered estimate matches the future error on average (within a factor
    of 1.5), though any one 300-step future window is noisy."""
    ordered_all, future_all = [], []
    for s in range(10):
        rng = np.random.default_rng(26_000 + s)
        y = ar1_series(2_300, 0.99, 0.5, rng)
        t = np.arange(len(y), dtype=float)[:, None]
        knn = KNeighborsRegressor(n_neighbors=5)
        past, future = slice(0, 2_000), slice(2_000, 2_300)

        def cv_mse(cv, past=past, t=t, y=y, knn=knn):
            scores = cross_val_score(knn, t[past], y[past], cv=cv,
                                     scoring="neg_mean_squared_error")
            return -scores.mean()

        shuffled = cv_mse(KFold(5, shuffle=True, random_state=s))
        ordered = cv_mse(TimeSeriesSplit(5))
        knn.fit(t[past], y[past])
        future_mse = np.mean((knn.predict(t[future]) - y[future]) ** 2)
        assert shuffled * 14 <= future_mse  # the chapter: "a factor of at least 14"
        ordered_all.append(ordered)
        future_all.append(future_mse)
    ratio = np.mean(ordered_all) / np.mean(future_all)
    assert 1 / 1.5 < ratio < 1.5
