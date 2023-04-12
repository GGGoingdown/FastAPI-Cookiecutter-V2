import aioredis
from typing import Dict, Any
from loguru import logger
from tortoise import Tortoise, connections
from dependency_injector import resources

from app.config import settings


#########################################################
#               Redis
#########################################################


def get_redis_url(
    username: str = settings.redis.username,
    password: str = settings.redis.password,
    host: str = settings.redis.host,
    port: str = settings.redis.port,
    db: int = settings.redis.backend_db,
) -> str:
    url = f"redis://{username}:{password}@{host}:{port}/{db}"
    return url


def redis_init(url: str = get_redis_url()) -> aioredis:
    redis_client = aioredis.from_url(
        url,
        encoding="utf-8",
        decode_responses=True,
    )
    return redis_client


async def check_redis_connection(url: str = get_redis_url()) -> bool:
    """
    check redis connection status

    :return: if redis is connected return True, else return False
    :rtype: bool
    """
    redis_client = redis_init(url=url)
    try:
        await redis_client.ping()
        return True
    except Exception as e:
        logger.error(e)
        return False


#########################################################
#               PostgreSQL
#########################################################
db_model_list = ["app.models"]


def get_pg_url(
    username: str = settings.pg.username,
    password: str = settings.pg.password,
    host: str = settings.pg.host,
    port: str = settings.pg.port,
    db: str = settings.pg.db,
    *,
    sqlalchemy_schema: bool = False,
) -> str:
    prefix: str = "postgresql" if sqlalchemy_schema else "postgres"
    url = f"{prefix}://{username}:{password}@{host}:{port}/{db}"
    return url


def get_tortoise_config(db_url: str = get_pg_url()) -> Dict:
    config = {
        "connections": {"default": db_url},
        "apps": {
            "models": {
                "models": [*db_model_list, "aerich.models"],
                "default_connection": "default",
            },
        },
    }
    return config


TORTOISE_ORM = get_tortoise_config()


class DBResource(resources.AsyncResource):
    async def init(self, config: Dict = TORTOISE_ORM) -> None:
        logger.debug("--- Initialize DB resource ---")
        await Tortoise.init(config=config)

    async def shutdown(self, *args: Any, **kwargs: Any):
        logger.debug("--- Shutdown DB resource ---")
        await connections.close_all()


async def check_pg_connection() -> bool:
    """
    check pg connection status

    :return: if pg is connected return True, else return False
    :rtype: bool
    """

    try:
        conn = Tortoise.get_connection("default")
        await conn.execute_query("SELECT 1")
        return True

    except ConnectionRefusedError as e:
        logger.warning(e)
        return False

    except Exception as e:
        logger.warning(e)
        return False
