"""Benchmark binary_search_leftmost. Run: python3 bench/benchmark.py

Same methodology across the Python / JavaScript / Clojure repos:
fixed set of 1024 seeded-random targets per scenario (cycled),
20,000 warmup ops, then 5 timed reps of 51,200 ops; report best-of-5 ns/op.
Comparison numbers are machine-specific — re-run locally to reproduce.
"""

import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from binary_search import binary_search_leftmost

REPS = 5
BATCH = 50 * 1024  # 51,200 searches per timed rep


def bench(name, data, targets):
    n = len(targets)
    for i in range(20_000):  # warmup
        binary_search_leftmost(data, targets[i % n])
    best = float("inf")
    for _ in range(REPS):
        start = time.perf_counter_ns()
        for i in range(BATCH):
            binary_search_leftmost(data, targets[i % n])
        best = min(best, (time.perf_counter_ns() - start) / BATCH)
    print(f"{name:<48s} n={len(data):<9d} best={best:9.1f} ns/op  ({1e9 / best:,.0f} ops/s)")


rng = random.Random(42)

full = list(range(1_000_000))
hit_targets = [rng.randrange(1_000_000) for _ in range(1024)]
bench("hit, unique elements", full, hit_targets)

evens = list(range(0, 2_000_000, 2))
miss_targets = [rng.randrange(1_000_000) * 2 + 1 for _ in range(1024)]  # odd -> absent
bench("miss, odd target in even array", evens, miss_targets)

dups = [i // 50 for i in range(1_000_000)]  # 0..19999, 50 copies each
dup_targets = [rng.randrange(20_000) for _ in range(1024)]
bench("hit, leftmost of duplicates", dups, dup_targets)

small = list(range(100))
small_targets = [rng.randrange(100) for _ in range(1024)]
bench("hit, small array", small, small_targets)
