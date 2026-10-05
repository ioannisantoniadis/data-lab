# Roadmap

Status markers: planned · researching · drafted · done (passes the quality bar) · blocked.

## Phase 0: foundation (2026-10-04): done; ⛳ Gate 0 passed 2026-10-04 (DECISIONS D7)

- [x] Read CLAUDE.md, SPEC.md, DECISIONS.md, research-log.md.
- [x] Read the sibling repos (none modified). rl-for-llms read in full where it serves as the
      process reference (CONVENTIONS, CLAUDE, notation appendix, theme, records, CI, a sample
      chapter); also loss-functions-lab (CONVENTIONS, notation), optimization-lab (CLAUDE,
      chapter list, the conditioning section), objectives-book (§§9–11, §21.1–21.2),
      transformer-atlas (MAP, tokenizer search), modern-ai-systems-and-methods and
      math-conceptual-map (chapter lists). Findings below.
- [x] Positioning search (SPEC §4): 10 books, courses and surveys examined, at the depths logged. Result: no work
      makes all three distinctive claims; claim 3 needs rewording (research-log.md, *Positioning*).
- [x] `skeptical-review` of SPEC §2: [`review.md`](review.md). Verdict: revise. No hard fails;
      a near miss on prior art (Dohmatob et al. 2024).
- [x] Scaffold:
  - docs: README, CLAUDE.md (updated), CONVENTIONS.md, ROADMAP.md, COVERAGE.md (57 items),
    research-log.md (extended);
  - the book: a Quarto skeleton with 16 chapter stubs and 5 appendix stubs (notation filled
    in); `references.bib` with 49 entries generated from the arXiv and Crossref APIs;
  - the `data_lab` package skeleton (uv, Python ≥ 3.11, `uv.lock`, a `Private :: Do Not
    Upload` classifier);
  - the theme with `save_figure` and a validated lever palette;
  - `scripts/technique_data.py` with one draft record;
  - 20 claim-test stubs, plus 28 passing tooling tests;
  - `scripts/word_count.py` and `scripts/check_portability.py`;
  - CI (`ci.yml`: ruff, pytest, word count, portability, stale includes; `docs.yml`: render,
    failing on any warning; **no deploy**).
- [x] Checks at the gate: `ruff` clean; `pytest`: 28 passed, 20 skipped (claim stubs);
      `quarto render docs`: 0 warnings, and every cross-file `#sec-` anchor resolves (checked by script); word count
      2,164 prose words (2,783 raw); portability checks pass. CI has not run on GitHub,
      because nothing is pushed.

### What Phase 0 found that changes the plan

1. **The long-tail half of the thesis needs rewording** (`review.md` issues 1–3). Redundancy
   explains why uniform sampling's exponent is α/(1+α) rather than α. The tail mass is what
   makes it a power law at all. The oracle coverage selector is still a power law
   (n^−α). The signature figure's panel B should add a non-oracle selector.
2. **Prior art for chapter 13 and claim 20:** Dohmatob et al. 2024 analyze Hutter's model with
   q ≠ p (tail cutting, model collapse, buying back the tail). Claim 20 becomes a check against
   their rates. Positioning claim 3 is reworded from "made computable" to "reproduced
   exactly and connected to the levers".
3. **Sibling coverage the spec assumed does not exist:**
   - `transformer-atlas` has no tokenization material (no page mentions a tokenizer). The
     "tokenizer internals: link transformer-atlas" pointer (SPEC §3, §4) has no target;
     chapters 3 and 7 must cite primary sources instead, or drop the pointer.
   - `optimization-lab` shows conditioning slowing gradient descent (Foundations, Least
     Squares) but never connects it to *feature scaling*. Chapter 5 must state the bridge
     itself: for linear least squares, per-feature scaling changes the conditioning of the
     Hessian. It needs a test, and the link then covers only the consequence. This moves the
     coverage item from M toward S.
   - `optimization-lab` has no CONVENTIONS.md and no notation appendix; its notation was taken
     from chapter text where needed.
