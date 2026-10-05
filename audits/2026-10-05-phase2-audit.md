# Audit: data-lab, Parts I–II (chapters 1–7, appendices T/Notation): 2026-10-05

**What was audited:** the working tree at HEAD `5d5e27b` plus the uncommitted Phase 2 changes. That is 65 modified or untracked paths, including all seven chapters, eight of the nine figures and the new data cards. The audit copy was made with `cp -R`, as instructed, so the audit covers this uncommitted state and not any commit. `origin/main` is at `c0ee9c8`, two commits behind the local HEAD.

**Profile:** book (Quarto). Figures are pre-generated PNGs made by scripts in `scripts/figures/`, and Quarto executes no code.

**Sample:** 14 source claims opened against primary sources or docs. About 45 quoted numbers were recomputed from fresh runs. All 9 figure scripts were re-run, including the three requested.

**Thesis (one sentence):** every data technique pulls one of four levers (representation, sampling distribution q, weights w, labels), and the book measures what each one does against synthetic testbeds with exact ground truth.

## Verdict

Parts I–II are unusually trustworthy. Every number I recomputed matched a fresh run except three small discrepancies, and none of those changes a conclusion. Every quote I opened is real and says what the book says it says. Eight of nine figures regenerate byte-identically. The research log is honest about what was read at what depth: Duan abstract only, the KDD 2011 version of Kaufman et al., Rubin 1976 not read.

The weaknesses are of two kinds:
- **Scope.** Two boxed or result-level statements are stated more broadly than either the source or the book's own Chapter 1 supports. The main one is "complete-case analysis is unbiased under MCAR only".
- **Reproducibility of one figure.** The encoding figure and its quoted cross-fit numbers are not reproducible, because `TargetEncoder` shuffles its folds unseeded.

There is also a set of consistency and staleness items: undeclared notation, a front page that still says "every chapter is a stub", and tests cited for numbers they do not compute.

**trustworthy with fixes**

## Scores

| Criterion | Score | Note |
|---|---|---|
| 1. Source fidelity | 4 | All 14 sampled sources verified; research log records depth honestly. Imprecisions: CL "four folds" cited to the wrong section and overstated; a QuantileTransformer quote stretched to cover distances; Kaufman section numbers come from the 2011 version while the 2012 article is cited (disclosed in the log, not in the book). |
| 2. Computed evidence | 4 | All 9 scripts run, and 8/9 PNGs regenerate byte-identically. `encoding.png` does not reproduce (unseeded `TargetEncoder` shuffle), and the committed image predates the last script edit. |
| 3. Claims match measurements | 4 | About 45 numbers recomputed and nearly all exact. Exceptions: CL precision 0.33 (measured 0.343); cross-fit coefficient 0.003 (one random draw; I got 0.040, 0.014 and −0.002 on three runs); "0.728 in every one of 10 seeds" (per-seed values are 0.719–0.731); "0.975–1.025" is the test tolerance, not the measurement (0.988–1.008). |
| 4. Correctness | 4 | Derivations re-checked: the noisy-label threshold, the imputation variances 0.6 and 0.744, aliasing, the log-normal shortfall, hash occupancy, the TF-IDF formula. Tests are real numeric checks (54 tolerance assertions; library behavior is tested, not recalled). Two overgeneralized result statements (Findings M1, M2). |
| 5. Pedagogy | 4 | Each chapter follows the template: motivate, assumptions with what breaks, derive, boxed result, failure modes, toy limits, connections. Chapter 2 (foundational) and Chapter 6 (advanced) both let the reader reconstruct the result from the page. Data cards are dense but generated and consistent. |
| 6. Honesty and currency | 4 | Every chapter has "What the toy cannot show". The SPEC's claim 9 was restated when the evidence contradicted it, and the book says so. Versions are dated (scikit-learn 1.9, SciPy 1.18). Evidence-type labels are mostly implicit, which is acceptable for this largely established material. |
| 7. Internal consistency | 3 | New symbols are missing from the notation appendix, against the CONVENTIONS rule. Code uses `w, c` where the book uses $u, u_0$, and $w$ is the book's per-example weight. `index.qmd`, README and CLAUDE.md say "stubs" or "Phase 0". Chapter 5 says T1's features are both log-normal and Gaussian. Several "Checked by" tests run a different configuration from the quoted number. |
| 8. Engineering hygiene | 3 | Locked deps; `uv sync`, `pytest` (106 passed, 8 skipped stubs), `ruff`, word count, portability and `quarto render` are all clean with 0 warnings. But all Phase 2 work is uncommitted, local HEAD is 2 commits ahead of origin, and `gh run list` returns no runs, so CI has never exercised this state. No deploy, by design (D5). |
| 9. Economy | 4 | Chapters run 1,278–1,730 words, are tight and stay in scope. Sibling repos are linked rather than re-derived. Minor: dead axis range in two figure panels. |

