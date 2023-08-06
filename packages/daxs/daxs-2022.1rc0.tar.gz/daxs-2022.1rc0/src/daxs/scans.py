# coding: utf-8
"""The module provides classes for the representation of scans in measurements."""

import copy
import logging
from typing import Optional

import numpy as np

from daxs.filters import hampel
from daxs.utils import arrays_intersect

logger = logging.getLogger(__name__)


class Scan:
    def __init__(
        self,
        x: np.ndarray,
        signal: np.ndarray,
        data: dict = None,
    ) -> None:

        """
        Base class for the representation of scans in measurements.

        Parameters
        ----------
        x :
            X-axis values (1D array).
        signal :
            Signal values (1D or 2D array). For a 2D array, the components must be
            stored as rows. A 1D array will be converted to a 2D array.
        data :
            Storage for the raw scan data and metadata.
        """
        assert x is not None, "The X-axis values must be set."
        assert signal is not None, "The signal values must be set."

        # Convert the signal to a 2D array.
        if signal.ndim == 1:
            signal = signal[np.newaxis, :]

        assert signal.ndim in (1, 2), "The signal must be a 1D or a 2D array."

        self._x = x
        self._y = None
        self._signal = signal
        self._monitor = None
        self._data = {} if data is None else data

        # Array of indices used to reindex the data.
        self._indices: Optional[np.ndarray] = None

        # Copy the X-axis and signal values.
        for attr in ("x", "signal"):
            self._data[attr] = copy.deepcopy(getattr(self, f"_{attr}"))

        self.outliers, self.medians = None, None

        self.reindex()

    @property
    def x(self):
        if self._x is None:
            self._x = self._data["x"]
        return self._x

    @x.setter
    def x(self, a: np.ndarray) -> None:
        a = np.sort(a, kind="stable")

        # Do nothing when receiving identical values.
        if np.array_equal(self._x, a):
            logger.debug("The new X-axis values are the same as the current ones.")
            return

        if not arrays_intersect(a, self._x):
            if self._x.shape == a.shape:
                # If the new values are not within the current values, but the two
                # arrays have the same shape, we simply assign the new values to the
                # X-axis. This is useful when the X-axis changes to different units,
                # e.g. angle to energy
                logger.debug("Assigning the new X-axis values.")
                self._x = np.copy(a)
                self._indices = None
                return
            raise ValueError(
                "Incompatible values for the new X-axis; outside the current ones "
                "and of different shape."
            )
        self.interpolate(a)

    @property
    def y(self):
        try:
            return self._data["y"]
        except KeyError:
            return None

    @property
    def signal(self):
        if self._signal is None:
            self._signal = self._data["signal"]
        return self._signal.mean(axis=0)

    @property
    def monitor(self):
        if self._monitor is None:
            try:
                self._monitor = self._data["monitor"]
            except KeyError:
                self._monitor = None
        return self._monitor

    @property
    def indices(self):
        return self._indices

    @indices.setter
    def indices(self, a: np.ndarray) -> None:
        assert (
            a.shape == self._x.shape
        ), "The shape of the indices and X-axis arrays must be the same."
        self._indices = a
        self.reset()

    @property
    def filename(self) -> Optional[str]:
        try:
            return self.data["filename"]
        except KeyError:
            return None

    @property
    def index(self) -> Optional[int]:
        try:
            return self.data["index"]
        except KeyError:
            return None

    @property
    def label(self) -> str:
        return f"{self.filename}/{self.index}"

    @property
    def data(self):
        return copy.deepcopy(self._data)

    def reset(self):
        """Reset the scan data to the values read from file."""
        self._x = self._data["x"]
        self._y = None
        self._signal = self.data["signal"]
        self._monitor = None
        self.outliers, self.medians = None, None
        self.reindex()

    def reindex(self):
        if self._indices is None:
            self._indices = np.argsort(self._x, kind="stable")
        self._x = self._x[self._indices]
        self._signal = self._signal[:, self._indices]
        if self.monitor is not None:
            self._monitor = self._monitor[self._indices]

    def find_outliers(self, method="hampel", **kwargs):
        """Find outliers in the signal.

        See the docstring in the :mod:`daxs.filters`.
        """
        if method == "hampel":
            self.outliers, self.medians = hampel(self._signal, axis=1, **kwargs)
        else:
            raise ValueError(f"Unknown method: {method}.")

    def remove_outliers(self, method="hampel", **kwargs):
        """Remove outliers from the signal.

        See the docstring of :meth:`daxs.scans.Scan.find_outliers`.
        """
        if self.outliers is None or self.medians is None:
            self.find_outliers(method=method, **kwargs)
        self._signal = np.where(self.outliers, self.medians, self._signal)

    def plot(self, ax=None, shift=None):
        """Plot the scan data and outliers if available.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes to plot the scan data on.
        shift : float
            Shift the signal by the given value.
        """
        assert ax is not None, "The axes must be provided."
        if shift is None:
            shift = np.mean(self._signal)
        for i, _ in enumerate(self._signal):
            ax.plot(self.x, self._signal[i, :] + i * shift, label=f"{i}")
            if self.outliers is not None:
                indices = self.outliers[i, :]
                ax.plot(self.x[indices], self._signal[i, :][indices] + i * shift, "k.")
            ax.legend()

    def dead_time_correction(self, tau=None, detection_time=None):
        """Perform a dead time correction using a non-paralyzable model.

        Parameters
        ----------
        tau : Iterable
            The detector dead time in seconds.
        detection_time : float
            The time spent on a point of the scan in seconds.
        """
        assert tau is not None, "The detector dead time (tau) must be set."

        if detection_time is None:
            if "detection_time" not in self.data:
                raise ValueError(
                    "Either the detection time parameter or data path must be set."
                )
            detection_time = copy.deepcopy(self._data["detection_time"])
        else:
            detection_time = np.ones_like(self.signal) * detection_time

        if np.any(detection_time == 0):
            raise ValueError("The detection time has zero values.")

        tau = np.array(tau)
        if self._signal.shape[0] != tau.shape[0]:
            raise ValueError(
                "Each signal data path must have a detector dead time (tau) value."
            )

        norm = 1 - ((self._signal / detection_time).T * tau).T
        if np.any(norm == 0):
            raise ValueError("The normalization has zero values.")

        self._signal = self._signal / norm

    def interpolate(self, a):
        """Interpolate the data.

        Parameters
        ----------
        a : numpy.array
            Array used to interpolate the signal and monitor.
        """
        if self._signal is None:
            raise ValueError

        logger.debug(
            "Interpolating the signal and monitor data for scan %s.", self.label
        )

        # The interpolated signal is probably going to have a different size,
        # so we can't change the values in-place, and a new array needs to be
        # initialized.
        signal = np.zeros((self._signal.shape[0], a.size))

        # Interpolate the signal from each counter individually.
        for i, _ in enumerate(self._signal):
            signal[i, :] = np.interp(a, self._x, self._signal[i, :])

        # Interpolate the monitor if present.
        if self._monitor is not None:
            self._monitor = np.interp(a, self._x, self._monitor)

        self._x = a
        self._signal = signal
        self._indices = None

    def __truediv__(self, other):
        """Divide the scan by a scalar, a list/tuple/ndarray, or another scan."""
        if isinstance(other, (int, float)):
            signal_div, monitor_div = other, None
        elif isinstance(other, (list, tuple, np.ndarray)):
            if len(other) == 2:
                signal_div, monitor_div = other
            else:
                signal_div, monitor_div = other, None
        elif isinstance(other, Scan):
            signal_div, monitor_div = other._signal, other._monitor
        else:
            raise ValueError("Unsupported type encounter in division.")

        try:
            self._signal /= signal_div
            if self._monitor is not None and monitor_div is not None:
                self._monitor /= monitor_div
        except (TypeError, ValueError) as e:
            raise type(e)("Cannot divide by the given type.") from e

        return self

    def __str__(self):
        return self.label
