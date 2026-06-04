# Bias, not Cooperation: a bias-controlled sampling test of criticality in LLM multi-agent systems

This repo accompanies a short, **honest methods paper**. It provides **HYBRID-MH**, a
Metropolis–Hastings sampler that uses an LLM as the *proposal* against a chosen Ising
target Hamiltonian, in order to separate an LLM agent's **intrinsic bias** from genuine
**cooperative criticality** — and a reproducible pipeline (figures, classical control,
data) for the results.

> **TL;DR of the findings (stated honestly).**
> 1. Under bias-controlled HYBRID-MH, the measured finite-size-scaling exponent on a 2D
>    lattice is **statistically consistent with the 2D-Ising value** (benchmarked against a
>    classical Ising control on identical lattices). It is **not** a new universality class.
> 2. The framework nonetheless has **discriminating power**: it reproduces the textbook
>    topological hierarchy — finite-dimensional graphs (2D lattice, scale-free) are
>    Ising-like, the 1D ring shows **no transition**, and the fully-connected (mean-field)
>    graph **freezes** into trivial order.
> 3. Two appealing conjectures **fail** under controlled measurement (no opinion↔task
>    isomorphism; no a-priori exponent law). See `docs/audit_trail.md`.
>
> This started as a "new universality class" claim and was **retracted by our own audit**
> (a vs-N/vs-L unit confusion + indistinguishability from Ising on small lattices), partly
> prompted by concurrent work (arXiv:2605.10528). The audit trail is included in full —
> the honesty *is* part of the contribution.

## Why HYBRID-MH

An LLM agent has a strong **intrinsic bias** (a preferred answer independent of its
neighbours). On a lattice that bias produces *crossovers* that mimic a phase transition
without any cooperative criticality (cf. arXiv:2605.10528, which finds raw LLM-lattice
dynamics are bias-dominated). HYBRID-MH divides the bias out **by construction**: the LLM
supplies only the proposal `q`, and an explicit accept/reject

```
alpha = min(1,  exp(-beta * dH) * q_rev / q_fwd )
```

corrects for it, so the chain samples the cooperative Ising target by detailed balance
(Hastings 1970). The LLM enters only through *mixing*, not the equilibrium distribution.

## Repository layout

```
src/
  hybrid_mh.py        Reference implementation of HYBRID-MH (+ a MockBackend, no GPU needed)
  topology.py         lattice_2d / scale_free / ring_1d / fully_connected graphs
  observables.py      susceptibility, Binder cumulant, magnetization
  analysis.py         finite-size-scaling exponent + bootstrap CI (with the vs-N/vs-L note)
  classical_ising.py  classical 2D-Ising control (the decisive benchmark)
figures/
  make_figures.py     regenerates figA (topology discrimination) + figB (classical benchmark)
  figA_*.png figB_*.png fig3-6_*.png
data/
  *.csv *.json        processed observables (susceptibility, exponents, topology comparison)
  raw_chains.tar.gz   944 raw MCMC chains (chain_summary.json + chain_history.npz)
paper/
  manuscript.md, claims_evidence_matrix.md
docs/
  audit_trail.md      the full rigor / self-falsification record (incl. the retraction)
```

## Reproduce

**Analysis & figures (no GPU):**
```bash
pip install -r requirements.txt
python figures/make_figures.py          # -> figures/figA_*.png, figB_*.png
python src/classical_ising.py           # the classical 2D-Ising benchmark (key control)
tar xzf data/raw_chains.tar.gz -C data  # if you want the raw chains
```

**Run HYBRID-MH (sampler smoke test, no GPU):**
```bash
cd src && python hybrid_mh.py
# Uses a MockBackend with a tunable intrinsic field h; verifies that the accept/reject
# divides the bias out (a strongly biased proposal still samples the zero-field target).
```

**Run HYBRID-MH with a real LLM (needs a GPU + vLLM):** implement `LLMBackend.label_probs`
in `src/hybrid_mh.py` to call your model (prompt = persona + task + visible neighbour
labels; return P(label) summed over all single-token encodings of each label). Then drive
`HybridMHSampler(topology, backend, J, beta).run(n_sweeps)` over a grid of N and J.

## A note on the convention bug (read this)

The 2D-Ising exponent `gamma/nu = 7/4` is defined vs the **linear** size `L`
(`chi ~ L^{gamma/nu}`). On a 2D lattice `N = L^2`, so a true 2D Ising scales as
`chi ~ N^{0.875}` — its "vs N" slope is **0.875**, not 1.75. Comparing a vs-N slope to a
vs-L exponent is the unit error that briefly inflated this project's central claim. Always
benchmark against the classical control in the **same** convention. `src/analysis.py`
documents this and `src/classical_ising.py` provides the benchmark.

## Concurrent / related work
- arXiv:2605.10528 (2026-05) — LLM multi-agent systems on a 2D lattice as a spin system;
  finds collective alignment is bias-dominated (raw dynamics). This work controls the bias
  with HYBRID-MH and adds cross-topology discrimination.

## License
MIT (see LICENSE).
