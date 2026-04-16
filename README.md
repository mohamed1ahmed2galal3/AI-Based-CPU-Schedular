🤖 AI-Based CPU Scheduler

📌 Project Overview

This project presents an **AI-based CPU Scheduling system** that improves traditional scheduling algorithms by using **Machine Learning** to classify processes and dynamically adjust scheduling decisions.

Traditional schedulers (e.g., FCFS, Round Robin) treat all processes equally, which often leads to inefficient CPU utilization and high waiting times.
This project introduces an intelligent scheduler that adapts based on process behavior.

---

🎯 Objectives

* Simulate and compare classical scheduling algorithms:

  * First Come First Serve (FCFS)
  * Round Robin (RR)
* Build a **Machine Learning model** to classify processes:

  * CPU-bound
  * IO-bound
* Develop an **AI Scheduler** that:

  * Assigns dynamic priorities
  * Adjusts time quantum based on process type
* Evaluate performance using multiple metrics

---

## 🧠 Core Idea

The system integrates:

1. Machine Learning (Random Forest)
2. Dynamic Scheduling
3. Hybrid Strategy (Priority + Round Robin)

Instead of static rules:

* CPU-bound processes → longer execution time (larger quantum)
* IO-bound processes → faster response (higher priority, smaller quantum)

---

## 📊 Dataset Generation

A synthetic dataset of processes is generated with the following features:

| Feature          | Description                  |
| ---------------- | ---------------------------- |
| process_id       | Unique identifier            |
| arrival_time     | Time when process arrives    |
| cpu_burst_time   | CPU execution time           |
| io_burst_time    | I/O waiting time             |
| io_frequency     | Frequency of I/O operations  |
| execution_cycles | Number of CPU cycles         |
| priority         | Process priority             |
| cpu_io_ratio     | Ratio of CPU to I/O time     |
| process_type     | Label (CPU-bound / IO-bound) |

---

## 🤖 Machine Learning Model

### Model Used:

* **Random Forest Classifier**

### Steps:

1. Load dataset
2. Select features and label
3. Encode labels
4. Split data (80% train / 20% test)
5. Train model
6. Evaluate using:

   * Accuracy
   * Cross-validation
   * Classification report
7. Save model using `joblib`

---

## ⚙️ Scheduling Algorithms

### 1. FCFS (First Come First Serve)

* Executes processes in order of arrival
* Non-preemptive
* Simple but inefficient

---

### 2. Round Robin

* Each process gets equal time quantum
* Preemptive
* Improves fairness but ignores process type

---

### 3. AI Scheduler (Proposed Model) 🚀

#### Key Features:

* Predicts process type using ML
* Assigns:

  * **CPU-bound** → Large quantum (20ms), low priority
  * **IO-bound** → Small quantum (5ms), high priority
* Uses **dynamic priority queue**
* Combines:

  * Priority Scheduling
  * Round Robin

---

## 📈 Performance Metrics

The system evaluates:

* **Waiting Time**
* **Turnaround Time**
* **Response Time**
* **CPU Utilization**

---

## 🔬 Simulation

* Random sample of 50 processes
* All schedulers are executed on the same dataset
* Results are compared using:

  * Statistical summaries
  * Visualization charts

---

## 📊 Results & Insights

### Key Findings:

* AI Scheduler significantly reduces **waiting time**
* IO-bound processes benefit the most
* CPU utilization improves
* Better balance between fairness and efficiency

---

## 📉 Visualizations

The project includes:

* Bar charts for:

  * Waiting Time
  * Turnaround Time
  * Response Time
  * CPU Utilization
* Box plots:

  * Distribution of waiting time per process type

---

## 🏗️ Project Structure

```
AI Based CPU Scheduler/
│
├── AI_CPU_Scheduler_Presentation/
│   └── ai_cpu_scheduler_presentation.html
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
│   └── sjf.py
│   └── srtf.py
│   └── ai_scheduler.py
│
├── simulation/
│   ├── comparison.png
│   └── waiting_by_type.png
│
└── main_simulation.py
```

---

## 🚀 How to Run

1. Generate dataset:

```
python generate_dataset.py
```

2. Train model:

```
python train_model.py
```

3. Run simulation:

```
python main_simulation.py
```

---

## 🧩 Technologies Used

* Python
* NumPy
* Pandas
* Scikit-learn
* Matplotlib
* Joblib

---

## 🔮 Future Improvements

* Dynamic quantum using Reinforcement Learning
* Real-time scheduling simulation
* Integration with OS-level schedulers
* Adding more process features

---

## 📌 Conclusion

This project demonstrates how **Artificial Intelligence can enhance operating system scheduling** by making smarter, data-driven decisions.

The AI Scheduler outperforms traditional methods by:

* Adapting to process behavior
* Reducing waiting time
* Improving system efficiency

---

## 👨‍💻 Author

Developed as part of an academic project on:
**AI-Based CPU Scheduling Systems**
