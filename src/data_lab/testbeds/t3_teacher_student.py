"""T3: the teacher-student perceptron, the theoretical setting of Sorscher et al. 2022
(arXiv 2206.14486, §2 and Appendices A.1 and C, read 2026-10-04).

- Inputs x ~ N(0, I_N), i.i.d.; a teacher T drawn uniformly on the sphere of radius sqrt(N);
  labels y = sign(T . x).
- Pruning keeps a fraction f of the examples by their margin |J_probe . x| along a probe
  vector: smallest margins = hardest, largest = easiest. With angle theta = 0 the probe is the
  teacher itself, so "easy" and "hard" are known exactly.
- The student is the max-margin separator (the solution SGD converges to on separable data, per
  the paper; the paper solves the QP with CVXPY). Here: the primal as a least-distance
  problem, solved exactly by non-negative least squares, and certified by the KKT conditions
  and a zero duality gap.
- Test error is exact, with no test sample: eps = arccos(R) / pi, R = J . T / (|J| |T|)
  (paper, Appendix A.1). A test checks it against fresh teacher-labeled data.
- The paper's simulations: N = 200, P = alpha_tot N for alpha_tot from 10^0.1 to 10^0.5,
  averaged over 100 draws. (The paper's alpha is the ratio P / N, unrelated to the Zipf
  exponent of T2; this module calls it ``ratio``.)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import nnls


@dataclass(frozen=True)
class Problem:
    teacher: np.ndarray

    @property
    def dim(self) -> int:
        return self.teacher.size

    def sample(self, n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
        x = rng.standard_normal((n, self.dim))
        y = np.sign(x @ self.teacher)
        y[y == 0] = 1.0  # probability zero; kept total for safety
        return x, y

    def probe(self, theta: float, rng: np.random.Generator) -> np.ndarray:
        """A unit vector at angle theta to the teacher (theta = 0: the teacher's direction)."""
        t = self.teacher / np.linalg.norm(self.teacher)
        u = rng.standard_normal(self.dim)
        u -= (u @ t) * t
        u /= np.linalg.norm(u)
        return np.cos(theta) * t + np.sin(theta) * u

    def test_error(self, student: np.ndarray) -> float:
        """Exact generalization error arccos(R) / pi for isotropic Gaussian inputs."""
        r = student @ self.teacher / (np.linalg.norm(student) * np.linalg.norm(self.teacher))
        return float(np.arccos(np.clip(r, -1.0, 1.0)) / np.pi)


def make_problem(dim: int, rng: np.random.Generator) -> Problem:
    """Teacher uniform on the sphere of radius sqrt(dim)."""
    t = rng.standard_normal(dim)
    return Problem(teacher=np.sqrt(dim) * t / np.linalg.norm(t))


def prune(x, y, probe, keep_fraction: float, keep: str = "hard"):
    """Keep a fraction of examples by margin |probe . x|: smallest ("hard") or largest ("easy")."""
    if keep not in ("hard", "easy"):
        raise ValueError("keep must be 'hard' or 'easy'")
    k = int(round(keep_fraction * len(y)))
    margin = np.abs(x @ probe)
    order = np.argsort(margin, kind="stable")
    idx = order[:k] if keep == "hard" else order[len(order) - k :]
    return x[idx], y[idx]


@dataclass(frozen=True)
class MaxMarginResult:
    weights: np.ndarray  # J = sum_mu a_mu y_mu x_mu, scaled so that min_mu y_mu J . x_mu = 1
    dual: np.ndarray
    duality_gap: float
    min_functional_margin: float


def max_margin(x: np.ndarray, y: np.ndarray, tol: float = 1e-8) -> MaxMarginResult:
    """Hard-margin separator through the origin: min |J|^2 / 2 s.t. y_mu J . x_mu >= 1.

    A least-distance problem, solved exactly by non-negative least squares (Lawson and
    Hanson's reduction; scipy's ``nnls`` is their active-set algorithm, which terminates in
    finitely many steps): with Z = y[:, None] * x (P x N), E = [Z'; 1'] and f = (0, ..., 0, 1),
    let u >= 0 minimize |E u - f| and r = E u - f. Then J = -r[:N] / r[N], and the dual
    variables are a = -u / r[N], so that J = Z' a.

    The result is certified, not assumed: the KKT conditions (min margin 1, a >= 0,
    complementary slackness, zero duality gap |J|^2 - sum(a)) must hold to ``tol`` relative to
    |J|^2, or a ValueError is raised. (An earlier L-BFGS-B solver with an active-set polish
    could stop short of the optimum without saying so; the final audit's CI run exposed it.)
    """
    z = y[:, None] * x
    p_count, dim = z.shape
    e = np.vstack([z.T, np.ones((1, p_count))])
    f = np.zeros(dim + 1)
    f[-1] = 1.0
    u, _ = nnls(e, f, maxiter=50 * p_count)
    r = e @ u - f
    if abs(r[-1]) < 1e-12:
        raise ValueError("the constraints are infeasible: the data are not separable")
    j = -r[:dim] / r[-1]
    a = -u / r[-1]
    margins = z @ j
    scale = float(j @ j)
    gap = float(scale - a.sum())
    ok = (
        abs(margins.min() - 1.0) <= tol
        and a.min() >= -tol
        and np.max(np.abs(a * (margins - 1.0))) <= tol * max(scale, 1.0)
        and abs(gap) <= tol * max(scale, 1.0)
        and np.allclose(z.T @ a, j, atol=tol * max(np.sqrt(scale), 1.0))
    )
    if not ok:
        raise ValueError("max-margin solution failed its KKT check")
    return MaxMarginResult(weights=j, dual=a, duality_gap=gap,
                           min_functional_margin=float(margins.min()))
