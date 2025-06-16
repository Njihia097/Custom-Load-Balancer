# consistent_hash.py
import hashlib

class ConsistentHash:
    def __init__(self, total_slots=512, num_virtual=100):
        self.total_slots = total_slots
        self.num_virtual = num_virtual
        self.servers = {}  # {slot: server_name}
        self.virtual_servers = {}  # {server_name: [virtual_slots]}

    def _hash(self, value):
        """Consistent hash function using SHA-256"""
        h = hashlib.sha256(value.encode()).hexdigest()
        return int(h, 16)

    def hash_request(self, path):
        return self._hash(path) % self.total_slots

    def hash_virtual_server(self, server_name, replica_idx):
        return self._hash(f"{server_name}#{replica_idx}") % self.total_slots

    def add_server(self, server_name):
        virtual_slots = []
        for j in range(self.num_virtual):
            slot = self.hash_virtual_server(server_name, j)
            # Handle collisions with linear probing
            while slot in self.servers:
                slot = (slot + 1) % self.total_slots
            self.servers[slot] = server_name
            virtual_slots.append(slot)
        self.virtual_servers[server_name] = virtual_slots

    def remove_server(self, server_name):
        for slot in self.virtual_servers.get(server_name, []):
            if slot in self.servers:
                del self.servers[slot]
        if server_name in self.virtual_servers:
            del self.virtual_servers[server_name]

    def get_server(self, path):
        if not self.servers:
            return None
        slot = self.hash_request(path)
        for i in range(self.total_slots):
            current_slot = (slot + i) % self.total_slots
            if current_slot in self.servers:
                return self.servers[current_slot]
        return None
