::: {.callout-tip title="Data card: RHO-LOSS (reducible holdout loss selection)"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: within each batch, trains on the points whose training loss most exceeds the loss of a small model trained on holdout data |
| **Assumption** | Holdout data from $p$ is available; a small model's loss estimates what is irreducible (noise) for each point |
| **What it does to the learned function** | Skips points that are already learned and points that are noisy or unlearnable, which plain high-loss selection would pick |
| **Which models care** | Reported for neural networks trained by SGD |
| **Fit on** | A holdout set, through the irreducible-loss model |
| **Failure modes** | A poor irreducible-loss model misjudges noise; holdout data that is not from $p$ |
| **Alternatives** | Uniform sampling; uncertainty or high-loss selection |
| **Checked by** | Not tested here; stated from [@mindermann2022prioritized] |
:::