**Hard fails:** none.
- No fabricated source: every sampled quote was found verbatim.
- No fabricated result: every figure is computed and every sampled number reproduces.
- No wrong core claim: M1 and M2 are scope overstatements in result statements, not false core derivations.

## What's strong (keep)

- **`research-log.md`** (rows 225–232) records URL, date, depth and caveats for each source. Examples: "Version read: the KDD 2011 conference paper; the bibliography cites the 2012 TKDD article … not read"; "Duan … abstract only". The book's Chapter 6 repeats the Duan caveat in prose (`06-changing-the-shape.qmd:60`). This is exemplary.
- **Library behavior is tested rather than recalled:**
  - `tests/test_invariance.py::test_tree_thresholds_are_midpoints_within_each_node` found the midpoint fine print that the Chapter 5 tree paragraph reports;
  - `test_tfidf_matches_the_documented_formula`;
  - Box–Cox λ recovery.
- **Chapter 4's leakage section** (`04-cleaning.qmd:97–114`) follows the evidence against the SPEC. Unsupervised steps fit on train plus test move accuracy by at most 0.4 points; supervised selection reports 0.825 against a true 0.5. The test docstring records the restatement.
- **Figures are honest computations,** seeded and fast (each runs in 1–9 s). `selection_bias.png`, `leakage.png` and `changing_shape.png` reproduce byte-identically.
- **Chapter 6's smearing failure mode** (`:125–131`) reports both the regional bias and the factor's seed-to-seed instability (2.1–11.1). Both reproduce exactly.

## Findings

### Blockers
None.

### Major

**M1. The result box and data card overstate when complete-case analysis is biased, which contradicts Chapter 1 and van Buuren.**
- *Where:* `docs/chapters/04-cleaning.qmd:59`: "Complete-case analysis is unbiased under MCAR only."
- *Where:* the card `docs/includes/cards/complete-case.md` (generated from `scripts/technique_data.py`) says that under MAR or MNAR "means and fitted relationships shift".
- *Evidence, Chapter 1:* the book's own result (`01-…qmd:49–54`, tested) is that selection depending on $x$ alone leaves $p(y\mid x)$ and the regression intact. Chapter 4's Connections (`:174–175`) even says "the selection-on-$x$ versus selection-on-$y$ result applies".
- *Evidence, van Buuren §1.3.1:* "complete-case analysis is not always bad. The implications of the missing data are different depending on where they occur (outcomes or predictors)…", and "listwise deletion is unbiased under two special MNAR scenarios (cf. Section 2.7)".
- *Fix:* scope the box to the estimand that was measured: "the complete-case *mean* is unbiased under MCAR only; regression coefficients survive missingness that depends only on the predictors (Chapter 1)". Mirror this in the card's record.

**M2. The encoding figure and its quoted cross-fit numbers are not reproducible.**
- *Where:* `src/data_lab/transforms.py:83` uses `TargetEncoder()`. In scikit-learn 1.9.1 that means `shuffle=True` (deprecated, but still the effective default) and `random_state=None`. Source: `_target_encoder.py:129–146, 349`.
- *Evidence:* three runs of `target_encoding_experiment()` gave cross-fit means (0.746, 0.751, coefficient 0.040), (0.747, 0.751, 0.014) and (0.748, 0.751, −0.002).
- *What is affected:*
  - the prose at `07-…qmd:67–68` says "0.747 and 0.751, with a coefficient of 0.003";
  - the regenerated `docs/images/encoding.png` differs from the committed one in panel A's cross-fit points (0.27% of pixels);
  - the committed PNG (00:38:56) is also older than the last edit to `fig_encoding.py` (00:39:11).
