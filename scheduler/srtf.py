class SRTFScheduler:
    """
    Shortest Remaining Time First — Preemptive SJF
    لو process جديدة وصلت وعندها remaining time أقل
    من اللي بتشتغل دلوقتي، الـ CPU بتوقفها وتبدأ الجديدة فوراً.
    """

    def run(self, processes):
        procs = [
            {**p, "remaining": p["cpu_burst_time"], "first_run": None}
            for p in sorted(processes, key=lambda x: x["arrival_time"])
        ]

        current_time = procs[0]["arrival_time"]
        done         = []
        completed    = 0
        n            = len(procs)

        while completed < n:
            # ready queue: وصلت ولسه فيها شغل
            ready = [
                p for p in procs
                if p["arrival_time"] <= current_time and p["remaining"] > 0
            ]

            if not ready:
                future = [p for p in procs if p["remaining"] > 0]
                if not future:
                    break
                current_time = min(p["arrival_time"] for p in future)
                continue

            # اختار الأقل remaining time
            chosen = min(ready, key=lambda p: (p["remaining"], p["arrival_time"]))

            # سجّل أول مرة بتشتغل
            if chosen["first_run"] is None:
                chosen["first_run"] = current_time

            # اشتغل لحد ما process تخلص أو process جديدة تيجي
            future_arrivals = [
                p["arrival_time"] for p in procs
                if p["arrival_time"] > current_time and p["remaining"] > 0
            ]

            if future_arrivals:
                next_arrival = min(future_arrivals)
                run_for = min(chosen["remaining"], next_arrival - current_time)
            else:
                run_for = chosen["remaining"]

            # ضمان إن run_for دايماً موجب
            if run_for <= 0:
                run_for = chosen["remaining"]

            chosen["remaining"] -= run_for
            current_time        += run_for

            # لو خلصت
            if chosen["remaining"] <= 1e-9:
                chosen["remaining"] = 0
                finish_time     = current_time
                waiting_time    = finish_time - chosen["arrival_time"] - chosen["cpu_burst_time"]
                turnaround_time = finish_time - chosen["arrival_time"]
                response_time   = chosen["first_run"] - chosen["arrival_time"]

                done.append({
                    "process_id":      chosen["process_id"],
                    "process_type":    chosen["process_type"],
                    "arrival_time":    chosen["arrival_time"],
                    "cpu_burst_time":  chosen["cpu_burst_time"],
                    "finish_time":     round(finish_time, 4),
                    "waiting_time":    round(max(waiting_time, 0), 4),
                    "turnaround_time": round(turnaround_time, 4),
                    "response_time":   round(max(response_time, 0), 4),
                })
                completed += 1

        total_burst = sum(p["cpu_burst_time"] for p in processes)
        cpu_util    = round((total_burst / current_time) * 100, 2) if current_time > 0 else 0
        return done, cpu_util
