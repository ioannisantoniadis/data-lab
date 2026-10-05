::: {.callout-tip title="Data card: Detecting shift with two-sample tests"}
| | |
|---|---|
| **Changes** | Evaluation only: compares new inputs with reference inputs (and, with labels, new accuracy with reference accuracy) |
| **Assumption** | Samples within each period are i.i.d.; for input-only tests, the shift that matters shows up in $p(x)$ |
| **What it does to the learned function** | None on the model; an alarm that the training distribution no longer matches deployment |
| **Which models care** | All |
| **Fit on** | A reference sample from training time; for the classifier test, half of each sample (the other half is held out) |
| **Failure modes** | Concept shift leaves the inputs unchanged and is invisible to input-only tests; small shifts need large samples; a detected shift may not hurt the model, and an undetected one may |
| **Alternatives** | Monitoring the deployed model's accuracy on a stream of labeled cases; monitoring its predicted-class distribution (prior shift) |
| **Checked by** | `tests/test_shift_detection.py::test_input_tests_detect_covariate_and_prior_shift_not_concept_shift` |
:::
