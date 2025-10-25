import random
import matplotlib.pyplot as plt

# -------------------------------
# PARAMETERS
# -------------------------------
CACHE_SIZE_L1 = 4       # L1 cache size
CACHE_SIZE_L2 = 8       # L2 cache size
MEMORY_SIZE = 20        # Total memory addresses
L1_TIME = 1             # L1 access time (cycles)
L2_TIME = 5             # L2 access time (cycles)
MEMORY_TIME = 10        # Main memory access time (cycles)

# -------------------------------
# MEMORY ACCESS SEQUENCES
# -------------------------------
sequential_access = list(range(MEMORY_SIZE))
random_access = [random.randint(0, MEMORY_SIZE - 1) for _ in range(MEMORY_SIZE)]

# -------------------------------
# SIMULATE L1 ONLY
# -------------------------------
def simulate_L1(access_sequence):
    L1_cache = []
    hits = 0
    misses = 0
    total_time = 0

    for addr in access_sequence:
        if addr in L1_cache:
            hits += 1
            total_time += L1_TIME
            # LRU: move to end
            L1_cache.remove(addr)
            L1_cache.append(addr)
        else:
            misses += 1
            total_time += MEMORY_TIME
            if len(L1_cache) < CACHE_SIZE_L1:
                L1_cache.append(addr)
            else:
                L1_cache.pop(0)
                L1_cache.append(addr)

    avg_time = total_time / len(access_sequence)
    hit_ratio = hits / len(access_sequence)
    miss_ratio = misses / len(access_sequence)
    return hits, misses, avg_time, hit_ratio, miss_ratio

# -------------------------------
# SIMULATE L1 + L2
# -------------------------------
def simulate_L1_L2(access_sequence):
    L1_cache = []
    L2_cache = []
    L1_hits = 0
    L2_hits = 0
    misses = 0
    total_time = 0
    access_times_list = []

    for addr in access_sequence:
        if addr in L1_cache:
            L1_hits += 1
            total_time += L1_TIME
            access_times_list.append(L1_TIME)
            L1_cache.remove(addr)
            L1_cache.append(addr)
        elif addr in L2_cache:
            L2_hits += 1
            total_time += L2_TIME
            access_times_list.append(L2_TIME)
            # Move to L1
            if len(L1_cache) < CACHE_SIZE_L1:
                L1_cache.append(addr)
            else:
                L1_cache.pop(0)
                L1_cache.append(addr)
            L2_cache.remove(addr)
            L2_cache.append(addr)
        else:
            misses += 1
            total_time += MEMORY_TIME
            access_times_list.append(MEMORY_TIME)
            # Add to L2
            if len(L2_cache) < CACHE_SIZE_L2:
                L2_cache.append(addr)
            else:
                L2_cache.pop(0)
                L2_cache.append(addr)
            # Add to L1
            if len(L1_cache) < CACHE_SIZE_L1:
                L1_cache.append(addr)
            else:
                L1_cache.pop(0)
                L1_cache.append(addr)

    avg_time = total_time / len(access_sequence)
    hit_ratio_L1 = L1_hits / len(access_sequence)
    hit_ratio_L2 = L2_hits / len(access_sequence)
    miss_ratio = misses / len(access_sequence)
    return L1_hits, L2_hits, misses, avg_time, hit_ratio_L1, hit_ratio_L2, miss_ratio, access_times_list

# -------------------------------
# RUN SIMULATION
# -------------------------------
# L1 Only
seq_L1_hits, seq_L1_misses, seq_L1_avg, seq_L1_hit_ratio, seq_L1_miss_ratio = simulate_L1(sequential_access)
rand_L1_hits, rand_L1_misses, rand_L1_avg, rand_L1_hit_ratio, rand_L1_miss_ratio = simulate_L1(random_access)

