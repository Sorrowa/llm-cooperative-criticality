#!/usr/bin/env python3
"""Two HONEST figures for the deflationary methods paper (2026-06-03 reframe):
  figA: topology DISCRIMINATION — chi(N) for 4 topologies; the framework reproduces stat-mech
        (finite-d Ising-like / 1D no-transition / mean-field frozen). This is the centerpiece.
  figB: classical-control BENCHMARK — LLM chi-vs-N vs a classical 2D-Ising control on matched
        lattices; shows the LLM cooperative exponent is Ising-consistent (no distinct class).
All numbers are measured (chi at J=1.08; classical from classical_ising_v2.py).
"""
import os, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

# --- measured chi(N) at J=1.08 (Mistral anchor / topologies) ---
TOPO = {
    "2D lattice":      (np.array([8,16,24,32]), np.array([5.77,10.78,13.84,18.44]), "#1f77b4", "o"),
    "scale-free (BA)": (np.array([8,16,24]),    np.array([4.67,8.81,10.10]),        "#2ca02c", "s"),
    "ring (1D)":       (np.array([8,16,24]),    np.array([2.34,2.30,2.20]),         "#ff7f0e", "^"),
    "fully-connected": (np.array([8,16,24]),    np.array([0.016,0.006,0.006]),      "#d62728", "v"),  # ~0, clamped for log
}
# classical 2D-Ising controls (classical_ising_v2.py)
CL_SQUARE = (np.array([16,36,64,100,144,256]), np.array([12.62,28.34,44.94,59.93,73.97,145.16]))  # slope vsN 0.839
CL_OURS   = (np.array([8,16,24,32]),           np.array([6.85,12.72,19.59,23.33]))                 # slope vsN 0.906
LLM_LAT   = (np.array([8,16,24,32]),           np.array([5.77,10.78,13.84,18.44]))                 # slope vsN 0.82

def slope(N, chi): return np.polyfit(np.log(N), np.log(chi), 1)[0]

# ===== figA: topology discrimination =====
fig, ax = plt.subplots(figsize=(7.0, 5.2))
for name, (N, chi, c, mk) in TOPO.items():
    ax.plot(N, chi, marker=mk, ms=8, lw=1.8, color=c, label=name)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("system size  N (agents)", fontsize=11)
ax.set_ylabel(r"susceptibility  $\chi=N\,\mathrm{Var}(m)$ at $J{=}1.08$", fontsize=11)
ax.set_title("The framework discriminates topologies (reproduces statistical mechanics)", fontsize=11.5)
ax.annotate("finite-d: Ising-like\ncritical growth", xy=(24, 13), xytext=(9, 22),
            fontsize=9, color="#1f77b4", arrowprops=dict(arrowstyle="->", color="#1f77b4"))
ax.annotate("1D: no transition\n($\\chi$ size-independent)", xy=(20, 2.25), xytext=(9, 3.3),
            fontsize=9, color="#ff7f0e", arrowprops=dict(arrowstyle="->", color="#ff7f0e"))
ax.annotate("mean-field: frozen\n($|m|{\\to}1,\\ \\chi{\\to}0$)", xy=(16, 0.02), xytext=(9, 0.05),
            fontsize=9, color="#d62728", arrowprops=dict(arrowstyle="->", color="#d62728"))
ax.set_ylim(0.008, 40); ax.legend(fontsize=9.5, loc="center right"); ax.grid(True, which="both", ls=":", alpha=0.4)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "figA_topology_discrimination.png"), dpi=200); plt.close(fig)
print("wrote figA_topology_discrimination.png")

# ===== figB: classical benchmark =====
fig, ax = plt.subplots(figsize=(7.0, 5.2))
for (N, chi), c, mk, lab in [
        (LLM_LAT, "#1f77b4", "o", f"LLM-HYBRID-MH (slope {slope(*LLM_LAT):.2f})"),
        (CL_OURS, "#ff7f0e", "s", f"classical Ising, our lattices (slope {slope(*CL_OURS):.2f})"),
        (CL_SQUARE, "#7f7f7f", "^", f"classical Ising, square even-L (slope {slope(*CL_SQUARE):.2f})")]:
    ax.plot(N, chi, marker=mk, ms=7, lw=1.6, color=c, label=lab)
    xf = np.array([N.min(), N.max()]); A = np.exp(np.polyfit(np.log(N), np.log(chi), 1)[1])
    ax.plot(xf, A*xf**slope(N, chi), ":", color=c, lw=1.0, alpha=0.7)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("system size  N (agents)", fontsize=11)
ax.set_ylabel(r"susceptibility  $\chi$ at criticality", fontsize=11)
ax.set_title("LLM cooperative exponent is Ising-consistent (no distinct class)", fontsize=11.5)
ax.text(0.03, 0.97, "LLM 0.82  vs  classical 2D-Ising 0.84\n=> indistinguishable within CI [0.77,0.86]",
        transform=ax.transAxes, va="top", fontsize=9, color="0.25",
        bbox=dict(boxstyle="round", fc="0.95", ec="0.7"))
ax.legend(fontsize=9, loc="lower right"); ax.grid(True, which="both", ls=":", alpha=0.4)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "figB_classical_benchmark.png"), dpi=200); plt.close(fig)
print("wrote figB_classical_benchmark.png")
print(f"[slopes] LLM={slope(*LLM_LAT):.3f}  classical-ours={slope(*CL_OURS):.3f}  classical-square={slope(*CL_SQUARE):.3f}")
