::: {.callout-tip title="Data card: SMOTE (synthetic minority oversampling)"}
| | |
|---|---|
| **Changes** | Sampling distribution $q$: adds synthetic minority examples on segments between a minority example and one of its $k$ nearest minority neighbors |
| **Assumption** | The minority class occupies the space between nearby minority examples (locally convex); features are on comparable scales |
| **What it does to the learned function** | More minority examples near existing ones; the minority region looks broader and smoother |
| **Which models care** | Models whose boundary depends on where minority examples lie (nearest neighbors, trees, kernels) |
| **Fit on** | Training minority examples only, inside each training fold |
| **Failure modes** | Minority clusters smaller than $k$, or separated by majority regions: synthetic points land between clusters; noisy minority labels are interpolated; applied before the split it leaks |
| **Alternatives** | Class weights; random oversampling; prior-shift correction |
| **Checked by** | `tests/test_imbalance.py::test_smote_fills_the_gap_when_k_exceeds_cluster_size` |
:::
