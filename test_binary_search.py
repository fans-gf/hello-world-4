import random
import unittest

from binary_search import binary_search_leftmost


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


    def test_matches_builtin_index_on_random_lists(self):
        rng = random.Random(42)
        for _ in range(1000):
            values = sorted(rng.randrange(0, 10) for _ in range(rng.randrange(0, 60)))
            target = rng.randrange(0, 10)
            expected = values.index(target) if target in values else -1
            self.assertEqual(binary_search_leftmost(values, target), expected)


if __name__ == "__main__":
    unittest.main()
