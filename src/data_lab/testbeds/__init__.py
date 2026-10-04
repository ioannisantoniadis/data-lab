"""Ground-truth testbeds (SPEC §7). Each must let every figure script run in under a minute
on a laptop CPU with no network access, and must expose the exact quantity it is the
ground truth for.

- ``t1_tabular``: T1, synthetic tabular generator. Truth: Bayes predictor and risk;
  conditional mean, median and geometric mean; density ratio.
- ``t2_zipf``: T2, Zipf feature stream (Hutter 2021). Truth: expected error of the
  memorizing learner, by exact summation.
- ``t3_teacher_student``: T3, teacher-student perceptron (Sorscher et al. 2022). Truth: each
  example's teacher margin.
- ``t4_markov_text``: T4, Markov text source. Truth: entropy rate; exact duplicate counts.
- ``t5_signals``: T5, synthetic signals and bundled digits. Truth: generating frequencies;
  invariance under a defined transform family.

All are stubs until Phase 1.
"""
