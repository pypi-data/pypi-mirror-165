# coding: utf-8
# pylint: disable=redefined-outer-name

import os

import h5py
import numpy as np
import pytest


@pytest.fixture()
def hdf5_mock_filename(tmp_path_factory):
    path = os.path.join(tmp_path_factory.mktemp("files"), "test.h5")
    with h5py.File(path, driver="core", mode="w") as h5:
        for scan_id in range(1, 6):
            h5.create_dataset(f"{scan_id}.1/title", data="fscan".encode("utf-8"))
            for counter in ["x", "signal", "monitor"]:
                if scan_id not in (1, 2):
                    h5.create_dataset(
                        f"{scan_id}.1/measurement/{counter}", data=np.random.rand(10)
                    )
        h5.create_dataset("2.1/measurement/x", data=np.random.rand(15))
        h5.create_dataset("2.1/measurement/signal", data=np.random.rand(15))
        h5.create_dataset("5.1/measurement/sec", data=np.random.rand(10))
    yield path
    os.remove(path)


@pytest.fixture()
def hdf5_mock_file(hdf5_mock_filename):
    return h5py.File(hdf5_mock_filename, driver="core", mode="r")
