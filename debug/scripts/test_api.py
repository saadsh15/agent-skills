#!/usr/bin/env python3
import sys
import urllib.request
import urllib.error
import time
import json
import ssl

def print_help():
    print("""
Usage: test_api.py <METHOD> <URL> [BODY] [HEADERS_JSON]

Example GET:
  python3 test_api.py GET http://localhost:8000/api/users

Example POST:
  python3 test_api.py POST http://localhost:8000/api/users '{"name":"John"}' '{"Content-Type":"application/json"}'
""")

def main():
    if len(sys.argv) < 3 or sys.argv[1] in ("--help", "-h"):
        print_help()
        sys.exit(0)
        
    method = sys.argv[1].upper()
    url = sys.argv[2]
    body = sys.argv[3] if len(sys.argv) > 3 else None
    headers_str = sys.argv[4] if len(sys.argv) > 4 else None

    # Parse headers
    headers = {}
    if headers_str:
        try:
            headers = json.loads(headers_str)
        except Exception as e:
            print(f"Error parsing headers JSON: {e}")
            sys.exit(1)

    data = None
    if body:
        data = body.encode('utf-8')
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

    # Create request
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    # Ignore SSL verification errors (common in local environments)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print(f"Sending Request: {method} {url}")
    if headers:
        print("Headers:")
        for k, v in headers.items():
            print(f"  {k}: {v}")
    if body:
        print(f"Body: {body[:300] + '...' if len(body) > 300 else body}")

    print("\nConnecting...")
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            latency = (time.time() - start_time) * 1000
            print(f"Status: {response.status} {response.reason}")
            print(f"Latency: {latency:.2f} ms")
            
            print("\nResponse Headers:")
            for k, v in response.getheaders():
                print(f"  {k}: {v}")
                
            response_body = response.read().decode('utf-8')
            print("\nResponse Body:")
            try:
                # Try formatting response if it's JSON
                json_data = json.loads(response_body)
                print(json.dumps(json_data, indent=2))
            except json.JSONDecodeError:
                # Fallback to plain text
                print(response_body)
                
    except urllib.error.HTTPError as e:
        latency = (time.time() - start_time) * 1000
        print(f"HTTP Error: {e.code} {e.reason}")
        print(f"Latency: {latency:.2f} ms")
        print("\nResponse Headers:")
        for k, v in e.headers.items():
            print(f"  {k}: {v}")
        try:
            err_body = e.read().decode('utf-8')
            print("\nResponse Body:")
            try:
                json_data = json.loads(err_body)
                print(json.dumps(json_data, indent=2))
            except json.JSONDecodeError:
                print(err_body)
        except Exception:
            pass
            
    except urllib.error.URLError as e:
        print(f"URL Error (Connection Failed): {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
