from enum import StrEnum


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
