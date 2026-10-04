# Decisions

Decisions reserved for the owner (marked ⚑ in `SPEC.md`). Move a decision to **Closed** with
the date and choice when made. Agents read this file before starting work.

## Open: needed in Phase 0

### D1. Repository name and book title ⚑

Current working name: `training-data-lab`. Rename it any time with
`gh repo rename <new> -R ioannisantoniadis/training-data-lab`.

**Repository name:**

| Option | Note |
|---|---|
| **`training-data-lab`** | *Recommended.* Matches `loss-functions-lab` and `optimization-lab`; says *training* data, not data engineering. |
| `data-lab` | Shortest; generic. |
| `data-for-learning` | Descriptive; breaks the `-lab` pattern. |
| `what-the-model-sees` | Matches a title option; less searchable. |

**Book title:**

| Option | Note |
|---|---|
| **What the Model Sees: Training Data from First Principles** | *Recommended.* Names the thesis (the representation and distribution the model is given). |
| Data for Learning, from First Principles | Plain; parallels the siblings. |
| From Samples to Scaling Laws: How Data Shapes What Models Learn | States the arc. |
| The Training Distribution | Precise and short; may read as narrow. |

Check the final title against existing books before adopting it.

### D2. Package name ⚑

`datalab` (working). Alternatives: one matching the repo name, such as `tdlab`.

### D3. License ⚑

- **(a)** MIT, like the sibling labs. *Recommended* for consistency.
- **(b)** Text under CC BY-NC-SA 4.0 and code under MIT, as recommended for `objectives-book`.

## Open: needed by Phase 2

### D4. External reviewer ⚑

One reviewer with a data-centric ML or applied statistics background (SPEC §14.3).
Recruiting during Phase 1 keeps Phase 2 from waiting.

### D5. External datasets and publication ⚑

- **Datasets:** the default is synthetic data plus scikit-learn's bundled data only. Any real
  dataset (for example a small public audio or text set) needs approval, a license check,
  and must not be required by CI.
- **Publication:** a GitHub Pages site on a personal account is public. Decide when to
  deploy: from Gate 2 (*recommended*, as with the sibling labs) or at release.

## Open: needed before release

### D6. Relationship to `objectives-book` ⚑

- **(a)** Standalone sibling lab, linked from `objectives-book`'s data-source discussion.
  *Recommended for now.*
- **(b)** Absorbed later as a part of `objectives-book` ("What to optimize *on*"), which would
  need that spec revised.

## Closed

### D0. Co-authorship (2026-10-04)

Inherited from `objectives-book` D10: credited "Ioannis Antoniadis, with Claude (Anthropic)",
with a "How this book was made" section in the preface.
