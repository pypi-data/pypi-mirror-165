# coding: utf-8
import numpy as np

from daxs.utils import arrays_intersect


def test_arrays_intersect():
    a = np.array([1, 2])
    b = np.array([2, 3])
    assert arrays_intersect(a, b)

    a = np.array([1, 2])
    b = np.array([-1, 1])
    assert arrays_intersect(a, b)

    a = np.array([0, 0])
    b = np.array([0, 1])
    assert arrays_intersect(a, b)

    a = np.array([1, 2])
    b = np.array([3, 1])
    assert arrays_intersect(a, b)

    a = np.array([1, 2])
    b = np.array([-1, 0])
    assert not arrays_intersect(a, b)

    a = np.array([1, 2])
    b = np.array([3, 4])
    assert not arrays_intersect(a, b)
