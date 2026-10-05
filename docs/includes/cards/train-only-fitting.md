::: {.callout-tip title="Data card: Fitting preprocessing on training data only"}
| | |
|---|---|
| **Changes** | Evaluation only: every fitted step (scaler, imputer, selector, encoder) sees training data only |
| **Assumption** | The evaluation should mimic deployment, where test labels and test inputs are not available at fit time |
| **What it does to the learned function** | None on what the model can learn; removes optimism, which is large for supervised steps and small for unsupervised ones on i.i.d. data |
| **Which models care** | All |
| **Fit on** | Training folds only (inside each cross-validation fold) |
| **Failure modes** | Steps fit outside the pipeline (feature selection, target encoding, resampling) before splitting |
| **Alternatives** | A scikit-learn Pipeline cross-validated as one estimator |
| **Checked by** | `tests/test_leakage.py::test_fitting_preprocessing_on_test_is_optimistic` |
:::
