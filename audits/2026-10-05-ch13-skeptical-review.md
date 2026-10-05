# Skeptical review of chapter 13 (2026-10-05)

Run by a fresh agent with the `skeptical-review` skill on the Phase 3 draft of
`docs/chapters/13-why-power-laws.qmd`. The review is reproduced unchanged below; the resolution
follows it.

# Skeptical review: chapter 13, *Why Power Laws: The Long Tail*

Reviewed with the `skeptical-review` skill. What I read: the chapter; `docs/appendix-testbeds.qmd`
§T2; `src/data_lab/testbeds/t2_zipf.py`; `tests/test_long_tail.py`;
`scripts/figures/fig_long_tail_signature.py`; the `ch13` namespace of `docs/_variables.yml`;
the coverage-selection card; the signature figure (looked at); SPEC §2.1 and §7; the
research log; and the earlier thesis review (`review.md`). I opened the full text (PDF) of all
seven primary sources. I ran the tests and my own checks in a scratch copy of the repo
(`scratchpad/review-copy`, `scratchpad/check.py`, `scratchpad/check2.py`). Nothing under the
repo was modified.

## Round 1 — 2026-10-05 (reviewing chapter 13, working tree on top of 5d5e27b)

### Verdict

This is a careful, honest chapter. Every quote I checked is accurate, every published number
reproduces, and the 20 tests pass. It now separates the two mechanisms the thesis review said
it was merging: the tail makes the curve a power law, and redundancy only makes it shallow.
It also shows an oracle selector next to a selector that has no oracle. Its headline, though,
says that coverage selection "steepens" the exponent from α/(1+α) to α, and that is mostly a
change of what gets counted, not something selection buys. Suppose a learner labels each
*distinct* case from an ordinary uniform stream, and never labels a repeat. Its error,
counted in labels, already falls as n^−α, within a factor of 1.46–1.66 of the oracle
(α = 0.5–2). Counted in draws, no selector without an oracle beats α/(1+α). The pool selector
in Panel B also leaves most of its labeling budget unspent at M = 10n and M = 100n, so the
"labeled examples" axis overstates what it used. The chapter deserves its reader's attention.
It should revise its central framing before it is accepted as the signature chapter.

### Scores

| Criterion | Score (1–5) | Note |
|---|---|---|
| thesis_clarity | 4 | The result callout is sharp and falsifiable. The cost axis behind "steeper" (labels vs. draws) is left implicit |
| originality | 3 | It is honest that the oracle rate is Michaud's eq. 2. The pool bound restates Dohmatob et al.'s finite-sample tail cut without crediting it |
| significance | 3 | A clear, exact teaching model of diminishing returns; meaningful for the stated reader |
| evidence | 4 | All 7 sources verified; numbers are tested and reproduce. Missing: the spectral accounts and 2025–26 work on where language-model exponents come from |
| consistency | 3 | "Labels the top n" is false for the M = 10n and 100n pools. The unscoped "selection cannot escape the power law" will clash with chapter 14's Sorscher result. It forward-cites a stub ("Choosing Data reproduces it") |
| assumptions | 3 | Three assumptions are listed well. The load-bearing one is hidden: that uniform sampling pays a label for every repeat |
| objections | 3 | Five competing accounts get one line each. The strongest current ones (spectral; Cagnetta et al. 2026) and Michaud's own non-coverage mechanism are absent |
| falsifiability | 3 | Inside the toy, everything is tested. For real systems there are no signposts, such as Michaud's α_D = α_N/(α_N+1), or a measured case-frequency exponent that predicts the data exponent |
| actionability | 3 | "The pool must grow like n^(1+α)" is concrete. The practitioner's takeaway (deduplicate first; ordering buys a constant) is missing |

**Hard fails:** none. No citation is fabricated or misrepresented. There is a near miss on
*already-done* for the pool-selector bound (issue 4). It is not a hard fail, because the book
claims reproduction, not research novelty.

