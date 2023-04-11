from datetime import datetime


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(microsecond=0)
