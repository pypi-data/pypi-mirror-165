import sys

import fitbit
import pytest
from freezegun import freeze_time

from fitbit_downloader.config import Config
from fitbit_downloader.download import download_data
from tests.config import DOWNLOAD_INPUT_PATH, GENERATED_PATH
from tests.dirutils import assert_dir_trees_are_equal, reset_generated_path
from tests.fake_client import FakeFitbit


@pytest.fixture(autouse=True)
def fake_fitbit(monkeypatch):
    monkeypatch.setattr(fitbit, "Fitbit", FakeFitbit)


@freeze_time("2021-11-14")
def test_download(config: Config):
    # Temporarily disable on Windows
    if sys.platform == "win32":
        return

    reset_generated_path()
    download_data(config)
    assert_dir_trees_are_equal(GENERATED_PATH, DOWNLOAD_INPUT_PATH)
