from fastapi import FastAPI
from fastapi.security import SecurityScopes
from app import services


def test_jwt(app: FastAPI):
    authentication_service: services.AuthenticationService = (
        app.container.service.authentication_service()
    )

    authorization_service: services.AuthorizationService = (
        app.container.service.authorization_service()
    )

    user_id = "1234567890"

    token = authorization_service.create_jwt_token(user_id=user_id)

    user_info = authentication_service.authenticate_jwt(
        security_scopes=SecurityScopes(), token=token
    )

    assert user_info.user_id == user_id
