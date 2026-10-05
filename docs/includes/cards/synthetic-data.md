::: {.callout-tip title="Data card: Training on model-generated data"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: training examples are drawn from a fitted model instead of from $p$ |
| **Assumption** | The generator's distribution covers $p$, including its tail |
| **What it does to the learned function** | A generator fit to finite data misses the unseen tail; a learner trained on its output plateaus at that missing mass |
| **Which models care** | Every model trained on generated data |
| **Fit on** | The generator's own training data |
| **Failure modes** | Replacing real data generation after generation loses more of the tail each time; accumulating real and synthetic data does not |
| **Alternatives** | Keeping and reusing the real data; mixing a share of fresh real data |
| **Checked by** | `tests/test_collapse.py::test_refitting_on_own_samples_loses_tail` |
:::