4. **Word-count basis.** SPEC §1's sibling sizes are raw `wc -w` counts (reproduced exactly:
   15,229 / 27,552 / 28,895 / 36,967). The siblings' *prose*, counted the way
   `scripts/word_count.py` counts it, is 9,097 / 24,838 / 25,590 / 33,138. The cap is
   enforced on prose, as SPEC §1 words it, so it is effectively looser than the calibration
   suggests. Owner question.
5. **Notation conflicts** resolved in `docs/appendix-notation.qmd`: class priors are p(y) and
   q(y), not π_y (siblings reserve π for policies), so claim 10 is restated; Hutter's θ_i is
   p_i; σ is the sigmoid, so noise scale is σ_ε.

## Phase 1: testbeds and the signature figure (2026-10-04): done; ⛳ Gate 1 passed 2026-10-04 (DECISIONS D8)

- [x] T1–T5 implemented in `src/data_lab/testbeds/`, each with ground-truth tests:
  - T1: 7 tests, against SciPy's lognorm, quadrature and Monte Carlo;
  - T2: 20 tests (claims 14–16, plus the selection derivation);
  - T3: 7 tests, including a primal reference solver compared by objective value;
  - T4: 5 tests, including an entropy-rate check by brute-force enumeration;
  - T5: 4 tests, including exact invariance of the synthetic label.
- [x] §7's coverage-selection extension derived and tested, with a non-oracle (pool) selector
      added (docs/appendix-testbeds.qmd, section T2).
- [x] Signature figure `fig_long_tail_signature.py` → `docs/images/long_tail_signature.png`
      (about 9 s), inspected twice; included in the testbeds appendix.
- [x] Testbeds appendix written (T1–T5, each with what it cannot show); notation extended.
- [x] Checks: `ruff` clean; `pytest`: 71 passed, 18 skipped (claim stubs for Phases 2–3), 6 s;
      `quarto render docs`: 0 warnings; 3,288 prose words.

### What Phase 1 showed (and why it matters for Part IV)

1. **SPEC §7's extension holds.** The oracle coverage selector's error is sum_{i>n} p_i,
   between (n+1)^−α and n^−α over αζ(α+1): exponent α against uniform's α/(1+α). It is still a
   power law.
2. **New result: what a non-oracle selector can buy is limited by its unlabeled pool.** A
   selector that ranks features by their count in a pool of M draws has expected error ≥
   max(oracle at n, E_M).
   - With M ∝ n it keeps uniform's exponent: a constant-factor gain only (slopes −0.49 to
     −0.51 at α = 1 over 10 seed sets).
   - With M = n^(1+α) it reaches the oracle's exponent (slopes −0.99 to −1.01), at about 1.45
     times the oracle's error.

   This sharpens the thesis: in this model, selection steepens the power law only if the pool
   of candidates grows superlinearly in the labeling budget. It is a natural bridge to active
   learning and to Dohmatob et al.'s "acquiring the missing tail".
3. **Hutter's coefficient for the normalized Zipf distribution** (his eq. 4 rescaled) matches
   the exact sum to 0.1%, so the figure's guide lines are computed, not fitted.
4. **The max-margin solver needed an exact polish.** L-BFGS-B alone stopped 2·10⁻⁵ short of
   the optimum, which the primal reference test caught. With the active-set polish, the
   duality gap is below 10⁻¹⁴.

### Applied to SPEC v0.3 at Gate 1 (D8)

