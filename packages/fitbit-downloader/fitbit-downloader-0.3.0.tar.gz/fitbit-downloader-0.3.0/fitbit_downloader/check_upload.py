import datetime

from fs import open_fs, path

from fitbit_downloader.config import Config, Dataset
from fitbit_downloader.constants import DATE_FORMAT


def begin_date_based_on_config_and_last_full_upload(config: Config) -> datetime.date:
    fs = open_fs(config.download.fs_url)
    if not fs.exists(config.download.fs_folder):
        # No existing data at all, start from begin date
        return config.download.data_begin_date
    dates = [_last_uploaded(dataset, config) for dataset in config.download.datasets]
    if not dates:
        # Folder existed but no downloaded data, start from begin date
        return config.download.data_begin_date
    last_downloaded = min(dates)
    # If last downloaded is before begin date, use begin date
    return max(last_downloaded, config.download.data_begin_date)


def _last_uploaded(dataset: Dataset, config: Config) -> datetime.date:
    fs = open_fs(config.download.fs_url)
    out_folder = path.join(config.download.fs_folder, dataset.value)
    if not fs.exists(out_folder):
        # No existing data at all, start from begin date
        return config.download.data_begin_date
    dates = [_file_to_date(file) for file in fs.listdir(out_folder)]
    return max(dates)


def _file_to_date(file: str) -> datetime.date:
    name, ext = file.split(".")
    if ext != "json":
        raise ValueError(f"got unexpected file {file}")
    dt = datetime.datetime.strptime(name, DATE_FORMAT)
    return dt.date()
