from typing import Dict
from fastapi import HTTPException, status
from fastapi.security import SecurityScopes
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import ValidationError

from app import utils
from app.schema import UserSchema, AuthSchema


class JWTHandler:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    __slots__ = (
        "_secret_key",
        "_algorithm",
        "_expire_minutes",
    )

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        expire_minutes: int = 120,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def decode(self, token: str) -> Dict:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                options={"verify_aud": False},
            )

            return payload

        except JWTError:
            raise self.credentials_exception

    def encode(self, payload: Dict) -> str:
        encoded_jwt = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def create_expired_time(self) -> datetime:
        expried_dt = utils.get_utc_now() + timedelta(minutes=self._expire_minutes)
        return expried_dt


class AuthenticationSelector:
    def __init__(self, jwt: JWTHandler) -> None:
        self.jwt = jwt


################################################
# Authentication
################################################


class AuthenticationService:
    __slots__ = ("_auth_selector",)

    def __init__(
        self,
        auth_selector: AuthenticationSelector,
    ) -> None:
        self._auth_selector = auth_selector

    def authenticate_jwt(
        self, security_scopes: SecurityScopes, token: str
    ) -> UserSchema.UserInfo:
        # Decode JWT
        jwt_payload = self._auth_selector.jwt.decode(token)

        try:
            user = UserSchema.UserInfo(**jwt_payload)
        except ValidationError:
            raise self._auth_selector.jwt.credentials_exception

        # TODO: If you want to check user's scopes, you can use this code.
        # user_scopes = jwt_payload.get("scopes", [])
        # if security_scopes.scopes:
        #     authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        # else:
        #     authenticate_value = "Bearer"

        # for scope in security_scopes.scopes:
        #     if scope not in user_scopes:
        #         raise HTTPException(
        #             status_code=status.HTTP_403_FORBIDDEN,
        #             detail="權限不足",
        #             headers={"WWW-Authenticate": authenticate_value},
        #         )

        return user


################################################
# Authorization
################################################
class AuthorizationService:
    __slots__ = ("_auth_selector",)

    def __init__(
        self,
        auth_selector: AuthenticationSelector,
    ) -> None:
        self._auth_selector = auth_selector

    def get_login_expired_time(self, unit: str = "sec") -> int:
        if unit == "sec":
            return self._auth_selector.jwt._expire_minutes * 60
        return self._auth_selector.jwt._expire_minutes

    def create_jwt_token(self, *, user_id: str) -> str:
        expried_dt = self._auth_selector.jwt.create_expired_time()
        now = utils.get_utc_now()
        payload = jsonable_encoder(
            AuthSchema.JWTPayload(
                sub=user_id, exp=expried_dt.timestamp(), iat=now.timestamp()
            )
        )
        return self._auth_selector.jwt.encode(payload)
