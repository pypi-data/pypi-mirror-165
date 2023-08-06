# coding: utf-8
"""The module provides classes to deal with different types of measurements."""

import logging
import re

import numpy as np
import silx.io

from daxs.interpolators import Interpolator2D
from daxs.scans import Scan, Scans

logger = logging.getLogger(__name__)


class Source:
    """Class to represent a source of scans."""

    def __init__(self, filename=None, inclusions=None, exclusions=None):
        """
        Parameters
        ----------
        filename : str
            Name of the HDF5 file.
        inclusions : Union[int,str,list[Union[int,str]]]
            Included scans.
        exclusions : Union[int,str,list[Union[int,str]]]
            Excluded scans.

        Notes
        -----
        The two selections arguments can be an integer, string, or a
        list of integers or strings, e.g [9, "12-16"]. The inclusions argument
        can also be a string that will be used to match the **starting** of the
        command used for the acquisition ("fscan").
        """
        assert filename is not None, "The filename must be specified."
        assert inclusions is not None, "The inclusions argument is required."

        self.filename = filename

        self.inclusions = self.normalize_selections(inclusions)
        self.exclusions = self.normalize_selections(exclusions)

        self.selections = []

        with silx.io.open(filename) as fp:
            for group in fp.values():
                title = group["title"][()]
                try:
                    title = title.decode()
                except AttributeError:
                    pass
                # The group.name is of the form /8.1.
                name = group.name[1:]
                # Skip scans that are not ending in .1.
                if name[-2:] != ".1":
                    continue

                for selection in self.inclusions:
                    if title.startswith(selection) or selection == name:
                        self.selections.append(name)

        if self.exclusions is not None:
            for name in self.exclusions:
                # Remove the excluded scans.
                self.selections = [s for s in self.selections if s != name]
                logger.info("Removed scan %s.", name)

        # Sort the selections.
        remove_channel_idx = lambda s: int(s[:-2])
        self.selections = sorted(self.selections, key=remove_channel_idx)

    @staticmethod
    def normalize_selections(selections):
        """Convert selections to the proper format.

        Parameters
        ----------
        selections : Union[int,str,list[Union[int,str]]]
            Selections used to identify the scans.

        Returns
        -------
        list[str]
            Formatted selections.

        Examples
        --------
        A few examples on how different selections are normalized:

        - 12 to ["12.1",]
        - "12" to ["12.1",]
        - "12-14" to ["12.1", "13.1", "14.1"]
        - ["12", "fscan"] to ["12.1", "fscan"]
        """
        out = []

        if selections is None:
            return out

        if isinstance(selections, (int, str)):
            selections = (selections,)

        add_channel_idx = lambda selection: f"{selection}.1"

        for selection in selections:
            if isinstance(selection, int):
                out.append(add_channel_idx(selection))
            # Search for strings used to select the scans.
            elif isinstance(selection, str):
                if re.search(r"^\d+$", selection):
                    out.append(add_channel_idx(selection))
                elif re.search(r"^\d+\-\d+$", selection):
                    start, stop = selection.split("-")
                    for i in range(int(start), int(stop) + 1):
                        out.append(add_channel_idx(i))
                else:
                    out.append(selection)

        return out


class Measurement:
    """Base class for measurements."""

    def __init__(self, sources=None, counters=None, positioners=None):
        """
        Parameters
        ----------
        sources : Union[Source,list[Source]]
            Sources of scans.
        counters : dict
            Counters used to identify the X-axis, signal, and monitor scan data.
        positioners : list
            Positioners used to get additional information about the scan.
        """
        assert sources is not None, "The sources argument is required."

        self.counters = counters
        self.positioners = positioners

        if isinstance(sources, Source):
            sources = (sources,)

        self.scans = Scans()
        for source in sources:
            for selection in source.selections:
                scan = Scan(source.filename, selection, counters, positioners)
                self.scans.append(scan)

        if len(self.scans) == 0:
            raise ValueError("The measurement has no scans.")

        self.scans.check()
        self._x, self._signal, self._monitor = None, None, None


