class ConsistentHash:
    def __init__(self, num_slots=512, replicas=9):
        self.ring = {}           # { hash_value: server_id }
        self.sorted_keys = []    # sorted list of all hash keys
        self.num_slots = num_slots
        self.replicas = replicas

    def _request_hash(self, i):
       
        return (3 * i + 17) % self.num_slots

    def _virtual_hash(self, sid, j):
        
        return (sid + 3 * j + 25) % self.num_slots

    def add_server(self, server_id):
       
        sid = int(server_id.replace("server", ""))
        for j in range(self.replicas):
            h = self._virtual_hash(sid, j)
            self.ring[h] = server_id
            self.sorted_keys.append(h)
        self.sorted_keys.sort()

    def remove_server(self, server_id):
        
        to_remove = [h for h, v in self.ring.items() if v == server_id]
        for h in to_remove:
            del self.ring[h]
            self.sorted_keys.remove(h)

    def get_server(self, client_id):
       
        h = self._request_hash(client_id)
        for key in self.sorted_keys:
            if h <= key:
                return self.ring[key]
        return self.ring[self.sorted_keys[0]]  # wrap around
