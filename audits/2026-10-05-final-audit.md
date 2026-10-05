# Audit: data-lab (*What the Model Sees*): final draft, 2026-10-05

**Commit audited:** HEAD `d0959e8` plus 24 uncommitted paths (Phase 4: chapter 15, the Map, the appendices, `src/data_lab/worked.py`, `tests/test_worked_examples.py`, `fig_decision_guide.py` and others). As instructed, the audit copy was made from the working tree (`rsync`, without `.venv`), so the audit covers this **uncommitted** state, not a commit. `origin/main` is still `c0ee9c8`.
**Profile:** book (Quarto). Figures are pre-generated PNGs, Quarto runs no code, and published numbers come from `docs/_variables.yml`, which the figure scripts write.
**Auditor sample:**
- 22 source claims opened against primary sources: arXiv abstracts, full-text PDFs and a tech report.
- About 40 quoted numbers recomputed.
- All 16 figure scripts re-run, including the signature figure, and all 16 PNGs inspected.

**Thesis (one sentence):** every data technique pulls one of four levers (representation, sampling distribution q, weights w, labels), and on a long tail the error is the uncovered mass, so selection steepens the power law per label but never escapes it. Each claim is measured on testbeds with exact ground truth.

## Verdict

A reader can trust this book. Every figure regenerates byte-identically. Every published variable is reproduced exactly by a fresh run. All 146 tests pass, and every one of the 67 distinct tests named in the prose exists. Each of the 22 sampled source claims says what the book says it says. The strongest assets:
- the exact long-tail machinery;
- the research log;
- the habit of restating the SPEC when the evidence disagreed (claims 2, 9, 16, 17, 18 and 43).

One issue matters. The signature figure's Panel B plots the M = 10n and M = 100n pool selectors against "labels used n", but those selectors never spend their budget. At n = 1,000 they label 137 and 436 cases. The chapter 13 review raised this as issue 2, and the fix covered only the M = n case.

The other findings are minor consistency items. **Verdict: trustworthy with fixes.**

## Scores

