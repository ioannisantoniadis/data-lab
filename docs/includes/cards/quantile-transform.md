::: {.callout-tip title="Data card: Quantile transform"}
| | |
|---|---|
| **Changes** | Representation: each feature is replaced by its estimated quantile, then mapped to a uniform or normal distribution |
| **Assumption** | Only the order of values within a feature matters, not their spacing |
| **What it does to the learned function** | Any marginal shape becomes the chosen one; ranks within a feature are kept, distances and linear correlations are not |
| **Which models care** | Distance-based and linear models change most; trees are unaffected on the training data (monotone) |
| **Fit on** | Training data only: the quantiles of each feature |
| **Failure modes** | Distances lose their meaning (two values far apart in the tail become neighbors); no extrapolation: everything beyond the training range maps to the boundary |
| **Alternatives** | A log or power transform, which keeps the spacing's order of magnitude |
| **Checked by** | `tests/test_transforms.py::test_quantile_transform_changes_distances_preserves_ranks` |
:::
