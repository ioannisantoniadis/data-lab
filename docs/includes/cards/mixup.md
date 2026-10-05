::: {.callout-tip title="Data card: mixup"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$ and labels: trains on convex combinations of pairs of inputs, with the same combination of their labels |
| **Assumption** | Between two training examples, the target changes linearly along the segment joining them (a vicinal distribution around the data) |
| **What it does to the learned function** | Trains the model on targets that change linearly between examples, so the learned function is pushed toward that behavior between them |
| **Which models care** | Models trained by gradient on a loss that accepts soft labels, mostly neural networks |
| **Fit on** | Training batches, with the mixing weight drawn from Beta($\alpha$, $\alpha$) |
| **Failure modes** | Mixed inputs that are not plausible inputs; targets that are not linear between examples; small $\alpha$ changes little, large $\alpha$ blurs classes |
| **Alternatives** | Label-preserving augmentation; label smoothing |
| **Checked by** | `tests/test_augmentation.py::test_mixup_forms_the_same_convex_combination_of_inputs_and_labels` |
:::
