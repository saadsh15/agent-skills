#!/usr/bin/env python3
import os
import sys
import subprocess
import socket
import json

def get_runtime_version(cmd):
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
        if res.returncode == 0:
            return res.stdout.strip().replace('\n', ' ')
        else:
            return res.stderr.strip().replace('\n', ' ')
    except Exception:
        return "Not installed / not in PATH"

def check_ports(ports_to_check):
    results = {}
    for port in ports_to_check:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            # Try to connect. If it succeeds, something is listening.
            result = s.connect_ex(('127.0.0.1', port))
            if result == 0:
                # Port is open (something is listening)
                results[port] = "LISTENING"
            else:
                results[port] = "CLOSED"
    return results

def scan_env_keys(start_dir):
    env_files = []
    # Search for .env files up to 3 levels deep
    for root, dirs, files in os.walk(start_dir):
        # Limit depth
        depth = root[len(start_dir):].count(os.sep)
        if depth > 3:
            continue
        for file in files:
            if file == '.env' or file.startswith('.env.'):
                env_files.append(os.path.join(root, file))
    
    env_diagnostics = {}
    for filepath in env_files:
        try:
            with open(filepath, 'r') as f:
                keys = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key = line.split('=', 1)[0].strip()
                            keys.append(key)
                env_diagnostics[os.path.relpath(filepath, start_dir)] = keys
        except Exception as e:
            env_diagnostics[os.path.relpath(filepath, start_dir)] = f"Error reading: {str(e)}"
    return env_diagnostics

def get_system_load():
    try:
        if sys.platform.startswith('linux'):
            with open('/proc/loadavg', 'r') as f:
                load = f.read().strip()
            with open('/proc/meminfo', 'r') as f:
                mem = f.read().splitlines()
            mem_total = [line for line in mem if "MemTotal" in line][0].split()[1]
            mem_free = [line for line in mem if "MemAvailable" in line or "MemFree" in line][0].split()[1]
            return {
                "load_avg": load,
                "mem_total_kb": mem_total,
                "mem_free_or_avail_kb": mem_free
            }
    except Exception:
        pass
    return "Unavailable"

def main():
    print("=== Antigravity Debug Helper: Environment Diagnostics ===")
    
    # 1. Runtimes
    runtimes = {
        "Python": [sys.executable, "--version"],
        "Node": ["node", "--version"],
        "npm": ["npm", "--version"],
        "Docker": ["docker", "--version"],
        "Docker Compose": ["docker-compose", "--version"],
        "Git": ["git", "--version"],
        "Go": ["go", "version"],
        "Java": ["java", "-version"]
    }
    
    print("\n--- Runtime Versions ---")
    for name, cmd in runtimes.items():
        version = get_runtime_version(cmd)
        print(f"  {name:15}: {version}")
        
    # 2. Port Check
    common_ports = [80, 443, 3000, 3001, 5000, 5001, 8000, 8080, 8443, 9000, 27017, 5432, 6379, 3306]
    print("\n--- Common Ports Status ---")
    port_status = check_ports(common_ports)
    listening = [str(port) for port, status in port_status.items() if status == "LISTENING"]
    if listening:
        print(f"  Listening on: {', '.join(listening)}")
    else:
        print("  No common development ports are active on 127.0.0.1.")

    # 3. Environment Variables
    print("\n--- Local .env Configurations (Keys Only) ---")
    env_keys = scan_env_keys(os.getcwd())
    if env_keys:
        for file, keys in env_keys.items():
            print(f"  File: {file}")
            if isinstance(keys, list):
                if keys:
                    print(f"    Variables defined: {', '.join(keys)}")
                else:
                    print("    No variables defined (empty file).")
            else:
                print(f"    {keys}")
    else:
        print("  No .env files found in current directory.")

    # 4. System Diagnostics
    print("\n--- System Metrics ---")
    sys_metrics = get_system_load()
    if isinstance(sys_metrics, dict):
        print(f"  Load Avg:  {sys_metrics['load_avg']}")
        print(f"  Total Mem: {int(sys_metrics['mem_total_kb'])/1024:.1f} MB")
        print(f"  Avail Mem: {int(sys_metrics['mem_free_or_avail_kb'])/1024:.1f} MB")
    else:
        print("  System metrics only available on Linux platform.")
        
    print("\n=======================================================")

if __name__ == "__main__":
    main()
