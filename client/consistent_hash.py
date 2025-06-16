class ConsistentHash:
    def __init__(self, total_slots=512, num_virtual=9):
        self.total_slots = total_slots
        self.num_virtual = num_virtual
        self.servers = {}  # {slot: server_name}
        self.virtual_servers = {}  # {server_name: [virtual_slots]}
    
    def hash_request(self, path):
        # H(i) = i + 2i + 17
        hash_val = sum(ord(c) for c in path)
        return (hash_val + 2*hash_val + 17) % self.total_slots
    
    def hash_virtual_server(self, server_name, replica_idx):
        # Φ(i,j) = i + j + 2j + 25
        i = sum(ord(c) for c in server_name)
        j = replica_idx
        return (i + j + 2*j + 25) % self.total_slots
    
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
        # Find the next available server in the ring
        for i in range(self.total_slots):
            current_slot = (slot + i) % self.total_slots
            if current_slot in self.servers:
                return self.servers[current_slot]
        return None