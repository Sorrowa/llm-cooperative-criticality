"""Finite-size-scaling exponent extraction.

chi(N) ~ N^(gamma/nu) at the susceptibility peak. We fit the log-log slope and get a
bootstrap CI over seeds.

CONVENTION WARNING (a lesson from this project; see docs/audit_trail.md):
the 2D-Ising exponent gamma/nu = 7/4 is defined vs the LINEAR size L (chi ~ L^{gamma/nu}).
On a 2D lattice N = L^2, so a TRUE 2D Ising scales as chi ~ N^{0.875} -- i.e. the "vs N"
slope of a 2D Ising is 0.875, NOT 1.75. Always compare exponents in ONE convention, and
benchmark against the classical control (classical_ising.py) on identical lattices.
"""
import numpy as np


def fss_slope_vs_N(N, chi):
    """Slope of log chi vs log N."""
    return float(np.polyfit(np.log(N), np.log(chi), 1)[0])


def fss_with_ci(per_seed_chi: dict, n_boot: int = 2000, seed: int = 0):
    """per_seed_chi: {N: [chi_seed0, chi_seed1, ...]}. Returns (slope, lo, hi) vs N."""
    Ns = sorted(per_seed_chi)
    point = fss_slope_vs_N(Ns, [np.mean(per_seed_chi[N]) for N in Ns])
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        chis = [np.mean(rng.choice(per_seed_chi[N], size=len(per_seed_chi[N]), replace=True)) for N in Ns]
        boot.append(fss_slope_vs_N(Ns, chis))
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return point, float(lo), float(hi)


def to_linear_size_exponent(slope_vs_N, dim=2):
    """Convert a vs-N slope to the vs-L convention for a d-dimensional lattice (N=L^d)."""
    return slope_vs_N * dim
