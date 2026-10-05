::: {.callout-tip title="Data card: Stratified sampling"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: fixes how many examples come from each stratum |
| **Assumption** | Strata are known for the whole population before sampling, and the target varies more between strata than within them |
| **What it does to the learned function** | None on $q(y \mid x)$; with proportional allocation, $q$ matches $p$ on the strata exactly instead of on average, so estimates vary less |
| **Which models care** | Every model, through the variance of what it is fit on; most visible for rare strata |
| **Fit on** | The population frame: stratum sizes |
| **Failure modes** | Strata unrelated to the target (no gain); disproportionate allocation without weights (biased estimates) |
| **Alternatives** | Simple random sampling; post-stratification weights ($w$) |
| **Checked by** | `tests/test_selection.py::test_stratified_sampling_lowers_the_variance_of_the_mean` |
:::
