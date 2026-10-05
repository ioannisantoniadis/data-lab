# Research log

Every source consulted, what was checked, and what could not be verified. Add an entry
whenever a source is used.

**Depth levels:**

- **bib:** existence and bibliographic data confirmed (arXiv API or Crossref).
- **abstract:** the abstract was read.
- **passage:** the specific passage relied on was read in the paper.

Content beyond the recorded depth must be read before it is used in the book.

## 2026-10-04: spec drafting

### Sibling repos (local)

- **Size:** prose word counts of `docs/**/*.qmd`:
  - `optimization-lab` ≈ 15.2k;
  - `math-conceptual-map` ≈ 27.6k;
  - `loss-functions-lab` ≈ 28.9k;
  - `rl-for-llms` ≈ 37.0k.

  These set the size cap in SPEC §1.
- **Overlap:** a grep for data topics (scaling law, Chinchilla, augmentation, log transform,
  imbalance, data selection or pruning, deduplication, leakage, label noise, covariate shift,
  active learning, data mixtures) found:
  - mentions only in `modern-ai-systems-and-methods` (leakage, drift, active learning);
  - mentions in `loss-functions-lab` (augmentation inside contrastive objectives; imbalance
    and label noise as loss-design examples);
  - no treatment of transforms, missing-data mechanisms, data selection or scaling laws.

### Passages read

| Source | Depth | What was verified |
|---|---|---|
| Hutter 2021, *Learning Curve Theory*, arXiv 2102.04074 | passage | Toy model: features i drawn i.i.d. with probabilities θ_i, deterministic labels, a memorizing learner. Expected error E_n = Σ_i θ_i (1 − θ_i)^n (eq. 2). For Zipf data, θ_i ∝ i^−(α+1), E_n ≈ n^−β with β = α/(1+α). Finite support gives exponential decay; most distributions give power laws, but with "uninteresting" β = 1. |
| Sorscher et al. 2022, *Beyond neural scaling laws*, arXiv 2206.14486 | passage | Analytic theory in the teacher–student perceptron setting, pruning by teacher margin (large margin = easy). The optimal strategy depends on initial data: with abundant (scarce) data, retain only hard (easy) examples. Exponential scaling in pruned dataset size is possible with an increasing Pareto-optimal pruning fraction. Empirical results on CIFAR-10, SVHN and ImageNet; a benchmark of ten pruning metrics; a self-supervised metric. |

### Abstracts read (arXiv API, 2026-10-04)

| arXiv | Paper | Abstract-level content noted |
|---|---|---|
| 1712.00409 | Hestness et al. 2017, *Deep Learning Scaling is Predictable, Empirically* | Large-scale empirical characterization of generalization error vs. training set size |
| 2001.08361 | Kaplan et al. 2020, *Scaling Laws for Neural Language Models* | Loss is a power law in model size, data and compute over more than seven orders of magnitude; compute-optimal allocation |
| 1909.12673 | Rosenfeld et al. 2019, *A Constructive Prediction of the Generalization Error Across Scales* | A functional form approximating error across model and data scales |
| 2203.15556 | Hoffmann et al. 2022, *Training Compute-Optimal Large Language Models* | Over 400 models; for compute-optimal training, scale model size and tokens equally |
| 2102.06701 | Bahri et al. 2021, *Explaining Neural Scaling Laws* | Variance-limited and resolution-limited regimes, for data and model size (four regimes) |
| 2305.16264 | Muennighoff et al. 2023, *Scaling Data-Constrained Language Models* | Up to 4 epochs of repeated data gives negligible change in loss vs. unique data; value decays with more repetition |
| 2303.13506 | Michaud et al. 2023, *The Quantization Model of Neural Scaling* | Skills as quanta learned in order of use frequency; a power law in frequencies explains power-law loss; tentative LLM evidence |
| 1906.05271 | Feldman 2019, *Does Learning Require Memorization? A Short Tale about a Long Tail* | Memorization is necessary for near-optimal generalization when subpopulation frequencies are long-tailed |
| 2211.08411 | Kandpal et al. 2022, *Large Language Models Struggle to Learn Long-Tail Knowledge* | QA accuracy relates to the number of relevant pretraining documents; retrieval reduces the dependence |
| 2103.10948 | Viering & Loog 2021, *The Shape of Learning Curves: a Review* | Definition, estimation, shapes of learning curves |
| 2107.07075 | Paul et al. 2021, *Deep Learning on a Data Diet* | GraNd and EL2N scores identify important examples early |
| 1812.05159 | Toneva et al. 2018, *An Empirical Study of Example Forgetting* | Forgetting events; some examples never forgotten |
| 1906.11829 | Coleman et al. 2019, *Selection via Proxy* | Small proxy models for data selection |
| 2206.07137 | Mindermann et al. 2022, *Prioritized Training on Points that are Learnable, Worth Learning, and Not Yet Learnt* | RHO-LOSS; high-loss points are often noisy |
| 2305.10429 | Xie et al. 2023, *DoReMi* | Domain weights from a small proxy trained with Group DRO, transferred to a larger model |
| 2402.16827 | Albalak et al. 2024, *A Survey on Data Selection for Language Models* | Survey |
| 2107.06499 | Lee et al. 2021, *Deduplicating Training Data Makes Language Models Better* | Near-duplicates; less memorized output, fewer training steps, reduced train–test overlap |
| 2304.14108 | Gadre et al. 2023, *DataComp* | A benchmark for dataset filtering (12.8B image–text pool) |
| 2406.17557 | Penedo et al. 2024, *The FineWeb Datasets* | A documented 15T-token web dataset with ablated curation choices |
| 2305.17493 | Shumailov et al. 2023, *The Curse of Recursion* | Training on generated data loses the tails of the original distribution |
| 1710.09412 | Zhang et al. 2017, *mixup* | Training on convex combinations of examples and labels |
| 1909.13719 | Cubuk et al. 2019, *RandAugment* | Augmentation with a reduced search space |
| 1904.08779 | Park et al. 2019, *SpecAugment* | Time warping, frequency masking and time masking on filter-bank features |
| 1106.1813 | Chawla et al., *SMOTE* | Synthetic minority oversampling (JAIR; journal year not confirmed here) |
| 1911.00068 | Northcutt et al. 2019, *Confident Learning* | Estimates the joint of noisy and true labels under class-conditional noise |
| 1902.10811 | Recht et al. 2019, *Do ImageNet Classifiers Generalize to ImageNet?* | New test sets; accuracy drops of 3–15% (CIFAR-10) and 11–14% (ImageNet), attributed to distribution shift, not adaptivity |
| 1803.09010 | Gebru et al. 2018, *Datasheets for Datasets* | Dataset documentation proposal |