- *Not affected:* the conclusion, since leakage is removed in every run.
- *Fix:* pass `cv=KFold(5, shuffle=True, random_state=s)`, which is also the non-deprecated API. Then regenerate the figure and re-quote the numbers.

**M3. Chapter 1's result box says selection on $y$ cannot be undone by any amount of data, without the "unless $s$ is known" caveat.**
- *Where:* `01-…qmd:52–53`: "no amount of data from $q$ recovers it".
- *Evidence:* when $s(x,y)$ is known and positive, weighting by $1/s$ recovers $p$. The chapter itself notes "T1 knows $s(x, y)$ exactly" (`:143`), and the same reasoning appears for selection on $x$ (`:58`).
- *Fix:* "…recovers it unless the selection probability $s(x, y)$ is known".

### Minor

**m1. Measured numbers in prose that drift from a fresh run.**
- `02-labels.qmd:108–109`: precision "0.33" at Bayes risk 0.35. The figure script gives 0.343 ± 0.014.
- `06-…qmd:51–52`: "averaged 0.728 … in every one of 10 seeds". Per-seed values are 0.719–0.731, with a mean of 0.726.
- `06-…qmd:61`: "between 0.975 and 1.025 of the true mean in every seed". That is the test tolerance (`test_transforms.py:37`); the measured range is 0.988–1.008.

**m2. "Checked by" tests that run a different configuration from the quoted number.**
- `05-affine-scaling.qmd:60–63`: the accuracy "0.729 to 0.563" uses a scale of 300, from the figure script. The cited `test_knn_prediction_flips_under_feature_rescaling` uses a scale of 100 and asserts only a gap above 0.05.
- `05-…qmd:68–72`: the condition numbers 1.4×10⁸ and 2.4 use scales (1, 1, 10⁴), from `fig_affine_scaling.py`. The cited test uses (1, 100, 0.01) with an offset of 50.
- `02-labels.qmd:59`: "within 0.25 of the predicted point" is in logit-score units in the test (`test_labels.py:47`). The prose then gives the point as $\eta = 0.67$, so a reader will read 0.25 on the probability scale.
- I re-ran all of the quoted numbers and they reproduce. The problem is the traceability that CONVENTIONS promises.

**m3. Notation not declared.**
- CONVENTIONS ("Use only symbols in `docs/appendix-notation.qmd`; a new symbol is added there in the same change") is violated by $\eta$, $\tilde y$, $\rho_0$, $\rho_1$, $t_j$ (Chapter 2), $s(x,y)$, $W_h$, $S_h$ (Chapter 1), $m(x)$, $\hat\varepsilon$ (Chapter 6) and $r$ (Chapter 4). `git diff` shows `appendix-notation.qmd` unchanged in Phase 2.
- Separately, `src/data_lab/testbeds/t1_tabular.py` names the classification coefficients `w`, `c`, and its docstring says "sigmoid(w . z + c)". The book uses $u, u_0$ and reserves $w$ for per-example weights.

**m4. Stale status text that readers see.**
- `docs/index.qmd:4`: "This book is in Phase 0 (foundation). Every chapter is a stub; nothing here is yet a claim." This renders on the book's front page above seven written chapters.
- `README.md:17, 48–50` says "Chapters are stubs", "stubs until Phase 1" and "20 claim stubs".
- `CLAUDE.md:34` says "stubs until Phase 1".

**m5. Chapter 5 describes T1's features two ways.** Line 50 says "T1's log-normal features" (the skewness test uses `skewed=True`), while line 129 says "T1's features are Gaussian" (the kNN, conditioning and outlier demonstrations). Say which variant each demonstration uses.

