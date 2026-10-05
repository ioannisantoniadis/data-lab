::: {.callout-tip title="Data card: Removing train/test duplicates"}
| | |
|---|---|
| **Changes** | Evaluation only: test rows that also appear in training are removed from the test set |
| **Assumption** | Deployment inputs will not be copies of training inputs |
| **What it does to the learned function** | None on the model; the test score stops rewarding memorization |
| **Which models care** | Most visible for models that can memorize (nearest neighbors, deep trees, large networks) |
| **Fit on** | Exact (or near-duplicate) matching of test rows against training rows |
| **Failure modes** | Near-duplicates that exact matching misses; deployment that genuinely repeats inputs, where duplicates are part of $p$ |
| **Alternatives** | Group-aware splits (all copies of an entity on one side) |
| **Checked by** | `tests/test_leakage.py::test_train_test_duplicates_inflate_the_test_score` |
:::
