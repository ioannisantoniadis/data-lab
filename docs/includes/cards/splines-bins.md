::: {.callout-tip title="Data card: Splines and discretization"}
| | |
|---|---|
| **Changes** | Representation (of a numeric $x$): a basis of piecewise polynomials (splines) or of interval indicators (bins) |
| **Assumption** | The effect of $x$ is smooth (splines) or roughly constant within intervals (bins); enough data per knot or bin |
| **What it does to the learned function** | A linear model can fit a curve in $x$; bins give a step function, splines a smooth one |
| **Which models care** | Linear and GLM-type models; trees already cut a feature into intervals |
| **Fit on** | Training data only: knot or bin positions (quantiles or a uniform grid) |
| **Failure modes** | Too many knots or bins (variance); extrapolation beyond the training range; bins hide variation within an interval |
| **Alternatives** | A shape-changing transform; a model that is nonlinear in $x$ itself |
| **Checked by** | `tests/test_encoding.py::test_splines_and_bins_let_a_linear_model_fit_a_curve` |
:::
