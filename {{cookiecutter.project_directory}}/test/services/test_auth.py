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
    # Create a JWT token
    token = authorization_service.create_jwt_token(user_id=user_id)
    # Authenticate the token
    user_info = authentication_service.authenticate_jwt(
        security_scopes=SecurityScopes(), token=token
    )

    assert user_info.user_id == user_id


def test_password_hash(app: FastAPI):
    authentication_service: services.AuthenticationService = (
        app.container.service.authentication_service()
    )

    password = "1234567890"
    # Create a password hash
    password_hash = authentication_service.get_password_hash(password)
    # Verify the password hash
    is_correct = authentication_service.verify_password(password, password_hash)
    assert is_correct is True, "Password hash is not correct"
