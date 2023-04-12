from celery import shared_task
from typing import Dict, Any
from loguru import logger
from celery.signals import worker_process_init
from sentry_sdk.integrations.celery import CeleryIntegration

from app import __VERSION__
from app.config import settings
from app.services.sentry import sentry_init


def check_broker_connection() -> bool:
    from app.main import celery_app

    try:
        celery_app.broker_connection().ensure_connection(max_retries=3)
        return True
    except Exception:
        return False


# Inititalize
@worker_process_init.connect
def worker_initialize(*args: Any, **kwargs: Any) -> None:
    logger.info("--- Worker initialize ...")
    if settings.sentry.dsn:
        sentry_init(
            dsn=settings.sentry.dsn,
            release_name=settings.app.application_name,
            version=__VERSION__,
            environment=settings.app.environment,
            trace_sample_rates=settings.sentry.trace_sample_rates,
            integrations=[CeleryIntegration()],
        )


@shared_task()
def health_check() -> Dict:
    return {"detail": "ok"}