### What's strong (keep)

- **The decomposition, stated plainly** (lines 42–56, and the failure mode "Mistaking redundancy
  for the cause"). This fixes the thesis review's issue 1 exactly: the power law comes from the
  tail mass, the shallow exponent comes from redundancy, and "remove all redundancy and the tail
  remains."
- **The pool selector and its bound** (lines 75–85; appendix T2): E[error] ≥ max(oracle_n, E_M).
  I checked the proof and it is correct: the unlabeled set contains everything absent from the
  pool, and everything beyond the n cases it labels. The tie-breaking test
  (`test_pool_selector_ties_are_not_broken_by_index`) is the kind of care that makes a toy
  trustworthy. I re-ran the M = n^(1+α) claim at α = 0.5 (M = n^1.5, n = 100 to 10⁴): slope
  −0.499, 1.41× the oracle. At α = 2 (M = n³, n = 30 to 100): slope −2.007, about 1.5× the
  oracle. The claim generalizes beyond the α = 1 that is tested.
- **The Michaud paragraph** (lines 65–71). It is correct to the equation (their eq. 2 and the
  τ-threshold derivation of α_D = α/(α+1), §2), and it is honest: "This rate is not new."
- **The exact machinery.** It brackets the sum instead of truncating it, uses a coefficient
  generalized for the normalized p (tested to 0.1%), and checks Monte Carlo against the exact
  sum over 400 seeds. All 8 `ch13` variables reproduce: 0.02184, 0.000608, 86.7%.
- **The scope paragraph** ("What the toy cannot show"), and the hedged closing sentence on which
  account dominates.

### Issues (ranked, most important first)

1. **The "steeper exponent" is mostly a change of cost axis, and deduplication alone gets
   it.** The chapter compares uniform sampling and selection at an equal number of *labels*.
   But under its own assumption 3 (cases are exact identities), a repeat never needs a new
   label. If you label only the distinct cases of a uniform stream of M draws, the number of
   labels is D(M) ∝ M^(1/(1+α)) (Heaps' law), and the error is E_M ∝ M^(−α/(1+α)) ∝ D^(−α).
   The oracle's exponent α is therefore the exponent of error in *distinct cases covered*, and
   ordinary deduplication reaches it. Computed exactly with the repo's `ZipfStream` between
   M = 10⁵ and 10⁶:

   | α | slope of E_M against D(M) | E_M ÷ oracle error at the same label count |
   |---|---|---|
   | 0.5 | −0.500 | 1.46 |
   | 1 | −0.999 | 1.57 |
   | 2 | −1.988 | 1.66 |

   So at 1,000 labels the chapter's 36× gain, from 0.0218 to 0.00061, splits into about 23×
   from not paying for repeats and only about 1.57× from frequency ordering. Measured in
   *draws* (unlabeled data, compute or tokens), the chapter's own bound E ≥ E_M means that no
   selector without an oracle beats n^(−α/(1+α)). The callout ("A selector that covers the
   most frequent cases first reaches n^−α"), the card ("the error falls as n^−α instead of
   n^−α/(1+α)") and the Panel B title ("Coverage steepens it") all credit selection with what
   is really an accounting change. This is the most useful correction the chapter can make.
   The true statement is sharper and more practical.

   **Fix:** state both axes.
   - Per draw, the exponent is α/(1+α) for every selector that does not know p.
   - Per distinct label, it is α for deduplication alone; frequency ordering adds a constant
     factor (about 1.5 on this model), and an oracle adds nothing more to the exponent.

   Then:
   - add a "uniform + dedup" curve to Panel B, or a second x-axis for draws;
   - add a test (slope of E_M against D(M) → −α, and the ratio in the table above);
   - reword the callout, the card's *What it does* field and the Panel B title;
   - cite Heaps' law: Dębowski 2025 derives it from Zipf in exactly this chain; see also
     Gnedin, Hansen and Pitman 2007.

2. **The pool selector at M = 10n and 100n does not spend its budget, so Panel B's x-axis and
   "labels the top n" are wrong in that regime.** Expected distinct cases in the pool, at α = 1:

   | Budget n | M = 10n | M = 100n | M = n² |
   |---|---|---|---|
   | 1,000 | 138 (13.8% of n) | 437 (44%) | 1,381 (full budget) |
   | 2,000 | 195 (9.7%) | 617 (31%) | 2,764 (full budget) |

   In my Monte Carlo run with M = 10n, the selector actually labeled 43 cases at n = 100 and 137
   at n = 1,000. At the labels it actually used, its error was 1.58× and 1.57× the oracle's,
   on the oracle's own slope. The code's docstring says this ("the rest of the budget is
   unusable"), but the chapter and the caption do not. There is also an exact statement the
   chapter misses: once the pool has fewer than n distinct cases, the selector labels all of
   them, and its expected error *equals* E_M. That is stronger than the measured slope
   "−0.49". **Fix:** say it in the text, and state and test the equality. Plot Panel B against
   labels actually used, or mark where each pool line becomes pool-limited.

3. **The theorem behind "not an escape" is not stated, and the unscoped failure mode will
   contradict chapter 14.** On this model, any selector that labels n cases has error at least
   Σ_{i>n} p_i, because the n labeled cases carry at most the mass of the top n. So the oracle
   is *optimal*, and the power law is a lower bound for every selector. That is a one-line
   proof, stronger than "the oracle is still a power law", and the chapter only implies it. On
   the other side, "Expecting selection to escape the power law" is stated as a general failure
   mode. Sorscher et al. (2022), whose T3 setting the book uses in chapter 14, show exponential
   scaling with a perfect pruning metric. **Fix:** state the optimality bound, and scope the
   failure mode: "on a memorizing learner with a long tail, no selection escapes the power
   law; for learners that generalize, see chapter 14 (Sorscher et al.)."

4. **The earlier review's issue 3 is only partly fixed: Dohmatob et al. are credited for
   model collapse but not for the pool argument.** Their eq. 6 and Corollary 2.2 say that an
   i.i.d. sample of size T₀ supports only the ranks k ≍ T₀^(1/β), so E ≍ T^(−c) + T₀^(−c) with
   c = 1 − 1/β = α/(1+α). That is the chapter's pool bound in another form (pool M ↔ T₀).
   Their §3.1, "Acquiring Missing Tail" (Theorem 3.1), is a selection result on the same
   model: buying tail data "too deep" is "worthless". There are four further gaps:
   - SPEC §7 says chapter 13 "cites it and checks against it", but there is no test against
     their rates;
   - "Choosing Data reproduces it" (line 129) points at a stub;
   - Hutter himself notes that his model "formally is equivalent to the model in [Cha81]"
     (Chao 1981, species discovery), and E_n is the expected missing mass of the classical
     occupancy problem (Good–Turing; Karlin; Gnedin, Hansen and Pitman 2007). None of that
     lineage appears;
   - Cabannes et al. 2023 is in the bibliography but not in the chapter.

   **Fix:** one sentence after the pool result: "Dohmatob et al. derive the same truncation
   for a finite sample (their eq. 6, Cor. 2.2)." Add a test against Cor. 2.2. Change "reproduces
   it" to future tense until chapter 14 exists. Add a lineage line on missing mass and
   occupancy.

5. **The competing accounts omit the strongest current ones.** The list covers the manifold,
   Bahri, Feldman, Kandpal and Michaud, and stops at 2023. It is missing:
   - **The spectral / random-feature account:** power-law eigenspectra give power-law data
     scaling. It is in Maloney, Roberts and Sully (2022); Bordelon, Atanasov and Pehlevan
     (2024); Paquette, Paquette and Xiao (2024); and Lin, Wu and Kakade (2024), where the
     error is Θ(M^−(a−1) + N^−(a−1)/a) for a power-law spectrum of degree a. It is arguably
     the dominant theoretical account of 2022–2025. It is also a "tail" (of eigenvalues),
     which is worth saying.
   - **Michaud et al.'s own single-epoch mechanism (§2):** the same exponent α/(α+1) arises
     because steps to learn quantum k scale as 1/p_k. That is an optimization bottleneck, not
     a coverage one, and coverage selection would act on it differently.
   - **Counter-evidence and new evidence, 2025–26:**
     - Cagnetta, Raventós and Ganguli (2026, arXiv 2602.07488) claim "the first such theory":
       data-limited exponents of GPT-2- and LLaMA-style models predicted with no free
       parameters, from the decay of token correlations and of conditional entropy, with no
       unseen-case tail.
     - Dębowski (2025, 2512.13491) derives neural scaling from Zipf via Heaps' law and
       Hilberg's hypothesis.
     - Brill (2024, 2412.07942) unifies the "discrete subtasks" and "data manifold" regimes
       using percolation theory.
     - On the supporting side, Ye, Feldman and Talwar (2026, 2604.08519) show that data
       selection which flattens fact frequencies raises fact memorization (1.3× more facts in
       GPT-2 Small). That is real-model evidence close to this chapter's selector.

   "As of October 2026, which account dominates … is an open question" is defensible, but it
   should cite these. **Fix:** add a bullet for the spectral account, a sentence on Michaud's
   single-epoch mechanism, and two dated sentences on Cagnetta et al. and Ye et al.

6. **The earlier review's issue 6 (the conditions under which selection works) is not
   addressed here; it is deferred to a stub.** Line 112 says removing redundancy and
   targeting the uncovered "can change the curve", without qualification. Chapter 14 is empty,
   so a reader of chapter 13 gets none of these:
   - Sorscher et al.'s condition of "a high-quality data pruning metric";
   - Ayed and Hayou's result that random pruning beats most methods at high compression;
   - Goyal et al.'s finding that the best filter depends on compute.

   Kazdan et al. (2026, 2603.06603) add that what counts as a duplicate depends on the scale
   of the model. That bears directly on assumption 3. **Fix:** one paragraph with these
   citations, labeled *recent/contested*, and assumption 3 linked to Kazdan et al.

7. **The α the chapter illustrates is far from text.** Assumption 2 ties the model to word
   frequencies. But every quantitative example is at α = 1 (p_i ∝ i^−2), and the classical
   word-frequency Zipf exponent is near s = 1, that is α near 0, where the uniform exponent
   α/(1+α) is close to 0. I have not re-verified that exponent against Piantadosi here; check
   chapter 3's source. Michaud et al. tie α to the empirical language-model
   parameter exponent (abstract), which is small; I did not re-verify its value here. **Fix:** say what α a text-like tail implies, and add a small α (for example 0.1) to
   Panel A, or note why α = 1 is used.

8. **Minor.**
   - **Pool tests only at α = 1.** Tests of the pool exponent run only at α = 1, where
     n^(1+α) = n², so they cannot tell "n^(1+α)" from "n²". My α = 0.5 and α = 2 runs
     (above) pass; add them.
   - **Hutter quote context.** Hutter's "no indication that our findings transfer" refers to
     two other modeling routes: scaling the model with data, and non-parametric models. It
     is close to the chapter's use, but say so.
   - **Toy-to-real overreach.** "That is why averages improve slowly while specific rare cases
     flip" (line 110) states a toy result as a fact about real models. Write "In this model,
     …".
   - **Research log depth.** The log records Michaud, Feldman and Kandpal at abstract depth,
     but the chapter cites Michaud's eq. 2 and §2. I verified them; log the passage-level
     read.
   - **Panel A whitespace.** Panel A's x-axis runs to 3×10⁸ while the data end at 10⁶, which
     wastes about a third of the panel on label room.

### Decisions for the author

1. **What does the chapter claim selection buys?**
   - (a) Keep "coverage steepens the exponent", and add the axis caveat.
   - (b) Reframe: the exponent depends on what you count. Per draw, it is α/(1+α) for anything
     without an oracle. Per label, deduplication alone gets α, and frequency ordering is worth
     a constant (about 1.5×).

   *Recommended (b).* It is true on the page's own model, it gives practitioners a concrete
   rule (deduplicate first; ranking buys a constant), and it is a cleaner signature result
   than the current one. It means changing Panel B, which SPEC §9 owns, so it is your call.
2. **How much space do competing accounts get?**
   - (a) A bullet each for the spectral account and the 2026 language-model-statistics
     paper, plus Michaud's single-epoch sentence. *Recommended.*
   - (b) A full subsection steelmanning the spectral account. This costs words against the
     35k cap.
3. **Forward references to chapter 14.** Either write chapter 14's model-collapse
   reproduction before chapter 13 is accepted, or reword chapter 13's references to it as
   future work. *Recommended: reword now.* SPEC §13 acceptance needs "no unresolved major
   issue", and a citation to a stub is one.
4. **Originality positioning of the pool selector.** Present it as a reproduction of
   Dohmatob et al.'s finite-sample truncation applied to selection (*recommended*), or as the
   book's own extension with that citation alongside.

### Citations checked

| Reference | Verdict | Note |
|---|---|---|
| [Hutter 2021, arXiv 2102.04074](https://arxiv.org/abs/2102.04074) | ok | Full text. Eq. 2: EE_n = Σ θ_i(1−θ_i)^n. §3: "the expected error (2) is dominated by samples i′ for which θ_i′ ≈ 1/n". Zipf θ_i ∝ i^−(α+1) gives β = α/(1+α). §1: "we have no indication that our findings transfer", said of model-scaling and non-parametric routes. §2 notes the model's formal equivalence to Chao 1981 (not mentioned in the chapter). No selection or active-learning analysis |
| [Michaud et al. 2023, arXiv 2303.13506](https://arxiv.org/abs/2303.13506) | ok | Full text. Eq. 2: L_n ≈ a + (b−a)/(αζ(α+1)) n^−α, matching the chapter exactly. §2: τ-threshold data scaling n ∝ (D/τ)^(1/(α+1)), so α_D = α/(α+1), and α_N = α. Abstract: "We tentatively find…", quoted accurately. They also give a single-epoch mechanism (steps ∝ 1/p_k), not in the chapter. They call Hutter "the closest prior work" |
| [Dohmatob et al. 2024, arXiv 2402.07043](https://arxiv.org/abs/2402.07043) | ok (under-credited) | The plateau from tail cutting on the Hutter LLM is Thm 2.1, as cited. Not credited: eq. 6 and Cor. 2.2 (a finite sample cuts the tail at k ≍ T₀^(1/β)), which match the chapter's pool bound, and §3.1/Thm 3.1, which is selection of tail data |
| [Sharma & Kaplan 2020, arXiv 2004.10802](https://arxiv.org/abs/2004.10802) | ok | Abstract: L ∝ N^−α, with "α ≈ 4/d" from "regression on a data manifold of intrinsic dimension d". The chapter's "parameter-scaling" is correct. Worth adding: their language-model section (p. 14) finds language modeling does not confirm 4/d ("it would have been more exciting to discover α ≈ 4/d for language modeling") |
| [Bahri et al. 2021, arXiv 2102.06701](https://arxiv.org/abs/2102.06701) | ok | Abstract: variance-limited "from the existence of a well-behaved infinite data or infinite width limit"; resolution-limited from "resolving a smooth data manifold"; also linked to kernel spectra |
| [Feldman 2019, arXiv 1906.05271](https://arxiv.org/abs/1906.05271) | ok | Abstract: "memorization is necessary whenever the distribution of subpopulation frequencies is long-tailed". "This is the learning-theoretic face of the same tail" is the author's gloss, which is reasonable |
| [Kandpal et al. 2022, arXiv 2211.08411](https://arxiv.org/abs/2211.08411) | ok | Abstract: "a language model's ability to answer a fact-based question relates to how many documents associated with that question were seen during pre-training", quoted exactly |
| [Cagnetta, Raventós, Ganguli 2026, arXiv 2602.07488](https://arxiv.org/abs/2602.07488) | ok (new; counter-account) | Abstract: the first theory to predict data-limited exponents for modern language models, with no free parameters, from token-correlation decay and conditional-entropy decay |
| [Dębowski 2025, arXiv 2512.13491](https://arxiv.org/abs/2512.13491) | ok (new; supporting) | Abstract: Zipf → Heaps → Hilberg → neural scaling |
| [Brill 2024, arXiv 2412.07942](https://arxiv.org/abs/2412.07942) | ok (new) | Abstract: percolation model; two regimes, discrete power-law subtasks and a dominant manifold |
| [Ye, Feldman, Talwar 2026, arXiv 2604.08519](https://arxiv.org/abs/2604.08519) | ok (new; supporting) | Abstract: frequency-flattening data selection gives 1.3× more facts memorized (GPT-2 Small) |
| [Kazdan et al. 2026, arXiv 2603.06603](https://arxiv.org/abs/2603.06603) | ok (new) | Abstract: semantic duplicates act increasingly like exact duplicates as models scale; bears on assumption 3 |
| [Maloney et al. 2022, arXiv 2210.16859](https://arxiv.org/abs/2210.16859); [Bordelon et al. 2024, 2402.01092](https://arxiv.org/abs/2402.01092); [Paquette et al. 2024, 2405.15074](https://arxiv.org/abs/2405.15074); [Lin et al. 2024, 2406.08466](https://arxiv.org/abs/2406.08466) | ok (new; missing account) | Abstracts: solvable random-feature and linear models with power-law spectra produce data and parameter scaling laws |
| [Gnedin, Hansen, Pitman 2007, arXiv math/0701718](https://arxiv.org/abs/math/0701718) | ok (new; lineage) | Abstract: the occupancy scheme with infinitely many boxes, power laws and regular variation. This is the classical home of D(n) and the missing mass |

**Recommendation:** revise. The mathematics and the evidence are sound, but the headline
("coverage selection steepens the exponent") credits selection with what is mostly a change
from counting draws to counting distinct labels. The pool panel also overstates the labels
it used. Both are fixable with one new curve, one new test and a reworded callout.

---

## Resolution (2026-10-05)

- **Issue 1 (per label vs per draw): fixed.** Verified exactly: labeling each new case from a
  uniform stream has per-label slope −α (−0.499, −0.998, −1.996 at α = 0.5, 1, 2) at
  β Γ(β)^(1+α) times the oracle's error (1.46, π/2, 1.66; derived in the T2 appendix), after
  about n^(1+α) draws. The chapter now separates the two axes; Panel B plots error against
  labels used and adds the exact "uniform, new cases only" curve; the coverage card is restated.
  Tests: `tests/test_long_tail.py::test_deduplicated_stream_*`.
- **Small pools never spend the budget: fixed** (`::test_small_pool_cannot_spend_its_budget`).
- **Optimality bound stated; "no escape" scoped to memorizing learners: fixed**
  (`::test_any_n_labels_cost_at_least_the_tail_mass`).
- **Dohmatob et al. credited for the pool bound (eq. 6, Cor. 2.2): fixed.**
- **Competing accounts:** Maloney et al. 2022 and Cagnetta et al. 2026 added after verifying
  their abstracts; Michaud's §2 read at passage depth (multi-epoch and single-epoch data
  scaling) and logged.
- **α illustrative; Hutter's "no indication" quote put in context: fixed.**
- **Panel A x-range trimmed: fixed.**
- **Chapter 14 written,** so the forward reference resolves to real content.
- **Panel B reframing:** applied as a correctness fix; flagged for the owner at Gate 3 because
  SPEC §9 describes the signature figure.
