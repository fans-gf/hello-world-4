"""Property-based tests for binary_search, powered by Hypothesis.

These complement the example-based tests in test_binary_search.py: instead of
hand-picked cases, they assert the contract holds for *every* sorted sequence
from a small duplicated-heavy alphabet (which is where binary search bugs
live), with the built-in `list.index` / stdlib `bisect` as oracles.
"""

import unittest
from bisect import bisect_left

from hypothesis import given, settings
from hypothesis import strategies as st

from binary_search import binary_search_leftmost, lower_bound

# Small alphabet + size cap => many sequences with heavy duplication.
sorted_lists = st.lists(st.integers(min_value=0, max_value=9), max_size=60).map(sorted)
small_ints = st.integers(min_value=0, max_value=9)


class TestBinarySearchLeftmostHypothesis(unittest.TestCase):
    @settings(max_examples=500)
    @given(values=sorted_lists, target=small_ints)
    def test_matches_builtin_index_leftmost_semantics(self, values, target):
        expected = values.index(target) if target in values else -1
        self.assertEqual(binary_search_leftmost(values, target), expected)

    @settings(max_examples=500)
    @given(values=sorted_lists, target=small_ints)
    def test_result_index_is_a_true_first_occurrence(self, values, target):
        index = binary_search_leftmost(values, target)
        if index == -1:
            self.assertNotIn(target, values)
        else:
            self.assertTrue(0 <= index < len(values))
            self.assertEqual(values[index], target)
            self.assertTrue(all(v != target for v in values[:index]))


class TestLowerBoundHypothesis(unittest.TestCase):
    @settings(max_examples=500)
    @given(values=sorted_lists, target=small_ints)
    def test_matches_stdlib_bisect_left(self, values, target):
        self.assertEqual(lower_bound(values, target), bisect_left(values, target))

    @settings(max_examples=500)
    @given(values=sorted_lists, target=small_ints)
    def test_equals_number_of_elements_strictly_less_than_target(self, values, target):
        expected = sum(1 for v in values if v < target)
        self.assertEqual(lower_bound(values, target), expected)


if __name__ == "__main__":
    unittest.main()
