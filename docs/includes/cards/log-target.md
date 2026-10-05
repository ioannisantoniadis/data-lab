::: {.callout-tip title="Data card: Log-transforming a skewed target"}
| | |
|---|---|
| **Changes** | Representation (of $y$) |
| **Assumption** | $y > 0$, with multiplicative noise or right skew |
| **What it does to the learned function** | With MSE, the model learns $\mathbb{E}[\log y \mid x]$: on the original scale, the geometric mean (the median under log-normal noise), not the mean |
| **Which models care** | Linear and GLM-type models, neural nets; trees much less |
| **Fit on** | None (a fixed function); the smearing correction is fit on training residuals |
| **Failure modes** | Retransformation bias; zeros and negatives; smearing fails when the log-scale noise depends on $x$, and its factor is unstable when residuals are heavy-tailed |
| **Alternatives** | Box-Cox / Yeo-Johnson; a log-link GLM; a loss matched to the noise |
| **Checked by** | `tests/test_transforms.py::test_log_target_mse_predicts_geometric_mean` |
:::
