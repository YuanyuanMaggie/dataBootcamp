# Day 02 — Process Benchmark Analysis

## 1. Environment
- CPU logical cores: 4
- CPU quota: No bandwidth quota configured in the checked session and parent cgroups (max 100000)
- Python version: 3.12.3

## 2. Hypothesis
运行实验前，我预计：
- 1 worker：1x
- 2 workers：0.5x
- 4 workers：0.35x

原因：
对于CPU-bounded task, 增加workers一般能减少wall time。但是不是等比例减少。会有一些损耗在别的地方。

## 3. Results
- 1 worker 平均 wall time：0.4330s
- 2 workers 平均 wall time：0.2451s
- 4 workers 平均 wall time：0.1281s
- 最快的配置：4 workers
- 2 workers speedup（相对 1 worker）：1.77×
- 4 workers speedup（相对 1 worker）：3.38×

## 4. Analysis
**Q1. 为什么最快的 worker 数量是这个？**

我的解释：我们有4个CPU cores，可以让4个workers同时计算，大大减少wall time

**Q2. CPU time 和 wall time 有什么区别？你的实验是否观察到并行执行？**

我的解释：CPU time是CPU 实际参与计算的时间，而wall time是真实世界的时间。有并行，因为在workers为2或者4的时候，总CPU time 大于 wall time

**Q3. 实验结果是否符合假设？有哪些其他可能的影响因素？**

我的解释：符合。CPU scheduling等其他因素都会影响结果。
process startup、IPC、VM 噪声

**Q4. 这些结果能否证明增加 workers 一定提高生产环境的 throughput？为什么？**

我的解释：不一定。取决于生产环境是否能并行处理，cpu是否饱和等。我们还需要看具体情况。

## 5. Limitations
- 实验中可能存在的干扰：VM operations
- 我还没有验证的假设：workers大于cpu cores的影响是否会导致throtting 跟queue的增加。
- 如果再做一次实验，我会改进：继续增加workers数量看是不是会变慢
任务运行时间非常短（约 0.13–0.43 秒），实验噪声和进程启动开销的相对影响可能较大。2 workers 三次 wall time 的变异系数约 7.8%，建议在后续性能实验中使用更长的测试时间。

## 6. Conclusion
用 2–3 句话总结实验发现和证据边界。
对于CPU-bounded task, 增加workers一般能减少wall time。但是不是等比例减少。会有一些损耗在别的地方。
还不能证明 4 workers 是全局最优
还不能把未达到 4× 的原因归结为 context switching