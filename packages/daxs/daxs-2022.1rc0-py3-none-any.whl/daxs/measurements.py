# coding: utf-8
"""The module provides classes to deal with different types of measurements."""

import copy
import logging
from typing import Any, Dict, List, Union

import numpy as np

from daxs.interpolators import Interpolator2D
from daxs.scans import Scan
from daxs.sources import Hdf5Source, Source

logger = logging.getLogger(__name__)


class Measurement:
    """Base class for measurements."""

    def __init__(self, sources: Union[Source, List[Source]] = None):
        """
        Parameters
        ----------
        sources :
            Sources of scans.
        """
        assert sources is not None, "The sources argument is required."

        if isinstance(sources, Source):
            sources = [sources]
        self.sources = sources

        self._scans: Any = None
        self._x, self._signal, self._monitor = None, None, None

    @property
    def scans(self) -> List[Scan]:
        """The scans of the measurement."""
        if self._scans is None:
            scans: List[Scan] = []
            for source in self.sources:
                scans.extend(source.scans)

            if len(scans) == 0:
                raise ValueError("The measurement has no scans.")

            # Sanity check the scans.
            reference = None
            for scan in scans:
                if reference is None:
                    reference = scan
                    continue

                # Check if the number of points between the current scan and the
                # previous scan differs by more than 10%.
                delta = np.abs(scan.x.size - reference.x.size)
                if delta > int(reference.x.size / 10) and reference.x.size != 0:
                    message = (
                        f"Scan {scan.label} has {scan.x.size} points. "
                        f"The previous value from {reference.label} "
                        f"was {reference.x.size}. Please check the scans."
                    )
                    logger.warning(message)

                reference = scan

            self._scans = scans
        return self._scans

    def get_scans_common_axis(
        self, axis: str = "x", mode: str = "intersection", sort: bool = False
    ) -> np.ndarray:
        """The common axis of the scans in the measurement."""
        # If there is a single scan, use its axis as the common axis.
        if len(self.scans) == 1:
            [scan] = self.scans
            return getattr(scan, axis)

        start, stop, size = None, None, None
        for scan in self.scans:
            a = getattr(scan, axis)

            step = np.abs((a[0] - a[-1]) / (a.size - 1))
            message = (
                f"{axis.upper()}-axis parameters for scan {scan.label}: "
                f"start = {a[0]:.8f}, stop = {a[-1]:.8f}, step = {step:.8f} "
                f"number of points = {a.size:d}."
            )
            logger.debug(message)

            if None in [start, stop, size]:
                start, stop, size = a[0], a[-1], a.size
                continue

            if sort:
                a = np.sort(a, kind="stable")

            if mode == "intersection":
                start = max(start, a[0])
                stop = min(stop, a[-1])
            elif mode == "union":
                start = min(start, a[0])
                stop = max(stop, a[-1])
            else:
                raise ValueError(f"Unknown mode: {mode}.")

            size = np.max([a.size, size])

            a, step = np.linspace(start, stop, size, retstep=True)

        message = (
            f"Common axis parameters using {mode} mode: "
            f"min = {a.min():.8f}, max = {a.max():.8f}, step = {step:.8f}, "
            f"number of points = {a.size:d}."
        )
        logger.info(message)
        return a

    def remove_scans(self, indices: Union[int, List[int]] = None) -> None:
        """Remove scans from the measurement.

        Parameters
        ----------
        indices :
            Indices of the scans to be removed.
        """
        assert indices is not None, "The indices argument is required."

        if isinstance(indices, int):
            indices = [indices]

        for index in indices:
            for scan in self.scans:
                if index == scan.index:
                    self.scans.remove(scan)
                    logger.debug("Scan %s was removed.", scan.label)
                    self._signal, self._monitor = None, None


