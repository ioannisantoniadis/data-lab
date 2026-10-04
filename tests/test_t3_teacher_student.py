"""T3 ground truths: the teacher, the exact test-error formula, pruning, and the max-margin
student, checked against a primal reference solver by objective value (not only predictions)."""

import numpy as np
import pytest
from scipy.optimize import minimize

from data_lab.testbeds.t3_teacher_student import make_problem, max_margin, prune


def test_teacher_on_the_sphere_and_labels_from_it():
    rng = np.random.default_rng(0)
    prob = make_problem(200, rng)
    assert np.linalg.norm(prob.teacher) == pytest.approx(np.sqrt(200))
    x, y = prob.sample(500, rng)
    assert np.all(y == np.sign(x @ prob.teacher))


def test_exact_test_error_matches_fresh_teacher_labeled_data():
    rng = np.random.default_rng(1)
    prob = make_problem(50, rng)
    student = prob.teacher + 6.0 * rng.standard_normal(50)  # some angle to the teacher
    x, y = prob.sample(400_000, rng)
    mc = np.mean(np.sign(x @ student) != y)
    exact = prob.test_error(student)
    assert abs(mc - exact) < 4 * np.sqrt(exact * (1 - exact) / len(y))
    assert prob.test_error(prob.teacher) == pytest.approx(0.0, abs=1e-7)


def test_probe_has_the_requested_angle():
    rng = np.random.default_rng(2)
    prob = make_problem(100, rng)
    for theta in (0.0, 0.3, 1.0):
        p = prob.probe(theta, rng)
        cos = p @ prob.teacher / np.linalg.norm(prob.teacher)
        assert np.arccos(np.clip(cos, -1, 1)) == pytest.approx(theta, abs=1e-9)


def test_prune_keeps_the_hardest_or_easiest_fraction():
    rng = np.random.default_rng(3)
    prob = make_problem(20, rng)
    x, y = prob.sample(1_000, rng)
    probe = prob.probe(0.0, rng)
    xh, _ = prune(x, y, probe, 0.2, "hard")
    xe, _ = prune(x, y, probe, 0.2, "easy")
    assert len(xh) == len(xe) == 200
    assert np.abs(xh @ probe).max() <= np.quantile(np.abs(x @ probe), 0.2) + 1e-12
    assert np.abs(xe @ probe).min() >= np.quantile(np.abs(x @ probe), 0.8) - 1e-12


def test_max_margin_satisfies_kkt_conditions():
    rng = np.random.default_rng(4)
    prob = make_problem(200, rng)
    x, y = prob.sample(400, rng)  # ratio P / N = 2, inside the paper's range
    res = max_margin(x, y)
    assert res.min_functional_margin == pytest.approx(1.0, abs=1e-5)
    assert abs(res.duality_gap) < 1e-6 * (res.weights @ res.weights)
    margins = (y[:, None] * x) @ res.weights
    support = res.dual > 1e-8 * res.dual.max()
    np.testing.assert_allclose(margins[support], 1.0, atol=1e-4)  # complementary slackness


def test_max_margin_matches_a_primal_reference_solver_objective():
    """Same optimum as SLSQP on the primal QP: compare objective values, not just predictions."""
    rng = np.random.default_rng(5)
    prob = make_problem(10, rng)
    x, y = prob.sample(40, rng)
    ours = max_margin(x, y)
    z = y[:, None] * x
    ref = minimize(
        lambda j: 0.5 * j @ j,
        x0=prob.teacher / np.min(z @ prob.teacher),  # a feasible start
        jac=lambda j: j,
        constraints=[{"type": "ineq", "fun": lambda j: z @ j - 1.0, "jac": lambda j: z}],
        method="SLSQP",
        options={"ftol": 1e-14, "maxiter": 1_000},
    )
    assert ref.success
    assert 0.5 * ours.weights @ ours.weights == pytest.approx(ref.fun, rel=1e-6)
    np.testing.assert_allclose(ours.weights, ref.x, rtol=1e-4, atol=1e-6)


def test_more_data_lowers_the_student_error_without_pruning():
    """Sanity: with f = 1, error falls from ratio 1.26 to 3.16 (the paper's range), on average
    over 20 teachers."""
    rng = np.random.default_rng(6)
    errs = {1.26: [], 3.16: []}
    for _ in range(20):
        prob = make_problem(100, rng)
        for ratio in errs:
            x, y = prob.sample(int(ratio * 100), rng)
            errs[ratio].append(prob.test_error(max_margin(x, y).weights))
    assert np.mean(errs[3.16]) < np.mean(errs[1.26])
