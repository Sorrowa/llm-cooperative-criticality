# Rigor Audit Findings (2026-05-28) — Critical Honest Assessment

User asked "is the evidence rich enough?" → chose path A (do experiments thoroughly).
First two rigor checks (P1 break-circularity + bootstrap CI) FALSIFIED the headline results.

## Finding 1: C3 predictive law is an artifact of circular h̃ proxy

Original (proxy h̃ derived from consensus baseline):
- γ/ν = 1/(1+2.58·h̃), R²=0.881, Spearman -1.000 (p<0.0001), LOO within-20%=100%

After DIRECT h̃ measurement from logits (balanced-neighbor prompts, no dynamics → no circularity):
| cell | |h̃|_measured | γ/ν |
|------|-------------|-----|
| mistral_01 | 0.000 | 0.99 |
| qwen3_01 | 0.206 | 0.566 |
| qwen25_AB | 0.207 | 0.56 |
| llama3_AB | 0.224 | 0.79 |
| qwen25_01 | 0.649 | 0.35 |
| llama3_01 | 0.922 | 0.80 |

Re-fit: R²=0.030, Spearman -0.257 (p=0.62, NOT significant), LOO within-20%=33%.
**CONCLUSION: the h̃→γ/ν law does NOT survive circularity removal. It was spurious.**
llama3_01 has highest measured h̃ (0.92) but high γ/ν (0.80) — breaks monotone.

## Finding 2: γ/ν spread across cells is NOT statistically distinguishable

Bootstrap 95% CI (resample 3 seeds, refit γ/ν via peak-J log-log):
| cell | γ/ν | 95% CI | width |
|------|-----|--------|-------|
| Mistral+0/1 | 0.98 | [0.83, 1.13] | 0.30 |
| L3+A/B | 0.97 | [0.74, 1.26] | 0.51 |
| Q3+0/1 | 0.75 | [-0.03, 1.26] | 1.28 |
| Q2.5+A/B | 0.61 | [-0.72, 0.97] | 1.68 |
| L3+0/1 | 0.39 | [-1.43, 1.60] | 3.03 |
| Q2.5+0/1 | 0.59 | [-3.19, 0.94] | 4.12 |

**ALL pairwise CIs overlap → no two cells distinguishable. The "0.35-0.99 spread" is consistent with pure noise.**

## Root cause: insufficient statistics per cell
- 3 seeds (need 20-50)
- N range 8-32 (factor 4; need decade: 8-96/128)
- 1000 sweeps (critical slowing → N_eff ~20)

## What remains solid
- HYBRID-MH protocol: rigorous Wilson-RG-legitimate sampler (textbook MH detailed balance) — this is the durable methodological contribution
- Critical-like behavior exists (χ peak growth >1.5× in all cells, J*_c clusters ~1.0)
- β/ν ≈ 0 across cells (MF-like signature) — but also uncertain given CIs

## Three possibilities (path C will discriminate)
1. γ/ν varies but noise-buried → high-stat reveals it → Nature MI story
2. γ/ν ≈ constant ≈ 1 (all MF) → weaker but honest "AI populations are MF-like" finding
3. LLM-MH intrinsically too noisy → no clean exponents → pivot to method-only paper

## Path C feasibility test (LAUNCHED 2026-05-28)
Mistral+0/1, N∈{8,16,24,32}, J∈{0.92,1.0,1.08}, 10 seeds (vs 3), 2500 sweeps (vs 1000).
Dual-GPU split (A: seeds 42-46, B: seeds 47-51). ~1.3 days.
DECISION RULE: if bootstrap γ/ν CI width shrinks below ~0.3 AND can distinguish MF(1.0) from non-MF → path A viable, scale to 5 new models (DeepSeek/Qwen2.5-3B/14B/Yi/InternLM already downloaded). Else → pivot to method paper (path B).

---

## PATH C VERDICT (2026-05-29): PASS — signal is REAL