class Measurement1D(Measurement):
    """Base class for 1D measurements."""

    @property
    def x(self):
        if self._x is None:
            self._x = self.get_scans_common_axis()
            # Assign the common axis to the scans.
            for scan in self.scans:
                scan.x = self._x
        return self._x

    @x.setter
    def x(self, a):
        logger.info("Setting new x-axis.")
        for scan in self.scans:
            scan.x = a
        self._x = a
        self._signal, self._monitor = None, None

    @property
    def signal(self):
        if self._signal is None:
            self.process()
        return self._signal

    @property
    def monitor(self):
        if self._monitor is None:
            self.process()
        return self._monitor

    def find_outliers(self, method="hampel", **kwargs):
        """Find outliers in the data.

        See the docstring of :meth:`.scans.Scan.find_outliers`.
        """
        for _, scan in enumerate(self.scans):
            scan.find_outliers(method=method, **kwargs)

    def remove_outliers(self, method="hampel", **kwargs):
        """Remove outliers from the signal.

        See the docstring of :meth:`.scans.Scan.remove_outliers`.
        """
        logger.info("Removing outliers.")
        for scan in self.scans:
            scan.remove_outliers(method=method, **kwargs)
        self._signal = None

    def process(self, aggregation="fraction of sums", normalization=None):
        """Process the scans data.

        The processing includes aggregating the data of the selected scans
        and normalizing the signal.
        """
        self.aggregate(mode=aggregation)
        if normalization is not None:
            self.normalize(mode=normalization)

    def aggregate(self, mode="fraction of sums"):
        # pylint: disable=too-many-branches
        """Aggregate the scans signal using the selected mode. When present, the
        aggregated monitor is always a sum of the monitors from the individual scans.

        Parameters
        ----------
        mode : str
            Defines how the signal is aggregated.

                - "sum" : Sum of the signals from all scans.
                - "fraction of sums" : Fraction of the signals sum and monitors sum.
                - "sum of fractions" : Sum of the signal and monitor fractions.
        """
        for scan in self.scans:
            if scan.monitor is None:
                logger.info(
                    "No monitor data for scan %s. Setting aggregation mode to sum.",
                    scan.label,
                )
                mode = "sum"

        self._signal = np.zeros_like(self.x)
        if mode != "sum":
            self._monitor = np.zeros_like(self.x)

        for scan in self.scans:
            if mode == "sum":
                self._signal += scan.signal
            elif mode == "sum of fractions":
                self._signal += scan.signal / scan.monitor
            elif mode == "fraction of sums":
                self._signal += scan.signal
            else:
                raise ValueError(f"Unknown aggregation mode {mode}.")
            if mode != "sum":
                self._monitor += scan.monitor

        if mode == "fraction of sums":
            self._signal = self._signal / self._monitor

        logger.info("The scans data was aggregated using the %s mode.", mode)

    def normalize(self, mode: str = "area") -> None:
        """Normalize the signal.

        Parameters
        ----------
        mode :
            Defines how the signal is normalized.

              - "area": Normalize using the absolute signal area calculated using the
                trapezoidal rule.
              - "maximum": Normalize using the absolute maximum intensity of the signal.

        Notes
        -----
        This will overwrite the original signal with the normalized one.
        """
        assert mode is not None, "The mode has to be defined."

        if self._signal is None:
            self.aggregate()

        if mode == "area":
            self._signal = self._signal / np.abs(np.trapz(self._signal, self.x))
        elif mode == "maximum":
            self._signal = self._signal / np.abs(np.max(self._signal))
        else:
            raise ValueError(f"Unknown normalization mode {mode}.")

        logger.info("The signal was normalized using the %s.", mode)

    def dead_time_correction(self, tau=None, detection_time=None):
        """Perform a dead time correction using a non-paralyzable model.

        See the docstring of :meth:`.scans.Scan.dead_time_correction`.
        """
        assert tau is not None, "The detector dead time (tau) must be set."
        for scan in self.scans:
            scan.dead_time_correction(tau, detection_time)

    def reset(self, scans=True):
        """Reset the measurement."""
        self._x, self._signal, self._monitor = None, None, None
        if scans:
            for scan in self.scans:
                scan.reset()

    def save(self, filename=None, delimiter=","):
        """Save the current x and signal to file.

        Parameters
        ----------
        filename : str
            Name of the output file.
        delimiter : str
            Column delimiter in the output file.
        """
        assert filename is not None, "The filename argument is required."
        with open(filename, "w", encoding="utf-8") as fp:
            fp.write("# x signal\n")
            data = np.array(list(zip(self.x, self.signal)))
            np.savetxt(fp, data, delimiter=delimiter, fmt="%.6e %.6e")
            logger.info("The data was saved to %s.", filename)


class Xas(Measurement1D):
    """Class to represent a X-ray absorption measurement."""


