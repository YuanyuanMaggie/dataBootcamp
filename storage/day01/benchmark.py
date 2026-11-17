
import csv
import resource
import socket
import threading
import time

CPU_LOOPS = 12_000_000
IO_CHUNKS = 100
IO_CHUNK_BYTES = 4096
IO_INTERVAL_S = 0.01
REPEATS = 3


def cpu_task():
    value = 0
    for i in range(CPU_LOOPS):
        value = (value + i * 17) % 1_000_000_007
    return value


def io_task():
    reader, writer = socket.socketpair()

    def sender():
        with writer:
            for _ in range(IO_CHUNKS):
                time.sleep(IO_INTERVAL_S)
                writer.sendall(b"x" * IO_CHUNK_BYTES)

    t = threading.Thread(target=sender)
    t.start()

    total = 0
    with reader:
        while True:
            data = reader.recv(65536)
            if not data:
                break
            total += len(data)

    t.join()
    assert total == IO_CHUNKS * IO_CHUNK_BYTES
    return total


def measure(name, func, rep):
    before = resource.getrusage(resource.RUSAGE_SELF)
    start = time.perf_counter()

    result = func()

    wall = time.perf_counter() - start
    after = resource.getrusage(resource.RUSAGE_SELF)

    user = after.ru_utime - before.ru_utime
    sys = after.ru_stime - before.ru_stime

    return [
        name,
        rep,
        round(wall, 6),
        round(user, 6),
        round(sys, 6),
        round((user + sys) / wall, 4),
        result,
    ]


def main():
    cases = [
        ("cpu", cpu_task),
        ("socket_io", io_task),
    ]

    # Warm-up: not included in results
    for _, fn in cases:
        fn()

    rows = []
    for rep in range(1, REPEATS + 1):
        for name, fn in cases:
            row = measure(name, fn, rep)
            rows.append(row)
            print(row)

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "mode", "rep", "wall_s", "user_s",
            "sys_s", "cpu_over_wall", "result"
        ])
        writer.writerows(rows)

    print("Saved results.csv")


if __name__ == "__main__":
    main()
