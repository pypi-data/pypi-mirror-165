# coding: utf-8
# pylint: disable=redefined-outer-name

import os

import numpy as np
import pytest

from daxs.measurements import Measurement, Measurement1D, Xes
from daxs.sources import Hdf5Source
from daxs.utils import resources


def test_measurement_init(hdf5_mock_filename):
    with pytest.raises(AssertionError):
        measurement = Measurement(None)
        assert measurement

    data_mappings = {"x": ".1/measurement/x", "signal": ".1/measurement/signal"}
    source = Hdf5Source(hdf5_mock_filename, None, None, data_mappings)

    with pytest.raises(ValueError):
        measurement = Measurement(source)
        _ = measurement.scans

    source = Hdf5Source(hdf5_mock_filename, 3, None, data_mappings)
    measurement = Measurement(source)

    source = Hdf5Source(hdf5_mock_filename, [2, 3], None, data_mappings)
    measurement = Measurement(source)


def test_measurement_remove_scans(hdf5_mock_filename):
    data_mappings = {"x": ".1/measurement/x", "signal": ".1/measurement/signal"}
    source = Hdf5Source(hdf5_mock_filename, [3, 4, 5], None, data_mappings)
    measurement = Measurement(source)

    with pytest.raises(AssertionError):
        measurement.remove_scans()

    indices = [f"{source.filename}/{i}" for i in (3, 4, 5)]
    measurement.remove_scans(indices)


@pytest.fixture()
def hdf5_filename():
    return resources.getfile("pd_foil_la_xanes.h5")


@pytest.fixture()
def data_mappings():
    return {
        "x": ".1/measurement/hdh_angle",
        "signal": [".1/measurement/g09", ".1/measurement/g14"],
    }


def test_measurement_get_scans_common_axis(hdf5_filename, data_mappings):

    source = Hdf5Source(hdf5_filename, included_scans=[3], data_mappings=data_mappings)
    measurement = Measurement(source)
    values = measurement.get_scans_common_axis("x")
    assert np.all(values == getattr(measurement.scans[0], "x"))

    source = Hdf5Source(hdf5_filename, [3, 4, 7, 8, 9], data_mappings=data_mappings)
    measurement = Measurement(source)

    with pytest.raises(ValueError):
        measurement.get_scans_common_axis("x", mode="wrong")

    values = measurement.get_scans_common_axis("x")
    assert values[-1] == pytest.approx(38.72936736)

    values = measurement.get_scans_common_axis("x", mode="union")
    assert values[-1] == pytest.approx(38.72939236)

    values = measurement.get_scans_common_axis("x", sort=True)
    assert values[-1] == pytest.approx(38.72936736)


def test_measurement1d_properties(hdf5_filename, data_mappings):
    source = Hdf5Source(
        hdf5_filename, included_scans=[3, 4, 7], data_mappings=data_mappings
    )
    measurement = Measurement1D(source)
    assert measurement.x[-1] == pytest.approx(38.72936736)
    assert measurement.signal[-1] == pytest.approx(21.1642857)

    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(
        hdf5_filename, included_scans=[3, 4, 7], data_mappings=data_mappings
    )
    measurement = Measurement1D(source)
    assert measurement.monitor[-1] == pytest.approx(167717.885714)

    measurement.process(normalization="area")
    assert measurement.signal[-1] == pytest.approx(0.00128218482)

    measurement.x = np.append(measurement.x, 39.0)
    assert measurement.signal[-1] == pytest.approx(0.000126189795)


def test_measurement1d_aggregate(hdf5_filename, data_mappings):
    # pylint: disable=protected-access
    source = Hdf5Source(hdf5_filename, included_scans=[7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    assert np.all(measurement.x == measurement.scans[0].x)

    measurement.aggregate()
    assert np.all(measurement.signal == measurement.scans[0].signal)

    assert np.all(measurement.signal == measurement.scans[0].signal)

    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_filename, included_scans=[7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    measurement.aggregate()
    assert measurement.signal[-1] == pytest.approx(0.0001546175)

    source = Hdf5Source(
        hdf5_filename, included_scans=[3, 7], data_mappings=data_mappings
    )
    measurement = Measurement1D(source)
    measurement.aggregate(mode="fraction of sums")
    assert measurement.signal[-1] == pytest.approx(0.0001306488)

    measurement.reset()
    measurement.aggregate(mode="sum of fractions")
    assert measurement.signal[-1] == pytest.approx(0.0002612987)

    with pytest.raises(ValueError):
        measurement.aggregate(mode="wrong")


def test_measurement1d_normalize(hdf5_filename, data_mappings):
    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_filename, included_scans=[7], data_mappings=data_mappings)
    measurement = Measurement1D(source)

    with pytest.raises(ValueError):
        measurement.normalize(mode="wrong")

    measurement.normalize(mode="area")
    assert measurement.signal[-1] == pytest.approx(0.0015740913)

    measurement.normalize(mode="maximum")
    assert measurement.signal[-1] == pytest.approx(0.0004231201)

    measurement.reset()
    measurement.normalize(mode="maximum")
    assert measurement.signal[-1] == pytest.approx(0.0004231201)


def test_measurement1d_outliers(hdf5_filename, data_mappings):
    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(
        hdf5_filename, included_scans=[3, 5], data_mappings=data_mappings
    )
    measurement = Measurement1D(source)

    measurement.find_outliers(method="hampel", threshold=2.0)
    outliers = measurement.scans[0].outliers
    assert np.all(np.where(outliers)[1][:2] == [28, 60])

    measurement.reset()
    measurement.remove_outliers(method="hampel", threshold=3.5)
    outliers = measurement.scans[0].outliers
    assert np.all(np.where(outliers)[1][:2] == [123, 284])


def test_measurement1d_dead_time_correction(hdf5_filename, data_mappings):
    data_mappings.update({"detection_time": ".1/measurement/sec"})
    source = Hdf5Source(
        hdf5_filename, included_scans=[3, 5], data_mappings=data_mappings
    )
    measurement = Measurement1D(source)
    with pytest.raises(AssertionError):
        measurement.dead_time_correction()
    measurement.dead_time_correction(tau=[0.1, 0.1])


def test_measurement_1d_save(hdf5_filename, data_mappings):
    source = Hdf5Source(
        hdf5_filename, included_scans=[3, 5], data_mappings=data_mappings
    )
    measurement = Measurement1D(source)
    with pytest.raises(AssertionError):
        measurement.save()
    filename = "test.dat"
    measurement.save(filename)
    assert os.path.isfile(filename)
    os.remove(filename)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_xes_concentration_correction(hdf5_filename, data_mappings):
    source = Hdf5Source(hdf5_filename, included_scans=3, data_mappings=data_mappings)
    measurement = Xes(source)
    measurement.concentration_correction(5)
    assert measurement.signal[0:2] == pytest.approx([1.11283322, 1.18376119])
