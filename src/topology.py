"""Interaction-network topologies for the LLM-agent population.

Four topologies are used in the paper to test the framework's discriminating power:
  - lattice_2d      : finite-dimensional, has an Ising-like transition
  - scale_free      : Barabasi-Albert hub network (finite-d-like), same regime
  - ring_1d         : 1D ring -> NO finite-temperature transition (control)
  - fully_connected : mean-field -> trivial ordering (control)
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class Topology:
    N: int
    name: str
    neighbors: List[List[int]]            # per-agent neighbour index lists
    edges: List[Tuple[int, int]]          # undirected edges (i < j)

    def degree(self, i: int) -> int:
        return len(self.neighbors[i])


def lattice_2d(N: int, periodic: bool = True) -> Topology:
    """2D lattice with von-Neumann (4) neighbourhood. Auto-tiles N as L1 x L2."""
    L1 = int(round(math.sqrt(N)))
    while N % L1 != 0 and L1 > 1:
        L1 -= 1
    L2 = N // L1
    assert L1 * L2 == N, f"N={N} cannot be tiled as a rectangle"

    def idx(r, c):
        if periodic:
            return (r % L1) * L2 + (c % L2)
        return r * L2 + c if (0 <= r < L1 and 0 <= c < L2) else -1

    neighbors = [[] for _ in range(N)]
    edges = set()
    for r in range(L1):
        for c in range(L2):
            i = idx(r, c)
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                j = idx(r + dr, c + dc)
                if j < 0 or j == i:
                    continue
                neighbors[i].append(j)
                edges.add((min(i, j), max(i, j)))
    return Topology(N, "lattice_2d", neighbors, sorted(edges))


def fully_connected(N: int) -> Topology:
    neighbors = [[j for j in range(N) if j != i] for i in range(N)]
    edges = [(i, j) for i in range(N) for j in range(i + 1, N)]
    return Topology(N, "fully_connected", neighbors, edges)


def ring_1d(N: int) -> Topology:
    neighbors = [[(i - 1) % N, (i + 1) % N] for i in range(N)]
    edges = sorted({tuple(sorted((i, (i + 1) % N))) for i in range(N)})
    return Topology(N, "ring_1d", neighbors, edges)


def scale_free(N: int, m: int = 2, seed: int = 12345) -> Topology:
    """Barabasi-Albert preferential attachment: m edges per new node."""
    rng = np.random.default_rng(seed)
    edges = set()
    targets = list(range(m))
    repeated = list(range(m))
    for new in range(m, N):
        chosen = set()
        while len(chosen) < m:
            chosen.add(repeated[rng.integers(len(repeated))])
        for t in chosen:
            edges.add(tuple(sorted((new, t))))
        repeated.extend(chosen)
        repeated.extend([new] * m)
    neighbors = [[] for _ in range(N)]
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    return Topology(N, "scale_free", neighbors, sorted(edges))


def build_topology(spec: str, N: int) -> Topology:
    return {
        "lattice_2d": lambda: lattice_2d(N),
        "fully_connected": lambda: fully_connected(N),
        "ring_1d": lambda: ring_1d(N),
        "scale_free": lambda: scale_free(N),
    }[spec]()