class Xes(Measurement1D):
    """Class to represent a X-ray emission measurement."""

    def concentration_correction(
        self,
        indices: Union[int, List[int]] = None,
        data_mappings: Dict[str, Any] = None,
        scans: Union[Scan, List[Scan]] = None,
    ) -> None:
        """Apply the concentration correction using data from the specified scans.

        Parameters
        ----------
        indices :
            Indices of the scans used for concentration correction.
        data_mappings :
            Mappings used to retrieve the data of the concentration correction scans.
        scans :
            Scans used for concentration corrections.
        """
        assert (
            indices is not None or scans is not None
        ), "Either the indices or scans must be specified."

        conc_corr_scans: List[Scan] = []

        if indices is not None:
            if isinstance(indices, int):
                indices = [indices]

            if len(self.sources) != 1:
                raise ValueError(
                    "The concentration correction scans are specified using indices, "
                    "but there are more than one source in the measurement."
                )
            [source] = self.sources

            if not isinstance(source, Hdf5Source):
                raise ValueError(
                    "Indices can not be used to identify scans in the source."
                )

            if data_mappings is None:
                data_mappings = {"x": ".1/measurement/elapsed_time"}
            original_data_mappings = copy.deepcopy(source.data_mappings)
            source.data_mappings.update(data_mappings)

            # Extract the concentration correction scans.
            for index in indices:
                conc_corr_scans.append(source.read_scan(index))

            # Change back the data mappings.
            source.data_mappings.update(original_data_mappings)

        elif scans is not None:
            if isinstance(scans, Scan):
                scans = [scans]

            for scan in scans:
                conc_corr_scans.extend(scans)

        if len(self.scans) != len(conc_corr_scans):
            raise AttributeError(
                "The number of concentration correction scans is different than "
                "the number of measurement scans."
            )

        for scan, conc_corr_scan in zip(self.scans, conc_corr_scans):
            # Signal data in the concentration correction scan must be sorted using
            # the same order as the one from the scan that is being corrected. The
            # assignment does that.
            conc_corr_scan.indices = copy.deepcopy(scan.indices)
            scan = scan / conc_corr_scan

        # Force signal and monitor reevaluation.
        self._signal, self._monitor = None, None


class Measurement2D(Measurement):
    """Base class for 2D measurements."""


