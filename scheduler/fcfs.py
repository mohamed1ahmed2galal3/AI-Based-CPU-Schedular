class FCFSScheduler:
    """First Come First Serve — بيشغّل الـ processes بترتيب وصولها"""

    def run(self, processes):
        # ترتيب حسب arrival_time
        queue = sorted(processes, key=lambda p: p["arrival_time"])

        current_time = 0
        results = []

        for p in queue:
            # لو الـ CPU فاضية وفيه وقت قبل وصول الـ process
            if current_time < p["arrival_time"]:
                current_time = p["arrival_time"]

            start_time      = current_time
            burst           = p["cpu_burst_time"]
            finish_time     = current_time + burst
            waiting_time    = start_time - p["arrival_time"]
            turnaround_time = finish_time - p["arrival_time"]
            response_time   = waiting_time  # في FCFS أول استجابة = وقت الانتظار

            results.append({
                "process_id":       p["process_id"],
                "process_type":     p["process_type"],
                "arrival_time":     p["arrival_time"],
                "cpu_burst_time":   burst,
                "start_time":       start_time,
                "finish_time":      finish_time,
                "waiting_time":     round(waiting_time, 4),
                "turnaround_time":  round(turnaround_time, 4),
                "response_time":    round(response_time, 4),
            })

            current_time = finish_time

        # CPU Utilization = وقت الشغل الفعلي / الوقت الكلي
        total_burst    = sum(p["cpu_burst_time"] for p in processes)
        total_time     = current_time if current_time > 0 else 1
        cpu_util       = round((total_burst / total_time) * 100, 2)

        return results, cpu_util
