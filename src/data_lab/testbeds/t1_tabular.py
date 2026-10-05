"""T1: a synthetic tabular generator with a known joint distribution (SPEC §7).

Latent features z ~ N(mu_z, Sigma) in d dimensions, with equicorrelation ``rho``. The observed
features are x = z, or x = exp(z) when ``skewed`` (log-normal features). Every truth below is a
closed form in z, so a method can be measured against it exactly.

Regression target, on the log scale: log y = a + b . z + eps, eps ~ N(0, sigma_eps(z)^2), with
sigma_eps(z) = sigma0 exp(gamma z_1) (``gamma = 0`` is homoscedastic). Given z, y is log-normal,
so (scipy.stats.lognorm with s = sigma_eps, scale = exp(m), docstring read 2026-10-04, is the
independent reference used in the tests):

- conditional median and geometric mean: exp(m), where m = a + b . z = E[log y | z];
- conditional mean: exp(m + sigma_eps^2 / 2).

With ``additive=True`` the target is y = a + b . z + eps instead (mean = median = a + b . z).

Classification target: P(y = 1 | z) = sigmoid(u . z + u0) under the target distribution p. The
Bayes risk under p is a one-dimensional integral, because u . z is Gaussian. (The book's
notation: u, u_0; w is reserved for per-example weights.)

Covariate shift: the training distribution q draws z ~ N(0, Sigma); the target p draws
z ~ N(delta, Sigma). The density ratio p(z)/q(z) = exp(delta' S^-1 z - delta' S^-1 delta / 2)
is exact (S = Sigma).

Missingness masks for one column j (M = 1 means missing): MCAR (constant rate), MAR (rate
depends only on another, always-observed column k), MNAR (rate depends on column j itself).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import integrate, stats
from scipy.special import expit


@dataclass
class TabularGenerator:
    d: int = 3
    rho: float = 0.0
    skewed: bool = False
    # regression (log scale unless additive)
    a: float = 1.0
    b: np.ndarray = field(default_factory=lambda: np.array([0.8, -0.5, 0.3]))
    sigma0: float = 0.5
    gamma: float = 0.0
    additive: bool = False
    # classification
    u: np.ndarray = field(default_factory=lambda: np.array([1.5, -1.0, 0.5]))
    u0: float = 0.0

    def __post_init__(self) -> None:
        self.b = np.asarray(self.b, dtype=float)[: self.d]
        self.u = np.asarray(self.u, dtype=float)[: self.d]
        if self.b.size != self.d or self.u.size != self.d:
            raise ValueError("b and u need at least d entries")
        if not -1.0 / max(self.d - 1, 1) < self.rho < 1.0:
            raise ValueError("rho must keep the equicorrelation matrix positive definite")

    # --- features ---------------------------------------------------------------------------

    @property
    def cov(self) -> np.ndarray:
        return (1 - self.rho) * np.eye(self.d) + self.rho * np.ones((self.d, self.d))

    def sample_z(self, n: int, rng: np.random.Generator, shift=None) -> np.ndarray:
        mean = np.zeros(self.d) if shift is None else np.asarray(shift, dtype=float)
        return rng.multivariate_normal(mean, self.cov, size=n)

    def features(self, z: np.ndarray) -> np.ndarray:
        return np.exp(z) if self.skewed else z

    # --- regression -------------------------------------------------------------------------

    def log_location(self, z: np.ndarray) -> np.ndarray:
        """m(z) = a + b . z: E[log y | z] (or E[y | z] when additive)."""
        return self.a + z @ self.b

    def noise_scale(self, z: np.ndarray) -> np.ndarray:
        return self.sigma0 * np.exp(self.gamma * z[:, 0])

    def sample_y(self, z: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        eps = rng.standard_normal(len(z)) * self.noise_scale(z)
        m = self.log_location(z)
        return m + eps if self.additive else np.exp(m + eps)

    def conditional_mean(self, z: np.ndarray) -> np.ndarray:
        m, s = self.log_location(z), self.noise_scale(z)
        return m if self.additive else np.exp(m + 0.5 * s**2)

    def conditional_median(self, z: np.ndarray) -> np.ndarray:
        m = self.log_location(z)
        return m if self.additive else np.exp(m)

    def conditional_geometric_mean(self, z: np.ndarray) -> np.ndarray:
        """exp(E[log y | z]); only defined for the positive (log-normal) target."""
        if self.additive:
            raise ValueError("the geometric mean needs a positive target")
        return np.exp(self.log_location(z))

    # --- classification ---------------------------------------------------------------------

    def posterior(self, z: np.ndarray) -> np.ndarray:
        """P(y = 1 | z) under the target distribution p."""
        return expit(z @ self.u + self.u0)

    def sample_labels(self, z: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        return (rng.random(len(z)) < self.posterior(z)).astype(int)

    def prior(self, shift=None) -> float:
        """P(y = 1) under z ~ N(shift, Sigma): a 1-D Gaussian integral over t = u . z + u0."""
        loc, scale = self._score_moments(shift)
        val, _ = integrate.quad(
            lambda t: expit(t) * stats.norm.pdf(t, loc, scale), loc - 12 * scale, loc + 12 * scale
        )
        return val

    def bayes_risk(self, shift=None) -> float:
        """E[min(eta, 1 - eta)] with eta = P(y = 1 | z): the floor of any classifier's 0-1 risk."""
        loc, scale = self._score_moments(shift)
        val, _ = integrate.quad(
            lambda t: min(expit(t), 1 - expit(t)) * stats.norm.pdf(t, loc, scale),
            loc - 12 * scale,
            loc + 12 * scale,
            points=[0.0],
        )
        return val

    def threshold_risk(self, tau: float, shift=None) -> float:
        """Clean 0-1 risk of predicting 1 exactly when eta(z) > tau (tau = 1/2: Bayes risk)."""
        loc, scale = self._score_moments(shift)
        cut = float(np.log(tau / (1 - tau)))  # eta > tau  <=>  score > logit(tau)
        val, _ = integrate.quad(
            lambda t: (1 - expit(t) if t > cut else expit(t)) * stats.norm.pdf(t, loc, scale),
            loc - 12 * scale,
            loc + 12 * scale,
            points=[cut],
        )
        return val

    def score(self, z: np.ndarray) -> np.ndarray:
        """The classification score u . z + u0; eta = sigmoid(score)."""
        return z @ self.u + self.u0

    def _score_moments(self, shift):
        mean = np.zeros(self.d) if shift is None else np.asarray(shift, dtype=float)
        return float(self.u @ mean + self.u0), float(np.sqrt(self.u @ self.cov @ self.u))

    def sample_with_prior(
        self, n: int, prior: float, rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray]:
        """n examples whose class frequencies are exactly round(n * prior) positives.

        Class-conditional distributions p(z | y) are kept; only the class prior changes. This is
        prior shift: q(z | y) = p(z | y), q(y) chosen. Implemented by drawing from p and keeping
        the first examples of each class, which samples p(z | y) exactly.
        """
        n_pos = int(round(n * prior))
        need = {1: n_pos, 0: n - n_pos}
        zs, ys = {0: [], 1: []}, {0: 0, 1: 0}
        while ys[0] < need[0] or ys[1] < need[1]:
            z = self.sample_z(max(4 * n, 1_000), rng)
            y = self.sample_labels(z, rng)
            for k in (0, 1):
                take = z[y == k][: need[k] - ys[k]]
                zs[k].append(take)
                ys[k] += len(take)
        z = np.vstack([np.vstack(zs[1]), np.vstack(zs[0])])
        y = np.r_[np.ones(n_pos, int), np.zeros(n - n_pos, int)]
        order = rng.permutation(n)
        return z[order], y[order]

    # --- covariate shift --------------------------------------------------------------------

    def density_ratio(self, z: np.ndarray, delta) -> np.ndarray:
        """p(z) / q(z) for p = N(delta, Sigma), q = N(0, Sigma): the exact importance weight."""
        delta = np.asarray(delta, dtype=float)
        s_inv_delta = np.linalg.solve(self.cov, delta)
        return np.exp(z @ s_inv_delta - 0.5 * delta @ s_inv_delta)

    def density_ratio_second_moment(self, delta) -> float:
        """E_q[w^2] = exp(delta' Sigma^-1 delta); Var_q[w] = this minus 1."""
        delta = np.asarray(delta, dtype=float)
        return float(np.exp(delta @ np.linalg.solve(self.cov, delta)))


# --- missingness masks ------------------------------------------------------------------------


def mcar_mask(n: int, rate: float, rng: np.random.Generator) -> np.ndarray:
    """Missing completely at random: every entry missing with the same probability."""
    return rng.random(n) < rate


def mar_probability(other: np.ndarray, base: float, slope: float) -> np.ndarray:
    """Missing at random: the probability depends only on an always-observed column."""
    return expit(np.log(base / (1 - base)) + slope * other)


def mar_mask(other, base, slope, rng) -> np.ndarray:
    return rng.random(len(other)) < mar_probability(other, base, slope)


def mnar_mask(own, base, slope, rng) -> np.ndarray:
    """Missing not at random: the probability depends on the value that goes missing."""
    return rng.random(len(own)) < mar_probability(own, base, slope)
