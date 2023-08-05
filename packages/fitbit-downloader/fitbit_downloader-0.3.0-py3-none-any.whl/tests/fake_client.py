import datetime
import json

import fitbit

from tests.config import INTRADAY_RESPONSES_FOLDER, RESPONSES_FOLDER


class FakeFitbit(fitbit.Fitbit):
    def __init__(
        self,
        client_id,
        client_secret,
        access_token=None,
        refresh_token=None,
        expires_at=None,
        refresh_cb=None,
        redirect_uri=None,
        system="en_US",
        **kwargs,
    ):
        # Override init as it does weird dynamic things that override
        # some of the methods defined here
        pass

    def intraday_time_series(
        self,
        resource: str,
        base_date="today",
        detail_level="1min",
        start_time=None,
        end_time=None,
    ) -> dict:
        resource_parts = resource.split("/")
        if len(resource_parts) != 2:
            raise ValueError(f"could not parse resource {resource}")
        dataset = resource_parts[1]
        return _load_intraday_response_data(dataset)

    def activities(self, date: datetime.date) -> dict:
        return _load_normal_response_data("activity")

    def get_sleep(self, date: datetime.date) -> dict:
        return _load_normal_response_data("sleep")


def _load_intraday_response_data(name: str) -> dict:
    path = INTRADAY_RESPONSES_FOLDER / f"{name}.json"
    return json.loads(path.read_text())


def _load_normal_response_data(name: str) -> dict:
    path = RESPONSES_FOLDER / f"{name}.json"
    return json.loads(path.read_text())
