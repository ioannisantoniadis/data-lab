::: {.callout-tip title="Data card: Importance weighting for covariate shift"}
| | |
|---|---|
| **Changes** | Weights $w(x) = p(x)/q(x)$ on each training example's loss |
| **Assumption** | Covariate shift: $p(y \mid x) = q(y \mid x)$; $q(x) > 0$ wherever $p(x) > 0$; the density ratio is known or well estimated |
| **What it does to the learned function** | Weighted averages under $q$ estimate averages under $p$ without bias |
| **Which models care** | Any model trained or evaluated by an average loss |
| **Fit on** | The density ratio: known here; in practice estimated, which adds its own error |
| **Failure modes** | Variance grows with $\mathbb{E}_q[w^2]$, which grows exponentially with a Gaussian shift; regions where $q$ is tiny dominate; an estimated ratio can be badly wrong where data is sparse |
| **Alternatives** | Collecting data from $p$; clipping or normalizing the weights (adds bias) |
| **Checked by** | `tests/test_shift.py::test_importance_weighting_unbiased_with_growing_variance` |
:::
