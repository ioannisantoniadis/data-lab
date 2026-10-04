# Agent entry point

You are building *What the Model Sees: Training Data from First Principles*, a short book
with code on data for learning (repo `data-lab`; see `DECISIONS.md`). The project is in **Phase 0: foundation**. No chapters
or code exist yet.

## Read first, in this order

1. `SPEC.md`, end to end: the implementation contract.
2. `DECISIONS.md`: owner decisions. Do not act on an open one; ask.
3. `research-log.md`: what has already been verified, and at what depth.
4. The sibling repos' `CONVENTIONS.md` and notation appendices, especially:
   - `rl-for-llms`, the process reference;
   - `loss-functions-lab`;
   - `optimization-lab`.

## Non-negotiable rules (SPEC §12, §18)

- **Never write technical content from memory,** including library defaults. Open the
  source or the documentation, check it, and log it.
- **Every checkable claim is a test; every figure is a script.** Look at every image you
  generate.
- **Respect the size cap:** ≤ 35,000 words of prose, enforced in CI.
- **Respect topic ownership:** link sibling repos for topics they own; never edit them.
- **Follow the evidence,** even against the spec, and report it.
- **Owner decisions:** ⚑ decisions are the owner's. Stop at every gate (⛳).
- **Do not deploy the site before D5:** GitHub Pages on this account is public.
- **Commit and push only when the owner asks.**

## Skills

From the `ioannisantoniadis/claude-skills` marketplace:

- **Plugin `learning-repo`:**
  - `learning-repo-build` to build;
  - `learning-repo-audit` to judge, in a *fresh* session.
- **Plugin `skeptical-review`:** for the thesis, and for chapter 13.

## Current status

- **2026-10-04:** SPEC v0.1 drafted. Name, title, license (MIT) and standalone status decided.
- **Next, Phase 0:**
  - positioning search;
  - `skeptical-review` of the thesis;
  - scaffold;
  - owner decision D2 (package name).
