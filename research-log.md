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