- Claim 16: add the pool-selector results (bound; linear pool keeps uniform's exponent; a pool
  of size n^(1+α) recovers the oracle's). Tests exist already.
- The signature figure's panel B is as specified, plus the pool selectors.
- T5 images: a synthetic "side" label gives exact invariance (up–down flip) and exact label
  reversal (left–right flip); digit-class labels alone have no exactly known invariance.

## Phase 2: Parts I and II (2026-10-04 to 2026-10-05): drafted, at ⛳ Gate 2 (audit pending)

- [x] Chapters 1–7 written to the template, each researched first (research-log.md, Phase 2),
      with a computed figure that was inspected (8 figures), data cards generated from records
      (19 cards so far), and every checkable statement named with its test.
- [x] Claims 1–9 and 21 pass; claims 22–35 added for statements the chapters needed
      (selection, stratification, label noise, confident learning, aliasing, spectrogram,
      temporal leakage, duplicates, robust scaling, smearing, quantile clipping, encodings).
- [x] COVERAGE.md: all 27 Part I and II items present at their depth.
- [x] Checks: ruff clean; pytest 106 passed, 8 skipped (Phase 3 stubs); render 0 warnings;
      12,488 prose words (chapters 1,193 to 1,699 each); portability checks pass.
- [x] Fresh-agent `learning-repo-audit` after chapter 7 (SPEC §15), 2026-10-05:
      [`audits/2026-10-05-phase2-audit.md`](audits/2026-10-05-phase2-audit.md). No hard fails
      or blockers; scores 4 on criteria 1–6 and 9, 3 on consistency and hygiene. All findings
      fixed the same day (below) except the two that need the owner (commit, CI).
- [ ] Decision test with Part II material (SPEC §14.1, partial): needs 3–5 human readers;
      cannot be run by the agent.
- [x] The owner reads chapters 1–7 (SPEC §13): Gate 2, 2026-10-05.

### What Phase 2 found (evidence over the spec)

1. **Claim 9 was wrong as worded.** Unsupervised steps (scaler, imputer) fit on train + test
   change i.i.d. test accuracy by under 0.4 points and not consistently upward (200 seeds); the
   large optimism comes from supervised steps (feature selection before CV: 0.825 against a
   true 0.5). Restated in the test and in chapter 4.
2. **Claim 2 holds only on the training points.** scikit-learn thresholds sit at node-level
   midpoints, which nonlinear monotone transforms do not keep: up to 0.16% of new points
   change prediction. Restated in the test and in chapter 5.
3. **Smearing has a second failure:** with heteroscedastic noise the factor is not just biased
   by region but unstable across seeds (from 2.1 to 11.1). New claim 31.
4. **Confident learning's precision is set by class overlap,** from 0.999 down to 0.33 at a 20%
   noise rate, which the chapter now leads with.
5. **Sources not fully readable:** Duan 1983 (abstract only; the smearing formula is derived and
   tested, and the chapter says so); Rubin 1976 (definitions taken from van Buuren 2018);
   Kaufman et al. read in the KDD 2011 version, cited as the 2012 article.

### Audit findings and their fixes (2026-10-05)

- **M1** complete-case result box too broad → limited to the mean; regressions on complete
  cases tied to chapter 1's selection-on-x result; card updated.
- **M2** encoding figure not reproducible (TargetEncoder shuffles folds unseeded) → seeded
  `KFold(5, shuffle=True, random_state=s)`; figure regenerated twice, byte-identical; prose
  number updated (cross-fit coefficient −0.05); practitioner box warns about the default.
- **M3** chapter 1 box omitted known-s reweighting → added, with a new test showing that 1/s
  weights undo selection on y, slowly (0.781 at n = 4,000; 0.801 at 256,000).
- **m1** drifting prose numbers → replaced by measured ranges (0.719–0.731; 0.988–1.008; 0.34).
- **m2** "Checked by" mismatches → chapter 5 now quotes the tests' own settings (scale 100;
  scales 1, 100, 0.01 with offset 50) and cites the figure for scale 300; logit units stated.
- **m3** notation → 10 symbols added to the appendix; T1's classifier coefficients renamed
  `u, u0` in code to match the book (`w` is reserved for weights). All figures regenerated:
  byte-identical except encoding.png.
