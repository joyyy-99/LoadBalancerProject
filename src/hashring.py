import math

class ConsistentHashRing:
    def __init__(self, num_slots=512, virtual_nodes=9):
        self.num_slots = num_slots
        self.virtual_nodes = virtual_nodes  # K = 9
        self.ring = [None] * self.num_slots  # 512 slots initialized to None
        self.servers = []
        self.server_to_slots = {}  # Mapping of server to its virtual slot indices

    def clear(self):
        self.ring = [None] * self.num_slots
        self.servers = []
        self.server_to_slots = {}

    def _hash_virtual(self, server_id, replica_idx):
        """ Φ(i,j) = (i + j + 2^j + 25) % 512 """
        try:
            i = int(server_id.strip("S"))  # e.g., S1 → 1
        except:
            i = hash(server_id) % 100
        h = (i + replica_idx + pow(2, replica_idx) + 25) % self.num_slots
        return h

    def _hash_request(self, request_id):
        """ H(i) = (i + 2^i + 17) % 512 """
        h = (request_id + pow(2, request_id) + 17) % self.num_slots
        return h

    def add_server(self, server_id):
        if server_id in self.servers:
            return

        self.servers.append(server_id)
        self.server_to_slots[server_id] = []

        for j in range(self.virtual_nodes):
            slot = self._hash_virtual(server_id, j)
            initial_slot = slot
            attempts = 0

            # Resolve collision with linear probing
            while self.ring[slot] is not None:
                slot = (slot + 1) % self.num_slots
                attempts += 1
                if attempts >= self.num_slots:
                    raise Exception("Ring is full. Cannot add more virtual nodes.")

            self.ring[slot] = server_id
            self.server_to_slots[server_id].append(slot)

    def remove_server(self, server_id):
        if server_id not in self.servers:
            return

        self.servers.remove(server_id)
        for slot in self.server_to_slots.get(server_id, []):
            self.ring[slot] = None
        del self.server_to_slots[server_id]

    def get_server(self, request_id):
        if not self.servers:
            return None

        slot = self._hash_request(request_id)
        initial = slot
        attempts = 0

        # Clockwise probing to find next available server
        while self.ring[slot] is None:
            slot = (slot + 1) % self.num_slots
            attempts += 1
            if attempts >= self.num_slots:
                return None  # no servers available

        return self.ring[slot]

    def describe(self):
        return {
            "N": len(self.servers),
            "replicas": self.servers,
            "slots": {srv: self.server_to_slots[srv] for srv in self.server_to_slots}
        }
