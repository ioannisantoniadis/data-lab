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
