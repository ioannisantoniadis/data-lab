::: {.callout-tip title="Data card: Label-preserving augmentation (flips, crops, color, SpecAugment, RandAugment)"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: adds transformed copies of training inputs with their labels unchanged |
| **Assumption** | The target is invariant under the transform: $p(y \mid T(x)) = p(y \mid x)$ for every transform $T$ used, at the strengths used |
| **What it does to the learned function** | More training data consistent with $p$, so less variance; the model is pushed toward the assumed invariance |
| **Which models care** | Every model; most valuable at small $n$ and for models that cannot build the invariance in |
| **Fit on** | Training data only, transformed during training |
| **Failure modes** | The invariance is false, or false beyond some strength: augmented examples are then mislabeled; test-time inputs never look like the augmented ones |
| **Alternatives** | An architecture that has the invariance built in; label-changing augmentation when the transform's effect is known |
| **Checked by** | `tests/test_augmentation.py::test_invariant_augmentation_helps_noninvariant_hurts` |
:::
