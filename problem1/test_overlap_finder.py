
import pytest

from .overlap_finder import find_overlap

def test_overlap_finder():
    assert find_overlap((1, 5),(4, 9)) == True
    assert find_overlap((1, 5), (5, 9)) == True
    assert find_overlap((1, 5), (6, 9)) == False
    assert find_overlap((5, 1), (9, 4)) == True