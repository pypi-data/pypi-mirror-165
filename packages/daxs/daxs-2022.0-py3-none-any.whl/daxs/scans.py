# coding: utf-8
"""The module provides classes for the representation of scans in measurements."""

import copy
import logging

import numpy as np
import silx

from daxs.filters import hampel
from daxs.utils import arrays_intersect

logger = logging.getLogger(__name__)


class Scan:
    # pylint: disable=no-member, too-many-branches
    """Class to represent a scan group from a HDF5 file."""

    def __init__(self, filename, name, counters, positioners=None):
        """
        Parameters
        ----------
        filename : str
            Name of the HDF5 data file.
        name : str
            Name of the scan.
        counters : dict
            The counters identifying the x-axis, signal, and monitor data.
        positioners : list
            The positioners used to get additional information about the scan.
        """
        self.filename = filename
        self.name = name
        self.title = str()

        self.counters = counters
        if positioners is not None:
            self.positioners = dict.fromkeys(positioners)
        else:
            self.positioners = None

        with silx.io.open(self.filename) as sf:
            measurement = sf[self.name]["measurement"]

            x = measurement[self.counters["x"]][()]

            # If needed, convert the signal counters to a tuple.
            if isinstance(self.counters["signal"], str):
                self.counters["signal"] = (self.counters["signal"],)

            # Read all counters associated with the signal into a 2D array. Each
            # counter is read to a row of the matrix. We assume that the signal
            # from each counter has the same length.
            ncounters = len(self.counters["signal"])
            signal = np.zeros((ncounters, x.size))
            for i, counter in enumerate(self.counters["signal"]):
                if counter not in measurement.keys():
                    raise ValueError(f"Scan {self.name} has no counter {counter}.")
                signal[i, :] = measurement[counter][()]

            if x.size == 0 or signal.size == 0:
                raise ValueError(f"No data available for scan {self.name}.")

            monitor = None
            if "monitor" in self.counters:
                monitor = measurement[self.counters["monitor"]][()]

            # Read additional counters if provided.
            for key, counter in counters.items():
                if key in ("x", "signal", "monitor"):
                    continue
                # These are not critical, so we do not raise an error if they are
                # not found.
                try:
                    values = measurement[counter][()]
                except KeyError:
                    logger.error("Scan %s has no counter %s.", self.name, counter)
                except TypeError:
                    logger.error(
                        "Could not read %s data in scan %s.", counter, self.name
                    )
                else:
                    setattr(self, key, values)

            if self.positioners is not None:
                positioners = sf[self.name]["instrument"]["positioners"]
                for positioner in self.positioners:
                    self.positioners[positioner] = positioners[positioner][()]

            self.title = sf[self.name]["title"][()]
            try:
                self.title = self.title.decode()
            except AttributeError:
                pass

        self._x, self._signal, self._monitor = x, signal, monitor
        self._data = {"_x": x, "_signal": signal, "_monitor": monitor}
        self.outliers, self.medians = None, None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, a):
        # Do nothing when receiving identical values.
        if np.array_equal(self._x, a):
            logger.debug("The new values are the same as the current values.")
            return

        # If the new values are not within the current values, but the two
        # arrays have the same shape, we simply assign the new values to the
        # X-axis. This is useful when the X-axis changes to different units,
        # e.g. angle to energy
        if self._x.shape == a.shape and not arrays_intersect(a, self._x):
            logger.debug("Assigning new X-axis to scan %s.", self.name)
            self._x = np.copy(a)
            return

        if arrays_intersect(a, self._x):
            logger.debug("Interpolating scan %s data.", self.name)
            self.interpolate(a)

    @property
    def signal(self):
        return self._signal.mean(axis=0)

    @property
    def monitor(self):
        return self._monitor

    def reset(self):
        """Reset the scan data to the values read from file."""
        for key, value in self._data.items():
            setattr(self, key, copy.deepcopy(value))

    def find_outliers(self, **kwargs):
        """Find outliers in the signal.

        See the docstring of :func:`daxs.filters.hampel`.
        """
        self.outliers, self.medians = hampel(self._signal, axis=1, **kwargs)

    def remove_outliers(self, **kwargs):
        """Remove outliers from the signal.

        See the docstring of :meth:`daxs.scans.Scan.find_outliers`.
        """
        if self.outliers is None or self.medians is None:
            self.find_outliers(**kwargs)
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
        counters = self.counters["signal"]
        for i, counter in enumerate(counters):
            label = f"{counter}"
            ax.plot(self.x, self._signal[i, :] + i * shift, label=label)
            if self.outliers is not None:
                ids = self.outliers[i, :]
                ax.plot(self.x[ids], self._signal[i, :][ids] + i * shift, "k.")

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
            if not hasattr(self, "detection_time"):
                raise ValueError(
                    "Either the detection time parameter or counter must be set."
                )
            detection_time = getattr(self, "detection_time")
        else:
            detection_time = np.ones_like(self.signal) * detection_time

        if np.any(detection_time == 0):
            raise ValueError("The detection time counter has zero values.")

        tau = np.array(tau)
        if len(self.counters["signal"]) != tau.size:
            raise ValueError(
                "Each signal counter must have a detector dead time (tau) value."
            )

        norm = 1 - ((self._signal / detection_time).T * tau).T
        if np.any(norm == 0):
            raise ValueError("The normalization has zero values.")

        self._signal = self._signal / norm

    def interpolate(self, x):
        """Interpolate the data.

        Parameters
        ----------
        x : numpy.array
            Array used to interpolate the data.
        """
        if self._signal is None:
            raise ValueError

        # The interpolated signal is probably going to have a different size,
        # so we can't change the values in-place, and a new array needs to be
        # initialized.
        ncounters, _ = self._signal.shape
        signal = np.zeros((ncounters, x.size))

        # Sort the raw x-values in ascending order.
        ids = np.argsort(self._x, kind="stable")

        # Interpolate the signal from each counter individually.
        for i, _ in enumerate(self._signal):
            signal[i, :] = np.interp(x, self._x[ids], self._signal[i, :][ids])

        # Interpolate the monitor if needed.
        if self._monitor is not None:
            monitor = np.interp(x, self._x[ids], self._monitor[ids])
            self._monitor = monitor

        self._x = x
        self._signal = signal

    def __truediv__(self, other):
        if isinstance(other, (list, tuple)):
            signal_factor, monitor_factor = other
        elif isinstance(other, Scan):
            signal_factor, monitor_factor = other.signal, other.monitor
        else:
            raise TypeError("Unsupported type for division.")

        self._signal = self._signal / signal_factor
        try:
            self._monitor = self._monitor / monitor_factor
        except TypeError:
            pass

        return self


