"""T5 ground truths: the spectrogram recovers known frequencies and a known switch time; the
digits load offline; the synthetic side label has exactly the stated invariances."""

import numpy as np

from data_lab.testbeds.t5_signals import (
    digit_images,
    flip_left_right,
    flip_up_down,
    side_label,
    side_task,
    sinusoids,
    spectrogram,
)

FS = 8_000.0


def test_spectrogram_peaks_at_the_generating_frequencies():
    rng = np.random.default_rng(0)
    freqs = [440.0, 1_250.0]
    _, x = sinusoids(freqs, [1.0, 0.6], FS, 1.0, noise=0.3, rng=rng)
    f, _, mag = spectrogram(x, FS, nperseg=256)
    power = (mag**2).mean(axis=1)
    top2 = np.sort(f[np.argsort(power)[-2:]])
    resolution = FS / 256
    np.testing.assert_allclose(top2, freqs, atol=resolution)


def test_spectrogram_localizes_a_frequency_switch_in_time():
    rng = np.random.default_rng(1)
    _, x = sinusoids([500.0, 2_000.0], [1.0, 1.0], FS, 1.0, noise=0.1, rng=rng, switch_time=0.4)
    f, t, mag = spectrogram(x, FS, nperseg=256)
    low = mag[np.argmin(np.abs(f - 500.0))]
    high = mag[np.argmin(np.abs(f - 2_000.0))]
    crossing = t[np.argmax(high > low)]
    assert abs(crossing - 0.4) <= 256 / FS  # within one window length


def test_digits_are_bundled_and_shaped():
    images, labels = digit_images()
    assert images.shape == (1797, 8, 8) and set(labels) == set(range(10))
    assert images.min() >= 0 and images.max() <= 16


def test_side_label_invariances_are_exact():
    images, y = side_task()
    assert len(y) > 1_500 and set(np.unique(y)) == {0, 1}
    np.testing.assert_array_equal(side_label(flip_up_down(images)), y)
    np.testing.assert_array_equal(side_label(flip_left_right(images)), 1 - y)
