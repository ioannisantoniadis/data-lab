# Agent entry point

You are building *What the Model Sees: Training Data from First Principles*, a short Quarto
book with code on data for learning (repo `data-lab`; see `DECISIONS.md`).

## Read first, in this order

1. `SPEC.md`, end to end: the implementation contract.
2. `DECISIONS.md`: owner decisions. Do not act on an open one; ask.
3. `ROADMAP.md`: phase status, Phase 0 findings that change the plan, the decision log.
4. `CONVENTIONS.md`: how chapters, data cards, figures and tests are written.
5. `research-log.md`: what has been verified, and at what depth. `review.md`: the thesis review.
6. The sibling repos' `CONVENTIONS.md` and notation appendices (`rl-for-llms` is the process
   reference; `loss-functions-lab`; `objectives-book` SPEC §21.1 for portability).
   `optimization-lab` has neither file.

## Non-negotiable rules (SPEC §12, §18)

- **Never write technical content from memory,** including library defaults. Open the source
  or the documentation, check it, and log it.
- **Every checkable claim is a test; every figure is a script.** Look at every image you
  generate.
- **Respect the size cap:** ≤ 35,000 words of prose, enforced in CI.
- **Respect topic ownership:** link sibling repos for topics they own; never edit them.
- **Follow the evidence,** even against the spec, and report it.
- **Owner decisions:** ⚑ decisions are the owner's. Stop at every gate (⛳).
- **Do not deploy the site before D5:** GitHub Pages on this account is public. `docs.yml`
  deliberately has no deploy job.
- **Commit and push only when the owner asks.**

## Where things live

```
src/data_lab/           testbeds/ (T1–T5), sampling, labels, cleaning, transforms, selection
tests/                  test_<area>.py: one test per SPEC §8 claim; test_tooling.py
scripts/technique_data.py   data-card records -> docs/includes/ (never edit includes by hand)
scripts/figures/        fig_<slug>.py + _theme.py (save_figure, LEVER_COLOR)
scripts/word_count.py, scripts/check_portability.py   CI checks
docs/                   Quarto book; chapters start with "# Title {#sec-id}"; no code execution
```

## Commands

```bash
uv sync
uv run ruff check . && uv run pytest
uv run python scripts/word_count.py && uv run python scripts/check_portability.py
uv run python scripts/technique_data.py
quarto render docs          # must produce zero WARN lines
```

## Skills

From the `ioannisantoniadis/claude-skills` marketplace:

- **Plugin `learning-repo`:**
  - `learning-repo-build` to build;
  - `learning-repo-audit` to judge, in a *fresh* session.
- **Plugin `skeptical-review`:** run on the thesis in Phase 0 (`review.md`); run again on
  chapter 13.

## Current status

- **2026-10-04:** SPEC v0.1. Name, title, license (MIT), package (`data_lab`, local only) and
  standalone status decided.
- **2026-10-04: Phase 0 done; ⛳ Gate 0 passed** (DECISIONS D7; SPEC v0.2). Phase 0 committed
  locally (not pushed).
- **2026-10-04: Phase 1 done; ⛳ Gate 1 passed** (D8; SPEC v0.3), committed locally. Testbeds T1–T5 with tests, the
  coverage-selection derivation, and the signature figure. See ROADMAP.md, *What Phase 1
  showed*.
- **2026-10-05: Phase 2 done; ⛳ Gate 2 passed** (D9; SPEC v0.4), uncommitted.
- **2026-10-05: Phase 3 done; ⛳ Gate 3 passed** (D10; SPEC v0.5). Phases 2–3 committed
  locally (d0959e8), not pushed.
- **2026-10-05: Phase 4 drafted and committed; pushed to the private remote** (no deploy).
  Chapter 15, the Map, the appendices and the preface written; claims 44–46 pass; the final
  fresh-agent audit passed SPEC §14's bar and its findings are fixed
  (`audits/2026-10-05-final-audit.md`). Open: the reader tests (need human readers), D4
  (external reviewer), D5 (publication).
