# SPEC: data for learning, from first principles

**Status:** v0.3, 2026-10-04 (revised at Gate 0, `DECISIONS.md` D7 and `review.md`; and at
Gate 1, D8). Repo `data-lab`; title *What the Model Sees: Training
Data from First Principles* (see [`DECISIONS.md`](DECISIONS.md)); license MIT. This file is the implementation contract for the agent that
builds the book. Read it end to end before writing anything.

**Owner:** Ioannis Antoniadis. **Authors:** Ioannis Antoniadis, with Claude (Anthropic), as in
the sibling `objectives-book` (its DECISIONS D10).

**Decisions:** those reserved for the owner are in `DECISIONS.md` and marked ⚑ below. The
implementing agent decides everything else, records the reasoning in `ROADMAP.md`, and reports.

---

## Contents

1. [What this book is](#1-what-this-book-is)
2. [Thesis and lens](#2-thesis-and-lens)
3. [Reader, prerequisites, scope](#3-reader-prerequisites-scope)
4. [Neighbors and positioning](#4-neighbors-and-positioning)
5. [Architecture](#5-architecture)
6. [Coverage criteria](#6-coverage-criteria)
7. [Ground-truth testbeds](#7-ground-truth-testbeds)
8. [Claims to test](#8-claims-to-test)
9. [Figures](#9-figures)
10. [Recurring devices](#10-recurring-devices)
11. [Style](#11-style)
12. [Process and guardrails](#12-process-and-guardrails)
13. [Acceptance criteria](#13-acceptance-criteria)
14. [Success criteria](#14-success-criteria)
15. [Plan and gates](#15-plan-and-gates)
16. [Repository layout and tooling](#16-repository-layout-and-tooling)
17. [Risks](#17-risks)
18. [Agent operating rules](#18-agent-operating-rules)

Appendices: [A. Source starting points](#appendix-a-source-starting-points) ·
[B. Glossary](#appendix-b-glossary-of-this-specs-terms)

---

## 1. What this book is

A short Quarto book, with code, about **data for learning** (training, evaluation and test data): where it comes from, how it is
transformed, how the training distribution is shaped, and how much of it (and which of it) a
model needs. It is a sibling of `loss-functions-lab` (what to optimize) and `optimization-lab`
(how to optimize). This book covers what the model is optimized *on*.

The book answers practical questions with derivations and computed evidence rather than
rules of thumb:

- When to use a log transform rather than standard or min-max scaling, and which models
  care at all.
- What text, images, audio and tables each require, and why.
- When to resample a dataset and when to reweight it.
- What augmentation actually adds to a model.
- How much data a problem needs, and what that number depends on.
- Why returns on more data diminish as a power law.
- How smarter data selection can beat that law.

**Size.** The content sets the length, within a cap:

| Book | Words |
|---|---|
| `optimization-lab` | ≈ 15,000 |
| `math-conceptual-map` | ≈ 28,000 |
| `loss-functions-lab` | ≈ 29,000 |
| `rl-for-llms` | ≈ 37,000 |

Counts are raw words (`wc -w`) in `docs/**/*.qmd`, measured 2026-10-04. Counted as prose by
`scripts/word_count.py` (no code, math or markup), the same books are about 9,100, 24,800,
25,600 and 33,100 words. **The cap and target below are prose words, as counted by
`scripts/word_count.py`** (owner decision at Gate 0, D7).

- **Target:** 22,000–30,000 words of prose.
- **Hard cap:** 35,000 words.
- **If a chapter exceeds its share,** cut it or move material to a pointer. Never go over the
  cap.

## 2. Thesis and lens

### 2.1 Thesis

> A model learns the distribution it is trained on, through the representation it is given.
> Every technique that acts on training data changes one or more of four things:
>
> - the **representation**: how inputs and targets are encoded and transformed;
> - the **sampling distribution** q: which examples are drawn, compared with the target
>   distribution p the model will face;
> - the **weights** w: how much each example counts;
> - the **labels**: what each example says.
>
> Which of the four a technique changes determines what it can fix and what it can break.
> Resampling with q and reweighting with w target the same population objective (the
> effective distribution, proportional to q·w); the split between them sets the finite-sample
> variance. Techniques that act only on evaluation (splits, leakage control, shift detection,
> learning-curve estimation) change what we measure, not what the model learns, and their
> cards say so.
>
> How much data a problem needs depends on noise, the complexity of the target, the input
> dimension, and the probability mass in rare but necessary cases. Where learning is
> memorization-like and inputs are long-tailed, the last of these dominates: error is the mass
> of what has not yet been covered. Uniform sampling reaches that mass slowly, because most
> draws repeat what is already covered. A selector that targets the uncovered steepens the
> power law, but only with an oracle for what is covered; real selection methods approximate
> that oracle, with mixed results at scale. Other accounts (data-manifold dimension;
> variance- vs. resolution-limited regimes) explain power laws without a long tail, and the
> book presents them alongside.

This deliberately mirrors `rl-for-llms` Thesis 2: every method is a sampling distribution q
plus per-sample weights w. Here the same pair describes data engineering. The book states
this connection and links it; it does not re-derive the RL side. The older lineage
(importance weighting under covariate shift; the dataset-shift literature) gets a lineage
callout, sourced in Phase 3.

The v0.1 wording ("is set by" the long tail; uniform sampling's redundancy as "one explanation
of power-law returns"; selection that can "beat that law") was revised at Gate 0 after
`review.md`: redundancy explains the slower exponent, the tail mass explains the power law,
and an oracle selector is still a power law.

### 2.2 The lens: the data card

Every technique gets a **data card**, generated from a record in `scripts/technique_data.py`:

| Field | Question | Example (log-transforming a skewed target) |
|---|---|---|
| Changes | Representation / q / w / labels, or *evaluation only* | Representation (of y) |
| Assumption | What must be true for it to help | y > 0, with multiplicative noise or right skew |
| What it does to the learned function | In terms of the loss's minimizer | With MSE, the model learns E[log y ∣ x]: on the original scale, a geometric-mean-like prediction, not the mean |
| Which models care | Model families whose results change | Linear and GLM-type models, neural nets; trees much less |
| Fit on | What data its parameters are estimated from | None (a fixed function); the smearing correction is fit on training residuals |
| Failure modes | How it breaks | Retransformation bias; zeros and negatives; heavy-tailed residuals after transform |
| Alternatives | Same goal, other trade-off | Box-Cox / Yeo-Johnson; a log-link GLM; a loss matched to the noise |
| Checked by | Test name | `tests/test_transforms.py::test_log_target_mse_predicts_geometric_mean` |

The example row's claims are what the book must derive and test. Duan (1983) introduces the
smearing estimate (Crossref-verified bibliographic data; content to be read in Phase 2).

**Evaluation-only techniques** (splits, leakage control, shift detection, learning-curve
estimation) get cards with *Changes: evaluation only*; the *Fit on* field carries the leakage
lesson.

**Falsifiability.** Where a technique does not fit the four-way split cleanly (for example,
deduplication changes both q and the effective weights), the card says so. A lens that fits
everything by being vague is not the goal.

## 3. Reader, prerequisites, scope

**Reader.**

- An engineer or data scientist who trains models and has used scalers, augmentation and
  resampling from a library.
- They want to know *why* and *when* each works, with evidence.
- Same reader as the sibling labs.

**Prerequisites:**

- probability up to conditional expectation and Bayes' rule;
- basic linear algebra;
- Python with NumPy;
- for the scaling-law part, logs and power laws.

`math-conceptual-map` is the pointer for gaps.

**Non-goals** (scope findings at review if covered beyond a mention):

- **Data engineering infrastructure** (pipelines, warehouses, streaming, data versioning
  tools). Link `modern-ai-systems-and-methods` (MLOps chapter).
- **Architectures** (CNNs, transformers). Link `transformer-atlas`. **Tokenizer internals**
  are also out of scope; no sibling covers them (checked 2026-10-04), so chapters 3 and 7
  point to primary sources.
- **Loss derivations, including loss-based remedies for noise and imbalance.** Owned by
  `loss-functions-lab`; link it.
- **Optimizer behavior.** Owned by `optimization-lab`, except where data scaling changes
  conditioning, which is linked.
- **Legal and ethical treatment of data collection** (consent, licensing, privacy law) beyond
  one honest section that points to authoritative sources. Fairness and privacy appear only
  as consequences of sampling choices.
- **Survey breadth.** A technique enters only if it teaches something about the lens or
  answers one of §1's questions.

## 4. Neighbors and positioning

**Sibling repos** (read their `CONVENTIONS.md` and notation appendices first):

| Repo | Relationship |
|---|---|
| `loss-functions-lab` | Owns noise model → loss derivations (MSE → mean, MAE → median) used in chapters 6 and 8; link, don't re-derive. Covers augmentation only inside contrastive objectives. |
| `optimization-lab` | Owns conditioning: its Foundations chapter shows gradient descent slowed by an ill-conditioned quadratic. It does not connect conditioning to feature scaling (checked 2026-10-04), so chapter 5 states and tests that bridge, then links for the consequence. It has no CONVENTIONS.md or notation appendix. |
| `rl-for-llms` | Owns the (q, w) weighted-likelihood view and the toy-language testbed; chapter 8 links it. |
| `transformer-atlas` | Owns architectures. Has no tokenization material (checked 2026-10-04). |
| `modern-ai-systems-and-methods` | Mentions leakage, drift and active learning briefly; this book goes deeper. Link both ways. |
| `math-conceptual-map` | Prerequisites. |
| `objectives-book` | Standalone for now; may later become part of it (D6, closed). Keep its conventions where possible. Do not edit it from here. |

A grep of the sibling repos (2026-10-04) found no coverage of the following:

- scaling laws (beyond a mention), data pruning or selection;
- deduplication;
- log/power/quantile transforms;
- missing-data mechanisms;
- data mixtures.

The gap is real.

**External positioning** (Phase 0 task, not yet done): find and read the closest books and
courses on data preparation and data-centric ML. Candidates to search for:

- feature-engineering books;
- data-centric AI courses;
- the survey literature in Appendix A.

State in `research-log.md` and the README what this book adds. The candidate claims, which
Phase 0 must verify:

1. Every technique is placed on one lens (§2) and tested against exact ground truth.
2. Classical preprocessing and modern data selection and scaling laws are in one argument.
3. The long-tail account of data requirements is reproduced exactly, in a form a
   practitioner can run, and connected to the data levers. (v0.1 said "made computable";
   Hutter 2021 and Dohmatob et al. 2024 already did that at research level.)

If an existing work already does all three, stop and report.

**Phase 0 result (2026-10-04):** no work found does all three; claims 1 and 2 are distinctive;
claim 3 was reworded as above. Details in `research-log.md`.

## 5. Architecture

Sixteen chapters in five parts. Chapters are short: 1,200–2,200 words of prose each. Titles
are working titles.

### Part 0: Orientation

| # | Chapter | Content |
|---|---|---|
| 0 | The Map | The four-way lens; the questions of §1 and where each is answered; reading paths |

### Part I: Where data comes from

| # | Chapter | Key content |
|---|---|---|
| 1 | The data-generating process | Population vs. sample; target distribution p vs. training distribution q; i.i.d. and its violations; sampling designs (simple random, stratified, cluster, convenience) and selection bias; documenting a dataset (Gebru et al.) |
| 2 | Labels | Where labels come from; annotation and agreement; label-noise models (class-conditional); finding label errors (confident learning); when a label is a measurement with its own noise. Pointer for loss-based remedies: `loss-functions-lab` |
| 3 | Data types and their structure | Tabular (numeric, categorical, ordinal, datetime), text (tokens, Zipf-like frequencies), images (pixels, spatial structure, invariances), audio (waveform, sampling rate, spectrograms), time series (order, autocorrelation, leakage through time), graphs (pointer). For each: what structure exists, which invariances are plausible, which representation exposes them |

### Part II: Transforming data

| # | Chapter | Key content |
|---|---|---|
| 4 | Cleaning: missing values, duplicates, outliers, leakage | Missing-data mechanisms MCAR/MAR/MNAR (Rubin 1976) and what each imputation does under each; multiple imputation (pointer, van Buuren); duplicates and near-duplicates; outliers: error vs. tail; leakage taxonomy (Kaufman et al.) and fitting transforms on training data only |
| 5 | Affine scaling | Standard, min-max, max-abs, robust scaling: all affine per feature, so they **do not change the shape** of a distribution. Which models care (distance-based, regularized, and gradient-trained models; tree splits are unaffected by monotone transforms); outlier sensitivity; per-sample normalization is a different operation |
| 6 | Changing the shape | Log, Box-Cox (strictly positive data), Yeo-Johnson, quantile transforms: nonlinear, so they **change what the model sees** and what MSE averages. Feature transforms vs. target transforms; retransformation bias and smearing; the quantile transform distorts distances; a decision guide against chapter 5 |
| 7 | Encoding and features | One-hot, ordinal, hashing, target encoding (and its leakage without cross-fitting); discretization; splines and polynomials; text vectorization from counts to TF-IDF (embeddings: pointer); image and audio input normalization |

### Part III: Shaping the training distribution

| # | Chapter | Key content |
|---|---|---|
| 8 | Sampling and weighting | Class imbalance: resampling vs. reweighting vs. moving the threshold, and what each does to the learned probabilities; correcting for a known prior shift (Saerens et al.; King & Zeng); SMOTE (Chawla et al.) and its assumptions; stratified splits; importance weighting for covariate shift, and its variance. The (q, w) lens made explicit |
| 9 | Augmentation | Augmentation as an invariance assumption, or a prior, that expands q; label-preserving vs. label-changing transforms; images (geometric, color; RandAugment), audio (SpecAugment), text (and why text is hard); mixup as vicinal risk; when augmentation hurts |
| 10 | Distribution shift | Covariate, prior and concept shift (Moreno-Torres et al.); detecting shift; what reweighting can and cannot fix; evidence that test sets drift (Recht et al.) |

### Part IV: How much data, and which

| # | Chapter | Key content |
|---|---|---|
| 11 | Learning curves | Definition, estimation and shapes (Viering & Loog); the Bayes-error floor; what sample size depends on (noise, complexity of the target, input dimension, the mass in rare cases); estimating "how much data" from a pilot study by fitting and extrapolating a learning curve, with honest uncertainty; classical bounds as a pointer, not a course |
| 12 | Scaling laws | Empirical power laws in data and model size (Hestness et al.; Kaplan et al.; Rosenfeld et al.); compute-optimal allocation (Hoffmann et al.); variance- vs. resolution-limited regimes (Bahri et al.); repeated data (Muennighoff et al.). Evidence labels and dates throughout |
| 13 | Why power laws: the long tail | **The signature chapter.** Hutter's toy model: memorizing a Zipf-distributed feature stream gives error n^(−α/(1+α)); the quantization model (Michaud et al.); memorization of rare subpopulations (Feldman); long-tail knowledge in LLMs (Kandpal et al.). The owner's intuition, made computable: uniform sampling spends its budget on what is already covered |
| 14 | Choosing data | Deduplication (Lee et al.); pruning by difficulty and the easy/hard crossover (Sorscher et al.), with difficulty scores EL2N/GraNd (Paul et al.) and forgetting events (Toneva et al.); proxy selection (Coleman et al.); learnable and not-yet-learnt points (Mindermann et al.); mixtures (DoReMi); filtering at scale (DataComp, FineWeb); active learning; synthetic data and model collapse (Shumailov et al.) |

### Part V: Synthesis

| # | Chapter | Content |
|---|---|---|
| 15 | A data decision guide | The generated table of every data card; a decision procedure (question → which of the four levers → technique → check), with two worked examples: one tabular, one image or audio |

**Appendices:**

- notation;
- the testbeds;
- glossary;
- further reading;
- "What the toys cannot show" (a consolidated list).

The agent may merge or split chapters (record why in `ROADMAP.md`), but may not drop a
coverage item (§6) or exceed the size cap (§1).

## 6. Coverage criteria

**Depths:**

- **D:** derived or demonstrated in full, with a test or computed figure.
- **S:** stated precisely with a citation and used.
- **M:** mentioned with a pointer.

`COVERAGE.md` is created in Phase 0 from this list. Every item is ticked, with its chapter,
before release.

**Part I:**

- target vs. training distribution (D);
- selection bias from non-random sampling (D, on the tabular testbed);
- sampling designs (S);
- dataset documentation (S);
- class-conditional label noise and its effect on the learned classifier (D);
- label-error detection (S);
- the structure and plausible invariances of each data type (S);
- spectrograms as a representation (D, on synthetic audio);
- temporal leakage (D).

**Part II:**

- MCAR/MAR/MNAR (S) and the bias of mean imputation and complete-case analysis under each (D);
- duplicates inflating test scores (D);
- train-only fitting of preprocessing (D: a leakage demonstration);
- affine scalers preserve shape (D);
- which models are invariant to which transforms: trees under monotone transforms (D),
  distance-based models under scaling (D);
- feature scaling changes the conditioning of least squares (S, with a test); its consequence
  for gradient descent (M → optimization-lab);
- RobustScaler and outliers (D);
- log transform (D);
- Box-Cox (D, including the λ MLE);
- Yeo-Johnson (S);
- quantile transform and distance distortion (D);
- retransformation bias and smearing (D);
- one-hot / ordinal / hashing (S);
- target-encoding leakage and cross-fitting (D);
- discretization and splines (S);
- TF-IDF (S).

**Part III:**

- resampling vs. reweighting vs. threshold, with their effect on calibrated probabilities (D);
- prior-shift correction (D: EM, Saerens et al.);
- SMOTE (S, with a failure case D);
- importance weighting under known covariate shift, including its variance (D);
- augmentation as invariance (D, on a testbed with a known invariance);
- label-changing augmentation (D);
- mixup (S);
- SpecAugment and RandAugment (S);
- the shift taxonomy (S);
- shift detection (D, a two-sample test on the testbed).

**Part IV:**

- learning-curve estimation and extrapolation with uncertainty (D);
- the Bayes floor (D);
- dependence on noise and target complexity (D);
- power-law scaling (S, with evidence labels);
- compute-optimal allocation (S);
- repeated-data returns (S);
- Hutter's model and its exponent (D, exact);
- coverage-driven selection on the same model (D; see §7);
- the quantization model (S);
- memorization and the long tail (S);
- deduplication (D, on the text testbed);
- easy/hard pruning crossover (D, teacher–student, multi-seed);
- difficulty scores (S);
- RHO-LOSS (S);
- data mixtures (S);
- large-scale filtering (S/M);
- active learning (D, on a simple uncertainty-sampling demonstration);
- model collapse (D, a resampling-from-own-fit demonstration on the Zipf testbed).

**Part V:** every data card in the generated table; two worked examples.

## 7. Ground-truth testbeds

Every claim is measured against a known truth. Each testbed must be small enough that every
figure script runs in under a minute on a laptop CPU, with no network access.

| # | Testbed | Ground truth available exactly | Used in |
|---|---|---|---|
| T1 | **Synthetic tabular generator.** Known joint distribution of features and target; switchable skew (log-normal), outliers, heteroscedastic or multiplicative noise, class prior, missingness mechanism (MCAR/MAR/MNAR), covariate and prior shift | Bayes-optimal predictor and risk; true conditional mean, median and geometric mean; true density ratio for shift | Ch 1, 4–8, 10, 11 |
| T2 | **Zipf feature stream (Hutter's model).** Features i with probabilities θ_i ∝ i^−(α+1); deterministic labels; a memorizing learner | Expected error E_n = Σ_i θ_i (1 − θ_i)^n, computed exactly by summation, and the asymptotic exponent α/(1+α) (Hutter 2021, eq. 2 and the Zipf section, verified) | Ch 11, 13, 14 |
| T3 | **Teacher–student perceptron** (Sorscher et al.'s theoretical setting) | The teacher, hence each example's margin, so "easy" and "hard" are known exactly; test error by Monte Carlo on fresh teacher-labeled data | Ch 14 |
| T4 | **Markov text source.** A small vocabulary with Zipf-like unigram frequencies and a known transition matrix; optional injected duplicates | Exact entropy rate, hence the cross-entropy floor for any model; exact duplicate counts | Ch 3, 7, 12, 14 |
| T5 | **Synthetic signals.** Sinusoids with noise for audio; small images from scikit-learn's bundled `load_digits` (no download) for a known invariance experiment | Known generating frequencies; for images, ground-truth invariance only under a defined transform family | Ch 3, 9 |

**Coverage-driven selection on T2.** This is an extension to derive and test, not a claim
from the source. A selector that never draws an already-seen feature reaches error
Σ_{i>n} θ_i after n draws if it takes features in order of frequency. Under Zipf this decays
roughly as n^−α, faster than uniform sampling's n^−α/(1+α). Phase 1 must derive this
properly, state the assumptions (such as knowing which features are seen), test it, and say
what it does and does not imply for real selection methods. If the derivation does not hold
up, record that and revise chapter 13's argument. The selector is still a power law (a
steeper one), not an escape from it, and it needs an oracle; Phase 1 also implements a
non-oracle selector that estimates coverage from counts, so the oracle's share of the gain is
visible. Prior art: Dohmatob et al. (2024) analyze Hutter's model trained on q ≠ p, including
tail cutting and acquiring the missing tail; chapter 13 cites it and checks against it.

**Datasets.** Synthetic, or bundled with scikit-learn. Any external dataset needs an owner
decision (⚑ D5), a license check, and must not be needed by CI.

## 8. Claims to test

Each item is a test in `tests/`, named after the claim. Phase 0 turns this list into test
stubs. Each passes in the phase of its chapter: claims 14–16 in Phase 1, 1–9 and 21 in
Phase 2, 10–13 and 17–20 in Phase 3. Add more as chapters need them.

1. Standard, min-max, max-abs and robust scaling leave sample skewness and kurtosis unchanged
   (affine invariance).
2. A decision tree's predictions are unchanged by any strictly monotone transform of a
   feature (given the same tie-breaking).
3. k-NN predictions change under per-feature rescaling. Show a case where scaling flips the
   prediction.
4. With MSE on log y, back-transforming the predictions estimates exp(E[log y ∣ x]). For
   log-normal noise, this underestimates E[y ∣ x] by the factor exp(σ²/2). The smearing
   estimate corrects it (T1).
5. Box-Cox λ by maximum likelihood recovers a known λ on T1 data.
6. A quantile transform to uniform changes pairwise Euclidean distances (not
   distance-preserving), while preserving ranks within each feature.
7. Under MCAR, mean imputation leaves the mean unbiased but shrinks the variance. Under MAR,
   complete-case estimates of the mean are biased (T1, multi-seed).
8. Target encoding without cross-fitting gives a pure-noise high-cardinality feature a large
   training score and no test advantage. Cross-fitting removes the gap.
9. Fitting a scaler or imputer on train + test changes test metrics vs. fitting on train
   only, in the direction of optimism, on a constructed case.
10. Training on resampled balanced data shifts the predicted probabilities. The prior-shift
    correction p(y ∣ x) ∝ q(y ∣ x) · p(y) / q(y) restores calibration (T1). (v0.1 wrote the
    priors as π_y, which conflicts with §11's "π for policies only".)
11. EM prior estimation (Saerens et al.) recovers a known test prior on T1.
12. Importance weighting with the true density ratio gives an unbiased risk estimate under
    covariate shift, with variance that grows as the shift grows (T1).
13. Augmenting with a transform the true function is invariant to does not hurt test error
    (and helps at small n). Augmenting with a non-invariant transform does hurt. On T5, use
    the synthetic side label: it is exactly invariant under an up-down flip and exactly
    reversed by a left-right flip (digit classes have no exactly known invariance; D8).
14. Hutter's exact sum matches Monte Carlo simulation of the memorizing learner (T2).
15. The log-log slope of E_n approaches −α/(1+α) on T2 for several α.
16. Coverage-driven selection beats uniform sampling at equal budget on T2, at the derived rate
    (§7): the oracle reaches n^−α against uniform's n^−α/(1+α), still a power law. A selector
    that knows nothing about p and labels the most frequent features of an unlabeled pool of M
    draws has expected error at least max(oracle at n, E_M). With M ∝ n it keeps uniform's
    exponent; with M = n^(1+α) it recovers the oracle's (D8).
17. On T3, keeping hard examples beats keeping easy ones when initial data is abundant, and the
    reverse when it is scarce (multi-seed; quote the number of seeds that show it).
18. Removing duplicates from T4 lowers the measured test cross-entropy optimism caused by
    train/test overlap.
19. A learning curve fitted on small n extrapolates to within its stated interval at larger n
    on T1, or the chapter reports that it does not.
20. (Replace regime; checked against the rates of Dohmatob et al. 2024, and contrasted with
    accumulation, Gerstgrasser et al. 2024.) Repeatedly refitting a model on samples from its
    own previous fit loses the tail of T2's distribution (model collapse in miniature,
    multi-seed).
21. Per-feature rescaling changes the condition number of the least-squares Hessian
    (proportional to XᵀX), and standardization reduces it on a constructed T1 case (added at
    Gate 0: the bridge `optimization-lab` does not cover).

## 9. Figures

**Mechanics:**

- One script per figure (`scripts/figures/fig_<slug>.py`), importing the package.
- Each script writes `docs/images/<slug>.png` at ≥ 200 dpi, through a shared `save_figure`
  in the theme module.
- Each script has a docstring ending "this figure makes visible that …".
- Run every script and look at the image before the chapter counts as done.

**Colors and theme:**

- **Palette:** use the sibling palette (`rl-for-llms/scripts/figures/_theme.py`) and its ink
  and surface tokens.
- **Color is semantic:** it encodes which of the four levers a technique pulls
  (representation / q / w / labels). Elsewhere, assign the categorical order in a fixed
  order, never cycled.
- **Validation:** validate the palette with the dataviz validator.

**Signature figure (Phase 1, before any chapter):**

- **Panel A:** T2's exact learning curves for several α on log-log axes, with Monte Carlo
  points and the n^−α/(1+α) guide lines.
- **Panel B:** uniform sampling vs. coverage-driven selection at equal budget, oracle and
  non-oracle, with the n^−α guide line.

If this figure does not make the long-tail argument visibly, rethink chapter 13 before
writing it.

**Also required:**

- affine vs. nonlinear transforms on the same skewed feature: histograms plus what MSE
  averages;
- the resampling vs. reweighting vs. threshold calibration comparison;
- missingness mechanisms vs. imputation bias;
- the easy/hard pruning crossover on T3;
- learning-curve extrapolation with its interval;
- the decision-guide table (generated).

## 10. Recurring devices

- **Chapter template** (from `learning-repo-build`):
  - motivating problem (no heading);
  - `## The problem`;
  - `## Assumptions` (what breaks if each fails);
  - `## Derivation or demonstration`;
  - boxed result, then the **data card**;
  - `## What it does to the learned model`;
  - `## Failure modes` (with a computed figure);
  - `## What the toy cannot show`;
  - `## Connections` (2–4 links, each with why).

  The Map and the decision guide may deviate but keep *Connections*.
- **Data cards** (`callout-tip`): §2.2's fields, generated from `scripts/technique_data.py`,
  which also generates chapter 15's table.
- **Lever tags:** representation / q / w / labels on every card.
- **Evidence labels:**
  - *mathematical fact*, stated plainly;
  - *replicated finding*, with citations;
  - *recent/contested*: "the paper reports", dated, with counter-evidence.

  Scaling-law content is mostly the second and third kinds and must be labeled so.
- **"Checked by" notes** naming the test for every checkable statement.
- **Practitioner box** (`callout-note`, "In practice"): the library call (scikit-learn,
  torchaudio, etc.) that does what the chapter derived, and the parameter that matters. It is
  never a substitute for the derivation.

## 11. Style

Inherited from the sibling labs:

- **Voice:** direct, explanatory, unhurried. Plain words; define terms at first use; one
  idea per paragraph; no hype or filler.
- **Derive before naming.** Every rule of thumb ("use RobustScaler with outliers") is earned
  by a demonstration, then stated with its assumptions.
- **Precision:** say which distribution (p or q), which scale (original or transformed),
  which data was used for fitting (train only), and which regime (data-rich or data-scarce)
  every time it could be either.
- **Cross-references by title and link,** targeting Quarto IDs, never hand-typed numbers.
- **Dates:** anything frontier says "as of ⟨Month YYYY⟩".
- **Math and notation:** symbols only from the notation appendix. Reuse the siblings'
  conventions where they exist: π for policies only; p for the target distribution; q for
  the sampling distribution, as in `rl-for-llms`.
- **Portability:** follow `objectives-book` SPEC §21.1 (no layout code in chapters; standard
  LaTeX math; nothing essential only interactive; reasonable widths), so a PDF stays cheap.
- **Economy:** short chapters; if a paragraph can be deleted without loss, delete it.

## 12. Process and guardrails

1. **Use the skills** from the `ioannisantoniadis/claude-skills` marketplace:
   - `learning-repo-build` (plugin `learning-repo`) to build. Follow its phases and its
     playbook.
   - `learning-repo-audit` (same plugin) to judge, run by a **fresh** session with no drafting
     context, after Part II and again at the end.
   - `skeptical-review` (plugin `skeptical-review`) on the thesis (§2) in Phase 0 and on
     chapter 13 before it is accepted.
2. **Never write technical content from memory.** Equations, defaults (including library
   defaults), results, dates and author lists come from the primary source or the official
   documentation, opened and read, and logged in `research-log.md`. Appendix A lists starting
   points; most were verified only for bibliographic data and abstract.
3. **Follow the evidence.** If research contradicts this spec (including §7's extension or a
   thesis sentence), record it, follow the evidence, and report it.
4. **Claims are tests; figures are computations.** Quote numbers from a fresh run, and show
   multi-seed spread for effects about typical behavior.
5. **Library behavior is checked, not recalled.** When the book says what a scikit-learn
   transformer does, a test exercises it against the derivation.
6. **Bounded resources.** Tests and figures are CPU-only, bounded in memory and time, and run
   with `pytest-timeout`.
7. **Owner decisions** (⚑) are asked, not assumed. Everything else is decided and logged.
8. **Commits and pushes** only when the owner asks.

## 13. Acceptance criteria

**Per chapter:**

- [ ] Follows the template; every technique has a generated data card.
- [ ] Every coverage item assigned to it is present at its depth.
- [ ] Every checkable claim names its test, and the test passes.
- [ ] Every empirical claim is labeled; frontier content is dated.
- [ ] Every citation resolves and is logged.
- [ ] Every figure is generated by its script and was inspected after its last change; the
      caption states the lesson.
- [ ] Every symbol is in the notation appendix; cross-references resolve.
- [ ] Within its word share.
- [ ] `quarto render` has no warnings; `ruff` and `pytest` pass.
- [ ] The owner has read it.

**Whole book:**

- [ ] Every chapter is accepted; every `COVERAGE.md` item is ticked.
- [ ] Total prose is ≤ 35,000 words, counted by a script in CI.
- [ ] The decision-guide table is generated and covers every card.
- [ ] A fresh-agent `learning-repo-audit` scores **≥ 4 on every rubric criterion**, with no
      hard fails, and **5** on computed evidence.
- [ ] `skeptical-review` of chapter 13 has no unresolved major issue.
- [ ] CI (lint, tests, render) is green from a clean clone, with locked dependencies.
- [ ] The README states what the book adds over the positioning works (§4), and the claim
      survived Phase 0.

## 14. Success criteria

Acceptance says the book is correct. Success says it is useful.

1. **Decision test.** Give 3–5 target readers who have read the book six realistic data
   scenarios that it does not walk through, for example:
   - a skewed price target;
   - a 1:200 fraud class ratio;
   - a sensor feed with drifting calibration.

   Success: in ≥ 70% of the scenarios, they name the lever, the technique, its key assumption
   and one way it could fail.
2. **"How much data" test.** The same readers, given a small pilot dataset, produce a
   learning-curve estimate of the data needed for a target error, with an honest interval.
3. **Expert read.** One external reviewer, with data-centric ML or applied statistics
   background, finds no wrong core claim and says the lens adds something (⚑ D4).

If the decision test fails after Part II, revisit the lens with the owner before Parts III–IV.

## 15. Plan and gates

Each phase ends with a report and a stop. Nothing passes a gate (⛳) without the owner.

### Phase 0: foundation

- Read the sibling repos (§4).
- Positioning search (§4).
- `skeptical-review` of §2.
- Scaffold with `learning-repo-build`:
  - `README.md`, `CLAUDE.md` (update), `CONVENTIONS.md`, `ROADMAP.md`, `COVERAGE.md`,
    `research-log.md`;
  - the notation appendix;
  - a Quarto skeleton with every chapter stubbed;
  - the package skeleton;
  - the theme module;
  - `scripts/technique_data.py`;
  - test stubs for §8;
  - CI: lint, tests, the render, and the word-count check.
- ⛳ **Gate 0.**

### Phase 1: testbeds and the signature figure

- Implement T1–T5 with their tests.
- Derive and test §7's coverage-selection extension.
- Produce the signature figure and look at it.
- ⛳ **Gate 1:** the signature figure is convincing, or the framing of Part IV is revised.

### Phase 2: Parts I and II

- Write chapters 1–7 in order, per §10.
- Run a fresh-agent audit after chapter 7.
- Run the decision test with Part II material (§14.1, partial).
- ⛳ **Gate 2.**

### Phase 3: Parts III and IV

- Write chapters 8–14.
- Run `skeptical-review` on chapter 13.
- ⛳ **Gate 3.**

### Phase 4: synthesis and release

- Write chapter 15 and the Map last, from the finished chapters.
- Write the appendices.
- Run the final fresh-agent audit and the success tests.
- **Publication:** per the owner (⚑ D5). GitHub Pages on a personal account is public, so do
  not deploy before D5.

Record actual durations in `ROADMAP.md`.

## 16. Repository layout and tooling

```
README.md  CLAUDE.md  SPEC.md  DECISIONS.md  CONVENTIONS.md  ROADMAP.md  COVERAGE.md
research-log.md
docs/                     Quarto book; images/ pre-generated; no code execution at render
src/data_lab/            testbeds T1–T5, transforms, selection methods (NumPy, SciPy, scikit-learn)
tests/                    claim tests (§8)
scripts/figures/          fig_<slug>.py, one per figure; _theme.py with save_figure
scripts/technique_data.py records → data cards and the decision-guide table
scripts/word_count.py     enforces the size cap
.github/workflows/        ci.yml (ruff, pytest, word count), docs.yml (render; deploy after D5)
```

**Tooling:**

- uv with a lockfile; Python ≥ 3.11;
- ruff; pytest with `pytest-timeout`;
- Quarto; GitHub Actions.

**Packaging:** `data_lab` is a local package installed by `uv sync`. It is never published to
PyPI or any other index.

**Core dependencies:**

- NumPy, SciPy, scikit-learn, matplotlib.
- Audio uses NumPy/SciPy only (a short-time Fourier transform), with no audio library.

## 17. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Becomes a catalogue of preprocessing tips | High | Lens (§2), data cards, "derive before naming", coverage depths, size cap |
| Scaling-law content overclaims or dates fast | High | Evidence labels; dates; the toy carries the argument, real-scale results are cited, not reproduced |
| The long-tail story is presented as *the* explanation | Medium | Chapter 13 presents several accounts (Hutter, Michaud, Bahri), with their scopes; `skeptical-review` |
| Toy results mistaken for real-scale results | Medium | Mandatory "What the toy cannot show" section in every chapter |
| Overlap with sibling repos | Medium | §4 ownership table; links instead of re-derivation |
| Library behavior misdescribed | Medium | §12.5: tests exercise the library |
| Size creep beyond the cap | Medium | CI word count; per-chapter shares |

## 18. Agent operating rules

- **Read, in order:**
  1. `CLAUDE.md`;
  2. this file;
  3. `DECISIONS.md`;
  4. `research-log.md`;
  5. the sibling repos' `CONVENTIONS.md` and notation appendices.
- **Process:** follow `learning-repo-build`'s phases; this spec fills in its scope step.
- **Decisions:** ask only ⚑ decisions. Decide everything else, record it in `ROADMAP.md`,
  and report.
- **Boundaries:** never modify sibling repos; propose changes to the owner.
- **Commits:** never commit or push without the owner's go-ahead.
- **Gates:** stop at every gate with a report covering:
  - what was built;
  - what was verified;
  - what could not be;
  - the decisions needed;
  - every place where evidence overrode this spec.

---

## Appendix A: Source starting points

These sources were verified on 2026-10-04 for existence and bibliographic data (arXiv API or
Crossref), and their abstracts were read; details are in `research-log.md`. **Content claims
beyond the abstract must still be read in the paper before use**, except the two marked ✓,
whose specific passages were read.

**Scaling and the long tail:**

- Hestness et al. 2017 (arXiv 1712.00409)
- Kaplan et al. 2020 (2001.08361)
- Rosenfeld et al. 2019 (1909.12673)
- Hoffmann et al. 2022 (2203.15556)
- Bahri et al. 2021 (2102.06701)
- Muennighoff et al. 2023 (2305.16264)
- Hutter 2021 (2102.04074) ✓ (error formula and Zipf exponent)
- Michaud et al. 2023 (2303.13506)
- Feldman 2019 (1906.05271)
- Kandpal et al. 2022 (2211.08411)
- Viering & Loog 2021 (2103.10948)

**Selection:**

- Sorscher et al. 2022 (2206.14486) ✓ (easy/hard crossover; teacher–student perceptron)
- Paul et al. 2021 (2107.07075)
- Toneva et al. 2018 (1812.05159)
- Coleman et al. 2019 (1906.11829)
- Mindermann et al. 2022 (2206.07137)
- Xie et al. 2023, DoReMi (2305.10429)
- Albalak et al. 2024 survey (2402.16827)
- Lee et al. 2021, deduplication (2107.06499)
- Gadre et al. 2023, DataComp (2304.14108)
- Penedo et al. 2024, FineWeb (2406.17557)
- Shumailov et al. 2023 (2305.17493)

**Augmentation and imbalance:**

- Zhang et al. 2017, mixup (1710.09412)
- Cubuk et al. 2019, RandAugment (1909.13719)
- Park et al. 2019, SpecAugment (1904.08779)
- Shorten & Khoshgoftaar 2019 (doi:10.1186/s40537-019-0197-0)
- Chawla et al., SMOTE (JAIR; arXiv 1106.1813; confirm the journal year)
- King & Zeng 2001 (doi:10.1093/oxfordjournals.pan.a004868)
- Saerens et al. 2002 (doi:10.1162/089976602753284446)

**Labels, shift, documentation:**

- Northcutt et al. 2019, confident learning (1911.00068)
- Moreno-Torres et al. 2012 (doi:10.1016/j.patcog.2011.06.019)
- Recht et al. 2019 (1902.10811)
- Gebru et al. 2018, datasheets (1803.09010)

**Transforms and missing data:**

- Box & Cox 1964 (doi:10.1111/j.2517-6161.1964.tb00553.x)
- Yeo & Johnson 2000 (doi:10.1093/biomet/87.4.954)
- Duan 1983 (doi:10.1080/01621459.1983.10478017)
- Rubin 1976 (doi:10.1093/biomet/63.3.581)
- van Buuren & Groothuis-Oudshoorn 2011 (doi:10.18637/jss.v045.i03)
- Kaufman et al. 2012, leakage (doi:10.1145/2382577.2382579)

**Library documentation:**

- scikit-learn, Preprocessing data (https://scikit-learn.org/stable/modules/preprocessing.html):
  the transformer list and the stated caveats (outliers and RobustScaler; Box-Cox requires
  strictly positive data; the quantile transform distorts distances).

**Found in Phase 0** (bibliographic data verified; content depth in `research-log.md`):
Dohmatob et al. 2024 (2402.07043); Cabannes et al. 2023 (2310.02984); Sharma & Kaplan 2020
(2004.10802); Ayed & Hayou 2023 (2302.06960); Goyal et al. 2024 (2404.07177); Gerstgrasser
et al. 2024 (2404.01413); Shumailov et al. 2024, *Nature* (doi:10.1038/s41586-024-07566-y),
and its 2025 author correction; SMOTE is JAIR 2002 (doi:10.1613/jair.953); Settles 2012,
*Active Learning* (doi:10.1007/978-3-031-01560-1); Kuhn & Johnson 2019, *Feature Engineering
and Selection* (doi:10.1201/9781315108230).

**Was to find in Phase 0:**

- an active-learning reference (for example a survey);
- a feature-engineering reference;
- the best current evidence on synthetic data in training.

## Appendix B: Glossary of this spec's terms

- **Lever:** one of representation, sampling distribution q, weights w, labels (§2.1).
- **Data card:** the per-technique record of §2.2.
- **p / q:** the target distribution / the training (sampling) distribution.
- **Signature figure:** the figure the thesis rests on (§9), made before any chapter.
- **Fresh-agent audit:** `learning-repo-audit` run in a new session without drafting context.
- **⚑ / ⛳:** an owner decision / a gate.
