# Day 01 Baseline

## Can Explain
1	CPU cache、RAM、Page Cache 有什么区别？
CPU -> CPU cache -> RAM -> Page Cache -> SSD/HDD
CPU cache is managed by hardware, Page Cache is managed by OS
2	CPU-bound 与 I/O-bound 如何分别提升吞吐？
CPU-bound: improve computation efficiency, reduce replication, more cores
I/O-bound: cache, batch, concurrency, improve hardware performance
3	Virtual Memory 中 Page Fault 可能经历什么？
Page not available or it seeks for the page address
4	SSD 为什么需要 GC / Write Amplification？
To improve storage usage efficiency. When there are more and more data deleted, there are more gabage space in one page, but SSD need to write a page as a whole one, so it will copy remain items together to the new place, so it will have WA. 
5	write()、fsync()、durability 有什么区别？
When save a data, write() can return the data is committed but it's not garantee to be written into persistent storage. fsync() will make sure it saved in persistent storage based on protocals. durability makes sure the data can stay if there is disaster such as power off of the system.
6	IOPS、throughput、p99、queue depth 有什么关系？
Throughput = IOPS * size of IO
if throughput is fixed, when queue depth increases, p99 can reduce first and then increase once it hits the bottleneck.

7	怎样公平比较 4KiB random 和 256KiB sequential read？
We need to make sure measure in fixed time. with metrics such as iops, thoughput, p99
8	WAL → MemTable → SSTable → Compaction 的链路是什么？
data will append to WAL to persist the data. Then it updates into MemTable. When MemTable is full, flush into SSTable. Periodadically, SSTables will be compact to make future queries more efficient.
9	B+Tree 和 LSM 分别适合什么 workload？
B+Tree uses a lot in read heavy and LSM for write heavy. But it just in general, more depends on real data.
10	分布式文件系统分离 metadata / data 的收益和代价是什么？
benefit: can be managed seperately and migration easily. 
cost: manage cost
11	Sync / async replication 的 ack 对 latency、RPO、consistency 有何影响？
async ack could have lower latency, but the commit could be lost if disaster happens.
12	如何在不同 GCP storage 产品之间选择并验证性能？
Depends on use cases. If need high performance I/O but local storage, can use LocalSSD. If need distributed backup, need to use cloud solution. 

## Partially Understand

- CPU cache / RAM / page cache
- IOPS / Throughput
- SSD Garbage Collection
- B+Tree vs LSM
- Replication

## Need to Learn

- Page fault
- Queue depth and latency, RPO
- Distributed filesystem metadata
- GCP storage selection