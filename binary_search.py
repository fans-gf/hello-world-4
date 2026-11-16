"""Binary search utilities."""

from typing import Sequence, TypeVar

T = TypeVar("T")


def binary_search_leftmost(values: Sequence[T], target: T) -> int:
    """Return the leftmost index of *target* in sorted *values*.

    Performs a binary search over ``values`` (which must be sorted in
    non-decreasing order) and returns the index of the first occurrence of
    ``target``. Returns -1 if ``target`` is not present.

    >>> binary_search_leftmost([1, 2, 2, 2, 3], 2)
    1
    >>> binary_search_leftmost([1, 2, 3], 4)
    -1
    """
    left, right = 0, len(values) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            result = mid
            right = mid - 1  # keep scanning left half for an earlier match
        elif values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
