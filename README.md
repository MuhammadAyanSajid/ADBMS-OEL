
# Advanced Database Management Systems (ADBMS) Final Project

This repository contains the complete implementation suite and database scripts developed for the Advanced Database Management Systems (ADBMS) course at the University of Engineering and Technology, Lahore. The project is structured as a single flat directory containing six independent technical tasks spanning distributed systems, high availability, database indexing, query optimization, concurrency control, and analytical mining.

---

## Repository Files & Descriptions

### `Task1.py` — CAP Theorem Simulation
A Python implementation simulating distributed network partitioning across three virtualized nodes:
* **CP Mode:** Verifies majority quorum checks, blocking write updates during partition to protect data consistency.
* **AP Mode:** Permits local write commits on active nodes during a partition, with asynchronous conflict resolution via a Last-Write-Wins (LWW) timestamp engine upon network healing.

### `Task2_Setup.txt` — MongoDB Replica Set Configuration
Detailed commands and connection parameters used to deploy a local high availability MongoDB 8.2 replica set across customized ports (`27018`, `27019`, and `27020`) to bypass default system service conflicts. Includes:
* Replica set initialization via `rs.initiate()`.
* Secondary read preference routing.
* Primary node termination and automated consensus-based failover election.

### `Task3.py` — Indexing Performance Profiling
Algorithmic benchmarking of B+ Tree and Hash-based index models on a randomized dataset of 50,000 records:
* Measures point lookup execution times, demonstrating the constant-time $O(1)$ efficiency of the Hash index versus $O(\log N)$ tree binary search.
* Measures range query execution times, showing how the sorted leaf nodes of the B+ Tree outperform hash tables.

### `Task4.sql` — SQL Server Query Optimization
T-SQL script demonstrating the optimization of a complex correlated query in Microsoft SQL Server:
* Restructures nested correlated subqueries with nested-loop joins into set-based `inner join` and `group by` aggregates.
* Deploys targeted non-clustered indexes on foreign keys, reducing CPU computation time by 2,127x (from 165,953 ms to 78 ms) and memory page reads by 1,993x (from 1.26M to 635 reads).

### `Task5.py` — Concurrency Control & Deadlocks
A Python lock manager simulating concurrent transaction blocks under a Two-Phase Locking (2PL) protocol:
* Monitors exclusive lock allocations on shared accounts.
* Detects cyclic transaction dependencies by evaluating a Waits-For Graph (WFG) cycle.
* Implements automated deadlock resolution via transaction rollback.

### `Task6_Schema.sql` — Dimensional Data Warehouse
A T-SQL script that deploys a de-normalized Star Schema warehouse on SQL Server. It creates three dimension tables (`dim_customer`, `dim_product`, `dim_time`) and a central fact table (`fact_sales`) loaded with test transaction data.

### `Task6.py` — Database-Connected Data Mining
A database-connected Python ETL script that queries the Star Schema in SQL Server using `pyodbc`:
* Joins dimension and fact tables to extract transactional baskets and customer profiles.
* Applies the Apriori algorithm (`mlxtend`) to extract market basket association rules (e.g., `{Leather Wallet} -> {Charging Cable}` with 1.5x lift).
* Trains a Decision Tree classifier (`scikit-learn`) to predict premium plan purchase segments.

---

## Technical Prerequisites

### 1. Database Servers
* **Microsoft SQL Server** (with SQL Server Management Studio)
* **MongoDB Server 8.2** (with MongoDB Shell `mongosh`)

### 2. Python Environment
Install the required packages using pip:
```bash
pip install pandas mlxtend scikit-learn pyodbc
```

---

## How to Execute the Tasks

* **Task 1, 3, 5:** Run the individual Python scripts:
  ```bash
  python Task1.py
  python Task3.py
  python Task5.py
  ```
* **Task 2:** Refer to the instructions inside `Task2_Setup.txt` to spin up your three `mongod` nodes and initiate the replica set.
* **Task 4:** Open SSMS, open `Task4.sql`, and execute the statements. Enable "Include Actual Execution Plan" to observe physical operator changes.
* **Task 6:** 
  1. Open SSMS and execute `Task6_Schema.sql` to build and populate the database.
  2. Run the analytical mining script:
     ```bash
     python Task6.py
     ```

---

## Authors
* [**Muhammad Ayan Sajid**](https://github.com/MuhammadAyanSajid)
* [**Muhammad Bilal**](https://github.com/Bilal-013) 
* [**Shareen Asim**](https://linkedin.com/in/shareen-asim-9987a33a8)
* [**Muhammad Husnain**](https://github.com/nexHus) 
