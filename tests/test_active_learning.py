"""Claim tests: Part IV, active learning (claim 43, added in Phase 3 for chapter 14; T1)."""

from data_lab.selection import active_learning_experiment


def test_uncertainty_sampling_gains_shrink_with_label_noise():
    """Claim 43. Pool-based uncertainty sampling (query the example whose predicted probability
    is nearest 1/2) reaches a rule closer to the Bayes rule than random labeling at the same
    budget when the classes are nearly separable (at 40 and 100 labels, under 0.7 times the
    disagreement), and gains nothing measurable when labels are noisy (at 100 labels, over 0.85
    times); 60 seeds, T1. (A 20-seed pilot suggested uncertainty sampling was worse than random
    on noisy labels; with 60 seeds the difference is within noise.)"""
    clean = active_learning_experiment(scale=4.0, seeds=60)
    noisy = active_learning_experiment(scale=1.0, seeds=60)
    c = clean["uncertainty"].mean(axis=0) / clean["random"].mean(axis=0)
    n = noisy["uncertainty"].mean(axis=0) / noisy["random"].mean(axis=0)
    assert c[1] < 0.7 and c[2] < 0.7
    assert n[2] > 0.85
