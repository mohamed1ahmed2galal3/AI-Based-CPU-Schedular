from collections import deque

class RoundRobinScheduler:
    """Round Robin — بيدي كل process نفس الـ time quantum بالتساوي"""

    def __init__(self, quantum=10):
        self.quantum = quantum  # ms

    def run(self, processes):
        # نسخة من الـ processes مع remaining burst
        procs = [
            {**p, "remaining": p["cpu_burst_time"], "first_run": None}
            for p in sorted(processes, key=lambda x: x["arrival_time"])
        ]

        queue        = deque()
        current_time = procs[0]["arrival_time"]  # نبدأ من أول arrival_time
        done         = []
        i            = 0  # index للـ process اللي لسه ما دخلتش الـ queue

        # نحط أول process في الـ queue
        while i < len(procs) and procs[i]["arrival_time"] <= current_time:
            queue.append(procs[i])
            i += 1

        while queue:
            p = queue.popleft()

            # أول مرة بتشتغل
            if p["first_run"] is None:
                p["first_run"] = current_time

            run_time = min(self.quantum, p["remaining"])
            current_time    += run_time
            p["remaining"]  -= run_time

            # نضيف الـ processes اللي وصلت خلال هذا الـ quantum
            while i < len(procs) and procs[i]["arrival_time"] <= current_time:
                queue.append(procs[i])
                i += 1

            if p["remaining"] > 0:
                # لسه ما خلصتش — ترجع للـ queue
                queue.append(p)
            else:
                # خلصت
                finish_time     = current_time
                waiting_time    = finish_time - p["arrival_time"] - p["cpu_burst_time"]
                turnaround_time = finish_time - p["arrival_time"]
                response_time   = p["first_run"] - p["arrival_time"]

                done.append({
                    "process_id":       p["process_id"],
                    "process_type":     p["process_type"],
                    "arrival_time":     p["arrival_time"],
                    "cpu_burst_time":   p["cpu_burst_time"],
                    "finish_time":      finish_time,
                    "waiting_time":     round(max(waiting_time, 0), 4),
                    "turnaround_time":  round(turnaround_time, 4),
                    "response_time":    round(max(response_time, 0), 4),
                })

            # لو الـ queue فاضية وفيه processes لسه
            if not queue and i < len(procs):
                current_time = procs[i]["arrival_time"]
                queue.append(procs[i])
                i += 1

        total_burst = sum(p["cpu_burst_time"] for p in processes)
        total_time  = current_time if current_time > 0 else 1
        cpu_util    = round((total_burst / total_time) * 100, 2)

        return done, cpu_util