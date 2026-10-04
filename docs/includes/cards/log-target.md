::: {.callout-tip title="Data card: Log-transforming a skewed target (draft: not yet verified)"}
| | |
|---|---|
| **Changes** | Representation (of $y$) |
| **Assumption** | $y > 0$, with multiplicative noise or right skew |
| **What it does to the learned function** | With MSE, the model learns $\mathbb{E}[\log y \mid x]$: on the original scale, a geometric-mean-like prediction, not the mean |
| **Which models care** | Linear and GLM-type models, neural nets; trees much less |
| **Fit on** | None (a fixed function); the smearing correction is fit on training residuals |
| **Failure modes** | Retransformation bias; zeros and negatives; heavy-tailed residuals after transform |
| **Alternatives** | Box-Cox / Yeo-Johnson; a log-link GLM; a loss matched to the noise |
| **Checked by** | `tests/test_transforms.py::test_log_target_mse_predicts_geometric_mean` |
:::
