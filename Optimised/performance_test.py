import time
import subprocess
import statistics


def run_file(filename, runs=50):
    times = []

    print(f"\nRunning {filename}...")

    # warm-up run
    subprocess.run(["python", filename],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    for i in range(runs):
        start = time.perf_counter()

        subprocess.run(["python", filename],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

        end = time.perf_counter()

        times.append(end - start)

        if (i + 1) % 10 == 0:
            print(f"Completed {i+1}/{runs}")

    return times


# =========================
# SETTINGS
# =========================
RUNS = 50


# =========================
# RUN BOTH SYSTEMS
# =========================
baseline_times = run_file("baseline_system.py", RUNS)
optimised_times = run_file("optimised_system.py", RUNS)


# =========================
# RESULTS
# =========================
baseline_avg = statistics.mean(baseline_times)
optimised_avg = statistics.mean(optimised_times)

baseline_min = min(baseline_times)
optimised_min = min(optimised_times)

baseline_max = max(baseline_times)
optimised_max = max(optimised_times)


print("\n" + "=" * 60)
print("TASK 6: PERFORMANCE COMPARISON")
print("=" * 60)

print(f"{'Metric':<25}{'Baseline':<20}{'Optimised':<20}")
print("-" * 65)

print(f"{'Average Time':<25}{baseline_avg:.6f}s{'':<10}{optimised_avg:.6f}s")
print(f"{'Fastest Run':<25}{baseline_min:.6f}s{'':<10}{optimised_min:.6f}s")
print(f"{'Slowest Run':<25}{baseline_max:.6f}s{'':<10}{optimised_max:.6f}s")


improvement = ((baseline_avg - optimised_avg) / baseline_avg) * 100

print("\nImprovement:")
print(f"{improvement:.2f}% faster in optimised system")

print("\nTEST COMPLETE")
