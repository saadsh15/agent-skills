#!/usr/bin/env python3
import sys
import re
from collections import Counter

# Common error keywords to look for
ERROR_KEYWORDS = [
    r"(?i)exception",
    r"(?i)error",
    r"(?i)failed",
    r"(?i)fatal",
    r"(?i)uncaught",
    r"(?i)traceback",
    r"(?i)crash",
    r"(?i)promise rejection"
]

ERROR_PATTERN = re.compile("|".join(ERROR_KEYWORDS))

# Regex to match Python/JS stack trace line formats:
# e.g., File "app.py", line 42, in my_func
# e.g., at myFunc (index.js:42:15)
STACK_LINE_PATTERN = re.compile(
    r'(File\s+"(?P<py_file>[^"]+)",\s+line\s+(?P<py_line>\d+))|'
    r'(\((?P<js_file>[^:]+):(?P<js_line>\d+):(?P<js_col>\d+)\))'
)

def print_help():
    print("""
Log Analyzer: Analyze application logs for errors and stack traces.

Usage:
  python3 log_analyzer.py [log_file_path]
  cat app.log | python3 log_analyzer.py
""")

def analyze_stream(stream):
    lines = stream.readlines()
    total_lines = len(lines)
    
    error_lines = []
    stack_traces = []
    current_trace = []
    in_traceback = False
    
    file_occurrences = Counter()
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Check if line indicates start of a stack trace or contains trace details
        is_stack_line = STACK_LINE_PATTERN.search(line_stripped)
        if "Traceback (" in line or "stack trace" in line or line_stripped.startswith("at ") or is_stack_line:
            in_traceback = True
            current_trace.append((i + 1, line_stripped))
            
            # Extract file and line info if available
            m = STACK_LINE_PATTERN.search(line_stripped)
            if m:
                gd = m.groupdict()
                file_path = gd.get("py_file") or gd.get("js_file")
                line_no = gd.get("py_line") or gd.get("js_line")
                if file_path:
                    # Keep basename for neatness
                    basename = file_path.split("/")[-1]
                    file_occurrences[f"{basename}:{line_no}"] += 1
            continue
        
        if in_traceback:
            # Traceback lines are usually indented or start with specific prefixes
            if line.startswith(" ") or line.startswith("\t") or not line_stripped:
                current_trace.append((i + 1, line_stripped))
                continue
            else:
                # End of traceback
                if current_trace:
                    stack_traces.append(current_trace)
                    current_trace = []
                in_traceback = False
        
        # Check standard error patterns
        if ERROR_PATTERN.search(line_stripped):
            error_lines.append((i + 1, line_stripped))
            
    # Flush remaining trace
    if current_trace:
        stack_traces.append(current_trace)
        
    # Output formatting
    print("=== Antigravity Debug Helper: Log Analysis Report ===")
    print(f"Total lines scanned: {total_lines}")
    print(f"Total error/fatal matches found: {len(error_lines)}")
    print(f"Total stack traces identified: {len(stack_traces)}")
    
    if file_occurrences:
        print("\n--- Top Exception/Error Locations ---")
        for loc, count in file_occurrences.most_common(5):
            print(f"  {loc:30} : {count} times")
            
    if error_lines:
        print("\n--- Recent Error Highlights ---")
        # Print top 10 error lines
        for lno, text in error_lines[-10:]:
            print(f"  Line {lno:5}: {text[:100] + '...' if len(text) > 100 else text}")
            
    if stack_traces:
        print("\n--- Stack Traces Captured ---")
        for idx, trace in enumerate(stack_traces[:3]): # Show up to 3 traces
            print(f"\n  Trace #{idx+1} (starts at line {trace[0][0]}):")
            for lno, text in trace[-8:]: # Show last 8 lines of the trace
                print(f"    {text}")
        if len(stack_traces) > 3:
            print(f"\n  ... and {len(stack_traces) - 3} more stack trace(s) omitted.")
            
    print("\n=====================================================")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print_help()
            sys.exit(0)
        filepath = sys.argv[1]
        try:
            with open(filepath, "r", errors="ignore") as f:
                analyze_stream(f)
        except Exception as e:
            print(f"Failed to read file '{filepath}': {e}")
            sys.exit(1)
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print_help()
            sys.exit(0)
        analyze_stream(sys.stdin)

if __name__ == "__main__":
    main()
