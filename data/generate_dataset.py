import numpy as np
import pandas as pd

np.random.seed(42)
NUM_PROCESSES = 1000

def generate_dataset(n=NUM_PROCESSES):
    records = []

    for i in range(n):
        # ---- نحدد النوع عشوائياً 50/50 ----
        process_type = np.random.choice(["CPU-bound", "IO-bound"])

        if process_type == "CPU-bound":
            # CPU-bound: burst طويل، I/O قليل، execution كتير
            cpu_burst_time    = round(np.random.uniform(40, 100), 2)   # ms
            io_burst_time     = round(np.random.uniform(2,  15),  2)   # ms
            io_frequency      = round(np.random.uniform(0,  0.3), 2)   # نسبة من وقت التشغيل
            arrival_time      = round(np.random.uniform(0,  50),  2)   # ms
            execution_cycles  = int(np.random.uniform(500, 2000))      # cycles
            priority          = int(np.random.uniform(1,   5))         # 1=low, 10=high
        else:
            # IO-bound: burst قصير، I/O كتير، execution أقل
            cpu_burst_time    = round(np.random.uniform(2,  25),  2)
            io_burst_time     = round(np.random.uniform(30, 90),  2)
            io_frequency      = round(np.random.uniform(0.5, 1.0), 2)
            arrival_time      = round(np.random.uniform(0,  50),  2)
            execution_cycles  = int(np.random.uniform(50,  400))
            priority          = int(np.random.uniform(5,   10))

        # Feature مشتقة: نسبة CPU/IO
        cpu_io_ratio = round(cpu_burst_time / (io_burst_time + 0.001), 4)

        records.append({
            "process_id":       i + 1,
            "arrival_time":     arrival_time,
            "cpu_burst_time":   cpu_burst_time,
            "io_burst_time":    io_burst_time,
            "io_frequency":     io_frequency,
            "execution_cycles": execution_cycles,
            "priority":         priority,
            "cpu_io_ratio":     cpu_io_ratio,
            "process_type":     process_type          # ← الـ label
        })

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    df = generate_dataset()

    # حفظ الـ dataset
    output_path = r"C:\Users\dell\Desktop\AI Based CPU Schedular\data\processes_dataset.csv"
    df.to_csv(output_path, index=False)

    # ---- تقرير سريع ----
    print("=" * 50)
    print("  Dataset Generated Successfully!")
    print("=" * 50)
    print(f"  Total processes   : {len(df)}")
    print(f"  CPU-bound count   : {(df['process_type'] == 'CPU-bound').sum()}")
    print(f"  IO-bound count    : {(df['process_type'] == 'IO-bound').sum()}")
    print()
    print("  Sample (first 5 rows):")
    print(df.head().to_string(index=False))
    print()
    print("  Stats per type:")
    print(df.groupby("process_type")[
        ["cpu_burst_time", "io_burst_time", "io_frequency", "execution_cycles"]
    ].mean().round(2).to_string())
    print()
    print(f"  Saved to: {output_path}")
    print("=" * 50)
