from pydantic import BaseSettings, Field
from functools import lru_cache
from kombu import Queue

from app.schema import GenericSchema


class Application(BaseSettings):
    environment: GenericSchema.EnvironmentMode = Field(
        GenericSchema.EnvironmentMode.DEV, env="ENVIRONMENT"
    )
    log_level: GenericSchema.LogLevel = Field(
        GenericSchema.LogLevel.DEUBG, env="LOG_LEVEL"
    )
    application_name: str = Field(env="APPLICATION_NAME")


class Sentry(BaseSettings):
    dsn: str = Field("", env="SENTRY_DSN", description="Sentry DSN")
    trace_sample_rates: float = Field(0.1, env="SENTRY_TRACE_SAMPLE_RATES")


class JWT(BaseSettings):
    secret_key: str = Field(env="JWT_SECRET_KEY")
    algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    expire_minutes: int = Field(60, env="JWT_EXPIRE_MINUTE")


class PostgreConfiguration(BaseSettings):
    host: str = Field(env="POSTGRE_HOST")
    port: str = Field(env="POSTGRE_PORT")
    username: str = Field(env="POSTGRE_USERNAME")
    password: str = Field(env="POSTGRE_PASSWORD")
    db: str = Field(env="POSTGRE_DB")


class RedisConfiguration(BaseSettings):
    host: str = Field(env="REDIS_HOST")
    port: str = Field(env="REDIS_PORT")
    username: str = Field(env="REDIS_USERNAME")
    password: str = Field(env="REDIS_PASSWORD")
    backend_db: int = Field(0, env="REDIS_BACKEND_DB")
    result_db: int = Field(1, env="REDIS_RESULT_DB")


class RabbitMQConfiguration(BaseSettings):
    host: str = Field(env="RABBITMQ_HOST")
    port: str = Field(env="RABBITMQ_PORT")
    username: str = Field(env="RABBITMQ_USERNAME")
    password: str = Field(env="RABBITMQ_PASSWORD")


class Admin(BaseSettings):
    username: str = Field("admin", env="ADMIN_USERNAME")
    password: str = Field("admin", env="ADMIN_PASSWORD")
    email: str = Field("admin@gmail.com", env="ADMIN_EMAIL")


class Settings(BaseSettings):
    app: Application = Application()

    sentry: Sentry = Sentry()

    jwt: JWT = JWT()

    pg: PostgreConfiguration = PostgreConfiguration()

    redis: RedisConfiguration = RedisConfiguration()

    rabbitmq: RabbitMQConfiguration = RabbitMQConfiguration()

    admin: Admin = Admin()


@lru_cache(maxsize=50)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


class CeleryConfiguration:
    broker_url = f"amqp://{settings.rabbitmq.username}:{settings.rabbitmq.password}@{settings.rabbitmq.host}:{settings.rabbitmq.port}//"

    result_backend = f"redis://{settings.redis.username}:{settings.redis.password}@{settings.redis.host}:{settings.redis.port}/{settings.redis.result_db}"

    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]

    task_queues = (Queue("p1"), Queue("p2"))
    task_default_queue = "p1"
    task_default_exchange = "Task"
    task_default_exchange_type = "direct"

    worker_send_task_event = False

    task_ignore_result = True

    if settings.app.environment == GenericSchema.EnvironmentMode.TEST:
        task_always_eager = True
