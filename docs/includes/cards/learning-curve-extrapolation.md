::: {.callout-tip title="Data card: Estimating data needs from a pilot learning curve"}
| | |
|---|---|
| **Changes** | Evaluation only: fits a parametric curve (here POW3, $A n^{-B} + C$) to errors measured on subsets of a pilot dataset, and extrapolates |
| **Assumption** | The fitted form holds beyond the pilot range; the pilot range already shows the asymptotic behavior; the floor $C$ is identifiable from the pilot |
| **What it does to the learned function** | None on the model; an estimate, with an interval, of the error at a larger $n$ or of the $n$ needed for a target error |
| **Which models care** | Any model; the estimate is specific to the model and its settings |
| **Fit on** | The pilot data only, with train/test splits that never put copies of a row on both sides (bootstrap included) |
| **Failure modes** | The floor is poorly determined, so targets near it are often judged unreachable; the pre-asymptotic curve is steeper than the asymptote, so needed sizes are underestimated; intervals are wide |
| **Alternatives** | An independent estimate of the noise floor (repeated measurements or labels); collecting a second, larger pilot |
| **Checked by** | `tests/test_learning_curves.py::test_extrapolated_data_requirement_is_biased_and_needs_the_floor` |
:::
