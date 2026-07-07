#!/usr/bin/env python3
import sys
import os
import cProfile
import pstats
import io

def print_help():
    print("""
Antigravity Python Code Profiler

Usage:
  python3 profile_code.py <sort_by> <script_path> [arguments...]

Available sort options:
  tottime   - Total time spent in the function itself (excludes sub-calls)
  cumtime   - Cumulative time spent in the function and all sub-calls
  calls     - Number of times the function was called
  name      - Alphabetical by function name

Example:
  python3 profile_code.py cumtime app.py --mode=test
""")

def main():
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    sort_by = sys.argv[1]
    if sort_by not in ("tottime", "cumtime", "calls", "name"):
        print(f"Invalid sort option: {sort_by}. Defaulting to 'cumtime'.")
        sort_by = "cumtime"

    script_path = sys.argv[2]
    if not os.path.exists(script_path):
        print(f"Script path not found: {script_path}")
        sys.exit(1)

    # Set up sys.argv for the target script
    target_args = sys.argv[2:]
    sys.argv = target_args

    # Add the target script's directory to python path
    script_dir = os.path.dirname(os.path.abspath(script_path))
    sys.path.insert(0, script_dir)

    print(f"Profiling '{script_path}' sorted by '{sort_by}'...\n")

    # Start profiling
    pr = cProfile.Profile()
    pr.enable()

    try:
        # Run the script globally
        with open(script_path, 'rb') as file:
            code = compile(file.read(), script_path, 'exec')
            # Set up globals for execution context
            exec_globals = {
                "__file__": script_path,
                "__name__": "__main__",
                "__package__": None,
                "__cached__": None,
            }
            exec(code, exec_globals)
    except SystemExit as e:
        # Catch sys.exit() calls from the target script gracefully
        pass
    except Exception as e:
        print(f"\nExecution crashed during profiling:\n{e}")
        import traceback
        traceback.print_exc()
    finally:
        pr.disable()
        print("\n=== Profiler Execution Complete ===")

        # Format stats
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
        
        # Limit to top 30 functions to avoid overwhelming output
        ps.print_stats(30)
        
        print("\nTop 30 Functions:")
        print(s.getvalue())

if __name__ == "__main__":
    main()
