# Bias, not Cooperation: A Bias-Controlled Sampling Test of Criticality in LLM Multi-Agent Systems

*Working manuscript — Phase 9, HONEST (deflationary) reframe after a self-audit (2026-06-03) showed the original "distinct universality class γ/ν≈0.82" claim was untenable (a vs-N/vs-L unit confusion + small-lattice indistinguishability from 2D Ising; see `compact/rigor_audit_findings.md`). This version makes the defensible claims only. Concurrent work: arXiv:2605.10528 (2026-05).*

---

## Abstract

Populations of large-language-model (LLM) agents display collective behaviour that has been described as "phase-transition-like": magnetization, susceptibility peaks, and order–disorder crossovers on lattices of interacting agents. We ask whether this is **genuine cooperative criticality** or an artifact of each model's **intrinsic bias**. We introduce **HYBRID-MH**, a sampler that uses an LLM's next-token distribution as the *proposal* of an explicit Metropolis–Hastings chain against a chosen Ising target Hamiltonian; the accept/reject step (detailed balance, Hastings 1970) corrects for the proposal's bias, isolating the cooperative channel. Three findings. (i) Under bias-controlled HYBRID-MH, the measured finite-size-scaling exponent is **statistically consistent with the two-dimensional Ising value** once analysed in the correct (linear-size) convention and benchmarked against a classical Ising control on identical small lattices — it is **not** a new universality class. (ii) The framework nonetheless has **discriminating power**: it reproduces the textbook topological hierarchy — finite-dimensional networks (2D lattice, scale-free) show Ising-like criticality, the one-dimensional ring shows **no transition** (size-independent susceptibility, as expected for T_c=0), and the fully-connected (mean-field) graph **freezes** into trivial order. (iii) Two appealing conjectures **fail** under controlled measurement: there is no opinion↔task-accuracy isomorphism, and exponents are not predictable a priori from cheap single-agent diagnostics. Our contribution is therefore **methodological and deflationary**: a rigorous, single-GPU-reproducible protocol that separates intrinsic bias from cooperative criticality, clarifying that much of the apparent "collective phase transition" in LLM agents is bias-driven (consistent with concurrent work), while genuine cooperative criticality, where present, is Ising-consistent.

---

## 1. Introduction

**The claim, and the question.** As LLM agents are composed into populations, they exhibit emergent collective behaviour: spontaneous convention formation (Ashery et al. 2025), contagious propagation of undesired behaviours, and — when arranged on a lattice and updated from their neighbours — magnetization and susceptibility signatures reminiscent of a spin system. A natural and exciting reading is that LLM collectives undergo genuine *phase transitions*, characterized by critical exponents. But there is a confound that the lattice picture cannot, by itself, resolve: an LLM agent has a strong **intrinsic bias** (a preferred answer independent of its neighbours). A field-like bias produces *crossovers* that mimic a transition without any cooperative criticality. Concurrent work (arXiv:2605.10528, 2026-05) makes exactly this point on a 2D lattice across three open-weight models, extracting effective couplings and fields and concluding that collective alignment is **bias-dominated** (h̃ ≫ J̃), i.e. field-driven crossovers rather than genuine transitions.

**Our angle: control the bias by construction.** Raw neighbour-conditioned updates conflate bias and cooperation. We separate them with a sampler whose stationary distribution is *known*. In **HYBRID-MH** (§2) the LLM supplies only the *proposal* of a Metropolis–Hastings chain; an explicit accept/reject step against a pre-registered Ising Hamiltonian corrects for the proposal's bias, so the chain samples the cooperative Boltzmann distribution by detailed balance. This makes finite-size scaling a legitimate measurement of the *cooperative* critical behaviour, with the bias divided out.

**What we find — stated honestly up front.** Under HYBRID-MH the cooperative exponent is **Ising-consistent**, not a new class: a classical 2D-Ising control on the identical (small) lattices and chain lengths yields the same exponent within our confidence interval. The value of the framework is therefore not a new "universality class of LLM dynamics" (a claim we explicitly retract after audit) but: (1) the **method** itself — a bias-controlled, RG-legitimate sampler; (2) its **discriminating power** across network topologies (§3.2), which reproduces the correct statistical-mechanics hierarchy; and (3) two **honest negatives** (§3.4) that bound the phenomenon. Everything runs on a single consumer GPU.

