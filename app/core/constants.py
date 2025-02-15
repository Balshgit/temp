from enum import StrEnum

DEFAULT_REDIS_TIMEOUT = 0.5


class StageEnum(StrEnum):
    production = "production"
    dev = "dev"
    runtests = "runtests"


class LogLevelEnum(StrEnum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    NOTSET = ""
