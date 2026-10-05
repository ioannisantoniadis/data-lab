::: {.callout-tip title="Data card: Filtering web-scale data"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: keeps the documents a quality filter scores highly |
| **Assumption** | The filter's notion of quality predicts usefulness for the target; enough data remains for the compute available |
| **What it does to the learned function** | Reported to give better models for the same training budget when the filter is good; benchmarks such as DataComp compare filters directly |
| **Which models care** | Large models trained on web data |
| **Fit on** | Heuristics or classifiers, sometimes trained on reference data |
| **Failure modes** | Filtering away rare but needed content (the tail); filtering choices that are right for one compute budget and wrong for another (Goyal et al.) |
| **Alternatives** | Deduplication only; reweighting by quality instead of discarding |
| **Checked by** | Not tested here; stated from [@goyal2024scaling] |
:::
