---
name: check-optimize
description: A performance analysis and optimization skill. It performs end-to-end checks for unoptimized code, writes tests to benchmark performance, and logs distinct optimization tasks into a dedicated directory.
when_to_use: Use this skill when the user asks to find performance bottlenecks, optimize the codebase, or invokes the `/check-optimize` command.
---

# Performance Optimization & Benchmarking Skill

## Objective
Your primary goal is to perform a rigorous, end-to-end analysis of an application or feature to identify areas that can be optimized. You must not blindly change code; instead, you will write benchmark/performance tests to prove where the bottlenecks exist. Finally, you will organize your findings by generating separate, component-specific markdown logs inside an `optimization_tasks/` directory to prevent confusion.

## Core Directives

### 1. End-to-End Bottleneck Discovery
- **Identify Inefficiencies:** Look for algorithmic complexity issues (e.g., O(N^2) loops that could be O(N)), redundant database queries (e.g., N+1 query problems), excessive memory allocation, unnecessary network requests, or blocking synchronous operations.
- **Architectural Review:** Check if caching (Redis, CDN, Memoization) could be applied, or if heavy computations can be offloaded to background workers.
- **Frontend/UI:** Look for unnecessary re-renders, large bundle sizes, unoptimized images, or missing lazy-loading.

### 2. Evidence-Based Testing (Write Tests First)
- **Do not guess performance issues.** If you suspect a function is slow, you must write a test or a benchmarking script to prove it.
- Create tests that measure execution time, memory usage, or query count.
- **Instruction:** "Write a script or use the project's testing framework to establish a baseline performance metric before proposing a fix."

### 3. Structured Logging (The `optimization_tasks` Directory)
- You must create a directory named `optimization_tasks` in the root of the project (if it doesn't already exist).
- For every unoptimized component, feature, or function you discover, you must create a *separate* Markdown file inside `optimization_tasks/`.
- **Do not bundle everything into one file.** Keeping them separate prevents confusion.
- *Naming Convention:* `optimization_tasks/[component_name]_optimization.md`

## The Output Format for Task Logs

Every file you generate in `optimization_tasks/` MUST follow this structure:

```markdown
# Optimization Task: [Component or Function Name]

## Description of the Bottleneck
[Explain exactly why this code is unoptimized. Mention time complexity, memory usage, or network latency.]

## Current Performance Metric (Baseline)
[Include the results of the performance test/benchmark you wrote. How long does it currently take? What is the memory footprint?]

## Proposed Optimization Strategy
[Detail your plan. Example: "Implement caching using Redis", "Refactor the nested loop using a hash map", or "Add an index to the database column."]

## Steps to Implement & Verify
1. [Step 1...]
2. [Step 2...]
3. [Run the benchmark test created in `tests/perf/[name].test.ts` to verify the improvement.]
```

## Execution Flow for `/check-optimize [target]`

1. **Analyze Target:** Deeply analyze the file, directory, or feature the user specified. Trace the execution flow end-to-end.
2. **Identify Suspects:** Find the most likely performance bottlenecks.
3. **Write Benchmarks:** Generate the necessary tests or scripts to measure the current performance of those suspects. Ask the user to run them if you cannot.
4. **Create Directory:** Run the command to create the `optimization_tasks/` directory.
5. **Log Findings:** Write a separate `.md` file for each distinct component or issue you found, filling out the required template based on your analysis and test results.
6. **Report:** Provide the user with a brief summary of what you found and list the files you created in the `optimization_tasks/` directory. Do not dump all the details in the chat; point them to the logs.
