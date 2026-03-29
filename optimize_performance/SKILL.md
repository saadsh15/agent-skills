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
2.  **Verify Baseline:** Run the existing benchmark/test to confirm the current performance metric.
3.  **Implement (Iterative & Safe):** Apply the optimization.
4.  **Validate:** Run the benchmark/test again. The new metric MUST be significantly better than the baseline. Run the entire test suite to ensure no regressions.
5.  **Mark as Complete:** Once validated, move the file to `optimization_tasks/completed/` or update the markdown file to explicitly state `STATUS: COMPLETED` with the new performance metrics.
6.  **Repeat:** Move to the next file.

### 2. Backend Exhaustive Use Cases & Strategies
When executing optimizations, you must be prepared to implement any of the following advanced backend patterns. Do not settle for surface-level fixes; push the system to the limit:

#### A. Database & Data Access
-   **N+1 Query Annihilation:** Replace lazy loading with aggressive eager loading, JOINs, or dataloader patterns (batching and caching).
-   **Indexing Strategy:** Analyze query plans (e.g., `EXPLAIN ANALYZE`). Add composite indices, covering indices, or partial indices where necessary.
-   **Connection Pooling:** Ensure the database connection pool is optimally sized.
-   **Query Caching:** Implement Redis/Memcached for read-heavy, infrequently changing queries.
-   **Denormalization:** If read performance is critical and joins are too expensive, implement materialized views or denormalized read-models.

#### B. Algorithmic & Compute Efficiency
-   **Big-O Reduction:** Refactor O(N^2) or O(N^3) nested loops into O(N) or O(N log N) using HashMaps, Sets, or efficient sorting.
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

## Execution Flow for `/optimize_performance`

1.  **Check for Directory:** Verify the existence of `optimization_tasks/`. If empty or non-existent, halt and inform the user.
2.  **Inventory:** List all pending optimization `.md` files in the directory.
3.  **Prioritize:** Start with the tasks that have the highest impact (e.g., Database N+1 queries usually yield the highest ROI).
4.  **Execute the Loop:** Follow the "Execution Loop" (Section 1) strictly for the first prioritized task.
5.  **Report & Pause:** After successfully optimizing *one* component and updating its markdown file, present the before/after metrics to the user and ask for permission to proceed to the next file. This ensures the user retains control over the aggressive optimization process.