Mistral+0/1 high-stat (10 seeds × 2500 sweeps × 4N{8,16,24,32} × 3J), 102/120 chains:
- γ/ν = 0.763, 95% CI = [0.731, 0.866], width = 0.136 (was 0.30 at 3 seeds)
- **EXCLUDES mean-field (γ/ν=1.0)** — upper bound 0.866 < 1.0
- **EXCLUDES 2D Ising (γ/ν=1.75)**
- Per-(N,J) cell std small (0.09-2.0) → chain-to-chain variance controllable; the earlier "huge error bars" were a seed-count artifact, NOT intrinsic LLM noise

**CONCLUSION: γ/ν is a real, measurable, non-trivial exponent (~0.76), distinct from both MF and 2D Ising.
Path A is viable. The high-statistics protocol (10 seeds, 2500 sweeps) resolves the signal.**

DECISION: launch 9-cell high-stat campaign (5 original cells re-run + 4 new models:
DeepSeek-V2-Lite, Qwen2.5-3B, Qwen2.5-14B, Yi-1.5-9B, InternLM2.5-7B) to test whether
γ/ν VARIES across LLMs (→ tunable-universality story) or is CONSTANT ≈0.76 (→ universal
"LLM-population class" story). Either outcome is now publishable at NMI/NC tier because
the exponent is cleanly resolved.

### Path C FINAL (120/120 chains, 2026-05-29)
γ/ν = 0.821, 95% CI = [0.768, 0.864], width = 0.095 (vs 0.30 at 3-seeds = 3× shrink)
EXCLUDES mean-field (1.0) AND 2D Ising (1.75). Signal definitively real.
Mistral+0/1 γ/ν = 0.82 ± 0.05 — a clean, non-trivial, novel exponent.
→ 10-cell HS campaign launched (llama3_01 first). Will test variation vs constancy of γ/ν across LLMs.

### C2 isomorphism — FINAL DEMOTE TO HONEST NEGATIVE RESULT (2026-05-29)
40-chain Qwen2.5+0/1: ψ_by_N = {8:0.375, 12:0.115, 20:0.05, 32:0.077} (decreasing);
acc_by_N = {8:0.699, 12:0.851, 20:0.837, 32:0.85} (increasing). Spearman(ψ,acc)=-0.2, p=0.8.
ψ and task-accuracy are ANTI-correlated, NOT two projections of one critical phenomenon.
The C2 isomorphism hypothesis is FALSIFIED. This is reported as an honest negative result
(not a measurement artifact): the transcript order parameter and downstream task success
do not share a critical N*. Paper narrative: this RULES OUT the naive "unification" of the
opinion-dynamics and performance-scaling literatures via a shared order parameter — itself
a publishable clarifying finding.

## REVISED PAPER NARRATIVE (post-rigor)
PRIMARY (solid): HYBRID-MH rigorous Wilson-RG protocol for LLM populations + clean measurement
  of a novel exponent γ/ν≈0.82 (Mistral, distinct from MF and 2D Ising).
SECONDARY (pending 10-cell): whether γ/ν varies across LLMs (tunable) or is constant (universal class).
NEGATIVE (honest): C2 isomorphism falsified; C3 h̃-law spurious under direct measurement.
This is a HONEST, RIGOROUS paper — weaker than the initial "tunable universality law" hype
but defensible at NMI/NC. The rigor self-corrections (breaking circularity, bootstrap CIs)
are themselves a methodological strength reviewers will respect.

### UNIVERSALITY CONFIRMED — 4-cell consistency (2026-05-31)
High-stat γ/ν across 3 model families × 2 prompts:
| Cell | model | γ/ν | 95% CI |
|------|-------|-----|--------|
| Mistral+0/1 | Mistral-7B | 0.821 | [0.768, 0.864] |
| Llama3+0/1 | Llama-3-8B | 0.816 | [0.787, 0.848] |
| Llama3+A/B | Llama-3-8B | 0.809 | [0.742, 0.963] |
| Qwen3+0/1 | Qwen3-8B | 0.833 | [0.757, 0.907] |

