::: {.callout-tip title="Data card: Spectrogram (short-time Fourier magnitude)"}
| | |
|---|---|
| **Changes** | Representation (of $x$): from samples over time to energy per frequency per time window |
| **Assumption** | The task depends on which frequencies are present and when, not on their phase; the window is long enough to resolve the frequencies that matter |
| **What it does to the learned function** | Makes frequency content a feature a linear or local model can use; discards phase, so phase-dependent targets become harder |
| **Which models care** | Linear and distance-based models, which cannot build the transform themselves; whether a flexible model learns an equivalent front end from raw audio is not tested here |
| **Fit on** | None: a fixed transform (window length and overlap chosen in advance) |
| **Failure modes** | Window too short to resolve close frequencies or too long to localize changes in time; aliasing of frequencies above half the sampling rate happens before the transform and cannot be undone |
| **Alternatives** | Raw waveform with a learned front end; mel or other perceptual frequency scales |
| **Checked by** | `tests/test_data_types.py::test_spectrogram_representation_makes_tone_classes_linearly_separable` |
:::
