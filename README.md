# 🤖 AI-Based Smart CPU Scheduler (Enhanced Version)

## 📌 Project Overview

This project presents an advanced AI-based CPU Scheduling system that significantly improves traditional scheduling algorithms by combining Machine Learning with adaptive runtime mechanisms.

Unlike conventional schedulers such as FCFS and Round Robin, which rely on static rules, this system introduces a **fully adaptive scheduler** capable of dynamically adjusting its behavior based on real-time process characteristics.

The enhanced version includes:
- Dynamic time quantum allocation  
- Continuous priority recalculation  
- Aging to prevent starvation  
- Preemptive decision-making  

It also benchmarks performance against **SJF and SRTF**, achieving **near-optimal results in realistic environments**.

---

## 🎯 Objectives

- Compare multiple scheduling algorithms:
  - FCFS  
  - Round Robin  
  - SJF  
  - SRTF  

- Build an ML model to classify:
  - CPU-bound  
  - IO-bound  

- Develop an adaptive AI scheduler that:
  - Uses dynamic quantum  
  - Applies dynamic priority  
  - Prevents starvation  
  - Supports preemption  

---

## 🧠 Core Idea

The system integrates:

- Machine Learning (**Random Forest**)  
- Adaptive Scheduling  
- Hybrid Strategy (Priority + Preemption)

### 🔥 Key Innovations

- **Dynamic Quantum**
  - CPU-bound → 4–25 ms  
  - IO-bound → 1–5 ms  

- **Dynamic Priority**
  - Based on remaining time  
  - Shorter processes get higher priority  

- **Aging**
  - Prevents starvation  

- **Preemption**
  - High-priority processes interrupt execution  

👉 Result:  
A hybrid scheduler that approximates **SJF + SRTF behavior without prior knowledge**.

---

## 📊 Dataset

Synthetic dataset with features:

| Feature | Description |
|--------|------------|
| process_id | Unique ID |
| arrival_time | Arrival time |
| cpu_burst_time | CPU time |
| io_burst_time | I/O time |
| io_frequency | I/O frequency |
| execution_cycles | Cycles |
| priority | Initial priority |
| cpu_io_ratio | CPU vs IO |
| process_type | Label |

---

## 🤖 Machine Learning Model

**Model:** Random Forest  

### Steps:
- Load dataset  
- Train/Test split (80/20)  
- Train model  
- Evaluate (accuracy, CV)  
- Save using `joblib`  

---

## ⚙️ Scheduling Algorithms

### 1. FCFS
- Non-preemptive  
- Simple, inefficient  

### 2. Round Robin
- Preemptive  
- Fixed quantum  

### 3. SJF
- Optimal (non-preemptive)  
- Unrealistic assumption  

### 4. SRTF
- Optimal (preemptive)  
- Theoretical benchmark  

### 5. AI Scheduler 🚀

- ML-based classification  
- Dynamic quantum  
- Dynamic priority  
- Aging  
- Preemptive  

👉 Near-optimal performance without unrealistic assumptions.

---

## 📈 Performance Metrics

- Waiting Time  
- Turnaround Time  
- Response Time  
- CPU Utilization  

---

## 🔬 Simulation

- 50 processes  
- Same dataset for all schedulers  
- Fair comparison  

### Includes:
- 5-scheduler comparison  
- SJF vs SRTF analysis  
- Waiting time distribution  

---

## 📊 Results

### 🔥 Improvements:

- AI Waiting Time:
  - **738 → 659 ms**

- Improvement:
  - FCFS → ~42%  
  - RR → ~50%  

- IO-bound:
  - **154 → 92 ms**

- vs SRTF:
  - ~**4 ms difference only**

---

## 📉 Visualizations

- Bar charts:
  - Waiting / Turnaround / Response / CPU  

- Boxplots:
  - Waiting distribution  

- Deep dive:
  - SJF vs SRTF  

---

## 🏗️ Project Structure

```
AI Based CPU Scheduler/
│
├── AI_CPU_Scheduler_Presentation/
│   └── ai_cpu_scheduler_presentation.html
│
├── data/
│   └── processes_dataset.csv
│
├── model/
│   ├── scheduler_model.pkl
│   └── label_encoder.pkl
│
├── scheduler/
│   ├── fcfs.py
│   ├── round_robin.py
│   ├── sjf.py
│   ├── srtf.py
│   └── ai_scheduler.py
│
├── simulation/
│   ├── comparison.png
│   ├── sjf_vs_srtf.png
│   └── waiting_distribution.png
│
├── run_simulation.py
└── cpu_scheduler_ui.html
```

---

## 🚀 How to Run

### 1. Generate Dataset
```bash
python generate_dataset.py
```

### 2. Train Model
```bash
python train_model.py
```

### 3. Run Simulation
```bash
python run_simulation.py
```

### 4. Open UI
Open:
```
cpu_scheduler_ui.html
```

---

## 🧩 Technologies

- Python  
- NumPy  
- Pandas  
- Scikit-learn  
- Matplotlib  
- Joblib  

---

## 🔮 Future Work

- Reinforcement Learning  
- Multi-core scheduling  
- Real OS integration  
- Context-switch modeling  

---

## 📌 Conclusion

This project transforms CPU scheduling into a **dynamic and intelligent system**.

The AI Scheduler:
- Adapts in real time  
- Achieves near-SRTF performance  
- Reduces waiting time  
- Prevents starvation  

---

## 👨‍💻 Author

Academic Project:  
**AI-Based Smart CPU Scheduling**
