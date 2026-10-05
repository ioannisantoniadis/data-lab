::: {.callout-tip title="Data card: Target encoding"}
| | |
|---|---|
| **Changes** | Representation: each level is replaced by a shrunk estimate of the mean target among training rows with that level |
| **Assumption** | Levels with few rows are shrunk toward the global mean; each row's encoding is computed without that row's own label (cross-fitting) |
| **What it does to the learned function** | One informative column per categorical feature, however many levels; without cross-fitting, each row's own label leaks into its feature |
| **Which models care** | Every model; most useful for high-cardinality categories with linear or tree models |
| **Fit on** | Training labels, cross-fitted on the training rows (out-of-fold), and fit on all training rows for test data |
| **Failure modes** | Encoding training rows with an encoder fit on those same rows: noise becomes a training signal that fails on new data; leakage across a time order |
| **Alternatives** | One-hot; hashing; grouping rare levels |
| **Checked by** | `tests/test_leakage.py::test_target_encoding_without_cross_fitting_leaks` |
:::