**m6. Source-location and quote imprecisions.**
- `02-labels.qmd:84–85`: "The paper fixes four folds [§3.2]". Northcutt et al.'s four-fold statement is in §5 ("Unless otherwise specified, we compute out-of-sample predicted probabilities … using four-fold cross-validation"). §5.2 uses 5-fold for Amazon Reviews.
- `06-…qmd:99–100`: "warns of exactly this: the transform 'may distort linear correlations between variables'". The docstring continues "…measured at the same scale but renders variables measured at different scales more directly comparable". It is about cross-variable correlation, not pairwise distances.
- `03-…qmd:84–86` and `04-…qmd:89–92` cite Kaufman §3.2–3.3. Those section numbers come from the KDD 2011 paper that was read; the bibliography cites the 2012 TKDD article. Note the version in the bib or in the text.

**m7. Hygiene.** All Phase 2 work (65 paths, including 8 figures and 19 cards) is uncommitted. Local HEAD is 2 commits ahead of `origin/main`. There are no CI runs (`gh run list` is empty), so CI's "generated includes are current" and lint/test gates have never run on this content. Note also that `git diff --exit-code docs/includes` in `ci.yml` ignores untracked files.

### Polish
1. `leakage.png` panel A has an x-axis to 0.8 with data ending at 0.5. `changing_shape.png` bottom right has an x-axis to 3.5 with data ending at 1.75.
2. `01-…qmd:121`: "miscalibrated everywhere". The fitted line crosses the truth near $z_1 \approx -2.5$ in panel A.
3. `07-…qmd:112–113`: "two or more alphanumeric characters". The pattern `\w\w+` also matches underscores and Unicode word characters.
4. Chapter 3's raw-waveform argument (`:76–77`): symmetry rules out linear *separation*, not an above-chance threshold when the class variances differ. The "does little better than guessing" hedge covers it.
5. 37 bibliography entries are not yet cited (for Parts III–IV). This is expected at this phase.

## Mechanical checks

- **Images:** 9 referenced, 9 with a generating script, 0 missing, 0 orphan.
- **Citations:** 0 undefined keys. 37 bib entries uncited (future chapters). 0 non-book entries without an identifier.
- **Online identifiers:** 35 arXiv ids and 18 DOIs checked; 0 not found; 0 title mismatches.
- **Links:** 0 dangling paths in project docs; 0 broken internal links.
- **Tests:** 82 test functions in 22 files at collection (106 passed, 8 skipped Phase 3 stubs, in 41.6 s); 54 numeric-tolerance assertions.
- **Lint and scripts:** `ruff check .` reports all checks passed. `word_count.py` gives 12,488 prose words (cap 35,000). `check_portability.py` passes.
- **Generated includes:** `technique_data.py` regenerates 19 cards and the decision guide byte-identically to the working tree.
- **Render:** `quarto render docs` finishes with 0 warnings and no unresolved cross-references. Rendered titles number chapters 1–7 correctly; The Map is unnumbered.
- **CI and site:** CI has no runs on record. No live site, by design (D5).
- **Dependency drift:** none from a fresh `uv sync` (scikit-learn 1.9.1, SciPy 1.18.1).

<details><summary>Mechanical-check script output (abridged)</summary>

```
- Profile (guess): book
- Images referenced: 9; with a generating script: 9
- Bibliography entries: 54
- Lockfile: uv.lock; CI workflows: .github/workflows/ci.yml, .github/workflows/docs.yml
- Tests: 82 functions in 22 files; 54 numeric-tolerance assertions
Missing images (0) · Orphan images (0) · Unscripted images (0)
Citation keys with no bib entry (0) · Bib entries never cited (37) · No DOI/URL (0)
Dangling paths (0) · Broken internal links (0)
arXiv ids checked: 35; DOIs checked: 18; not found 0; unresolved 0; title mismatches 0
```
</details>

## Claims checked

