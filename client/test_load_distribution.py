import asyncio
import aiohttp
from collections import defaultdict
import matplotlib.pyplot as plt

NUM_REQUESTS = 10000
LB_URL = "http://localhost:6000/home?id="

async def fetch(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            data = await response.json()
            server_msg = data.get("container_response", {}).get("message", "")
            server_id = server_msg.split()[-1]  # Extract "Server X"
            return server_id
    except Exception:
        return "error"

async def main():
    counts = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(NUM_REQUESTS):
            url = LB_URL + str(i)
            tasks.append(fetch(session, url))

        responses = await asyncio.gather(*tasks)

        for server_id in responses:
            counts[server_id] += 1

    # Output counts
    print("\nRequest Distribution (10,000 requests):")
    for server, count in counts.items():
        print(f"{server}: {count} requests")

    # Plot bar chart
    plt.bar(counts.keys(), counts.values(), color='steelblue')
    plt.title("Load Distribution Across Servers")
    plt.xlabel("Server ID")
    plt.ylabel("Requests Handled")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("client/load_distribution.png")
    print("\nBar chart saved as client/load_distribution.png")

if __name__ == "__main__":
    asyncio.run(main())
