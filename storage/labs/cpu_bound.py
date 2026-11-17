import time
import hashlib

def cpu_workload(n):
    for i in range(n):
        hashlib.sha256(str(i).encode()).digest()

start = time.perf_counter()
cpu_start = time.process_time()

cpu_workload(2_000_000)

wall_time = time.perf_counter() - start
cpu_time = time.process_time() - cpu_start

print(f"Wall time: {wall_time:.3f}s")
print(f"CPU time: {cpu_time:.3f}s")