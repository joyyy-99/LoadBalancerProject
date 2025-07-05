# analyze_a2.py
import aiohttp
import asyncio
import matplotlib.pyplot as plt
import time

LOAD_BALANCER_URL = "http://localhost:5000"

async def send_requests(num_requests):
    counts = {}
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(f"{LOAD_BALANCER_URL}/home") for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)
        for r in responses:
            try:
                data = await r.json()
                server = data.get("server", "unknown")
                counts[server] = counts.get(server, 0) + 1
            except:
                pass
    return counts

async def set_replicas(n):
    hostnames = [f"S{i}" for i in range(1, n + 1)]
    async with aiohttp.ClientSession() as session:
        # Remove existing replicas (optional, clean slate)
        await session.post(f"{LOAD_BALANCER_URL}/clear")  # Make sure this endpoint exists in your backend
        await session.post(f"{LOAD_BALANCER_URL}/add", json={"n": n, "hostnames": hostnames})
        await asyncio.sleep(5)  # Wait for containers to spin up

async def run_experiment():
    N_values = list(range(2, 7))
    avg_loads = []

    for N in N_values:
        print(f"\nSetting replicas to {N}")
        await set_replicas(N)

        print(f"Sending 10,000 requests to N = {N}")
        counts = await send_requests(10000)

        total = sum(counts.values())
        avg = total / N if N else 0
        avg_loads.append(avg)

        print(f"Counts for N={N}: {counts}")
        print(f"Average load per server: {avg:.2f}")

    return N_values, avg_loads

if __name__ == "__main__":
    # Fix deprecation warning
    import sys
    if sys.version_info >= (3, 10):
        N_values, avg_loads = asyncio.run(run_experiment())
    else:
        loop = asyncio.get_event_loop()
        N_values, avg_loads = loop.run_until_complete(run_experiment())

    plt.plot(N_values, avg_loads, marker='o', color='blue')
    plt.title("Scalability Test: Avg Load vs N")
    plt.xlabel("Number of Replicas (N)")
    plt.ylabel("Avg Requests per Server")
    plt.grid(True)
    plt.savefig("a2_scalability.png")
    plt.show()
