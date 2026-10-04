# Skeptical review: SPEC §2 (thesis and lens)

Reviewed with the `skeptical-review` skill. Context read: SPEC §1, §2, §4, §7, §11 (chapter 11
row), §17; research-log.md; Hutter 2021 and Dohmatob et al. 2024 in full text; abstracts listed
under *Citations checked*. Scratch computations are described inline and were run on
2026-10-04; they are not book content and will be redone as tests in Phase 1.

## Round 1 — 2026-10-04 (reviewing SPEC v0.1, 2026-10-04)

### Verdict

The lens is a good teaching device. It is concrete: four levers plus a card with a "Checked by"
field. It is falsifiable on purpose, and it ties classical preprocessing to the
(q, w) view the sibling book already uses. The long-tail half of the thesis is weaker than it
reads. It merges two different mechanisms: redundant sampling, and mass in the tail. It
overstates that mechanism's reach ("is set by"). And it does not know the closest prior art,
Dohmatob et al. (2024). That paper already studies Hutter's model with a training distribution q
different from the target p, including tail cutting, model collapse and buying back the missing
tail. None of this sinks the book: a textbook need not be original research. But two sentences
of §2.1 and the third distinctive claim in §4 should change before chapter 13 is planned around
them.

### Scores

| Criterion | Score (1–5) | Note |
|---|---|---|
| thesis_clarity | 3 | Two theses (the lens; the long tail) joined by juxtaposition. The second hedges ("one explanation") right after an unhedged "is set by" |
| originality | 3 | The (q, w) split is importance sampling and the dataset-shift framing. The long-tail account is Hutter, Michaud, Feldman and Dohmatob. What is new is the synthesis and the exact checking, and the spec should say so |
| significance | 3 | Useful to the stated reader; not a new result |
| evidence | 3 | Sources are real and logged honestly by depth. "Is set by" outruns them, and the counter-accounts are missing from §2 |
| consistency | 2 | §2.1 says data needs are "set by" the tail; the chapter 11 row lists four factors. §1 says selection can "beat" the power law; §7's own selector is still a power law |
| assumptions | 3 | §7 names the oracle assumptions. §2.1 does not say the long-tail account assumes a memorization-like learner with deterministic labels |
| objections | 2 | §17 names the risk of presenting the long tail as *the* explanation, but §2 does not answer it. Manifold-dimension and variance-limited accounts and pruning's limits are absent |
| falsifiability | 4 | The falsifiability paragraph, Gate 1 on the signature figure, and "if the derivation does not hold up, record that" are exactly right |
| actionability | 4 | Phases, gates and test stubs make the next step cheap. Issue 1 gives a concrete figure change |

**Hard fails:** none. Near miss on *already-done*: chapter 13's selection argument on Hutter's
model overlaps Dohmatob et al. 2024 §§2–3 (issue 3). It is not a hard fail because the book does
not claim research novelty, but SPEC §4's claim 3 does claim distinctiveness and must be
reworded.

### What's strong (keep)

- **The data card (§2.2)** with *Fit on* and *Checked by*. The *Fit on* field quietly carries
  the leakage lesson. The worked example (log target, which under MSE estimates E[log y ∣ x]) is
  the right kind of claim: derivable, testable, and commonly misunderstood.
- **The falsifiability paragraph.** It names a case that does not fit (deduplication) instead
  of hiding it.
- **The §7 extension, stated as a conjecture to derive, with a revise-if-wrong clause.**
  A scratch computation supports it. With p_i ∝ i^−(α+1) on 10⁷ features, the log-log slopes of
  uniform sampling's exact error between n = 10³ and 10⁴ were −0.335, −0.500 and −0.666 for
  α = 0.5, 1, 2 (predicted −α/(1+α) = −0.333, −0.5, −0.667). For the frequency-ordered coverage
  selector they were −0.509, −1.000 and −2.000 (predicted −α).
- **The mirror with rl-for-llms Thesis 2.** Readers of both books get one idea twice, in two
  settings.

### Issues (ranked, most important first)

