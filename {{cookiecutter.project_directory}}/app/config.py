from pydantic import BaseSettings, Field
from functools import lru_cache

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


class Settings(BaseSettings):
    app: Application = Application()

    sentry: Sentry = Sentry()

    jwt: JWT = JWT()


@lru_cache(maxsize=50)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