class Measurement1D(Measurement):
    """Base class for 1D measurements."""

    def __init__(self, sources=None, counters=None):
        super().__init__(sources, counters=counters, positioners=None)

    @property
    def x(self):
        if self._x is None:
            self._x = self.scans.common_xaxis
            for scan in self.scans:
                scan.x = self._x
        return self._x

    @x.setter
    def x(self, a):
        for scan in self.scans:
            scan.x = a
        self._x = a

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

    def find_outliers(self, **kwargs):
        """Find outliers in the data.

        See the docstring of :meth:`.scans.Scan.find_outliers`.
        """
        for _, scan in enumerate(self.scans):
            scan.find_outliers(**kwargs)

    def remove_outliers(self, **kwargs):
        """Remove outliers from the signal.

        See the docstring of :meth:`.scans.Scan.remove_outliers`.
        """
        logger.info("Removing outliers.")
        for scan in self.scans:
            scan.remove_outliers(**kwargs)
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
        # The case of measurements having a single scan.
        if len(self.scans) == 1:
            scan = list(self.scans)[0]
            if scan.monitor is not None:
                self._signal = scan.signal / scan.monitor
                self._monitor = scan.monitor
            else:
                self._signal = scan.signal
            return

        for scan in self.scans:
            if scan.monitor is None:
                logger.info(
                    "No monitor data for scan %s. Setting aggregation mode to sum.",
                    scan.name,
                )
                mode = "sum"

        self._signal = np.zeros_like(self.x)
        if mode != "sum":
            self._monitor = np.zeros_like(self.x)

        for scan in self.scans:
            if mode == "sum":
                self._signal += scan.signal
            else:
                if scan.monitor is None:
                    raise ValueError(f"Scan {scan.name} has no monitor data.")
                if mode == "sum of fractions":
                    self._signal += scan.signal / scan.monitor
                elif mode == "fraction of sums":
                    self._signal += scan.signal
                else:
                    raise ValueError(f"Unknown aggregation mode {mode}.")
                self._monitor += scan.monitor

        if mode == "fraction of sums":
            self._signal = self._signal / self._monitor

        logger.info("The scans data was aggregated using the %s mode.", mode)

    def normalize(self, mode="area"):
        """Normalize the signal.

        Parameters
        ----------
        mode : str
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

    def remove_scans(self, selections=None):
        """Remove scans from the measurement.

        Parameters
        ----------
        selection : Union[str,list[str]]
            Selection of scans to be removed.
        """
        if selections is None:
            return

        selections = Source.normalize_selections(selections)

        for scan in self.scans:
            if scan.name in selections:
                self.scans.remove(scan)

    def reset(self, scans=True):
        """Reset the measurement."""
        self._x, self._signal, self._monitor = None, None, None
        if scans:
            for scan in self.scans:
                scan.reset()
            self.scans.reset()

    def save(self, filename=None, delimiter=","):
        """Save the current x and signal to file.

        Parameters
        ----------
        filename : str
            Name of the output file.
        delimiter : str
            Column delimiter in the output file.
        """
        if filename is None:
            logger.info("Please specify a name for the file.")
            return
        with open(filename, "w", encoding="utf-8") as fp:
            fp.write("# x signal\n")
            data = np.array(list(zip(self.x, self.signal)))
            np.savetxt(fp, data, delimiter=delimiter, fmt="%.6e %.6e")
            logger.info("The data was saved to %s.", filename)


class Xas(Measurement1D):
    """Class to represent a X-ray absorption measurement."""

    def __init__(self, sources=None, counters=None):
        if counters is None:
            counters = {"x": "hdh_energy", "signal": "det_dtc_apd", "monitor": "I02"}
        super().__init__(sources=sources, counters=counters)


class Xes(Measurement1D):
    """Class to represent a X-ray emission measurement."""

    def __init__(self, sources=None, counters=None):
        if counters is None:
            counters = {"x": "xes_en", "signal": "det_dtc_apd", "monitor": "I02"}
        super().__init__(sources=sources, counters=counters)

    def concentration_correction(self, selections):
        """Apply the concentration correction.

        Parameters
        ----------
        selections : list[str]
            Selection of scans used for the concentration correction.
        """
        selections = Source.normalize_selections(selections)

        if len(selections) != len(self.scans):
            message = (
                "The number of concentration correction scans is different than "
                "the number of scans specified initially."
            )
            raise AttributeError(message)

        for scan, selection in zip(self.scans, selections):
            filename = scan.filename
            counters = dict(self.counters)
            counters["x"] = "elapsed_time"
            logger.info("Reading correction scan %s from %s.", selection, filename)
            conc_corr_scan = Scan(filename, selection, counters)
            scan = scan / conc_corr_scan

        # Force signal and monitor reevaluation.
        self._signal = None
        self._monitor = None


class Measurement2D(Measurement):
    """Base class for 2D measurements."""


class Rixs(Measurement2D):
    """Class to represent a resonant inelastic X-ray scattering measurement."""

    def __init__(self, sources=None, counters=None, positioners=None):
        if counters is None:
            counters = {"x": "hdh_energy", "signal": "det_dtc_apd", "monitor": "I02"}
        if positioners is None:
            positioners = ("xes_en",)
        super().__init__(sources=sources, counters=counters, positioners=positioners)
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
        if all("fscan" in scan.title for scan in self.scans):
            return "absorption"
        return "emission"

    def reset(self, scans=True):
        """Reset the measurement."""
        self._x, self._y, self._signal, self._monitor = None, None, None, None
        self._interpolator = None
        self.cuts = {}
        if scans:
            for scan in self.scans:
                scan.reset()
            self.scans.reset()

    def concentration_correction(self, selection):
        """Apply the concentration correction.

        A point in the concentration correction scan is used to correct a scan
        of the plane.

        Parameters
        ----------
        selection : str
            Scan used for the concentration correction.
        """
        selection = Source.normalize_selections(selection)[0]
        filename = list(self.scans)[0].filename
        counters = dict(self.counters)
        counters["x"] = "elapsed_time"

        logger.info("Reading correction scan %s from %s.", selection, filename)
        conc_corr_scan = Scan(filename, selection, counters)

        for i, scan in enumerate(self.scans):
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
                # Get the value of the first positioner.
                value = next(iter(scan.positioners.values()))
                y.extend(value * np.ones_like(scan.x))
                # If present, use the monitor data to normalize the signal.
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