1. **The long-tail sentence merges two mechanisms, and "beat that law" overclaims.**
   §2.1: "Uniform sampling spends most of its budget on cases already learned, which is one
   explanation of power-law returns. Selection that targets what is not yet learned can do
   better." In Hutter's model the *power law* comes from the tail mass. Hutter writes that the
   expected error "is dominated by samples i′ for which θ_i′ ≈ 1/n" (§3). The *redundancy*
   explains why uniform sampling's exponent is α/(1+α) rather than α. The redundancy is real: in
   the scratch run, 70–95% of uniform draws had been seen before by n = 100. But a selector with
   zero redundancy is still a power law, n^−α, because what remains is the tail mass beyond
   coverage. Compare finite support with uniform θ: maximal redundancy, yet exponential decay
   (Hutter §3). So redundancy is neither necessary nor sufficient for a power law. Hutter's own
   caveat also belongs in the book: "we have no indication that our findings transfer."
   **Fix:** rewrite as "under a long-tailed p, error is the mass of what has not yet been seen.
   Uniform sampling reaches it slowly because most draws repeat what is covered. A selector that
   targets the uncovered steepens the power law (n^−α instead of n^−α/(1+α) on Hutter's model),
   but only with an oracle for what is covered." Panel B of the signature figure should show
   the oracle selector *and* a non-oracle one, for example a selector that estimates coverage
   from counts, so the gap between them is visible.

2. **"How much data a problem needs is set by how much probability mass sits in rare but
   necessary cases" overstates the case and contradicts chapter 11.** The chapter 11 row lists
   noise, target complexity, input dimension and rare-case mass. Two published accounts derive
   scaling exponents without a long tail: Sharma & Kaplan (2020) get α ≈ 4/d from regression on
   a data manifold of intrinsic dimension d, and Bahri et al. (2021) describe variance-limited
   and resolution-limited regimes. §17 already wants several accounts in chapter 13; the thesis
   should say so too. **Fix:** "...is, in memorization-like settings with long-tailed inputs,
   set largely by the mass in rare but necessary cases; noise and smoothness set it elsewhere
   (chapter 11)".

3. **The closest prior art is not cited: Dohmatob et al. 2024, "A Tale of Tails"
   (arXiv 2402.07043).** They analyze the "Hutter LLM" trained on samples from q and tested on
   p (their eq. 9, E_test = Σ_i p_i P(f̂(i) ≠ j_i)). Their results:
   - tail cutting at rank k gives E_test ≍ T^−(β−1)/β + k^−(β−1), so error plateaus (Thm 2.1);
   - finite sampling itself cuts the tail at k ≍ T₀^(1/β) (their eq. 6);
   - model collapse over generations;
   - mixing clean data ("grokking", Thm 3.2);
   - acquiring the missing tail: data "too deep" in the tail is worthless (§3.1).

   Their Zipf exponent is β with p_i ∝ i^−β, so β = α + 1 in Hutter's notation. This is SPEC
   claim 20 (model collapse on T2) and much of chapter 13's selection argument, already derived.
   **Fix:**
   - add it, plus Cabannes et al. 2023 (associative memories, arXiv 2310.02984), to Appendix A
     and chapter 13;
   - turn claim 20 into a check against their Thm 2.1/Cor 2.2 rates;
   - reword §4's claim 3 from "the long-tail account … is made computable" (the literature
     already did that) to "the long-tail account is reproduced exactly, in a form a practitioner
     can run, and connected to the data levers".

4. **q and w are not independent levers in expectation.** Reweighting by w and resampling with
   probabilities ∝ q·w target the same population objective. They differ in finite-sample
   variance, in duplicate examples, and in how they interact with SGD. Deduplication sits
   awkwardly for this reason, not by accident. "Which of the four a technique changes determines
   what it can fix" is therefore too strong for q vs. w: the *target* is set by the effective
   distribution q·w, and the q/w split sets the *variance*. Claims 10 and 12 already test both
   sides. **Fix:** state it in §2.1 and on the card. One option is an *Effective distribution*
   line under *Changes*, so that resampling and reweighting show the same target and different
   variance.

5. **The lens does not cover techniques that act on evaluation rather than training.** These
   include:
   - leakage and train-only fitting (chapter 4);
   - stratified and temporal splits (chapters 1, 3, 8);
   - shift *detection* (chapter 10);
   - learning-curve estimation (chapter 11);
   - test-set reuse (Recht et al.).

   They change what we *measure*, not what the model learns. Forcing them onto a lever is the
   "fits everything by being vague" failure the spec warns against. **Fix:** declare the
   four levers as levers on *training*. Give cards a *Changes* value of "evaluation only"
   (or "diagnostic"), and let *Fit on* carry the leakage lesson. This also bears on D1's open
   subtitle point: if the lens is about training, "Training Data" in the subtitle is accurate.

6. **"Selection can do better" needs its conditions.** Sorscher et al.'s exponential scaling
   assumes "a high-quality data pruning metric", and they report that most metrics "scale
   poorly to ImageNet". Ayed & Hayou (2023, arXiv 2302.06960) report that random pruning
   "outperforms most existing data pruning methods in the high compression regime" and prove
   no-free-lunch results for score-based pruning. Goyal et al. (2024, arXiv 2404.07177) show
   that the best filter depends on the training compute, because repeated high-quality data
   loses utility. **Fix:** cite these in §2.1's context and chapter 14, and label the
   selection claims *recent/contested* where they are about real models.

7. **The lineage of the (q, w) lens is only given as rl-for-llms.** Importance weighting for
   covariate shift and the dataset-shift taxonomy predate it (Moreno-Torres et al. 2012 is
   already in Appendix A). The earliest primary sources for importance-weighted risk under
   covariate shift still have to be found and read in Phase 3. **Fix:** a lineage callout on
   the lens, sourced in Phase 3.

