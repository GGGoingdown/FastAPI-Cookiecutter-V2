import sys
import asyncio
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_fixed
from loguru import logger

try:
    from app import db, broker
except ModuleNotFoundError:
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]  # app folder
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))  # add ROOT to PATH

    from app import db, broker


max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds))
async def db_connected():
    logger.info("Checking database connection...")
    if not await db.check_pg_connection():
        raise ConnectionError("Database connection failed")


@retry(stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds))
async def cache_connecttion():
    logger.info("Checking cache connection...")
    if not await db.check_redis_connection():
        raise ConnectionError("Cache connection failed")


@retry(stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds))
def broker_connecttion():
    logger.info("Checking broker connection...")
    if not broker.check_broker_connection():
        raise ConnectionError("Cache connection failed")


async def main():
    from app.containers import Application

    try:
        container = Application()
        await container.gateway.pg_client.init()

        await db_connected()
        await cache_connecttion()
        broker_connecttion()
    finally:
        await container.gateway.pg_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
