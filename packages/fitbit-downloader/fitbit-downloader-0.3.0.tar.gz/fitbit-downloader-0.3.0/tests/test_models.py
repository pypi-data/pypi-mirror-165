from pathlib import Path
from typing import Type

from pydantic import BaseModel

from fitbit_downloader.models.activityresponse import ActivityResponse
from fitbit_downloader.models.distanceresponse import DistanceResponse
from fitbit_downloader.models.elevationresponse import ElevationResponse
from fitbit_downloader.models.floorsresponse import FloorsResponse
from fitbit_downloader.models.heartresponse import HeartResponse
from fitbit_downloader.models.refreshtokenresponse import RefreshTokenResponse
from fitbit_downloader.models.sleepresponse import SleepResponse
from fitbit_downloader.models.stepsresponse import StepsResponse
from tests.config import INTRADAY_RESPONSES_FOLDER, RESPONSES_FOLDER


def _model_construction_test(path: Path, model_cls: Type[BaseModel]):
    model_cls.parse_file(path)


def test_elevation_response():
    json_path = INTRADAY_RESPONSES_FOLDER / "elevation.json"
    _model_construction_test(json_path, ElevationResponse)


def test_heart_response():
    json_path = INTRADAY_RESPONSES_FOLDER / "heart.json"
    _model_construction_test(json_path, HeartResponse)


def test_steps_response():
    json_path = INTRADAY_RESPONSES_FOLDER / "steps.json"
    _model_construction_test(json_path, StepsResponse)


def test_distance_response():
    json_path = INTRADAY_RESPONSES_FOLDER / "distance.json"
    _model_construction_test(json_path, DistanceResponse)


def test_floors_response():
    json_path = INTRADAY_RESPONSES_FOLDER / "floors.json"
    _model_construction_test(json_path, FloorsResponse)


def test_sleep_response():
    json_path = RESPONSES_FOLDER / "sleep.json"
    _model_construction_test(json_path, SleepResponse)


def test_activity_response():
    json_path = RESPONSES_FOLDER / "activity.json"
    _model_construction_test(json_path, ActivityResponse)


def test_refresh_token_response():
    json_path = RESPONSES_FOLDER / "refresh-token.json"
    _model_construction_test(json_path, RefreshTokenResponse)
