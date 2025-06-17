import requests
from consistent_hash import ConsistentHash
from collections import defaultdict

servers = {
    "server1": "http://localhost:5001/home",
    "server2": "http://localhost:5002/home",
    "server3": "http://localhost:5003/home",
}

ch = ConsistentHash()
for server in servers.keys():
    ch.add_server(server)

distribution = defaultdict(int)

for i in range(1000):
    path = f"/client/{i}"
    assigned_server = ch.get_server(path)
    try:
        res = requests.get(servers[assigned_server])
        if res.status_code == 200:
            distribution[assigned_server] += 1
    except:
        print(f"Failed to connect to {assigned_server}")

# Print distribution
print("\nRequest Distribution:")
for server, count in distribution.items():
    print(f"{server:8}: {count} requests")
