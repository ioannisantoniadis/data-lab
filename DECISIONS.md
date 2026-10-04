# Decisions

Decisions reserved for the owner (marked ⚑ in `SPEC.md`). Move a decision to **Closed** with
the date and choice when made. Agents read this file before starting work.

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

## Closed

### D1. Repository name and book title (2026-10-04)

- **Repository:** `data-lab`, renamed from `training-data-lab`. The scope is data for
  learning in general (training, evaluation and test data, shift and leakage), not only
  training sets. It matches the `-lab` siblings.
- **Title:** *What the Model Sees: Training Data from First Principles*, approved by the
  owner.
- **Open point:** given the broader scope, the subtitle could drop "Training" (*What the
  Model Sees: Data from First Principles*). Confirm before the title is set anywhere
  public.

### D2. Package name (2026-10-04)

**`data_lab`** (distribution name `data-lab`), chosen by the agent at the owner's request.

**The package is never published to PyPI.** Like the sibling labs' packages (`rl4llm`,
`optimlab`), it exists only inside the repository: `uv sync` installs it into the local
virtual environment so figure scripts and tests can import it. The name only has to avoid
clashing with installed packages. That is why `datalab`, an existing PyPI project, was
avoided.

### D3. License (2026-10-04)

MIT, matching the sibling labs.

### D6. Relationship to `objectives-book` (2026-10-04)

**Standalone for now.** The owner's plan for `objectives-book` is to describe AI/ML processes
from a different angle, and this book may later become part of it.

To keep that path cheap:

- follow `objectives-book`'s conventions where they do not conflict with the sibling labs:
  - the portability rules (its SPEC §21.1);
  - the notation choices (π for policies only, p/q);
  - evidence labels;
- keep the data-card records (`scripts/technique_data.py`) in a format that could be merged
  with `objectives-book`'s method records.

Do not edit `objectives-book` from here.

### D0. Co-authorship (2026-10-04)

Inherited from `objectives-book` D10: credited "Ioannis Antoniadis, with Claude (Anthropic)",
with a "How this book was made" section in the preface.
