import time

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}
        self.timestamps = {}  

class DistributedSystem:
    def __init__(self, mode="CP"):
        self.mode = mode 
        self.nodes = {1: Node(1), 2: Node(2), 3: Node(3)}
        self.partitioned = False 

    def set_partition(self, state: bool):
        self.partitioned = state
        print(f"\nNetwork Partition State: {'ACTIVE' if state else 'INACTIVE'}")

    def write(self, key, value, coordinator_id=1):
        timestamp = time.time()
        
        accessible_nodes = [1, 2]
        if not self.partitioned:
            accessible_nodes.append(3)

        if self.mode == "CP":
            if self.partitioned:
                print(f"[CP Write Fail] Cannot reach write quorum. Write rejected on {key}={value}")
                return False
            else:
                for nid in accessible_nodes:
                    self.nodes[nid].data[key] = value
                print(f"[CP Write Success] Key '{key}' written to all nodes")
                return True

        elif self.mode == "AP":
            for nid in accessible_nodes:
                self.nodes[nid].data[key] = value
                self.nodes[nid].timestamps[key] = timestamp
            print(f"[AP Write Success] Key '{key}' written to reachable nodes: {accessible_nodes}")
            return True

    def read(self, key, node_id):
        if self.partitioned and node_id == 3:
            print(f"[Network Info] Node 3 is isolated")
            
        val = self.nodes[node_id].data.get(key, None)
        print(f"[Read from Node {node_id}] Key: '{key}' -> Value: {val}")
        return val

    def heal_partition(self):
        if not self.partitioned:
            return
        
        print("\nHealing network partition and reconciling data")
        self.partitioned = False
        
        all_keys = set()
        for node in self.nodes.values():
            all_keys.update(node.data.keys())

        for key in all_keys:
            latest_time = -1
            latest_val = None
            for node in self.nodes.values():
                t = node.timestamps.get(key, -1)
                if t > latest_time:
                    latest_time = t
                    latest_val = node.data.get(key)
            
            for node in self.nodes.values():
                node.data[key] = latest_val
                node.timestamps[key] = latest_time
        print("Data synchronized across all nodes")

print("CP Mode Demo")
sys_cp = DistributedSystem(mode="CP")
sys_cp.write("item_id", "100")
sys_cp.set_partition(True)
sys_cp.write("item_id", "200") 
sys_cp.read("item_id", 3)

print("\nAP Mode Demo ")
sys_ap = DistributedSystem(mode="AP")
sys_ap.write("item_id", "100")
sys_ap.set_partition(True)
sys_ap.write("item_id", "200") 
sys_ap.read("item_id", 3)      
sys_ap.read("item_id", 1)      
sys_ap.heal_partition()        
sys_ap.read("item_id", 3)      