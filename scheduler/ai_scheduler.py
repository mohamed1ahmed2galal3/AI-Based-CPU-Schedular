import joblib
import numpy as np
from collections import deque

class AIScheduler:
    """
    AI-Based Scheduler:
    - بيحمّل الـ ML model
    - بيصنّف كل process (CPU-bound / IO-bound)
    - CPU-bound  → quantum كبير (20ms) + priority منخفض
    - IO-bound   → quantum صغير (5ms)  + priority عالي
    - بيشغّل بـ priority queue ديناميكية
    """

    def __init__(self,
                model_path   = "C:\\Users\\dell\\Desktop\\AI Based CPU Schedular\\model\\scheduler_model.pkl",
                encoder_path = "C:\\Users\\dell\\Desktop\\AI Based CPU Schedular\\model\\label_encoder.pkl"):

        self.model   = joblib.load(model_path)
        self.encoder = joblib.load(encoder_path)

        # Quantum بالـ ms لكل نوع
        self.quantum_cpu = 20   # CPU-bound: quantum أكبر
        self.quantum_io  = 5    # IO-bound : quantum أصغر

    # ── predict نوع الـ process ──────────────────────────────────
    def _predict(self, p):
        import pandas as pd
        features = pd.DataFrame([{
            "cpu_burst_time":   p["cpu_burst_time"],
            "io_burst_time":    p["io_burst_time"],
            "io_frequency":     p["io_frequency"],
            "execution_cycles": p["execution_cycles"],
            "priority":         p["priority"],
            "cpu_io_ratio":     p["cpu_io_ratio"],
        }])
        encoded = self.model.predict(features)[0]
        return self.encoder.inverse_transform([encoded])[0]

    # ── تحديد الـ quantum والـ dynamic priority ──────────────────
    def _get_quantum_and_priority(self, predicted_type):
        if predicted_type == "CPU-bound":
            return self.quantum_cpu, 1   # priority منخفض (1 = أقل أهمية)
        else:
            return self.quantum_io, 10  # priority عالي (10 = أكثر أهمية)

    # ── run ──────────────────────────────────────────────────────
    def run(self, processes):
        # نصنّف كل process ونحدد quantum ودynamic priority
        enriched = []
        for p in processes:
            pred_type                 = self._predict(p)
            quantum, dyn_priority     = self._get_quantum_and_priority(pred_type)
            enriched.append({
                **p,
                "predicted_type": pred_type,
                "quantum":        quantum,
                "dyn_priority":   dyn_priority,
                "remaining":      p["cpu_burst_time"],
                "first_run":      None,
            })

        # ترتيب مبدئي بالـ arrival_time
        enriched.sort(key=lambda x: x["arrival_time"])

        # Priority queue (max priority = يتشغل أول)
        # نستخدم list ونعمل sort كل مرة بعد إضافة processes جديدة
        ready_queue  = []
        current_time = 0
        done         = []
        i            = 0

        def enqueue_arrived():
            nonlocal i
            while i < len(enriched) and enriched[i]["arrival_time"] <= current_time:
                ready_queue.append(enriched[i])
                i += 1
            # ترتيب: priority عالي أول، لو متساويين → arrival_time أول
            ready_queue.sort(key=lambda x: (-x["dyn_priority"], x["arrival_time"]))

        enqueue_arrived()

        while ready_queue or i < len(enriched):
            if not ready_queue:
                # الـ CPU idle — نقفز للـ process الجاية
                current_time = enriched[i]["arrival_time"]
                enqueue_arrived()

            p        = ready_queue.pop(0)
            quantum  = p["quantum"]

            if p["first_run"] is None:
                p["first_run"] = current_time

            run_time        = min(quantum, p["remaining"])
            current_time   += run_time
            p["remaining"] -= run_time

            enqueue_arrived()

            if p["remaining"] > 0:
                # لسه ما خلصتش — ترجع للـ queue
                ready_queue.append(p)
                ready_queue.sort(key=lambda x: (-x["dyn_priority"], x["arrival_time"]))
            else:
                finish_time     = current_time
                waiting_time    = finish_time - p["arrival_time"] - p["cpu_burst_time"]
                turnaround_time = finish_time - p["arrival_time"]
                response_time   = p["first_run"] - p["arrival_time"]

                done.append({
                    "process_id":       p["process_id"],
                    "process_type":     p["process_type"],
                    "predicted_type":   p["predicted_type"],
                    "arrival_time":     p["arrival_time"],
                    "cpu_burst_time":   p["cpu_burst_time"],
                    "quantum_used":     p["quantum"],
                    "finish_time":      finish_time,
                    "waiting_time":     round(max(waiting_time, 0), 4),
                    "turnaround_time":  round(turnaround_time, 4),
                    "response_time":    round(max(response_time, 0), 4),
                })

        total_burst = sum(p["cpu_burst_time"] for p in processes)
        total_time  = current_time if current_time > 0 else 1
        cpu_util    = round((total_burst / total_time) * 100, 2)

        return done, cpu_util