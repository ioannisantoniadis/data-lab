::: {.callout-tip title="Data card: Time-ordered evaluation splits"}
| | |
|---|---|
| **Changes** | Evaluation only: validation examples always come after the training examples in time |
| **Assumption** | Predictions will be made about later times than the training data; the series is autocorrelated or drifts |
| **What it does to the learned function** | None on the model; makes the error estimate match the error on the following period on average instead of on interpolated neighbors |
| **Which models care** | All, most of all those that can interpolate (nearest neighbors, trees, flexible networks) |
| **Fit on** | Split boundaries set by time stamps |
| **Failure modes** | Features computed over the whole series (rolling statistics, normalizers) still carry the future into the past; a single future window gives a noisy estimate |
| **Alternatives** | Blocked cross-validation with gaps; a final held-out future period |
| **Checked by** | `tests/test_data_types.py::test_shuffled_cross_validation_leaks_time` |
:::
