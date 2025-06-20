import bisect

class ConsistentHashRing:
    def __init__(self, num_slots=512, virtual_servers=9):
        self.num_slots = num_slots
        self.virtual_servers = virtual_servers
        self.ring = {}  # slot → server_id
        self.sorted_slots = []  # sorted list of slot positions
        self.servers = set()

    def _hash_request(self, request_id):
        return (request_id + 2 * request_id ** 2 + 17) % self.num_slots

    def _hash_virtual(self, server_id, v_id):
        return (server_id ** 3 + v_id ** 2 + 2 * v_id + 25) % self.num_slots

    def add_server(self, server_id):
        if server_id in self.servers:
            return
        self.servers.add(server_id)
        for v_id in range(self.virtual_servers):
            slot = self._hash_virtual(server_id, v_id)
            while slot in self.ring:
                slot = (slot + 1) % self.num_slots  # linear probing
            self.ring[slot] = server_id
            bisect.insort(self.sorted_slots, slot)

    def remove_server(self, server_id):
        self.servers.discard(server_id)
        to_remove = [slot for slot, sid in self.ring.items() if sid == server_id]
        for slot in to_remove:
            del self.ring[slot]
            self.sorted_slots.remove(slot)

    def get_server(self, request_id):
        slot = self._hash_request(request_id)
        idx = bisect.bisect_right(self.sorted_slots, slot)
        if idx == len(self.sorted_slots):
            idx = 0
        return self.ring[self.sorted_slots[idx]]

    def get_ring_state(self):
        return {slot: self.ring[slot] for slot in self.sorted_slots}
        
if __name__ == "__main__":
    import random
    ring = ConsistentHashRing()
    for sid in range(3):
        ring.add_server(sid)

    print("Hash ring state:")
    print(ring.get_ring_state())

    print("\nRouting diverse requests:")
    for _ in range(10):
        rid = random.randint(100000, 999999)
        server = ring.get_server(rid)
        print(f"Request {rid} → Server {server}")

