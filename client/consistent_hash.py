import re

class ConsistentHash:
    def __init__(self, total_slots=512, num_virtual=9):
        self.total_slots = total_slots
        self.num_virtual = num_virtual
        self.servers = {}  # {slot: server_name}
        self.virtual_servers = {}  # {server_name: [virtual_slots]}

    def hash_request(self, request_id):
        """Hash function for requests: H(i) = i^2 + 2i + 17 mod M"""
        if isinstance(request_id, str):
            i = sum(ord(c) for c in request_id)
        else:
            i = int(request_id)
        return (i**2 + 2*i + 17) % self.total_slots

    def hash_virtual_server(self, server_name, replica_idx):
        """Hash function for virtual server: Φ(i,j) = i^2 + j^2 + 2j + 25 mod M"""
        match = re.search(r'\d+', server_name)
        if not match:
            raise ValueError(f"No numeric ID found in server name '{server_name}'")
        i = int(match.group())  # Extract numeric part from server name
        j = replica_idx
        return (i**2 + j**2 + 2*j + 25) % self.total_slots

    def add_server(self, server_name):
        """Adds a physical server with its virtual replicas into the hash ring."""
        virtual_slots = []
        for j in range(self.num_virtual):
            slot = self.hash_virtual_server(server_name, j)
            # Handle collisions using linear probing
            original_slot = slot
            while slot in self.servers:
                slot = (slot + 1) % self.total_slots
                if slot == original_slot:
                    raise Exception("Hash ring is full.")
            self.servers[slot] = server_name
            virtual_slots.append(slot)
        self.virtual_servers[server_name] = virtual_slots

    def remove_server(self, server_name):
        """Removes a physical server and its virtual replicas from the hash ring."""
        for slot in self.virtual_servers.get(server_name, []):
            if slot in self.servers:
                del self.servers[slot]
        if server_name in self.virtual_servers:
            del self.virtual_servers[server_name]

    def get_server(self, request_id):
        """Finds the server responsible for a given request."""
        if not self.servers:
            return None
        slot = self.hash_request(request_id)
        # Look for the next available server clockwise (linear probe in ring)
        for i in range(self.total_slots):
            current_slot = (slot + i) % self.total_slots
            if current_slot in self.servers:
                return self.servers[current_slot]
        return None


from collections import Counter

if __name__ == "__main__":
    ch = ConsistentHash(total_slots=512, num_virtual=9)

    # Add 3 servers
    ch.add_server("Server 1")
    ch.add_server("Server 2")
    ch.add_server("Server 3")

    # Count how many requests each server handles
    request_counts = Counter()

    for i in range(1000):
        server = ch.get_server(i)
        request_counts[server] += 1

    print("Request distribution across servers:")
    for server, count in request_counts.items():
        print(f"{server}: {count} requests")

    # Optional: Visualize first few slots in the hash ring
    print("\nSample of hash ring slots:")
    for slot in sorted(ch.servers.keys())[:10]:
        print(f"Slot {slot}: {ch.servers[slot]}")
