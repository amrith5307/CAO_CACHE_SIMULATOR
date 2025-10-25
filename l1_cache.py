import random
import matplotlib.pyplot as plt

# -------------------------------
# PARAMETERS
# -------------------------------
CACHE_SIZE = 4
MEMORY_SIZE = 20
L1_TIME = 1
MEMORY_TIME = 10

# -------------------------------
# MEMORY ACCESS SEQUENCES
# -------------------------------
sequential_access = list(range(MEMORY_SIZE)) * 3
random_access = [random.randint(0, MEMORY_SIZE - 1) for _ in range(MEMORY_SIZE * 3)]

# -------------------------------
# FUNCTION TO SIMULATE L1 CACHE
# -------------------------------
def simulate_L1(access_sequence):
    L1_cache = []
    L1_hits = 0
    misses = 0
    total_time = 0

    for address in access_sequence:
        if address in L1_cache:
            L1_hits += 1
            total_time += L1_TIME
            L1_cache.remove(address)
            L1_cache.append(address)
        else:
            misses += 1
            total_time += MEMORY_TIME
            if len(L1_cache) < CACHE_SIZE:
                L1_cache.append(address)
            else:
                L1_cache.pop(0)
                L1_cache.append(address)

    avg_access_time = total_time / len(access_sequence)
    return L1_hits, misses, avg_access_time

# -------------------------------
# SIMULATION
# -------------------------------
seq_hits, seq_misses, seq_avg_time = simulate_L1(sequential_access)
rand_hits, rand_misses, rand_avg_time = simulate_L1(random_access)

# -------------------------------
# PRINT RESULTS
# -------------------------------
print(f"L1 Cache Simulation Results (Cache Size = {CACHE_SIZE})")
print("-"*60)
print("Memory Access Type | Total Accesses | L1 Hits | Misses | Avg Access Time")
print(f"Sequential        | {len(sequential_access):<13} | {seq_hits:<7} | {seq_misses:<6} | {seq_avg_time:.2f}")
print(f"Random            | {len(random_access):<13} | {rand_hits:<7} | {rand_misses:<6} | {rand_avg_time:.2f}")

# -------------------------------
# PROFESSIONAL GRAPHS
# -------------------------------
plt.style.use('ggplot')  # Built-in style

# Graph 1: L1 Hits Comparison
plt.figure(figsize=(8,5))
bars = plt.bar(['Sequential','Random'], [seq_hits, rand_hits], color=['#4CAF50','#F44336'], width=0.5)
plt.title("L1 Cache Hits: Sequential vs Random", fontsize=16, fontweight='bold')
plt.ylabel("Number of Hits", fontsize=13)
plt.xlabel("Memory Access Type", fontsize=13)
plt.ylim(0, max(seq_hits, rand_hits)+2)

# Annotate bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, yval, ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()

# Graph 2: Average Access Time Comparison
plt.figure(figsize=(8,5))
bars = plt.bar(['Sequential','Random'], [seq_avg_time, rand_avg_time], color=['#2196F3','#FF9800'], width=0.5)
plt.title("Average Access Time: Sequential vs Random", fontsize=16, fontweight='bold')
plt.ylabel("Cycles", fontsize=13)
plt.xlabel("Memory Access Type", fontsize=13)
plt.ylim(0, max(seq_avg_time, rand_avg_time)+1)

# Annotate bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval,2), ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()
