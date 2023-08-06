# coding: utf-8
# pylint: disable=redefined-outer-name
import copy

import matplotlib.pyplot as plt
import numpy as np
import pytest

from daxs.scans import Scan


def test_scan_init():
    x = np.random.rand(10)
    signal = np.random.rand(10)

    with pytest.raises(AssertionError):
        Scan(None, signal)
    with pytest.raises(AssertionError):
        Scan(x, None)
    with pytest.raises(AssertionError):
        Scan(x, signal[np.newaxis, :, np.newaxis])

    Scan(x, signal)


@pytest.fixture
def scan():
    x = np.array([3, 1, 2, 0, 4], dtype=float)
    signal = np.array([[2, 9, 0, 4, 1], [9, 1, 3, 4, 3]], dtype=float)
    data = {
        "monitor": np.array([1, 1, 2, 4, 2], dtype=float),
        "detection_time": [0.2, 0.2, 0.2, 0.2, 0.2],
        "filename": "No file name",
        "index": 1,
    }
    return Scan(x, signal, data=data)


def test_scan_reset(scan):
    scan.x = np.array([1, 1, 1, 1, 1])
    scan.reset()
    assert scan.x == pytest.approx([0, 1, 2, 3, 4])


def test_scan_properties(scan):
    assert scan.x == pytest.approx([0, 1, 2, 3, 4])
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 5.5, 2.0])
    assert scan.monitor == pytest.approx([4, 1, 2, 1, 2])

    scan.x = np.array([3, 1, 2, 0, 4])
    assert scan.x == pytest.approx([0, 1, 2, 3, 4])
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 5.5, 2.0])

    scan.reset()
    scan.x = np.array([5, 6, 7, 9, 11])
    assert scan.x == pytest.approx([5, 6, 7, 9, 11])
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 5.5, 2.0])

    scan.reset()
    with pytest.raises(ValueError):
        scan.x = np.array([5, 6, 7, 9, 11, 12])

    scan.reset()
    scan.x = np.array([0, 1, 2, 3, 5, 10])
    assert scan.x == pytest.approx([0, 1, 2, 3, 5, 10])
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 5.5, 2.0, 2.0])


def test_scan_interpolate(scan):
    # pylint: disable=protected-access
    scan._signal = None
    with pytest.raises(ValueError):
        scan.interpolate(a=np.random.rand(10))


def test_scan_outliers_removal(scan):
    scan.remove_outliers(method="hampel")
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 2.5, 2.0])


def test_scan_dead_time_correction(scan):
    # pylint: disable=protected-access
    with pytest.raises(AssertionError):
        scan.dead_time_correction()

    tau = np.array([1.0, 1.0, 1.0]) * 1e-3
    with pytest.raises(ValueError):
        scan.dead_time_correction(tau=tau)

    scan.reset()
    tau = np.array([1.0, 1.0]) * 1e-3
    scan.dead_time_correction(tau)
    assert scan.signal == pytest.approx(
        np.array([4.08163265, 5.21455445, 1.52284264, 5.72214289, 2.0253552])
    )

    scan.reset()
    scan._data.pop("detection_time", None)
    with pytest.raises(ValueError):
        scan.dead_time_correction(tau)

    with pytest.raises(ValueError):
        scan.dead_time_correction(tau=tau, detection_time=0.0)

    with pytest.raises(ValueError):
        scan.dead_time_correction(tau=[1.0, 1.0], detection_time=2)


def test_scan_plot(scan):
    _, ax = plt.subplots()
    scan.remove_outliers(method="hampel")
    scan.plot(ax)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_scan_true_div(scan):
    with pytest.raises(TypeError):
        scan1 = scan / (1.0, "b")

    scan1 = copy.deepcopy(scan)
    scan1 = scan1 / 0.5
    assert scan1.signal == pytest.approx(scan.signal / 0.5)

    scan1.reset()
    scan1 = scan1 / (0.4, 0.3)
    assert scan1.signal == pytest.approx(scan.signal / 0.4)
    assert scan1.monitor == pytest.approx(scan.monitor / 0.3)

    scan1.reset()
    scan1 = scan1 / np.array([1, 1, 1, 1, 1])
    assert scan1.signal == pytest.approx(scan.signal)

    scan1.reset()
    scan2 = copy.deepcopy(scan)
    scan2 = scan2 / scan1
    assert scan2.signal[0:2] == pytest.approx([1.0, 1.0])


def test_str(scan):
    assert str(scan) == "No file name/1"