ALL CIs overlap at γ/ν≈0.82. ALL exclude MF (1.0) and 2D Ising (1.75).
→ STRONG evidence for a UNIFIED LLM-population universality class γ/ν≈0.82,
invariant across architecture (Mistral/Llama/Qwen) AND prompt (A/B vs 0/1).
This is textbook universality: disparate microscopic systems → identical critical exponent.
β/ν≈0 across all (MF-like) but γ/ν≈0.82≠1 (NOT pure MF). A new "cognitive-agent" class.
Remaining 5 cells (qwen25×2, deepseek, yi, internlm) in progress to confirm.

## FINAL PAPER NARRATIVE (locked)
TITLE direction: "A Universality Class for LLM Collective Dynamics"
PRIMARY: (1) HYBRID-MH rigorous Wilson-RG protocol; (2) a clean universality class
  γ/ν≈0.82, β/ν≈0, invariant across LLM architecture+prompt, distinct from MF and Ising.
NEGATIVE (honest): C2 isomorphism falsified; C3 h̃-tuning-law spurious (no per-LLM variation).
The story SHIFTED from "tunable exponents" (hyped, falsified) to "universal class" (cleaner, true).

### Data collapse (②) + Binder cumulant (④) analysis (2026-05-31, zero-GPU)
Two INDEPENDENT universality fingerprints both agree across 4 cells:
- gamma/nu (collapse): 0.856, 0.856, 0.955, 0.861 (consistent with chi-peak's 0.82)
- Binder U4 at criticality: 0.56-0.58 across ALL N and ALL cells — STABLE universal value
  (U4* is itself a universality-class fingerprint; same ~0.57 across models = strong signal)

PROBLEM: nu (correlation-length exponent) is NOT well-determined:
- Mistral/Qwen3 collapse gives nu=2.0; Llama3 gives nu=0.67 (3x discrepancy)
- Root cause: N range only 8-32, too narrow to pin nu. Collapse insensitive to nu at small N.
- The 3-exponent data collapse cannot yet produce a clean single master curve.

IMPLICATION: larger N (48, 64) is now REQUIRED (not optional) to:
  (a) pin nu reliably, (b) make the data-collapse figure publication-grade.
This is the key remaining experiment. Reviewers will demand a clean collapse for a
universality claim. Plan: anchor model (Mistral) at N up to 64, then re-do collapse.

### Remaining GPU experiments queued (for universality rigor):
① cross-topology (scale-free, fully-connected, 1D ring) on anchor — tests exponent invariance
③ T_temp sweep (0.5, 0.7, 1.0, 1.3) — probes sampling-noise dependence
⑤ larger N (48, 64) on anchor — REQUIRED to pin nu + clean collapse (upgraded from optional)

### Related work to cite (user-surfaced 2026-06-01)
"Got a Secret? LLM Agents Can't Keep It" (Priyanshu/Vijay/Pahwa, arXiv:2605.27766, 2026-05)
- Reddit/Moltbook multi-agent social sim: 2533 agents, 124 subreddits, 25 sim-days
- KEY FINDING: privacy leakage is CONTAGIOUS — 8× amplification (leak after a leaked reply: 12.8%
  vs after clean: 1.6%, baseline 1.8%, Fig 6). Single→multi-turn social: 19.95%→45.30% (RQ1).
- This is the TWIN of our work on a DIFFERENT observable:
  THEM: privacy-leak contagion = a social epidemic (measured via LLM-as-judge macro rates)
  US: consensus/magnetization critical phase transition (measured via FSS critical exponents)
  BOTH establish: multi-LLM-agent populations have emergent collective dynamics invisible to single-agent eval.
- CITATION ROLE (Phase 9 intro): they = the PHENOMENON (emergent collective dynamics is real),
  we = the THEORY (it obeys a statistical-physics universality class).
- DEEPER LINK (discussion): epidemic/percolation models share critical exponents with our universality;
  their 8× contagion hints the system sits near a percolation critical point. Our framework could
  in principle predict such contagion thresholds. (speculative, discussion only)
- Pairs with DarkForest (2026-05-28, "more communication is worse") as motivation cluster:
  collective LLM dynamics are real, consequential, and previously only described empirically — we give the physics.
- NOT an experiment gap; cite-and-position only. User's air-ground-swarm transfer hook is a SEPARATE project.

### Incident log: deepseek_rerun collision (2026-06-01 ~02:37-03:48 UTC)
- deepseek_rerun.sh had a BROKEN gate — fired at 02:47 while eco_pipeline still running qwen25_3b_01.
- DeepSeek STILL crashes on this box even after config re-download: "RuntimeError: Engine core
  initialization failed" (vLLM EngineCore init). DeepSeek = confirmed casualty, dropped from dataset.
- Its premature vLLM launch collided with qwen25_3b_01's GPU → killed qwen's EngineCore →
  qwen25_3b_01 A/B sa3 parents hung on dead engine (alive 2h19m, no log progress 1h9m, GPU idle).
- RECOVERY (03:48 UTC): killed hung qwen25_3b_01 procs (447147/447148) → eco_pipeline `wait` returned →
  auto-advanced to yi_01 (cell 7). GPU clean, yi_01 launched healthy.
- qwen25_3b_01 LOST: only completed N=8 block (24 chains, N=8 × J{0.92,1.0,1.08} × 8 seeds) before
  collision; never reached N=12/16/20/24 → NOT FSS-analyzable (single-N, no slope). Bonus 3B cell,
  immaterial to spectrum (6 valid cells already). Can re-run cleanly by hand post-cascade if wanted.
- LESSON: no premature-launch "rerun" scripts while a pipeline holds the GPU. The eco→diverse→rigor
  gates work correctly (diverse/rigor still waiting); only deepseek_rerun's gate was broken (now dead, DONE=1).

### Scope decision: RIGOR-FIRST (user, 2026-06-01 ~06:28 UTC)
- Discovered pace = ~12h/cell (confirmed from completed eco cells: llama3_AB/qwen3/qwen25/qwen25_AB each ~12h).
- Full original queue (yi, internlm, +3 diverse models, then rigor incl. largeN48/64) ≈ 10-14 days dual-GPU → budget risk (≤$300).
- Core result ALREADY locked: γ/ν≈0.82 across 4 model families (Mistral/Llama3/Qwen3/Qwen2.5), 6 cells, CIs overlap.
- USER CHOSE "Rigor-first": let eco finish (yi_01→internlm_01 = 8-cell model spectrum), SKIP the 3 diverse
  models (phi35/falcon3/olmo2), jump to rigor. Rationale: cross-topology (γ/ν topology-independence) +
  larger-N (pins ν + data-collapse figure) STRENGTHEN the paper more than +3 redundant model families.
- IMPLEMENTATION: killed diverse_pipeline.sh + old rigor_pipeline.sh waiters; installed rigor_pipeline_v2.sh
  gated on eco (not diverse) with anti-collision GPU-free check. New cascade: eco→rigor_v2 (~2 days rigor).
- Rigor set (Mistral anchor, already downloaded): largeN48, largeN64 (N→5-pt FSS curve 8/16/24/48/64),
  topo_scale_free, topo_fully_connected, topo_ring_1d, temp_0_5, temp_0_7, temp_1_3 — run 2-per-GPU.
- Final model spectrum target: 8 cells (Mistral, Llama3×2, Qwen3, Qwen2.5×2, yi, internlm). Diverse 3 = dropped.
- KEY UPCOMING TRANSITIONS to monitor: (1) yi→internlm ~16:00 Jun1; (2) eco→rigor_v2 ~04:00 Jun2 (CRITICAL: verify rigor launches clean on freed GPU).

### MILESTONE: eco complete, 7-cell spectrum, rigor launched (2026-06-01 18:34 UTC)
- eco pipeline DONE. yi_01 (Yi-1.5-9B) completed: γ/ν=0.826, CI=[0.811,0.923], 72 chains, N={8,16,24}.
- 7-cell spectrum (5 model families: Mistral, Llama3, Qwen3, Qwen2.5, Yi):
  Mistral 0.821, Llama3+0/1 0.816, Llama3+AB 0.809, Qwen3 0.833, Qwen25+0/1 0.687, Qwen25+AB 0.833, Yi 0.826.
  mean=0.804 std=0.048; ALL 7 CIs contain 0.82; ALL exclude MF(1.0) and 2D-Ising(1.75). Universality HOLDS.
- internlm_01 CRASHED (58s): OSError missing configuration_internlm2.py (same *.py-excluded-from-download
  issue as deepseek). FIXABLE casualty but bonus 6th family; per rigor-first NOT chased now. To recover
  later: download internlm2 config .py files, re-run cleanly post-rigor.
- CRITICAL eco→rigor handoff SUCCEEDED: rigor_pipeline_v2 anti-collision gate worked perfectly. Launched
  viz_jsweep (GPU0, pid 517349) + largeN48 (GPU1, pid 517348), both loaded + running chains, GPU 88-89%, NO collision.
- Figures regenerated: fig1 forest now 7 cells (Yi added, on the line). spectrum_results_7cell JSON saved.

### CANONICAL critical-phenomena figures from viz_jsweep wide-J (2026-06-02 ~05:15 UTC)
- viz_jsweep N=8/16/24 FULLY done (7 wide-J [0.2-1.5] × 3 seeds each); N=32 still running.
- Rendered canonical Fig3-6 (supersede coarse 3-J versions), source figdata_jsweep_20260602.json:
  * Fig4 χ(J): CLEAR susceptibility PEAK at J*≈1.0 (N=24 χ=10.95 @ J1.0, drops to 4.57 @ J1.2),
    peak sharpens+grows with N (N=8 broad ~6 → N=24 sharp ~11) = textbook finite-size divergence.
  * Fig3 Binder U4(J): clean 3-curve CROSSING at J*≈0.95-1.0, U4*≈0.57 (matches the known U4≈0.57).
  * Fig5 |m|(J): full sigmoid 0.20→0.97 (disorder→consensus).
  * Fig6 snapshots (N=24, 4×6): J=0.2 genuinely DISORDERED (|m|=0.20), J=1.0 partial, J=1.5 full consensus.
- KEY: TWO independent J* estimates (χ peak + Binder crossing) BOTH ≈1.0 — strong cross-validation of the critical point.
  Refines the earlier narrow-grid "peakJ=1.08" (which was just the edge of a 3-point grid). True J*≈1.0.
- Pending: N=32 (refine + snapshots at N=32) + largeN48/64 (ν + Fig7 data-collapse). Archive viz raw chains when N=32 done.

### largeN48 done + largeN64 trimmed (2026-06-02 09:30 UTC)
- largeN48 (N=48) COMPLETE, χ@J=1.0=18.77, |m|=0.65 (5 seeds). FSS extends: χ(N=24→48) ratio 18.77/10.95=1.71 ≈ 2^0.77, consistent with γ/ν≈0.82. Universality HOLDS at N=48.
  NOTE: largeN48 narrow grid {0.92,1.0,1.08} has χ still rising at 1.08 (26.91) → true N=48 peak ≥1.08; use J=1.0 (common w/ viz) as the FSS coupling for the collapse.
- largeN64 TRIMMED before launch: J_multipliers [1.0,1.08], seeds 3 → 6 chains (~15h) vs original 15 chains (~37h). Saves ~22h, unblocks topology experiments (key topology-independence claim) ~22h sooner. N=64 is a marginal 6th FSS point (already have N=8/16/24/32/48).
- GPU1 idle after largeN48 = benign pipeline barrier (wait $PA on viz_jsweep); not a hang. viz_jsweep N=32 at 14/21, GPU0 87%.

### Fig7 data-collapse (preliminary, 2026-06-02 20:25 UTC)
- largeN64(trim) done: N=64 χ@J=1.08=35.68 (3 seeds). FSS χ@J=1.08 over N=8..64: 5.77/10.78/13.84/18.44/26.91/35.68.
- Fig7 built (fig7_data_collapse.png): (a) FSS log-log slope γ/ν=0.87 CI[0.81,0.96] over 8× size range (CI contains model-spectrum 0.82 → consistent; J=1.08 sits slightly above peak J*≈1.0 so γ/ν reads a touch high). (b) data collapse of viz wide-J (N=8,16,24,32) χN^-γ/ν vs (J-J*)N^(1/ν), J*=1.0, best-collapse ν≈1.55 — DISTINCT from 2D-Ising(ν=1) and mean-field(ν=0.5), supports own universality class. Disordered+peak collapse well; ordered tail noisier (slow mixing).
- PRELIMINARY (largeN64 trimmed 3 seeds); refine when largeN64_full (largeN64_A+B, 5 seeds) done.
- FSS data saved: paper/results/data/fss_largeN.csv. Script: figures/make_fig7.py.

### TOPOLOGY-INDEPENDENCE result: scale-free = lattice (2026-06-02 23:48 UTC)
- scale_free pair DONE (RIGOR_DONE=2). mistral_scale_free (Barabási-Albert) γ/ν=0.804 CI[0.755,0.900] peakJ=1.0.
- SAME as 2D lattice (≈0.82): CI contains 0.82, excludes MF(1.0). UNIVERSALITY IS TOPOLOGY-INDEPENDENT.
  This is a MAJOR strengthening — exponent independent of network structure (hub-network vs regular lattice), not just model.
- 8-cell forest (fig1 regenerated): 7 model cells + Mistral/scale-free, all on 0.82. mean=0.804.
- NOW RUNNING: fully_connected + ring_1d (pair 3). fully_connected = mean-field-like (expect γ/ν→1.0, the controlled
  EXCEPTION that proves the framework can distinguish classes); ring_1d = 1D (may differ from 2D). Then temps. Then largeN64_full.
- scale_free raw chains archived (36). manuscript §3.2 updated.

### TOPOLOGY hierarchy: framework DISCRIMINATES classes (2026-06-03 11:20 UTC, RIGOR_DONE=3)
- fully_connected + ring_1d pairs DONE. Results are RICHER than expected — the controls behave as physics demands:
  * mistral_fully_connected: |m|→0.98-1.00 (FROZEN ordered), χ→0 at all N,J. apparent γ/ν=-20.9 = artifact of χ→0,
    NOT an exponent. Physics: mean-field J_c∝1/N → at fixed J grid the MF system is deep ordered → no fluctuations.
    Distinct (mean-field) class; its critical point is outside the fixed-J window.
  * mistral_ring_1d: χ FLAT ~2.2 across N=8,16,24 (N-independent); |m| DECREASES 0.41→0.25. apparent γ/ν≈0 = NO
    critical scaling. Physics: 1D Ising has T_c=0, NO finite-T transition. Correct.
- COMPLETE topology hierarchy (textbook stat-mech): 2D-lattice 0.82 + scale-free 0.80 (finite-d, the CLASS);
  ring-1D = no transition (χ flat); fully-connected = mean-field trivial order (χ→0). The framework DISCRIMINATES —
  finds 0.82 ONLY where a genuine finite-d transition exists. STRONGER than "all topologies=0.82" (which would be suspect).
- IMPORTANT: do NOT put fully_connected/ring_1d on the main γ/ν forest (their -20.9/-0.05 aren't exponents). They go in a
  topology-DISCRIMINATION discussion/table (topology_comparison.csv saved). full_spectrum.py "All CIs contain 0.82?=False"
  is EXPECTED now (controls included) — the universality verdict applies to finite-d cells only.
- manuscript §3.2 rewritten with the honest hierarchy. both cells archived (820 total raw chains).
- NOW RUNNING: temp_0_5 + temp_0_7 (pair 4). Then temp_1_3. Then largeN64_full.

### CRITICAL: central "distinct universality class" claim FAILS — vs-N/vs-L unit error (2026-06-03, competitor-triggered)
- Competitor arXiv:2605.10528 (2026-05) scooped the core framing (2D-lattice LLM-Ising, FSS γ/ν, multi-model incl mistral:7b,
  h̃/J̃ extraction). Their conclusion: h̃≫J̃, bias-dominated, "field-driven crossovers NOT genuine phase transitions."
- Forced a stress-test of OUR central claim "γ/ν≈0.82 distinct from 2D-Ising 1.75". RAN classical 2D-Ising MC control
  (code/analysis_pipeline/classical_ising_control.py, pure CPU, known model):
  * UNIT ERROR found: our γ/ν is fit as χ vs N (#agents). 2D-Ising γ/ν=1.75 is vs LINEAR size L; since N=L^2,
    a TRUE 2D Ising gives χ~N^{1.75/2}=N^0.875 (vs N), NOT 1.75. So "0.82 excludes 1.75" compares vs-N to vs-L = INVALID.
  * Classical 2D Ising IN OUR EXACT REGIME (lattice shapes N=8/16/24/32, 2000 sweeps, β=0.4, J-swept): χ-vs-N slope = 0.98.
    Our LLM gives 0.82. So LLM is BELOW classical-Ising-in-regime (bias suppression, consistent w/ competitor) but the
    regime is too crude (even classical Ising gives 0.69-0.98 depending on L-range) to claim a DISTINCT class.
- VERDICT: the headline "new universality class γ/ν≈0.82 distinct from 2D-Ising" is NOT defensible (unit confusion +
  small-L indistinguishability). MUST drop/reframe.
- SURVIVES: (1) HYBRID-MH method (RG-legitimate sampler, real novelty, answers competitor's bias critique);
  (2) topology DISCRIMINATION — QUALITATIVE & robust (1D χ flat=no transition, MF χ→0 frozen, finite-d has peak),
  independent of the precise exponent; (3) honest negatives C2/C3; (4) cross-model qualitative robustness.
- DOES NOT survive: the quantitative "0.82 universality class distinct from Ising" headline.
- Strategy decision pending (user). Experiments (temp, largeN64_full) still running — data still useful for topology/qualitative story.

### SALVAGE VERDICT: quantitative claim NOT recoverable (2026-06-03, classical_ising_v2.py)
- Reliable vectorized classical 2D-Ising baseline (wide J to capture true peak, long chains):
  * A. proper square even-L (L=4-16, 6000 sweeps): γ/ν vs N=0.839, vs L=1.678 (≈ theory 1.75 → PIPELINE VALIDATED).
  * B. our lattice shapes, 2000 sweeps: γ/ν vs N=0.906. C. our shapes, 8000 sweeps: 0.958.
  * LLM-HYBRID-MH: 0.82 (CI [0.77,0.86]).
- VERDICT: proper-square classical Ising (0.839 vs N) is INSIDE our LLM CI → LLM exponent STATISTICALLY CONSISTENT with 2D Ising.
  No distinct universality class. Also: under correct HYBRID-MH detailed balance, ALL models sample the SAME target π_Ising,
  so "same exponent across models" is BUILT-IN (trivial), not a discovery.
- Only weak signal: in matched lattice shapes, LLM 0.82 < classical 0.91-0.96 (~0.1 suppression, consistent w/ competitor's
  bias-domination); but baseline unconverged (0.91→0.96 w/ chain length) and small-L too crude → not headline-worthy.
- SURVIVING contributions: HYBRID-MH method; topology DISCRIMINATION (qualitative: 1D no-transition / MF frozen / finite-d Ising-like);
  honest negatives. HONEST FRAMING = deflationary: "most LLM-agent 'phase transitions' are bias-driven (cf competitor); under
  bias-controlled HYBRID-MH the dynamics are Ising-consistent; value is methodological + topological discrimination." Modest, not Nature.
