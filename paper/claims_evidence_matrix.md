# Phase 5 — Claims ↔ Evidence Matrix (post-execution, honest)

**Project:** DTPU — Multi-Agent LLM criticality
**Date:** 2026-06-01 → **REVISED 2026-06-03 (major retraction)**

> ⚠️ **2026-06-03 RETRACTION (competitor-triggered audit).** The headline claim **C1 — "a distinct universality class γ/ν≈0.82, excluding 2D Ising 1.75" — is RETRACTED.** Two reasons: (a) a **vs-N / vs-L unit confusion** (our χ-vs-N exponent 0.82 ⇒ 1.64 vs L, *close to* Ising 1.75, not excluding it); (b) a **classical 2D-Ising control** on identical small lattices gives χ-vs-N = 0.839, **inside** our CI [0.77,0.86] → LLM exponent is **statistically indistinguishable from 2D Ising**. Also, cross-model agreement is **built into** HYBRID-MH (all sample the same target π), not a discovery. Concurrent work arXiv:2605.10528 (2026-05) independently scooped the broad framing and reached the bias-domination conclusion. See `compact/rigor_audit_findings.md`.
>
> **Revised defensible paper (deflationary methods paper):** **(M) HYBRID-MH** = bias-controlled RG-legitimate sampler (the method, real); **(T) topology DISCRIMINATION** = qualitative hierarchy 1D-no-transition / finite-d-Ising-like / MF-frozen (robust, independent of the exponent value); **(N) honest negatives** (no isomorphism, no predictive law). NOT a new universality class. NOT Nature-tier. Target: methods/physics venue or workshop.

**(Original 2026-06-01 status, now superseded:)** post-rigor-audit synthesis superseding the pre-execution 4-claim plan. C2, C3 falsified. C1 was thought to survive as a discovery — **but C1 is now also retracted (see above).**

---

## 0. One-line on what changed vs the plan

The synthesis card promised a 4-claim *unification* (universality ⊕ isomorphism ⊕ predictive-law ⊕ leakage-gating). Execution + adversarial self-audit (break-circularity h̃ measurement, bootstrap CIs, multi-seed FSS) **confirmed C1 and falsified C2 and C3**. We do **not** inflate the surviving scope: the paper is now a *discovery + methods* paper, not a unification paper. The falsifications are a credibility asset, not a loss — they show the framework is genuinely falsifiable and that we held it to that standard.

---

## 1. The matrix

