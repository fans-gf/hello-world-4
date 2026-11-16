"""Binary search utilities.

All functions assume their input sequence is sorted in non-decreasing order.
"""

from typing import Sequence, TypeVar

T = TypeVar("T")


def lower_bound(values: Sequence[T], target: T) -> int:
    """Return the insertion point of *target* in sorted *values*.

    This is the index of the first element that is greater than or equal to
    *target* — equivalently, the position where *target* could be inserted to
    keep the sequence sorted. Runs in O(log n) time and O(1) space.

    >>> lower_bound([1, 2, 2, 2, 3], 2)
    1
    >>> lower_bound([1, 2, 3], 4)
    3
    """
    left, right = 0, len(values)  # invariant: answer is in [left, right]
    while left < right:
        mid = (left + right) // 2
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def binary_search_leftmost(values: Sequence[T], target: T) -> int:
    """Return the leftmost index of *target* in sorted *values*.

    Returns the index of the first occurrence of *target*, or -1 if *target*
    is not present. Runs in O(log n) time and O(1) space.

    >>> binary_search_leftmost([1, 2, 2, 2, 3], 2)
    1
    >>> binary_search_leftmost([1, 2, 3], 4)
    -1
    """
    index = lower_bound(values, target)
    if index < len(values) and values[index] == target:
        return index
    return -1
