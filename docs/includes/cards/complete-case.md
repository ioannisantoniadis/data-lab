::: {.callout-tip title="Data card: Complete-case analysis (dropping rows with missing values)"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: keeps only rows whose value was observed |
| **Assumption** | MCAR: whether a value is missing is unrelated to anything |
| **What it does to the learned function** | Under MCAR, none beyond a smaller sample; under MAR or MNAR the kept rows follow a different distribution, so means shift, and so do fitted relationships unless the missingness depends only on the model's inputs (selection on $x$) |
| **Which models care** | Every model |
| **Fit on** | Nothing is fit; the selection is made by the missingness itself |
| **Failure modes** | MAR or MNAR missingness (biased estimates); many columns with a little missingness each (few complete rows left) |
| **Alternatives** | Regression or multiple imputation (MAR); modeling the missingness (MNAR) |
| **Checked by** | `tests/test_missing.py::test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased` |
:::
