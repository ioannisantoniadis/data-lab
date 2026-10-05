"""Chapter 3: a representation that exposes structure, and a split that ignores it (T5).

Panel A: spectrogram (log magnitude) of one second of noisy audio at 8 kHz that plays 500 Hz
until 0.4 s and 2,000 Hz after; labels mark the generating frequencies and switch time.
Panel B: test accuracy of the same linear classifier on raw waveforms and on log power spectra,
for two classes of noisy tones with random phase (5 seeds; claim 27).
Panel C: for an autocorrelated series, the error a 5-nearest-neighbor regressor on time reports
under shuffled 5-fold cross-validation and under time-ordered splits, against its actual error
on the next 300 steps (10 seeds; claim 26).

This figure makes visible that the spectrogram turns frequency into something a linear model
can use, and that shuffling an autocorrelated series lets the model look up the answer.

Run: uv run python scripts/figures/fig_data_types.py   (about 5 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score
from sklearn.neighbors import KNeighborsRegressor

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _theme import (  # noqa: E402
    EVALUATION_COLOR,
    INK,
    INK_SECONDARY,
    LEVER_COLOR,
    MUTED,
    apply_theme,
    save_figure,
)

from data_lab.testbeds.t5_signals import (  # noqa: E402
    ar1_series,
    log_power_spectrum,
    sinusoids,
    spectrogram,
    tone_classes,
)

apply_theme()
FS = 8_000.0
fig, axes = plt.subplots(1, 3, figsize=(13, 4.0), gridspec_kw={"width_ratios": [1.3, 0.8, 1]})

# A
_, x = sinusoids([500.0, 2_000.0], [1.0, 1.0], FS, 1.0, noise=0.5,
                 rng=np.random.default_rng(3), switch_time=0.4)
f, t, mag = spectrogram(x, FS, nperseg=256)
ax = axes[0]
ax.pcolormesh(t, f, 20 * np.log10(mag + 1e-6), shading="auto", cmap="Blues", rasterized=True)
ax.annotate("500 Hz until 0.4 s", xy=(0.2, 500), xytext=(0.05, 900), fontsize=9.5, color=INK,
            arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.8})
ax.annotate("2,000 Hz after", xy=(0.7, 2_000), xytext=(0.55, 2_500), fontsize=9.5, color=INK,
            arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.8})
ax.set_ylim(0, 3_000)
ax.set_xlabel("time (s)")
ax.set_ylabel("frequency (Hz)")
ax.set_title("A. Spectrogram: where the energy is")
ax.grid(False)

# B
raw, spec = [], []
for s in range(5):
    rng = np.random.default_rng(27_000 + s)
    xtr, ytr = tone_classes(400, rng)
    xte, yte = tone_classes(400, rng)
    model = LogisticRegression(C=1.0, max_iter=5_000)
    raw.append(model.fit(xtr, ytr).score(xte, yte))
    spec.append(model.fit(log_power_spectrum(xtr), ytr).score(log_power_spectrum(xte), yte))
ax = axes[1]
for j, (vals, color, _label) in enumerate([(raw, MUTED, "raw\nwaveform"),
                                          (spec, LEVER_COLOR["representation"],
                                           "log power\nspectrum")]):
    ax.bar(j, np.mean(vals), width=0.6, color=color)
    ax.scatter(np.full(5, j) + np.linspace(-0.15, 0.15, 5), vals, s=12, color=INK, zorder=3)
    ax.annotate(f"{np.mean(vals):.2f}", xy=(j, max(vals)), xytext=(0, 6),
                textcoords="offset points", ha="center", fontsize=9.5)
ax.axhline(0.5, color=INK_SECONDARY, lw=0.8, ls=(0, (4, 3)))
ax.set_xticks([0, 1], ["raw\nwaveform", "log power\nspectrum"])
ax.set_ylim(0, 1.1)
ax.set_ylabel("test accuracy, same linear model")
ax.set_title("B. Same model, two representations")
ax.grid(axis="x", visible=False)

# C
rows = []
for s in range(10):
    rng = np.random.default_rng(26_000 + s)
    y = ar1_series(2_300, 0.99, 0.5, rng)
    tt = np.arange(len(y), dtype=float)[:, None]
    knn = KNeighborsRegressor(n_neighbors=5)
    past, future = slice(0, 2_000), slice(2_000, 2_300)
    sh = -cross_val_score(knn, tt[past], y[past], cv=KFold(5, shuffle=True, random_state=s),
                          scoring="neg_mean_squared_error").mean()
    od = -cross_val_score(knn, tt[past], y[past], cv=TimeSeriesSplit(5),
                          scoring="neg_mean_squared_error").mean()
    knn.fit(tt[past], y[past])
    rows.append((sh, od, np.mean((knn.predict(tt[future]) - y[future]) ** 2)))
rows = np.array(rows)
ax = axes[2]
labels = ["shuffled\n5-fold", "time-ordered\nsplits", "actual error,\nnext 300 steps"]
markers = ["v", "o", "D"]
colors = [EVALUATION_COLOR, EVALUATION_COLOR, INK]
for j in range(3):
    ax.scatter(np.full(10, j) + np.linspace(-0.15, 0.15, 10), rows[:, j], s=16,
               marker=markers[j], color=colors[j])
    ax.plot([j - 0.25, j + 0.25], [np.mean(rows[:, j])] * 2, color=INK, lw=1.5)
ax.set_yscale("log")
ax.set_xticks(range(3), labels)
ax.set_ylabel("mean squared error")
ax.set_title("C. Shuffling a time series leaks")
ax.grid(axis="x", visible=False)

save_figure(fig, "data_types")
