import random
import unittest
from bisect import bisect_left
from itertools import combinations_with_replacement

from binary_search import binary_search_leftmost, lower_bound


class TestBinarySearchLeftmost(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(binary_search_leftmost([], 1), -1)

    def test_single_element_found(self):
        self.assertEqual(binary_search_leftmost([7], 7), 0)

    def test_single_element_not_found(self):
        self.assertEqual(binary_search_leftmost([7], 8), -1)

    def test_exact_match_unique(self):
        self.assertEqual(binary_search_leftmost([1, 3, 5, 7, 9], 5), 2)
        self.assertEqual(binary_search_leftmost([1, 3, 5, 7, 9], 1), 0)
        self.assertEqual(binary_search_leftmost([1, 3, 5, 7, 9], 9), 4)

    def test_not_found_smaller_than_all(self):
        self.assertEqual(binary_search_leftmost([2, 4, 6], 1), -1)

    def test_not_found_larger_than_all(self):
        self.assertEqual(binary_search_leftmost([2, 4, 6], 7), -1)

    def test_not_found_between_elements(self):
        self.assertEqual(binary_search_leftmost([2, 4, 6], 5), -1)

    def test_leftmost_of_duplicates(self):
        self.assertEqual(binary_search_leftmost([1, 2, 2, 2, 3], 2), 1)
        self.assertEqual(binary_search_leftmost([2, 2, 2, 2], 2), 0)
        self.assertEqual(binary_search_leftmost([1, 2, 3, 3, 4], 3), 2)

    def test_duplicates_at_end(self):
        self.assertEqual(binary_search_leftmost([1, 2, 3, 3], 3), 2)

    def test_duplicates_at_start(self):
        self.assertEqual(binary_search_leftmost([3, 3, 4, 5], 3), 0)

    def test_all_same_elements(self):
        self.assertEqual(binary_search_leftmost([5, 5, 5, 5, 5], 5), 0)

    def test_even_length_list(self):
        self.assertEqual(binary_search_leftmost([1, 2, 2, 3, 4, 5], 2), 1)
        self.assertEqual(binary_search_leftmost([1, 2, 2, 3, 4, 5], 4), 4)

    def test_strings(self):
        self.assertEqual(binary_search_leftmost(["a", "b", "b", "c"], "b"), 1)

    def test_floats(self):
        self.assertEqual(binary_search_leftmost([0.5, 1.5, 1.5, 2.5], 1.5), 1)

    def test_negative_numbers(self):
        self.assertEqual(binary_search_leftmost([-5, -3, -3, -1, 0], -3), 1)

    def test_zero_and_boundary_values(self):
        self.assertEqual(binary_search_leftmost([0, 0, 1], 0), 0)
        self.assertEqual(binary_search_leftmost([-1, 0, 1], 0), 1)

    def test_large_list_with_duplicates(self):
        values = [i // 100 for i in range(100_000)]  # 0..999, 100 copies each
        self.assertEqual(binary_search_leftmost(values, 0), 0)
        self.assertEqual(binary_search_leftmost(values, 500), 50_000)
        self.assertEqual(binary_search_leftmost(values, 999), 99_900)
        self.assertEqual(binary_search_leftmost(values, 1000), -1)

    def test_large_list_even_numbers_only(self):
        values = list(range(0, 20_000, 2))  # 0, 2, ..., 19998
        self.assertEqual(binary_search_leftmost(values, 0), 0)
        self.assertEqual(binary_search_leftmost(values, 1234), 617)
        self.assertEqual(binary_search_leftmost(values, 1235), -1)  # odd, absent
        self.assertEqual(binary_search_leftmost(values, 19_998), 9_999)
        self.assertEqual(binary_search_leftmost(values, 20_000), -1)

    def test_duplicates_everywhere(self):
        values = [1] * 50 + [2] * 50 + [3] * 50
        self.assertEqual(binary_search_leftmost(values, 1), 0)
        self.assertEqual(binary_search_leftmost(values, 2), 50)
        self.assertEqual(binary_search_leftmost(values, 3), 100)
        self.assertEqual(binary_search_leftmost(values, 4), -1)
        self.assertEqual(binary_search_leftmost(values, 0), -1)

    def test_every_element_found_at_its_first_occurrence(self):
        values = [1, 1, 2, 3, 3, 3, 4, 5, 5, 6]
        for i, v in enumerate(values):
            if i == 0 or values[i - 1] != v:  # first occurrence of v
                self.assertEqual(binary_search_leftmost(values, v), i)

    def test_tuple_input(self):
        self.assertEqual(binary_search_leftmost((1, 2, 2, 3), 2), 1)

    def test_list_of_tuples(self):
        values = [(1, "a"), (2, "b"), (2, "c"), (3, "d")]
        self.assertEqual(binary_search_leftmost(values, (2, "b")), 1)
        self.assertEqual(binary_search_leftmost(values, (2, "a")), -1)

    def test_returns_int_index(self):
        self.assertIsInstance(binary_search_leftmost([1, 2, 2, 3], 2), int)

    def test_matches_builtin_index_on_random_lists(self):
        rng = random.Random(42)
        for _ in range(1000):
            values = sorted(rng.randrange(0, 10) for _ in range(rng.randrange(0, 60)))
            target = rng.randrange(0, 10)
            expected = values.index(target) if target in values else -1
            self.assertEqual(binary_search_leftmost(values, target), expected)


class TestLowerBound(unittest.TestCase):
    def test_empty_sequence(self):
        self.assertEqual(lower_bound([], 1), 0)

    def test_insert_at_front(self):
        self.assertEqual(lower_bound([5, 6, 7], 1), 0)
        self.assertEqual(lower_bound([5, 6, 7], 5), 0)

    def test_insert_at_end(self):
        self.assertEqual(lower_bound([1, 2, 3], 4), 3)
        self.assertEqual(lower_bound([1, 2, 3], 3), 2)

    def test_insert_between(self):
        self.assertEqual(lower_bound([1, 3, 5], 4), 2)
        self.assertEqual(lower_bound([1, 3, 5], 3), 1)

    def test_duplicates_return_first_position(self):
        self.assertEqual(lower_bound([1, 2, 2, 2, 3], 2), 1)
        self.assertEqual(lower_bound([2, 2, 2], 2), 0)
        self.assertEqual(lower_bound([1, 1, 1], 2), 3)

    def test_all_equal_elements(self):
        self.assertEqual(lower_bound([4, 4, 4, 4], 4), 0)
        self.assertEqual(lower_bound([4, 4, 4, 4], 3), 0)
        self.assertEqual(lower_bound([4, 4, 4, 4], 5), 4)

    def test_negative_numbers(self):
        self.assertEqual(lower_bound([-5, -3, -1], -4), 1)
        self.assertEqual(lower_bound([-5, -3, -1], -5), 0)

    def test_tuple_input(self):
        self.assertEqual(lower_bound((1, 2, 2, 3), 2), 1)

    def test_matches_stdlib_bisect_left_on_random_lists(self):
        rng = random.Random(1234)
        for _ in range(1000):
            values = sorted(rng.randrange(0, 20) for _ in range(rng.randrange(0, 80)))
            target = rng.randrange(0, 20)
            self.assertEqual(lower_bound(values, target), bisect_left(values, target))


class TestExhaustiveSmallInputs(unittest.TestCase):
    def test_all_sorted_multisets_up_to_length_7(self):
        alphabet = (0, 1, 2, 3)
        targets = [0, 1, 2, 3, 4]  # 4 is always absent
        for length in range(0, 8):
            for combo in combinations_with_replacement(alphabet, length):
                values = list(combo)
                for target in targets:
                    expected = values.index(target) if target in values else -1
                    self.assertEqual(
                        binary_search_leftmost(values, target),
                        expected,
                        msg=f"values={values} target={target}",
                    )


if __name__ == "__main__":
    unittest.main()
