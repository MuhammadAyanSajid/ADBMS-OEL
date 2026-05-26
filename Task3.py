import time
import random

class BPlusTreeMockIndex:
    def __init__(self):
        self.keys = []
        self.values = []

    def insert(self, key, value):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        self.keys.insert(idx, key)
        self.values.insert(idx, value)

    def exact_match(self, key):
        low, high = 0, len(self.keys) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.keys[mid] == key:
                return self.values[mid]
            elif self.keys[mid] < key:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def range_query(self, start_key, end_key):
        results = []
        for i in range(len(self.keys)):
            if start_key <= self.keys[i] <= end_key:
                results.append(self.values[i])
            elif self.keys[i] > end_key:
                break
        return results

class HashIndex:
    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        self.table[key] = value

    def exact_match(self, key):
        return self.table.get(key, None)

    def range_query(self, start_key, end_key):

        results = []
        for k, v in self.table.items():
            if start_key <= k <= end_key:
                results.append(v)
        return results

data_size = 50000
test_data = [(random.randint(1, 100000), f"Record_{i}") for i in range(data_size)]

b_tree = BPlusTreeMockIndex()
hash_idx = HashIndex()

for k, v in test_data:
    b_tree.insert(k, v)
    hash_idx.insert(k, v)

target = test_data[len(test_data)//2][0]

t0 = time.perf_counter()
b_tree.exact_match(target)
t1 = time.perf_counter()
b_tree_time = t1 - t0

t0 = time.perf_counter()
hash_idx.exact_match(target)
t1 = time.perf_counter()
hash_time = t1 - t0

print(f"Exact Match Lookup Time:")
print(f" - B+ Tree: {b_tree_time:.8f} seconds")
print(f" - Hash Index: {hash_time:.8f} seconds (Typically faster due to O(1) complexity)")

start, end = 20000, 30000

t0 = time.perf_counter()
b_tree.range_query(start, end)
t1 = time.perf_counter()
b_tree_range_time = t1 - t0

t0 = time.perf_counter()
hash_idx.range_query(start, end)
t1 = time.perf_counter()
hash_range_time = t1 - t0

print(f"\nRange Query ({start} to {end}) Time:")
print(f" - B+ Tree: {b_tree_range_time:.8f} seconds")
print(f" - Hash Index: {hash_range_time:.8f} seconds")