class Rixs(Measurement2D):
    """Class to represent a resonant inelastic X-ray scattering measurement."""

    def __init__(self, sources=None):
        super().__init__(sources=sources)
        self._x, self._y, self._signal, self._monitor = None, None, None, None
        self._interpolator = None
        self.cuts = {}

    @property
    def x(self):
        if self._x is None:
            self.process()
        return self._x

    @property
    def y(self):
        if self._y is None:
            self.process()
        return self._y

    @property
    def signal(self):
        if self._signal is None:
            self.process()
        return self._signal

    @property
    def interpolator(self):
        """The interpolator of the current plane."""
        if self._interpolator is None:
            self._interpolator = Interpolator2D(self.x, self.y, self.signal)
        return self._interpolator

    @property
    def acquisition_mode(self):
        """There are two ways to measure a RIXS plane:

        1. Step through a range of emission energies and scan the incoming
           (monochromator) energy for each step.
        2. Step through incoming (monochromator) energy and scan the emission energy.
        """
        if all(isinstance(scan.y, (int, float)) for scan in self.scans):
            mode = "absorption"
        else:
            mode = "emission"
        logger.debug("The RIXS plane was acquired in %s mode.", mode)
        return mode

    def reset(self, scans=True):
        """Reset the measurement."""
        self._x, self._y, self._signal, self._monitor = None, None, None, None
        self._interpolator = None
        self.cuts = {}
        if scans:
            for scan in self.scans:
                scan.reset()

    def concentration_correction(
        self,
        index: int = None,
        data_mappings: Dict[str, Any] = None,
        scan: Scan = None,
    ) -> None:
        """Apply the concentration correction.

        A point in the concentration correction scan is used to correct a scan
        of the plane.

        Parameters
        ----------
        index :
            Index of the scan used for concentration correction.
        data_mappings:
            Mappings used to retrieve the data of the concentration correction scan.
        scan:
            Scan used for concentration corrections.
        """

        assert (
            index is not None or scan is not None
        ), "Either the index or scan must be specified."

        conc_corr_scan: Scan = None

        if index is not None:
            if len(self.sources) != 1:
                raise ValueError(
                    "The concentration correction scans are specified using indices, "
                    "but there are more than one source in the measurement."
                )
            [source] = self.sources

            if not isinstance(source, Hdf5Source):
                raise ValueError(
                    "Indices can not be used to identify scans in the source."
                )

            if data_mappings is None:
                data_mappings = {"x": ".1/measurement/elapsed_time"}
            original_data_mappings = copy.deepcopy(source.data_mappings)
            source.data_mappings.update(data_mappings)

            conc_corr_scan = source.read_scan(index)

            # Change back the data mappings.
            source.data_mappings.update(original_data_mappings)

        elif scan is not None:
            assert isinstance(scan, Scan), "Received invalid type for the scan."

            conc_corr_scan = scan

        if conc_corr_scan is None:
            raise ValueError("Invalid type for the concentration correction scan.")

        assert len(self.scans) == len(conc_corr_scan.signal), (
            "The number of points in the concentration correction ",
            "scan is not equal to the number of scans in the measurement.",
        )

        for i, scan in enumerate(self.scans):  # pylint: disable=all
            scan = scan / (conc_corr_scan.signal[i], conc_corr_scan.monitor[i])

        self.reset(scans=False)

    def process(self):
        """Read and store the scans data."""
        acquisition_mode = self.acquisition_mode

        if acquisition_mode == "emission":
            raise NotImplementedError("The emission mode is not implemented yet.")

        x, y, signal = [], [], []

        if acquisition_mode == "absorption":
            for scan in self.scans:
                x.extend(scan.x)
                y.extend(scan.y * np.ones_like(scan.x))
                if scan.monitor is not None:
                    signal.extend(scan.signal / scan.monitor)
                else:
                    signal.extend(scan.signal)

            # Convert to arrays.
            x = np.array(x)
            y = np.array(y)
            signal = np.array(signal)

            # Convert to energy transfer.
            y = x - y

        self._x, self._y, self._signal = x, y, signal

    def interpolate(self, xi=None, yi=None):
        """Interpolate the plane using new axes.

        Parameters
        ----------
        xi : numpy.array
            The new X-axis.
        yi : numpy.array
            The new Y-axis.
        """
        if xi is None or yi is None:
            logger.info("Please specify both function arguments.")
            return

        xi, yi = np.meshgrid(xi, yi)
        signal = self.interpolator(xi, yi)

        # Flatten arrays for storage.
        signal = signal.ravel()
        x = xi.ravel()
        y = yi.ravel()

        # Remove NaNs.
        mask = np.isfinite(signal)
        x = x[mask]
        y = y[mask]
        signal = signal[mask]

        # Assign the values.
        self._x, self._y, self._signal = x, y, signal

        # Update the interpolator.
        self.interpolator.update({"x": x, "y": y, "z": signal})

    def cut(self, mode="CEE", energies=None, npoints=1024):
        """Calculate the cuts specified by the mode and energies.

        Parameters
        ----------
        mode : str
            Defines the way to cut the plane:

            - "CEE" - constant emission energy
            - "CIE" - constant incident energy
            - "CET" - constant energy transfer

        energies : list(float)
            Energies of the cuts.

        npoints : int
            Number of points for the cuts.
        """
        assert energies is not None, "The energies parameter must be defined."

        mode = mode.upper()

        # Update the xc and yc arrays depending on the type of cut.
        for energy in energies:
            xc = np.linspace(self.x.min(), self.x.max(), npoints)
            yc = np.linspace(self.y.min(), self.y.max(), npoints)

            if mode == "CEE":
                yc = xc - np.ones_like(xc) * energy
            elif mode == "CIE":
                xc = np.ones_like(yc) * energy
            elif mode == "CET":
                yc = np.ones_like(xc) * energy

            points = np.stack((xc, yc), axis=-1)
            signal = self.interpolator(points)

            if np.isnan(signal).all():
                logger.info("The %s cut at %s is empty.", mode, energy)
                continue

            # Remove NaNs.
            mask = np.isfinite(signal)
            xc = xc[mask]
            yc = yc[mask]
            signal = signal[mask]

            label = f"{mode.upper()}@{energy}"
            self.cuts[label] = (xc, yc, signal)