- **m4** stale status text → front page, README and CLAUDE.md updated.
- **m5** "T1's features are Gaussian" → "Gaussian or exactly log-normal".
- **m6** citation locations → confident learning's four folds cited to §5 as a default; the
  QuantileTransformer quote now matches its context; Kaufman et al. now cited to the KDD 2011
  paper that was read (Crossref 10.1145/2020408.2020496).
- **m7** CI include check ignored untracked files → `git status --porcelain` check.
- **Not fixed (owner):** the work is uncommitted, and CI has never run on GitHub.
- **Audit suggestion, deferred to Phase 3:** generate headline numbers from scripts into
  includes, as the data cards are, since every number discrepancy came from hand-copying.

### Proposed for SPEC at Gate 2

- Restate claims 2 and 9 as in the tests; add claims 22–35 to §8.
- The tokenizer pointer stays dropped; chapter 3 says no sibling covers it.

## Phase 3: Parts III and IV (2026-10-05): done; ⛳ Gate 3 passed 2026-10-05 (DECISIONS D10)

- [x] Gate 2 passed 2026-10-05 (the owner read chapters 1–7: "looks good ... move on").
- [x] Chapters 8–14 written to the template, each researched first (research-log.md,
      Phase 3), with a computed, inspected figure (6 new figures; the signature figure revised)
      and 18 new data cards (37 in all), all generated from records.
- [x] Claims 10–13 and 17–20 pass; claims 36–43 added for statements the chapters needed
      (balancing variance, SMOTE's gap, label-changing augmentation, shift detection, the
      least-squares floor, how-much-data extrapolation, the scaling floor, uncertainty
      sampling). Chapter 13 gained five tests from its review (below).
- [x] Published numbers (D9): chapters 8–14 quote `{{< var >}}` values written by their figure
      scripts; nothing is hand-copied.
- [x] `skeptical-review` of chapter 13 by a fresh agent:
      [`audits/2026-10-05-ch13-skeptical-review.md`](audits/2026-10-05-ch13-skeptical-review.md).
      "Revise", no hard fails; every issue fixed (resolution at the end of that file).
- [x] COVERAGE.md: all Part III and IV items ticked.
- [x] Checks: ruff clean; pytest 142 passed; render 0 warnings; 22,257 prose words;
      portability checks pass; mechanical checks: no missing or orphan images, no unresolved
      citations or links.
- [x] The owner accepts chapters 8–15 (SPEC §13): 2026-10-05, at publication.

### What Phase 3 found (evidence over the spec)

1. **Coverage selection gains per label, not per draw, and not from the ordering** (chapter 13
   review, verified exactly). Labeling each new case from a uniform stream already has the
   oracle's exponent −α per label, at β Γ(β)^(1+α) times its error (π/2 at α = 1; derived in
   the T2 appendix and tested). It costs about n^(1+α) draws, and per draw nothing beats
   uniform sampling. SPEC §7 and §9 attribute the gain to frequency-first selection; the
   chapter, Panel B of the signature figure and the coverage card are revised.
2. **Balancing tilts the posterior in a correctable way.** Undersampling and class weights
   aim at the same target with different variance (sd 0.068 against 0.048).
3. **SMOTE fills the gap between minority clusters only when k exceeds the cluster size.**
4. **Importance weighting's variance explodes with shift** (computed exactly: effective n
   about 100 of 1,000 at the largest shift shown).
5. **Concept shift is invisible to input-only tests.**
6. **Extrapolating how much data is needed is dominated by the floor:** with it unknown, half
   the pilots give infinite estimates; with it known, the median is 130 against a true 230 and
   the interval spans a factor of 95.
7. **Scaling forms on a known floor:** a pure power law extrapolates below the entropy rate,
   a law with a floor overestimates, and the local exponent drifts.
8. **Active learning on noisy labels:** a 20-seed pilot suggested harm; 60 seeds showed no
   measurable difference (ratio 1.07). Claim restated as "the gain vanishes".
9. **Deduplication:** restated as optimism above 0.3 nats removed by deduplication, not
   "below the entropy rate".
