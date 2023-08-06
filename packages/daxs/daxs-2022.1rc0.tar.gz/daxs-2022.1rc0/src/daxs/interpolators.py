# coding: utf-8
"""The module provides interpolators."""
import logging

import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator

logger = logging.getLogger(__name__)


class Interpolator2D:
    """Two-dimensional interpolator."""

    def __init__(self, x, y, z, kind="linear", fill_value=np.nan):

        """

        Parameters
        ----------
        x : numpy.array
            X-axis values (1-D array)
        y : numpy.array
            Y-axis values (1-D array)
        z : numpy.array
            Data values (1-D array)
        kind : {'nearest', 'linear'}
            The kind of interpolation to use.
        fill_value : float
            Value used to fill in for requested points outside of the convex hull
            of the input points.
        """
        self.x = x
        self.y = y
        self.z = z

        self.kind = kind
        self.fill_value = fill_value

        self._interpolator = None

    @property
    def interpolator(self):
        """The actual interpolator."""
        if self._interpolator is None:
            if self.kind == "nearest":
                interp = NearestNDInterpolator((self.x, self.y), self.z)
            elif self.kind == "linear":
                interp = LinearNDInterpolator((self.x, self.y), self.z, self.fill_value)
            self._interpolator = interp
        return self._interpolator

    def update(self, parameters=None):
        """Update the interpolator parameters."""
        if parameters is None or not parameters:
            return
        for key, value in parameters.items():
            setattr(self, key, value)
        logger.info("The interpolator parameters have been updated.")
        self._interpolator = None

    def __call__(self, *args, **kwargs):
        """Evaluate interpolator."""
        return self.interpolator.__call__(*args, **kwargs)
