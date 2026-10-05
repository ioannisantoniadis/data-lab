::: {.callout-tip title="Data card: Deduplicating training data"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$ and weights: removes repeated examples, which also removes their extra weight in the loss |
| **Assumption** | Repeats are artifacts of collection, not part of $p$; what counts as a repeat (exact or near) can be defined |
| **What it does to the learned function** | Less memorization of repeated content; evaluation that measures generalization rather than recall; on a long tail, labels are not spent on covered cases |
| **Which models care** | Most visible for models that memorize (large language models, nearest neighbors) |
| **Fit on** | The whole corpus, before any split |
| **Failure modes** | Near-duplicates missed by exact matching; deduplicating genuine frequency information away; deduplicating after splitting |
| **Alternatives** | Down-weighting repeats; group-aware splits |
| **Checked by** | `tests/test_dedup.py::test_deduplication_reduces_overlap_optimism` |
:::