| # | Claim (location) | Source opened | Verdict | What the source says |
|---|---|---|---|---|
| 1 | Convenience sample: "it is often difficult to discern what sub-population a convenience sample represents" (`01:90–91`, IMS §2.1.5) | openintro-ims.netlify.app/data-design | ok | Verbatim, in §2.1.5 "Four sampling methods". |
| 2 | Datasheets ask whether the dataset is "a sample (not necessarily random) of instances from a larger set" (`01:136–138`, §3.2) | arXiv 1803.09010 PDF | ok | §3.2 "Composition", verbatim. |
| 3 | CL: class-conditional assumption (§2); threshold $t_j$ = average self-confidence; "CL method 2" = off-diagonals of the confident joint (`02:21–23, 70–76`) | arXiv 1911.00068v6 PDF | ok | "CL method 2: Cỹ,y∗. Estimate label errors as {x ∈ X̂ỹ=i,y∗=j : i ≠ j}"; "expected (average) self-confidence for class j used as a threshold". |
| 4 | "The paper fixes four folds [§3.2]" (`02:84–85`) | same | imprecise | Four-fold CV is stated in §5 "unless otherwise specified"; 5-fold is used for Amazon Reviews. |
| 5 | Piantadosi: "approximately [follow] … Zipf's law"; "considerable structure" (`03:43–45`) | PMC4176592 | ok | "approximately follows a simple mathematical form known as Zipf's law"; "considerable structure … beyond the fit of the Zipf–Mandelbrot equation". |
| 6 | Kaufman et al.: leakage definition; "no-time-machine requirement"; leaking features vs. training examples §3.2–3.3 (`03:84–88`, `04:89–92`) | KDD 2011 PDF (cs.umb.edu) | ok (version caveat) | All verbatim; §3.2 "Leaking Features", §3.3 "Leakage in Training Examples". This is the 2011 version; the 2012 TKDD article is cited. |
| 7 | `scipy.signal.stft` default window `'hann_periodic'` in SciPy 1.18; `TimeSeriesSplit` quote; `KFold` shuffle default (`03:112–115`) | installed SciPy 1.18.1 / sklearn 1.9.1 signatures and docstrings | ok | `window='hann_periodic'`; "returns the first k folds as the train set and the (k+1)-th fold as the test set"; `shuffle=False`. |
| 8 | van Buuren's MCAR/MAR definitions (§1.2) and listwise deletion, mean-imputation and regression-imputation quotes (§1.3) (`04:19–22, 65–69`) | stefvanbuuren.name/fimd §1.2, §1.3 | ok as quotes | All verbatim. But §1.3.1 also says "complete-case analysis is not always bad…" and "listwise deletion is unbiased under two special MNAR scenarios", which bears on the book's own box (M1). |
| 9 | scikit-learn *Common pitfalls* §12.2: "almost all transformations … StandardScaler, SimpleImputer, and PCA" (`04:92–95`) | scikit-learn.org/stable/common_pitfalls.html (1.9.1) | ok | §12.2.2: "This risk of leakage is however relevant with almost all transformations in scikit-learn, including (but not limited to) StandardScaler, SimpleImputer, and PCA." |
| 10 | Scaler table: StandardScaler `ddof=0`; RobustScaler `quantile_range=(25,75)`; MinMax `feature_range=(0,1)`, `clip` (`05:31–38, 99–101`) | installed docstrings and signatures | ok | "equivalent to `numpy.std(x, ddof=0)`"; defaults as stated. |
| 11 | Duan: "a nonparametric estimate of the expected response on the untransformed scale after fitting a linear regression model on a transformed scale" (`06:58–60`) | OpenAlex abstract, DOI 10.1080/01621459.1983.10478017 | ok | Verbatim. The book correctly says only the abstract was read. |
| 12 | Yeo–Johnson: Box–Cox of $x+1$ for $x \ge 0$, exponent $2-\lambda$ for negatives; Box–Cox needs $y>0$; PowerTransformer and QuantileTransformer defaults (`06:27–28, 83–88, 105–109`) | SciPy `yeojohnson` docstring; sklearn docstrings and signatures | ok | All as stated ("Box-Cox requires input data to be strictly positive"). |
| 13 | QuantileTransformer "may distort linear correlations between variables" as a warning about distances (`06:99–100`) | sklearn docstring | imprecise | The sentence continues "…measured at the same scale but renders variables measured at different scales more directly comparable". It is about cross-variable correlation. |
| 14 | TargetEncoder follows Micci-Barreca; `fit_transform` cross-fits with `cv=5`; `fit(X,y).transform(X)` "does not equal" it; TF-IDF default formula (`07:52–53, 92–96, 109–110`) | sklearn 1.9.1 source and docstrings | ok, with omission | All as stated. Not mentioned: the folds are shuffled unseeded by default (`shuffle=True`, `random_state=None`), which is the cause of M2. |
| 15 | Hutter: "no indication that our findings transfer" (`appendix-testbeds:85–86`) | arXiv 2102.04074 PDF | ok | Verbatim (p. 3). |

