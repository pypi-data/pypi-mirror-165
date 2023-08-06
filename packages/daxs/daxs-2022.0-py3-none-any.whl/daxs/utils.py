# coding: utf-8
"""Module for utilities."""

import logging

import numpy as np

logger = logging.getLogger(__name__)


def arrays_intersect(a, b):
    """Returns True if a intersects with b.

    Parameters
    ----------
    a, b : numpy.array
        The arrays to compare.

    Returns
    -------
    : bool
    """
    # The first element of each array is smaller than the last.
    if a[0] < a[-1] and b[0] < b[-1]:
        if (b[-1] < a[0]) or (a[-1] < b[0]):
            return False
    # The first element of each array is greater than the last.
    elif a[0] > a[-1] and b[0] > b[-1]:
        if (a[-1] > b[0]) or (b[-1] > a[0]):
            return False
    return True


def merge_measurements(ms, mode="trim"):
    # TODO: This probably doesn't work for cases where the points of the X-axis are
    # in descending order.
    # TODO: Add alignment of the adjacent scans.

    # Sort the measurements.
    ms = sorted(ms, key=lambda m: m.x.min())

    # Pad the measurements list.
    ms = [None, *ms, None]

    x, y = [], []

    for i, (p, c, n) in enumerate(zip(ms, ms[1:], ms[2:])):
        ids = []

        # Check if the current measurement overlaps with the previous.
        if p is not None and p.x.max() >= c.x.min():
            logger.info("Measurements %d and %d overlap.", i - 1, i)
            if mode == "trim":
                # The current measurement has a larger step than the previous.
                if np.mean(np.diff(c.x)) > np.mean(np.diff(p.x)):
                    # Save the indices that need to be removed.
                    ids.extend(*np.where(c.x <= p.x.max()))

        # Check if the current measurement overlaps with the next.
        if n is not None and c.x.max() >= n.x.min():
            if mode == "trim":
                # The current measurement has a larger step than the next.
                if np.mean(np.diff(c.x)) > np.mean(np.diff(n.x)):
                    # Save the indices that need to be removed.
                    ids.extend(*np.where(c.x >= n.x.min()))

        if ids:
            logger.info("Removing indices %s from measurement %d.", ids, i)
            x.extend(np.delete(c.x, ids))
            y.extend(np.delete(c.signal, ids))
        else:
            x.extend(c.x)
            y.extend(c.signal)

    return np.array(x), np.array(y)
