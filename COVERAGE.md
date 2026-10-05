# Coverage

Generated in Phase 0 from SPEC §6 (updated for SPEC v0.2). Every item is ticked, with its chapter, before release
(SPEC §13). Depths: **D** derived or demonstrated in full, with a test or computed figure;
**S** stated precisely with a citation and used; **M** mentioned with a pointer.

A box is ticked only when the item is present at its depth *and*, for D items, its test passes
and its figure was inspected. Parts I and II ticked 2026-10-05 (Phase 2); the owner's reading
of each chapter (SPEC §13) is tracked in ROADMAP.md, not here.

## Part I. Where data comes from

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [x] | Target vs. training distribution | D | [The Data-Generating Process](docs/chapters/01-the-data-generating-process.qmd) |
| [x] | Selection bias from non-random sampling (tabular testbed) | D | [The Data-Generating Process](docs/chapters/01-the-data-generating-process.qmd) |
| [x] | Sampling designs | S | [The Data-Generating Process](docs/chapters/01-the-data-generating-process.qmd) |
| [x] | Dataset documentation | S | [The Data-Generating Process](docs/chapters/01-the-data-generating-process.qmd) |
| [x] | Class-conditional label noise and its effect on the learned classifier | D | [Labels](docs/chapters/02-labels.qmd) |
| [x] | Label-error detection | S | [Labels](docs/chapters/02-labels.qmd) |
| [x] | Structure and plausible invariances of each data type | S | [Data Types and Their Structure](docs/chapters/03-data-types.qmd) |
| [x] | Spectrograms as a representation (synthetic audio) | D | [Data Types and Their Structure](docs/chapters/03-data-types.qmd) |
| [x] | Temporal leakage | D | [Data Types and Their Structure](docs/chapters/03-data-types.qmd) |

## Part II. Transforming data

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [x] | MCAR / MAR / MNAR | S | [Cleaning: Missing Values, Duplicates, Outliers, Leakage](docs/chapters/04-cleaning.qmd) |
| [x] | Bias of mean imputation and complete-case analysis under each mechanism | D | [Cleaning: Missing Values, Duplicates, Outliers, Leakage](docs/chapters/04-cleaning.qmd) |
| [x] | Duplicates inflating test scores | D | [Cleaning: Missing Values, Duplicates, Outliers, Leakage](docs/chapters/04-cleaning.qmd) |
| [x] | Train-only fitting of preprocessing (leakage demonstration) | D | [Cleaning: Missing Values, Duplicates, Outliers, Leakage](docs/chapters/04-cleaning.qmd) |
| [x] | Affine scalers preserve shape | D | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [x] | Trees invariant under monotone transforms | D | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [x] | Distance-based models change under scaling | D | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [x] | Feature scaling changes least-squares conditioning (test: claim 21); consequence for gradient descent (pointer to optimization-lab) | S | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [x] | RobustScaler and outliers | D | [Affine Scaling](docs/chapters/05-affine-scaling.qmd) |
| [x] | Log transform | D | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [x] | Box-Cox, including the lambda MLE | D | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [x] | Yeo-Johnson | S | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [x] | Quantile transform and distance distortion | D | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [x] | Retransformation bias and smearing | D | [Changing the Shape](docs/chapters/06-changing-the-shape.qmd) |
| [x] | One-hot / ordinal / hashing | S | [Encoding and Features](docs/chapters/07-encoding-and-features.qmd) |
| [x] | Target-encoding leakage and cross-fitting | D | [Encoding and Features](docs/chapters/07-encoding-and-features.qmd) |
| [x] | Discretization and splines | S | [Encoding and Features](docs/chapters/07-encoding-and-features.qmd) |
| [x] | TF-IDF | S | [Encoding and Features](docs/chapters/07-encoding-and-features.qmd) |

## Part III. Shaping the training distribution

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [x] | Resampling vs. reweighting vs. threshold, and their effect on calibrated probabilities | D | [Sampling and Weighting](docs/chapters/08-sampling-and-weighting.qmd) |
| [x] | Prior-shift correction (EM, Saerens et al.) | D | [Sampling and Weighting](docs/chapters/08-sampling-and-weighting.qmd) |
| [x] | SMOTE (with a failure case at D) | S | [Sampling and Weighting](docs/chapters/08-sampling-and-weighting.qmd) |
| [x] | Importance weighting under known covariate shift, including its variance | D | [Sampling and Weighting](docs/chapters/08-sampling-and-weighting.qmd) |
| [x] | Augmentation as invariance (testbed with a known invariance) | D | [Augmentation](docs/chapters/09-augmentation.qmd) |
| [x] | Label-changing augmentation | D | [Augmentation](docs/chapters/09-augmentation.qmd) |
| [x] | Mixup | S | [Augmentation](docs/chapters/09-augmentation.qmd) |
| [x] | SpecAugment and RandAugment | S | [Augmentation](docs/chapters/09-augmentation.qmd) |
| [x] | The shift taxonomy | S | [Distribution Shift](docs/chapters/10-distribution-shift.qmd) |
| [x] | Shift detection (two-sample test on the testbed) | D | [Distribution Shift](docs/chapters/10-distribution-shift.qmd) |

## Part IV. How much data, and which

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [x] | Learning-curve estimation and extrapolation with uncertainty | D | [Learning Curves](docs/chapters/11-learning-curves.qmd) |
| [x] | The Bayes floor | D | [Learning Curves](docs/chapters/11-learning-curves.qmd) |
| [x] | Dependence on noise and target complexity | D | [Learning Curves](docs/chapters/11-learning-curves.qmd) |
| [x] | Power-law scaling (with evidence labels) | S | [Scaling Laws](docs/chapters/12-scaling-laws.qmd) |
| [x] | Compute-optimal allocation | S | [Scaling Laws](docs/chapters/12-scaling-laws.qmd) |
| [x] | Repeated-data returns | S | [Scaling Laws](docs/chapters/12-scaling-laws.qmd) |
| [x] | Hutter's model and its exponent (exact) | D | [Why Power Laws: The Long Tail](docs/chapters/13-why-power-laws.qmd) |
| [x] | Coverage-driven selection on the same model (SPEC §7) | D | [Why Power Laws: The Long Tail](docs/chapters/13-why-power-laws.qmd) |
| [x] | The quantization model | S | [Why Power Laws: The Long Tail](docs/chapters/13-why-power-laws.qmd) |
| [x] | Memorization and the long tail | S | [Why Power Laws: The Long Tail](docs/chapters/13-why-power-laws.qmd) |
| [x] | Deduplication (text testbed) | D | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [x] | Easy/hard pruning crossover (teacher-student, multi-seed) | D | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [x] | Difficulty scores | S | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [x] | RHO-LOSS | S | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [x] | Data mixtures | S | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [x] | Large-scale filtering | S/M | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [x] | Active learning (uncertainty-sampling demonstration) | D | [Choosing Data](docs/chapters/14-choosing-data.qmd) |
| [x] | Model collapse (resampling from own fit on the Zipf testbed) | D | [Choosing Data](docs/chapters/14-choosing-data.qmd) |

## Part V. Synthesis

| Done | Item | Depth | Chapter |
|---|---|---|---|
| [x] | Every data card in the generated table | D | [A Data Decision Guide](docs/chapters/15-decision-guide.qmd) |
| [x] | Two worked examples (one tabular, one image or audio) | D | [A Data Decision Guide](docs/chapters/15-decision-guide.qmd) |
