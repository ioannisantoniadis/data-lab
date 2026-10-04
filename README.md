# training-data-lab (working name)

A short book, with code, on training data from first principles. It covers:

- where data comes from;
- how it is cleaned, scaled, transformed and encoded, and when each choice matters;
- how the training distribution is shaped by sampling, weighting and augmentation;
- how much data a problem needs, and which data.

That last part runs from learning curves to scaling laws, and to why the long tail makes
returns diminish. The book is a sibling of
[loss-functions-lab](https://github.com/ioannisantoniadis/loss-functions-lab) and
[optimization-lab](https://github.com/ioannisantoniadis/optimization-lab). Every claim is
checked against synthetic data with a known ground truth.

**Status:** specification only (SPEC v0.1, 2026-10-04). Private while the plan is settled.
**Authors:** Ioannis Antoniadis, with Claude (Anthropic).

| File | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The implementation contract: thesis and lens, scope, architecture, coverage, testbeds, claims to test, figures, guardrails, acceptance and success criteria, plan |
| [`DECISIONS.md`](DECISIONS.md) | Owner decisions: name and title options, package, license, reviewer, datasets and publication, relation to `objectives-book` |
| [`CLAUDE.md`](CLAUDE.md) | Entry point for the implementing agent |
| [`research-log.md`](research-log.md) | Sources verified so far, and to what depth |
