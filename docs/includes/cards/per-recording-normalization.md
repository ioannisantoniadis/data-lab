::: {.callout-tip title="Data card: Per-recording (per-sample) normalization"}
| | |
|---|---|
| **Changes** | Representation (of $x$): each example is rescaled by a statistic of itself (here, its mean log spectrum is subtracted), not by statistics of the training set |
| **Assumption** | The nuisance acts on the whole example the same way (a recording gain scales every frequency alike), and the absolute level carries no information about the label |
| **What it does to the learned function** | Makes the features exactly invariant to the nuisance, so a shift in it at deployment cannot move the predictions |
| **Which models care** | Every model that sees the features; unlike per-feature scaling, it changes what even a tree can see |
| **Fit on** | Nothing: each example's own values |
| **Failure modes** | The level does carry label information (loudness that matters is erased); the nuisance acts differently on different parts of the example (frequency-dependent gain is only partly removed) |
| **Alternatives** | Augmentation with random gains (teaches the invariance through $q$); per-feature scaling, which does not remove a per-example offset |
| **Checked by** | `tests/test_worked_examples.py::test_centering_the_log_spectrum_removes_any_gain_exactly` |
:::
