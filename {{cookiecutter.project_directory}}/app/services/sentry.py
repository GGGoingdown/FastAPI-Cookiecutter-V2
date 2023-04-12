import sentry_sdk
from loguru import logger
from typing import Any, Optional
from dependency_injector import resources


def sentry_init(
    dsn: str,
    release_name: str,
    version: str,
    environment: str,
    trace_sample_rates: float,
    integrations: Optional[list] = None,
) -> None:
    sentry_sdk.init(
        dsn,
        traces_sample_rate=trace_sample_rates,
        release=f"{release_name}@{version}",
        environment=environment,
        server_name=release_name,
        integrations=integrations,
    )


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

        sentry_init(
            dsn=dsn,
            release_name=release_name,
            version=version,
            environment=environment,
            trace_sample_rates=trace_sample_rates,
        )

    def shutdown(self, *args: Any, **kwargs: Any) -> None:
        pass
