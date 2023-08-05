import datetime

from fitbit_downloader.check_upload import (
    begin_date_based_on_config_and_last_full_upload,
)
from fitbit_downloader.config import Config
from fitbit_downloader.dateutils import yesterday
from fitbit_downloader.download import download_data


def sync_data(config: Config):
    begin_date = begin_date_based_on_config_and_last_full_upload(config)
    delta = yesterday() - begin_date

    for i in range(1, delta.days + 1):
        day = begin_date + datetime.timedelta(days=i)
        download_data(config, day)


def main():
    config = Config.load_recursive()
    sync_data(config)


if __name__ == "__main__":
    main()
