# Storage & Computing Bootcamp — Curriculum Tracker

**Curriculum source:** `storage_computing_intensive_plan_2026-11-15.md` (60-session v2; Nov 9 version historical only)

**Last reviewed:** 2026-11-16  
**Session numbering:** Study sessions, not calendar days.  
**Status values:** `not started` / `in progress` / `complete` / `blocked`.  
**Current position:** Day 01 complete; Day 02 not started. No automatic advancement.

## Progress

| Session | Exact topic | Status | Evidence / deliverables | Carry-over / review |
|---|---|---|---|---|
| Day 01 | 简短 Baseline Review + Ubuntu 实验环境核验 | **complete** | `baseline.md`; `day01/env.txt`; `day01/benchmark.py`; `day01/results.csv`; `day01/run.log`; `day01/baseline-review.md`; guided EM responses; `knowledge-map-day01.md` created in chat | Review CPU vs VM utilization Day 02; CPU cache vs RAM/page cache Day 03/10; p99/queueing Day 04/06/07 |
| Day 02 | Process、Syscall 与 Scheduling | **not started** | Awaiting process benchmark | Day 01 CPU ratio concept as prerequisite |
| Day 03 | CPU Cache 与 Memory Hierarchy | **not started** | Awaiting memory-locality experiment | Address page-cache layering misconception |
| Day 04 | Virtual Memory / TLB / Page Fault | **not started** | Awaiting vm-faults.md | Minor/major faults |
| Day 05 | Threads、Processes、Async 与 GIL | **not started** | Awaiting concurrency.csv | Concurrency vs parallelism |
| Day 06 | Queueing、Backpressure 与 Little’s Law | **not started** | Awaiting queue_latency.csv | p99 and queue waiting |
| Day 07 | W1 综合验收 / Computing 基础 | **not started** | Weekly Exit Gate pending | Clean rerun ≥2 labs, five competencies × 0–2, knowledge map, evidence-based EM judgment |
| Day 08–60 | Remaining topics per authoritative v2 syllabus | **not started** | No submitted evidence assessed for these sessions | Prior 1 GiB page-cache experiment reserved as partial carry-over to Day 10, not automatic completion |

## Day 01 assessment (accepted)

- **Final assessment:** 85/100 — Concepts 25/30; Implementation/Reproducibility 28/30; Experimental Reasoning 14/20; Technical Communication/EM 18/20.
- **Environment:** Ubuntu 6.8.0-149-generic; Python 3.12.3; QEMU/UTM; 4 vCPU; 5.8 GiB RAM; ext4; guest virtual disk. Source: submitted `env.txt`.
- **Workloads:** CPU-bound and deliberately paced socket I/O-wait, 3 measured repetitions each. CPU-bound wall ~0.634 s and CPU/wall ~1.0; socket wait wall ~1.182 s and CPU/wall ~0.0185. Results are guest application/process metrics, **not SSD benchmarks**.
- **Reconciliation:** User subsequently pasted matching six-row `run.log` and `results.csv` output in chat. This reconciles the earlier mismatched log and CSV values; the revised files have **not** been re-uploaded as an archive.
- **Concept follow-up:** User correctly explained 1 fully busy vCPU out of 4 as ~25% aggregate capacity under otherwise idle, equal-capacity assumptions. Clarified this is normalization, not automatic distribution of one process across all cores.
- **EM exercise:** Option C (collect evidence before changing workers/SSD), queue/p99 follow-ups Q1=B and Q2=A; scored 18/20.
- **Acceptance:** Day 01 marked **complete** based on submitted baseline, environment, runnable workload, repeated data, limitations, concept and EM follow-up. Remaining misconceptions are review items, not blocking acceptance.

## Knowledge Map & review queue

Knowledge Map file: `knowledge-map-day01.md` (created in chat, not verified on Ubuntu VM).

| Topic | Level | Evidence | Specific gap | Next study session |
|---|---|---|---|---|
| CPU-bound vs I/O-wait; wall/user/sys | L3 (basic lab) | Two workloads ×3 reps | Real storage I/O remains untested | Day 02 |
| Process CPU ratio vs VM utilization | L2 | 4 vCPU → ~25% explanation | Confirm with process/system metrics | Day 02 |
| Queue waiting and p99 | L2 | Guided EM answers | Correlate per-request latency breakdown | Day 06/07 |
| CPU cache, RAM, page cache | L1 | Baseline misconception identified | Page cache is RAM-managed OS cache, not a separate hardware tier | Day 03/10 |
| Virtual memory / page faults | L1 | Partial baseline answers | Minor vs major faults | Day 04 |

**Review cadence:** after approximately 1 / 3 / 7 / 14 *study sessions*, not calendar days. Additional topics and evidence remain in `knowledge-map-day01.md`.

## W1 Exit Gate (Day 07; not yet assessed)

Submit all unaccepted required deliverables for Days 01–06; reproduce at least two experiments from a clean environment; complete five competencies scored 0–2 each; update Knowledge Map; demonstrate an evidence-based guided EM decision. Day 01 evidence can be reused; it does not waive remaining prerequisites.

## Tracker provenance / update rule

This is a **new downloadable tracker** prepared from the available authoritative syllabus and evidence. No existing `curriculum_status.md` was available to edit, and this action **does not modify files inside the Ubuntu VM**. Do not mark subsequent days complete without submitted evidence. On each accepted session, update the relevant row, evidence, carry-over and review queue.
