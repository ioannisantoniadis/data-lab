::: {.callout-tip title="Data card: Label-changing augmentation"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$ and labels: adds transformed inputs with labels changed as the transform is known to change them |
| **Assumption** | The transform's effect on the label is known exactly (here: a left-right flip reverses which half holds more ink) |
| **What it does to the learned function** | As much new, correctly labeled data as a label-preserving augmentation, including examples near the boundary from the other side |
| **Which models care** | Every model |
| **Fit on** | Training data only |
| **Failure modes** | A wrongly assumed label change is label noise by construction; the effect may be known only for some inputs |
| **Alternatives** | Label-preserving augmentation with a different transform; collecting the transformed cases |
| **Checked by** | `tests/test_augmentation.py::test_label_changing_augmentation_helps_when_the_change_is_known` |
:::
