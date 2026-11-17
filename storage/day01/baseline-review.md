Day 01 Hypotheses
CPU-bound: CPU-bound 的 CPU time 接近 wall time，因为任务主要在执行计算。
I/O-bound: I/O-bound 的 wall time 明显大于 CPU time，因为接收数据时需要等待。

Limitation：
1. Socket I/O 不是 storage I/O，因此本实验不能证明任何 SSD IOPS、bandwidth 或 p99 性能。
2. VM scheduling、host contention 和 CPU quota 可能影响 wall time。
3. 只有 3 次重复，足够观察基本现象，不足以报告生产级 tail latency。

Questions:
Q1. 一个 API 的 wall time 为 500 ms，user CPU time 为 20 ms，system CPU time 为 5 ms。它一定是磁盘慢吗？为什么？
No. It could be other reasons such as there are long waiting queue.

Q2. 如果一个 Python 程序调用 time.sleep(2)，wall time 和 CPU time 可能是什么关系？这能证明 SSD 很慢吗？
Wall time could be around 2 seconds more than CPU time. No. The cpu just unscheduled for this program.

Q3. CPU-bound 程序的 CPU ratio 接近 1，为什么这不代表整台 VM 的 CPU utilization 是 100%？
CPU also have other things to do.
单进程 CPU ratio 接近 1，只说明它平均占用了约一个 CPU core 的计算时间。你的 VM 有 4 个 vCPU，所以不能据此说整个 VM 的 CPU utilization 达到 100%。

Q4. 如果两次 benchmark 的 wall time 差距很大，你需要记录哪些环境或执行条件，才能判断性能是否真的变化？
queue waiting time, cpu times and etc.
需要记录两次运行的具体条件，例如 VM vCPU/RAM、CPU quota、运行时负载、warm-up、workload 参数、重复次数，以及是否有 host contention，而不只是 queue waiting 和 CPU times。