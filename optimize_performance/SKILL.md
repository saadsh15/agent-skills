---
name: optimize_performance
description: A relentless, backend-focused execution skill that systematically implements the performance optimizations logged in the `optimization_tasks/` directory until the application is pushed to its absolute performance limits.
when_to_use: Use this skill when the user asks to apply performance optimizations, execute optimization tasks, or invokes the `/optimize_performance` command.
---

# Ultimate Backend Performance Optimization Skill

## Objective
Your sole purpose is to systematically, relentlessly, and safely execute the performance optimization tasks logged in the `optimization_tasks/` directory. You will focus primarily on backend infrastructure (APIs, databases, background jobs, memory management). Your goal is to optimize the application to its absolute limit—until no further optimizations can mathematically or practically be made—without breaking existing functionality. You must not fail. You must prove your optimizations work.

## Core Mandates

### 1. The Execution Loop (Step-by-Step)
You must NOT attempt to optimize everything at once. You will process the `optimization_tasks/` directory one file at a time.
For each `[component]_optimization.md` file:
1.  **Read and Understand:** Parse the bottleneck, the baseline metric, and the proposed strategy.
2.  **Verify Baseline:** Run the existing benchmark/test, or utilize [benchmark_tool.py](file:///home/saad/.gemini/config/skills/optimize_performance/scripts/benchmark_tool.py) or [profile_code.py](file:///home/saad/.gemini/config/skills/optimize_performance/scripts/profile_code.py) to measure and log the precise baseline metric and execution hotspots.
3.  **Implement (Iterative & Safe):** Apply the optimization.
4.  **Validate:** Run the benchmark/test again using the same profiling/benchmarking tools. The new metric MUST be significantly better than the baseline. Run the entire test suite to ensure no regressions.
5.  **Mark as Complete:** Once validated, move the file to `optimization_tasks/completed/` or update the markdown file to explicitly state `STATUS: COMPLETED` with the new performance metrics.
6.  **Repeat:** Move to the next file.

### 2. Backend Exhaustive Use Cases & Strategies
When executing optimizations, you must be prepared to implement any of the following advanced backend patterns. Do not settle for surface-level fixes; push the system to the limit:

#### A. Database & Data Access
-   **N+1 Query Annihilation:** Replace lazy loading with aggressive eager loading, JOINs, or dataloader patterns (batching and caching). Use [analyze_db_queries.py](file:///home/saad/.gemini/config/skills/optimize_performance/scripts/analyze_db_queries.py) to scan codebase directories for N+1 query patterns.
-   **Indexing Strategy:** Analyze query plans (e.g., SQLite `EXPLAIN QUERY PLAN` via [analyze_db_queries.py](file:///home/saad/.gemini/config/skills/optimize_performance/scripts/analyze_db_queries.py) or database native `EXPLAIN ANALYZE`). Add composite indices, covering indices, or partial indices where necessary.
-   **Connection Pooling:** Ensure the database connection pool is optimally sized.
-   **Query Caching:** Implement Redis/Memcached for read-heavy, infrequently changing queries.
-   **Denormalization:** If read performance is critical and joins are too expensive, implement materialized views or denormalized read-models.

#### B. Algorithmic & Compute Efficiency
-   **Big-O Reduction:** Refactor O(N^2) or O(N^3) nested loops into O(N) or O(N log N) using HashMaps, Sets, or efficient sorting. Use [profile_code.py](file:///home/saad/.gemini/config/skills/optimize_performance/scripts/profile_code.py) to pinpoint functions taking the most cpu time.
-   **Memory Allocation:** Prevent memory leaks and garbage collection pauses. Use object pooling if necessary. Stream large files/data instead of loading them entirely into RAM.
-   **Concurrency & Parallelism:** 
    -   *Node.js:* Use `Worker Threads` for CPU-bound tasks or `Promise.all` for independent I/O tasks.
    -   *Python:* Use `asyncio` for I/O, `multiprocessing` for CPU-bound tasks.
    -   *Go/Rust:* Maximize goroutines/threads safely.

#### C. Network & API Layer
-   **Payload Compression:** Ensure gzip/brotli is enabled.
-   **Serialization Speed:** Swap slow serializers (e.g., native JSON) for faster alternatives (e.g., Protocol Buffers, MessagePack, or optimized JSON parsers like `simdjson`).
-   **Pagination & Cursoring:** Replace offset-based pagination with cursor-based pagination for large datasets.

#### D. Architecture & Background Processing
-   **Offloading:** Move synchronous, heavy operations (e.g., sending emails, image processing, PDF generation) to background job queues (e.g., Celery, BullMQ, Sidekiq, RabbitMQ).

### 3. Absolute Robustness & Anti-Failure Protocols
-   **Never Break the Build:** If an optimization breaks a core unit test, you must REVERT the optimization, analyze the failure, and try a different approach. Performance does not trump correctness.
-   **The "Limit" Check:** Before concluding an optimization, ask yourself: "Can this be faster?" 
    -   *Did I just cache it?* Can I cache it closer to the edge?
    -   *Did I parallelize it?* Am I hitting connection limits?
    -   *If the limit is reached:* State clearly why it cannot be optimized further (e.g., "Network latency to the database is the remaining bottleneck, theoretical minimum reached").

### 4. Performance Optimization Helper Scripts
You have access to a set of specialized helper tools located in the [scripts/](file:///home/saad/.gemini/config/skills/optimize_performance/scripts) directory:
-   **[benchmark_tool.py](file:///home/saad/.gemini/config/skills/optimize_performance/scripts/benchmark_tool.py):** Run commands or HTTP URLs repeatedly to calculate statistical execution latencies (min, max, mean, stddev) and track peak memory consumption.
-   **[profile_code.py](file:///home/saad/.gemini/config/skills/optimize_performance/scripts/profile_code.py):** Profile Python execution paths to pinpoint exactly which functions are responsible for the highest CPU/cumulative running times.
-   **[analyze_db_queries.py](file:///home/saad/.gemini/config/skills/optimize_performance/scripts/analyze_db_queries.py):** Scan static codebase source files for N+1 ORM query patterns or run SQLite query plan analysis to find table scan bottlenecks.

## Execution Flow for `/optimize_performance`

1.  **Check for Directory:** Verify the existence of `optimization_tasks/`. If empty or non-existent, halt and inform the user.
2.  **Inventory:** List all pending optimization `.md` files in the directory.
3.  **Prioritize:** Start with the tasks that have the highest impact (e.g., Database N+1 queries usually yield the highest ROI).
4.  **Execute the Loop:** Follow the "Execution Loop" (Section 1) strictly for the first prioritized task.
5.  **Report & Pause:** After successfully optimizing *one* component and updating its markdown file, present the before/after metrics to the user and ask for permission to proceed to the next file. This ensures the user retains control over the aggressive optimization process.
