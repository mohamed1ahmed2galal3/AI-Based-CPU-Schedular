import joblib
import pandas as pd


class AIScheduler:
    """
    Enhanced AI-Based Scheduler — v2
    التحسينات:
    1. Dynamic Quantum  → quantum = cpu_burst_time * factor (مختلف لكل نوع)
    2. Dynamic Priority → 1/cpu_burst_time + cpu_io_ratio weight (العمليات الصغيرة أولاً)
    3. Aging            → priority += elapsed_time * factor (منع starvation)
    """

    def __init__(self,
                 model_path   = "C:\Users\dell\Desktop\AI Based CPU Schedular\model\scheduler_model.pkl",
                 encoder_path = "C:\Users\dell\Desktop\AI Based CPU Schedular\model\label_encoder.pkl",
                 cpu_q_factor = 0.25,   # quantum = burst * factor للـ CPU-bound
                 io_q_factor  = 0.10,   # quantum = burst * factor للـ IO-bound
                 cpu_q_min    = 10,     # حد أدنى للـ CPU-bound quantum
                 cpu_q_max    = 40,     # حد أقصى للـ CPU-bound quantum
                 io_q_min     = 2,      # حد أدنى للـ IO-bound quantum
                 io_q_max     = 10,     # حد أقصى للـ IO-bound quantum
                 aging_factor = 0.002): # كل ms انتظار بيزيد الأولوية بمقدار ده

        self.model       = joblib.load(model_path)
        self.encoder     = joblib.load(encoder_path)
        self.cpu_q_factor = cpu_q_factor
        self.io_q_factor  = io_q_factor
        self.cpu_q_min    = cpu_q_min
        self.cpu_q_max    = cpu_q_max
        self.io_q_min     = io_q_min
        self.io_q_max     = io_q_max
        self.aging_factor = aging_factor

    # ── 1. Predict process type ──────────────────────────────────
    def _predict(self, p):
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

    # ── 2. Dynamic Quantum ───────────────────────────────────────
    def _dynamic_quantum(self, predicted_type, cpu_burst_time):
        if predicted_type == "CPU-bound":
            q = cpu_burst_time * self.cpu_q_factor
            return round(max(self.cpu_q_min, min(self.cpu_q_max, q)), 2)
        else:
            q = cpu_burst_time * self.io_q_factor
            return round(max(self.io_q_min, min(self.io_q_max, q)), 2)

    # ── 3. Dynamic Base Priority (SRTF-inspired) ────────────────
    def _base_priority(self, predicted_type, p):
        remaining = max(p.get("remaining", p["cpu_burst_time"]), 0.1)

        if predicted_type == "IO-bound":
            # IO-bound: أولوية عالية جداً — مبنية على 1/remaining
            # + bonus من io_frequency عشان الـ IO processes تتقدم أكتر
            base = (1.0 / remaining) * 200 + p.get("io_frequency", 0) * 10
        else:
            # CPU-bound: أولوية مبنية على 1/remaining بس أقل weight
            # ده بيخليه يشبه SRTF في اختيار الأقصر
            base = (1.0 / remaining) * 50

        return round(base, 6)

    # ── 4. Effective Priority with Aging ────────────────────────
    def _effective_priority(self, p, current_time):
        # وقت الانتظار الفعلي = الوقت الحالي - وقت الوصول - الوقت اللي اتشغّل فيه
        time_run = p["cpu_burst_time"] - p["remaining"]
        wait_so_far = max(0, current_time - p["arrival_time"] - time_run)
        # aging: كل ms انتظار بيزيد الأولوية
        aged = self._base_priority(p["predicted_type"], p) + wait_so_far * self.aging_factor
        return round(aged, 6)

    # ── 5. Run ───────────────────────────────────────────────────
    def run(self, processes):
        enriched = []
        for p in processes:
            pred_type  = self._predict(p)
            quantum    = self._dynamic_quantum(pred_type, p["cpu_burst_time"])
            base_prio  = self._base_priority(pred_type, p)

            enriched.append({
                **p,
                "predicted_type": pred_type,
                "quantum":        quantum,
                "base_priority":  self._base_priority(pred_type, {**p, "remaining": p["cpu_burst_time"]}),
                "remaining":      p["cpu_burst_time"],
                "first_run":      None,
            })

        enriched.sort(key=lambda x: x["arrival_time"])

        ready_queue  = []
        current_time = 0
        done         = []
        i            = 0

        def enqueue_arrived():
            nonlocal i
            while i < len(enriched) and enriched[i]["arrival_time"] <= current_time:
                ready_queue.append(enriched[i])
                i += 1
            # ترتيب بـ effective priority (شاملة الـ aging)
            ready_queue.sort(
                key=lambda x: (-self._effective_priority(x, current_time),
                               x["arrival_time"])
            )

        enqueue_arrived()

        while ready_queue or i < len(enriched):
            if not ready_queue:
                current_time = enriched[i]["arrival_time"]
                enqueue_arrived()

            p       = ready_queue.pop(0)
            quantum = p["quantum"]

            if p["first_run"] is None:
                p["first_run"] = current_time

            # ── Preemptive check ────────────────────────────────
            # نشتغل لحد ما الـ quantum يخلص أو process جديدة تيجي
            future_arrivals = [
                e["arrival_time"] for e in enriched
                if e["arrival_time"] > current_time and e["remaining"] > 0
                and e not in ready_queue and e["first_run"] is None
            ]
            if future_arrivals:
                run_time = min(quantum, p["remaining"], min(future_arrivals) - current_time)
                run_time = max(run_time, min(quantum, p["remaining"]))
            else:
                run_time = min(quantum, p["remaining"])

            run_time = min(run_time, p["remaining"])
            if run_time <= 0:
                run_time = p["remaining"]

            current_time   += run_time
            p["remaining"] -= run_time

            enqueue_arrived()

            if p["remaining"] > 1e-9:
                # ترجع للـ queue — quantum يتحدث بناءً على remaining
                p["quantum"] = self._dynamic_quantum(
                    p["predicted_type"], p["remaining"]
                )
                ready_queue.append(p)
                ready_queue.sort(
                    key=lambda x: (-self._effective_priority(x, current_time),
                                   x["arrival_time"])
                )
            else:
                p["remaining"]  = 0
                finish_time     = current_time
                waiting_time    = finish_time - p["arrival_time"] - p["cpu_burst_time"]
                turnaround_time = finish_time - p["arrival_time"]
                response_time   = p["first_run"] - p["arrival_time"]

                done.append({
                    "process_id":     p["process_id"],
                    "process_type":   p["process_type"],
                    "predicted_type": p["predicted_type"],
                    "arrival_time":   p["arrival_time"],
                    "cpu_burst_time": p["cpu_burst_time"],
                    "quantum_used":   p["quantum"],
                    "finish_time":    finish_time,
                    "waiting_time":   round(max(waiting_time, 0), 4),
                    "turnaround_time":round(turnaround_time, 4),
                    "response_time":  round(max(response_time, 0), 4),
                })

        total_burst = sum(p["cpu_burst_time"] for p in processes)
        total_time  = current_time if current_time > 0 else 1
        cpu_util    = round((total_burst / total_time) * 100, 2)

        return done, cpu_util
