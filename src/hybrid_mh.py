"""
HYBRID-MH — a bias-controlled Metropolis-Hastings sampler for LLM multi-agent systems.

Idea
----
Each of N agents sits on a node of a graph and holds a binary state s_i in {-1, +1}
(encoded as a token label, e.g. "A"/"B" or "0"/"1"). We want to test whether the
*cooperative* (neighbour-coupling) part of LLM collective dynamics is critical, with the
agent's *intrinsic bias* (its preferred answer, independent of neighbours) divided out.

We pre-register an Ising target Hamiltonian
        H(s) = -J * sum_{<i,j> in graph} s_i s_j
and sample its Boltzmann distribution  pi(s) ~ exp(-beta H(s))  with a Metropolis-Hastings
chain whose PROPOSAL is the LLM. At each step we pick a site i, show the LLM its
neighbourhood, and read its next-token distribution q(s'_i | s) over the two labels. We
accept the proposed flip with

        alpha = min(1,  exp(-beta * dH) * q(s_i | s') / q(s'_i | s) )

The q-ratio is exactly what corrects for the LLM's intrinsic bias: a model that "wants"
to answer +1 proposes +1 more often, but the ratio cancels it. By Hastings (1970) the
chain satisfies detailed balance w.r.t. pi for ANY proposal with full support, so the
stationary distribution is the cooperative Ising pi — the LLM enters only through mixing,
not through the equilibrium distribution.

IMPORTANT (honest note). Because MH samples the chosen target, the *equilibrium* critical
exponents are properties of that target, not of the LLM. HYBRID-MH therefore measures the
LLM proposal's COMPATIBILITY with cooperative criticality, and (with a classical control,
see classical_ising.py) we find the resulting exponent is Ising-consistent. The value of
this tool is (a) separating bias from cooperation and (b) discriminating topologies
(see analysis.py / the paper), NOT a new universality class.

This is a clean reference implementation. Plug in any LLM via the LLMBackend interface;
a MockBackend is provided so the sampler can be exercised/tested without a GPU.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Sequence
import numpy as np

from topology import Topology


# ----------------------------------------------------------------------------------------
# LLM backend interface
# ----------------------------------------------------------------------------------------
class LLMBackend:
    """Return P(label | prompt) for the two state labels, normalized to sum to 1.

    A real backend (e.g. vLLM) builds the prompt from the agent's persona + task framing +
    visible neighbour labels, runs one forward pass, and sums the probability mass over all
    single-token encodings of each label (bare 'A', space-prefixed ' A', upper-case, ...),
    then renormalizes over the two labels. See `label_probs` for the contract.
    """
    labels: tuple[str, str] = ("0", "1")  # maps to (-1, +1)

    def label_probs(self, neighbour_states: Sequence[int], round_idx: int) -> tuple[float, float]:
        """Return (p_minus, p_plus) with p_minus + p_plus == 1."""
        raise NotImplementedError


class MockBackend(LLMBackend):
    """A test backend with a tunable intrinsic field h and conformity coupling k.

    P(+1) = sigmoid(h + k * sum(neighbours)). With h != 0 it mimics a biased LLM; the MH
    accept/reject in HYBRID-MH divides the bias out, so the sampled distribution is the
    *target* Ising regardless of h (modulo mixing). Useful to verify detailed balance.
    """
    def __init__(self, h: float = 0.0, k: float = 0.3, labels=("0", "1")):
        self.h, self.k, self.labels = h, k, labels

    def label_probs(self, neighbour_states, round_idx=0):
        z = self.h + self.k * float(np.sum(neighbour_states))
        p_plus = 1.0 / (1.0 + math.exp(-z))
        return (1.0 - p_plus, p_plus)


# ----------------------------------------------------------------------------------------
# HYBRID-MH sampler
# ----------------------------------------------------------------------------------------
@dataclass
class HybridMHSampler:
    topology: Topology
    backend: LLMBackend
    J: float = 1.0           # Ising coupling
    beta: float = 0.4        # inverse temperature (target = exp(-beta H))
    seed: int = 0
    eps: float = 1e-6        # proposal-probability floor (keep full support)
    _rng: np.random.Generator = field(init=False)

    def __post_init__(self):
        self._rng = np.random.default_rng(self.seed)

    def _neighbours(self, s, i):
        return [int(s[j]) for j in self.topology.neighbors[i]]

    def _q_plus(self, s, i, round_idx):
        """Proposal probability that site i is +1 given the current config."""
        p_minus, p_plus = self.backend.label_probs(self._neighbours(s, i), round_idx)
        # floor + renormalize to keep full support (required for MH validity)
        p_minus = min(max(p_minus, self.eps), 1 - self.eps)
        return 1.0 - p_minus if False else max(min(p_plus, 1 - self.eps), self.eps)

    def step(self, s, round_idx):
        N = self.topology.N
        i = int(self._rng.integers(N))
        q_plus = self._q_plus(s, i, round_idx)                 # P(propose +1)
        s_new_i = +1 if self._rng.random() < q_plus else -1    # draw proposal
        if s_new_i == s[i]:
            return s                                            # no move proposed
        # energy change for flipping site i: dH = 2 J s_i sum(neighbours)
        nb_sum = sum(int(s[j]) for j in self.topology.neighbors[i])
        dH = 2.0 * self.J * s[i] * nb_sum
        # proposal ratio q(s_i | s') / q(s'_i | s)
        q_fwd = q_plus if s_new_i == +1 else (1.0 - q_plus)
        q_rev = (1.0 - q_plus) if s_new_i == +1 else q_plus     # same neighbourhood (single flip)
        log_alpha = -self.beta * dH + math.log(q_rev) - math.log(q_fwd)
        if math.log(self._rng.random() + 1e-300) < log_alpha:
            s = s.copy(); s[i] = s_new_i
        return s

    def run(self, n_sweeps: int = 2000, burn_frac: float = 0.25):
        """Run the chain; return the magnetization trace m(t) and the spin history."""
        N = self.topology.N
        s = self._rng.choice(np.array([-1, 1], dtype=np.int8), size=N)
        m_trace = np.empty(n_sweeps)
        s_hist = np.empty((n_sweeps, N), dtype=np.int8)
        for t in range(n_sweeps):
            for _ in range(N):            # one sweep = N attempted updates
                s = self.step(s, t)
            m_trace[t] = s.mean()
            s_hist[t] = s
        return {"m_trace": m_trace, "s_history": s_hist, "burn_frac": burn_frac}


if __name__ == "__main__":
    # smoke test: detailed balance should make a STRONGLY biased proposal (h large)
    # still sample the zero-field Ising target -> magnetization symmetric around 0 at low J.
    from topology import build_topology
    topo = build_topology("lattice_2d", 16)
    for h in (0.0, 2.0):
        out = HybridMHSampler(topo, MockBackend(h=h, k=0.3), J=1.0, beta=0.4, seed=1).run(1500)
        m = out["m_trace"][375:]
        print(f"mock bias h={h}: <|m|>={np.mean(np.abs(m)):.3f}  chi={topo.N*np.var(m):.2f}")