| Criterion | Score | Note |
|---|---|---|
| 1. Source fidelity | 5 | 22 of 22 sampled claims verified (numbers, quotes, section and table locations); the research log records reading depth honestly; corrections are cited (Besiroglu et al. on Chinchilla, the Shumailov 2025 correction marked unread, Gerstgrasser et al.). One gap: the importance-weighting lineage source SPEC §2.1 promises is absent (m4). |
| 2. Computed evidence | 5 | All 16 scripts run (1–44 s each). All 16 PNGs, `_variables.yml` and every generated include are byte-identical to the committed files. No hard-coded results. The seeded `TargetEncoder` fix (Phase 2 M2) holds: two runs are identical. |
| 3. Claims match measurements | 4 | Every quoted number checked matches a fresh run, including the hand-typed numbers in chapters 1–7. But Panel B's "labels used" axis is false for two pool curves, and the prose reads them that way (M1). Chapter 15 cites panel A for a number it does not show (m3). |
| 4. Correctness | 5 | Re-derived the chapter 13 / T2 constant βΓ(β)^(1+α) (1.46, π/2, 1.66) and m ≈ (n/Γ(β))^s/A (524,000 draws at n = 1,000), the noisy-label threshold, and E_q[w²] = exp(δᵀΣ⁻¹δ). Tests check closed forms, exact sums and reference solvers by objective value (69 numeric-tolerance assertions). |
| 5. Pedagogy | 4 | One thesis, a strict template, assumptions with what breaks, Connections that say why. The Map openly says the original question ("beat the law") was answered "it cannot". Chapter 14's at-scale paragraphs and the 38 dense cards read more like a catalogue than the rest of the book. |
| 6. Honesty and currency | 5 | Evidence labels throughout chapters 12–14 ("replicated", "single study, 2022", "contested, as of October 2026"); every chapter has *What the toy cannot show*, collected in an appendix; negative and seed-dependent results are reported (claim 43's 20-seed versus 60-seed result). |
| 7. Internal consistency | 4 | Render has 0 warnings, 0 broken links and 0 undefined citations. But the front page and the Map claim every number is script-written, which is false for chapters 1–7 (m1); there are notation collisions in chapter 12 and two figures (m2); the complete-case card disagrees with chapter 15 (m5). |
| 8. Engineering hygiene | 4 | `uv sync`, ruff, pytest (146 passed, 153 s), word count, portability, `technique_data.py` and `quarto render docs` (0 WARN) all work verbatim; dependencies are locked. However, CI has **never run** (`gh run list` is empty), the Phase 4 work is uncommitted, and there is no deploy, by design (D5). |
| 9. Economy | 5 | 25,685 prose words (target 22–30k, cap 35k). Chapters run 1,201–1,737 words, tight and in scope; sibling topics are linked, not re-derived. |

**Hard fails:** none.
- **No fabricated source:** all 22 sampled claims were found in the source.
- **No fabricated result:** every figure and variable regenerates exactly.
- **No wrong core claim:** M1 mislabels what a curve's x-axis counts. The bound and the exact results in chapter 13 are correct.

**Against SPEC §13 (whole-book acceptance):**
- ≥ 4 on every criterion, no hard fails, 5 on computed evidence: **met** by this audit.
- Still open, as the owner's items: "CI green from a clean clone" and the human success tests.

## What's strong (keep)

- **`docs/_variables.yml` plus `{{< var >}}`** (chapters 8–15). Every published number in Parts III–V is written by the script that computed it, and a fresh run reproduced the file byte for byte.
- **The T2 machinery** (`src/data_lab/testbeds/t2_zipf.py`, `docs/appendix-testbeds.qmd:8–115`):
  - an exact bracketed sum;
  - a normalized-Zipf coefficient tested to 0.1%;
  - the optimality bound `test_any_n_labels_cost_at_least_the_tail_mass`;
  - the per-label versus per-draw split (`13-why-power-laws.qmd:65–91`).

  The derivation at `appendix-testbeds.qmd:61–73` is correct; I re-derived it.
- **Evidence over the SPEC, said in the book:**
  - the Map's last-row note (`00-the-map.qmd:55–56`);
  - claim 43's restatement (`14-choosing-data.qmd:84–85`);
  - the duplicate-in-bootstrap failure mode (`11-learning-curves.qmd:106–108`).
- **Chapter 15's worked examples** (`15-decision-guide.qmd:55–113`). They surface a real interaction (regression imputation plus smearing gives +3.8%) and test it.
- **The phase 2 audit fixes held:**
  - M1: complete-case box scoped (`04-cleaning.qmd:58–66`).
  - M2: encoding seeded and reproducible.
  - M3: known-s caveat (`01-…qmd:53–54`).
  - m1/m2: chapter 5 now quotes the tests' own settings; recomputed 0.603, 0.563, 0.729, 1.23×10⁸ and 2.35.
  - m3: notation declared.
  - m4: front page updated.
  - m6: Northcutt §5, Kaufman 2011.
  - m7: CI porcelain check.
- **The chapter 13 review fixes held** for issues 1, 3 and 4, plus the added accounts (Maloney et al.; Cagnetta et al. 2026, verified).

## Findings

### Blockers
None.

### Major

**M1. Signature figure Panel B: the M = 10n and M = 100n pool curves are plotted at the nominal budget on an axis labeled "labels used", but they never spend that budget. The chapter's "constant factor, not a steeper curve" reading depends on it.**

*Where:*
- `scripts/figures/fig_long_tail_signature.py:107–117, 153`: x is the nominal n; the label is "labels used $n$".
- The captions say "error against labels used": `13-why-power-laws.qmd:154` and `appendix-testbeds.qmd:103`.
- `13-why-power-laws.qmd:103–104` ("labels the top $n$"), `:110–111` ("With $M = 10n$, the slope was −0.49: uniform sampling's exponent, shifted down by a constant") and `:162–163` ("A pool proportional to the budget gives a constant factor, not a steeper curve").
- `appendix-testbeds.qmd:94–97`.

*Evidence:* `pool_selector` in a fresh run, α = 1, 20 seeds:

| n | M = 10n: labels actually used | error | E_M | M = 100n: labels used | error | E_M |
|---|---|---|---|---|---|---|
| 1,000 | 137 | 0.00714 | 0.00691 | 436 | 0.00218 | 0.00219 |
| 2,000 | 197 | 0.00484 | 0.00489 | 620 | 0.00153 | 0.00155 |

Over the whole plotted range, both selectors label every case in their pool, and their error is E_M, the uniform curve at the pool size. Measured against the labels they actually use, they lie on the "uniform, new cases only" curve, at slope −α. The chapter 13 review raised exactly this (issue 2: "Plot Panel B against labels actually used, or mark where each pool line becomes pool-limited"). The resolution (`audits/2026-10-05-ch13-skeptical-review.md:282`) fixed only the M = n case. A reader who trusts the axis will believe a pool proportional to the budget buys only a constant factor per label actually spent, which is false.

*Fix:* either
- plot the pool selectors at labels actually used, or
- keep nominal n, but relabel the axis "labeling budget n" and say in the caption and at `:110–111` that for M = 10n and M = 100n the budget is never spent, so the error equals E_M exactly (as already stated for M = n).

Then scope `:162–163` to "per unit of budget". Add a test asserting that `len(pool_selector(...)) < n` for M = 10n at n ≥ 100.

### Minor

**m1. The front page and the Map overstate how numbers are produced.**
- `docs/index.qmd:29–31`: "every number in the text is written by the script that computed it".
- `00-the-map.qmd:66–67`: "every quoted number is written by the script that computed it".

But chapters 1–7, the testbeds appendix and `15-decision-guide.qmd:149` ("within about 10%") use hand-typed numbers. `grep -c "{{< var"` gives 0 for chapters 0–7 and the appendices. The ROADMAP says this was applied only from chapter 8 on. The hand-typed values I recomputed all match (chapter 1: 0.781/0.801, largest weights with medians 64/478; chapter 2: precision 0.343, recall 0.565–0.680; chapter 5: as above; chapter 7: 0.747/0.751/−0.051).
*Fix:* move the chapter 1–7 headline numbers to variables, or reword both sentences ("from chapter 8 on…; earlier numbers are checked by tests").

**m2. Notation collisions not in the appendix.**
- `12-scaling-laws.qmd:39–58` uses $D$ for tokens, while the appendix (`appendix-notation.qmd:22`) defines it as a dataset and chapter 13 uses $D_m$ for distinct counts.
- It uses $E$ and $A$, which the appendix gives to the learning curve and to 1/ζ(s), and $\alpha$ for Hoffmann's and Kaplan's exponents, next to chapter 13's Zipf $\alpha$.
- `fig_scaling_laws.py:59–61` labels its fits with $A D^{-\alpha}$ and $E + A D^{-\alpha}$.
- `fig_learning_curves.py:63, 113` use a bare $\sigma^2$ ("Bayes floor σ²", "1.05 σ²"), against `appendix-notation.qmd:95` ("bare σ is never a standard deviation in this book").

*Fix:* add a "quoting a source's notation" row (or subscripts such as $\alpha_N$, $\alpha_D$, $L$, $N$, $D_{\text{tok}}$) and use $\sigma_\varepsilon^2$ in both figures.

**m3. Chapter 15 cites a panel for a number it does not show, and the number is untested.**
- `15-decision-guide.qmd:149–150`: "Least squares on the raw cost gets the total within about 10% and every row wrong (panels A and B)". Panel A plots only the exp-fit and smearing rows; the raw pipeline is not in it.
- A fresh run gives a raw complete-case total bias of −10.2% (range −15.8% to −3.0%).
- No variable or test checks it.

*Fix:* add the raw rows to panel A, or cite panel B only and publish the bias as a `ch15` variable.

**m4. The lineage callout SPEC §2.1 promises is missing, and importance weighting has no source.**
- `SPEC.md:113–115`: "importance weighting under covariate shift; the dataset-shift literature gets a lineage callout, sourced in Phase 3".
- CONVENTIONS defines a `callout-important` "Lineage" box.
- `grep` finds no Lineage callout and no Shimodaira (or similar) entry in the bib or the research log. `08-sampling-and-weighting.qmd:95–113` presents importance weighting uncited.

*Fix:* add the callout with the primary source (e.g. Shimodaira 2000, *J. Stat. Plan. Inference*), read and logged, or record in ROADMAP why it was dropped.

**m5. The complete-case card's Assumption field contradicts chapter 15's own use of complete cases.**
- `scripts/technique_data.py:163` gives "MCAR: whether a value is missing is unrelated to anything", and the generated decision-guide table shows only Assumption and Failure modes ("MAR or MNAR missingness (biased estimates)").
- Yet `15-decision-guide.qmd:74–76` correctly drops incomplete rows under MAR on an observed predictor and keeps $p(y\mid x)$.

*Fix:* make the Assumption field "MCAR for means; for a regression, missingness that depends only on its inputs".

**m6. Hygiene, owner-gated.**
- CI has never run (`gh run list` is empty), so SPEC §13's "CI green from a clean clone" is unverified.
- Phase 4 (24 paths, including chapter 15 and `worked.py`) is uncommitted.
- `origin/main` = `c0ee9c8`.

*Fix:* commit and push to a private remote, or run the two workflows with `act` or `workflow_dispatch`, before release.

### Polish
1. `01-the-data-generating-process.qmd:131` "miscalibrated everywhere" and `07-encoding-and-features.qmd:115` "two or more alphanumeric characters" were Phase 2 polish items and are unchanged.
2. `01-…qmd:85–86`: "largest weight grew from about 60 to about 480" are medians across seeds (64 and 478; the means are 89 and 738). Say "median".
3. `14-choosing-data.qmd:32–33`: Sorscher et al.'s faster-than-power-law result holds "if we have access to a high-quality data pruning metric" (abstract). Put that condition in the sentence.
4. `02-labels.qmd:111`: "Recall stays between 0.55 and 0.69"; measured 0.565–0.680.
5. `13-why-power-laws.qmd:79–80`: 524,000 draws "about $n^{1+\alpha}$" (10⁶). The appendix's $(n/\Gamma(\beta))^s/A$ is the accurate count; cite it here.

## Mechanical checks

- **Images:** 16 referenced, 16 with a script; 0 missing, 0 orphan, 0 unscripted.
- **Bibliography:** 54 entries; 0 undefined keys; 0 uncited; 0 without an identifier.
- **Online identifiers:** 37 arXiv ids and 15 DOIs checked; 0 not found; 0 title mismatches.
- **Links:** 0 dangling paths in project docs; 0 broken internal links.
- **Tests:** 108 test functions in 26 files (146 collected cases, all passed, 0 skipped, 153 s); 69 numeric-tolerance assertions.
- **Test references:** a script cross-checked every test reference in the prose, cards and records: 146 references, 67 distinct, all exist (the only non-matches are the `test_x::test_y` format examples in `technique_data.py`).
- **Lint and scripts:** `ruff` reports all checks passed; `word_count.py` gives 25,685 prose words (the Map's 882 is outside the per-chapter band, warning only); `check_portability.py` passes.
- **Generated files:** `technique_data.py` regenerates the 38 cards, the decision guide and the toy limits byte-identically.
- **Render:** `quarto render docs` finishes with 0 WARN lines. Rendered titles: the Map unnumbered, chapters 1–15 matching the file names, appendices A–E, consistent with the README ("the Map, 15 chapters, 5 appendices").
- **CI and site:** CI has no runs. No live site, by design (D5).

<details><summary>Mechanical-check script output</summary>

```
- Profile (guess): book
- Images referenced: 16; with a generating script: 16
- Bibliography entries: 54
- Lockfile: uv.lock; CI workflows: .github/workflows/ci.yml, .github/workflows/docs.yml
- Tests: 108 functions in 26 files; 69 numeric-tolerance assertions
- Research/source log: research-log.md; license: LICENSE
Missing images (0) · Orphan images (0) · Unscripted (0)
Citation keys with no bib entry (0) · Never cited (0) · No DOI/URL/eprint (0)
Dangling paths (0) · Broken internal links (0)
arXiv ids checked: 37; DOIs checked: 15; not found 0; unresolved 0; title mismatches 0
```
</details>

## Claims checked

| # | Claim (location) | Source opened | Verdict | What the source says |
|---|---|---|---|---|
| 1 | Hestness: theory −0.5 or −1; measured "usually settles between −0.07 and −0.35" (§1) (`12:30–33`) | arXiv 1712.00409 PDF | ok | "βg usually settles between −0.07 and −0.35, exponents that are unexplained by prior theoretical work"; "βg = −0.5 or −1" |
| 2 | Kaplan: α_D ≈ 0.095 (eq. 1.2), α_N ≈ 0.076 (eq. 1.1), N ∝ C^0.73 (`12:37–42`) | arXiv 2001.08361 PDF | ok | eq. 1.1 αN ∼ 0.076; eq. 1.2 αD ∼ 0.095; eq. 6.1 N(Cmin) ∝ Cmin^0.73 |
| 3 | Hoffmann: over 400 models; equal-scaling quote; Table 2: 0.50, 0.49, 0.46; 70B on 1.4T (`12:44–51`) | arXiv 2203.15556 abstract and PDF | ok | Abstract verbatim; Table 2 rows 0.50 / 0.49 / 0.46; "70B model, called Chinchilla, on 1.4 trillion tokens" |
| 4 | Hoffmann: E = 1.69, α = 0.34, β = 0.28; "should correspond to the entropy of natural text" (§3.3, D.2) (`12:53–58`) | same PDF | ok | "E = 1.69, A = 406.4, B = 410.7", exponents 0.34 / 0.28; quote at §3.3 |
| 5 | Besiroglu: "inconsistent with their first two estimation methods", "implausibly narrow", refit compatible (`12:58–62`) | arXiv 2404.10102 abstract | ok | Verbatim |
| 6 | Muennighoff: 4 epochs "negligible changes", value "decays to zero", half-life ≈ 16 epochs, "returns diminish extremely fast" (§6) (`12:64–68`) | arXiv 2305.16264 abstract and PDF | ok | Abstract verbatim; §6: "up to around 16 epochs (RD) beyond which returns diminish extremely fast" |
| 7 | Cagnetta et al. 2026: parameter-free data-limited exponents from token-correlation decay and conditional-entropy decay; GPT-2 / LLaMA style on TinyStories and WikiText (`13:135–138`) | arXiv 2602.07488 abstract | ok | As stated; labeled "one study" |
| 8 | Maloney et al.: spectral power laws in test loss; finite spectrum gives a plateau (`13:132–134`) | arXiv 2210.16859 abstract | ok | "the finite extent of the data's spectral power law causes the model's performance to plateau" |
| 9 | Michaud: "tentatively find" (`13:140–141`) | arXiv 2303.13506 abstract | ok | Verbatim |
| 10 | Feldman: "memorization is necessary" with long-tailed subpopulations (`13:126–128`) | arXiv 1906.05271 abstract | ok | Verbatim |
| 11 | Kandpal quote (`13:129–131`) | arXiv 2211.08411 abstract | ok | Verbatim |
| 12 | Sharma & Kaplan: exponents ≈ 4/d (`13:120–122`) | arXiv 2004.10802 abstract | ok | "α ≈ 4/d" (as a parameter-scaling exponent, as the book says) |
| 13 | Recht: drops 3–15% / 11–14%; not adaptivity, "slightly 'harder' images" (`10:83–89`) | arXiv 1902.10811 abstract | ok | Verbatim; framed as one study, dated 2019 |
| 14 | Lopez-Paz & Oquab: C2ST pairing and "near chance-level" quotes (`10:46–49`) | arXiv 1610.06545 abstract | ok | Verbatim |
| 15 | DoReMi "2.6x fewer training steps" (`14:97–100`) | arXiv 2305.10429 abstract | ok | Verbatim |
| 16 | RHO-LOSS: 18× fewer steps on a web-scraped noisy benchmark (`14:89–93`) | arXiv 2206.07137 abstract | ok | "On … Clothing-1M, RHO-LOSS trains in 18x fewer steps" |
| 17 | Ayed & Hayou: random pruning "outperforms most existing data pruning methods in the high compression regime" (`14:48–50`) | arXiv 2302.06960 abstract | ok | Verbatim |
| 18 | Goyal et al.: "rapidly loses its utility when repeated"; "cannot be agnostic of the total compute" (`14:102–105`) | arXiv 2404.07177 abstract | ok | Verbatim |
| 19 | Sorscher: faster than a power law with pruning (`14:31–33`) | arXiv 2206.14486 abstract | imprecise (polish 3) | True "if we have access to a high-quality data pruning metric"; that condition is dropped from the sentence |
| 20 | Settles §3.1: uncertainty sampling "queries the instance whose posterior probability of being positive is nearest 0.5" (`14:75–76`) | burrsettles.com tech-report PDF | ok | Verbatim, §3.1 |
| 21 | SpecAugment: f and t uniform from 0 to F and T (§2) (`09:75–79`) | arXiv 1904.08779 PDF | ok | "chosen from a uniform distribution from 0 to the frequency/time mask parameter" |
| 22 | Hutter rate, the oracle bound and the β Γ(β)^(1+α) constant (`13:34–77`; `appendix-testbeds:54–73`) | re-derived by hand, plus a fresh run | ok | The integral approximation gives E[D_m] ≈ Γ(β)(Am)^{1/s} and E_m ≈ A^{1/s}Γ(β)m^{−β}/s, hence ratio βΓ(β)^{1+α}: 1.462 / 1.571 / 1.655 for α = 0.5 / 1 / 2, matching the variables; 524,000 draws at n = 1,000 matches (n/√π)²ζ(2) |

## Figures re-run

All 16 scripts were run in a copy. Every PNG is byte-identical to the committed one, `_variables.yml` is identical, and so are the generated includes. All 16 images were inspected.

| Figure | Script | Reproduces? | Caption accurate? | Note |
|---|---|---|---|---|
| `long_tail_signature.png` (signature) | `fig_long_tail_signature.py` (19 s) | yes, byte-identical | **no** for Panel B's pool curves | M1: the "labels used" axis is not the labels used for M = 10n and 100n |
| `decision_guide.png` | `fig_decision_guide.py` (11 s) | yes | mostly | Prose cites panel A for the raw-cost total, which panel A does not show (m3) |
| `choosing_data.png` | `fig_choosing_data.py` (44 s) | yes | yes | Crossover, dedup, AL ratio 0.57 / 0.97 / 1.07 and collapse curves all match the prose |
| `learning_curves.png` | `fig_learning_curves.py` (28 s) | yes | yes | Bare σ² in the axis labels (m2) |
| `sampling_weighting.png` | `fig_sampling_weighting.py` | yes | yes | sd 0.068 / 0.048 visible; SMOTE threshold annotated |
| `scaling_laws.png` | `fig_scaling_laws.py` | yes | yes | Legend's α collides with the Zipf α (m2) |
| `encoding.png` | `fig_encoding.py` | yes, and reproducible across runs (Phase 2 M2 fixed) | yes | Cross-fit 0.747 / 0.751 / −0.051 recomputed |
| The other 9 (`affine_scaling`, `augmentation`, `changing_shape`, `data_types`, `distribution_shift`, `label_noise`, `leakage`, `missingness`, `selection_bias`) | respective scripts | yes | yes | Chapter 5's 0.603 / 0.563 / 0.729 and 1.23×10⁸ / 2.35 recomputed |

## Decisions for the author

1. **How to fix Panel B (M1).**
   - (a) Plot the pool selectors at labels actually used: they then sit on the new-cases-only curve, which strengthens the chapter's point that skipping repeats is what buys the exponent.
   - (b) Keep the nominal-budget axis and relabel it.

   Recommend (a), with the prose saying "a pool of M draws can supply at most E[D_M] labels".
2. **Chapters 1–7 numbers (m1).** Either convert them to `{{< var >}}` (consistent with chapters 8–15 and the front page's claim), or soften the claim. Recommend converting the headline numbers. This audit found them all correct, so this is about durability, not accuracy.
3. **Release gating (m6).** Push to a private remote, or run CI another way, so that "CI green from a clean clone" is shown rather than inferred. The human success tests (SPEC §14) and D4/D5 remain owner items.

---

## Resolution (2026-10-05)

- **M1 fixed.** Panel B now plots each pool selector at the labels it actually used (mean over
  seeds); the small pools fall on the "uniform, new cases only" curve. Chapter 13, the T2
  appendix, both captions, the coverage card, SPEC claim 16 and the figure index now say that
  a pool with fewer distinct cases than the budget labels them all (138 of 1,000 at M = 10n)
  and has error E_M. New test: `tests/test_long_tail.py::test_linear_pool_leaves_its_budget_unspent`.
- **m1 fixed.** The front page and the Map now say numbers are script-written from *Sampling
  and Weighting* on, and copied from fresh runs before it.
- **m2 fixed.** Chapter 12 states that it keeps the papers' symbols, and the notation
  appendix lists the exception; the scaling-law legend uses $\alpha_D$; the learning-curve
  figure uses $\sigma_\varepsilon^2$.
- **m3 fixed.** The raw-cost total is now a published number (−10%) and cites panel B only.
- **m4 fixed, at bibliographic depth.** A Lineage callout in chapter 8 cites Shimodaira (2000)
  for weighting the likelihood under covariate shift. The paper is closed access and no
  abstract could be retrieved; the callout claims only what the title states and says so.
- **m5 fixed.** The complete-case card's assumption now separates summaries (MCAR) from models
  of $p(y \mid x)$ (missingness that depends only on the inputs).
- **m6 open (owner):** CI has never run on GitHub; Phase 4 is uncommitted.
- **Polish fixed:** "median" largest weights (64 and 478); "over most of the range"; the
  `TfidfVectorizer` token pattern quoted from scikit-learn 1.9.1; recall 0.56–0.68;
  Sorscher et al.'s "high-quality data pruning metric" condition; chapter 13 cites the exact
  draw count from the appendix.
