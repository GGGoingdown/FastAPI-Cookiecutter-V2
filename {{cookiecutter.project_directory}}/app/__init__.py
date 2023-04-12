#######
#   Application Metadata
#######
__VERSION__ = "{{ cookiecutter.project_version }}"
__TITLE__ = "{{ cookiecutter.project_name }}"
__DESCRIPTION__ = "{{ cookiecutter.project_description }}"
__DOCS_URL__ = None
__ROOT_PATH__ = "/api/v1"
__SERVER_HOST__ = {
    "production": "https://www.gggoingdown.com",
}
##########################################################################################
import celery
from celery import current_app as current_celery_app
from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager

from app.config import settings, CeleryConfiguration


def create_celery() -> celery:
    celery_app = current_celery_app
    celery_app.config_from_object(CeleryConfiguration)

    return celery_app


def add_excepptions(app: FastAPI) -> None:
    from fastapi import Request, status
    from fastapi.responses import JSONResponse
    from asyncio.exceptions import TimeoutError
    from aiohttp.client_exceptions import ClientError

    @app.exception_handler(TimeoutError)
    async def asyncio_timeouterror_handler(request: Request, exc: TimeoutError):
        logger.error(exc)
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": "timeout error"},
        )

    @app.exception_handler(ClientError)
    async def aiohttp_client_exception_handler(request: Request, exc: ClientError):
        logger.error(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
            headers={"X-Error": str(exc)},
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await app.container.service.init_resources()

    yield
    logger.info("Shutting down...")
    await app.container.service.shutdown_resources()


def create_app() -> FastAPI:
    app = FastAPI(
        title=__TITLE__,
        description=__DESCRIPTION__,
        version=__VERSION__,
        docs_url=__DOCS_URL__,
        root_path=__ROOT_PATH__,
        servers=[
            {
                "url": __SERVER_HOST__["production"],
                "description": "Production Server",
            }
        ],
        lifespan=lifespan,
    )

    app.celery_app = create_celery()

    # Create routers
    from app import router

    app.include_router(router.health_router)

    # Create dependency injector application
    import sys
    from app.containers import Application
    from app import security, broker

    container = Application()

    container.config.from_pydantic(settings)
    container.wire(modules=[sys.modules[__name__], security, broker])
    logger.info("Dependency injector application created")
    app.container = container

    add_excepptions(app)

    return app
