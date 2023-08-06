from dataclasses import dataclass
import logging
import requests

from earthscope_sdk.auth.auth_flow import (
    AuthFlow,
    AuthFlowError,
    UnauthorizedError,
)

logger = logging.getLogger(__name__)


class ClientCredentialsFlowError(AuthFlowError):
    pass


@dataclass
class ClientCredentials:
    client_id: str
    client_secret: str


@dataclass
class GetTokensErrorResponse:
    error: str
    error_description: str


class ClientCredentialsFlow(AuthFlow):
    def __init__(
        self, domain: str, audience: str, client_credentials: ClientCredentials
    ) -> None:
        if not client_credentials or not client_credentials.client_secret:
            raise ValueError("Client secret missing")

        super().__init__(
            domain=domain,
            audience=audience,
            client_id=client_credentials.client_id,
            scope="",
        )

        # Flow management vars
        self._secret = client_credentials.client_secret

    def request_tokens(self):
        r = requests.post(
            f"https://{self.auth0_domain}/oauth/token",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.auth0_client_id,
                "client_secret": self._secret,
                "audience": self.auth0_audience,
            },
        )
        if r.status_code == 200:
            self.validate_and_save_tokens(r.json())
            logger.debug(f"Got tokens: {self.tokens}")
            return self

        if r.status_code == 401:
            err = GetTokensErrorResponse(**r.json())
            if err.error == "access_denied":
                if err.error_description == "Unauthorized":
                    raise UnauthorizedError

        raise ClientCredentialsFlowError
