# coding: utf-8
"""The module provides classes to deal with different types of data sources."""

import copy
import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import numpy as np
import silx.io.h5py_utils

from daxs.scans import Scan

logger = logging.getLogger(__name__)


class Selection:
    def __init__(
        self,
        items: Union[int, str, List[int], List[str], List[Union[int, str]]] = None,
    ):
        self.items: Optional[Any] = items
        self.normalize()

    def normalize(self):
        """Convert the items to proper formatting.

        Examples
        --------
        A few examples on how different selection are normalized:

        - 1 to [1,]
        - "1" to [1,]
        - [1, "fscan"] to [1, "fscan"]
        - ["1-3", "fscan"] to [1, 2, 3, "fscan"]
        """
        if self.items is None:
            self.items = []
        elif isinstance(self.items, (int, str)):
            self.items = [self.items]

        items = []
        for item in self.items:
            if isinstance(item, int):
                items.append(item)
            elif isinstance(item, str):
                if re.search(r"^\d+$", item):
                    items.append(int(item))
                elif re.search(r"^\d+\-\d+$", item):
                    start, stop = item.split("-")
                    for i in range(int(start), int(stop) + 1):
                        items.append(i)
                else:
                    items.append(item)
        self.items = items

    def __iter__(self):
        return iter(self.items)


class Source(ABC):
    """Base class for sources of scans."""

    @property
    @abstractmethod
    def filename(self) -> str:
        """The filename of the source."""

    @property
    @abstractmethod
    def scans(self) -> List[Scan]:
        """Return all source scans."""


class Hdf5Source(Source):
    def __init__(
        self,
        filename: str = None,
        included_scans: Any = None,
        excluded_scans: Any = None,
        data_mappings: dict = None,
    ):

        """Class for a HDF5 source of scans

        Parameters
        ----------
        filename :
            Name of the HDF5 file.
        included_scans :
            Selection of included scans.
        excluded_scans :
            Selection of excluded scans.
        data_mappings :
            Mappings between scan attributes (x, signal, monitor, etc.) and paths in
            the HDF5 file.
        """

        self._filename = filename
        self.included_scans = Selection(included_scans)
        self.excluded_scans = Selection(excluded_scans)
        self.data_mappings = data_mappings

        self._scans: List[Scan] = None
        self._selected_scans: List[int] = None

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def selected_scans(self) -> List[int]:
        """The selected scans considering the inclusions and exclusions selections."""
        if self._selected_scans is not None:
            return self._selected_scans

        included_scans, excluded_scans, selected_scans = [], [], []

        with silx.io.h5py_utils.File(self.filename) as fp:

            indices = []

            for group in fp.values():
                title = group["title"][()]

                try:
                    title = title.decode("utf-8")
                except AttributeError as e:
                    raise AttributeError(f"Unable to decode title of {group}.") from e

                # The group.name is of the form /1.1, /1.2, /2.1, etc.
                # The title contains the command executed by the user, e.g.
                # fscan 3.16 3.22 60 0.0002.
                index = int(group.name[1:-2])
                if index in indices:
                    continue
                indices.append(index)

                for item in self.included_scans:
                    if item == index or (
                        isinstance(item, str) and re.search(item, title)
                    ):
                        included_scans.append(index)

                for item in self.excluded_scans:
                    if item == index or (
                        isinstance(item, str) and re.search(item, title)
                    ):
                        excluded_scans.append(index)

        for index in sorted(included_scans):
            if index not in excluded_scans:
                selected_scans.append(index)
            else:
                logger.info("Scan %s/%d was excluded.", self.filename, index)

        self._selected_scans = selected_scans
        logger.debug(
            "The scans %s have been selected from %s.", selected_scans, self.filename
        )
        return self._selected_scans

    @property
    def scans(self):
        """Return the scans."""
        if self._scans is None:
            self._scans = [self.read_scan(index) for index in self.selected_scans]
        return self._scans

    def read_data(self, index: int, data_path: str) -> np.ndarray:
        """Read the data given the scan index and path."""

        data_path = f"{index}{data_path}"

        with silx.io.h5py_utils.File(self.filename) as fp:
            try:
                data = fp[data_path][()]
            except KeyError as e:
                raise KeyError(f"Unable to access {data_path}.") from e
            except TypeError as e:
                raise TypeError(f"Unable to read data from {data_path}.") from e

            if data.size == 0:
                raise ValueError(f"Data from {data_path} is empty.")

        return data

    def read_scan(self, index: int) -> Scan:
        """Return a scan object at the index."""
        assert isinstance(index, int), "The index must be an integer."
        assert (
            self.data_mappings is not None
        ), "The data_mappings attribute must be set."
        assert (
            "x" in self.data_mappings
        ), "The data_mappings attribute must contain an entry for the X-axis values."
        assert (
            "signal" in self.data_mappings
        ), "The data_mappings attribute must contain an entry for the signal values."

        # If needed, convert the signal data paths to a list.
        if isinstance(self.data_mappings["signal"], str):
            self.data_mappings["signal"] = [self.data_mappings["signal"]]

        data: Dict[str, Any] = {}

        x = self.read_data(index, self.data_mappings["x"])

        # Read data from the paths associated with the signal into a 2D
        # array. Each data path is stored into a row. We assume that the
        # signal from each path has the same length.
        n = len(self.data_mappings["signal"])
        signal = np.zeros((n, x.size))
        for i, data_path in enumerate(self.data_mappings["signal"]):
            signal[i, :] = self.read_data(index, data_path)

        # Read additional data paths.
        for key, data_path in self.data_mappings.items():
            if key in ("x", "signal"):
                continue
            # These are not critical, so we do not raise an error if they are
            # not found.
            value = None
            try:
                value = self.read_data(index, data_path)
            except (KeyError, TypeError):
                logger.error(
                    "Could not read data from %s. Setting %s value to None",
                    data_path,
                    key,
                )
            else:
                data[key] = copy.deepcopy(value)

        # Finally, store some metadata.
        data["filename"] = self.filename
        data["index"] = index

        return Scan(x, signal, data)
