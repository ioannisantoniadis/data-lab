"""T3: the teacher-student perceptron, the theoretical setting of Sorscher et al. 2022
(arXiv 2206.14486, §2 and Appendices A.1 and C, read 2026-10-04).

- Inputs x ~ N(0, I_N), i.i.d.; a teacher T drawn uniformly on the sphere of radius sqrt(N);
  labels y = sign(T . x).
- Pruning keeps a fraction f of the examples by their margin |J_probe . x| along a probe
  vector: smallest margins = hardest, largest = easiest. With angle theta = 0 the probe is the
  teacher itself, so "easy" and "hard" are known exactly.
- The student is the max-margin separator (the solution SGD converges to on separable data, per
  the paper; the paper solves the QP with CVXPY). Here: the hard-margin dual, solved by
  L-BFGS-B with non-negativity bounds, checked by KKT conditions and a duality gap.
- Test error is exact, with no test sample: eps = arccos(R) / pi, R = J . T / (|J| |T|)
  (paper, Appendix A.1). A test checks it against fresh teacher-labeled data.
- The paper's simulations: N = 200, P = alpha_tot N for alpha_tot from 10^0.1 to 10^0.5,
  averaged over 100 draws. (The paper's alpha is the ratio P / N, unrelated to the Zipf
  exponent of T2; this module calls it ``ratio``.)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize


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


def _polish_active_set(gram: np.ndarray, a0: np.ndarray, max_iter: int = 200) -> np.ndarray:
    """Make a first-order solution exact. On the support S of the optimum the KKT conditions
    are equalities, (gram a)_S = 1 with a_S >= 0, and (gram a)_i >= 1 off S. Solve on S by
    least squares, drop negative entries, add violated constraints, and repeat."""
    support = a0 > 1e-6 * max(a0.max(), 1e-300)
    a = a0
    for _ in range(max_iter):
        idx = np.flatnonzero(support)
        sol, *_ = np.linalg.lstsq(gram[np.ix_(idx, idx)], np.ones(idx.size), rcond=None)
        if np.any(sol < 0):
            support[idx[sol < 0]] = False
            continue
        cand = np.zeros_like(a0)
        cand[idx] = sol
        margins = gram @ cand
        violated = (~support) & (margins < 1.0 - 1e-10)
        if not violated.any():
            return cand
        support[np.argmin(np.where(violated, margins, np.inf))] = True
        a = cand
    return a  # fall back to the last iterate; callers check the KKT conditions


@dataclass(frozen=True)
class MaxMarginResult:
    weights: np.ndarray  # J = sum_mu a_mu y_mu x_mu, scaled so that min_mu y_mu J . x_mu = 1
    dual: np.ndarray
    duality_gap: float
    min_functional_margin: float


def max_margin(x: np.ndarray, y: np.ndarray, tol: float = 1e-10) -> MaxMarginResult:
    """Hard-margin separator through the origin: min |J|^2 / 2 s.t. y_mu J . x_mu >= 1.

    Dual: max sum(a) - |Z' a|^2 / 2 over a >= 0, with Z = y[:, None] * x and J = Z' a.
    At the optimum the primal and dual objectives agree, so the duality gap
    |J|^2 / 2 - (sum(a) - |J|^2 / 2) = |J|^2 - sum(a) is zero.
    """
    z = y[:, None] * x
    gram = z @ z.T

    def objective(a):
        ga = gram @ a
        return 0.5 * a @ ga - a.sum(), ga - 1.0

    res = minimize(
        objective,
        x0=np.full(len(y), 1e-3),
        jac=True,
        method="L-BFGS-B",
        bounds=[(0.0, None)] * len(y),
        options={"maxiter": 100_000, "maxfun": 200_000, "ftol": tol, "gtol": tol},
    )
    a = _polish_active_set(gram, res.x)
    j = z.T @ a
    return MaxMarginResult(
        weights=j,
        dual=a,
        duality_gap=float(j @ j - a.sum()),
        min_functional_margin=float(np.min(z @ j)),
    )
