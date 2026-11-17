
import argparse
import csv
import multiprocessing as mp
import os
import resource
import time


def cpu_work(start, stop):
    result = 0
    for i in range(start, stop):
        result += (i * i) % 1000003
    return result


def worker(args):
    start, stop = args
    t0 = time.perf_counter()
    cpu0 = time.process_time()
    result = cpu_work(start, stop)
    return (
        result,
        time.perf_counter() - t0,
        time.process_time() - cpu0,
    )


def run(workers, n):
    ranges = [
        (n * i // workers, n * (i + 1) // workers)
        for i in range(workers)
    ]

    t0 = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)

    with mp.Pool(processes=workers) as pool:
        results = pool.map(worker, ranges)

    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    wall = time.perf_counter() - t0

    return {
        "workers": workers,
        "iterations": n,
        "wall_s": wall,
        "user_s": after.ru_utime - before.ru_utime,
        "sys_s": after.ru_stime - before.ru_stime,
        "worker_cpu_s": sum(r[2] for r in results),
        "cpu_per_wall": (
            sum(r[2] for r in results) / wall
        ),
        "checksum": sum(r[0] for r in results),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, required=True)
    parser.add_argument("--iterations", type=int, default=8000000)
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--output", default="process-benchmark.csv")
    args = parser.parse_args()

    rows = []
    for rep in range(args.repeat):
        row = run(args.workers, args.iterations)
        row["repeat"] = rep + 1
        rows.append(row)
        print(row, flush=True)

    with open(args.output, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)
