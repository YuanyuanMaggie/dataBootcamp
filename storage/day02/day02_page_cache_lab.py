#!/usr/bin/env python3
"""Day 02: Linux buffered file I/O vs page cache; run inside an Ubuntu VM."""
import argparse
import os
import sys
from pathlib import Path
import time

MIB = 1024 * 1024


def self_io():
    try:
        with open('/proc/self/io', 'r', encoding='ascii') as f:
            return {k.rstrip(':'): int(v) for line in f if (parts := line.split())
                    for k, v in [parts]}
    except (OSError, ValueError):
        return {}


def prepare(path: Path, size_mib: int):
    nbytes = size_mib * MIB
    if path.exists():
        if path.stat().st_size != nbytes:
            raise SystemExit(f'{path} exists with a different size; choose another --file (no overwrite).')
        print(f'Using existing {path} ({size_mib} MiB)', file=sys.stderr)
        return
    print(f'Creating {path} ({size_mib} MiB of non-sparse test data)...', file=sys.stderr, flush=True)
    with path.open('xb', buffering=0) as f:
        for _ in range(size_mib):
            f.write(os.urandom(MIB))
        os.fsync(f.fileno())  # ensure this file's dirty data is synchronized before eviction attempts
    print('File prepared and fsync completed.', file=sys.stderr, flush=True)


def read_trial(path: Path, label: str, advise_evict: bool):
    with path.open('rb', buffering=0) as f:
        if advise_evict:
            if not hasattr(os, 'posix_fadvise') or not hasattr(os, 'POSIX_FADV_DONTNEED'):
                raise SystemExit('posix_fadvise(DONTNEED) unavailable: use a Linux/Python VM.')
            os.posix_fadvise(f.fileno(), 0, 0, os.POSIX_FADV_DONTNEED)
        before = self_io()
        wall_start = time.perf_counter()
        cpu_start = time.process_time()
        nread = 0
        checksum = 0
        while True:
            block = os.read(f.fileno(), MIB)
            if not block:
                break
            nread += len(block)
            checksum ^= block[0]
        cpu_s = time.process_time() - cpu_start
        wall_s = time.perf_counter() - wall_start
        after = self_io()
    read_bytes = after.get('read_bytes', 0) - before.get('read_bytes', 0)
    rchar = after.get('rchar', 0) - before.get('rchar', 0)
    print(f'{label},{nread},{wall_s*1000:.2f},{cpu_s*1000:.2f},'
          f'{nread/MIB/wall_s:.1f},{read_bytes},{rchar},{checksum}', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mib', type=int, default=256)
    parser.add_argument('--file', type=Path, default=Path('data.bin'))
    args = parser.parse_args()
    if not 8 <= args.mib <= 1024:
        parser.error('--mib must be between 8 and 1024 (safety cap).')
    prepare(args.file, args.mib)
    print('trial,bytes,wall_ms,cpu_ms,throughput_MiB_s,proc_read_bytes,rchar,checksum', flush=True)
    for i in range(1, 4):
        read_trial(args.file, f'evict_attempt_{i}', advise_evict=True)
        read_trial(args.file, f'warm_{i}', advise_evict=False)


if __name__ == '__main__':
    main()
