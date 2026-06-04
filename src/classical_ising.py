#!/usr/bin/env python3
"""Salvage analysis: a RELIABLE classical 2D-Ising baseline (vectorized checkerboard
Metropolis, wide J grid to capture the true χ peak, long chains) to compare against our
LLM γ/ν, in BOTH conventions (vs N and vs L). Decides whether the LLM exponent is cleanly
distinguishable from a true 2D Ising in the same small-lattice regime.
"""
import numpy as np

def run_chain(L1, L2, beta, J, n_sweeps, burn, rng):
    s = rng.choice(np.array([-1, 1], dtype=np.int8), size=(L1, L2))
    cb = (np.add.outer(np.arange(L1), np.arange(L2)) % 2).astype(bool)  # checkerboard mask
    mt = np.empty(n_sweeps)
    for t in range(n_sweeps):
        for mask in (cb, ~cb):
            nb = (np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1))
            dH = 2.0 * J * s * nb
            flip = mask & ((dH <= 0) | (rng.random((L1, L2)) < np.exp(-beta * dH)))
            s[flip] *= -1
        mt[t] = s.mean()
    m = mt[int(n_sweeps * burn):]
    return (L1 * L2) * np.var(m), np.mean(np.abs(m))

def chi_peak(L1, L2, beta, Js, n_sweeps=6000, burn=0.3, n_seed=6, seed0=0):
    rng = np.random.default_rng(seed0 + L1 * 131 + L2 * 17)
    best = (None, -1)
    for J in Js:
        chis = [run_chain(L1, L2, beta, J, n_sweeps, burn, rng)[0] for _ in range(n_seed)]
        c = np.mean(chis)
        if c > best[1]:
            best = (J, c)
    return best

def fss(shapes, beta, Js, label, n_sweeps=6000):
    print(f"\n=== {label} (beta={beta}, sweeps={n_sweeps}) ===")
    Ns, Ls, chis = [], [], []
    for (L1, L2) in shapes:
        pJ, chi = chi_peak(L1, L2, beta, Js, n_sweeps=n_sweeps)
        N = L1 * L2; Ns.append(N); Ls.append(np.sqrt(N)); chis.append(chi)
        print(f"  {L1}x{L2} (N={N:3d}, L~{np.sqrt(N):.2f}): peakJ={pJ:.2f}  chi={chi:.2f}")
    gN = np.polyfit(np.log(Ns), np.log(chis), 1)[0]
    gL = np.polyfit(np.log(Ls), np.log(chis), 1)[0]
    print(f"  --> gamma/nu vs N = {gN:.3f}   vs L = {gL:.3f}")
    return gN, gL

if __name__ == "__main__":
    Js = [0.85, 0.95, 1.05, 1.10, 1.15, 1.25, 1.40]   # bracket J_c(beta=0.4)=1.10
    # (A) proper square even-L — validate pipeline recovers ~1.75 vs L
    fss([(4,4),(6,6),(8,8),(10,10),(12,12),(16,16)], 0.4, Js, "A: proper square even-L 2D Ising")
    # (B) OUR exact lattice shapes + our chain length — the apples-to-apples baseline
    fss([(2,4),(4,4),(4,6),(4,8)], 0.4, Js, "B: OUR shapes (N=8/16/24/32), our 2000 sweeps", n_sweeps=2000)
    # (C) OUR shapes but LONG chains — isolate undersampling vs finite-size
    fss([(2,4),(4,4),(4,6),(4,8)], 0.4, Js, "C: OUR shapes, LONG 8000 sweeps", n_sweeps=8000)
    print("\nLLM-HYBRID-MH measured: gamma/nu vs N = 0.82  (=> vs L = 1.64). Compare to B and C above.")
