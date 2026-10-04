# Authoring conventions for data-lab

This file is the single source of truth for *how* chapters are written. `SPEC.md` is the
conceptual contract; this file turns it into mechanics. Read `docs/appendix-notation.qmd` first
(it defines every symbol), then this file. It is adapted from `rl-for-llms/CONVENTIONS.md` (the
process reference) and the portability rules of `objectives-book` SPEC §21.1 (DECISIONS D6).

Not part of the rendered book.

## What this book is, in one paragraph

Not a catalogue of preprocessing tips. One argument: a model learns the distribution it is
trained on, through the representation it is given. Every data technique changes one or more of
four levers: the **representation**, the **sampling distribution $q$** compared with the target
distribution $p$, the **per-example weights $w$**, or the **labels**. Which lever it pulls
determines what it can fix and what it can break. Resampling and reweighting
target the same population objective and differ in variance. Techniques that act only on
evaluation pull no lever, and their cards say *evaluation only*. Part IV asks how much data a
problem needs, and why returns diminish. Where learning is memorization-like and inputs are
long-tailed, error is the mass of what has not yet been covered. Uniform sampling reaches it
slowly, because most draws repeat what is covered; an oracle selector steepens the power law
but does not escape it. Other accounts of power laws are presented alongside (SPEC v0.2 §2.1).

## Standing rules

1. **Research first; never write from memory.** Equations, library defaults, reported results,
   dates and author lists come from the primary source or official documentation. Open it,
   read it, and log it in `research-log.md` with its depth (bib / abstract / passage). Search
   for later work that corrects or disputes each source.
2. **Every checkable statement is a test** in `tests/`, named after the claim. **Every figure is
   a script** that imports `data_lab`, and every image is looked at after every change.
3. **Scope test for every paragraph:** does it help the reader decide what to do with data, or
   understand why a data technique works? If not, cut it or link the sibling that owns the
   topic (SPEC §3 non-goals, §4 ownership table).
4. **Library behavior is checked, not recalled** (SPEC §12.5). When the book says what a
   scikit-learn transformer does, a test exercises the installed version against the
   derivation.

## Chapter file and first line

`docs/chapters/NN-slug.qmd`. There is no YAML title. The first line is the chapter heading with
its Quarto ID:

```markdown
# Changing the Shape {#sec-shape}
```

The ID is what cross-references target. A test (`tests/test_tooling.py`) checks every chapter
for it. The Map is `{#sec-map .unnumbered}`, so that chapter numbers match SPEC §5 (1–15).

## The chapter template (SPEC §10)

1. **Motivating problem**, no heading: the practical question, and which earlier limitation
   motivates it.
2. `## The problem`
3. `## Assumptions`: each assumption, and what breaks if it fails.
4. `## Derivation or demonstration`
5. **The boxed result**: `::: {.callout-note title="Result: <name>"}`, then **the data card**
   (below).
6. `## What it does to the learned model`: in terms of the loss's minimizer, on which
   distribution ($p$ or $q$) and which scale (original or transformed).
7. `## Failure modes`: with at least one computed figure.
8. `## What the toy cannot show`
9. `## Connections`: 2–4 links, each with *why*.

The Map and the decision guide may deviate, but never drop *Connections*. Chapters are
1,200–2,200 words of prose (`scripts/word_count.py` reports each one).

## Data cards

Every technique gets a card: a `callout-tip` *generated* from its record in
`scripts/technique_data.py` and included right after the result box:

```markdown
{{< include ../includes/cards/<slug>.md >}}
```

The fields are fixed, in this order: **Changes · Assumption · What it does to the learned
function · Which models care · Fit on · Failure modes · Alternatives · Checked by**. Never edit
`docs/includes/`; edit the record and run `uv run python scripts/technique_data.py`. CI fails if
the committed includes are stale.

- **Lever tags:** `levers` is a non-empty subset of representation / q / w / labels, or
  exactly `["evaluation"]` for a technique that acts only on evaluation (drawn in
  `EVALUATION_COLOR`, a neutral). If a
  technique pulls more than one (deduplication changes both $q$ and the effective weights), the
  card says so, and the prose explains why. That is the lens's falsifiability, not a defect.
- **Status:** a record is `draft` until every field is sourced and its test passes, then
  `verified`. Draft cards render with "(draft: not yet verified)" in the title.

## Callouts

| Callout | Use | Title pattern |
|---|---|---|
| `callout-note` | The boxed result of a derivation | `Result: <name>` |
| `callout-tip` | Data cards (generated only) | `Data card: <technique>` |
| `callout-note` | Practitioner box: the library call that does what was derived, and the parameter that matters. Never a substitute for the derivation | `In practice` |
| `callout-important` | Lineage: a technique reuses an older idea (importance sampling, the (q, w) view of rl-for-llms) | `Lineage: this is <idea>` |
| `callout-warning` | Stubs only; removed when the chapter is written | `Stub` |

Collapsed callouts never hold essential content (objectives-book SPEC §21.1, rule 4).

## Evidence labels

Every empirical claim is one of three kinds, and the prose says which:

