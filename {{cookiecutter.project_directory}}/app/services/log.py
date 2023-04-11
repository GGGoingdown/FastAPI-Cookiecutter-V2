import sys
from loguru import logger
from dependency_injector import resources
from typing import Any

# Settings
from app.schema import GenericSchema


class LoggerHandler(resources.Resource):
    def init(
        self,
        application_name: str,
        log_level: GenericSchema.LogLevel = GenericSchema.LogLevel.DEUBG,
        env_mode: GenericSchema.EnvironmentMode = GenericSchema.EnvironmentMode.DEV,
    ) -> None:
        #! WARNING: Logger remove must at the begin of logger initialize !#
        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<green>{time:YYYY-MM-DDTHH:mm:ss}</green> |<y>[{level}]</y> | <e>{file}::{function}::{line}</e> | {message}",
            level=log_level.value,
        )
        logger.info(
            f"--- [{application_name}]::Logger initialize in {env_mode.value} mode success ---"
        )

    def shutdown(self, *args: Any, **kwargs: Any) -> None:
        logger.remove()
