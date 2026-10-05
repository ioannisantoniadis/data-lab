::: {.callout-tip title="Data card: Mean imputation"}
| | |
|---|---|
| **Changes** | Representation: a missing value is encoded as the observed mean |
| **Assumption** | MCAR, and only the column's mean matters downstream |
| **What it does to the learned function** | Keeps the mean under MCAR; shrinks the variance by the share imputed and weakens correlations; biases the mean under MAR or MNAR |
| **Which models care** | Linear and distance-based models see a spike at the mean; trees can split it off |
| **Fit on** | Training rows only (the observed mean) |
| **Failure modes** | Non-MCAR missingness; heavy missingness (variance collapses); downstream use of variances or correlations |
| **Alternatives** | Regression imputation; multiple imputation; a missing-indicator feature |
| **Checked by** | `tests/test_missing.py::test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased` |
:::
