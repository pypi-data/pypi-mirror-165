import datetime
from typing import Any, Dict, Optional, Type

import fitbit
from fs import open_fs, path
from fs.base import FS
from pydantic import BaseModel

from fitbit_downloader.client import get_client
from fitbit_downloader.config import Config, Dataset
from fitbit_downloader.constants import DATE_FORMAT
from fitbit_downloader.dateutils import yesterday
from fitbit_downloader.logger import logger
from fitbit_downloader.models.activityresponse import ActivityResponse
from fitbit_downloader.models.distanceresponse import DistanceResponse
from fitbit_downloader.models.elevationresponse import ElevationResponse
from fitbit_downloader.models.floorsresponse import FloorsResponse
from fitbit_downloader.models.heartresponse import HeartResponse
from fitbit_downloader.models.sleepresponse import SleepResponse
from fitbit_downloader.models.stepsresponse import StepsResponse


def download_data(config: Config, custom_date: Optional[datetime.date] = None):
    date = custom_date or yesterday()
    logger.info(f"Downloading data for {date}")
    client = get_client(config)
    fs = open_fs(config.download.fs_url)
    if not fs.exists(config.download.fs_folder):
        fs.makedir(config.download.fs_folder)
    for dataset in config.download.datasets:
        logger.info(f"Downloading data for {dataset.value}")
        if dataset in (
            Dataset.STEPS,
            Dataset.HEART,
            Dataset.ELEVATION,
            Dataset.DISTANCE,
            Dataset.FLOORS,
        ):
            _download_intraday_data(dataset, client, config, date, fs)
        elif dataset == Dataset.SLEEP:
            _download_sleep_data(dataset, client, config, date, fs)
        elif dataset == Dataset.ACTIVITIES:
            _download_activity_data(dataset, client, config, date, fs)


def _download_intraday_data(
    dataset: Dataset, client: fitbit.Fitbit, config: Config, date: datetime.date, fs: FS
):
    activity_str = f"activities/{dataset.value}"
    data = client.intraday_time_series(activity_str, base_date=date)
    response_cls = _get_intraday_response_class(dataset)
    out_path = _get_out_path(dataset, config, date, fs)
    _save(out_path, data, response_cls, fs)


def _download_sleep_data(
    dataset: Dataset, client: fitbit.Fitbit, config: Config, date: datetime.date, fs: FS
):
    data = client.get_sleep(date)
    out_path = _get_out_path(dataset, config, date, fs)
    _save(out_path, data, SleepResponse, fs)


def _download_activity_data(
    dataset: Dataset, client: fitbit.Fitbit, config: Config, date: datetime.date, fs: FS
):
    data = client.activities(date=date)  # type: ignore
    out_path = _get_out_path(dataset, config, date, fs)
    _save(out_path, data, ActivityResponse, fs)


def _save(out_path: str, data: Dict[str, Any], response_cls: Type[BaseModel], fs: FS):
    model = response_cls(**data)
    fs.writetext(out_path, model.json(indent=2))


def _get_out_path(dataset: Dataset, config: Config, date: datetime.date, fs: FS) -> str:
    out_folder = path.join(config.download.fs_folder, dataset.value)
    if not fs.exists(out_folder):
        fs.makedir(out_folder)
    out_path = path.join(out_folder, date.strftime(DATE_FORMAT) + ".json")
    return out_path


def _get_intraday_response_class(dataset: Dataset) -> Type[BaseModel]:
    if dataset == Dataset.STEPS:
        return StepsResponse
    if dataset == Dataset.HEART:
        return HeartResponse
    if dataset == Dataset.ELEVATION:
        return ElevationResponse
    if dataset == Dataset.DISTANCE:
        return DistanceResponse
    if dataset == Dataset.FLOORS:
        return FloorsResponse
    raise NotImplementedError(f"need to add handling for intraday {dataset.value}")
