import sys
sys.path.insert(0, r"C:\Users\dell\Desktop\AI Based CPU Schedular")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from scheduler.fcfs        import FCFSScheduler
from scheduler.round_robin import RoundRobinScheduler
from scheduler.ai_scheduler import AIScheduler

# ─── 1. Load 50 processes للـ simulation ────────────────────────
df = pd.read_csv( r"C:\Users\dell\Desktop\AI Based CPU Schedular\data\processes_dataset.csv")
sample = df.sample(50, random_state=7).to_dict("records")

# ─── 2. شغّل الـ 3 schedulers ───────────────────────────────────
fcfs_results, fcfs_util   = FCFSScheduler().run(sample)
rr_results,   rr_util     = RoundRobinScheduler(quantum=10).run(sample)
ai_results,   ai_util     = AIScheduler().run(sample)

def summarize(results, cpu_util, name):
    df_r = pd.DataFrame(results)
    return {
        "Scheduler":          name,
        "Avg Waiting Time":   round(df_r["waiting_time"].mean(), 2),
        "Avg Turnaround":     round(df_r["turnaround_time"].mean(), 2),
        "Avg Response Time":  round(df_r["response_time"].mean(), 2),
        "CPU Utilization %":  cpu_util,
    }

summary = pd.DataFrame([
    summarize(fcfs_results, fcfs_util, "FCFS"),
    summarize(rr_results,   rr_util,   "Round Robin"),
    summarize(ai_results,   ai_util,   "AI Scheduler"),
])

print("=" * 62)
print("        Simulation Results — 50 Processes")
print("=" * 62)
print(summary.to_string(index=False))
print("=" * 62)

# ─── 3. AI prediction accuracy ──────────────────────────────────
ai_df = pd.DataFrame(ai_results)
correct = (ai_df["process_type"] == ai_df["predicted_type"]).sum()
print(f"\n  AI Prediction Accuracy : {correct}/{len(ai_df)} "
      f"({correct/len(ai_df)*100:.1f}%)")

# ─── 4. Per-type breakdown for AI ───────────────────────────────
print("\n  AI Scheduler — Avg Waiting Time per process type:")
for ptype in ["CPU-bound", "IO-bound"]:
    sub = ai_df[ai_df["process_type"] == ptype]
    print(f"    {ptype:<12} → {sub['waiting_time'].mean():.2f} ms "
          f"(n={len(sub)})")

print()

# ─── 5. Plots ───────────────────────────────────────────────────
colors = ["#e06666", "#f6b26b", "#4a86e8"]
metrics = ["Avg Waiting Time", "Avg Turnaround", "Avg Response Time"]
labels  = summary["Scheduler"].tolist()

fig, axes = plt.subplots(1, 4, figsize=(18, 5))
fig.suptitle("Scheduler Comparison — 50 Processes",
             fontsize=14, fontweight="bold")

# Bar charts for each metric
for idx, metric in enumerate(metrics):
    ax = axes[idx]
    bars = ax.bar(labels, summary[metric], color=colors,
                  edgecolor="white", width=0.5)
    ax.set_title(metric)
    ax.set_ylabel("Time (ms)")
    ax.set_ylim(0, summary[metric].max() * 1.25)
    for bar, val in zip(bars, summary[metric]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + summary[metric].max() * 0.02,
                f"{val:.1f}", ha="center", va="bottom",
                fontsize=10, fontweight="bold")
    ax.tick_params(axis="x", labelsize=9)

# CPU Utilization
ax = axes[3]
bars = ax.bar(labels, summary["CPU Utilization %"],
              color=colors, edgecolor="white", width=0.5)
ax.set_title("CPU Utilization %")
ax.set_ylabel("Utilization (%)")
ax.set_ylim(0, 115)
for bar, val in zip(bars, summary["CPU Utilization %"]):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{val:.1f}%", ha="center", va="bottom",
            fontsize=10, fontweight="bold")
ax.tick_params(axis="x", labelsize=9)

plt.tight_layout()
plt.savefig(r"C:\Users\dell\Desktop\AI Based CPU Schedular\scheduler\comparison.png",
            dpi=150, bbox_inches="tight")
print("  Chart saved → simulation/comparison.png")

# ─── 6. Waiting time by process type (AI vs RR) ─────────────────
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
fig2.suptitle("Waiting Time by Process Type — AI vs Round Robin",
              fontsize=13, fontweight="bold")

rr_df = pd.DataFrame(rr_results)

for ax, (df_sched, sched_name) in zip(
        axes2, [(rr_df, "Round Robin"), (ai_df, "AI Scheduler")]):
    cpu_wt = df_sched[df_sched["process_type"] == "CPU-bound"]["waiting_time"]
    io_wt  = df_sched[df_sched["process_type"] == "IO-bound"]["waiting_time"]
    ax.boxplot([cpu_wt, io_wt], labels=["CPU-bound", "IO-bound"],
               patch_artist=True,
               boxprops=dict(facecolor="#dce8fb"),
               medianprops=dict(color="#4a86e8", linewidth=2))
    ax.set_title(sched_name)
    ax.set_ylabel("Waiting Time (ms)")

plt.tight_layout()
plt.savefig(r"C:\Users\dell\Desktop\AI Based CPU Schedular\simulation\waiting_by_type.png",
            dpi=150, bbox_inches="tight")
print("  Chart saved → simulation/waiting_by_type.png")