10. **Sources not fully readable:** Shumailov et al.'s 2025 correction (Nature login; the
    chapter says so); Moreno-Torres et al. read in the 2013 thesis reprint.

### Proposed for SPEC at Gate 3

- Add claims 36–43 to §8, as worded in the tests.
- Restate claim 16 and §7: per label, not labeling repeats buys the exponent α and frequency
  order a constant β Γ(β)^(1+α); the gain costs about n^(1+α) draws; per draw nothing beats
  n^(−α/(1+α)). Restate claims 17–18 as tested.
- §9, signature figure Panel B: error against labels used, with the exact
  "uniform, new cases only" curve (already applied, as a correctness fix).

## Phase 4: synthesis and release (2026-10-05): done; published

- [x] Phases 2 and 3 committed locally (d0959e8), not pushed (D10).
- [x] Chapter 15, *A Data Decision Guide*: a four-step procedure (deployment question →
      representation → training distribution → enough data), each step checked against a
      baseline, and two worked examples computed on T1 and T5 (claims 44–46; one figure; one
      new card, per-recording normalization; 38 cards in the generated table).
- [x] The Map: the four levers and evaluation, the SPEC §1 questions with short answers and
      where each is answered, how the book argues, reading paths.
- [x] Appendices: the glossary (37 terms, each linked to its chapter); Further Reading (only
      sources read for the book); What the Toys Cannot Show (generated from the chapters).
- [x] Front page: "How this book was made" (D0), with roles and the model version.
- [x] COVERAGE.md: every item ticked.
- [x] Final fresh-agent `learning-repo-audit` (SPEC §15), 2026-10-05:
      [`audits/2026-10-05-final-audit.md`](audits/2026-10-05-final-audit.md). Scores 5, 5, 4, 5,
      4, 5, 4, 4, 5 (≥ 4 everywhere, 5 on computed evidence); no hard fails or blockers. All
      figures, numbers and includes reproduced byte-identically. One major finding (Panel B
      plotted small pools at an unspent budget) and five minor ones fixed the same day; CI on
      GitHub (m6) is the owner's call.
- [ ] Success tests (SPEC §14): optional (D4); they need human readers.
- [x] Publication (D5, 2026-10-05): repository made public; GitHub Pages deployed from `main`
      by `docs.yml`; site linked from the README.

### What Phase 4 found

1. **The worked examples surfaced an interaction.** Regression imputation and smearing are
   each sound, and together bias the total upward (+3.8%): the imputed values carry no noise,
   so their error lands in the residuals the smearing factor averages. Mean imputation shrinks
   the coefficients instead. Both mechanisms are tested.
2. **The Map answers the SPEC §1 question "How smarter data selection can beat that law"
   with "it cannot, only steepen it per label"** (D10), and says so.
3. **The final audit caught a real error in the signature figure.** A pool of $M = 10n$ draws
   holds only about 138 distinct cases at $n = 1{,}000$, so its selector never spends the
   budget; plotted at the labels it actually uses, it lies on the deduplicated stream's curve.
   The per-label story holds and is now simpler: what any selector reading a uniform stream
   buys per label is skipping repeats, plus at most the ordering constant.
4. **The first CI run exposed an inexact solver.** The T3 max-margin solver (L-BFGS-B plus an
   active-set polish, Phase 1) silently returned non-optimal students in 3 of 60 solves at
   P/N = 16 (minimum margin as low as 0.62), and took over 120 s on the CI runner. It is
   replaced by an exact least-distance solver via non-negative least squares that certifies
   every answer by its KKT conditions or raises; the pruning experiment runs in 1 s, and no
   published number changed at its printed precision. A second test (`arccos` near 1 compared
   to 10⁻⁹) was ill-posed and now compares cosines.
5. **Notation slip caught:** chapter 15's first draft used bare σ for a standard deviation;
   the book reserves it for the sigmoid (now σ_ε).

## After publication: cross-repository assessment (2026-10-05)

