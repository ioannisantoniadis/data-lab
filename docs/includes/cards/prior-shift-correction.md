::: {.callout-tip title="Data card: Prior-shift correction (and EM prior estimation)"}
| | |
|---|---|
| **Changes** | Weights $w$ on the model's output: each class's posterior is multiplied by $p(y)/q(y)$ and renormalized |
| **Assumption** | Only the priors differ between training and target data; the model's posteriors are calibrated under $q$; for EM, the new data are unlabeled draws from the target |
| **What it does to the learned function** | Turns posteriors learned under $q$ into posteriors under $p$; EM also estimates the unknown target prior |
| **Which models care** | Any classifier with calibrated probabilities |
| **Fit on** | The training prior (counts) and the target prior (known, or estimated by EM on unlabeled target data) |
| **Failure modes** | $p(x \mid y)$ also changed (not prior shift); miscalibrated training posteriors; EM converging slowly or to a biased value with few target examples |
| **Alternatives** | Retraining on data from $p$; recalibration on labeled target data |
| **Checked by** | `tests/test_imbalance.py::test_em_prior_estimation_recovers_test_prior` |
:::
