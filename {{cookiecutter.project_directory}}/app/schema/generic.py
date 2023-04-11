from pydantic import BaseModel
from enum import Enum


class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEUBG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EnvironmentMode(str, Enum):
    DEV = "dev"
    TEST = "test"
    STAG = "staging"
    PROD = "production"


class DetailResponse(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "some message",
            }
        }
