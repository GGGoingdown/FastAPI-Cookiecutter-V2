import asyncio
import sys

try:
    from app.config import settings
except ModuleNotFoundError:
    from pathlib import Path

    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]  # app folder
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))  # add ROOT to PATH

    from app.config import settings
    from app.schema import UserSchema
    from app import repositories, services
    from app import models


def get_admin_info() -> UserSchema.CreateUser:
    return UserSchema.CreateUser(
        username=settings.admin.username,
        email=settings.admin.email,
        password=settings.admin.password,
    )


async def create_user(
    user_repo: repositories.UserRepo,
    authentication_service: services.AuthenticationService,
    *,
    user_info: UserSchema.CreateUser,
) -> models.User:
    password_hash = authentication_service.get_password_hash(user_info.password)
    user = await user_repo.create(
        name=user_info.username, email=user_info.email, password_hash=password_hash
    )
    return user


async def main():
    from app.containers import Application
    from loguru import logger

    try:
        container = Application()
        await container.gateway.pg_client.init()

        user_repo: repositories.UserRepo = container.service.user_repo()
        authentication_service: services.AuthenticationService = (
            container.service.authentication_service()
        )
        # Create user
        admin_info = get_admin_info()
        admin_in_db = await create_user(
            user_repo=user_repo,
            authentication_service=authentication_service,
            user_info=admin_info,
        )
        assert admin_in_db is not None, "Admin user not created"
        logger.info("Create user success")

    finally:
        await container.gateway.pg_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