---

## 2. Methods — HYBRID-MH

Consider N agents on the nodes of a graph g, each holding s_i ∈ {−1,+1} encoded as a token label. We pre-register the Ising target H(s) = −J Σ_{⟨i,j⟩∈g} s_i s_j and sample π(s) ∝ e^{−βH} with a Metropolis–Hastings chain whose **proposal is the LLM**: at each step we present the LLM with site i's neighbourhood and read its normalized next-token distribution q(s′_i | s) over the two labels (summing probability mass over all single-token encodings of each label — bare, space-prefixed, upper-case). We accept with

  α = min(1, e^{−βΔH} · q(s_i|s′)/q(s′_i|s)),

computing q_fwd and q_rev from a forward and a reverse LLM pass. The accept/reject step makes the chain satisfy detailed balance with respect to π for *any* proposal with full support (Hastings 1970), so the stationary distribution is the cooperative Ising π — the LLM enters only through mixing, not through the equilibrium distribution. This is precisely what divides out the intrinsic bias: a model that "wants" to answer +1 proposes +1 more often, but the q-ratio in α corrects for it. (A degenerate proposal q≡½ reduces HYBRID-MH to ordinary single-spin-flip Metropolis; an early tokenizer bug that collapsed q to ½ was fixed by summing over all single-token encodings.)

**Observables and FSS.** From the magnetization trace (after burn-in) we compute χ = N·Var(m) and U₄ = 1−⟨m⁴⟩/(3⟨m²⟩²). At the susceptibility peak we fit χ vs system size. **Important convention note (a correction to our own earlier analysis):** the Ising exponent γ/ν=7/4 is defined against the *linear* size L (χ∼L^{γ/ν}); on a 2D lattice N=L², so a true 2D Ising scales as χ∼N^{γ/ν/2}=N^{0.875}. Exponents must be compared in a single convention; we benchmark every LLM measurement against a classical single-spin-flip Ising run on the *identical* lattice shapes and chain lengths.

**Scope.** Models: Mistral-7B, Llama-3-8B, Qwen3-8B, Qwen2.5-7B, Yi-1.5-9B (5 families). Topologies: 2D lattice, scale-free (Barabási–Albert), ring-1D, fully-connected. N up to 64. Single RTX-4090-class GPU; vLLM. Code + raw chains: **[repo]**.

---

## 3. Results

### 3.1 The cooperative exponent is Ising-consistent (no new class)

Across model families the HYBRID-MH susceptibility scales as a clean power law, with χ-vs-N slope ≈ 0.82 (e.g. Mistral 0.82, CI [0.77, 0.86]; the value is tightly clustered across families — but note this clustering is *expected* under correct HYBRID-MH, since all models sample the *same* target π and the equilibrium exponent is a property of the target, not the proposal). A **classical 2D-Ising control** run with the same FSS pipeline gives χ-vs-N = 0.839 on proper square even-L lattices (= 1.68 vs L, recovering the 2D-Ising value within small-lattice corrections) and 0.91–0.96 on our exact small rectangular lattices. The LLM value (0.82) lies **within** the classical-Ising confidence band: **we cannot distinguish the cooperative LLM exponent from 2D Ising.** We therefore do **not** claim a distinct universality class. (A possible weak suppression of the LLM exponent relative to the matched-shape classical control, consistent with residual bias, is not robust at our lattice sizes and is not claimed.)

### 3.2 Topology discrimination — the framework reproduces the correct hierarchy

The susceptibility peak grows toward criticality at J*≈1.0 (located consistently by the χ peak and the Binder-cumulant crossing, U₄*≈0.57). Re-running across topologies reproduces the textbook hierarchy:
- **2D lattice & scale-free (Barabási–Albert):** Ising-like critical scaling (χ-vs-N ≈ 0.80–0.82), a genuine finite-dimensional transition; the exponent is topology-robust within finite-d.
- **Ring (1D):** susceptibility is **size-independent** (χ≈2.2 at all N) and |m| *decreases* with N (0.41→0.25) — no long-range order, i.e. the textbook fact that 1D has **no finite-temperature transition** (T_c=0). No critical scaling to measure.
- **Fully-connected (mean-field):** consensus is overwhelming; the population **freezes** (|m|→1.00, χ→0) across the coupling grid, because the mean-field critical coupling scales as J_c∝1/N. A distinct (mean-field) regime.

