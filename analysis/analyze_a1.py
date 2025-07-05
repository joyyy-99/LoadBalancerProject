import asyncio
import matplotlib
matplotlib.use("TkAgg")
import aiohttp
import matplotlib.pyplot as plt
from collections import Counter

URL = "http://localhost:5000/home"  # load balancer endpoint
NUM_REQUESTS = 10000                # number of requests

counter = Counter()

async def fetch(session):
    try:
        async with session.get(URL) as response:
            data = await response.json()
            server = data.get("server")
            if server:
                counter[server] += 1
    except Exception as e:
        print(f"Error: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session) for _ in range(NUM_REQUESTS)]
        await asyncio.gather(*tasks)

    print("\n--- Request Counts ---")
    for server, count in counter.items():
        print(f"{server}: {count}")

    # Plot the bar chart
    plt.bar(counter.keys(), counter.values(), color='skyblue')
    plt.title(f"Request Distribution among 3 Servers (N=3, {NUM_REQUESTS} requests)")
    plt.xlabel("Server ID")
    plt.ylabel("Number of Requests Handled")
    plt.savefig("a1_results.png")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    asyncio.run(main())
