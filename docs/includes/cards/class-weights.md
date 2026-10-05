::: {.callout-tip title="Data card: Class weights"}
| | |
|---|---|
| **Changes** | Weights $w$: each example's loss is multiplied by its class's weight |
| **Assumption** | As for rebalancing: only the class priors are to be changed |
| **What it does to the learned function** | Same tilted posterior as resampling to the same proportions, with less variance because no example is discarded |
| **Which models care** | Every model trained by a weighted loss |
| **Fit on** | Training labels (class counts); scikit-learn's "balanced" uses n / (classes x count) |
| **Failure modes** | Probabilities are wrong unless corrected; very large weights on very rare classes make training noisy |
| **Alternatives** | Resampling ($q$); moving the threshold; prior-shift correction |
| **Checked by** | `tests/test_imbalance.py::test_resampling_and_reweighting_share_a_target_not_a_variance` |
:::
