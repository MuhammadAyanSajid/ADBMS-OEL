import threading
import time

class LockManager:
    def __init__(self):
        self.locks = {}  
        self.waiting_queue = {}  

    def acquire_lock(self, transaction_id, data_item):
        if data_item not in self.locks:
            self.locks[data_item] = transaction_id
            print(f"[Lock Acquired] Transaction {transaction_id} locked {data_item}")
            return True
        elif self.locks[data_item] == transaction_id:
            return True
        else:
            print(f"[Lock Conflict] Transaction {transaction_id} blocked by Transaction {self.locks[data_item]} on item '{data_item}'")
            return False

    def release_locks_for_txn(self, transaction_id):
        released_items = []
        for item, holder in list(self.locks.items()):
            if holder == transaction_id:
                del self.locks[item]
                released_items.append(item)
        if released_items:
            print(f"[Locks Released] Transaction {transaction_id} released: {released_items}")

lock_mgr = LockManager()

def transaction_1():
    print("\nStarting Transaction 1")
    if lock_mgr.acquire_lock(1, "Account_A"):
        time.sleep(1) 
        print("[T1 Executing] Attempting to lock Account_B")
        if not lock_mgr.acquire_lock(1, "Account_B"):
            print("[Deadlock Detection/T1 Blocked] Waiting for Account_B")
    
    lock_mgr.release_locks_for_txn(1)

def transaction_2():
    print("\nStarting Transaction 2")
    if lock_mgr.acquire_lock(2, "Account_B"):
        time.sleep(1)
        print("[T2 Executing] Attempting to lock Account_A")
        if not lock_mgr.acquire_lock(2, "Account_A"):
            print("[Deadlock Detection/T2 Blocked] Waiting for Account_A")
            
    lock_mgr.release_locks_for_txn(2)

t1 = threading.Thread(target=transaction_1)
t2 = threading.Thread(target=transaction_2)

t1.start()
t2.start()
t1.join()
t2.join()