class Scans:
    """Class to represent a group of scans."""

    def __init__(self, items=None):
        if items is None:
            items = []
        self._items = items
        self._common_xaxis = None

    @property
    def common_xaxis(self):
        """The common X-axis of the scans."""
        if self._common_xaxis is None:

            # If there is a single scan, use its X-axis as the common axis.
            if len(self._items) == 1:
                return self._items[0].x

            start, stop, size = None, None, None
            for scan in self._items:
                x = scan.x
                step = np.abs((x[0] - x[-1]) / (x.size - 1))
                message = (
                    f"X-axis parameters for scan {scan.name}: "
                    f"start = {x[0]:.8f}, stop = {x[-1]:.8f}, step = {step:.8f} "
                    f"number of points = {x.size:d}."
                )
                logger.debug(message)

                if None in [start, stop, size]:
                    start, stop, size = x[0], x[-1], x.size
                    continue

                if x[0] < x[-1]:
                    start = np.min([x[0], start])
                    stop = np.max([x[-1], stop])
                elif x[0] > x[-1]:
                    start = np.max([x[0], start])
                    stop = np.min([x[-1], stop])
                size = np.max([x.size, size])

                x, step = np.linspace(start, stop, size, retstep=True)

            message = (
                f"Common X-axis parameters: "
                f"min = {x.min():.8f}, max = {x.max():.8f}, step = {step:.8f}, "
                f"number of points = {x.size:d}."
            )
            logger.info(message)

            self._common_xaxis = x
        return self._common_xaxis

    def reset(self):
        """Reset the data to default."""
        self._common_xaxis = None

    def append(self, scan):
        """Append the scan to the end."""
        self._items.append(scan)

    def check(self):
        """Sanity check the data in the scans."""
        reference = None
        for scan in self._items:
            if reference is None:
                reference = scan
                continue

            # Check if the number of points between the current scan and the
            # previous scan differs by more than 10%.
            delta = np.abs(scan.x.size - reference.x.size)
            if delta > int(reference.x.size / 10) and reference.x.size != 0:
                message = (
                    f"Scan {scan.name} has {scan.x.size} points. "
                    f"The previous values was {reference.x.size}. "
                    "Please check the scan."
                )
                logger.info(message)

            reference = scan

    def remove(self, scan):
        """Remove the scan from the list."""
        self._items.remove(scan)

    def __iter__(self):
        yield from self._items

    def __len__(self):
        return len(self._items)
