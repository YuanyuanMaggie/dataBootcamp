import os
import time

FILE = "test_data.bin"
SIZE_MB = 256
CHUNK = b"x" * (1024 * 1024)

start = time.perf_counter()

with open(FILE, "wb") as f:
    for _ in range(SIZE_MB):
        f.write(CHUNK)
    # f.flush()
    # os.fsync(f.fileno())

write_time = time.perf_counter() - start

start = time.perf_counter()

with open(FILE, "rb") as f:
    while f.read(1024 * 1024):
        pass

read_time = time.perf_counter() - start

print(f"Buffered write time: {write_time:.3f}s")
print(f"Read time: {read_time:.3f}s")

os.remove(FILE)