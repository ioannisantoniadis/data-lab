::: {.callout-tip title="Data card: Regression imputation"}
| | |
|---|---|
| **Changes** | Representation: a missing value is encoded as its prediction from observed columns |
| **Assumption** | MAR on the observed columns used as predictors, and a correctly specified imputation model |
| **What it does to the learned function** | Removes the bias of the mean under MAR; still understates the variance (imputed values have no noise) and overstates correlations |
| **Which models care** | Every model; downstream uncertainty estimates are too narrow |
| **Fit on** | Training rows with the value observed |
| **Failure modes** | MNAR (the missing values differ in ways the predictors do not show); treating imputed values as observed |
| **Alternatives** | Multiple imputation, which adds the missing noise back (van Buuren); stochastic regression imputation |
| **Checked by** | `tests/test_missing.py::test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased` |
:::
