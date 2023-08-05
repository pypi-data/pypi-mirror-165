import datetime
import json
from pathlib import Path

import fitbit

from fitbit_downloader.client import get_client
from fitbit_downloader.config import Config
from fitbit_downloader.logger import logger
from tests.config import INTRADAY_RESPONSES_FOLDER, RESPONSES_FOLDER


def download_sample_responses(client: fitbit.Fitbit):
    for activity_type in ("steps", "heart", "elevation", "distance", "floors"):
        activity_str = f"activities/{activity_type}"
        logger.info(f"Downloading {activity_str}")
        out_path = INTRADAY_RESPONSES_FOLDER / f"{activity_type}.json"
        data = client.intraday_time_series(activity_str)
        _write_json(data, out_path)

    logger.info("Downloading sleep")
    sleep_data = client.get_sleep(datetime.date.today())
    sleep_out_path = RESPONSES_FOLDER / "sleep.json"
    _write_json(sleep_data, sleep_out_path)

    logger.info("Downloading activities")
    activity_data = client.activities()  # type: ignore
    activity_out_path = RESPONSES_FOLDER / "activity.json"
    _write_json(activity_data, activity_out_path)


def _write_json(data: dict, path: Path):
    path.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    config = Config.load_recursive()
    client = get_client(config)
    download_sample_responses(client)
