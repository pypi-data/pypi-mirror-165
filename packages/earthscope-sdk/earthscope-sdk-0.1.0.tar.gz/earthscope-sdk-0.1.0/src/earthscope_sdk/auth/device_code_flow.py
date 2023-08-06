import logging
import requests

from dataclasses import dataclass
from enum import Enum
from time import sleep
from typing import Optional

from earthscope_sdk.auth.auth_flow import AuthFlow


logger = logging.getLogger(__name__)


class PollingErrorType(str, Enum):
    AUTHORIZATION_PENDING = "authorization_pending"
    SLOW_DOWN = "slow_down"
    EXPIRED_TOKEN = "expired_token"
    ACCESS_DENIED = "access_denied"


class RequestDeviceTokensError(RuntimeError):
    pass


class PollingError(ValueError):
    pass


class PollingExpiredError(PollingError):
    pass


class PollingAccessDeniedError(PollingError):
    pass


@dataclass
class GetDeviceCodeResponse:
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


@dataclass
class PollingErrorResponse:
    error: PollingErrorType
    error_description: str


class DeviceCodeFlow(AuthFlow):
    @property
    def polling(self):
        return self._is_polling

    @property
    def started(self):
        return self._device_codes is not None

    def __init__(self, domain: str, audience: str, client_id: str, scope: str) -> None:
        super().__init__(
            domain=domain,
            audience=audience,
            client_id=client_id,
            scope=scope,
        )

        # Flow management vars
        self._is_polling = False
        self._device_codes: Optional[GetDeviceCodeResponse] = None

    def do_flow(self):
        self.request_device_code()
        self.prompt_user()
        self.poll()
        return self.tokens

    def poll(self):
        if not self._device_codes:
            raise PollingError("Cannot poll without initial device code response")

        if self._is_polling:
            raise PollingError("Attempted to double poll")

        self._is_polling = True
        try:
            while True:
                sleep(self._device_codes.interval)

                r = requests.post(
                    f"https://{self.auth0_domain}/oauth/token",
                    headers={"content-type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        "device_code": self._device_codes.device_code,
                        "client_id": self.auth0_client_id,
                    },
                )
                if r.status_code == 200:
                    tokens = self.validate_and_save_tokens(r.json())
                    logger.debug(f"Got tokens: {tokens}")
                    return self

                poll_err = PollingErrorResponse(**r.json())
                if poll_err.error in [
                    PollingErrorType.AUTHORIZATION_PENDING,
                    PollingErrorType.SLOW_DOWN,
                ]:
                    continue

                if poll_err.error == PollingErrorType.EXPIRED_TOKEN:
                    raise PollingExpiredError

                if poll_err.error == PollingErrorType.ACCESS_DENIED:
                    raise PollingAccessDeniedError

                if poll_err:
                    raise PollingError(f"Unknown polling error: {poll_err}")
        finally:
            self._is_polling = False

    def prompt_user(self):
        raise NotImplementedError(
            "This class cannot prompt a user. Create a subclass that implements this method."
        )

    def request_device_code(self):
        r = requests.post(
            f"https://{self.auth0_domain}/oauth/device/code",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "client_id": self.auth0_client_id,
                "scope": self.token_scope,
                "audience": self.auth0_audience,
            },
        )
        if r.status_code == 200:
            self._device_codes = GetDeviceCodeResponse(**r.json())
            logger.debug(f"Got device code response: {self._device_codes}")
            return self

        raise RequestDeviceTokensError(f"Failed to get a device code: {r.text}")
