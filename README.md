# hello-world-4

[![Python unit tests](https://github.com/fans-gf/hello-world-4/actions/workflows/test.yml/badge.svg)](https://github.com/fans-gf/hello-world-4/actions/workflows/test.yml)

A simple hello-world repository created with the GitHub CLI (`gh`).

## Usage

```bash
python3 hello_world_4.py
# Hello, world!
```

## Binary search

```python
from binary_search import binary_search_leftmost, lower_bound

binary_search_leftmost([1, 2, 2, 2, 3], 2)  # 1 (leftmost exact match)
binary_search_leftmost([1, 2, 3], 4)        # -1 (absent)
lower_bound([1, 2, 2, 3], 2)                # 1 (insertion point, like bisect_left)
```

Input sequences must be sorted in non-decreasing order; the precondition is
not validated and behavior on unsorted input is undefined.

## Running the tests

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -v
```

With coverage (must stay at 100%, enforced via `.coveragerc`):

```bash
coverage run -m unittest discover -v
coverage report -m
```

Tests include example-based cases (empty/single/duplicate-heavy inputs, large
arrays, string/float/tuple comparisons), an exhaustive check of every sorted
multiset of length ≤ 7 over `{0,1,2,3}`, seeded randomized property tests
against the built-in `list.index`, and Hypothesis property-based tests
(`test_binary_search_hypothesis.py`) checked against the stdlib `bisect_left`.

Tests run on every push and pull request via GitHub Actions (see
[.github/workflows/test.yml](.github/workflows/test.yml)).

## Benchmarks

`python3 bench/benchmark.py` (CPython 3.12, best-of-5 after warmup; 1,024
seeded targets cycled, 51,200 ops per rep). Example measurement on the
author's machine — numbers are machine-specific, re-run to reproduce:

| Scenario | n | ns/op |
|---|---|---|
| hit, unique elements | 1,000,000 | ~1,821 |
| miss, odd target in even array | 1,000,000 | ~1,822 |
| hit, leftmost of duplicates | 1,000,000 | ~1,869 |
| hit, small array | 100 | ~476 |

See [BENCHMARK.md](BENCHMARK.md) for full methodology, machine details, scaling analysis and cross-language comparison.