**Measured numbers re-run (fresh runs in the copy):**
- **Chapter 1:** slopes 0.802/0.801/0.670 and 9.0 SD; means 0.999/1.449/0.328; stratified ratio 0.605 vs predicted 0.591. All match.
- **Chapter 2:** threshold 0.667, risk 0.278, Bayes risk 0.251 (match); CL precision 0.999→0.343 (prose says 0.33); recall 0.565–0.68.
- **Chapter 3:** raw 0.485–0.528; spectrum 1.00×5; MSE 1.25/59.5/64.3; minimum ratio 14.7; future window 18.6–176.6. All match.
- **Chapter 4:** variances 0.995/0.596/0.740; MAR −0.321/−0.002; MNAR −0.392; duplicates 0.660/0.762/0.830, Bayes 0.749; gaps ≤0.39 points (largest −0.39); supervised selection 0.825/0.513. All match.
- **Chapter 5:** 0.729→0.563; conditioning 1.38×10⁸ and 2.35. Both match.
- **Chapter 6:** naive 0.719–0.731 (prose "0.728 in every seed"); smeared 0.988–1.008; Box–Cox −1.007/−0.504/−0.006/0.495/1.486; distance correlation 0.452, robust across seeds 1–3 (0.40–0.47); heteroscedastic region ratio 2.29–2.44 and factor 2.12–11.11 vs 1.37–1.38.
- **Chapter 7:** R² 0.947/0.008 (ceiling 0.947); hashing 880/1,775; R² 0.142/0.816/0.846 (ceiling 0.851); target encoding none 0.746/0.752, naive 0.854/0.618/7.79. All match. Cross-fit values vary from run to run (M2).

## Figures re-run

| Figure | Script | Reproduces? | Caption accurate? | Note |
|---|---|---|---|---|
| `selection_bias.png` (Chapter 1) | `fig_selection_bias.py` | yes, byte-identical | yes | Panel A's truth line correctly marginalizes $z_2, z_3$ given $z_1$. |
| `leakage.png` (Chapter 4) | `fig_leakage.py` | yes, byte-identical | yes | Panel B's supervised row is the leaky-minus-clean CV accuracy (about 0.31), consistent with 0.825 − 0.513. |
| `changing_shape.png` (Chapter 6) | `fig_changing_shape.py` | yes, byte-identical | yes | — |
| `long_tail_signature.png` (signature) | `fig_long_tail_signature.py` | yes, byte-identical | not re-audited (Phase 1) | — |
| `label_noise.png`, `data_types.png`, `missingness.png`, `affine_scaling.png` | respective scripts | yes, byte-identical | yes | — |
| `encoding.png` (Chapter 7) | `fig_encoding.py` | **no**: 0.27% of pixels differ, in panel A's cross-fit points only | yes qualitatively | Unseeded `TargetEncoder` shuffle (M2); the committed PNG predates the last script edit. |

## Decisions for the author

1. **Complete-case result box (M1).** Options:
   - (a) scope it to the mean;
   - (b) keep it general but add the selection-on-$x$ exception and van Buuren's MNAR special cases;
   - (c) drop the complete-case clause from the box.

   Recommend (a), plus one sentence linking Chapter 1.
2. **Quoted numbers vs. the tests that check them (m1, m2).** Options:
   - (a) make each "Checked by" test assert the exact configuration and number quoted, within a tight tolerance;
   - (b) generate the quoted numbers from the figure scripts into an include, as the data cards already are.

   Recommend (b) for the per-chapter headline numbers. It removes hand-copied numbers, which is where every discrepancy in this audit came from.
3. **Front page and README status (m4).** Update them at this gate, or keep them until Phase 2 is committed. Recommend updating them in the same commit as the chapters, so a reader never sees "every chapter is a stub" above written chapters.
