::: {.callout-tip title="Data card: Choosing domain mixtures (DoReMi)"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: the proportion of training data drawn from each domain |
| **Assumption** | Weights found by a small proxy model transfer to a larger model |
| **What it does to the learned function** | Reported to reach a baseline's downstream accuracy in fewer steps |
| **Which models care** | Reported for language models |
| **Fit on** | A small proxy model trained with group distributionally robust optimization over domains |
| **Failure modes** | Weights that do not transfer to the larger model or to the target task |
| **Alternatives** | Default or hand-tuned proportions; mixture scaling laws |
| **Checked by** | Not tested here; stated from [@xie2023doremi] |
:::
