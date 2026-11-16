# Benchmarks: binary-search-leftmost

Recorded benchmark results and methodology. Numbers are **machine-specific** —
re-run locally; do not quote without your own measurement.

Run the benchmark with `python3 bench/benchmark.py`.

## Machine

- Linux 7.0.0-42-generic x86_64
- Python 3.12.3 (CPython), Node v24.18.1, Clojure CLI 1.12.4.1618 on OpenJDK Temurin 25.0.2
- Measured on 2026-11-16; idle machine, single run per repo

## Methodology

Identical benchmark protocol in all three repos via `bench/benchmark.*`:

- Fixed set of **1,024 seeded-random targets per scenario**, cycled; deterministic RNGs
  (Python `random.Random(42)`, JS `mulberry32(42)`, Clojure `java.util.Random(42)`) —
  same distributions, not identical target sequences.
- **Warmup**: 20,000 ops (Python, JS) / 50,000 ops (Clojure) before timing.
- **Timing**: 5 timed reps x 51,200 ops; report **best-of-5 ns/op** (min) and ops/s.
- **Scenarios**:
  1. `hit, unique elements` — data `0..999,999`, target uniform in range
  2. `miss, odd target in even array` — even-only data `0,2,...,1,999,998`, odd (absent) target
  3. `hit, leftmost of duplicates` — value `i//50` (each value x50 copies), target uniform in `0..19,999`
  4. `hit, small array` — data `0..99` (overhead-dominated)
- Steady state is allocation-free in all three; single-threaded.

## This repo (Python, CPython 3.12.3)

| Scenario | n | ns/op | ops/s |
|---|---|---|---|
| hit, unique elements | 1,000,000 | 1,821 | ~549,131 |
| miss, odd target in even array | 1,000,000 | 1,822 | ~548,854 |
| hit, leftmost of duplicates | 1,000,000 | 1,869 | ~535,077 |
| hit, small array | 100 | 476 | ~2,100,853 |

Also measured: Python stdlib `bisect.bisect_left` as a C reference — ~500 ns/op at n = 1,000,000 (~3.8x faster than the hand-rolled loop).

## Cross-language results (same machine, best-of-5 ns/op)

| Scenario | n | Python | JavaScript | Clojure |
|---|---|---|---|---|
| hit, unique elements | 1,000,000 | 1,821 | **255** | 573 |
| miss, odd target in even array | 1,000,000 | 1,822 | **243** | 591 |
| hit, leftmost of duplicates | 1,000,000 | 1,869 | **246** | 687 |
| hit, small array | 100 | 476 | **60** | 102 |

Reference point: Python stdlib `bisect.bisect_left` (the C implementation of the same
algorithm) measured at ~500 ns/op at n = 1,000,000 — ~3.8x faster than the hand-rolled
Python loop, why production Python uses `bisect`.

## Scaling across n (ns/op, separate sweep, best of 4 reps)

| log2 n | Python loop | Python `bisect` | JavaScript | Clojure |
|---|---|---|---|---|
| 7 (128) | 505 | 174 | 65 | 92 |
| 10 (1,024) | 953 | 224 | 121 | 133 |
| 13 (8,192) | 1,200 | 268 | 149 | 229 |
| 16 (65,536) | 1,499 | 350 | 206 | 381 |
| 17 (131,072) | 1,589 | 383 | 252 | 417 |
| 19 (524,288) | 1,802 | 465 | 267 | 527 |
| 20 (1,048,576) | 1,888 | 500 | 284 | 574 |

Approximate cost per binary-search tree level (large sizes): **JS ~17 ns, Clojure
~37 ns, Python `bisect` ~30–40 ns, Python loop ~106 ns.** Fixed entry overhead
(n=128): JS ~65 ns, Clojure ~92 ns, Python ~505 ns.

## Analysis

Same algorithm, same O(log n) (~20 tree levels at n = 1M). The ~7x throughput gap
(Python -> JS) is **constant-factor engineering, not algorithmic**:

- **Python loop**: per probe, pointer dereference -> PyObject header -> type switch ->
  compare; plus bytecode dispatch. Heap objects for ints >256 -> two dependent loads
  per element per compare. Use `bisect` in real code (3.8x faster, measured).
- **JavaScript**: TurboFan inlines the hot loop; packed SMI array (8B/elem, dense);
  integer compare and loop arithmetic inlined; no allocation. Best cache behavior of
  the three.
- **Clojure**: each probe walks the `IPersistentVector` 32-way trie (4 levels at
  1M) via interface dispatch, with boxed args at `compare`. A `^IPersistentVector` +
  primitive-`long` hint experiment gained only 3–5% and would narrow the API
  (no seqs), so it was **not** adopted.

**Leftmost-duplicates anomaly**: Clojure measured ~687 ns vs ~573 ns for unique hits
(reproducible, ~19% slower); Python (+2.6%) and JS (-3%) were flat/noise. Same probe
count, code path, and data size — not the algorithm. Hypothesized branch-predictor
behavior on heavy-duplicate data; unconfirmed, worth a JMH run if it matters.

**Variance** across whole-benchmark runs: Python +/-1.5%, JS +/-5–7%, Clojure +/-3–10%
(JIT/GC dependent). Duplicate-case numbers are consistent enough to trust as a signal;
small-n numbers do not carry signal beyond "Python has large fixed overhead".

## Caveats

- Micro-benchmark: single-threaded, no CPU pinning/isolation, turbo boost possible,
  best-of-5 biases toward lucky runs.
- Machine-specific; re-run on target hardware before quoting numbers.
- RNG seeds differ across languages (same distributions, different target sequences).
- Uniform-random hit workload; absent probes behave statistically like hits here.
- JVM in particular wants forking + JMH for publication-grade numbers (not done here).
- These figures describe **runtime characteristics of each language's execution model**,
  not implementation quality — same algorithm, same asymptotic complexity.
