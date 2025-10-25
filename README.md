# L1 + L2 Cache Simulator

## Overview
This project simulates **L1 and L2 CPU caches** to compare the performance of **L1-only cache** vs **L1 + L2 cache**.  
It demonstrates how cache hierarchy affects **hits, misses, and average memory access time** for both **sequential** and **random memory access patterns**.

---

## Features
- Simulates **L1-only cache** and **L1 + L2 cache** with configurable sizes.  
- Implements **LRU (Least Recently Used) cache replacement policy**.  
- Calculates:
  - L1 hits
  - L2 hits
  - Misses
  - Average access time
- Generates **professional graphs** using Matplotlib:
  - Random access hits comparison
  - Average access time comparison (sequential & random)
  - Random access hit/miss pie chart

---

## Tools Used
- **Programming Language:** Python  
- **IDE:** VS Code  
- **Libraries:** Matplotlib, random  

---



## Algorithm and Explanation

This project simulates L1 and L2 CPU caches using **LRU (Least Recently Used) cache replacement policy**. The following steps are used:

1. **Initialize Parameters:**
   - Set **cache sizes** for L1 and L2.
   - Set **access times** for L1, L2, and main memory.
   - Prepare **memory access sequences** (sequential and random).

2. **Simulate Memory Access:**
   For each memory address in the access sequence:
   - **Check L1 cache:**
     - If the address is present (**L1 hit**), add `L1_TIME` cycles.
     - Move the address to the **end of L1 cache** to mark it as most recently used.
   - **If L1 miss, check L2 cache:**
     - If the address is present (**L2 hit**), add `L2_TIME` cycles.
     - Move the address to **L1 cache** (insert using LRU policy) and remove least recently used if needed.
   - **If L2 miss, access main memory:**
     - Add `MEMORY_TIME` cycles.
     - Insert the address into **both L1 and L2 caches** following LRU policy.

3. **Maintain LRU Policy:**
   - When a cache is full, **evict the least recently used block** (the one accessed least recently).

4. **Calculate Metrics:**
   - Count **hits** in L1 and L2.
   - Count **misses** (accessed from main memory).
   - Compute **average access time** as:
     ```
     Avg Access Time = Total Access Time / Total Memory Accesses
     ```

5. **Generate Graphs:**
   - **Bar charts** for L1 & L2 hits.
   - **Average access time comparison** for sequential vs random accesses.
   - **Pie chart** showing hits vs misses for random access.
## Evaluation Metrics

The performance of the cache simulator is evaluated using the following metrics:

- **L1 Hit Rate (%):** Measures the efficiency of L1 cache in satisfying memory requests.  
  `L1 Hit Rate = (Number of L1 Hits / Total Memory Accesses) * 100`

- **L2 Hit Rate (%):** Indicates how often the L2 cache serves requests missed by L1.  
  `L2 Hit Rate = (Number of L2 Hits / Total Memory Accesses) * 100`

- **Miss Rate (%):** Shows the percentage of accesses that go all the way to main memory.  
  `Miss Rate = ((Total Accesses - L1 Hits - L2 Hits) / Total Accesses) * 100`

- **Average Memory Access Time (AMAT):** Represents the average time (in cycles) taken to access memory considering hits and misses.  
  `AMAT = (L1 Hits * L1_TIME + L2 Hits * L2_TIME + Misses * MEMORY_TIME) / Total Accesses`

- **Graphical Representation:** Bar charts and pie charts help **visualize hit/miss distribution** and **access times** for better understanding.


## Results and Findings

1. **L1 Cache Only:**
   - Sequential access generally shows higher efficiency due to **spatial locality**.
   - Random access leads to **more misses** because memory addresses are accessed unpredictably.
   - Small L1 cache size causes frequent eviction in random access.

2. **L1 + L2 Cache:**
   - Adding L2 significantly **reduces average memory access time**, especially for random access.
   - L2 cache acts as a secondary buffer, reducing the number of main memory accesses.
   - Even with small cache sizes, L2 improves performance for workloads with poor spatial locality.

3. **Graph Analysis:**
   - **Bar charts** clearly show the increase in hits when L2 is added.
   - **Pie chart** shows the proportion of hits vs misses, highlighting the reduction in main memory access.
   - Average access time comparison shows **faster overall memory access** with L1 + L2 cache versus L1 alone.

4. **Key Observation:**
   - The hierarchy of caches effectively reduces memory latency.
   - Sequential patterns benefit more from cache due to **predictable memory access**.
   - Random access patterns benefit greatly from multi-level caching.


## Future Work

1. **Add L3 Cache Simulation:**
   - Include a third-level cache to analyze further improvements in access time.

2. **Implement Write Policies:**
   - Add **write-back** and **write-through** policies to simulate real CPU memory operations.

3. **Increase Memory and Cache Sizes:**
   - Simulate larger main memory and caches for more realistic results.

4. **Advanced Access Patterns:**
   - Test with **strided, looping, and real program memory traces**.

5. **GUI/Interactive Simulation:**
   - Build a GUI to dynamically change cache parameters and visualize hits, misses, and graphs in real-time.

6. **Performance Comparison with Real Hardware:**
   - Compare simulator results with actual CPU cache statistics for verification.
