import sentry_sdk
from loguru import logger
from typing import Any
from dependency_injector import resources


class SentryHandler(resources.Resource):
    def init(
        self,
        dsn: str,
        release_name: str,
        version: str,
        environment: str,
        trace_sample_rates: float = 1.0,
    ) -> None:
        logger.info("--- Initial Sentry ---")
        if dsn == "":
            logger.warning("Sentry DSN is empty, Sentry will not be initialized")
            return

        sentry_sdk.init(
            dsn,
            traces_sample_rate=trace_sample_rates,
            release=f"{release_name}@{version}",
            environment=environment,
            server_name=release_name,
        )

    def shutdown(self, *args: Any, **kwargs: Any) -> None:
        pass
