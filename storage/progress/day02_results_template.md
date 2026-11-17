# Day 02 — Page Cache vs Block I/O

## Environment
- Date: Nov 14 2026
- Linux kernel (`uname -r`): 6.8.0-149-generic
- Python (`python3 --version`): 3.12.3
- VM provider / storage type (known/unknown): qemu, ext4
- Filesystem (`findmnt -T . -o TARGET,SOURCE,FSTYPE`):
TARGET
  SOURCE                            FSTYPE
/ /dev/mapper/ubuntu--vg-ubuntu--lv ext4

- RAM (`free -h`): 
               total        used        free      shared  buff/cache   available
Mem:           5.8Gi       1.1Gi       4.2Gi       5.2Mi       582Mi       4.7Gi
Swap:          4.0Gi          0B       4.0Gi
- Free disk (`df -h .`):
Filesystem                         Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv   46G  7.5G   37G  18% /
- Test data size (MiB): 1024
- Test file mounted on persistent filesystem? (yes/no/unknown):

## Hypotheses (write before running)
- Evict attempt vs warm read wall time:
- Evict attempt vs warm `proc_read_bytes`:
- CPU time vs wall time:

## Measurements
Paste `results.csv` here or attach it. Also include at least 1 `iostat -dx 1` snippet during an evict-attempt read if available.

trial,bytes,wall_ms,cpu_ms,throughput_MiB_s,proc_read_bytes,rchar,checksum
evict_attempt_1,1073741824,636.94,621.96,1607.7,1073741824,1073741924,175
warm_1,1073741824,134.79,134.77,7596.8,0,1073741937,175
evict_attempt_2,1073741824,317.12,239.06,3229.1,1073741824,1073741937,175
warm_2,1073741824,44.62,44.62,22950.1,0,1073741937,175
evict_attempt_3,1073741824,267.20,194.41,3832.3,1073741824,1073741937,175
warm_3,1073741824,44.86,44.84,22826.9,0,1073741937,175

## Interpretation
1. What evidence suggests a page-cache hit rather than backing-storage reads? 
The warm reads were significantly faster, and proc_read_bytes dropped from 1 GiB to 0 while rchar remained approximately 1 GiB. This strongly suggests that the data was served from the Linux page cache rather than requiring new block reads.
2. Why is seeing a `read()` call insufficient to prove actual SSD reads? it could read from page cache. application → kernel → page cache
3. Did `posix_fadvise(DONTNEED)` cause block I/O on every trial? What do the counters show? Yes. 
Every read following DONTNEED triggered 1 GiB of storage-layer reads. All three warm reads triggered zero. This suggests that the eviction hint was effective in this experiment.
4. Could readahead, hypervisor/host caches, tmpfs, filesystem compression, and background I/O affect these results? yes. Readahead can read following pages into page cache, which affect actual I/O request size and latency. 
Yes — ext4 on an LVM logical volume, rather than tmpfs; underlying host storage durability is not independently verified.
5. If a benchmark reports 10 GiB/s from an SSD rated 3 GiB/s, what questions would you ask? how much read from page cache
进一步还应该检查：
- 是否使用 buffered I/O 或 O_DIRECT？
- 设备层 iostat 显示多少实际 read throughput？
- 是否存在 VM host cache？
- 测试是 sequential 还是 random？Block size 和 concurrency 是多少？
这些因素决定了这个 benchmark 到底在测量什么。

## EM decision (5 sentences)
A team reports a 5x improvement after a cache change based on a single warm-cache microbenchmark. Decide whether to approve an optimization rollout. Define production workload, performance metric, cold/warm mix, and safety/reliability checks.
We still need more evidence and see the pattern. 

I would not approve a full rollout based on a single warm-cache benchmark.

First, I would ask the team to characterize the production workload, including read patterns, file sizes, concurrency, and cache hit rates.

Second, I would require cold-cache, warm-cache, and representative mixed-workload benchmarks, measuring throughput, IOPS, p50/p99 latency, and CPU utilization.

Third, I would evaluate the optimization's impact on memory consumption, cache eviction, reliability, and infrastructure cost.

Finally, I would approve a limited canary rollout only if the results meet our production SLOs without unacceptable regressions, with monitoring and rollback criteria defined in advance.

## Day 01 carry-over (if unfinished)
- `baseline.md` status: done
- Day 01 code and wall/CPU/fsync results status:
- What remains unknown:
