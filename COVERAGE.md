# Coverage

Generated in Phase 0 from SPEC §6 (updated for SPEC v0.2). Every item is ticked, with its chapter, before release
(SPEC §13). Depths: **D** derived or demonstrated in full, with a test or computed figure;
**S** stated precisely with a citation and used; **M** mentioned with a pointer.

A box is ticked only when the item is present at its depth *and*, for D items, its test passes
and its figure was inspected.

## Part I. Where data comes from

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [ ] | Target vs. training distribution | D | [The Data-Generating Process](docs/chapters/01-the-data-generating-process.qmd) |
| [ ] | Selection bias from non-random sampling (tabular testbed) | D | [The Data-Generating Process](docs/chapters/01-the-data-generating-process.qmd) |
| [ ] | Sampling designs | S | [The Data-Generating Process](docs/chapters/01-the-data-generating-process.qmd) |
| [ ] | Dataset documentation | S | [The Data-Generating Process](docs/chapters/01-the-data-generating-process.qmd) |
| [ ] | Class-conditional label noise and its effect on the learned classifier | D | [Labels](docs/chapters/02-labels.qmd) |
| [ ] | Label-error detection | S | [Labels](docs/chapters/02-labels.qmd) |
| [ ] | Structure and plausible invariances of each data type | S | [Data Types and Their Structure](docs/chapters/03-data-types.qmd) |
| [ ] | Spectrograms as a representation (synthetic audio) | D | [Data Types and Their Structure](docs/chapters/03-data-types.qmd) |
| [ ] | Temporal leakage | D | [Data Types and Their Structure](docs/chapters/03-data-types.qmd) |

## Part II. Transforming data

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [ ] | MCAR / MAR / MNAR | S | [Cleaning: Missing Values, Duplicates, Outliers, Leakage](docs/chapters/04-cleaning.qmd) |
| [ ] | Bias of mean imputation and complete-case analysis under each mechanism | D | [Cleaning: Missing Values, Duplicates, Outliers, Leakage](docs/chapters/04-cleaning.qmd) |
| [ ] | Duplicates inflating test scores | D | [Cleaning: Missing Values, Duplicates, Outliers, Leakage](docs/chapters/04-cleaning.qmd) |
| [ ] | Train-only fitting of preprocessing (leakage demonstration) | D | [Cleaning: Missing Values, Duplicates, Outliers, Leakage](docs/chapters/04-cleaning.qmd) |
| [ ] | Affine scalers preserve shape | D | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [ ] | Trees invariant under monotone transforms | D | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [ ] | Distance-based models change under scaling | D | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [ ] | Feature scaling changes least-squares conditioning (test: claim 21); consequence for gradient descent (pointer to optimization-lab) | S | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [ ] | RobustScaler and outliers | D | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [ ] | Log transform | D | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [ ] | Box-Cox, including the lambda MLE | D | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [ ] | Yeo-Johnson | S | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [ ] | Quantile transform and distance distortion | D | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [ ] | Retransformation bias and smearing | D | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [ ] | One-hot / ordinal / hashing | S | [Encoding and Features](docs/chapters/07-encoding-and-features.qmd) |
| [ ] | Target-encoding leakage and cross-fitting | D | [Encoding and Features](docs/chapters/07-encoding-and-features.qmd) |
| [ ] | Discretization and splines | S | [Encoding and Features](docs/chapters/07-encoding-and-features.qmd) |
| [ ] | TF-IDF | S | [Encoding and Features](docs/chapters/07-encoding-and-features.qmd) |

## Part III. Shaping the training distribution

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [ ] | Resampling vs. reweighting vs. threshold, and their effect on calibrated probabilities | D | [Sampling and Weighting](docs/chapters/08-sampling-and-weighting.qmd) |
| [ ] | Prior-shift correction (EM, Saerens et al.) | D | [Sampling and Weighting](docs/chapters/08-sampling-and-weighting.qmd) |
| [ ] | SMOTE (with a failure case at D) | S | [Sampling and Weighting](docs/chapters/08-sampling-and-weighting.qmd) |
| [ ] | Importance weighting under known covariate shift, including its variance | D | [Sampling and Weighting](docs/chapters/08-sampling-and-weighting.qmd) |
| [ ] | Augmentation as invariance (testbed with a known invariance) | D | [Augmentation](docs/chapters/09-augmentation.qmd) |
| [ ] | Label-changing augmentation | D | [Augmentation](docs/chapters/09-augmentation.qmd) |
| [ ] | Mixup | S | [Augmentation](docs/chapters/09-augmentation.qmd) |
| [ ] | SpecAugment and RandAugment | S | [Augmentation](docs/chapters/09-augmentation.qmd) |
| [ ] | The shift taxonomy | S | [Distribution Shift](docs/chapters/10-distribution-shift.qmd) |
| [ ] | Shift detection (two-sample test on the testbed) | D | [Distribution Shift](docs/chapters/10-distribution-shift.qmd) |

## Part IV. How much data, and which

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [ ] | Learning-curve estimation and extrapolation with uncertainty | D | [Learning Curves](docs/chapters/11-learning-curves.qmd) |
| [ ] | The Bayes floor | D | [Learning Curves](docs/chapters/11-learning-curves.qmd) |
| [ ] | Dependence on noise and target complexity | D | [Learning Curves](docs/chapters/11-learning-curves.qmd) |
| [ ] | Power-law scaling (with evidence labels) | S | [Scaling Laws](docs/chapters/12-scaling-laws.qmd) |
| [ ] | Compute-optimal allocation | S | [Scaling Laws](docs/chapters/12-scaling-laws.qmd) |
| [ ] | Repeated-data returns | S | [Scaling Laws](docs/chapters/12-scaling-laws.qmd) |
| [ ] | Hutter's model and its exponent (exact) | D | [Why Power Laws: The Long Tail](docs/chapters/13-why-power-laws.qmd) |
| [ ] | Coverage-driven selection on the same model (SPEC §7) | D | [Why Power Laws: The Long Tail](docs/chapters/13-why-power-laws.qmd) |
| [ ] | The quantization model | S | [Why Power Laws: The Long Tail](docs/chapters/13-why-power-laws.qmd) |
| [ ] | Memorization and the long tail | S | [Why Power Laws: The Long Tail](docs/chapters/13-why-power-laws.qmd) |
| [ ] | Deduplication (text testbed) | D | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [ ] | Easy/hard pruning crossover (teacher-student, multi-seed) | D | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [ ] | Difficulty scores | S | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [ ] | RHO-LOSS | S | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [ ] | Data mixtures | S | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [ ] | Large-scale filtering | S/M | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [ ] | Active learning (uncertainty-sampling demonstration) | D | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [ ] | Model collapse (resampling from own fit on the Zipf testbed) | D | [Choosing Data](docs/chapters/14-choosing-data.qmd) |

## Part V. Synthesis

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [ ] | Every data card in the generated table | D | [A Data Decision Guide](docs/chapters/15-decision-guide.qmd) |
| [ ] | Two worked examples (one tabular, one image or audio) | D | [A Data Decision Guide](docs/chapters/15-decision-guide.qmd) |
