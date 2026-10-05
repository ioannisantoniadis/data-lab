::: {.callout-tip title="Data card: Robust scaling (median and interquartile range)"}
| | |
|---|---|
| **Changes** | Representation (of $x$): each feature is centered at its median and divided by its interquartile range |
| **Assumption** | Outliers are a small share of each feature (fewer than a quarter on each side) |
| **What it does to the learned function** | Same as affine scaling for the bulk of the data, with a scale that outliers cannot inflate; the outliers themselves stay extreme |
| **Which models care** | The same models as affine scaling |
| **Fit on** | Training data only: median and quartiles |
| **Failure modes** | Outliers are left in place at large values; features with an interquartile range of zero (mostly constant) |
| **Alternatives** | Removing errors before scaling; clipping; a shape-changing transform; a robust loss (loss-functions-lab) |
| **Checked by** | `tests/test_scaling.py::test_robust_scaler_keeps_inlier_spread_under_outliers` |
:::
