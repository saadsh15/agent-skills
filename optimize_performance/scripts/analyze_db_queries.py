#!/usr/bin/env python3
import sys
import os
import re
import sqlite3

def print_help():
    print("""
Antigravity DB Query Optimizer & N+1 Loop Finder

Usage:
  # Find potential N+1 database queries in code files (.py, .js, .ts, .go)
  python3 analyze_db_queries.py scan <directory_path>
  
  # Explain SQLite query plans and inspect for table scans
  python3 analyze_db_queries.py explain <sqlite_db_file> "<sql_query>"

Examples:
  python3 analyze_db_queries.py scan ./src
  python3 analyze_db_queries.py explain app.db "SELECT * FROM users WHERE email = 'test@example.com'"
""")

# Regex patterns that indicate a database fetch call (ORM or raw SQL)
DB_FETCH_PATTERNS = [
    r"\.(find|findAll|findOne|get|select|update|delete|create)\(",
    r"db\.query\(",
    r"execute\(",
    r"session\.query\(",
    r"objects\.(all|filter|get)\(",
]
DB_REGEX = re.compile("|".join(DB_FETCH_PATTERNS))

# Loop structures in python, JS, TS, Go
LOOP_PATTERNS = [
    r"\bfor\b",
    r"\bwhile\b",
    r"\.forEach\(",
    r"\.map\(",
]
LOOP_REGEX = re.compile("|".join(LOOP_PATTERNS))

def scan_nplusone(directory):
    print(f"Scanning '{directory}' for potential N+1 queries...\n")
    matches_found = 0
    
    # Supported extensions
    extensions = ('.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rb', '.java')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(extensions):
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', errors='ignore') as f:
                    lines = f.readlines()
            except Exception:
                continue

            # Basic heuristic: Check if database-like methods occur near/inside loops
            # We track loop block scope or simple consecutive line presence
            in_loop = False
            loop_indent = -1
            
            for line_no, line in enumerate(lines, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith(("//", "#", "/*", "*")):
                    continue
                
                # Check if entering loop
                if LOOP_REGEX.search(stripped):
                    in_loop = True
                    # Simple indent calculation
                    loop_indent = len(line) - len(line.lstrip())
                    continue
                
                # Check if exiting loop (indentation decreased)
                if in_loop and (len(line) - len(line.lstrip())) <= loop_indent and stripped:
                    # In JS/TS, we also check closing brackets/parentheses
                    if not (stripped.startswith("}") or stripped.startswith(")")):
                        in_loop = False
                
                # If we are inside a loop structure and see a DB query
                if in_loop and DB_REGEX.search(stripped):
                    print(f"Potential N+1 Pattern: [ {os.path.relpath(filepath, directory)}:{line_no} ]")
                    print(f"  Line: {stripped}")
                    matches_found += 1
                    
    print(f"\nScan complete. Found {matches_found} potential N+1 database patterns.")

def explain_sqlite_query(db_path, query):
    if not os.path.exists(db_path):
        print(f"SQLite DB file not found: {db_path}")
        sys.exit(1)
        
    print(f"Explaining SQLite query plan for: '{query}' on database '{db_path}'...\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # EXPLAIN QUERY PLAN
        explain_query = f"EXPLAIN QUERY PLAN {query}"
        cursor.execute(explain_query)
        results = cursor.fetchall()
        
        print("Plan Results:")
        print(f"  {'ID':<5} {'PARENT':<8} {'NOTUSED':<8} {'DETAIL'}")
        print("  " + "-" * 60)
        
        has_table_scan = False
        for row in results:
            # row format: (id, parent, notused, detail)
            row_id, parent, notused, detail = row
            print(f"  {row_id:<5} {parent:<8} {notused:<8} {detail}")
            
            # Look for warnings in the plan
            if "SCAN TABLE" in detail:
                has_table_scan = True
                
        print("  " + "-" * 60)
        
        if has_table_scan:
            print("\n[WARNING] 'SCAN TABLE' detected! This indicates a Full Table Scan.")
            print("Suggest adding an INDEX on the columns in the WHERE/JOIN clauses to speed up this query.")
        else:
            print("\n[OPTIMAL] Query uses index lookups. No Full Table Scans found.")
            
        conn.close()
    except Exception as e:
        print(f"Failed to explain query: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)
        
    action = sys.argv[1].lower()
    
    if action == "scan":
        scan_nplusone(sys.argv[2])
    elif action == "explain":
        if len(sys.argv) < 4:
            print("Error: Missing query string.")
            print_help()
            sys.exit(1)
        explain_sqlite_query(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown action: {action}")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
