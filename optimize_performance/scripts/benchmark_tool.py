#!/usr/bin/env python3
import sys
import os
import time
import subprocess
import statistics
import json
import urllib.request
import urllib.error
import ssl

def print_help():
    print("""
Antigravity Performance Benchmark Tool

Usage:
  python3 benchmark_tool.py command <runs> "<shell_command>"
  python3 benchmark_tool.py http <runs> <url> [headers_json]

Examples:
  # Benchmark a shell command 10 times
  python3 benchmark_tool.py command 10 "python3 main.py --test"
  
  # Benchmark an HTTP API 50 times
  python3 benchmark_tool.py http 50 http://localhost:8000/api/users
""")

def run_command_benchmark(runs, command):
    times = []
    print(f"Benchmarking command: '{command}' over {runs} runs...\n")
    
    # We will use resource module to get peak memory on Unix systems if available
    has_resource = False
    try:
        import resource
        has_resource = True
    except ImportError:
        pass

    peak_rss_kb = 0
    for i in range(runs):
        start = time.perf_counter()
        
        # Run command
        res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elapsed = (time.perf_counter() - start) * 1000 # ms
        times.append(elapsed)
        
        # Get peak RSS if resource is available
        if has_resource:
            # ru_maxrss is in kilobytes on Linux, bytes on macOS
            usage = resource.getrusage(resource.RUSAGE_CHILDREN)
            rss = usage.ru_maxrss
            if sys.platform == 'darwin':
                rss = rss / 1024 # convert bytes to kb
            if rss > peak_rss_kb:
                peak_rss_kb = rss
                
        print(f"  Run {i+1:3}: {elapsed:.2f} ms" + (f" (Peak RSS: {peak_rss_kb/1024:.1f} MB)" if has_resource else ""))
        
    return times, peak_rss_kb

def run_http_benchmark(runs, url, headers_str):
    times = []
    headers = {}
    if headers_str:
        try:
            headers = json.loads(headers_str)
        except Exception as e:
            print(f"Error parsing headers: {e}")
            sys.exit(1)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print(f"Benchmarking HTTP GET: {url} over {runs} runs...\n")
    
    for i in range(runs):
        req = urllib.request.Request(url, headers=headers, method='GET')
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                response.read() # read body to measure full response transfer
                elapsed = (time.perf_counter() - start) * 1000 # ms
                times.append(elapsed)
                print(f"  Run {i+1:3}: {elapsed:.2f} ms (Status: {response.status})")
        except urllib.error.HTTPError as e:
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
            print(f"  Run {i+1:3}: {elapsed:.2f} ms (HTTP Error: {e.code})")
        except Exception as e:
            print(f"  Run {i+1:3}: Failed ({e})")
            
    return times, None

def print_stats(times, peak_rss_kb=None):
    if not times:
        print("No successful runs to calculate statistics.")
        return
        
    total_runs = len(times)
    min_time = min(times)
    max_time = max(times)
    mean_time = statistics.mean(times)
    median_time = statistics.median(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0.0

    print("\n--- Benchmark Statistics ---")
    print(f"  Total Runs: {total_runs}")
    print(f"  Min Time:   {min_time:.2f} ms")
    print(f"  Max Time:   {max_time:.2f} ms")
    print(f"  Mean:       {mean_time:.2f} ms")
    print(f"  Median:     {median_time:.2f} ms")
    print(f"  Std Dev:    {std_dev:.2f} ms")
    
    if peak_rss_kb:
        print(f"  Peak RSS:   {peak_rss_kb / 1024:.2f} MB")
    print("----------------------------")
    
    # Return dictionary for JSON export
    return {
        "total_runs": total_runs,
        "min_ms": min_time,
        "max_ms": max_time,
        "mean_ms": mean_time,
        "median_ms": median_time,
        "std_dev_ms": std_dev,
        "peak_rss_mb": peak_rss_kb / 1024 if peak_rss_kb else None
    }

def main():
    if len(sys.argv) < 4 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)
        
    mode = sys.argv[1].lower()
    try:
        runs = int(sys.argv[2])
    except ValueError:
        print("Runs must be an integer.")
        sys.exit(1)
        
    target = sys.argv[3]
    headers_str = sys.argv[4] if len(sys.argv) > 4 else None
    
    if mode == "command":
        times, peak_rss = run_command_benchmark(runs, target)
    elif mode == "http":
        times, peak_rss = run_http_benchmark(runs, target, headers_str)
    else:
        print(f"Unknown mode: {mode}")
        print_help()
        sys.exit(1)
        
    stats = print_stats(times, peak_rss)
    
    # Save to benchmark_results.json for comparison tracking
    if stats:
        try:
            with open("benchmark_results.json", "w") as f:
                json.dump(stats, f, indent=2)
            print("Results saved to 'benchmark_results.json'.")
        except Exception as e:
            print(f"Could not save benchmark_results.json: {e}")

if __name__ == "__main__":
    main()
