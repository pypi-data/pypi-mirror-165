from typing import Any, Dict

import fitbit

from fitbit_downloader.authorize import initial_client_authorization, set_authorization
from fitbit_downloader.config import Config, OAuthConfig


def get_client(config: Config) -> fitbit.Fitbit:
    if config.oauth_config is None:
        initial_client_authorization(config)

    def on_refresh_token(raw_token_data: Dict[str, Any]):
        set_authorization(config, raw_token_data)

    oa: OAuthConfig = config.oauth_config  # type: ignore
    return fitbit.Fitbit(
        config.client_id,
        config.client_secret,
        oauth2=True,
        access_token=oa.access_token,
        refresh_token=oa.refresh_token,
        expires_at=oa.expires_at,
        refresh_cb=on_refresh_token,
    )
