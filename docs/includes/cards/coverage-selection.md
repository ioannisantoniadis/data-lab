::: {.callout-tip title="Data card: Coverage-driven selection"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: labels only examples that cover what is not yet covered (optionally most frequent first) instead of every draw from $p$ |
| **Assumption** | What counts as covered can be recognized; unlabeled draws are cheap relative to labels or training steps |
| **What it does to the learned function** | On Hutter's model the error per label falls as $n^{-\alpha}$ instead of $n^{-\alpha/(1+\alpha)}$: a steeper power law, still a power law. Skipping repeats buys the exponent; frequency order adds only a constant factor (about 1.5) |
| **Which models care** | Models that learn one case per example (memorization-like); the gain for models that generalize between cases is not measured here |
| **Fit on** | An unlabeled pool (or an oracle) and the record of what has been labeled |
| **Failure modes** | The gain is per label: it costs about $n^{1+\alpha}$ unlabeled draws, and per draw nothing beats uniform sampling; a pool with fewer distinct cases than the labeling budget cannot spend it, and its error is that of the pool; recognizing coverage is trivial here and hard for real data (near-duplicates, semantic similarity) |
| **Alternatives** | Uniform sampling; active learning by model uncertainty; deduplication |
| **Checked by** | `tests/test_long_tail.py::test_deduplicated_stream_reaches_the_oracle_exponent_per_label` |
:::
