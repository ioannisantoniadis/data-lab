::: {.callout-tip title="Data card: Finding label errors by confident learning"}
| | |
|---|---|
| **Changes** | Labels: flags examples whose given label disagrees confidently with an out-of-sample model, to drop or relabel |
| **Assumption** | Class-conditional noise (flips independent of $x$ given the true class); out-of-sample probabilities that rank examples well; classes that overlap little |
| **What it does to the learned function** | If the flagged examples really are flips, removing them moves the learned posterior back toward $\eta(x)$ and the boundary back to the clean one |
| **Which models care** | Every model trained on the cleaned labels; the detector itself needs calibrated-enough probabilities |
| **Fit on** | Out-of-sample predictions (cross-validation), never the model's own training fit |
| **Failure modes** | Overlapping classes: genuine ambiguity looks like noise (precision near the noise rate); flips near the boundary are missed; noise that depends on $x$ breaks the assumption |
| **Alternatives** | Repeated annotation and adjudication; noise-robust losses (loss-functions-lab); modeling the noise rates explicitly |
| **Checked by** | `tests/test_labels.py::test_confident_learning_precision_depends_on_separability` |
:::
