import random
import matplotlib.pyplot as plt

# -------------------------------
# PARAMETERS
# -------------------------------
CACHE_SIZE_L1 = 8
CACHE_SIZE_L2 = 16
MEMORY_SIZE = 20
L1_TIME = 1
L2_TIME = 5
MEMORY_TIME = 10

# -------------------------------
# MEMORY ACCESS SEQUENCES
# -------------------------------
sequential_access = list(range(MEMORY_SIZE)) * 2
random_access = [random.randint(0, MEMORY_SIZE - 1) for _ in range(MEMORY_SIZE * 2)]

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
    return hits, misses, avg_time

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

    for addr in access_sequence:
        if addr in L1_cache:
            L1_hits += 1
            total_time += L1_TIME
            L1_cache.remove(addr)
            L1_cache.append(addr)
        elif addr in L2_cache:
            L2_hits += 1
            total_time += L2_TIME
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
    return L1_hits, L2_hits, misses, avg_time

# -------------------------------
# RUN SIMULATION
# -------------------------------
# L1 only
l1_rand_hits, l1_rand_misses, l1_rand_avg = simulate_L1(random_access)
l1_seq_hits, l1_seq_misses, l1_seq_avg = simulate_L1(sequential_access)

# L1 + L2
l1l2_rand_L1, l1l2_rand_L2, l1l2_rand_miss, l1l2_rand_avg = simulate_L1_L2(random_access)
l1l2_seq_L1, l1l2_seq_L2, l1l2_seq_miss, l1l2_seq_avg = simulate_L1_L2(sequential_access)

# -------------------------------
# TERMINAL OUTPUT
# -------------------------------
print("\nL1 Cache Only")
print("-"*40)
print("Type | L1 Hits | Misses | Avg Time")
print(f"Sequential | {l1_seq_hits:<7} | {l1_seq_misses:<7} | {l1_seq_avg:.2f}")
print(f"Random     | {l1_rand_hits:<7} | {l1_rand_misses:<7} | {l1_rand_avg:.2f}")

print("\nL1 + L2 Cache")
print("-"*40)
print("Type | L1 Hits | L2 Hits | Misses | Avg Time")
print(f"Sequential | {l1l2_seq_L1:<7} | {l1l2_seq_L2:<7} | {l1l2_seq_miss:<6} | {l1l2_seq_avg:.2f}")
print(f"Random     | {l1l2_rand_L1:<7} | {l1l2_rand_L2:<7} | {l1l2_rand_miss:<6} | {l1l2_rand_avg:.2f}")

# -------------------------------
# BAR GRAPH: Random Access Hits Comparison
# -------------------------------
plt.style.use('ggplot')
plt.figure(figsize=(6,5))
labels = ['L1-only L1 Hits','L1+L2 L1 Hits','L1+L2 L2 Hits']
values = [l1_rand_hits, l1l2_rand_L1, l1l2_rand_L2]
colors = ['#F44336','#FF7961','#9E9E9E']
bars = plt.bar(labels, values, color=colors, width=0.5)
plt.title("Random Access: L1-only vs L1+L2 Hits", fontsize=16, fontweight='bold')
plt.ylabel("Number of Hits", fontsize=13)
plt.ylim(0, max(values)+2)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, yval, ha='center', va='bottom', fontsize=12)
plt.tight_layout()
plt.show()

# -------------------------------
# PIE CHART: Random Access Hit/Miss (L1+L2)
# -------------------------------
plt.figure(figsize=(6,6))
labels = ['L1 Hits','L2 Hits','Misses']
values = [l1l2_rand_L1, l1l2_rand_L2, l1l2_rand_miss]
colors = ['#F44336','#FF7961','#9E9E9E']
plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title("Random Access: Hit/Miss % (L1 + L2)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# -------------------------------
# AVG ACCESS TIME BAR GRAPH (Sequential + Random)
# -------------------------------
plt.figure(figsize=(6,5))
labels = ['Sequential L1-only','Sequential L1+L2','Random L1-only','Random L1+L2']
avg_times = [l1_seq_avg, l1l2_seq_avg, l1_rand_avg, l1l2_rand_avg]
colors = ['#4CAF50','#81C784','#F44336','#FF7961']
plt.bar(labels, avg_times, color=colors, width=0.5)
plt.title("Average Access Time Comparison", fontsize=16, fontweight='bold')
plt.ylabel("Cycles", fontsize=13)
plt.ylim(0, max(avg_times)+2)
for i, val in enumerate(avg_times):
    plt.text(i, val+0.1, round(val,2), ha='center', fontsize=12)
plt.tight_layout()
plt.show()