A protocol for comparing the learning-repo books on output quality
([`assessment/PROTOCOL.md`](assessment/PROTOCOL.md)), piloted on data-lab and rl-for-llms
([`assessment/pilot-2026-10-05.md`](assessment/pilot-2026-10-05.md)). Neither book was
measurably more correct (4% sampled defect rate each; about 3 and 4 minor defects per 10,000
words, no major ones); data-lab is more verifiable (generated numbers, named tests). The 8
confirmed data-lab defects are fixed. Protocol v2 runs on all four books next.

## Durations

| Phase | Started | Gate reached |
|---|---|---|
| 0 | 2026-10-04 | 2026-10-04 |
| 1 | 2026-10-04 | 2026-10-04 |
| 2 | 2026-10-04 | 2026-10-05 |
| 3 | 2026-10-05 | 2026-10-05 |
| 4 | 2026-10-05 | 2026-10-05 (published) |

## Decision log

- 2026-10-04: **Gate 0 passed; SPEC v0.2.** The owner accepted review recommendations 1–3,
  chose prose for the word cap, and asked the agent to apply the SPEC edits (DECISIONS D7).
  Card schema gained `levers=["evaluation"]`; claim 21 (feature scaling and conditioning) and
  its stub were added; the coverage item moved from M to S.

- 2026-10-04: **Chapter heading carries the ID (`# Title {#sec-id}`) instead of a YAML
  title.** Why: SPEC §11 and objectives-book §21.1 want cross-references that target Quarto
  IDs; a chapter-level ID is the simplest form, and the render confirmed that
  a Markdown link to a chapter file plus its `#sec-` anchor resolves across files. Alternative: YAML title plus `@sec-`
  (prints numbers, which SPEC §11 avoids in prose).
- 2026-10-04: **The Map is unnumbered.** Why: SPEC §5 numbers chapters 0–15, with the Map as
  0. Quarto numbers from 1, so an unnumbered Map makes displayed numbers match the spec and
  the file names.
- 2026-10-04: **Lever palette: blue, orange, aqua, violet.** Why: it passes every validator
  check, compared across all pairs. Magenta (the fifth sibling slot) fails the normal-vision
  floor against orange (ΔE 12.9). Aqua is a contrast WARN, so labels are mandatory.
- 2026-10-04: **Theme's default color cycle is one gray.** Why: SPEC §9 forbids cycled
  colors; a forgotten `color=` then shows as obviously wrong.
- 2026-10-04: **`Private :: Do Not Upload` classifier.** Why: D2 says never published; PyPI
  "will always reject packages with classifiers beginning with `Private ::`"
  (pypi.org/classifiers, read 2026-10-04).
- 2026-10-04: **Python pinned to 3.12 for the venv (`.python-version`); `requires-python
  >= 3.11`.** Why: reproducible lock; 3.12 was the interpreter uv selected.
- 2026-10-04: **Dev tools in a uv dependency group** (`uv sync` installs them; CI uses
  `uv sync --locked`). Why: one command, and it fails if the lockfile is stale.
- 2026-10-04: **Portability checks in CI** (no raw HTML, 80-character code, no emoji, no
  hand-typed chapter numbers). Why: D6 adopts objectives-book §21.1; its §21.2 lists these
  checks.
- 2026-10-04: **`docs.yml` renders and fails on any `WARN`, with no deploy job.** Why: D5 is
  open and Pages on this account is public.
- 2026-10-04: **Bibliography generated from the APIs, not typed.** 49 entries: Appendix A, plus
  sources found in Phase 0 (Dohmatob, Cabannes, Sharma & Kaplan, Ayed & Hayou, Goyal,
  Gerstgrasser, the Nature version of Shumailov and its correction, Settles, Kuhn & Johnson).
- 2026-10-04: **Claim stubs skip with the phase of their chapter**, not "Phase 2" for all
  (see Phase 3 note).
- 2026-10-04: **No figure scripts yet.** Why: SPEC puts the signature figure and testbeds in
  Phase 1; `scripts/figures/` holds only the theme and its README.