### Bibliographic only (Crossref, 2026-10-04)

| DOI | Work |
|---|---|
| 10.1111/j.2517-6161.1964.tb00553.x | Box & Cox 1964, *An Analysis of Transformations*, JRSS-B |
| 10.1093/biomet/87.4.954 | Yeo & Johnson 2000, *A new family of power transformations to improve normality or symmetry*, Biometrika |
| 10.1080/01621459.1983.10478017 | Duan 1983, *Smearing Estimate: A Nonparametric Retransformation Method*, JASA |
| 10.1093/biomet/63.3.581 | Rubin 1976, *Inference and missing data*, Biometrika |
| 10.18637/jss.v045.i03 | van Buuren & Groothuis-Oudshoorn 2011, *mice*, JSS |
| 10.1016/j.patcog.2011.06.019 | Moreno-Torres et al. 2012, *A unifying view on dataset shift in classification*, Pattern Recognition |
| 10.1162/089976602753284446 | Saerens et al. 2002, *Adjusting the Outputs of a Classifier to New a Priori Probabilities*, Neural Computation |
| 10.1145/2382577.2382579 | Kaufman et al. 2012, *Leakage in data mining*, ACM TKDD |
| 10.1093/oxfordjournals.pan.a004868 | King & Zeng 2001, *Logistic Regression in Rare Events Data*, Political Analysis |
| 10.1186/s40537-019-0197-0 | Shorten & Khoshgoftaar 2019, *A survey on Image Data Augmentation for Deep Learning*, J. Big Data |

### Library documentation

| Source | Verified |
|---|---|
| https://scikit-learn.org/stable/modules/preprocessing.html | **Transformers:** StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, QuantileTransformer, PowerTransformer (Yeo-Johnson, Box-Cox), Normalizer, OrdinalEncoder, OneHotEncoder, TargetEncoder, KBinsDiscretizer, Binarizer, PolynomialFeatures, SplineTransformer, FunctionTransformer. **Quoted caveats:** with many outliers, mean/variance scaling "is likely to not work very well", and RobustScaler is the replacement; the quantile transform "distort[s] correlations and distances within and across features"; "Box-Cox can only be applied to strictly positive data". Re-check against the installed version when writing. |

### Derived in the spec, not from a source

- **SPEC §7, coverage-driven selection on Hutter's model:** error Σ_{i>n} θ_i, decaying
  roughly as n^−α under Zipf. This is the spec author's extension. Phase 1 must derive and
  test it, and report if it fails.
- **SPEC §8 claim 4, log-normal retransformation factor exp(σ²/2):** standard log-normal
  algebra. It is to be tested, and checked against Duan 1983 when that paper is read.

## 2026-10-04: Phase 0

### Positioning search (SPEC §4)

Question: does any existing book or course already make all three of the book's candidate
claims? (1) Every technique placed on one lens and tested against exact ground truth.
(2) Classical preprocessing and modern data selection and scaling laws in one argument.
(3) The long-tail account of data requirements made computable.

