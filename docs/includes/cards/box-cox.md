::: {.callout-tip title="Data card: Box-Cox and Yeo-Johnson power transforms"}
| | |
|---|---|
| **Changes** | Representation: a power transform whose exponent $\lambda$ is chosen by maximum likelihood to make the data as close to normal as the family allows |
| **Assumption** | Some power of the data is close to normal; Box-Cox needs strictly positive data, Yeo-Johnson does not |
| **What it does to the learned function** | Reduces skew; for a target, the model learns a mean on the transformed scale, which back-transforms to the median of $y$ when the transformed noise is symmetric, not to the mean |
| **Which models care** | Linear, GLM-type and distance-based models; trees are unaffected (monotone) |
| **Fit on** | Training data only: $\lambda$ by maximum likelihood |
| **Failure modes** | No power makes the data normal (multimodal data); $\lambda$ estimated on few points is noisy; retransformation bias as for the log |
| **Alternatives** | A fixed log; a quantile transform; modeling the skew in the loss |
| **Checked by** | `tests/test_transforms.py::test_box_cox_mle_recovers_known_lambda` |
:::
