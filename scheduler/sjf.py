class SJFNonPreemptiveScheduler:
    """
    Shortest Job First — Non-Preemptive
    لما الـ CPU تخلص من process، بتشغّل الـ process
    اللي عندها أقل cpu_burst_time من اللي في الـ ready queue.
    لو process بدأت، مش ممكن تتوقف.
    """

    def run(self, processes):
        procs      = sorted(processes, key=lambda p: p["arrival_time"])
        n          = len(procs)
        done_flags = [False] * n
        done       = []
        completed  = 0
        current_time = procs[0]["arrival_time"]

        while completed < n:
            # الـ processes اللي وصلت ولسه ما اتشغّلتش
            ready = [
                procs[i] for i in range(n)
                if not done_flags[i] and procs[i]["arrival_time"] <= current_time
            ]

            if not ready:
                # CPU idle — قفز لأقرب arrival_time جاي
                next_arrival = min(
                    procs[i]["arrival_time"] for i in range(n) if not done_flags[i]
                )
                current_time = next_arrival
                continue

            # اختار الأقل burst time
            chosen = min(ready, key=lambda p: p["cpu_burst_time"])
            idx    = next(i for i, p in enumerate(procs)
                          if p["process_id"] == chosen["process_id"])

            start_time      = current_time
            finish_time     = current_time + chosen["cpu_burst_time"]
            waiting_time    = start_time - chosen["arrival_time"]
            turnaround_time = finish_time - chosen["arrival_time"]
            response_time   = waiting_time  # non-preemptive: أول رد = وقت الانتظار

            done.append({
                "process_id":      chosen["process_id"],
                "process_type":    chosen["process_type"],
                "arrival_time":    chosen["arrival_time"],
                "cpu_burst_time":  chosen["cpu_burst_time"],
                "start_time":      start_time,
                "finish_time":     finish_time,
                "waiting_time":    round(max(waiting_time, 0), 4),
                "turnaround_time": round(turnaround_time, 4),
                "response_time":   round(max(response_time, 0), 4),
            })

            current_time    = finish_time
            done_flags[idx] = True
            completed      += 1

        total_burst = sum(p["cpu_burst_time"] for p in processes)
        cpu_util    = round((total_burst / current_time) * 100, 2) if current_time > 0 else 0
        return done, cpu_util
