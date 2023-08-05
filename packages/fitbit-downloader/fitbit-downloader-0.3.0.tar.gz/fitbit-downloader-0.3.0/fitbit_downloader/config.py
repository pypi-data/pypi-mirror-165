import datetime
from enum import Enum
from typing import Final, List, Optional

from pyappconf import AppConfig, BaseConfig, ConfigFormats
from pydantic import BaseModel, Field, validator

from fitbit_downloader.logger import add_file_handler

APP_NAME: Final = "fitbit-downloader"


class OAuthConfig(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: float

    @property
    def expires_at_time(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.expires_at)


class Dataset(str, Enum):
    STEPS = "steps"
    HEART = "heart"
    ELEVATION = "elevation"
    DISTANCE = "distance"
    FLOORS = "floors"
    SLEEP = "sleep"
    ACTIVITIES = "activities"


class DownloadConfig(BaseModel):
    datasets: List[Dataset] = Field(
        default_factory=lambda: [
            Dataset.STEPS,
            Dataset.HEART,
            Dataset.ELEVATION,
            Dataset.DISTANCE,
            Dataset.FLOORS,
            Dataset.SLEEP,
            Dataset.ACTIVITIES,
        ]
    )
    fs_url: str = f"osfs://."
    fs_folder: str = "fitbit-data"
    data_begin_date: datetime.date = datetime.date.today()


class Config(BaseConfig):
    client_id: str
    client_secret: str
    oauth_config: Optional[OAuthConfig]
    download: DownloadConfig = DownloadConfig()
    log_to_file: bool = False

    _settings = AppConfig(
        app_name=APP_NAME,
        default_format=ConfigFormats.TOML,
        config_name="fitbit-downloader",
    )

    @validator("log_to_file", always=True)
    def set_log_to_file(cls, v, values):
        if v:
            add_file_handler()
        return v

    class Config:
        env_file = ".env"
        env_prefix = "FITBIT_DOWNLOADER_"


if __name__ == "__main__":
    print(Config.load_recursive().to_toml())
