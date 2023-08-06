# coding: utf-8
# pylint: disable=redefined-outer-name
import numpy as np
import pytest

from daxs.filters import hampel
from daxs.sources import Hdf5Source
from daxs.utils import resources


@pytest.fixture
def scans():
    filename = resources.getfile("pd_foil_la_xanes.h5")
    data_mappings = {
        "x": ".1/measurement/hdh_angle",
        "signal": [".1/measurement/g09", ".1/measurement/g14"],
    }
    source = Hdf5Source(filename, included_scans=5, data_mappings=data_mappings)
    yield from source.scans


@pytest.mark.parametrize("indices, values", [(69, 14111.5)])
def test_hampel(scans, indices, values):
    outliers, medians = hampel(scans.signal, window_size=5, threshold=3.5, axis=0)
    assert outliers[indices]
    assert medians[indices] == pytest.approx(values, abs=np.finfo(float).eps)

    outliers, medians = hampel(scans.signal, window_size=4, threshold=3.5, axis=0)
    assert outliers[indices]
