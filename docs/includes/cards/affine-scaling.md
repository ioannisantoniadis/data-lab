::: {.callout-tip title="Data card: Affine scaling (standard, min-max, max-abs)"}
| | |
|---|---|
| **Changes** | Representation (of $x$): each feature is shifted and divided by a positive constant |
| **Assumption** | The model's behavior depends on the features' units; a feature's typical spread is a fair yardstick for its importance |
| **What it does to the learned function** | None on the shape of any feature (skewness and kurtosis unchanged); equalizes the units that distances and penalties compare; improves the conditioning of a least-squares fit |
| **Which models care** | Distance-based models (nearest neighbors, kernels, clustering), penalized models, gradient-trained models; not trees, and not unpenalized linear models' predictions |
| **Fit on** | Training data only: mean and standard deviation, or minimum and maximum, or maximum absolute value |
| **Failure modes** | Outliers set the scale (standard and min-max); a feature that should matter more is made to matter equally; test values outside the training range (min-max) |
| **Alternatives** | Robust scaling; a shape-changing transform when the problem is skew, not units |
| **Checked by** | `tests/test_scaling.py::test_affine_scalers_preserve_skewness_and_kurtosis` |
:::
