from typing import Any, Dict

from fitbit_downloader.config import Config, OAuthConfig
from fitbit_downloader.gather_keys_oauth2 import OAuth2Server
from fitbit_downloader.logger import logger
from fitbit_downloader.models.refreshtokenresponse import RefreshTokenResponse


def initial_client_authorization(config: Config):
    server = OAuth2Server(config.client_id, config.client_secret)
    server.browser_authorize()

    profile = server.fitbit.user_profile_get()
    logger.info(
        "You are authorized to access data for the user: {}".format(
            profile["user"]["fullName"]
        )
    )

    set_authorization(config, server.fitbit.client.session.token)


def set_authorization(config: Config, raw_token_data: Dict[str, Any]):
    token_data = RefreshTokenResponse(**raw_token_data)
    _update_config_with_token_data(config, token_data)
    logger.info(f"Token refreshed. New expiry: {config.oauth_config.expires_at_time}")  # type: ignore
    config.save()


def _update_config_with_token_data(config: Config, token_data: RefreshTokenResponse):
    oauth_config = OAuthConfig(
        access_token=token_data.access_token,
        refresh_token=token_data.refresh_token,
        expires_at=token_data.expires_at,
    )
    config.oauth_config = oauth_config
