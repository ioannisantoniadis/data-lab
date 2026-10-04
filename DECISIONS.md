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

### D8. Gate 1 decisions (2026-10-04)

The owner accepted the Phase 1 recommendations (`ROADMAP.md`, *What Phase 1 showed*):

1. **Claim 16 includes the pool-selector results** (the lower bound; a linear pool keeps
   uniform's exponent; a pool of size n^(1+α) recovers the oracle's). SPEC v0.3 §8.
2. **Claim 13 uses T5's synthetic side label,** which has exactly known invariances.
3. **The signature figure is accepted;** chapter 13 keeps the long tail as planned.
4. **Phase 1 committed locally** (not pushed).

Gate 1 passed. Phase 2 (chapters 1–7) waits for the owner's go-ahead.


### D7. Gate 0 decisions (2026-10-04)

The owner accepted the Phase 0 recommendations (`ROADMAP.md`, `review.md`), applied in SPEC v0.2:

1. **Long-tail thesis, reworded (§2.1).** Scoped to memorization-like settings with long-tailed
   inputs; noise, target complexity and input dimension are named as the other factors; the
   manifold-dimension and variance/resolution-limited accounts are presented alongside.
   Redundancy explains uniform sampling's slower exponent; the tail mass explains the power
   law; an oracle selector steepens it but does not escape it.
2. **Chapter 13 keeps the long tail as the signature,** presented as an exact reproduction
   that cites Hutter (2021) and Dohmatob et al. (2024), with a non-oracle selector beside the
   oracle one.
3. **Evaluation-only cards.** A card's *Changes* field may be "evaluation only" (splits,
   leakage control, shift detection, learning-curve estimation).
4. **Word cap counts prose,** as counted by `scripts/word_count.py`; the cap stays 35,000.
5. **SPEC edits applied by the agent** (v0.2), including the sibling-coverage corrections
   (tokenization; feature scaling and conditioning, with new claim 21) and the π → p/q
   notation for class priors.

Gate 0 passed; Phase 1 started 2026-10-04.


### D1. Repository name and book title (2026-10-04)

- **Repository:** `data-lab`, renamed from `training-data-lab`. The scope is data for
  learning in general (training, evaluation and test data, shift and leakage), not only
  training sets. It matches the `-lab` siblings.
- **Title:** *What the Model Sees: Training Data from First Principles*, approved by the
  owner.
- **Subtitle (closed at Gate 0, 2026-10-04):** keep "Training Data". The lens is about
  training data; techniques that act only on evaluation get cards marked *evaluation only*
  (D7).

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
