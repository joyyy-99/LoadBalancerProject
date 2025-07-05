import requests
import time
from collections import defaultdict
import docker

client = docker.from_env()

# Config
LB_URL = "http://localhost:5000"
REPLICAS = ["S1", "S2", "S3"]

def try_request(max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            res = requests.get(f"{LB_URL}/home", timeout=2)
            if res.ok:
                return res.json()
        except Exception:
            time.sleep(delay)
    return {"status": "failure"}

def main():
    print("[*] Clearing old replicas...")
    try:
        res = requests.post(f"{LB_URL}/clear")
        print(res.json())
    except Exception as e:
        print(f"[!] Failed to clear: {e}")
        return

    time.sleep(2)

    print("\n[*] Adding 3 replicas (S1, S2, S3)...")
    try:
        res = requests.post(f"{LB_URL}/add", json={"hostnames": REPLICAS})
        print(res.json())
    except Exception as e:
        print(f"[!] Failed to add servers: {e}")
        return

    time.sleep(2)

    print("\n[*] Sending 10 initial requests...")
    before_failure = defaultdict(int)

    for _ in range(10):
        response = try_request()
        server = response.get("server")
        if server:
            before_failure[server] += 1
        else:
            print("Failure response:", response)

    print("Requests before failure:", dict(before_failure))

    print("\n[!] Simulating failure: stopping S2...\n")
    try:
        s2_container = client.containers.get("S2")
        print("S2")
        s2_container.stop()
    except Exception as e:
        print(f"[!] Could not stop S2: {e}")
        return

    # Give time for load balancer to detect failure and recover
    time.sleep(5)

    print("[*] Sending 20 more requests after S2 is stopped...")
    after_failure = defaultdict(int)

    for _ in range(20):
        response = try_request()
        server = response.get("server")
        if server:
            after_failure[server] += 1
            if "recovered" in response.get("status", "") or "restarted" in response.get("message", ""):
                print("Recovery response:", response)

        else:
            print("Failure response:", response)

    print("Requests after failure:", dict(after_failure))

    final = defaultdict(int)
    for k in before_failure:
        final[k] += before_failure[k]
    for k in after_failure:
        final[k] += after_failure[k]

    print("\n[✔] Final request distribution:", dict(final))

if __name__ == "__main__":
    main()
