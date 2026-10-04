# data-lab

*What the Model Sees: Training Data from First Principles*: a short book, with code, on
data for learning, from first principles. It covers:

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
**License:** MIT.
**Authors:** Ioannis Antoniadis, with Claude (Anthropic).

| File | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The implementation contract: thesis and lens, scope, architecture, coverage, testbeds, claims to test, figures, guardrails, acceptance and success criteria, plan |
| [`DECISIONS.md`](DECISIONS.md) | Owner decisions: closed (name, title, license, relation to `objectives-book`) and open (package, reviewer, datasets and publication) |
| [`CLAUDE.md`](CLAUDE.md) | Entry point for the implementing agent |
| [`research-log.md`](research-log.md) | Sources verified so far, and to what depth |