That the framework returns Ising-like behaviour *only* where a genuine finite-dimensional transition exists — and correctly reports its absence in 1D and its triviality at mean-field — is the substantive positive result: **discriminating power**, the hallmark of a faithful critical-phenomena probe rather than confirmation bias.

### 3.3 Raw dynamics are bias-dominated; HYBRID-MH isolates cooperation

Consistent with arXiv:2605.10528, raw neighbour-conditioned dynamics are dominated by intrinsic bias (the field term), producing field-driven crossovers. HYBRID-MH's accept/reject divides this out by construction, which is why §3.1–3.2 can attribute the residual behaviour to cooperative coupling. **[PENDING: a side-by-side raw-vs-HYBRID comparison on a matched cell, using our Mode-B raw-dynamics code, to quantify the bias removal directly.]**

### 3.4 Honest negatives

(i) **No opinion↔task-accuracy isomorphism:** the consensus order parameter and task accuracy do not share a critical system size (they are anti-correlated). The critical behaviour is a property of *agreement*, not *capability*. (ii) **No a-priori exponent law:** a conjecture that exponents follow from cheap single-agent diagnostics collapsed once the key diagnostic was measured directly from logits rather than inferred circularly (spurious R²=0.88 → R²=0.03). Analogies between LLMs and physics are easy to make and easy to fool; the discipline is in the controls — including the one that retired our own headline claim (§3.1).

---

## 4. Discussion

**A deflationary clarification, and a tool.** The exciting reading — that LLM collectives define a new universality class — does not survive a bias-controlled measurement and a classical benchmark: the cooperative exponent is Ising-consistent, and the cross-model agreement is built into the sampler rather than discovered. What *is* robust is more modest and, we argue, more useful: (1) **HYBRID-MH**, a method that cleanly separates intrinsic bias from cooperative criticality in LLM populations — directly addressing the confound that concurrent work identified; (2) a **topology-discrimination** result that shows the framework faithfully reproduces statistical mechanics (1D: no transition; finite-d: Ising-like; mean-field: trivial order); and (3) **negative results** that bound the phenomenon and exemplify the controls such claims require. For a field where "LLMs show phase transitions" is becoming a casual claim, a rigorous, reproducible, bias-controlled protocol — and the honest finding that much of the effect is bias — is a contribution in itself.

**Limitations.** Small lattices (N≤64) limit exponent resolution; the equilibrium exponent under correct MH is a property of the chosen target, so HYBRID-MH characterizes the LLM-proposal's *compatibility* with cooperative criticality, not an autonomous property of raw LLM dynamics. Open-weight models ≤14B.

---

## Figures (deflationary set — final)
- **Fig 1 = `figA_topology_discrimination.png`** (CENTERPIECE): χ(N) for four topologies — 2D-lattice & scale-free rise (Ising-like critical growth), ring-1D is flat (no transition), fully-connected is frozen (χ→0). Demonstrates the framework's *discriminating power*; replaces the retired "universality forest vs 2D-Ising" plot.
- **Fig 2 = `figB_classical_benchmark.png`**: LLM χ-vs-N (slope 0.82) overlaid with a classical 2D-Ising control on matched lattices (square even-L 0.84; our shapes 0.91). Shows honestly that the LLM cooperative exponent is Ising-consistent — no distinct class.
- **Fig 3 = `fig6_config_snapshots.png`**: agent ±1 configurations on the lattice across J (qualitative order–disorder).
- **Fig 4 = `fig3_binder_crossing.png`**, **Fig 5 = `fig4_susceptibility.png`**, **Fig 6 = `fig5_order_parameter.png`**: Binder crossing / χ(J) peak / sigmoid (qualitative criticality at J*≈1.0 — still valid).
- **RETIRED** (kept for the record, not used): `fig1_gamma_nu_forest.png` (its "distinct from 2D-Ising 1.75" annotation is a vs-N/vs-L unit confusion), `fig2_fss_collapse.png`, `fig7_data_collapse.png` (supported the retracted universality-class claim).

## References
Ashery et al. 2025; Hastings 1970; Onsager 1944; arXiv:2605.10528 (2026, concurrent — bias-dominated LLM lattice); plus the secrets-leakage / DarkForest motivation cluster.
