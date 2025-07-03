import bisect
import random

class ConsistentHashRing:
    def __init__(self, num_slots=512, virtual_nodes=9):
        self.num_slots = num_slots
        self.virtual_nodes = virtual_nodes
        self.ring = [] 
        self.slot_to_server = {} 
        self.server_to_slots = {}

    # Hash for request ID
    def hash_request(self, request_id):
        return (request_id**2 + 2 * request_id + 17) % self.num_slots

    # Hash for virtual node of a server
    def hash_virtual_server(self, server_id, virtual_id):
        return (server_id**2 + virtual_id + 2 * virtual_id + 25) % self.num_slots

    # Add a physical server and its K virtual replicas to the ring
    def add_server(self, server_id):
        slots = []
        for j in range(self.virtual_nodes):
            slot = self.hash_virtual_server(server_id, j)
            original = slot
            attempt = 1
            # Quadratic probing to resolve collisions
            while slot in self.slot_to_server:
                slot = (original + attempt ** 2) % self.num_slots
                attempt += 1
            self.slot_to_server[slot] = server_id
            bisect.insort(self.ring, slot)
            slots.append(slot)
        self.server_to_slots[server_id] = slots

    # Remove all virtual nodes for a given server
    def remove_server(self, server_id):
        if server_id not in self.server_to_slots:
            return
        for slot in self.server_to_slots[server_id]:
            self.ring.remove(slot)
            del self.slot_to_server[slot]
        del self.server_to_slots[server_id]

    # Get server for given request ID using clockwise lookup
    def get_server(self, request_id):
        if not self.ring:
            return None
        slot = self.hash_request(request_id)
        idx = bisect.bisect_right(self.ring, slot)
        if idx == len(self.ring):
            idx = 0  # Wrap around the ring
        assigned_slot = self.ring[idx]
        return self.slot_to_server[assigned_slot]

    # View for debugging
    def show_ring(self):
        for slot in self.ring:
            print(f"Slot {slot} -> Server {self.slot_to_server[slot]}")

#Testing
if __name__ == "__main__":
    ring = ConsistentHashRing()

    # Add 3 servers
    ring.add_server(1)
    ring.add_server(2)
    ring.add_server(3)

    ring.show_ring()

    # Simulate request mapping
    for _ in range(10):
        rid = random.randint(100000, 999999)
        server = ring.get_server(rid)
        print(f"Request {rid} → Server {server}")
