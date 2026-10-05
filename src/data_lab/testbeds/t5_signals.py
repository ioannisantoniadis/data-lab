"""T5: synthetic signals, and small images with an exactly known invariance.

Audio: sums of sinusoids with known frequencies, amplitudes and switch times, plus Gaussian
noise, at a chosen sampling rate. The spectrogram is a short-time Fourier transform from
``scipy.signal.stft`` with every parameter passed explicitly (in SciPy 1.18 the default window
is 'hann_periodic'; docstring read 2026-10-04). No audio library (SPEC §16).

Images: scikit-learn's bundled ``load_digits`` (8 x 8 images; the data file ships inside the
package, ``sklearn/datasets/data/digits.csv.gz``, so nothing is downloaded). Real digit labels
have no exactly known invariance, so the testbed also defines a *synthetic* label with one:

    side(x) = 1 if the image's ink in the left half exceeds the ink in the right half, else 0.

This label is exactly invariant under an up-down flip and exactly reversed by a left-right
flip (for images without a tie, which are dropped). An augmentation can therefore be
label-preserving or label-changing by construction, not by judgment (SPEC §7, T5).
"""

from __future__ import annotations

import numpy as np
from scipy import signal
from sklearn.datasets import load_digits


def sinusoids(
    freqs,
    amps,
    fs: float,
    duration: float,
    noise: float,
    rng: np.random.Generator,
    switch_time: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Sum of sinusoids sampled at fs. With ``switch_time``, the first frequency plays before it
    and the remaining ones after it (a known time-frequency structure). Returns (t, x)."""
    t = np.arange(int(round(fs * duration))) / fs
    freqs, amps = np.asarray(freqs, float), np.asarray(amps, float)
    phases = rng.uniform(0, 2 * np.pi, size=freqs.size)
    parts = amps[:, None] * np.sin(2 * np.pi * freqs[:, None] * t + phases[:, None])
    if switch_time is not None:
        before = t < switch_time
        parts[0, ~before] = 0.0
        parts[1:, before] = 0.0
    return t, parts.sum(axis=0) + noise * rng.standard_normal(t.size)


def spectrogram(x: np.ndarray, fs: float, nperseg: int = 256):
    """Magnitude STFT with a periodic Hann window and 50% overlap. Returns (f, t, |Z|)."""
    f, t, z = signal.stft(
        x,
        fs=fs,
        window="hann_periodic",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        nfft=nperseg,
        detrend=False,
        return_onesided=True,
        boundary="zeros",
        padded=True,
        scaling="spectrum",
    )
    return f, t, np.abs(z)


def digit_images() -> tuple[np.ndarray, np.ndarray]:
    """The bundled digits as (n, 8, 8) float images in [0, 16], and their digit labels."""
    data = load_digits()
    return data.images.astype(float), data.target


def side_label(images: np.ndarray) -> np.ndarray:
    """1 where the left half holds more ink than the right half; -1 marks ties."""
    left = images[:, :, :4].sum(axis=(1, 2))
    right = images[:, :, 4:].sum(axis=(1, 2))
    return np.where(left > right, 1, np.where(left < right, 0, -1))


def side_task() -> tuple[np.ndarray, np.ndarray]:
    """Digit images with the synthetic side label, ties removed."""
    images, _ = digit_images()
    y = side_label(images)
    keep = y >= 0
    return images[keep], y[keep]


def flip_up_down(images: np.ndarray) -> np.ndarray:
    """Label-preserving for the side task, exactly."""
    return images[:, ::-1, :]


def flip_left_right(images: np.ndarray) -> np.ndarray:
    """Label-reversing for the side task, exactly."""
    return images[:, :, ::-1]


def tone_classes(
    n: int, rng: np.random.Generator, fs: float = 8_000.0, duration: float = 0.25,
    noise: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """n noisy tones, alternating classes: class 0 at a frequency drawn from 400-600 Hz, class 1
    from 1,200-1,400 Hz; random phase. Returns (waveforms, labels)."""
    waves, labels = [], []
    for i in range(n):
        c = i % 2
        f = rng.uniform(400, 600) if c == 0 else rng.uniform(1_200, 1_400)
        _, x = sinusoids([f], [1.0], fs, duration, noise=noise, rng=rng)
        waves.append(x)
        labels.append(c)
    return np.array(waves), np.array(labels)


def log_power_spectrum(waves: np.ndarray, fs: float = 8_000.0, nperseg: int = 256):
    """Per-frequency log of the time-averaged spectrogram magnitude: a phase-free representation."""
    return np.array([np.log(spectrogram(x, fs, nperseg)[2].mean(axis=1) + 1e-12) for x in waves])


def ar1_series(length: int, phi: float, noise: float, rng: np.random.Generator) -> np.ndarray:
    """y_t = s_t + noise * e_t with a latent AR(1) s_t = phi s_{t-1} + u_t (unit innovations):
    strongly autocorrelated when phi is close to 1."""
    s = np.zeros(length)
    u = rng.standard_normal(length)
    for t in range(1, length):
        s[t] = phi * s[t - 1] + u[t]
    return s + noise * rng.standard_normal(length)
