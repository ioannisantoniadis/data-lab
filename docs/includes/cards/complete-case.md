::: {.callout-tip title="Data card: Complete-case analysis (dropping rows with missing values)"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: keeps only rows whose value was observed |
| **Assumption** | For means and other summaries, MCAR: whether a value is missing is unrelated to anything. For a model of $p(y \mid x)$, it is enough that missingness depends only on the model's inputs |
| **What it does to the learned function** | Under MCAR, none beyond a smaller sample; under MAR or MNAR the kept rows follow a different distribution, so means shift, and so do fitted relationships unless the missingness depends only on the model's inputs (selection on $x$) |
| **Which models care** | Every model |
| **Fit on** | Nothing is fit; the selection is made by the missingness itself |
| **Failure modes** | MAR or MNAR missingness for summaries, and missingness that depends on the target for models (biased estimates); many columns with a little missingness each (few complete rows left) |
| **Alternatives** | Regression or multiple imputation (MAR); modeling the missingness (MNAR) |
| **Checked by** | `tests/test_missing.py::test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased` |
:::
