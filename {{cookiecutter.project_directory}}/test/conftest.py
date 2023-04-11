import pytest
import asyncio
from httpx import AsyncClient
from typing import Iterator, AsyncGenerator
from fastapi import FastAPI

try:
    # Application
    from app import create_app
except ModuleNotFoundError:
    from pathlib import Path
    import sys

    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]  # app folder
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))  # add ROOT to PATH

    from app import create_app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def app(event_loop) -> Iterator[FastAPI]:
    app = create_app()
    yield app
    app.container.unwire()


@pytest.fixture()
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