| Work | URL | Accessed | Depth | What it covers | Claims it makes |
|---|---|---|---|---|---|
| Kuhn & Johnson 2019, *Feature Engineering and Selection* (CRC; Crossref 10.1201/9781315108230) | https://feat.engineering/ (redirect from bookdown.org/max/FES) | 2026-10-04 | table of contents + preface | Encoding categorical predictors, engineering numeric predictors, interactions, missing data, feature selection | None of 1–3: no lens, no scaling laws or selection, no ground-truth testing visible |
| Zheng & Casari, *Feature Engineering for Machine Learning* (O'Reilly; year not verified: Crossref and Open Library lookups failed) | https://oreilly.com/library/view/~/9781491953235 | 2026-10-04 | table of contents via search snippet | Numeric features incl. log and power transforms, text, categorical, images | None of 1–3 |
| MIT IAP *Introduction to Data-Centric AI* (2023, 2024) | https://dcai.csail.mit.edu/ | 2026-10-04 | lecture list and stated approach | Label errors / confident learning, imbalance, outliers, shift, curation, LLM data curation, augmentation (2023), growing/compressing datasets (2023) | Partial 2 (curation alongside classical issues) but "rather than mathematical details"; no transforms, no scaling laws, no lens, no exact ground truth |
| Berkeley CS 294-288 *Data-Centric LLMs* (Fall 2025, Sewon Min) | https://www.sewonmin.com/courses/cs294_288_fa25/ | 2026-10-04 | full schedule | Pretraining curation, synthetic data, scaling laws, post-training data, model collapse | Partial 2 (LLM side only); seminar format; no classical preprocessing, no Hutter/long-tail theory, no testbeds |
| Hardt & Recht, *Patterns, Predictions, and Actions*, ch. 8 *Datasets* | https://mlstory.org/data.html | 2026-10-04 | section headings | Benchmarks, dataset history, test-set reuse, harms, documentation | None of 1–3 |
| Christensen et al. 2024, *Data-Centric Machine Learning with Python* (Packt) | packtpub.com product page | 2026-10-04 | unreachable (HTTP 403); title and blurb only | Data-centric practice | Not assessable; listed as unverified |
| Sarkis 2023, *Training Data for Machine Learning* (O'Reilly) | https://www.oreilly.com/library/view/-/9781492094517 | 2026-10-04 | publisher description only | Annotation, schemas, data operations | Not 1–3 by its description (practice and tooling) |
| Zha et al. 2023, *Data-centric AI: A Survey* (arXiv 2303.10158) | https://arxiv.org/abs/2303.10158 | 2026-10-04 | abstract | Organizes by lifecycle stage (training data development, inference data, maintenance) | Not a lens of the §2 kind; no ground truth |
| Albalak et al. 2024 survey; Viering & Loog 2021 review | (Appendix A) | 2026-10-04 | abstract (logged above) | Data selection for LMs; learning curves | Each covers one part of Part IV |
| Hutter 2021; Dohmatob et al. 2024 | (below) | 2026-10-04 | passage | The long-tail account, computed exactly, including q ≠ p | Claim 3 at research level |

**Result:** no single work makes all three claims. Claims 1 and 2 survive as distinctive for a
book. **Claim 3 does not survive as worded:** Hutter (2021) already makes the long-tail account
computable, and Dohmatob et al. (2024) extend it to a training distribution q ≠ p. The book's
contribution there is pedagogical: an exact reproduction a practitioner can run, connected to the
data levers. Suggested rewording in `review.md`, issue 3. Not found: a search for a 2025–2026
book combining preprocessing with scaling laws (two extended web searches) returned only papers.
Bach, *Learning Theory from First Principles* (MIT Press 2024) shares the subtitle phrase but is
a learning-theory text; it was not examined further.

### Sources read in Phase 0

| Source | URL | Depth | Verified | Notes / discrepancies |
|---|---|---|---|---|
| Hutter 2021, arXiv 2102.04074 | https://arxiv.org/pdf/2102.04074 | passage (full text, §§1, 3) | Eq. 2; Zipf θ_i ∝ i^−(α+1) gives β = α/(1+α), with coefficient c_α = α^(1/(1+α)) Γ(α/(1+α))/(α+1), c_1 = √π/2 ≈ 0.886; finite support gives exponential decay; skewed non-Zipf (e.g. exponential) distributions give "uninteresting" β = 1; error "dominated by samples i′ for which θ_i′ ≈ 1/n"; "we have no indication that our findings transfer" | c_α is derived with the unnormalized θ_i = α·i^−(α+1); tests must match the normalization |
| Dohmatob, Feng, Yang, Charton 2024, *A Tale of Tails*, arXiv 2402.07043 | https://arxiv.org/pdf/2402.07043v2 | passage (§§1–3, Appendix A opening) | Hutter LLM trained on q, tested on p (eq. 9); Thm 2.1: tail cut at k gives E_test ≍ T^−(β−1)/β + k^−(β−1); eq. 6: finite sampling cuts at k ≍ T₀^(1/β); Thm 3.2: mixing clean data gives "grokking"; §3.1: tail data "too deep" is worthless; tail narrowing via temperature | **Not in SPEC.** Their β (p_i ∝ i^−β) is α + 1 in Hutter's notation. Prior art for claim 20 and chapter 13 |
| Sharma & Kaplan 2020, arXiv 2004.10802 | arXiv API | abstract | Scaling exponent ≈ 4/d from regression on a data manifold of intrinsic dimension d (in parameters N) | Counter-account to "data needs are set by the tail" |
| Ayed & Hayou 2023, arXiv 2302.06960 | arXiv API | abstract | Random pruning beats most methods when ≤ 30% is kept; no-free-lunch for score-based pruning | Counter-evidence for selection claims |
| Goyal, Maini, Lipton, Raghunathan 2024, arXiv 2404.07177 | arXiv API | abstract | Data curation "cannot be agnostic of the total compute"; repeated high-quality data loses utility | Counter-evidence; chapter 14 |
| Cabannes, Dohmatob, Bietti 2023, arXiv 2310.02984 | arXiv API | abstract | Scaling laws for associative memories in sample and parameter size | Chapter 13 context |
| Gerstgrasser et al. 2024, arXiv 2404.01413 | arXiv API | abstract | Replacing real data with synthetic tends to collapse; accumulating avoids it | Claim 20 must say it is the replace regime |
| Shumailov et al. 2024, *Nature* (10.1038/s41586-024-07566-y) and Author Correction 2025 (10.1038/s41586-025-08905-3) | Crossref | bib | Published version of arXiv 2305.17493; a correction exists | Cite both; read the correction before use |
| Chawla et al. 2002, SMOTE, JAIR (10.1613/jair.953) | Crossref | bib | **Journal year 2002** (SPEC Appendix A asked to confirm) | — |
| Settles 2012, *Active Learning* (Synthesis Lectures; 10.1007/978-3-031-01560-1) | Crossref | bib | Fills SPEC Appendix A's "active-learning reference" | Content to be read in Phase 3 |
| Kuhn & Johnson 2019 (10.1201/9781315108230) | Crossref + feat.engineering | table of contents | Fills "a feature-engineering reference" | — |
| Sorscher et al. 2022; Bahri et al. 2021; Michaud et al. 2023 | arXiv API | abstract (re-read for the review) | Quoted in `review.md` | — |
| PyPI classifiers page | https://pypi.org/classifiers/ | page | "PyPI will always reject packages with classifiers beginning with `Private ::`" | Used in pyproject.toml |

Still open from SPEC Appendix A: "the best current evidence on synthetic data in training". There
are candidates (Shumailov 2024 and its correction, Dohmatob 2024, Gerstgrasser 2024), but they
have not been read beyond the abstract and Dohmatob's §§1–3. To be done in Phase 3.

### Bibliography

`docs/references.bib` (49 entries) was generated on 2026-10-04 from the arXiv API (titles,
authors, years, ids) and the Crossref REST API (DOI entries). Two Crossref titles had markup
stripped (mice; Saerens et al.). Presence in the bib means **bib** depth only; content depth is
as logged above.

### Sibling repos (read 2026-10-04, none modified)

| Repo | Commit | What was read | Finding |
|---|---|---|---|
| rl-for-llms | 1c4ae17 | CONVENTIONS, CLAUDE, notation appendix, `_theme.py`, `method_data.py`, CI, `_quarto.yml`, a chapter opening | Process reference; palette, theme, records format adopted |
| loss-functions-lab | 82b8b97 | CONVENTIONS, notation appendix, chapter list | ℓ / R / R̂ / 𝓛 conventions adopted; σ is the sigmoid |
| optimization-lab | 816e43f | CLAUDE, chapter list, Foundations conditioning section | **No CONVENTIONS.md, no notation appendix.** Conditioning is shown (GD on diag(1, 100)), but **feature scaling is never connected to it** |
| transformer-atlas | — | MAP.md, grep for tokenizer terms | **No tokenization coverage**; the SPEC pointer has no target |
| objectives-book | — | SPEC §§9–11, §21.1–21.2 | Portability rules adopted (D6) |
| modern-ai-systems-and-methods, math-conceptual-map | — | chapter lists; grep | Leakage and drift in ch. 17 (MLOps), ch. 14; prerequisites in ch. 22 (probability) etc. |

### Discrepancies with the spec

- **§2.1 long-tail sentences** → redundancy vs. tail mass are two mechanisms; the oracle
  coverage selector is still a power law (Hutter §3; scratch computation in `review.md`).
  Resolution: reworded in SPEC v0.2 §2.1 (D7).
- **§4 claim 3** → already done at research level (Hutter 2021; Dohmatob et al. 2024).
  Resolution: reworded in SPEC v0.2 (D7).
- **§3/§4 "tokenizer internals: link transformer-atlas"** → transformer-atlas has none.
  Resolution: SPEC v0.2 §3, §4 (primary sources in chapters 3 and 7).
- **§4 "chapter 5 links optimization-lab's account of why feature scaling changes gradient
  descent"** → that account covers conditioning only, not feature scaling. Resolution: SPEC v0.2
  §4, §6, claim 21.
- **§8 claim 10 writes π_y** → conflicts with SPEC §11 ("π for policies only"). Resolution:
  restated as p(y), q(y) in the notation appendix and test stub.
- **§1 sibling sizes are raw `wc -w`, while the cap is on "prose"** → prose is 10–40% lower.
  Resolution: owner chose prose (D7).
- **§8 "Phase 2 makes them pass"** vs. §15 (Parts III–IV in Phase 3) → stubs skip with their
  chapter's phase.
- **SPEC Appendix A "confirm the journal year" (SMOTE)** → 2002 (Crossref).

## 2026-10-04: Phase 1 (testbeds and the signature figure)

| Source | URL | Depth | Verified | Used for |
|---|---|---|---|---|
| Sorscher et al. 2022, arXiv 2206.14486v6 | https://arxiv.org/pdf/2206.14486v6 | passage (§2.3; App. A.1; App. C, "Perceptron in the teacher-student setting") | x ~ N(0, I_N); teacher uniform on the sphere of radius sqrt(N); y = sign(T.x); keep fraction f of smallest-margin examples along a probe at angle theta; student = max-margin solution (QP via CVXPY in the paper); eps_g = arccos(R)/pi; simulations N = 200, alpha_tot = P/N from 10^0.1 to 10^0.5, 100 draws. "the solution to which SGD converges on separable data" is the paper's wording | T3 |
| SciPy 1.18.1 `scipy.special.zeta` docstring | installed package | doc | two-argument form is the Hurwitz zeta, sum_{k>=0} (k+q)^-x | T2 tail masses |
| NumPy 2.5.3 `Generator.zipf`, `Generator.multinomial` docstrings | installed package | doc | zipf pmf k^-a / zeta(a), k >= 1; multinomial's last category takes the remaining mass | T2 sampling |
| SciPy 1.18.1 `scipy.stats.lognorm` docstring | installed package | doc | Y = exp(X), X ~ N(mu, sigma) is lognorm(s=sigma, scale=exp(mu)) | T1 reference in tests |
| SciPy 1.18.1 `scipy.signal.stft` signature and docstring | installed package | doc | default window is 'hann_periodic' in this version; T5 passes every parameter explicitly | T5 |
| scikit-learn 1.9.1 `load_digits` docstring and package data | installed package | doc | 1,797 8x8 images, 10 classes, a copy of the UCI test set; `sklearn/datasets/data/digits.csv.gz` ships with the package (no download) | T5 |

**Derived in Phase 1, not from a source** (all checked by tests; see docs/appendix-testbeds.qmd):

- Hutter's coefficient for the normalized Zipf p: c = zeta(a+1)^(-1/(a+1)) Gamma(a/(1+a)) / (a+1).
  It is Hutter's eq. 4 applied to theta_i = A i^-(a+1) with A = 1/zeta(a+1), and it matches the
  exact sum to 0.1% at n = 10^6.
- Oracle coverage error: sum_{i>n} p_i, between (n+1)^-a and n^-a over a zeta(a+1) (integral
  comparison). **SPEC §7's extension holds**: rate n^-a against uniform's n^-a/(1+a). It is
  still a power law.
- **New:** a selector that knows nothing about p and labels the top-n features of an
  unlabeled pool of M draws has expected error >= max(oracle_n, E_M). With M proportional to
  n, its exponent is uniform's (measured slopes -0.493 to -0.512 at a = 1, 10 seed sets); with
  M = n^2 = n^(1+a) it reaches the oracle's (slopes -0.990 to -1.008), at about 1.45 times the
  oracle's error.

**A solver problem, found and fixed.** L-BFGS-B alone stopped 2e-5 (relative) short of the
max-margin optimum in the primal reference comparison. An active-set polish now solves the
KKT system exactly (duality gap below 1e-14 over 90 solves at the paper's sizes).

## 2026-10-04 to 2026-10-05: Phase 2 (chapters 1-7)

| Source | URL | Accessed | Depth | Verified | Used in |
|---|---|---|---|---|---|
| Gebru et al. 2018, Datasheets for Datasets, arXiv 1803.09010 | https://arxiv.org/pdf/1803.09010 | 2026-10-04 | passage (§3, sections 3.1-3.7) | Seven sections (motivation, composition, collection process, preprocessing/cleaning/labeling, uses, distribution, maintenance); composition question on whether the dataset is "a sample (not necessarily random) of instances from a larger set" and whether it is representative | ch 1 |
| Çetinkaya-Rundel & Hardin 2024, Introduction to Modern Statistics 2e (OpenIntro, CC BY-SA) | https://openintro-ims.netlify.app/data-design | 2026-10-04 | passage (§2.1.5) | Definitions of simple random, stratified, cluster, multistage and convenience samples; "It is often difficult to discern what sub-population a convenience sample represents." No DOI; bib entry from the book's site | ch 1 |
| Northcutt et al. 2021, Confident Learning, arXiv 1911.00068 | https://arxiv.org/pdf/1911.00068 | 2026-10-04 | passage (§2 Assumptions; §3.1 eqs. 1-2; §3.2 methods 1-5; 4-fold CV) | Class-conditional noise assumption; per-class threshold t_j = mean self-confidence; confident joint; CL method 2 = off-diagonals | ch 2 |
| Piantadosi 2014, Psychonomic Bulletin & Review 21(5) (10.3758/s13423-014-0585-6) | https://pmc.ncbi.nlm.nih.gov/articles/PMC4176592/ | 2026-10-04 | abstract + two passages | Word frequency "approximately follows a simple mathematical form known as Zipf's law"; "considerable structure ... beyond the fit of the Zipf-Mandelbrot equation" | ch 3 |
| Kaufman, Rosset, Perlich 2011/2012, Leakage in data mining | https://www.cs.umb.edu/~ding/history/470_670_fall_2011/papers/cs670_Tran_PreferredPaper_LeakingInDataMining.pdf | 2026-10-04 | passage (abstract; §3.1-3.3) | Definition of leakage ("information about the data mining target, which should not be legitimately available to mine from"); leaking features (§3.2) vs leakage in training examples (§3.3); "no-time-machine requirement"; learn-predict separation. **Version read: the KDD 2011 conference paper; the bibliography cites the 2012 TKDD article (10.1145/2382577.2382579), not read.** | ch 3, 4 |
| van Buuren 2018, Flexible Imputation of Missing Data 2e (10.1201/9780429492259) | https://stefvanbuuren.name/fimd/ (§1.2, §1.3) | 2026-10-04 | passage | MCAR/MAR/MNAR definitions (after Rubin 1976); listwise deletion unbiased under MCAR; mean imputation underestimates the variance and biases the mean when not MCAR; regression imputation: weights unbiased under MAR, correlations biased upward, variability understated. **Rubin 1976 itself not read (paywalled).** | ch 4 |
| scikit-learn 1.9 user guide, Common pitfalls §12.2 | https://scikit-learn.org/stable/common_pitfalls.html | 2026-10-04 | page | Definition of leakage; "never call fit on the test data"; feature-selection example (0.76 leaky vs 0.5); the risk is "relevant with almost all transformations ... including StandardScaler, SimpleImputer, and PCA" | ch 4 |
| Duan 1983, Smearing estimate (JASA, 10.1080/01621459.1983.10478017) | OpenAlex abstract | 2026-10-05 | abstract only | "nonparametric estimate of the expected response on the untransformed scale after fitting a linear regression model on a transformed scale". **Full text not accessible; the smearing formula is derived in the book (and in src/data_lab/transforms.py) from first principles, and tested; the chapter says so.** | ch 6 |
| Micci-Barreca 2001, SIGKDD Explorations 3(1) (10.1145/507533.507538) | Crossref + scikit-learn TargetEncoder docstring | 2026-10-05 | bib + as cited by scikit-learn | scikit-learn's TargetEncoder "mixes the global target mean with the target mean conditioned on the value of the category (see [MIC])" | ch 7 |
| Weinberger et al. 2009, Feature Hashing, arXiv 0902.2206 | arXiv API | 2026-10-05 | abstract | Hashing for dimensionality reduction; tail bounds | ch 7 |
| Installed library docstrings (scikit-learn 1.9.1, SciPy 1.18.1) | installed packages | 2026-10-04/05 | doc | train_test_split stratify; LogisticRegression (L2, C=1.0 default; C=np.inf unpenalized; `penalty` deprecated in 1.8); cross_val_predict; KFold (shuffle=False default); TimeSeriesSplit; StandardScaler (ddof=0), MinMaxScaler, MaxAbsScaler, RobustScaler (quantile_range=(25, 75)); SimpleImputer (strategy="mean", add_indicator); scipy.stats.boxcox / boxcox_llf / yeojohnson formulas; PowerTransformer (method="yeo-johnson", standardize=True); QuantileTransformer (n_quantiles=1000, uniform, clips beyond the fitted range); TargetEncoder (cv=5 cross fitting in fit_transform; smooth="auto"; unseen levels -> target mean); FeatureHasher (signed 32-bit MurmurHash3); TfidfTransformer formula (smooth_idf) and TfidfVectorizer token_pattern | ch 1-7 |

### Library behavior checked by test rather than recalled

- scikit-learn decision trees place each threshold at the midpoint of the two adjacent values
  among the samples in the node (in float32): `tests/test_invariance.py::test_tree_thresholds_are_midpoints_within_each_node`.

### Discrepancies with the spec found in Phase 2

- **Claim 2 (tree invariance)** → true on the training points, but not exactly on new points
  under nonlinear monotone transforms, because thresholds sit at midpoints (measured: up to 0.16%
  of new points change). Resolution: claim restated in the test and chapter 5; proposed for
  SPEC at Gate 2.
- **Claim 9 (scaler or imputer fit on train + test is optimistic)** → not supported: on i.i.d.
  data, unsupervised steps change test accuracy by under 0.4 points on average and not
  consistently upward; the large optimism comes from supervised steps (feature selection fit
  before CV: 0.825 vs 0.513 on pure noise). scikit-learn's own page lists StandardScaler and
  SimpleImputer as risks; the book keeps the rule and reports the sizes. Resolution: claim
  restated in the test and chapter 4; proposed for SPEC at Gate 2.
- **Smearing (part of claim 4's card)** → works with constant noise but also has a second
  failure beyond bias under heteroscedastic noise: the factor itself is unstable (coefficient
  of variation 0.72 across seeds). New claim 31.

## 2026-10-05: Phase 3 (chapters 8-14)

Depth as in the rest of this log: *passage* = the PDF opened and the cited section read;
*abstract* = the arXiv or publisher abstract only; *bib* = metadata only. Every number the
book quotes from a source is from the depth stated here.

### Sources read in Phase 3

| Source | Where read | Depth | What was checked | Used in |
|---|---|---|---|---|
| Saerens, Latinne, Decaestecker 2002 | ULB repository PDF | passage (§2.2, eqs. 4 and 9) | Prior-shift correction of posteriors (eq. 4); EM for new priors (eq. 9) | Ch. 8, `prior_shift_correct`, `em_prior` |
| King and Zeng 2001 | PDF | passage (eq. 7) | Prior correction of the logistic intercept | Ch. 8 |
| Chawla et al. 2002, SMOTE | JAIR PDF | passage (§4.2) | Interpolation between a minority point and one of its k minority neighbors | Ch. 8; the gap-filling failure is this book's measurement, and occurs only when k exceeds the cluster size |
| Zhang et al. 2017, mixup (1710.09412) | arXiv PDF | passage (§2) | Convex combination of inputs and one-hot labels, λ ~ Beta(α, α) | Ch. 9 |
| Park et al. 2019, SpecAugment (1904.08779) | arXiv PDF | passage (§2) | Time warping, frequency and time masking | Ch. 9 |
| Cubuk et al. 2019, RandAugment (1909.13719) | arXiv PDF | passage (Figure 2) | Two parameters N and M | Ch. 9 |
| Moreno-Torres et al. 2012 | reprinted in Moreno-Torres's 2013 thesis (digibug.ugr.es); the journal PDF was not reachable | passage (Definitions 1-4) | Covariate, prior-probability and concept shift definitions | Ch. 10 |
| Recht et al. 2019 (1902.10811) | arXiv PDF | abstract and §1 | Accuracy drops of 3-15% (CIFAR-10) and 11-14% (ImageNet) | Ch. 10 |
| Lopez-Paz and Oquab 2016 (1610.06545) | arXiv API | abstract | Classifier two-sample tests | Ch. 10 |
| Viering and Loog 2021 (2103.10948) | arXiv PDF | passage (§§2, 2.2, 4.1) | Learning-curve shapes, power-law and other fits | Ch. 11 |
| Hestness et al. 2017 (1712.00409) | arXiv PDF | passage (§1) | "settles between −0.07 and −0.35" | Ch. 12 |
| Kaplan et al. 2020 (2001.08361) | arXiv PDF | passage (§1, eqs. 1.1-1.2) | α_D ≈ 0.095, α_N ≈ 0.076, N ∝ C^0.73 | Ch. 12 |
| Hoffmann et al. 2022 (2203.15556) | arXiv PDF | passage (abstract, §3.3, Table 2, Appendix D.2) | Exponents 0.50/0.49/0.46; E = 1.69, α = 0.34, β = 0.28 | Ch. 12 |
| Besiroglu et al. 2024 | arXiv API | abstract | Third-method estimates inconsistent, intervals implausibly narrow | Ch. 12 |
| Muennighoff et al. 2023 (2305.16264) | arXiv PDF | passage (abstract, §6) | Up to 4 epochs negligible; half-life about 16 epochs | Ch. 12 |
| Rosenfeld et al. 2019 | arXiv API | abstract | A joint functional form | Ch. 12 |
| Michaud et al. 2023 (2303.13506) | arXiv PDF | passage (§2, eqs. 1-2, data and single-epoch scaling) | Eq. 2 = a + (b−a) n^−α / (α ζ(α+1)); multi-epoch threshold τ gives D^−α/(α+1); single-epoch, n quanta need about T n^(α+1) steps, giving S^−α/(α+1) | Ch. 13 (the chapter 13 review asked for passage depth) |
| Hutter 2021 (2102.04074) | arXiv PDF | passage (§1, re-read 2026-10-05) | "no indication that our findings transfer" refers to the other modeling routes (models scaled with data; non-parametric models), not to real data in general; the chapter now says so | Ch. 13 |
| Dohmatob et al. 2024 (2402.07043v2) | arXiv PDF | passage (§§1-3) | Eq. 6 and Cor. 2.2: a finite sample of T_0 draws cuts the tail near probability 1/T_0, the bound behind the pool selector; Thm 2.1: the resulting plateau | Ch. 13 (pool bound credited), Ch. 14 |
| Maloney, Roberts, Sully 2022 (2210.16859) | arXiv API | abstract | Spectral power laws in data become power laws in loss in a solvable random-feature model; the spectrum's finite extent gives a plateau | Ch. 13, competing account |
| Cagnetta, Raventós, Ganguli, Wyart 2026 (2602.07488v3) | arXiv API | abstract | Data-limited exponents predicted without free parameters from the decay of token correlations and of conditional entropy; matched on TinyStories and WikiText with GPT-2- and LLaMA-style models | Ch. 13, competing account |
| Sorscher et al. 2022 | arXiv PDF (logged in Phase 1) | passage | Abundant (scarce) → keep hard (easy) | Ch. 14, reproduced on T3 |
| Paul et al. 2021 (2107.07075) | arXiv PDF | passage (§2, Definitions 2.1 and 2.3) | GraNd = expected gradient norm; EL2N = expected norm of the error vector, accurate after a few epochs | Ch. 14 |
| Toneva et al. 2018 (1812.05159) | arXiv PDF | abstract | The definition of a forgetting event | Ch. 14 |
| Coleman et al. 2019 | arXiv API | abstract | Selection via small proxy models | Ch. 14 |
| Ayed and Hayou 2023 | arXiv API | abstract | Random pruning beats most methods at high compression | Ch. 14 |
| Lee et al. 2021 (2107.06499) | arXiv PDF | abstract and §1 | Over 1% verbatim output; a 61-word sentence over 60,000 times; ten times less memorized text after dedup | Ch. 14 |
| Settles 2009, *Active Learning Literature Survey* | author's PDF | passage (§3.1) | Uncertainty sampling, binary case: posterior nearest 0.5 | Ch. 14 |
| Mindermann et al. 2022 (2206.07137) | arXiv PDF | abstract and the derivation of the irreducible holdout loss | RHO-LOSS = training loss minus irreducible holdout loss; 18× fewer steps on Clothing-1M | Ch. 14 |
| Xie et al. 2023, DoReMi (2305.10429) | arXiv PDF | abstract | 280M proxy with Group DRO; "2.6x fewer training steps" | Ch. 14 |
| Gadre et al. 2023, DataComp | arXiv API | abstract | 12.8B image-text pool; filtering as the benchmark | Ch. 14 |
| Penedo et al. 2024, FineWeb | arXiv API | abstract | 15T tokens; ablated curation | Ch. 14 |
| Goyal et al. 2024 | arXiv API | abstract | Curation "cannot be agnostic of the total compute" | Ch. 14 |
| Shumailov et al. 2023 / 2024 (Nature) | arXiv PDF / Nature abstract | abstract | Tails lost under recursive training | Ch. 14 |
| Shumailov et al. 2025, author correction | Nature | bib only | **Content not accessible** (Nature login); the chapter says so | Ch. 14 |
| Gerstgrasser et al. 2024 (2404.01413) | arXiv API | abstract | Replace collapses; accumulate avoids it | Ch. 14, reproduced on T2 |

### Derived in Phase 3, not from a source

- **The deduplicated uniform stream on Hutter's model.** Labeling each feature the first time it
  appears costs E[D_m] labels after m draws and leaves error E_m (both exact). From the integral
  approximation behind Hutter's eq. 4: E[D_m] ≈ Γ(β)(Am)^(1/s), so at n labels the error is
  β Γ(β)^(1+α) times the oracle's (π/2 at α = 1; 1.46 at α = 0.5; 1.66 at α = 2), after
  m ≈ (n/Γ(β))^s / A draws. Checked against the exact curve and a simulation
  (`tests/test_long_tail.py`). Not found in Hutter, Dohmatob or Michaud; derived here.

### Discrepancies with the spec found in Phase 3

- **Coverage selection (SPEC §7, claim 16).** The spec and the Phase 1 chapter attribute the
  steeper exponent to choosing the most frequent cases first. The evidence: per label, the
  exponent comes from not labeling repeats, which needs no knowledge of p; frequency order adds
  only a constant (about 1.5). Per draw, nothing beats uniform sampling's exponent. Chapter 13,
  the signature figure's Panel B and the coverage card are revised; SPEC §7/§9 wording is
  proposed at Gate 3.
- **Active learning on noisy labels (claim 18).** A 20-seed pilot suggested that uncertainty
  sampling is worse than random under heavy label noise; at 60 seeds the ratio was 1.07, within
  noise. The claim is restated as "the gain vanishes".
- **Deduplication (claim 17).** "Below the entropy rate" was not a reliable signature on T4;
  restated as optimism of more than 0.3 nats removed by deduplication.
- **SMOTE.** It fills the gap between minority clusters only when k exceeds the cluster size.

## 2026-10-05: Phase 4 (synthesis)

### Sources read in Phase 4

| Source | Where read | Depth | What was checked | Used in |
|---|---|---|---|---|
| `rl-for-llms/docs/chapters/00-map.qmd` (sibling, not modified) | local file | passage (the lens table) | $q$ is the "data regime" and $w$ the "estimator and weight" row; the published page is `chapters/00-map.html` | The Map |
| `objectives-book/SPEC.md` §13 item 10 and DECISIONS D10 (sibling, not modified) | local files | passage | "How this book was made": who did what, and model versions | Front page (D0) |
| This repository's commit trailers | `git log` | full | Every commit names Claude Opus 5.5 | Front page |

### Derived or measured in Phase 4, not from a source

- **The worked examples** (chapter 15, `src/data_lab/worked.py`, claims 44–46). Measured
  mechanisms, checked in tests: mean imputation shrinks the fitted coefficients (0.693 against
  a true 0.8 on the first feature); regression imputation keeps them within 0.01 but its
  smearing factor is 1.422 against a true exp(σ_ε²/2) = 1.377, because the imputed values
  carry no noise. A gain $g$ adds exactly $\log g$ to every bin of `log_power_spectrum` (the log
  of the time-averaged STFT magnitude), so per-recording centering removes it exactly.

### Decisions made in Phase 4

- **Settles 2012 removed** from the bibliography: it was never read beyond its metadata, and
  Further Reading lists only sources read for the book; the 2009 survey, read at passage
  depth, is listed instead.
- **The toy-limits appendix is generated** from each chapter's "What the toy cannot show"
  section by `scripts/technique_data.py`, so it cannot drift from the chapters.

### Sources checked for the final audit's findings

| Source | Where read | Depth | What was checked | Used in |
|---|---|---|---|---|
| Shimodaira 2000, J. Statistical Planning and Inference 90(2):227–244 (10.1016/s0378-3758(00)00115-4) | Crossref; Semantic Scholar and OpenAlex (closed access, abstract elided by the publisher) | bib only | Title, authors, venue. **Content not read**; the chapter 8 Lineage callout claims only what the title states and says so | Ch. 8 (final audit m4) |
| scikit-learn 1.9.1 `TfidfVectorizer` | the installed library | default checked by running it | `token_pattern = '(?u)\b\w\w+\b'`: two or more Unicode word characters, underscore included | Ch. 7 (final audit polish) |
| Lawson and Hanson, *Solving Least Squares Problems* (SIAM 1995, 10.1137/1.9781611971217), via scipy 1.x `nnls` | scipy's docstring (it implements their active-set NNLS) | docstring only | The least-distance-to-NNLS reduction is **not** read from the book; the solver's output is instead certified on every call by the KKT conditions and a zero duality gap, and against a primal SLSQP reference in the tests | T3 (CI exposed the old solver) |