# L1 + L2
seq_L1L2_hits, seq_L2_hits, seq_misses, seq_L1L2_avg, seq_hit_ratio_L1, seq_hit_ratio_L2, seq_miss_ratio, seq_access_times = simulate_L1_L2(sequential_access)
rand_L1L2_hits, rand_L2_hits, rand_misses, rand_L1L2_avg, rand_hit_ratio_L1, rand_hit_ratio_L2, rand_miss_ratio, rand_access_times = simulate_L1_L2(random_access)

# -------------------------------
# PRINT RESULTS IN TABLE
# -------------------------------
print("\n" + "-"*25)
print("         L1 Only")
print("-"*25)
print(f"{'Access Type':<12} | {'Hits':<5} | {'Misses':<7} | {'Avg Time':<10} | {'Hit Ratio':<9} | {'Miss Ratio':<10}")
print("-"*70)
print(f"{'Sequential':<12} | {seq_L1_hits:<5} | {seq_L1_misses:<7} | {seq_L1_avg:<10.2f} | {seq_L1_hit_ratio:<9.2f} | {seq_L1_miss_ratio:<10.2f}")
print(f"{'Random':<12} | {rand_L1_hits:<5} | {rand_L1_misses:<7} | {rand_L1_avg:<10.2f} | {rand_L1_hit_ratio:<9.2f} | {rand_L1_miss_ratio:<10.2f}")

print("\n" + "-"*25)
print("        L1 + L2")
print("-"*25)
print(f"{'Access Type':<12} | {'L1 Hits':<7} | {'L2 Hits':<7} | {'Misses':<7} | {'Avg Time':<10} | {'Hit Ratio L1':<12} | {'Hit Ratio L2':<12} | {'Miss Ratio':<10}")
print("-"*100)
print(f"{'Sequential':<12} | {seq_L1L2_hits:<7} | {seq_L2_hits:<7} | {seq_misses:<7} | {seq_L1L2_avg:<10.2f} | {seq_hit_ratio_L1:<12.2f} | {seq_hit_ratio_L2:<12.2f} | {seq_miss_ratio:<10.2f}")
print(f"{'Random':<12} | {rand_L1L2_hits:<7} | {rand_L2_hits:<7} | {rand_misses:<7} | {rand_L1L2_avg:<10.2f} | {rand_hit_ratio_L1:<12.2f} | {rand_hit_ratio_L2:<12.2f} | {rand_miss_ratio:<10.2f}")

# -------------------------------
# PROFESSIONAL BAR GRAPHS
# -------------------------------
# Hits Comparison
hits_labels = ['L1 Seq','L1+L2 Seq','L1 Rand','L1+L2 Rand']
hits_values = [seq_L1_hits, seq_L1L2_hits, rand_L1_hits, rand_L1L2_hits]
colors = ['#2ca02c', '#98df8a', '#d62728', '#ff9896']

plt.figure(figsize=(8,5))
bars = plt.bar(hits_labels, hits_values, color=colors)
plt.ylabel("Hits")
plt.title("Cache Hits Comparison")
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.2, f'{height}', ha='center', va='bottom')
plt.show()

# Average Access Time
aat_values = [seq_L1_avg, seq_L1L2_avg, rand_L1_avg, rand_L1L2_avg]
colors = ['#1f77b4','#aec7e8','#ff7f0e','#ffbb78']

plt.figure(figsize=(8,5))
bars = plt.bar(hits_labels, aat_values, color=colors)
plt.ylabel("Avg Access Time (cycles)")
plt.title("Average Access Time Comparison")
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.2, f'{height:.2f}', ha='center', va='bottom')
plt.show()

# -------------------------------
# LINE GRAPH: Step-by-step access time
# -------------------------------
plt.figure(figsize=(10,5))
plt.plot(range(len(seq_access_times)), seq_access_times, marker='o', label="Sequential Access Time", color='#1f77b4')
plt.plot(range(len(rand_access_times)), rand_access_times, marker='x', label="Random Access Time", color='#ff7f0e')
plt.xlabel("Memory Access #")
plt.ylabel("Access Time (cycles)")
plt.title("Step-by-Step Access Time (L1 + L2)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
