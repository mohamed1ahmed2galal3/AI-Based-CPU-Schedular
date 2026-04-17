import sys
sys.path.insert(0, "/home/claude/ai_cpu_scheduler")

import pandas as pd
import matplotlib.pyplot as plt

from scheduler.fcfs         import FCFSScheduler
from scheduler.round_robin  import RoundRobinScheduler
from scheduler.sjf          import SJFNonPreemptiveScheduler
from scheduler.srtf         import SRTFScheduler
from scheduler.ai_scheduler import AIScheduler

# ─── 1. Load 50 processes ───────────────────────────────────────
df     = pd.read_csv("/home/claude/ai_cpu_scheduler/data/processes_dataset.csv")
sample = df.sample(50, random_state=7).to_dict("records")

# ─── 2. Run all 5 schedulers ────────────────────────────────────
fcfs_res,  fcfs_util  = FCFSScheduler().run(sample)
rr_res,    rr_util    = RoundRobinScheduler(quantum=10).run(sample)
sjf_res,   sjf_util   = SJFNonPreemptiveScheduler().run(sample)
srtf_res,  srtf_util  = SRTFScheduler().run(sample)
ai_res,    ai_util    = AIScheduler(
    cpu_q_factor=0.10, io_q_factor=0.04,
    cpu_q_min=4,       cpu_q_max=25,
    io_q_min=1,        io_q_max=5,
    aging_factor=0.003
).run(sample)

# ─── 3. Summarize ───────────────────────────────────────────────
def summarize(results, cpu_util, name):
    df_r = pd.DataFrame(results)
    return {
        "Scheduler":         name,
        "Avg Waiting Time":  round(df_r["waiting_time"].mean(),    2),
        "Avg Turnaround":    round(df_r["turnaround_time"].mean(), 2),
        "Avg Response Time": round(df_r["response_time"].mean(),   2),
        "CPU Utilization %": cpu_util,
    }

summary = pd.DataFrame([
    summarize(fcfs_res,  fcfs_util,  "FCFS"),
    summarize(rr_res,    rr_util,    "Round Robin"),
    summarize(sjf_res,   sjf_util,   "SJF (Non-P)"),
    summarize(srtf_res,  srtf_util,  "SRTF"),
    summarize(ai_res,    ai_util,    "AI Scheduler"),
])

# ─── 4. Print results table ─────────────────────────────────────
print("=" * 72)
print("        Simulation Results — 5 Schedulers · 50 Processes")
print("=" * 72)
print(summary.to_string(index=False))
print("=" * 72)

ai_df   = pd.DataFrame(ai_res)
correct = (ai_df["process_type"] == ai_df["predicted_type"]).sum()
print(f"\n  AI Prediction Accuracy : {correct}/{len(ai_df)} ({correct/len(ai_df)*100:.1f}%)")

print("\n  AI Scheduler — Avg Waiting Time per process type:")
for ptype in ["CPU-bound", "IO-bound"]:
    sub = ai_df[ai_df["process_type"] == ptype]
    print(f"    {ptype:<12} -> {sub['waiting_time'].mean():.2f} ms (n={len(sub)})")

sjf_df  = pd.DataFrame(sjf_res)
srtf_df = pd.DataFrame(srtf_res)
imp     = round((sjf_df["waiting_time"].mean() - srtf_df["waiting_time"].mean())
                / sjf_df["waiting_time"].mean() * 100, 1)
print(f"\n  SRTF is {imp}% better than SJF in waiting time (preemption benefit)")
print()

# ─── 5. Colors ──────────────────────────────────────────────────
COLORS = {
    "FCFS":         "#e06666",
    "Round Robin":  "#f6b26b",
    "SJF (Non-P)":  "#a8d08d",
    "SRTF":         "#6aa84f",
    "AI Scheduler": "#4a86e8",
}
colors = [COLORS[s] for s in summary["Scheduler"]]
labels = summary["Scheduler"].tolist()

# ─── 6. Chart 1 — Full 5-scheduler comparison ───────────────────
metrics = ["Avg Waiting Time", "Avg Turnaround", "Avg Response Time"]

fig, axes = plt.subplots(1, 4, figsize=(20, 5.5))
fig.suptitle("CPU Scheduler Comparison — 5 Algorithms · 50 Processes",
             fontsize=14, fontweight="bold")
fig.patch.set_facecolor("#f8f9fa")