| Claim | Original tier (plan) | Evidence (what was run) | Verdict | Confidence | Role in revised paper |
|-------|---------------------|-------------------------|---------|-----------|----------------------|
| **C1 — LLM-population universality class** (χ ∝ N^{γ/ν}, γ/ν≈0.82 invariant across model families; distinct from mean-field 1.0 and 2D-Ising 1.75) | primary | HYBRID-MH FSS on 6 high-stat cells (Mistral, Llama-3×2, Qwen3, Qwen2.5×2), N∈{8,16,24(,32)}, peak-J, bootstrap CI. **+ pending rigor**: cross-topology (3), larger-N (48/64), temp (3). | **CONFIRMED** | HIGH (6/6 CIs contain 0.82, all exclude MF & Ising; mean 0.800, σ=0.051) | **PRIMARY contribution.** Fig 1 (forest), Fig 2 (FSS collapse). Strengthened (not gated) by pending topology/temp/largeN. |
| **HYBRID-MH** (LLM proposal q + explicit Metropolis–Hastings accept/reject against Ising H_target ⇒ provably samples π_Ising by Hastings 1970 ⇒ Wilson-RG-legitimate FSS) | method (under C1) | Derivation P1 v3/v4; implementation `llm_mcmc/hybrid_mh.py`; token-id-sum bug fix that made q non-degenerate; detailed-balance check. | **CONFIRMED (method)** | HIGH (textbook detailed balance; the reason C1's RG claim is legitimate rather than hand-wavy) | **METHODOLOGICAL contribution.** The key novelty that elevates "LLMs show scaling" to "measured critical exponents of a legitimate RG flow". |
| **C2 — opinion-dynamics ↔ task-accuracy isomorphism** (N*_ψ ≈ N*_acc) | primary | Mode-B raw dynamics; EA-overlap ψ; Binder N* for ψ vs task-accuracy; per-task-class Δ_critical. | **FALSIFIED** | HIGH (ψ and task-accuracy **anti**-correlated; no shared critical N*) | **HONEST NEGATIVE.** Reported in a "what does *not* transfer" subsection. Bounds the universality claim: the critical scaling is in the *consensus/magnetization* observable, NOT in task performance. |
| **C3 — a-priori predictive law** (cheap single-agent diagnostics h̃ ⇒ predicted exponents) | supporting / L4-upgrade lever | P3 analytic map; direct h̃ from logits on balanced-neighbor prompts (`measure_h_tilde.py`) to break circularity; refit. | **FALSIFIED** | HIGH (R²=0.030 with directly-measured h̃ vs spurious R²=0.881 with circular proxy) | **HONEST NEGATIVE.** Reported as a falsified conjecture + a cautionary note on circular proxies in LLM-physics analogies. |
| **C4 — leakage / confound falsification battery** (rule out that "universality" is a prompt-leakage artifact: obscurity-monotonicity, paraphrase, synthetic-mechanism controls) | supporting, GATING | `tasks/c4_controls.py`, `sanity/c4_runner.py` (Phase-4 run). | **PENDING-VERIFY** | MED (implemented + run; verdict not yet re-extracted post-audit) | **ROBUSTNESS control.** Must re-confirm from c4 outputs that γ/ν≈0.82 survives the controls before final submission. Action item below. |
| **C5 — saturation-aware framing** | auxiliary | — (framing only) | **AUXILIARY** | n/a | Intro/discussion framing only; no empirical load. |

---

## 2. Revised paper scope (honest)

**Title (working):** *A Universality Class for LLM Collective Dynamics*

**Thesis (≤25 words):** *N-LLM populations driven by a Metropolis–Hastings-legitimate sampler exhibit a single critical universality class (γ/ν ≈ 0.82), invariant across model families, distinct from mean-field and 2D-Ising.*

**Contribution stack:**
1. **Discovery (C1):** the γ/ν≈0.82 universality class — robust across ≥4 model families (target 6–8 cells) and (pending) across topologies and temperatures.
2. **Method (HYBRID-MH):** explicit MH accept/reject with an LLM proposal, making finite-size-scaling exponent extraction RG-legitimate rather than analogical.
3. **Honest negatives (C2, C3):** no opinion↔task isomorphism; no a-priori h̃ predictive law. These *delimit* the claim and demonstrate falsifiability.

**What we explicitly do NOT claim:** universality of *task performance*; a predictive a-priori exponent law; a single-system empirical bridge between the two communities (the original dual-track unification).

---

## 3. Evidence still pending (rigor campaign, rigor-first ordering)

| Pending experiment | Strengthens | Why it matters | Gate? |
|--------------------|-------------|----------------|-------|
| Cross-topology (scale-free, fully-connected, ring-1D) | C1 | γ/ν topology-independence ⇒ *stronger* universality claim than "more models" | No (enriches) |
| Larger-N (48, 64) → 5-point FSS curve | C1 | pins ν, enables the data-collapse figure (Fig 3) | No (enriches; needed for ν) |
| Temperature sweep (T=0.5/0.7/1.3) | C1 | robustness of the class to sampling temperature | No |
| yi_01, internlm_01 (2 more families) | C1 | breadth → 8-cell model spectrum | No |
| **C4 control re-extraction** | C1 robustness | confirm γ/ν survives leakage/paraphrase/obscurity controls | **Yes — must verify before submission** |

---

## 4. Integrity log (why the negatives are a strength)

- The h̃-law (C3) looked strong (R²=0.881) **only because the proxy was circular** (h̃ inferred from the same dynamics it was predicting). We built a direct, dynamics-free logit measurement (`measure_h_tilde.py`), and the law collapsed to R²=0.030. We report this.
- The γ/ν "spectrum" (0.35–0.99) that briefly looked like a *spread of classes* was **noise from 3 seeds**; at 10 seeds × 2500 sweeps all CIs collapse onto ≈0.82. We report the high-stat result, not the noisy one.
- C2 isomorphism was demoted from a headline to a falsified negative when ψ and task-accuracy came out anti-correlated.
- **Standard applied:** a claim survives only if its bootstrap CI excludes the competing hypotheses and survives a break-circularity / multi-seed re-test.

---

## 5. Action items before Phase 9 (paper writing)

1. **[blocking]** Re-extract C4 control verdict from `sanity/c4_runner` outputs; confirm γ/ν≈0.82 holds under controls.
2. **[on data]** Re-run `full_spectrum.py` + `make_figures.py` when rigor cells land → final Fig 1/2 + new Fig 3 (data-collapse, ν).
3. **[on data]** Merge largeN48/64 into the Mistral anchor FSS curve to report ν with a CI.
4. **[writing]** Methods §: HYBRID-MH detailed-balance derivation (from P1 v3/v4 cards).
5. **[writing]** Intro motivation cluster: emergent collective LLM dynamics are real but only empirically described (secrets-leakage contagion arXiv:2605.27766; DarkForest "more communication is worse") — we give the physics.
