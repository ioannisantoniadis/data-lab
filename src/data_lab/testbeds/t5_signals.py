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