8. **Phase 1 design notes for T2 (minor; Phase 1 owns them).**
   - Finite support bends the curves. In the scratch run with 10⁷ features, the coverage slope
     for α = 0.5 drifted to −0.532 by n = 10⁵. Size the support from n and α, or sum the tail
     analytically.
   - Hutter's constant c_α is derived for the unnormalized θ_i = α·i^−(α+1). Tests that compare
     with c_α must use the same normalization or rescale.

### Decisions for the author

1. **How strong should the long-tail sentence be?**
   - (a) Keep "is set by".
   - (b) Scope it to memorization-like settings, with the manifold and variance-limited
     accounts named. *Recommended (b);* §17 already asks for this.
2. **Chapter 13 framing, given Dohmatob et al.**
   - (a) Keep the long tail as the signature and present it as an exact reproduction plus the
     levers view, citing Hutter and Dohmatob.
   - (b) Move the signature to the lens itself, for example "resample vs. reweight vs.
     threshold: same target, different variance".

   *Recommended (a):* the figure is still the clearest picture of why returns diminish, and the
   reproduction is honest.
3. **Evaluation-side techniques:** add "evaluation only / diagnostic" as a *Changes* value
   (recommended), or keep the lens to four values and leave those techniques without a card.
4. **Subtitle (D1 open point):** with recommendation 3, the lens is about training data and the
   current subtitle is accurate. Recommended: keep "Training Data".

### Citations checked

| Reference | Verdict | Note |
|---|---|---|
| [Hutter 2021, arXiv 2102.04074](https://arxiv.org/abs/2102.04074) | ok | Full text read. E_n = Σ θ_i(1−θ_i)^n (eq. 2); Zipf θ_i ∝ i^−(α+1) gives β = α/(1+α) with c_α = α^(1/(1+α)) Γ(α/(1+α))/(α+1); finite support decays exponentially; skewed non-Zipf distributions give "uninteresting" β = 1; error dominated by θ_i ≈ 1/n; "no indication that our findings transfer" |
| [Dohmatob et al. 2024, arXiv 2402.07043](https://arxiv.org/abs/2402.07043) | ok (new; not in SPEC) | Full text, §§1–3 read. Hutter LLM under q ≠ p; Thm 2.1 tail cutting; eq. 6 k ≍ T₀^(1/β); Thm 3.2 mixing; §3.1 acquiring the missing tail |
| [Sorscher et al. 2022, arXiv 2206.14486](https://arxiv.org/abs/2206.14486) | ok | Abstract (passage-level entry already in research-log): exponential scaling "if we have access to a high-quality data pruning metric"; most metrics "scale poorly to ImageNet" |
| [Bahri et al. 2021, arXiv 2102.06701](https://arxiv.org/abs/2102.06701) | ok | Abstract: variance-limited and resolution-limited regimes; resolution-limited explained by "resolving a smooth data manifold" |
| [Michaud et al. 2023, arXiv 2303.13506](https://arxiv.org/abs/2303.13506) | ok | Abstract: quanta learned in order of use frequency; a power law in frequencies explains power-law loss; LLM evidence "tentative" |
| [Sharma & Kaplan 2020, arXiv 2004.10802](https://arxiv.org/abs/2004.10802) | ok (new) | Abstract: α ≈ 4/d from regression on a data manifold of intrinsic dimension d. Note: that abstract's α is a scaling exponent in parameters N, unrelated to Hutter's α |
| [Ayed & Hayou 2023, arXiv 2302.06960](https://arxiv.org/abs/2302.06960) | ok (new) | Abstract: random pruning beats most methods at ≤ 30% kept; no-free-lunch theorems for score-based pruning |
| [Goyal et al. 2024, arXiv 2404.07177](https://arxiv.org/abs/2404.07177) | ok (new) | Abstract: data curation "cannot be agnostic of the total compute"; repeated high-quality data loses utility |
| [Cabannes et al. 2023, arXiv 2310.02984](https://arxiv.org/abs/2310.02984) | ok (new) | Abstract: scaling laws for associative memories, in sample and parameter size |
| rl-for-llms Thesis 2 (`../rl-for-llms/CONVENTIONS.md`) | ok | "almost every method is a choice of sampling distribution q and per-sample weight w" |
| Duan 1983 | unreachable at content level | Bibliographic data only (Crossref, in research-log); content still to be read in Phase 2, as SPEC says |

**Recommendation:** revise. The lens and process are sound. Make issues 1–5 textual changes to
§2.1, §2.2 and §4 before Phase 1, so that the signature figure is designed to test the corrected
claim rather than the overstated one.

### Round 1 resolution (2026-10-04)

The owner accepted the recommendations for decisions 1–4. SPEC v0.2 applies issues 1–5:
§2.1 is reworded; the card gains *evaluation only*; §4 claim 3 is reworded; and Dohmatob et
al., Sharma & Kaplan, Ayed & Hayou, Goyal et al. and Gerstgrasser et al. are added to
Appendix A. Issue 6 (selection's conditions) is carried into chapters 13–14. Issue 7 (lens
lineage) is scheduled for Phase 3. Issue 8 (T2 design) is handled in Phase 1.
