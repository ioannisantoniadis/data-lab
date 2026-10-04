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

## Phase 1: testbeds and the signature figure: in progress (started 2026-10-04)

- Implement T1–T5 with their tests; size T2's support from n and α (`review.md` issue 8).
- Derive and test §7's coverage-selection extension, including a non-oracle selector.
- Claims 14–16 unskipped.
- Signature figure; look at it. ⛳ Gate 1.
- Social-preview image (generated, like any figure), added only once D5 allows a public site.

## Phase 2: Parts I and II: planned

Chapters 1–7; claims 1–9 and 21. Fresh-agent audit after chapter 7. ⛳ Gate 2.

## Phase 3: Parts III and IV: planned

Chapters 8–14; claims 10–13 and 17–20. `skeptical-review` of chapter 13. ⛳ Gate 3.

Note: SPEC §8 says "Phase 2 makes them pass", but claims 10–20 belong to Part III and IV
chapters, which SPEC §15 schedules for Phase 3. Each stub is skipped with the phase of its
chapter; claims 14–16 are Phase 1.

## Phase 4: synthesis and release: planned

Chapter 15, the Map, the appendices, the final audit, the success tests. Publication per D5.

## Durations

| Phase | Started | Gate reached |
|---|---|---|
| 0 | 2026-10-04 | 2026-10-04 |
| 1 | 2026-10-04 | |

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
