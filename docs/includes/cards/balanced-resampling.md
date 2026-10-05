::: {.callout-tip title="Data card: Rebalancing classes (undersampling or oversampling)"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: class proportions in training differ from those under $p$ |
| **Assumption** | Only the class priors change: $q(x \mid y) = p(x \mid y)$ |
| **What it does to the learned function** | The model learns the posterior tilted to the training priors; at threshold 1/2 a balanced model decides as the true posterior would at threshold $p(y = 1)$ |
| **Which models care** | Every probabilistic classifier |
| **Fit on** | Training labels (class counts) |
| **Failure modes** | Probabilities are wrong unless corrected; undersampling discards data and raises variance; oversampling by copying repeats examples |
| **Alternatives** | Class weights ($w$); training on $p$ and moving the threshold; prior-shift correction afterwards |
| **Checked by** | `tests/test_imbalance.py::test_prior_shift_correction_restores_calibration` |
:::
