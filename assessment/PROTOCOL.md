# Cross-repository quality assessment: protocol v2

A way to compare the learning-repo books (data-lab, rl-for-llms, loss-functions-lab,
optimization-lab, and later ones) on **output quality**, not on how much process they
recorded. It also produces the inventory needed to merge them into one book.

The question it answers: *how many of a book's checkable statements are wrong, and how
reproducible is it?* It does not answer whether the book is useful to readers; that needs
the reader tests of data-lab's SPEC §14, which are optional.

## 1. Principles

1. **Measure defects in the output.** The primary metric is the **confirmed defect density**:
   defects found in a full read and confirmed by the orchestrator, per 10,000 words of prose,
   by severity. A sampled defect rate with a confidence interval is secondary (the v1 pilot
   showed that 30 items cannot separate books). Rubric scores (1–5) are recorded but are not
   the comparison metric.
2. **Blind the auditor to the process.** Auditors see the book, code, tests, figures and
   bibliography, never the plans, decision logs, research logs or earlier audits, so a
   visible paper trail cannot raise a score.
3. **Measure the auditor too.** Known errors are planted in each copy; the share found
   estimates the audit's sensitivity, so a clean result can be interpreted.
4. **Two independent auditors per repository,** on the same sample, so agreement can be
   measured.
5. **Fixed before results are seen.** Sampling rule, defect definitions and severity scale
   are those below, applied identically to every repository. Changes make a new protocol
   version, and earlier results are not compared across versions.

## 2. Preparing a repository (the orchestrator)

1. **Blinded copy** (`assessment/blind_copy.py`): copy the repository, then remove `.git`,
   build outputs and virtual environments, and the process files: `SPEC.md`,
   `DECISIONS.md`, `ROADMAP.md`, `CLAUDE.md`, `CONVENTIONS.md`, `COVERAGE.md`,
   `research-log.md`, `review.md`, `audits/`, `assessment/`, except files that the
   repository's tests read (kept, so the tests still run). The README is replaced by a neutral
   one with the title and **the original README's code blocks verbatim**, so the documented
   build still works (v1 dropped install flags, and an auditor reported the result as a
   defect).
   *Known limit:* the book's own text (a preface, "Checked by" lines) still shows some
   process. That is output, and stays.
2. **Claim inventory and sample** (`assessment/inventory.py`): every paragraph, list item,
   caption, table row and display equation of the book's `.qmd` and generated include files
   is classified into one stratum, in this order of priority. Blocks that only point to a
   figure or section, ask a question, or carry no assertion are skipped (v1 sampled 3–4 such
   items per book):

   | Stratum | Rule | Quota |
   |---|---|---|
   | figure | a figure caption | 4 |
   | citation | contains a citation (`@key`) | 8 |
   | equation | a display equation, or inline math containing `=`, `\le`, `\ge`, `\propto` or `\approx` | 6 |
   | code | names a library, function or default in backticks | 4 |
   | number | contains a digit outside math, links and cross-references | 8 |

   Published-number shortcodes are replaced by their values first. A seeded random sample
   (seed = 2026 plus the repository's name) draws the quota from each stratum; a shortfall is
   filled from the largest remaining strata. **30 items per repository** for a quick check,
   **100** when the sampled rate is to be compared. Both auditors get the same sample.
3. **Planted errors** (the orchestrator, after sampling; the key is kept outside the copy):
   four per repository, two inside sampled items and two outside, one of each kind:
   - a changed number (in prose or in the published-number file);
   - a changed citation locator or a word changed inside a quotation;
   - a sign or factor error in an equation;
   - a caption statement contradicted by its figure.

   Each plant must be a plausible error, checkable from the copy and its sources.

## 3. Auditing (each auditor, a fresh session with no other context)

The auditor works only in its copy (scratch files in `<copy>/_audit/`) and on primary
sources. It must not open the original repository, its GitHub page or its published site.
It returns its report as its final message (subagents cannot write report files); the
orchestrator saves it.

1. **Reproduce:** `uv sync`, lint, tests, `quarto render`, and every figure script. Record
   failures, warnings and any image that differs visibly from the committed one.
2. **Verify each sampled item.** Check every checkable statement in it against its ground
   truth: recompute numbers from the code; open cited sources at the cited location;
   re-derive equations; re-run figures; execute library behavior. Give each item one
   verdict:
   - **correct:** every checkable statement holds;
   - **imprecise:** true in substance, but a number, locator or wording is off in a way that
     would not change a reader's understanding or action;
   - **wrong:** a statement is false;
   - **unsupported:** a factual statement with no source, test or derivation behind it in the
     book or repository;
   - **unverifiable:** the source could not be reached (not counted as a defect; reported).

   With each defect, give a **severity**: *major* if it would change a reader's conclusion or
   action, *minor* otherwise; and the evidence (file:line, what the source or computation
   says).
3. **Read the whole book** once, and report any other defect found, in the same format.
4. **Mechanical measures:**
   - reproducibility from a clean copy (pass/fail per step);
   - share of quoted numbers generated by scripts rather than typed;
   - share of checkable claims with a named test;
   - broken links, unresolved citations and cross-references.
5. **Rubric scores** (the `learning-repo-audit` rubric), recorded for reference.
6. **Report** in the template of §5, to the path given.

## 4. Metrics (the orchestrator)

- **Confirmed defect density** (primary) = defects from the sample and the full read that
  the orchestrator confirms against the original repository, per 10,000 prose words, by
  severity; planted errors and blinding artifacts excluded. A defect counts if one auditor
  reports it and the orchestrator confirms it, or both auditors report it independently.
- **Defect rate** = (wrong + unsupported) / (items verified, excluding unverifiable and
  planted), with a Wilson 95% interval; also with imprecise counted. Per auditor and pooled
  (an item is a defect if either auditor shows it with evidence that survives a check by
  the orchestrator).
- **Major defect rate,** the same with severity major only.
- **Sensitivity** = planted errors found / planted errors, per auditor; inside-sample and
  outside-sample separately.
- **Agreement:** Cohen's kappa between the two auditors on defect versus no defect, over the
  shared items.
- **Reproducibility and mechanical measures,** as reported.

With 30 items, a defect rate's interval is wide (for 2/30, about 2%–21%): the pilot shows
whether the method works and roughly how the books differ, not a precise ranking. A full
comparison should use 60–100 items per book.

## 5. Report template (auditor)

```markdown
# Audit: <repo> (protocol v1, auditor <A|B>, <date>)

## Reproduction
| Step | Result | Notes |

## Sampled items
| # | Stratum | Verdict | Severity | Evidence |

## Other defects found while reading
| Location | Kind | Severity | Evidence |

## Mechanical measures
...

## Rubric scores (reference only)
| Criterion | Score | Note |
```

## 6. Merge-readiness inventory (collected in the same pass)

From each repository, record:
- every symbol with its meaning (to find notation clashes across books);
- topics covered, and which neighbor owns each;
- recurring devices (cards, evidence labels, templates) and their formats.

These feed the monorepo's shared conventions, and do not count toward the quality metrics.

## 7. Version history

- **v1 (2026-10-05):** pilot on data-lab and rl-for-llms; results in
  `pilot-2026-10-05.md`.
- **v2 (2026-10-05):** primary metric changed to confirmed defect density; blinding keeps the
  README's commands and files the tests read; the sampler skips non-assertions; reports are
  returned as text; scratch work stays inside the copy.