- **Mathematical fact**: derived here or proved in a cited source. Stated plainly.
- **Replicated finding**: several independent groups report it. "Several groups report …",
  with citations.
- **Recent or contested**: one paper, a vendor, or an open debate. "The paper reports …",
  dated ("as of October 2026"), with the counter-evidence.

Scaling-law and data-selection content is mostly the second and third kinds (SPEC §10). A toy
result is never stated as a real-scale result. Every chapter's *What the toy cannot show*
exists for this.

**"Checked by" notes:** every checkable statement names its test, for example
`tests/test_transforms.py::test_log_target_mse_predicts_geometric_mean`.

## Distinctions never to blur

- **$p$ vs. $q$**: the target distribution vs. the training distribution. Every expectation
  says which.
- **Original scale vs. transformed scale**: a prediction, an error or a mean is always placed
  on one of them.
- **Fit on training data vs. fit on everything**: every fitted transform says what it was fit
  on (the card's *Fit on* field).
- **Data-rich vs. data-scarce regime**: pruning and augmentation results flip between them.
- **Resampling vs. reweighting**: the same population target and different finite-sample
  variance (`review.md` issue 4).
- **Changing what the model learns vs. changing what we measure**: splits, leakage and shift
  detection act on evaluation (`review.md` issue 5).
- **A steeper power law vs. escaping the power law**: coverage-driven selection on T2 changes
  the exponent; it is still a power law (`review.md` issue 1).
- **Tail cutting vs. tail narrowing** of a generated distribution (Dohmatob et al. 2024).
- **Replace vs. accumulate** in model collapse (Gerstgrasser et al. 2024).
- **MCAR vs. MAR vs. MNAR**; **covariate vs. prior vs. concept shift**; **label-preserving vs.
  label-changing augmentation**.
- **Mathematical fact vs. replicated finding vs. contested claim.**

## Math, code and citation mechanics

- Inline `$…$`, display `$$…$$`, standard LaTeX only (no MathJax-only extensions). Use only
  symbols in `docs/appendix-notation.qmd`; a new symbol is added there in the same change. In
  tables, write `\lvert … \rvert`, never a bare `|` inside math.
- **Quarto does not execute code.** Fenced `python` blocks are short display excerpts of the
  real code in `src/data_lab/`, at most 80 characters wide (checked in CI).
- **Citations:** `[@key]` against `docs/references.bib`. Entries are generated from the arXiv
  and Crossref APIs, never typed from memory. Every entry has a DOI or arXiv `eprint`.
- **Cross-references:** by title and link, targeting the Quarto ID, as in
  `[Changing the Shape](06-changing-the-shape.qmd#sec-shape)`. Figures and equations use
  `@fig-…` and `@eq-…`. Never type "Chapter 6" in prose; CI flags it. Generated tables may
  print chapter numbers.
- **Dates:** anything frontier says "as of ⟨Month YYYY⟩".
- **Portability** (objectives-book SPEC §21.1): no raw HTML or CSS in chapters; no emoji;
  reasonable widths; figures are PNGs written through `save_figure`.
  `scripts/check_portability.py` enforces what can be checked mechanically.

## Figures

- One script per figure: `scripts/figures/fig_<slug>.py`. It imports the shared theme and
  `data_lab`, and ends with `save_figure(fig, "<slug>")`, which writes `docs/images/<slug>.png`
  at 200 dpi:

  ```python
  import sys
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).resolve().parent))
  from _theme import LEVER_COLOR, REFERENCE_COLOR, apply_theme, save_figure

  apply_theme()
  ```

- The docstring ends with "this figure makes visible that …".
- **Color is semantic.**
  - Lever figures use `LEVER_COLOR`: representation blue, $q$ orange, $w$ aqua, labels violet.
    These were validated with the dataviz validator; see `_theme.py`.
  - Exact ground truth is `REFERENCE_COLOR` (ink).
  - Otherwise, index `CATEGORICAL` in its fixed order. The theme's default color cycle is a
    single gray, so a forgotten color shows up as an error rather than as a silently cycled
    hue.
- Every multi-series figure has a legend *and* direct labels or distinct line styles (aqua is a
  contrast WARN).
- Fixed seeds. When a claim is about typical behavior, show the spread over seeds (median plus
  a band), and the text says how many seeds show the effect.
- Embed with an ID and a caption that states the lesson:
  `![What is plotted. The lesson.](../images/<slug>.png){#fig-<slug>}`.
- Run the script and **look at the PNG** before the chapter counts as done.
- Every script runs in under a minute on a laptop CPU, with no network access (SPEC §7).

## Code

- `src/data_lab/` uses NumPy, SciPy, scikit-learn and matplotlib only. Audio uses a NumPy/SciPy
  short-time Fourier transform, with no audio library.
- Tests check claims numerically against ground truth: a closed form, exact summation, or a
  reference library on the same inputs. Seed-dependent claims test the multi-seed statistic
  the text quotes.
- Tests are bounded in time (`pytest-timeout`, 120 s default) and memory.
- `uv run ruff check .`, `uv run pytest`, `uv run python scripts/word_count.py` and
  `uv run python scripts/check_portability.py` pass before a chapter is called done, and
  `quarto render docs` has no warnings.
