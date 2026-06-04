"""Observables computed from a magnetization trace m(t)."""
import numpy as np


def tail(m, burn_frac=0.25):
    return np.asarray(m)[int(len(m) * burn_frac):]


def susceptibility(m, N, burn_frac=0.25):
    """chi = N * Var(m) over the post-burn-in tail."""
    return N * np.var(tail(m, burn_frac))


def binder_cumulant(m, burn_frac=0.25):
    """U4 = 1 - <m^4> / (3 <m^2>^2).  ~0 disordered, ~2/3 ordered; N-independent at T_c."""
    t = tail(m, burn_frac)
    m2 = np.mean(t ** 2)
    m4 = np.mean(t ** 4)
    return 1 - m4 / (3 * m2 ** 2) if m2 > 0 else float("nan")


def abs_magnetization(m, burn_frac=0.25):
    return float(np.mean(np.abs(tail(m, burn_frac))))
