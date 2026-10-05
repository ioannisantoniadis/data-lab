::: {.callout-tip title="Data card: Active learning by uncertainty sampling"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: the next example to label is the pool example the current model is least sure about |
| **Assumption** | Uncertainty reflects what the model has not learned, not irreducible label noise; the pool represents $p$ |
| **What it does to the learned function** | Labels concentrate near the current boundary, which helps when classes are nearly separable |
| **Which models care** | Probabilistic classifiers that are refit as labels arrive |
| **Fit on** | The labeled set so far and an unlabeled pool |
| **Failure modes** | Noisy labels: uncertainty points at noise, and the gain vanishes; the labeled set is no longer a sample of $p$ (biased estimates); querying outliers |
| **Alternatives** | Random labeling; diversity- or density-weighted selection; RHO-LOSS-style criteria |
| **Checked by** | `tests/test_active_learning.py::test_uncertainty_sampling_gains_shrink_with_label_noise` |
:::