for idx, metric in enumerate(metrics):
    ax   = axes[idx]
    vals = summary[metric]
    bars = ax.bar(labels, vals, color=colors, edgecolor="white", width=0.55)
    ax.set_title(metric, fontsize=10, fontweight="bold")
    ax.set_ylabel("Time (ms)", fontsize=9)
    ax.set_ylim(0, vals.max() * 1.28)
    ax.set_facecolor("#ffffff")
    ax.tick_params(axis="x", labelsize=7.5, rotation=12)
    best_idx = int(vals.idxmin())
    for i, (bar, val) in enumerate(zip(bars, vals)):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + vals.max() * 0.02,
                f"{val:.0f}", ha="center", va="bottom",
                fontsize=8.5,
                fontweight="bold" if i == best_idx else "normal")
    bars[best_idx].set_edgecolor("#1a5276")
    bars[best_idx].set_linewidth(2)

ax   = axes[3]
vals = summary["CPU Utilization %"]
bars = ax.bar(labels, vals, color=colors, edgecolor="white", width=0.55)
ax.set_title("CPU Utilization %", fontsize=10, fontweight="bold")
ax.set_ylabel("Utilization (%)", fontsize=9)
ax.set_ylim(0, 115)
ax.set_facecolor("#ffffff")
ax.tick_params(axis="x", labelsize=7.5, rotation=12)
for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

plt.tight_layout()
plt.savefig("/home/claude/ai_cpu_scheduler/simulation/comparison_5schedulers.png",
            dpi=150, bbox_inches="tight", facecolor="#f8f9fa")
print("  Chart saved -> simulation/comparison_5schedulers.png")

# ─── 7. Chart 2 — SJF vs SRTF deep dive ────────────────────────
fig2, axes2 = plt.subplots(1, 3, figsize=(14, 5))
fig2.suptitle("SJF (Non-Preemptive) vs SRTF (Preemptive) — Deep Dive",
              fontsize=13, fontweight="bold")
fig2.patch.set_facecolor("#f8f9fa")

sjf_srtf = summary[summary["Scheduler"].isin(["SJF (Non-P)", "SRTF"])].reset_index(drop=True)
s_colors = ["#a8d08d", "#6aa84f"]
s_labels = sjf_srtf["Scheduler"].tolist()

for idx, metric in enumerate(["Avg Waiting Time", "Avg Turnaround", "Avg Response Time"]):
    ax   = axes2[idx]
    vals = sjf_srtf[metric]
    bars = ax.bar(s_labels, vals, color=s_colors, edgecolor="white", width=0.45)
    ax.set_title(metric, fontsize=10, fontweight="bold")
    ax.set_ylabel("Time (ms)", fontsize=9)
    ax.set_ylim(0, vals.max() * 1.3)
    ax.set_facecolor("#ffffff")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + vals.max() * 0.025,
                f"{val:.2f}", ha="center", va="bottom",
                fontsize=10, fontweight="bold")
    if len(vals) == 2:
        diff = round((vals.iloc[0] - vals.iloc[1]) / vals.iloc[0] * 100, 1)
        ax.annotate(f"SRTF saves {diff}%",
                    xy=(0.5, 0.93), xycoords="axes fraction",
                    ha="center", fontsize=8.5, color="#1a5276",
                    bbox=dict(boxstyle="round,pad=0.3",
                              fc="#d6eaf8", ec="#1a5276", lw=0.8))

plt.tight_layout()
plt.savefig("/home/claude/ai_cpu_scheduler/simulation/sjf_vs_srtf.png",
            dpi=150, bbox_inches="tight", facecolor="#f8f9fa")
print("  Chart saved -> simulation/sjf_vs_srtf.png")

# ─── 8. Chart 3 — Waiting time boxplot all 5 ────────────────────
fig3, ax3 = plt.subplots(figsize=(13, 5))
fig3.suptitle("Waiting Time Distribution — All 5 Schedulers",
              fontsize=13, fontweight="bold")
fig3.patch.set_facecolor("#f8f9fa")
ax3.set_facecolor("#ffffff")

all_data = [
    pd.DataFrame(fcfs_res)["waiting_time"].values,
    pd.DataFrame(rr_res)["waiting_time"].values,
    sjf_df["waiting_time"].values,
    srtf_df["waiting_time"].values,
    ai_df["waiting_time"].values,
]
bp = ax3.boxplot(all_data, patch_artist=True,
                 tick_labels=["FCFS","Round Robin","SJF (Non-P)","SRTF","AI Scheduler"],
                 medianprops=dict(linewidth=2, color="#1a5276"))
for patch, color in zip(bp["boxes"], list(COLORS.values())):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)

ax3.set_ylabel("Waiting Time (ms)", fontsize=10)
ax3.tick_params(axis="x", labelsize=9)

plt.tight_layout()
plt.savefig("/home/claude/ai_cpu_scheduler/simulation/waiting_distribution.png",
            dpi=150, bbox_inches="tight", facecolor="#f8f9fa")
print("  Chart saved -> simulation/waiting_distribution.png")
