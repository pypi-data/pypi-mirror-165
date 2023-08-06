import datetime as dt
import logging

from dataclasses import dataclass
from typing import Dict, Optional, Union
import jwt

import requests

logger = logging.getLogger(__name__)


class AuthFlowError(Exception):
    """Generic authentication flow error"""


class UnauthorizedError(AuthFlowError):
    pass


class NoTokensError(AuthFlowError):
    pass


class NoIdTokenError(NoTokensError):
    pass


class NoRefreshTokenError(NoTokensError):
    pass


class InvalidRefreshTokenError(AuthFlowError):
    pass


@dataclass
class TokensResponse:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    token_type: str
    expires_in: int
    scope: Optional[str]


@dataclass
class UnvalidatedTokens:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    scope: str

    @classmethod
    def from_dict(cls, o: Dict):
        return cls(
            access_token=o.get("access_token"),
            id_token=o.get("id_token"),
            refresh_token=o.get("refresh_token"),
            scope=o.get("scope"),
        )


@dataclass
class ValidTokens(UnvalidatedTokens):
    expires_at: int
    issued_at: int

    @classmethod
    def from_unvalidated(cls, creds: UnvalidatedTokens, body: Dict):
        return cls(
            access_token=creds.access_token,
            id_token=creds.id_token,
            refresh_token=creds.refresh_token,
            scope=creds.scope,
            expires_at=body.get("exp"),
            issued_at=body.get("iat"),
        )


class AuthFlow:
    @property
    def access_token(self):
        return self.tokens.access_token

    @property
    def access_token_body(self):
        if self._access_token_body is None:
            raise NoTokensError
        return self._access_token_body

    @property
    def tokens(self):
        if not self._tokens:
            raise NoTokensError

        return self._tokens

    @property
    def expires_at(self):
        return dt.datetime.fromtimestamp(self.tokens.expires_at, dt.timezone.utc)

    @property
    def id_token(self):
        idt = self.tokens.id_token
        if not idt:
            raise NoIdTokenError

        return idt

    @property
    def id_token_body(self):
        if self._id_token_body is None:
            raise NoIdTokenError
        return self._id_token_body

    @property
    def issued_at(self):
        return dt.datetime.fromtimestamp(self.tokens.issued_at, dt.timezone.utc)

    @property
    def refresh_token(self):
        rt = self.tokens.refresh_token
        if not rt:
            raise NoRefreshTokenError

        return rt

    @property
    def refreshable(self):
        try:
            return self.tokens.refresh_token is not None
        except NoTokensError:
            return False

    @property
    def ttl(self):
        return self.expires_at - dt.datetime.now(dt.timezone.utc)

    def __init__(self, domain: str, audience: str, client_id: str, scope: str) -> None:
        self.auth0_domain = domain
        self.auth0_audience = audience
        self.auth0_client_id = client_id
        self.token_scope = scope

        self._tokens: Optional[ValidTokens] = None
        self._access_token_body: Optional[Dict[str, Union[str, int]]] = None
        self._id_token_body: Optional[Dict[str, Union[str, int]]] = None

    def load_tokens(self):
        raise NotImplementedError

    def save_tokens(self, creds: ValidTokens):
        logger.warning(
            "Token is not actually persisted. Override this method to handle persistence"
        )

    def refresh(self, scope: Optional[str] = None, persist=True):
        scope = scope or self.token_scope

        r = requests.post(
            f"https://{self.auth0_domain}/oauth/token",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "client_id": self.auth0_client_id,
                "refresh_token": self.refresh_token,
                "scopes": scope,
            },
        )

        if r.status_code == 200:
            if not persist:
                return self

            self.validate_and_save_tokens(r.json())
            logger.debug(f"Refreshed tokens: {self._tokens}")
            return self

        raise InvalidRefreshTokenError

    def validate_and_save_tokens(self, unvalidated_creds: Dict):
        self.validate_tokens(unvalidated_creds)
        try:
            self.save_tokens(self._tokens)
        except Exception as e:
            logger.error("Error while persisting tokens", exc_info=e)

        return self

    def validate_tokens(self, unvalidated_creds: Dict):
        creds = UnvalidatedTokens.from_dict(unvalidated_creds)
        idt_body: Optional[Dict] = None

        # TODO: validate tokens
        logger.warning("NO TOKEN VALIDATION IMPLEMENTED")
        try:
            at_body = jwt.decode(
                creds.access_token,
                options={"verify_signature": False},
            )

            if creds.id_token:
                idt_body = jwt.decode(
                    creds.id_token,
                    options={"verify_signature": False},
                )
        except Exception as e:
            logger.error("Invalid tokens", exc_info=e)
            raise

        self._access_token_body = at_body
        self._id_token_body = idt_body
        self._tokens = ValidTokens.from_unvalidated(
            creds=creds,
            body=at_body,
        )
        self.token_scope = self._tokens.scope

        return self
