::: {.callout-tip title="Data card: Pruning by difficulty (keep hard or easy examples)"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: keeps a fraction of the training set ranked by a difficulty score (margin, EL2N, GraNd, forgetting events) |
| **Assumption** | The score ranks examples as the true margin would; the right end to keep depends on how much data there is |
| **What it does to the learned function** | Keeping hard examples sharpens the boundary when data is abundant; keeping easy ones gives coarse information first when it is scarce |
| **Which models care** | Demonstrated for a max-margin perceptron; reported for image networks |
| **Fit on** | Scores from a probe model trained on the training data (a few epochs, or a different architecture) |
| **Failure modes** | Keeping hard examples with scarce data; noisy scores at high pruning rates, where random pruning can win (Ayed and Hayou); hard examples that are mislabeled |
| **Alternatives** | Random subsampling; self-supervised scores; reweighting instead of discarding |
| **Checked by** | `tests/test_pruning.py::test_pruning_crossover_hard_when_abundant_easy_when_scarce` |
:::
